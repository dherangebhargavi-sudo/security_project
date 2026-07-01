# security_project
advance packet sniffer and arp spoofing detector


A collection of Python-based security tools built during academic coursework and a one-month internship. All tools were tested on personal lab environments and legally designated vulnerable targets.

---

## Projects

### 1. Network Port Scanner
Scans a target for open ports, grabs service banners, and identifies running services using concurrent threading.

**Tools:** Python, socket, concurrent.futures  
**Tested on:** localhost, personal lab VMs

```bash
python scanner.py 192.168.1.1 --start 1 --end 1024
```

---

### 2. Web Vulnerability Tester
Detects SQL Injection and XSS vulnerabilities in web application forms and URL parameters using payload injection and error-pattern matching.

**Tools:** Python, requests, BeautifulSoup4  
**Tested on:** http://testphp.vulnweb.com/ (intentionally vulnerable legal target)

```bash
python tester.py http://testphp.vulnweb.com/
```

---

### 3. Packet Analyzer
Captures and analyzes live network packets. Identifies HTTP traffic, DNS queries, suspicious SYN rates, and potential DNS tunneling.

**Tools:** Python, Scapy  
**Tested on:** Local network interface only

```bash
sudo python analyzer.py -i eth0 -c 100 -f "tcp or udp"
```

---

### 4. Antivirus Simulator
Signature-based file scanner using MD5 and SHA256 hashing. Includes heuristic string detection, quarantine logic, real-time folder monitoring, and JSON report generation.

**Tools:** Python, hashlib, watchdog  
**Tested on:** Custom test files with known hashes

```bash
python av_sim.py scan ./test_folder --quarantine --report report.json
python av_sim.py monitor ./downloads
python av_sim.py hash suspicious.exe
```

---

### 5. ARP Spoofing Detector
Monitors network traffic for ARP poisoning attacks by tracking IP-to-MAC mappings and alerting on conflicts. Includes active ARP scanning, baseline comparison, and CSV/JSON reporting.

**Tools:** Python, Scapy  
**Tested on:** Personal lab network

```bash
sudo python arp_sniffer.py interfaces
sudo python arp_sniffer.py scan 192.168.1.0/24 --save baseline.json
sudo python arp_sniffer.py sniff -i eth0 --baseline baseline.json --report report.json
```

---

## Installation

```bash
git clone https://github.com/YOURUSERNAME/cybersecurity-portfolio
cd cybersecurity-portfolio
pip install -r requirements.txt
```

> **Note:** Packet capture tools require root/administrator privileges.  
> On Linux: prefix commands with `sudo`  
> On Windows: run terminal as Administrator

---

## Folder Structure
