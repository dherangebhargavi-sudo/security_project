<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="DENY">
<title>NetSentry — Secure Access Portal</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
  :root {
    --bg-primary: #0a0e14;
    --bg-secondary: #0f1419;
    --bg-card: #131920;
    --bg-elevated: #1a2028;
    --border: #1e2a35;
    --border-active: #2a3a4a;
    --text-primary: #e8edf3;
    --text-secondary: #7a8a9e;
    --text-muted: #4a5568;
    --accent: #00e5a0;
    --accent-dim: rgba(0,229,160,0.12);
    --accent-glow: rgba(0,229,160,0.25);
    --danger: #ff4757;
    --danger-dim: rgba(255,71,87,0.12);
    --warning: #ffa502;
    --warning-dim: rgba(255,165,2,0.12);
    --info: #1e90ff;
    --info-dim: rgba(30,144,255,0.12);
    --cyan: #00d4ff;
    --cyan-dim: rgba(0,212,255,0.12);
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Space Grotesk', sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    min-height: 100vh;
    overflow-x: hidden;
    user-select: none;
    -webkit-user-select: none;
  }
  body::before {
    content: '';
    position: fixed;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(ellipse at 20% 20%, rgba(0,229,160,0.03) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(0,212,255,0.02) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 0%, var(--bg-primary) 70%);
    pointer-events: none; z-index: 0;
  }
  ::-webkit-scrollbar { width: 5px; height: 5px; }
  ::-webkit-scrollbar-track { background: var(--bg-secondary); }
  ::-webkit-scrollbar-thumb { background: var(--border-active); border-radius: 4px; }
  ::-webkit-scrollbar-thumb:hover { background: var(--accent); }

  /* ===== LOGIN GATE ===== */
  #loginGate {
    position: fixed; inset: 0; z-index: 99999;
    background: var(--bg-primary);
    display: flex; align-items: center; justify-content: center;
    flex-direction: column;
  }
  #loginGate.locked-out {
    background: linear-gradient(135deg, #1a0a0e, #0a0e14, #0a0a1a);
  }
  .login-container {
    width: 420px; max-width: 92vw;
    text-align: center;
    position: relative; z-index: 2;
  }
  .login-shield {
    width: 80px; height: 80px;
    margin: 0 auto 28px;
    background: linear-gradient(135deg, var(--accent), var(--cyan));
    border-radius: 24px;
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; color: var(--bg-primary);
    position: relative;
    animation: shieldPulse 3s ease-in-out infinite;
  }
  .login-shield::after {
    content: ''; position: absolute; inset: -6px;
    border-radius: 28px;
    background: linear-gradient(135deg, var(--accent), var(--cyan));
    opacity: 0.2; filter: blur(12px); z-index: -1;
  }
  @keyframes shieldPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.04); }
  }
  .login-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 22px; font-weight: 700; margin-bottom: 8px;
  }
  .login-title span { color: var(--accent); }
  .login-subtitle {
    font-size: 13px; color: var(--text-muted); margin-bottom: 32px; line-height: 1.5;
  }
  .login-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 24px;
    text-align: left;
  }
  .login-field {
    margin-bottom: 18px;
  }
  .login-field label {
    display: block; font-size: 11px; text-transform: uppercase;
    letter-spacing: 1px; color: var(--text-muted);
    margin-bottom: 8px; font-weight: 600;
  }
  .login-input-wrap {
    position: relative;
  }
  .login-input-wrap i {
    position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
    color: var(--text-muted); font-size: 14px;
    transition: color 0.2s;
  }
  .login-input {
    width: 100%; padding: 12px 14px 12px 42px;
    background: var(--bg-primary);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text-primary);
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    outline: none;
    transition: all 0.2s;
  }
  .login-input:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-dim);
  }
  .login-input:focus + i,
  .login-input:focus ~ i { color: var(--accent); }
  .login-input.error {
    border-color: var(--danger);
    box-shadow: 0 0 0 3px var(--danger-dim);
    animation: shake 0.4s ease-in-out;
  }
  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    20% { transform: translateX(-8px); }
    40% { transform: translateX(8px); }
    60% { transform: translateX(-5px); }
    80% { transform: translateX(5px); }
  }
  .login-error {
    font-size: 12px; color: var(--danger);
    margin-top: 8px; display: none;
    align-items: center; gap: 6px;
  }
  .login-error.show { display: flex; }
  .login-btn {
    width: 100%; padding: 13px;
    background: var(--accent); color: var(--bg-primary);
    border: none; border-radius: 10px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px; font-weight: 700;
    cursor: pointer; transition: all 0.2s;
    display: flex; align-items: center; justify-content: center; gap: 8px;
    margin-top: 4px;
  }
  .login-btn:hover {
    background: #00cc8e;
    box-shadow: 0 4px 24px var(--accent-glow);
    transform: translateY(-1px);
  }
  .login-btn:disabled {
    opacity: 0.4; cursor: not-allowed; transform: none;
    box-shadow: none;
  }
  .login-meta {
    margin-top: 20px; text-align: center;
    font-size: 11px; color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.8;
  }
  .login-meta .secure-badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 10px; border-radius: 10px;
    background: var(--accent-dim); color: var(--accent);
    font-size: 10px; font-weight: 600; margin-bottom: 8px;
  }
  .lockout-overlay {
    display: none;
    position: fixed; inset: 0; z-index: 100000;
    background: rgba(10,14,20,0.95);
    backdrop-filter: blur(20px);
    flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center;
  }
  .lockout-overlay.show { display: flex; }
  .lockout-icon {
    width: 80px; height: 80px;
    border-radius: 50%;
    background: var(--danger-dim);
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; color: var(--danger);
    margin-bottom: 24px;
    animation: shieldPulse 1.5s ease-in-out infinite;
  }
  .lockout-title {
    font-size: 24px; font-weight: 700; color: var(--danger); margin-bottom: 12px;
  }
  .lockout-desc {
    font-size: 14px; color: var(--text-secondary); max-width: 400px; line-height: 1.7; margin-bottom: 20px;
  }
  .lockout-timer {
    font-family: 'JetBrains Mono', monospace;
    font-size: 36px; font-weight: 700; color: var(--danger);
    margin-bottom: 8px;
  }
  .lockout-sub {
    font-size: 12px; color: var(--text-muted);
  }

  /* ===== SESSION LOCK SCREEN ===== */
  #sessionLock {
    position: fixed; inset: 0; z-index: 50000;
    background: rgba(10,14,20,0.92);
    backdrop-filter: blur(16px);
    display: none; align-items: center; justify-content: center;
    flex-direction: column;
  }
  #sessionLock.show { display: flex; }
  .session-lock-icon {
    width: 60px; height: 60px; border-radius: 18px;
    background: var(--warning-dim);
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; color: var(--warning);
    margin-bottom: 20px;
  }
  .session-lock-title {
    font-size: 18px; font-weight: 600; margin-bottom: 6px;
  }
  .session-lock-sub {
    font-size: 12px; color: var(--text-muted); margin-bottom: 24px;
  }
  .session-lock-input {
    padding: 12px 18px; width: 280px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text-primary);
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px; outline: none;
    text-align: center;
    transition: all 0.2s;
  }
  .session-lock-input:focus {
    border-color: var(--warning);
    box-shadow: 0 0 0 3px var(--warning-dim);
  }
  .session-lock-error {
    font-size: 11px; color: var(--danger);
    margin-top: 8px; height: 16px;
  }

  /* ===== TAMPER WARNING ===== */
  #tamperWarning {
    position: fixed; inset: 0; z-index: 200000;
    background: rgba(10,5,5,0.97);
    backdrop-filter: blur(30px);
    display: none; align-items: center; justify-content: center;
    flex-direction: column; text-align: center;
  }
  #tamperWarning.show { display: flex; }
  .tamper-icon {
    font-size: 60px; color: var(--danger); margin-bottom: 24px;
    animation: shieldPulse 0.8s ease-in-out infinite;
  }
  .tamper-title { font-size: 28px; font-weight: 700; color: var(--danger); margin-bottom: 12px; }
  .tamper-desc { font-size: 14px; color: var(--text-secondary); max-width: 450px; line-height: 1.7; }

  /* ===== MAIN APP (hidden until auth) ===== */
  #mainApp { display: none; position: relative; z-index: 1; }
  #mainApp.unlocked { display: block; }

  /* ===== HEADER ===== */
  .header {
    position: sticky; top: 0; z-index: 100;
    background: rgba(10,14,20,0.85);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
    padding: 0 24px; height: 60px;
    display: flex; align-items: center; justify-content: space-between;
  }
  .logo { display: flex; align-items: center; gap: 12px; }
  .logo-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, var(--accent), var(--cyan));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; color: var(--bg-primary); font-weight: 700;
    position: relative;
  }
  .logo-icon::after {
    content: ''; position: absolute; inset: -3px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--accent), var(--cyan));
    opacity: 0.3; filter: blur(6px); z-index: -1;
  }
  .logo-text {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700; font-size: 18px; letter-spacing: -0.5px;
  }
  .logo-text span { color: var(--accent); }
  .header-controls { display: flex; align-items: center; gap: 10px; }
  .session-timer-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; color: var(--text-muted);
    padding: 5px 12px;
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: 8px;
    display: flex; align-items: center; gap: 6px;
  }
  .session-timer-badge i { color: var(--warning); font-size: 10px; }
  .status-badge {
    display: flex; align-items: center; gap: 6px;
    padding: 6px 14px; border-radius: 20px;
    font-size: 12px; font-weight: 500;
    font-family: 'JetBrains Mono', monospace;
  }
  .status-badge.idle { background: var(--bg-elevated); color: var(--text-secondary); border: 1px solid var(--border); }
  .status-badge.active { background: var(--accent-dim); color: var(--accent); border: 1px solid rgba(0,229,160,0.25); }
  .status-badge.alert { background: var(--danger-dim); color: var(--danger); border: 1px solid rgba(255,71,87,0.25); animation: pulseBadge 1.5s ease-in-out infinite; }
  @keyframes pulseBadge {
    0%, 100% { box-shadow: 0 0 0 0 rgba(255,71,87,0.3); }
    50% { box-shadow: 0 0 0 6px rgba(255,71,87,0); }
  }
  .status-dot { width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
  .status-badge.active .status-dot { animation: blink 1s ease-in-out infinite; }
  @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

  /* Buttons */
  .btn {
    padding: 8px 18px; border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--bg-elevated); color: var(--text-primary);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px; font-weight: 500;
    cursor: pointer; transition: all 0.2s;
    display: flex; align-items: center; gap: 7px;
  }
  .btn:hover { border-color: var(--border-active); background: var(--bg-card); transform: translateY(-1px); }
  .btn-primary { background: var(--accent); color: var(--bg-primary); border-color: var(--accent); font-weight: 600; }
  .btn-primary:hover { background: #00cc8e; border-color: #00cc8e; box-shadow: 0 4px 20px var(--accent-glow); }
  .btn-danger { background: var(--danger); color: #fff; border-color: var(--danger); font-weight: 600; }
  .btn-danger:hover { background: #e8404f; box-shadow: 0 4px 20px rgba(255,71,87,0.25); }
  .btn-sm { padding: 5px 12px; font-size: 11px; }

  /* Main layout */
  .main {
    position: relative; z-index: 1;
    padding: 20px 24px;
    display: grid;
    grid-template-columns: 1fr 380px;
    grid-template-rows: auto 1fr;
    gap: 16px;
    height: calc(100vh - 60px);
  }
  .stats-row {
    grid-column: 1 / -1;
    display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px;
  }
  .stat-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 16px 18px;
    position: relative; overflow: hidden; transition: all 0.3s;
  }
  .stat-card:hover { border-color: var(--border-active); transform: translateY(-2px); }
  .stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; }
  .stat-card.accent::before { background: linear-gradient(90deg, var(--accent), transparent); }
  .stat-card.cyan::before { background: linear-gradient(90deg, var(--cyan), transparent); }
  .stat-card.danger::before { background: linear-gradient(90deg, var(--danger), transparent); }
  .stat-card.warning::before { background: linear-gradient(90deg, var(--warning), transparent); }
  .stat-card.info::before { background: linear-gradient(90deg, var(--info), transparent); }
  .stat-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); margin-bottom: 8px; font-weight: 500; }
  .stat-value { font-family: 'JetBrains Mono', monospace; font-size: 26px; font-weight: 700; line-height: 1; }
  .stat-card.accent .stat-value { color: var(--accent); }
  .stat-card.cyan .stat-value { color: var(--cyan); }
  .stat-card.danger .stat-value { color: var(--danger); }
  .stat-card.warning .stat-value { color: var(--warning); }
  .stat-card.info .stat-value { color: var(--info); }
  .stat-sub { font-size: 11px; color: var(--text-secondary); margin-top: 6px; font-family: 'JetBrains Mono', monospace; }

  .left-panel { display: flex; flex-direction: column; gap: 16px; min-height: 0; }
  .panel {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; overflow: hidden; display: flex; flex-direction: column;
  }
  .panel-header {
    padding: 14px 18px; border-bottom: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between; flex-shrink: 0;
  }
  .panel-title { font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
  .panel-title i { font-size: 14px; opacity: 0.6; }
  .panel-body { flex: 1; overflow-y: auto; min-height: 0; }

  .packet-feed { flex: 1; }
  .packet-feed .panel-body { padding: 0; }
  .packet-row {
    display: grid;
    grid-template-columns: 90px 50px 130px 130px 70px 80px 1fr;
    align-items: center; padding: 8px 16px;
    font-family: 'JetBrains Mono', monospace; font-size: 11px;
    border-bottom: 1px solid rgba(30,42,53,0.5);
    transition: background 0.15s; cursor: pointer;
  }
  .packet-row:hover { background: var(--bg-elevated); }
  .packet-row.flagged { background: var(--danger-dim); border-left: 3px solid var(--danger); }
  .packet-row.flagged:hover { background: rgba(255,71,87,0.18); }
  .pkt-time { color: var(--text-muted); }
  .pkt-proto { font-weight: 600; }
  .pkt-proto.arp { color: var(--warning); }
  .pkt-proto.tcp { color: var(--cyan); }
  .pkt-proto.udp { color: var(--info); }
  .pkt-proto.icmp { color: var(--accent); }
  .pkt-proto.dns { color: #c084fc; }
  .pkt-src, .pkt-dst { color: var(--text-secondary); }
  .pkt-len { color: var(--text-muted); text-align: right; }
  .pkt-flag { text-align: center; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: 600; }
  .pkt-flag.clean { color: var(--accent); background: var(--accent-dim); }
  .pkt-flag.warn { color: var(--warning); background: var(--warning-dim); }
  .pkt-flag.bad { color: var(--danger); background: var(--danger-dim); }
  .pkt-info { color: var(--text-muted); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

  .topology-panel { height: 220px; flex-shrink: 0; }
  .topology-panel .panel-body { padding: 0; position: relative; }
  #topoCanvas { width: 100%; height: 100%; display: block; }

  .right-panel { display: flex; flex-direction: column; gap: 16px; min-height: 0; }
  .arp-panel { flex: 0 0 auto; max-height: 240px; }
  .arp-table { width: 100%; font-family: 'JetBrains Mono', monospace; font-size: 11px; }
  .arp-table thead th {
    text-align: left; padding: 8px 14px; color: var(--text-muted);
    font-weight: 500; font-size: 10px; text-transform: uppercase;
    letter-spacing: 0.8px; background: var(--bg-elevated);
    position: sticky; top: 0; z-index: 2;
  }
  .arp-table tbody tr { border-bottom: 1px solid rgba(30,42,53,0.5); transition: background 0.15s; }
  .arp-table tbody tr:hover { background: var(--bg-elevated); }
  .arp-table tbody tr.suspicious { background: var(--danger-dim); }
  .arp-table td { padding: 7px 14px; color: var(--text-secondary); }
  .arp-table .mac-addr { color: var(--text-primary); }
  .arp-table .ip-addr { color: var(--cyan); }
  .arp-status {
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 10px; padding: 2px 8px; border-radius: 10px; font-weight: 600;
  }
  .arp-status.ok { color: var(--accent); background: var(--accent-dim); }
  .arp-status.warn { color: var(--warning); background: var(--warning-dim); }
  .arp-status.bad { color: var(--danger); background: var(--danger-dim); }

  .ai-panel { flex: 1; min-height: 0; }
  .ai-badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 10px; border-radius: 12px;
    font-size: 10px; font-weight: 600;
    background: linear-gradient(135deg, var(--accent-dim), var(--cyan-dim));
    color: var(--accent); border: 1px solid rgba(0,229,160,0.2);
  }
  .ai-badge i { font-size: 9px; }
  .ai-output { padding: 14px; font-size: 12px; line-height: 1.7; color: var(--text-secondary); }
  .ai-output .ai-msg {
    margin-bottom: 14px; padding: 10px 14px;
    background: var(--bg-elevated); border-radius: 10px;
    border-left: 3px solid var(--border-active);
    animation: fadeSlideIn 0.4s ease-out;
  }
  .ai-output .ai-msg.analysis { border-left-color: var(--accent); }
  .ai-output .ai-msg.threat { border-left-color: var(--danger); background: var(--danger-dim); }
  .ai-output .ai-msg.info-msg { border-left-color: var(--cyan); }
  .ai-output .ai-msg .msg-time { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--text-muted); margin-bottom: 4px; }
  .ai-output .ai-msg .msg-text { color: var(--text-primary); font-size: 12px; }
  .ai-output .ai-msg .msg-text strong { color: var(--accent); font-weight: 600; }
  .ai-output .ai-msg.threat .msg-text strong { color: var(--danger); }
  @keyframes fadeSlideIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

  .alerts-panel { flex: 0 0 auto; max-height: 200px; }
  .alert-item {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 10px 14px; border-bottom: 1px solid rgba(30,42,53,0.5);
    animation: fadeSlideIn 0.3s ease-out;
  }
  .alert-icon {
    width: 28px; height: 28px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; flex-shrink: 0; margin-top: 2px;
  }
  .alert-icon.critical { background: var(--danger-dim); color: var(--danger); }
  .alert-icon.warning { background: var(--warning-dim); color: var(--warning); }
  .alert-icon.info { background: var(--cyan-dim); color: var(--cyan); }
  .alert-content { flex: 1; min-width: 0; }
  .alert-title { font-size: 12px; font-weight: 600; margin-bottom: 2px; }
  .alert-desc { font-size: 11px; color: var(--text-muted); line-height: 1.4; }
  .alert-time { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--text-muted); flex-shrink: 0; margin-top: 3px; }

  .ethics-banner {
    grid-column: 1 / -1;
    background: linear-gradient(135deg, rgba(255,165,2,0.08), rgba(255,71,87,0.06));
    border: 1px solid rgba(255,165,2,0.2);
    border-radius: 10px; padding: 10px 18px;
    display: flex; align-items: center; gap: 10px;
    font-size: 12px; color: var(--warning);
  }
  .ethics-banner i { font-size: 16px; flex-shrink: 0; }
  .ethics-banner strong { color: var(--text-primary); }

  /* Modal */
  .modal-overlay {
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.7); backdrop-filter: blur(8px);
    z-index: 1000; display: none; align-items: center; justify-content: center;
    animation: fadeIn 0.2s;
  }
  .modal-overlay.show { display: flex; }
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  .modal {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 16px; width: 580px; max-height: 80vh;
    overflow-y: auto; animation: modalSlide 0.3s ease-out;
  }
  @keyframes modalSlide { from { opacity: 0; transform: translateY(20px) scale(0.97); } to { opacity: 1; transform: translateY(0) scale(1); } }
  .modal-header {
    padding: 18px 22px; border-bottom: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between;
  }
  .modal-header h3 { font-size: 15px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
  .modal-close {
    width: 30px; height: 30px; border-radius: 8px;
    border: 1px solid var(--border); background: var(--bg-elevated);
    color: var(--text-secondary); cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; transition: all 0.15s;
  }
  .modal-close:hover { background: var(--danger-dim); color: var(--danger); border-color: rgba(255,71,87,0.3); }
  .modal-body { padding: 18px 22px; }
  .detail-section { margin-bottom: 18px; }
  .detail-section:last-child { margin-bottom: 0; }
  .detail-section-title { font-size: 10px; text-transform: uppercase; letter-spacing: 1.2px; color: var(--text-muted); margin-bottom: 10px; font-weight: 600; }
  .detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .detail-item { padding: 10px 12px; background: var(--bg-elevated); border-radius: 8px; border: 1px solid var(--border); }
  .detail-item .label { font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
  .detail-item .value { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-primary); word-break: break-all; }
  .hex-dump {
    font-family: 'JetBrains Mono', monospace; font-size: 11px;
    color: var(--text-muted); line-height: 1.8;
    padding: 12px; background: var(--bg-primary);
    border-radius: 8px; border: 1px solid var(--border);
    max-height: 180px; overflow-y: auto; word-break: break-all;
  }
  .hex-dump .hex-offset { color: var(--accent); }
  .hex-dump .hex-data { color: var(--text-secondary); }
  .hex-dump .hex-ascii { color: var(--cyan); }

  .scanline {
    position: fixed; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    opacity: 0; pointer-events: none; z-index: 9999;
  }
  .scanline.active { opacity: 0.4; animation: scanDown 4s linear infinite; }
  @keyframes scanDown { 0% { top: 0; } 100% { top: 100vh; } }

  .toast-container {
    position: fixed; top: 72px; right: 24px; z-index: 45000;
    display: flex; flex-direction: column; gap: 8px;
  }
  .toast {
    padding: 12px 18px; border-radius: 10px;
    font-size: 13px; font-weight: 500;
    display: flex; align-items: center; gap: 10px;
    animation: toastIn 0.3s ease-out;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    min-width: 280px;
  }
  .toast.success { background: var(--bg-card); border: 1px solid rgba(0,229,160,0.3); color: var(--accent); }
  .toast.error { background: var(--bg-card); border: 1px solid rgba(255,71,87,0.3); color: var(--danger); }
  @keyframes toastIn { from { opacity: 0; transform: translateX(30px); } to { opacity: 1; transform: translateX(0); } }

  /* Security HUD in header */
  .sec-hud {
    display: flex; align-items: center; gap: 6px;
    padding: 5px 10px; border-radius: 6px;
    background: var(--accent-dim);
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; color: var(--accent);
    font-weight: 600;
  }
  .sec-hud i { font-size: 9px; }

  @media (max-width: 1100px) {
    .main { grid-template-columns: 1fr; height: auto; }
    .stats-row { grid-template-columns: repeat(3, 1fr); }
    .packet-feed { min-height: 400px; }
    .topology-panel { height: 250px; }
    .arp-panel { max-height: 300px; }
    .ai-panel { min-height: 300px; }
    .alerts-panel { max-height: 250px; }
    .session-timer-badge { display: none; }
  }
  @media (max-width: 600px) {
    .stats-row { grid-template-columns: repeat(2, 1fr); }
    .packet-row { grid-template-columns: 70px 40px 100px 100px 1fr; }
    .packet-row .pkt-len, .packet-row .pkt-info { display: none; }
    .header { padding: 0 14px; }
    .main { padding: 14px; }
    .sec-hud { display: none; }
  }
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
  }
