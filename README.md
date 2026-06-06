# Offensive Security Tools

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Bash 4.0+](https://img.shields.io/badge/bash-4.0+-green.svg)](https://www.gnu.org/software/bash/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A curated collection of **modular security tools** for penetration testing, CTF competitions, and red teaming.  
Currently includes:

- **Dynamic Payload Generator** (`payload-gen.py`) – SQLi, XSS, SSTI, Command Injection  
- **Privilege Escalation Enumeration** (`privesc-check.sh`) – Linux post‑exploitation audit
- **Passive Reconnaissance Suite** (`recon-suite.py`) – Automated information gathering with JSON reporting

All tools are **self‑contained**, have **minimal dependencies**, and are ready to use on Linux/macOS.

---

## Tools Overview

### 1. `payload-gen.py` – Dynamic Payload Generator

Generate **thousands of unique injection payloads** on the fly (no hardcoded lists).  
Supports:

- **SQL Injection** (error‑based, union, time‑based, blind)
- **Cross‑Site Scripting (XSS)** (HTML, attribute, URI contexts)
- **Server‑Side Template Injection (SSTI)** (Jinja2, Twig, Freemarker, etc.)
- **Command Injection** (Linux / Windows patterns)

**Key features:**
- Context‑aware generation (`--context`)
- Bypass techniques (`--bypass`)
- Encoding chains (`--encode url b64 hex ...`)
- Output to plain text or JSON
- User‑controlled volume (`-n` up to 100,000+

### 2. `privesc-check.sh` – Privilege Escalation Scanner

Post‑exploitation script that enumerates **common Linux privilege escalation vectors**:

- SUID / SGID binaries
- Writable `$PATH` directories
- Cron jobs (user & system)
- Sudo misconfigurations (`NOPASSWD`, dangerous commands)
- Kernel version (potential exploits)
- Capabilities, environment variables (`LD_PRELOAD`)
- Readable sensitive files (`/etc/shadow`, SSH keys)
- Writable systemd unit files
- Open listening ports
- Container detection (Docker, LXC)

**Key features:**
- No external dependencies (pure bash)
- Color‑coded output (red = high risk)
- Read‑only – safe for live systems
- Easily extensible

## 3. `recon-suite.py` – Passive Reconnaissance Automation

A **passive reconnaissance automation script** built for penetration testers and CTF players. It chains multiple reconnaissance techniques into a single run and outputs a clean, structured **JSON report** — ready for further analysis or documentation.

**Capabilities include:**

- **Subdomain enumeration** – Certificate Transparency logs, DNS brute‑force, API integrations
- **WHOIS lookups** – Domain registration and expiration data
- **DNS enumeration** – A, AAAA, MX, TXT, NS, CNAME records
- **Technology fingerprinting** – HTTP headers, cookies, server banners
- **Endpoint discovery** – Directory/file fuzzing (optional)
- **Port scanning** – Common service ports with banner grabbing
- **Screenshotting** – Web interface preview (optional)

**Key features:**
- **Passive by design** – minimal footprint, no aggressive scanning
- **Modular architecture** – easy to add new data sources
- **Structured JSON output** – ready for parsing, storage, or reporting
- **Multi‑threaded** – fast execution with configurable concurrency
- **CTF‑ready** – quick setup, no complex configuration

---


