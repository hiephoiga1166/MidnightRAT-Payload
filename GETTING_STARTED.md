# 🚀 Getting Started with MidnightRAT

Welcome to **MidnightRAT** — a Python-based AES-encrypted Command & Control (C2) simulation payload for red teamers and security researchers.

This guide will walk you through all the important concepts, setup, and required configurations so you can run this payload in a test/lab environment.

---

## 📦 What You Get in This Repo

| File              | Description                              |
|-------------------|------------------------------------------|
| `midnight_rat.py` | The main RAT payload                     |
| `listener.py`     | Encrypted command & control listener     |
| `requirements.txt`| Python dependencies                      |
| `USAGE.md`        | Full usage guide                         |
| `LICENSE`         | MIT License (open source)                |

---

## ⚠️ Legal & Ethical Notice

**This tool is for educational and authorized red team use only.**  
Using this tool on unauthorized systems is illegal and unethical.  
Always test in a safe, isolated, permissioned environment.

---

## 🔐 Encryption & Key Info

MidnightRAT uses **AES-256-CBC encryption** for secure comms.

| Component        | Value                                      |
|------------------|--------------------------------------------|
| Shared Secret    | `b"k3yshar3dsecr3t123!"` *(default)*        |
| Key Derivation   | PBKDF2-HMAC (SHA256, 100k iterations)       |
| Salt             | Random per session (sent by RAT to server) |
| IV               | Random per message                         |
| Padding          | PKCS7                                      |

> 🔁 If you change the `shared_secret`, make sure you update it **in both**:
> - `midnight_rat.py`
> - `listener.py`

---

## 🧠 What YOU Need to Change

| File             | What to Edit                             | Example                  |
|------------------|-------------------------------------------|--------------------------|
| `midnight_rat.py`| `c2_host` and `c2_port` values            | `"192.168.1.10", 4444`   |
| `listener.py`    | `C2_PORT` if different                    | `C2_PORT = 4444`         |
| `shared_secret`  | (optional) match on both sides            | `b"newSecretHere123!"`   |

No other changes are needed unless you want to customize the tool.

---

## 🛠 Prerequisites

- ✅ Python 3.8+
- ✅ pip installed
- ✅ Local test lab, VM, or sandbox (do **not** run on real host)

---

## 🚀 How to Run (Quick Summary)

### ✅ 1. Install Requirements
```bash
pip install -r requirements.txt
```

### ✅ 2. Start the Listener (C2 Server)
```bash
python listener.py
```

### ✅ 3. Run the Payload on Victim Machine
```bash
python midnight_rat.py
```

### ✅ 4. Send Commands from Listener
```bash
MidnightRAT > whoami
MidnightRAT > ipconfig
```

### 📋 Default Supported Commands

| Type      | Description                                                   |
| --------- | ------------------------------------------------------------- |
| `syscall` | Run any OS command (e.g. `whoami`, `dir`, `ls`)               |
| `sleep`   | Adjust delay between beaconing                                |
| `lsass`   | Placeholder for LSASS dumping (Windows-only, not implemented) |

### ✅ Things to Remember

    ✅ shared_secret must be the same on both ends

    ✅ Listener should be started before running the payload

    ✅ Use isolated VMs or a controlled lab

    ❌ Never use this on public or production systems

    ✅ Port used (default: 8080) must be open on the listener

### ❓ Troubleshooting

| Issue                    | Solution                                  |
| ------------------------ | ----------------------------------------- |
| RAT not connecting       | Check host/port, firewall, listener up?   |
| Encrypted response error | Confirm both sides use same secret & salt |
| Listener crashes         | Use Python 3.8+, verify dependencies      |
| No response from command | Try basic commands like `whoami`          |

# 🙋 Author & Contact

## Developed by Syed Sharjeel Zaidi
### Follow the repo and stay tuned for future modules like:

    File upload/download

    Keylogger (lab-only)

    Screenshot capture

    Persistence (demo only)