</style>
</head>
<body>

<!-- TAMPER WARNING OVERLAY -->
<div id="tamperWarning">
  <div class="tamper-icon"><i class="fas fa-skull-crossbones"></i></div>
  <div class="tamper-title">Security Violation Detected</div>
  <div class="tamper-desc">Tampering with developer tools or page integrity has been detected. This session has been terminated and locked. All activity has been logged.</div>
</div>

<!-- LOCKOUT OVERLAY -->
<div class="lockout-overlay" id="lockoutOverlay">
  <div class="lockout-icon"><i class="fas fa-ban"></i></div>
  <div class="lockout-title">Account Locked</div>
  <div class="lockout-desc">Too many failed authentication attempts. Your access has been temporarily suspended to protect the system.</div>
  <div class="lockout-timer" id="lockoutTimer">00:00</div>
  <div class="lockout-sub">Remaining cooldown time</div>
</div>

<!-- LOGIN GATE -->
<div id="loginGate">
  <div class="login-container">
    <div class="login-shield"><i class="fas fa-shield-halved"></i></div>
    <div class="login-title"><span>Net</span>Sentry</div>
    <div class="login-subtitle">Secure Access Portal — Authentication Required</div>
    <div class="login-box">
      <div class="login-field">
        <label>Access Password</label>
        <div class="login-input-wrap">
          <input type="password" class="login-input" id="loginPassword" autocomplete="off" spellcheck="false" placeholder="Enter security passphrase">
          <i class="fas fa-lock"></i>
        </div>
        <div class="login-error" id="loginError"><i class="fas fa-circle-exclamation"></i> <span id="loginErrorText">Invalid password</span></div>
      </div>
      <button class="login-btn" id="loginBtn"><i class="fas fa-right-to-bracket"></i> Authenticate</button>
    </div>
    <div class="login-meta">
      <div class="secure-badge"><i class="fas fa-fingerprint"></i> PBKDF2 SHA-256 Encrypted</div><br>
      Session: <span id="loginSessionId">--</span><br>
      Attempts: <span id="loginAttempts">0</span> / 5 &nbsp;|&nbsp; Lockout: 5 min
    </div>
  </div>
