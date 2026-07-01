import time
import logging
import argparse
import json
import csv
import threading
from datetime import datetime
from collections import defaultdict
from pathlib import Path

from scapy.all import (
    sniff, ARP, Ether, IP, TCP, UDP, DNS, DNSQR,
    get_if_list, conf, send, srp
)

# ─────────────────────────────────────────────
#  LOGGING
# ─────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("arp_sniffer.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("ARP-Sniffer")

# ─────────────────────────────────────────────
#  ARP TABLE + SPOOF DETECTION
# ─────────────────────────────────────────────

class ARPTable:
    def __init__(self):
        self._table: dict[str, str] = {}          # ip → mac
        self._conflicts: list[dict] = []
        self._lock = threading.Lock()

    def check_and_update(self, ip: str, mac: str) -> dict | None:
        mac = mac.lower()
        with self._lock:
            if ip in self._table:
                known_mac = self._table[ip]
                if known_mac != mac:
                    conflict = {
                        "timestamp": datetime.now().isoformat(),
                        "ip": ip,
                        "known_mac": known_mac,
                        "new_mac": mac,
                        "severity": self._severity(ip),
                    }
                    self._conflicts.append(conflict)
                    return conflict
            else:
                self._table[ip] = mac
        return None

    def _severity(self, ip: str) -> str:
        octets = ip.split(".")
        if octets[-1] in ("1", "254"):
            return "CRITICAL"   # likely gateway
        return "HIGH"

    def get_table(self) -> dict:
        with self._lock:
            return dict(self._table)

    def get_conflicts(self) -> list:
        with self._lock:
            return list(self._conflicts)

    def load_baseline(self, path: str):
        try:
            with open(path) as f:
                baseline = json.load(f)
            with self._lock:
                self._table.update({k: v.lower() for k, v in baseline.items()})
            log.info(f"Loaded {len(baseline)} baseline entries from {path}")
        except (OSError, json.JSONDecodeError) as e:
            log.warning(f"Could not load baseline: {e}")

    def save_baseline(self, path: str):
        with self._lock:
            with open(path, "w") as f:
                json.dump(self._table, f, indent=2)
        log.info(f"Baseline saved to {path}")


# ─────────────────────────────────────────────
#  PACKET SNIFFER + ANALYZER
# ─────────────────────────────────────────────

