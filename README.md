# 🦇 MidnightRAT Payload

**Author:** Syed Sharjeel Zaidi  
**Tool Name:** MidnightRAT Payload  
**License:** MIT License  
**Category:** Red Team / Adversary Simulation / C2 Payload

---

## 🧠 What is MidnightRAT?

**MidnightRAT** is a stealthy, modular, Python-based **Command and Control (C2) payload** built for:

- Red team operations  
- Adversary emulation  
- Malware analysis labs  
- Detection engineering

This payload simulates the behavior of **Advanced Persistent Threat (APT)** actors and provides a testing ground for EDRs, NDRs, SIEMs, and blue team monitoring.

---

## 🧰 Features

| Feature                        | Description |
|-------------------------------|-------------|
| 🔐 AES-CBC Encrypted C2        | Secure comms using PBKDF2-derived AES keys with IV |
| 💤 Adaptive Sleep Calculus     | Dynamically adjusts sleep intervals to avoid pattern detection |
| 🎭 Runtime Polymorphism        | Function renaming at runtime to avoid static signature detection |
| 🧬 Simulated Process Migration | Scans for low-CPU processes and selects one (logic placeholder) |
| 🖥️ Remote Syscall Execution    | Executes shell commands sent from C2 server |
| 🧪 LSASS Stub                  | Simulated LSASS access logic (non-functional placeholder) |

---

## ⚠️ Legal Disclaimer

> This software is provided **strictly for educational and authorized red team use only**.

- ❌ Do **NOT** use this payload on unauthorized systems or networks.  
- ✅ Only deploy in **labs, sandboxes, honeypots, or environments** where you have explicit permission.  
- ⚖️ The author assumes **no responsibility** for misuse or damage caused.

---