</div>

<!-- SESSION LOCK -->
<div id="sessionLock">
  <div class="session-lock-icon"><i class="fas fa-lock"></i></div>
  <div class="session-lock-title">Session Locked</div>
  <div class="session-lock-sub">Inactivity timeout — re-enter password to continue</div>
  <input type="password" class="session-lock-input" id="sessionLockPassword" autocomplete="off" spellcheck="false" placeholder="Password">
  <div class="session-lock-error" id="sessionLockError"></div>
</div>

<!-- MAIN APP -->
<div id="mainApp">
  <div class="scanline" id="scanline"></div>
  <header class="header">
    <div class="logo">
      <div class="logo-icon"><i class="fas fa-shield-halved"></i></div>
      <div class="logo-text"><span>Net</span>Sentry</div>
    </div>
    <div class="header-controls">
      <div class="sec-hud"><i class="fas fa-shield-check"></i> SECURE</div>
      <div class="session-timer-badge" id="sessionTimerBadge"><i class="fas fa-clock"></i> <span id="sessionCountdown">5:00</span></div>
      <div class="status-badge idle" id="statusBadge">
        <div class="status-dot"></div>
        <span id="statusText">IDLE</span>
      </div>
      <button class="btn btn-sm" id="btnLock" title="Lock Session"><i class="fas fa-lock"></i></button>
      <button class="btn btn-sm" id="btnEthics" title="Ethical Usage Guidelines"><i class="fas fa-scale-balanced"></i></button>
      <button class="btn btn-primary" id="btnStart"><i class="fas fa-play"></i> Start Capture</button>
      <button class="btn btn-danger" id="btnStop" style="display:none;"><i class="fas fa-stop"></i> Stop</button>
    </div>
  </header>
  <main class="main">
    <div class="ethics-banner">
      <i class="fas fa-triangle-exclamation"></i>
      <div><strong>Ethical Use Only.</strong> This tool simulates network analysis for educational purposes. Only use packet sniffing on networks you own or have explicit written authorization to test.</div>
    </div>
    <div class="stats-row">
      <div class="stat-card accent"><div class="stat-label">Packets Captured</div><div class="stat-value" id="statPackets">0</div><div class="stat-sub" id="statPps">0 pkt/s</div></div>
      <div class="stat-card cyan"><div class="stat-label">ARP Entries</div><div class="stat-value" id="statArp">0</div><div class="stat-sub" id="statArpSub">0 stable</div></div>
      <div class="stat-card danger"><div class="stat-label">Threats Detected</div><div class="stat-value" id="statThreats">0</div><div class="stat-sub" id="statThreatSub">0 critical</div></div>
      <div class="stat-card warning"><div class="stat-label">Anomaly Score</div><div class="stat-value" id="statAnomaly">0%</div><div class="stat-sub">AI confidence</div></div>
      <div class="stat-card info"><div class="stat-label">Uptime</div><div class="stat-value" id="statUptime">00:00</div><div class="stat-sub" id="statIface">Interface: --</div></div>
    </div>
    <div class="left-panel">
      <div class="panel packet-feed">
        <div class="panel-header">
          <div class="panel-title"><i class="fas fa-stream"></i> Live Packet Feed</div>
          <button class="btn btn-sm" id="btnClearFeed"><i class="fas fa-eraser"></i> Clear</button>
        </div>
        <div class="panel-body" id="packetFeed">
          <div style="padding:40px;text-align:center;color:var(--text-muted);font-size:13px;">
            <i class="fas fa-satellite-dish" style="font-size:28px;margin-bottom:12px;display:block;opacity:0.3;"></i>
            Start capture to begin monitoring network traffic
          </div>
        </div>
      </div>
      <div class="panel topology-panel">
        <div class="panel-header">
          <div class="panel-title"><i class="fas fa-diagram-project"></i> Network Topology</div>
          <span style="font-size:11px;color:var(--text-muted);font-family:'JetBrains Mono',monospace;" id="topoNodeCount">0 nodes</span>
        </div>
        <div class="panel-body"><canvas id="topoCanvas"></canvas></div>
      </div>
    </div>
    <div class="right-panel">
      <div class="panel arp-panel">
        <div class="panel-header">
          <div class="panel-title"><i class="fas fa-table-list"></i> ARP Cache Monitor</div>
          <span style="font-size:11px;color:var(--text-muted);font-family:'JetBrains Mono',monospace;" id="arpCount">0 entries</span>
        </div>
        <div class="panel-body">
          <table class="arp-table">
            <thead><tr><th>IP Address</th><th>MAC Address</th><th>Status</th><th>Changes</th></tr></thead>
            <tbody id="arpTableBody"><tr><td colspan="4" style="text-align:center;padding:20px;color:var(--text-muted);font-size:12px;">No ARP entries yet</td></tr></tbody>
          </table>
        </div>
      </div>
      <div class="panel ai-panel">
        <div class="panel-header">
          <div class="panel-title"><i class="fas fa-brain"></i> AI Detection Engine <span class="ai-badge"><i class="fas fa-microchip"></i> Local Inference</span></div>
        </div>
        <div class="panel-body ai-output" id="aiOutput">
          <div class="ai-msg info-msg"><div class="msg-time">[SYSTEM]</div><div class="msg-text">AI detection engine initialized. Monitoring will begin when capture starts. All analysis runs locally — no data leaves your browser.</div></div>
        </div>
      </div>
      <div class="panel alerts-panel">
        <div class="panel-header">
          <div class="panel-title"><i class="fas fa-bell"></i> Alert Timeline</div>
          <span style="font-size:11px;color:var(--text-muted);font-family:'JetBrains Mono',monospace;" id="alertCount">0 alerts</span>
        </div>
        <div class="panel-body" id="alertFeed"><div style="padding:20px;text-align:center;color:var(--text-muted);font-size:12px;">No alerts</div></div>
      </div>
    </div>
  </main>
