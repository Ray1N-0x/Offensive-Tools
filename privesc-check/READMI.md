# privesc-check.sh – Privilege Escalation Enumeration

**Post‑exploitation script** to identify misconfigurations, vulnerable services, and common privilege escalation vectors on Linux systems.

![Bash](https://img.shields.io/badge/bash-4.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## Overview

`privesc-check.sh` automates the collection of system information that can lead to **privilege escalation** (user → root). It checks:

- SUID/SGID binaries
- Writable `$PATH` directories
- Cron jobs
- Sudo misconfigurations (including `NOPASSWD`)
- Kernel version (potential exploits)
- Capabilities, environment variables, open ports
- Sensitive file permissions (`/etc/shadow`, SSH keys, etc.)
- Container detection (Docker, LXC)

No external dependencies – runs with standard Linux tools (`find`, `grep`, `id`, `sudo`, etc.)

---

## Features

- **Lightweight & fast** – single bash script, minimal overhead.
- **Comprehensive checks** – 15+ enumeration categories.
- **Color output** – highlights risks in red/yellow.
- **Safe** – read‑only, no system modifications.
- **Portable** – works on most Linux distributions (Debian, RHEL, Arch, Alpine, etc.).

---

## Usage

### 1. Transfer the script to the target machine

```bash
# Using wget
wget https://your-server/privesc-check.sh

# Using curl
curl -O https://your-server/privesc-check.sh

# Or copy via SCP / netcat / base64

chmod +x privesc-check.sh

./privesc-check.sh 
         
./privesc-check.sh > privesc_report.txt
```

---

**This tool is intended for authorised penetration testing and educational purposes only. The user assumes all responsibility for compliance with applicable laws.**