class PacketSniffer:
    def __init__(
        self,
        iface: str | None = None,
        baseline_path: str | None = None,
        report_path: str | None = None,
        alert_threshold: int = 5,
        pcap_out: str | None = None,
    ):
        self.iface = iface
        self.report_path = report_path
        self.alert_threshold = alert_threshold
        self.pcap_out = pcap_out

        self.arp_table = ARPTable()
        self.stats: dict[str, int] = defaultdict(int)
        self.captured_packets = []
        self.alert_counts: dict[str, int] = defaultdict(int)
        self.dns_log: list[dict] = []
        self.http_log: list[dict] = []
        self._start_time = datetime.now()

        if baseline_path:
            self.arp_table.load_baseline(baseline_path)

    # ── ARP ──────────────────────────────────

    def _handle_arp(self, pkt):
        self.stats["arp"] += 1
        op = "request" if pkt[ARP].op == 1 else "reply"
        src_ip  = pkt[ARP].psrc
        src_mac = pkt[ARP].hwsrc
        dst_ip  = pkt[ARP].pdst

        log.info(f"[ARP {op.upper()}] {src_ip} ({src_mac}) → {dst_ip}")

        if op == "reply":
            conflict = self.arp_table.check_and_update(src_ip, src_mac)
            if conflict:
                self.stats["spoof_alerts"] += 1
                self.alert_counts[src_ip] += 1
                severity = conflict["severity"]

                log.warning(
                    f"\n{'!'*60}\n"
                    f"  [{severity}] ARP SPOOFING DETECTED\n"
                    f"  IP      : {conflict['ip']}\n"
                    f"  Known   : {conflict['known_mac']}\n"
                    f"  Forged  : {conflict['new_mac']}\n"
                    f"  Time    : {conflict['timestamp']}\n"
                    f"{'!'*60}"
                )

                if self.alert_counts[src_ip] >= self.alert_threshold:
                    log.critical(
                        f"[CRITICAL] {src_ip} has triggered {self.alert_counts[src_ip]} "
                        f"spoof alerts — possible active MITM attack in progress"
                    )

    # ── IP LAYER ─────────────────────────────

    def _handle_ip(self, pkt):
        self.stats["ip"] += 1
        src = pkt[IP].src
        dst = pkt[IP].dst

        if TCP in pkt:
            self.stats["tcp"] += 1
            self._handle_tcp(pkt, src, dst)
        elif UDP in pkt:
            self.stats["udp"] += 1
            self._handle_udp(pkt, src, dst)

    # ── TCP ──────────────────────────────────

    def _handle_tcp(self, pkt, src: str, dst: str):
        sport = pkt[TCP].sport
        dport = pkt[TCP].dport
        flags = pkt[TCP].flags

        flag_str = ""
        if flags & 0x02: flag_str += "S"
        if flags & 0x10: flag_str += "A"
        if flags & 0x01: flag_str += "F"
        if flags & 0x04: flag_str += "R"
        if flags & 0x08: flag_str += "P"

        log.info(f"[TCP] {src}:{sport} → {dst}:{dport} [{flag_str}]")

        # SYN flood heuristic
        if flags == 0x02:
            self.stats["syn_count"] += 1
            if self.stats["syn_count"] % 50 == 0:
                log.warning(f"[HEURISTIC] High SYN rate: {self.stats['syn_count']} SYN packets observed")

        # HTTP cleartext credential sniff
        from scapy.layers.http import HTTPRequest
        if HTTPRequest in pkt:
            method = pkt[HTTPRequest].Method.decode(errors="ignore")
            host   = pkt[HTTPRequest].Host.decode(errors="ignore")
            path   = pkt[HTTPRequest].Path.decode(errors="ignore")
            log.info(f"         └─ HTTP {method} {host}{path}")
            entry = {"time": datetime.now().isoformat(), "method": method, "host": host, "path": path}
            self.http_log.append(entry)

            from scapy.packet import Raw
            if Raw in pkt:
                body = pkt[Raw].load.decode(errors="ignore").lower()
                for kw in ["password=", "passwd=", "pass=", "pwd=", "token=", "secret="]:
                    if kw in body:
                        log.warning(f"[CLEARTEXT CRED] Keyword '{kw}' in HTTP body from {src}")
                        self.stats["cleartext_creds"] += 1
                        break

    # ── UDP / DNS ────────────────────────────

    def _handle_udp(self, pkt, src: str, dst: str):
        sport = pkt[UDP].sport
        dport = pkt[UDP].dport
        log.info(f"[UDP] {src}:{sport} → {dst}:{dport}")

        if DNS in pkt and DNSQR in pkt:
            self.stats["dns"] += 1
            qname = pkt[DNSQR].qname.decode(errors="ignore").rstrip(".")
            qtype = pkt[DNSQR].qtype
            log.info(f"         └─ DNS QUERY {qname} (type {qtype})")
            self.dns_log.append({
                "time": datetime.now().isoformat(),
                "src": src, "query": qname, "type": qtype
            })

            # DNS tunneling heuristic
            if len(qname) > 50:
                log.warning(
                    f"[HEURISTIC] Long DNS query ({len(qname)} chars) may indicate tunneling: "
                    f"{qname[:60]}..."
                )
                self.stats["dns_tunnel_suspects"] += 1

    # ── MAIN DISPATCH ────────────────────────

    def _process(self, pkt):
        self.stats["total"] += 1
        self.captured_packets.append(pkt)

        if ARP in pkt:
            self._handle_arp(pkt)
        elif IP in pkt:
            self._handle_ip(pkt)

    # ── SCAN ARP TABLE ───────────────────────

    def scan_network_arp(self, network: str = "192.168.1.0/24") -> dict[str, str]:
        log.info(f"[ARP SCAN] Scanning {network}")
        answered, _ = srp(
            Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network),
            timeout=3,
            iface=self.iface,
            verbose=False
        )
        discovered = {}
        for _, rcv in answered:
            ip  = rcv[ARP].psrc
            mac = rcv[ARP].hwsrc
            discovered[ip] = mac
            self.arp_table.check_and_update(ip, mac)
            log.info(f"  {ip:<18} {mac}")
        log.info(f"[ARP SCAN] Found {len(discovered)} hosts")
        return discovered

    # ── START ────────────────────────────────

    def start(
        self,
        count: int = 0,
        bpf_filter: str = "",
        timeout: int | None = None,
    ):
        log.info(f"[*] Starting capture on {self.iface or 'default interface'}")
        log.info(f"[*] Filter: '{bpf_filter or 'none'}' | Count: {count or 'unlimited'}")

        try:
            sniff(
                iface=self.iface,
                filter=bpf_filter,
                count=count,
                timeout=timeout,
                prn=self._process,
                store=False,
            )
        except KeyboardInterrupt:
            pass
        finally:
            self.print_summary()
            if self.report_path:
                self.save_report(self.report_path)

    # ── SUMMARY ──────────────────────────────

    def print_summary(self):
        elapsed = (datetime.now() - self._start_time).seconds
        conflicts = self.arp_table.get_conflicts()

        print(f"\n{'='*60}")
        print(f"  CAPTURE SUMMARY")
        print(f"{'='*60}")
        print(f"  Duration          : {elapsed}s")
        print(f"  Total Packets     : {self.stats['total']}")
        print(f"  ARP               : {self.stats['arp']}")
        print(f"  IP/TCP            : {self.stats['tcp']}")
        print(f"  IP/UDP            : {self.stats['udp']}")
        print(f"  DNS Queries       : {self.stats['dns']}")
        print(f"  SYN Packets       : {self.stats['syn_count']}")
        print(f"  Cleartext Creds   : {self.stats['cleartext_creds']}")
        print(f"  DNS Tunnel Suspects: {self.stats['dns_tunnel_suspects']}")
        print(f"  ARP Spoof Alerts  : {self.stats['spoof_alerts']}")

        if conflicts:
            print(f"\n  ARP SPOOFING EVENTS ({len(conflicts)}):")
            for c in conflicts:
                print(f"    [{c['severity']}] {c['ip']} — {c['known_mac']} → {c['new_mac']}")
        else:
            print(f"\n  No ARP spoofing detected.")

        arp_tbl = self.arp_table.get_table()
        print(f"\n  LEARNED ARP TABLE ({len(arp_tbl)} entries):")
        for ip, mac in sorted(arp_tbl.items()):
            print(f"    {ip:<18} {mac}")
        print(f"{'='*60}\n")

    # ── REPORT ───────────────────────────────

    def save_report(self, path: str):
        report = {
            "generated": datetime.now().isoformat(),
            "stats": dict(self.stats),
            "arp_table": self.arp_table.get_table(),
            "spoof_events": self.arp_table.get_conflicts(),
            "dns_log": self.dns_log[-100:],
            "http_log": self.http_log[-100:],
        }
        try:
            with open(path, "w") as f:
                json.dump(report, f, indent=2)
            log.info(f"Report saved → {path}")
        except OSError as e:
            log.error(f"Failed to save report: {e}")

        # CSV for spoof events
        csv_path = Path(path).with_suffix(".csv")
        try:
            with open(csv_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["timestamp", "ip", "known_mac", "new_mac", "severity"])
                writer.writeheader()
                writer.writerows(self.arp_table.get_conflicts())
            log.info(f"CSV report saved → {csv_path}")
        except OSError as e:
            log.error(f"Failed to save CSV: {e}")