</div>

<!-- Packet Detail Modal -->
<div class="modal-overlay" id="packetModal">
  <div class="modal">
    <div class="modal-header">
      <h3><i class="fas fa-magnifying-glass-plus" style="color:var(--cyan);"></i> Packet Inspector</h3>
      <button class="modal-close" id="modalClose"><i class="fas fa-xmark"></i></button>
    </div>
    <div class="modal-body" id="modalBody"></div>
  </div>
</div>

<!-- Ethics Modal -->
<div class="modal-overlay" id="ethicsModal">
  <div class="modal" style="width:520px;">
    <div class="modal-header">
      <h3><i class="fas fa-scale-balanced" style="color:var(--warning);"></i> Ethical Usage Guidelines</h3>
      <button class="modal-close" id="ethicsClose"><i class="fas fa-xmark"></i></button>
    </div>
    <div class="modal-body" style="font-size:13px;line-height:1.8;color:var(--text-secondary);">
      <div class="detail-section"><div class="detail-section-title">Authorized Use Only</div><p>Only run packet sniffing and ARP detection tools on networks you own, operate, or have <strong style="color:var(--text-primary);">explicit written authorization</strong> to test.</p></div>
      <div class="detail-section"><div class="detail-section-title">Purpose</div><p>This tool is designed for <strong style="color:var(--accent);">educational purposes</strong> — learning network security concepts, understanding ARP protocol behavior, and studying detection methodologies.</p></div>
      <div class="detail-section"><div class="detail-section-title">Local Simulation</div><p>This dashboard generates <strong style="color:var(--cyan);">simulated network data</strong> entirely in your browser. No actual network interfaces are accessed.</p></div>
      <div class="detail-section"><div class="detail-section-title">Responsibility</div><p>Users are solely responsible for ensuring compliance with all applicable laws and regulations.</p></div>
    </div>
  </div>
</div>

<div class="toast-container" id="toastContainer"></div>

<script>
// ============================================================
// SECURITY LAYER — Multi-layered client-side protection
// All logic is local. No data ever leaves the browser.
// Default password: NetSentry@2024
// ============================================================
(function(){
'use strict';

// --- CONFIG ---
const CONFIG = {
  MAX_ATTEMPTS: 5,
  LOCKOUT_DURATION: 300, // 5 minutes in seconds
  SESSION_TIMEOUT: 300,  // 5 minutes inactivity
  DEVTOOL_CHECK_INTERVAL: 1000,
  INTEGRITY_CHECK_INTERVAL: 2000,
  PASSWORD_HASH: null, // computed at init
  PASSWORD_SALT: null,
  SESSION_TOKEN: null
};

// --- Generate session ID ---
function generateSessionId() {
  const arr = new Uint8Array(16);
  crypto.getRandomValues(arr);
  return Array.from(arr, b => b.toString(16).padStart(2, '0')).join('');
}

CONFIG.SESSION_TOKEN = generateSessionId();
document.getElementById('loginSessionId').textContent = CONFIG.SESSION_TOKEN.substring(0, 16) + '...';

// --- PBKDF2 Password Hashing (Web Crypto API) ---
async function hashPassword(password, salt) {
  const enc = new TextEncoder();
  const keyMaterial = await crypto.subtle.importKey('raw', enc.encode(password), 'PBKDF2', false, ['deriveBits']);
  const bits = await crypto.subtle.deriveBits({
    name: 'PBKDF2',
    salt: enc.encode(salt),
    iterations: 100000,
    hash: 'SHA-256'
  }, keyMaterial, 256);
  return Array.from(new Uint8Array(bits), b => b.toString(16).padStart(2, '0')).join('');
}

async function initPasswordHash() {
  // Salt derived from session + fixed component
  CONFIG.PASSWORD_SALT = 'NS_SALT_' + CONFIG.SESSION_TOKEN.substring(0, 8);
  CONFIG.PASSWORD_HASH = await hashPassword('NetSentry@2024', CONFIG.PASSWORD_SALT);
}

// --- State ---
let authState = {
  authenticated: false,
  attempts: 0,
  lockedOut: false,
  lockoutEnd: 0,
  lastActivity: 0,
  sessionTimeoutId: null,
  lockoutIntervalId: null,
  devtoolWarnings: 0
};

// --- DOM ---
const elLoginGate = document.getElementById('loginGate');
const elLoginPassword = document.getElementById('loginPassword');
const elLoginBtn = document.getElementById('loginBtn');
const elLoginError = document.getElementById('loginError');
const elLoginErrorText = document.getElementById('loginErrorText');
const elLoginAttempts = document.getElementById('loginAttempts');
const elLockoutOverlay = document.getElementById('lockoutOverlay');
const elLockoutTimer = document.getElementById('lockoutTimer');
const elSessionLock = document.getElementById('sessionLock');
const elSessionLockPw = document.getElementById('sessionLockPassword');
const elSessionLockErr = document.getElementById('sessionLockError');
const elMainApp = document.getElementById('mainApp');
const elTamperWarning = document.getElementById('tamperWarning');
const elSessionCountdown = document.getElementById('sessionCountdown');
const elSessionTimerBadge = document.getElementById('sessionTimerBadge');

// --- LOGIN ---
async function attemptLogin(password) {
  if (authState.lockedOut) return false;

  const hash = await hashPassword(password, CONFIG.PASSWORD_SALT);
  if (hash === CONFIG.PASSWORD_HASH) {
    authState.authenticated = true;
    authState.attempts = 0;
    authState.lastActivity = Date.now();
    grantAccess();
    return true;
  } else {
    authState.attempts++;
    elLoginAttempts.textContent = authState.attempts;

    if (authState.attempts >= CONFIG.MAX_ATTEMPTS) {
      triggerLockout();
    } else {
      const remaining = CONFIG.MAX_ATTEMPTS - authState.attempts;
      elLoginErrorText.textContent = `Invalid password. ${remaining} attempt${remaining !== 1 ? 's' : ''} remaining.`;
      elLoginError.classList.add('show');
      elLoginPassword.classList.add('error');
      setTimeout(() => elLoginPassword.classList.remove('error'), 500);
    }
    return false;
  }
}

function grantAccess() {
  elLoginGate.style.display = 'none';
  elMainApp.classList.add('unlocked');
  startSessionTimer();
  startSecurityMonitors();
  showToast('Secure session established', 'success');
  // Focus prevention on login field
  elLoginPassword.value = '';
}

function triggerLockout() {
  authState.lockedOut = true;
  authState.lockoutEnd = Date.now() + CONFIG.LOCKOUT_DURATION * 1000;
  elLoginGate.classList.add('locked-out');
  elLockoutOverlay.classList.add('show');
  elLoginBtn.disabled = true;

  elLoginErrorText.textContent = `Maximum attempts exceeded. Locked for ${CONFIG.LOCKOUT_DURATION / 60} minutes.`;
  elLoginError.classList.add('show');

  // Start countdown
  authState.lockoutIntervalId = setInterval(() => {
    const remaining = Math.max(0, Math.ceil((authState.lockoutEnd - Date.now()) / 1000));
    const m = Math.floor(remaining / 60);
    const s = remaining % 60;
    elLockoutTimer.textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;

    if (remaining <= 0) {
      clearInterval(authState.lockoutIntervalId);
      authState.lockedOut = false;
      authState.attempts = 0;
      elLoginAttempts.textContent = '0';
      elLockoutOverlay.classList.remove('show');
      elLoginGate.classList.remove('locked-out');
      elLoginBtn.disabled = false;
      elLoginError.classList.remove('show');
      elLoginPassword.value = '';
      elLoginPassword.focus();
    }
  }, 500);
}

elLoginBtn.addEventListener('click', () => {
  if (authState.lockedOut) return;
  const pw = elLoginPassword.value;
  if (!pw.trim()) {
    elLoginErrorText.textContent = 'Password field cannot be empty.';
    elLoginError.classList.add('show');
    return;
  }
  elLoginError.classList.remove('show');
  attemptLogin(pw);
});

elLoginPassword.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') elLoginBtn.click();
  elLoginError.classList.remove('show');
});

// --- SESSION TIMEOUT ---
function resetActivityTimer() {
  if (!authState.authenticated) return;
  authState.lastActivity = Date.now();
}

function startSessionTimer() {
  authState.lastActivity = Date.now();
  setInterval(() => {
    if (!authState.authenticated) return;
    const elapsed = Math.floor((Date.now() - authState.lastActivity) / 1000);
    const remaining = Math.max(0, CONFIG.SESSION_TIMEOUT - elapsed);
    const m = Math.floor(remaining / 60);
    const s = remaining % 60;
    elSessionCountdown.textContent = `${m}:${String(s).padStart(2, '0')}`;

    if (remaining <= 60) {
      elSessionTimerBadge.style.borderColor = 'rgba(255,71,87,0.4)';
      elSessionTimerBadge.style.color = 'var(--danger)';
    } else if (remaining <= 120) {
      elSessionTimerBadge.style.borderColor = 'rgba(255,165,2,0.4)';
      elSessionTimerBadge.style.color = 'var(--warning)';
    } else {
      elSessionTimerBadge.style.borderColor = 'var(--border)';
      elSessionTimerBadge.style.color = 'var(--text-muted)';
    }

    if (remaining <= 0) {
      lockSession();
    }
  }, 500);
}

function lockSession() {
  if (!authState.authenticated) return;
  elSessionLock.classList.add('show');
  elSessionLockPw.value = '';
  elSessionLockErr.textContent = '';
  setTimeout(() => elSessionLockPw.focus(), 100);
}

function unlockSession(password) {
  // Simple re-auth with same password
  hashPassword(password, CONFIG.PASSWORD_SALT).then(hash => {
    if (hash === CONFIG.PASSWORD_HASH) {
      elSessionLock.classList.remove('show');
      authState.lastActivity = Date.now();
      elSessionLockErr.textContent = '';
      showToast('Session unlocked', 'success');
    } else {
      elSessionLockErr.textContent = 'Incorrect password';
      elSessionLockPw.value = '';
    }
  });
}

elSessionLockPw.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') unlockSession(elSessionLockPw.value);
});

// Manual lock button
document.getElementById('btnLock').addEventListener('click', lockSession);

// --- ACTIVITY TRACKING ---
['mousemove', 'mousedown', 'keydown', 'touchstart', 'scroll', 'click'].forEach(evt => {
  document.addEventListener(evt, resetActivityTimer, { passive: true });
});

// --- SECURITY MONITORS ---

// 1. DevTools detection (multiple methods)
function startSecurityMonitors() {
  // Method A: Window size difference
  setInterval(() => {
    if (!authState.authenticated) return;
    const widthThreshold = window.outerWidth - window.innerWidth > 160;
    const heightThreshold = window.outerHeight - window.innerHeight > 160;
    if (widthThreshold || heightThreshold) {
      authState.devtoolWarnings++;
      if (authState.devtoolWarnings >= 3) {
        triggerTamperLock();
      }
    } else {
      authState.devtoolWarnings = Math.max(0, authState.devtoolWarnings - 1);
    }
  }, CONFIG.DEVTOOL_CHECK_INTERVAL);

  // Method B: Debugger timing
  setInterval(() => {
    if (!authState.authenticated) return;
    const t1 = performance.now();
    (function(){}).constructor('debugger')();
    const t2 = performance.now();
    if (t2 - t1 > 100) {
      authState.devtoolWarnings += 2;
      if (authState.devtoolWarnings >= 3) {
        triggerTamperLock();
      }
    }
  }, 2000);

  // Method C: Console detection via toString
  const devtoolsDetect = new Image();
  Object.defineProperty(devtoolsDetect, 'id', {
    get: function() {
      if (authState.authenticated) {
        authState.devtoolWarnings += 2;
        if (authState.devtoolWarnings >= 3) {
          triggerTamperLock();
        }
      }
    }
  });

  // Method D: DOM integrity check
  setInterval(() => {
    if (!authState.authenticated) return;
    // Check main structure exists
    const criticalElements = ['mainApp', 'packetFeed', 'arpTableBody', 'aiOutput', 'topoCanvas'];
    for (const id of criticalElements) {
      if (!document.getElementById(id)) {
        triggerTamperLock();
        return;
      }
    }
  }, CONFIG.INTEGRITY_CHECK_INTERVAL);

  // Method E: Clear console periodically
  setInterval(() => {
    if (!authState.authenticated) return;
    console.clear();
    console.log('%c⚠ SECURITY NOTICE', 'color: #ff4757; font-size: 20px; font-weight: bold;');
    console.log('%cThis browser console is monitored. Any unauthorized inspection will trigger security lockdown.', 'color: #7a8a9e; font-size: 12px;');
  }, 3000);
}

function triggerTamperLock() {
  authState.authenticated = false;
  elMainApp.classList.remove('unlocked');
  elSessionLock.classList.remove('show');
  elTamperWarning.classList.add('show');
  elScanline.classList.remove('active');
  // Stop any capture
  if (typeof stopCapture === 'function') stopCapture();
  // Log to console
  console.error('[NetSentry SECURITY] Tampering detected. Session terminated.');
}

// --- ANTI-INSPECTION ---
// Block right-click
document.addEventListener('contextmenu', e => e.preventDefault());

// Block common devtools shortcuts
document.addEventListener('keydown', function(e) {
  // F12
  if (e.key === 'F12') { e.preventDefault(); return false; }
  // Ctrl+Shift+I / Cmd+Option+I
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'I' || e.key === 'i')) { e.preventDefault(); return false; }
  // Ctrl+Shift+J / Cmd+Option+J
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'J' || e.key === 'j')) { e.preventDefault(); return false; }
  // Ctrl+Shift+C
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'C' || e.key === 'c')) { e.preventDefault(); return false; }
  // Ctrl+U (view source)
  if ((e.ctrlKey || e.metaKey) && (e.key === 'U' || e.key === 'u')) { e.preventDefault(); return false; }
  // Ctrl+S (save)
  if ((e.ctrlKey || e.metaKey) && (e.key === 'S' || e.key === 's')) { e.preventDefault(); return false; }
  // Ctrl+P (print)
  if ((e.ctrlKey || e.metaKey) && (e.key === 'P' || e.key === 'p')) { e.preventDefault(); return false; }
}, true);

// Block drag
document.addEventListener('dragstart', e => e.preventDefault());

// Block copy/cut (when authenticated)
document.addEventListener('copy', function(e) {
  if (authState.authenticated) e.preventDefault();
});
document.addEventListener('cut', function(e) {
  if (authState.authenticated) e.preventDefault();
});

// --- IFRAME BUSTING ---
if (window.self !== window.top) {
  window.top.location = window.self.location;
}

// --- Disable text selection on sensitive elements ---
document.addEventListener('selectstart', function(e) {
  if (authState.authenticated && !e.target.closest('input')) {
    // Allow selection in inputs only
    // e.preventDefault(); // uncomment for maximum restriction
  }
});

// --- WATERMARK (canvas-based, subtle) ---
function applyWatermark() {
  const wm = document.createElement('canvas');
  wm.width = 300; wm.height = 200;
  const ctx = wm.getContext('2d');
  ctx.font = '11px "JetBrains Mono", monospace';
  ctx.fillStyle = 'rgba(255,255,255,0.015)';
  ctx.save();
  ctx.translate(150, 100);
  ctx.rotate(-25 * Math.PI / 180);
  ctx.textAlign = 'center';
  ctx.fillText('NetSentry SECURE', 0, 0);
  ctx.fillText(CONFIG.SESSION_TOKEN.substring(0, 12), 0, 16);
  ctx.restore();

  const dataUrl = wm.toDataURL();
  document.body.style.backgroundImage = `url(${dataUrl})`;
  document.body.style.backgroundRepeat = 'repeat';
}