# ─────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Advanced Packet Sniffer + ARP Spoofing Detector",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command")

    # sniff
    sniff_p = subparsers.add_parser("sniff", help="Capture packets and detect ARP spoofing")
    sniff_p.add_argument("-i", "--iface", default=None, help="Network interface")
    sniff_p.add_argument("-c", "--count", type=int, default=0, help="Packet count (0=unlimited)")
    sniff_p.add_argument("-t", "--timeout", type=int, default=None, help="Stop after N seconds")
    sniff_p.add_argument("-f", "--filter", default="", help="BPF filter e.g. 'arp or tcp port 80'")
    sniff_p.add_argument("--baseline", help="Path to baseline JSON (ip→mac)")
    sniff_p.add_argument("--report", help="Save JSON+CSV report to this path")
    sniff_p.add_argument("--threshold", type=int, default=5, help="Alerts before CRITICAL warning")

    # scan
    scan_p = subparsers.add_parser("scan", help="Active ARP scan to build baseline")
    scan_p.add_argument("network", help="CIDR e.g. 192.168.1.0/24")
    scan_p.add_argument("-i", "--iface", default=None)
    scan_p.add_argument("--save", help="Save discovered table as baseline JSON")

    # interfaces
    subparsers.add_parser("interfaces", help="List available network interfaces")

    args = parser.parse_args()

    if args.command == "sniff":
        sniffer = PacketSniffer(
            iface=args.iface,
            baseline_path=args.baseline,
            report_path=args.report,
            alert_threshold=args.threshold,
        )
        sniffer.start(count=args.count, bpf_filter=args.filter, timeout=args.timeout)

    elif args.command == "scan":
        sniffer = PacketSniffer(iface=args.iface)
        table = sniffer.scan_network_arp(args.network)
        if args.save:
            with open(args.save, "w") as f:
                json.dump(table, f, indent=2)
            log.info(f"Baseline saved → {args.save}")

    elif args.command == "interfaces":
        print("Available interfaces:")
        for iface in get_if_list():
            print(f"  {iface}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