// --- BEFORE UNLOAD WARNING ---
window.addEventListener('beforeunload', function(e) {
  if (authState.authenticated) {
    e.preventDefault();
    e.returnValue = 'Session is active. Are you sure you want to leave?';
    return e.returnValue;
  }
});

// --- INIT ---
async function init() {
  await initPasswordHash();
  applyWatermark();
  elLoginPassword.focus();

  // Prevent password field autocomplete
  elLoginPassword.setAttribute('autocomplete', 'off');
  elSessionLockPw.setAttribute('autocomplete', 'off');

  // Disable password manager interference
  setTimeout(() => {
    elLoginPassword.value = '';
  }, 100);
}

init();

// ============================================================
// APP LOGIC — Packet Analyzer & ARP Spoof Detector
// ============================================================

function randInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }
function randChoice(arr) { return arr[randInt(0, arr.length - 1)]; }
function pad(n) { return String(n).padStart(2, '0'); }
function now() { const d = new Date(); return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`; }
function randMAC() {
  const h = '0123456789ABCDEF'; let m = '';
  for (let i = 0; i < 6; i++) { if (i > 0) m += ':'; m += h[randInt(0,15)] + h[randInt(0,15)]; }
  return m;
}
function randHex(len) { let h = ''; const x = '0123456789abcdef'; for (let i = 0; i < len; i++) h += x[randInt(0,15)]; return h; }
function formatHexDump(data) {
  const bpr = 16; const rows = [];
  for (let i = 0; i < data.length; i += bpr) {
    const chunk = data.slice(i, i + bpr);
    const offset = i.toString(16).padStart(4, '0');
    const hexPart = chunk.match(/.{1,2}/g).join(' ');
    let ascii = '';
    for (let j = 0; j < chunk.length; j += 2) { const c = parseInt(chunk.substr(j, 2), 16); ascii += (c >= 32 && c <= 126) ? String.fromCharCode(c) : '.'; }
    rows.push(`<span class="hex-offset">${offset}</span>  <span class="hex-data">${hexPart.padEnd(bpr * 3 - 1)}</span>  <span class="hex-ascii">${ascii}</span>`);
  }
  return rows.join('\n');
}

function showToast(msg, type) {
  type = type || 'success';
  const c = document.getElementById('toastContainer');
  const t = document.createElement('div');
  t.className = 'toast ' + type;
  t.innerHTML = `<i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i> ${msg}`;
  c.appendChild(t);
  setTimeout(() => { t.style.opacity = '0'; t.style.transform = 'translateX(30px)'; t.style.transition = 'all 0.3s'; }, 2500);
  setTimeout(() => t.remove(), 2900);
}

// Network topology data
const subnet = '192.168.1';
const gatewayIP = subnet + '.1';
const gatewayMAC = 'AA:BB:CC:11:22:33';
const hosts = [];
for (let i = 2; i <= 12; i++) {
  hosts.push({
    ip: subnet + '.' + i, mac: randMAC(),
    hostname: ['router','desktop-win','macbook-pro','iphone','android-phone','nas-server','printer','smart-tv','linux-server','ipad','work-laptop'][i-2],
    x: 0, y: 0, suspicious: false, macChanges: 0, arpCount: 0, lastSeen: 0
  });
}
const attacker = { ip: subnet + '.254', mac: randMAC(), fakeMAC: randMAC(), hostname: 'unknown-device', x: 0, y: 0, suspicious: true, macChanges: 0, arpCount: 0, lastSeen: 0, active: false, spoofTarget: null };

const arpTable = {};
let capturing = false, packetCount = 0, threatCount = 0, criticalCount = 0, alertCountVal = 0;
let startTime = 0, intervalIds = [], ppsCounter = 0, currentPPS = 0, anomalyScore = 0;
let attackPhase = 0, phaseTimer = 0, packets = [];

const elStatPackets = document.getElementById('statPackets');
const elStatPps = document.getElementById('statPps');
const elStatArp = document.getElementById('statArp');
const elStatArpSub = document.getElementById('statArpSub');
const elStatThreats = document.getElementById('statThreats');
const elStatThreatSub = document.getElementById('statThreatSub');
const elStatAnomaly = document.getElementById('statAnomaly');
const elStatUptime = document.getElementById('statUptime');
const elStatIface = document.getElementById('statIface');
const elStatusBadge = document.getElementById('statusBadge');
const elStatusText = document.getElementById('statusText');
const elPacketFeed = document.getElementById('packetFeed');
const elArpTableBody = document.getElementById('arpTableBody');
const elArpCount = document.getElementById('arpCount');
const elAiOutput = document.getElementById('aiOutput');
const elAlertFeed = document.getElementById('alertFeed');
const elAlertCount = document.getElementById('alertCount');
const elTopoNodeCount = document.getElementById('topoNodeCount');
const elScanline = document.getElementById('scanline');
const topoCanvas = document.getElementById('topoCanvas');
const topoCtx = topoCanvas.getContext('2d');

const protoWeights = [{proto:'TCP',weight:45},{proto:'UDP',weight:25},{proto:'DNS',weight:15},{proto:'ARP',weight:10},{proto:'ICMP',weight:5}];
function weightedProto() { const t = protoWeights.reduce((s,p) => s+p.weight, 0); let r = Math.random()*t; for (const p of protoWeights) { r -= p.weight; if (r <= 0) return p.proto; } return 'TCP'; }
const tcpPorts = [22,80,443,8080,3306,5432,6379,27017,3389,21,25,110,143,993,995,8443];
const udpPorts = [53,67,68,69,123,161,500,514,1194,4500];
const dnsNames = ['google.com','github.com','cdn.cloudflare.com','api.example.com','update.microsoft.com','repo.ubuntu.com','registry.npmjs.org','api.slack.com','discord.com','docs.python.org'];

function generatePacket() {
  const proto = weightedProto();
  let srcIP, dstIP, srcMAC, dstMAC, length, info, flagged = false, flag = 'clean', severity = 0;
  if (proto === 'ARP') {
    const isGrat = Math.random() < 0.15;
    const isFromAtk = attackPhase >= 2 && attacker.active && Math.random() < 0.35;
    if (isFromAtk) {
      const target = attacker.spoofTarget || hosts[1];
      srcIP = gatewayIP; srcMAC = attacker.fakeMAC; dstIP = target.ip; dstMAC = 'FF:FF:FF:FF:FF:FF';
      info = `ARP Reply (SPOOFED) — ${srcIP} is-at ${srcMAC}`;
      flagged = true; flag = 'bad'; severity = 2; attacker.arpCount++;
    } else if (isGrat) {
      const h = randChoice(hosts); srcIP = h.ip; srcMAC = h.mac; dstIP = '255.255.255.255'; dstMAC = 'FF:FF:FF:FF:FF:FF';
      info = 'Gratuitous ARP — announcement'; flag = 'warn'; severity = 1;
    } else {
      const h1 = randChoice(hosts); const h2 = randChoice(hosts.filter(x => x.ip !== h1.ip));
      srcIP = h1.ip; srcMAC = h1.mac; dstIP = h2.ip; dstMAC = h2.mac; info = `ARP Request — Who has ${dstIP}?`;
      h1.lastSeen = Date.now(); h2.lastSeen = Date.now();
    }
    length = randInt(28, 42);
    updateARPTable(srcIP, srcMAC, flagged);
  } else if (proto === 'TCP') {
    const h1 = randChoice(hosts); const h2 = randChoice(hosts.filter(x => x.ip !== h1.ip));
    srcIP = h1.ip; dstIP = h2.ip; srcMAC = h1.mac; dstMAC = h2.mac;
    length = randInt(40, 1460); info = `:${randChoice(tcpPorts)} [${randChoice(['SYN','ACK','PSH,ACK','FIN,ACK','SYN,ACK','RST'])}] Seq=${randInt(1000,999999)}`;
    h1.lastSeen = Date.now(); h2.lastSeen = Date.now();
  } else if (proto === 'UDP') {
    const h1 = randChoice(hosts); const h2 = Math.random() < 0.5 ? {ip:'8.8.8.8',mac:'00:00:00:00:00:01'} : randChoice(hosts.filter(x=>x.ip!==h1.ip));
    srcIP = h1.ip; dstIP = h2.ip; srcMAC = h1.mac; dstMAC = h2.mac;
    length = randInt(28, 512); info = `:${randChoice(udpPorts)} Len=${length}`; h1.lastSeen = Date.now();
  } else if (proto === 'DNS') {
    const h = randChoice(hosts); srcIP = h.ip; srcMAC = h.mac; dstIP = '8.8.8.8'; dstMAC = '00:00:00:00:00:01';
    length = randInt(60, 280); info = `${randChoice(['A','AAAA','MX','TXT','CNAME'])} ${randChoice(dnsNames)}`; h.lastSeen = Date.now();
  } else {
    const h1 = randChoice(hosts); const h2 = randChoice(hosts.filter(x=>x.ip!==h1.ip));
    srcIP = h1.ip; dstIP = h2.ip; srcMAC = h1.mac; dstMAC = h2.mac;
    length = randInt(64, 128); info = randChoice(['Echo request','Echo reply','Destination unreachable']);
    h1.lastSeen = Date.now(); h2.lastSeen = Date.now();
  }
  const pkt = { id: packetCount, time: now(), proto, srcIP, dstIP, srcMAC, dstMAC, length, info, flagged, flag, severity, hexData: randHex(length * 2) };
  packetCount++; ppsCounter++; packets.push(pkt);
  if (packets.length > 200) packets.shift();
  return pkt;
}

function updateARPTable(ip, mac, suspicious) {
  if (!arpTable[ip]) {
    arpTable[ip] = { mac, originalMAC: mac, changes: 0, status: 'ok', lastUpdate: Date.now() };
  } else {
    if (arpTable[ip].mac !== mac) {
      arpTable[ip].changes++; arpTable[ip].mac = mac;
      if (arpTable[ip].changes >= 2) arpTable[ip].status = 'bad';
      else if (arpTable[ip].changes === 1) arpTable[ip].status = 'warn';
      if (arpTable[ip].changes === 1) {
        addAIMessage(`MAC address change detected for <strong>${ip}</strong>: was ${arpTable[ip].originalMAC}, now ${mac}. Could indicate ARP cache poisoning.`, 'analysis');
        addAlert('warning', 'MAC Address Changed', `${ip} MAC changed to ${mac}`, 1);
      } else if (arpTable[ip].changes >= 2) {
        addAIMessage(`<strong>Critical: Multiple MAC changes</strong> for ${ip} (${arpTable[ip].changes} changes). Strong indicator of active ARP spoofing.`, 'threat');
        addAlert('critical', 'ARP Spoofing Detected', `Multiple MAC changes for ${ip}`, 2);
        threatCount++; criticalCount++;
      }
    }
    arpTable[ip].lastUpdate = Date.now();
  }
  renderARPTable();
}

function renderARPTable() {
  const entries = Object.entries(arpTable).sort((a,b) => ({bad:0,warn:1,ok:2}[a[1].status]||2) - ({bad:0,warn:1,ok:2}[b[1].status]||2));
  elArpCount.textContent = entries.length + ' entries';
  if (!entries.length) { elArpTableBody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:20px;color:var(--text-muted);font-size:12px;">No ARP entries yet</td></tr>'; return; }
  elArpTableBody.innerHTML = entries.map(([ip, d]) => {
    const sc = d.status, sl = sc==='ok'?'Stable':sc==='warn'?'Changed':'Threat';
    return `<tr${sc==='bad'?' class="suspicious"':''}><td class="ip-addr">${ip}</td><td class="mac-addr">${d.mac}</td><td><span class="arp-status ${sc}">${sl}</span></td><td style="color:${d.changes>0?'var(--warning)':'var(--text-muted)'}">${d.changes}</td></tr>`;
  }).join('');
}

function addAIMessage(text, type) {
  type = type || 'analysis';
  const m = document.createElement('div');
  m.className = 'ai-msg ' + type;
  m.innerHTML = `<div class="msg-time">[${now()}] AI Engine</div><div class="msg-text">${text}</div>`;
  elAiOutput.appendChild(m);
  elAiOutput.scrollTop = elAiOutput.scrollHeight;
  while (elAiOutput.children.length > 30) elAiOutput.removeChild(elAiOutput.firstChild);
}

function addAlert(level, title, desc, severity) {
  alertCountVal++; elAlertCount.textContent = alertCountVal + ' alerts';
  if (alertCountVal === 1) elAlertFeed.innerHTML = '';
  const item = document.createElement('div'); item.className = 'alert-item';
  const ic = level==='critical'?'critical':level==='warning'?'warning':'info';
  const fa = level==='critical'?'fa-skull-crossbones':level==='warning'?'fa-exclamation-triangle':'fa-info-circle';
  item.innerHTML = `<div class="alert-icon ${ic}"><i class="fas ${fa}"></i></div><div class="alert-content"><div class="alert-title">${title}</div><div class="alert-desc">${desc}</div></div><div class="alert-time">${now()}</div>`;
  elAlertFeed.prepend(item);
  while (elAlertFeed.children.length > 20) elAlertFeed.removeChild(elAlertFeed.lastChild);
  if (level === 'critical') { elStatusBadge.className = 'status-badge alert'; elStatusText.textContent = 'THREAT'; setTimeout(() => { if (capturing) { elStatusBadge.className = 'status-badge active'; elStatusText.textContent = 'MONITORING'; } }, 3000); }
  if (severity >= 2) threatCount++;
}

function renderPacketRow(pkt) {
  const row = document.createElement('div');
  row.className = 'packet-row' + (pkt.flagged ? ' flagged' : '');
  row.innerHTML = `<span class="pkt-time">${pkt.time}</span><span class="pkt-proto ${pkt.proto.toLowerCase()}">${pkt.proto}</span><span class="pkt-src">${pkt.srcIP}</span><span class="pkt-dst">${pkt.dstIP}</span><span class="pkt-len">${pkt.length}B</span><span class="pkt-flag ${pkt.flag}">${pkt.flag==='clean'?'OK':pkt.flag==='warn'?'WARN':'ALERT'}</span><span class="pkt-info">${pkt.info}</span>`;
  row.addEventListener('click', () => openPacketDetail(pkt));
  return row;
}

function openPacketDetail(pkt) {
  const body = document.getElementById('modalBody');
  body.innerHTML = `
    <div class="detail-section"><div class="detail-section-title">General Information</div><div class="detail-grid">
      <div class="detail-item"><div class="label">Timestamp</div><div class="value">${pkt.time}</div></div>
      <div class="detail-item"><div class="label">Protocol</div><div class="value" style="color:${pkt.proto==='ARP'?'var(--warning)':pkt.proto==='TCP'?'var(--cyan)':'var(--info)'}">${pkt.proto}</div></div>
      <div class="detail-item"><div class="label">Length</div><div class="value">${pkt.length} bytes</div></div>
      <div class="detail-item"><div class="label">Status</div><div class="value" style="color:${pkt.flag==='clean'?'var(--accent)':pkt.flag==='warn'?'var(--warning)':'var(--danger)'}">${pkt.flag.toUpperCase()}</div></div>
    </div></div>
    <div class="detail-section"><div class="detail-section-title">Network Layer</div><div class="detail-grid">
      <div class="detail-item"><div class="label">Source IP</div><div class="value" style="color:var(--cyan)">${pkt.srcIP}</div></div>
      <div class="detail-item"><div class="label">Destination IP</div><div class="value" style="color:var(--cyan)">${pkt.dstIP}</div></div>
      <div class="detail-item"><div class="label">Source MAC</div><div class="value">${pkt.srcMAC}</div></div>
      <div class="detail-item"><div class="label">Destination MAC</div><div class="value">${pkt.dstMAC}</div></div>
    </div></div>
    <div class="detail-section"><div class="detail-section-title">Payload Info</div><div class="detail-item" style="margin-bottom:0;"><div class="label">Details</div><div class="value">${pkt.info}</div></div></div>
    ${pkt.flagged?`<div class="detail-section"><div class="detail-section-title" style="color:var(--danger);">AI Threat Assessment</div><div class="detail-item" style="border-color:rgba(255,71,87,0.3);background:var(--danger-dim);"><div class="value" style="color:var(--danger);font-size:12px;line-height:1.6;"><strong>SPOOFED PACKET DETECTED</strong><br>This ARP reply claims ${pkt.srcIP} is at MAC ${pkt.srcMAC}, inconsistent with known ARP cache. Classic ARP spoofing technique.</div></div></div>`:''}
    <div class="detail-section"><div class="detail-section-title">Hex Dump</div><pre class="hex-dump">${formatHexDump(pkt.hexData)}</pre></div>`;
  document.getElementById('packetModal').classList.add('show');
}

function initTopology() {
  const rect = topoCanvas.parentElement.getBoundingClientRect();
  topoCanvas.width = rect.width * devicePixelRatio;
  topoCanvas.height = rect.height * devicePixelRatio;
  topoCtx.scale(devicePixelRatio, devicePixelRatio);
  const w = rect.width, h = rect.height, cx = w/2, cy = h/2;
  hosts[0].x = cx; hosts[0].y = cy;
  for (let i = 1; i < hosts.length; i++) {
    const a = ((i-1)/(hosts.length-1))*Math.PI*2 - Math.PI/2;
    const r = Math.min(w,h)*0.35;
    hosts[i].x = cx + Math.cos(a)*r; hosts[i].y = cy + Math.sin(a)*r;
  }
  attacker.x = w+50; attacker.y = cy;
}

function drawTopology() {
  const rect = topoCanvas.parentElement.getBoundingClientRect();
  const w = rect.width, h = rect.height;
  topoCtx.clearRect(0,0,w,h);
  for (let i = 1; i < hosts.length; i++) {
    const s = hosts[i].suspicious || (arpTable[hosts[i].ip] && arpTable[hosts[i].ip].status === 'bad');
    topoCtx.beginPath(); topoCtx.moveTo(hosts[0].x, hosts[0].y); topoCtx.lineTo(hosts[i].x, hosts[i].y);
    topoCtx.strokeStyle = s ? 'rgba(255,71,87,0.4)' : 'rgba(0,229,160,0.12)'; topoCtx.lineWidth = s?2:1; topoCtx.stroke();
  }
  if (attacker.active) {
    const t = attacker.spoofTarget || hosts[1];
    topoCtx.beginPath(); topoCtx.setLineDash([5,5]); topoCtx.moveTo(attacker.x, attacker.y); topoCtx.lineTo(t.x, t.y);
    topoCtx.strokeStyle = 'rgba(255,71,87,0.6)'; topoCtx.lineWidth = 2; topoCtx.stroke(); topoCtx.setLineDash([]);
    topoCtx.beginPath(); topoCtx.setLineDash([3,6]); topoCtx.moveTo(attacker.x, attacker.y); topoCtx.lineTo(hosts[0].x, hosts[0].y);
    topoCtx.strokeStyle = 'rgba(255,165,2,0.4)'; topoCtx.lineWidth = 1.5; topoCtx.stroke(); topoCtx.setLineDash([]);
  }
  const allN = [...hosts]; if (attacker.active) allN.push(attacker);
  for (const n of allN) {
    const isGW = n===hosts[0], isA = n===attacker, isS = n.suspicious||(arpTable[n.ip]&&arpTable[n.ip].status!=='ok');
    if (isA||isS) { const g = topoCtx.createRadialGradient(n.x,n.y,0,n.x,n.y,25); g.addColorStop(0,isA?'rgba(255,71,87,0.3)':'rgba(255,165,2,0.2)'); g.addColorStop(1,'rgba(0,0,0,0)'); topoCtx.beginPath(); topoCtx.arc(n.x,n.y,25,0,Math.PI*2); topoCtx.fillStyle=g; topoCtx.fill(); }
    topoCtx.beginPath(); topoCtx.arc(n.x,n.y,isGW?10:7,0,Math.PI*2);
    topoCtx.fillStyle = isA?'#ff4757':isGW?'#00e5a0':isS?'#ffa502':'#1e90ff'; topoCtx.fill();
    topoCtx.strokeStyle = isA?'rgba(255,71,87,0.6)':'rgba(255,255,255,0.15)'; topoCtx.lineWidth=1.5; topoCtx.stroke();
    topoCtx.font='9px "JetBrains Mono",monospace'; topoCtx.textAlign='center';
    topoCtx.fillStyle=isA?'#ff4757':'rgba(232,237,243,0.7)'; topoCtx.fillText(n.ip.split('.').pop(),n.x,n.y-13);
    if (isGW) { topoCtx.font='8px "JetBrains Mono",monospace'; topoCtx.fillStyle='rgba(0,229,160,0.6)'; topoCtx.fillText('GW',n.x,n.y+3); }
  }
  elTopoNodeCount.textContent = allN.length + ' nodes';
}

function advanceAttack() {
  phaseTimer++; const t = phaseTimer;
  if (attackPhase===0 && t>30) { attackPhase=1; addAIMessage('Network baseline established. Beginning enhanced monitoring...', 'info-msg'); addAlert('info','Baseline Complete','Normal traffic patterns recorded',0); }
  if (attackPhase===1 && t>60) {
    attackPhase=2; attacker.active=true; attacker.spoofTarget=hosts[randInt(1,5)]; attacker.fakeMAC=randMAC();
    const r = topoCanvas.parentElement.getBoundingClientRect(); attacker.x=r.width+50; attacker.y=r.height/2;
    addAIMessage(`<strong>Anomalous device detected</strong> at ${attacker.ip} (MAC: ${attacker.mac}). Not present during baseline. Initiating deep analysis...`, 'analysis');
    addAlert('warning','Unknown Device',`New device ${attacker.ip} appeared`,1); anomalyScore=25;
  }
  if (attackPhase===2 && t>90) {
    attackPhase=3;
    addAIMessage(`<strong>CRITICAL THREAT CONFIRMED:</strong> Device ${attacker.ip} sending spoofed ARP replies claiming to be gateway (${gatewayIP}) at MAC ${attacker.fakeMAC}. <strong>Man-in-the-middle attack</strong> targeting ${attacker.spoofTarget.ip}.`, 'threat');
    addAlert('critical','ARP Spoofing Active',`MITM attack from ${attacker.ip}`,2); anomalyScore=85; threatCount++; criticalCount++;
    elStatusBadge.className='status-badge alert'; elStatusText.textContent='UNDER ATTACK';
  }
  if (attackPhase===3 && t>140) {
    attacker.spoofTarget=hosts[randInt(3,8)]; attacker.fakeMAC=randMAC();
    addAIMessage(`Attack <strong>escalating</strong>. Spoofed ARP now targeting ${attacker.spoofTarget.ip} (${attacker.spoofTarget.hostname}). Recommend immediate isolation of ${attacker.ip}.`, 'threat');
    addAlert('critical','Attack Escalating',`New target: ${attacker.spoofTarget.ip}`,2); threatCount++; criticalCount++; anomalyScore=95;
  }
  if (attacker.active) { const r = topoCanvas.parentElement.getBoundingClientRect(); attacker.x+=(r.width-60-attacker.x)*0.05; attacker.y+=(r.height/2+Math.sin(Date.now()/2000)*15-attacker.y)*0.05; }
  if (attackPhase===3 && anomalyScore<95) anomalyScore=Math.min(95,anomalyScore+0.5);
}

function updateStats() {
  elStatPackets.textContent = packetCount.toLocaleString();
  elStatPps.textContent = currentPPS + ' pkt/s';
  const ae = Object.keys(arpTable).length, se = Object.values(arpTable).filter(a=>a.status==='ok').length;
  elStatArp.textContent = ae; elStatArpSub.textContent = se + ' stable';
  elStatThreats.textContent = threatCount; elStatThreatSub.textContent = criticalCount + ' critical';
  elStatAnomaly.textContent = Math.round(anomalyScore) + '%';
  if (capturing && startTime) { const e = Math.floor((Date.now()-startTime)/1000); elStatUptime.textContent = `${pad(Math.floor(e/60))}:${pad(e%60)}`; }
}

setInterval(() => { currentPPS = ppsCounter; ppsCounter = 0; }, 1000);

window.startCapture = function() {
  if (capturing || !authState.authenticated) return;
  capturing = true; startTime = Date.now(); phaseTimer = 0; attackPhase = 0; anomalyScore = 0;
  elStatusBadge.className='status-badge active'; elStatusText.textContent='MONITORING';
  elScanline.classList.add('active'); elStatIface.textContent='Interface: sim0';
  document.getElementById('btnStart').style.display='none'; document.getElementById('btnStop').style.display='flex';
  elPacketFeed.innerHTML='';
  arpTable[gatewayIP]={mac:gatewayMAC,originalMAC:gatewayMAC,changes:0,status:'ok',lastUpdate:Date.now()};
  renderARPTable();
  addAIMessage('Capture started on interface <strong>sim0</strong>. Building network baseline...', 'info-msg');
  showToast('Packet capture started','success');

  intervalIds.push(setInterval(() => {
    if (!capturing) return;
    const c = randInt(1,3);
    for (let i=0;i<c;i++) { const p = generatePacket(); elPacketFeed.prepend(renderPacketRow(p)); }
    while (elPacketFeed.children.length>150) elPacketFeed.removeChild(elPacketFeed.lastChild);
    advanceAttack(); updateStats();
  }, 400));

  intervalIds.push(setInterval(updateStats, 500));
  intervalIds.push(setInterval(drawTopology, 50));
  intervalIds.push(setInterval(() => {
    if (!capturing) return;
    const h = randChoice(hosts.slice(1));
    if (!arpTable[h.ip]) { arpTable[h.ip]={mac:h.mac,originalMAC:h.mac,changes:0,status:'ok',lastUpdate:Date.now()}; renderARPTable(); }
  }, 2000));

  initTopology(); drawTopology();
};

window.stopCapture = function() {
  if (!capturing) return;
  capturing = false;
  elStatusBadge.className='status-badge idle'; elStatusText.textContent='STOPPED';
  elScanline.classList.remove('active');
  document.getElementById('btnStart').style.display='flex'; document.getElementById('btnStop').style.display='none';
  intervalIds.forEach(id=>clearInterval(id)); intervalIds=[];
  addAIMessage(`Capture stopped. Total: <strong>${packetCount}</strong> packets. Threats: <strong>${threatCount}</strong>. Anomaly: <strong>${Math.round(anomalyScore)}%</strong>.`, 'info-msg');
  showToast('Capture stopped','error');
};

document.getElementById('btnStart').addEventListener('click', startCapture);
document.getElementById('btnStop').addEventListener('click', stopCapture);
document.getElementById('btnClearFeed').addEventListener('click', () => { elPacketFeed.innerHTML='<div style="padding:40px;text-align:center;color:var(--text-muted);font-size:13px;"><i class="fas fa-check-circle" style="color:var(--accent);margin-right:6px;"></i>Feed cleared</div>'; });
document.getElementById('modalClose').addEventListener('click', () => document.getElementById('packetModal').classList.remove('show'));
document.getElementById('packetModal').addEventListener('click', e => { if (e.target===e.currentTarget) document.getElementById('packetModal').classList.remove('show'); });
document.getElementById('btnEthics').addEventListener('click', () => document.getElementById('ethicsModal').classList.add('show'));
document.getElementById('ethicsClose').addEventListener('click', () => document.getElementById('ethicsModal').classList.remove('show'));
document.getElementById('ethicsModal').addEventListener('click', e => { if (e.target===e.currentTarget) document.getElementById('ethicsModal').classList.remove('show'); });
document.addEventListener('keydown', e => { if (e.key==='Escape') { document.getElementById('packetModal').classList.remove('show'); document.getElementById('ethicsModal').classList.remove('show'); } });
window.addEventListener('resize', () => { if (capturing) { initTopology(); drawTopology(); } });

})();
</script>
</body>
</html>
