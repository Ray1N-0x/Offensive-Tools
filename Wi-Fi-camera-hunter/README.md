#  Wi-Fi Camera Hunter

<div align="center">

**Automated tool for detecting and analyzing Wi-Fi security cameras**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-red.svg)](https://linux.org)

</div>

---

## 📋 Contents

- [Description](#description)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Automatic Installation](#automatic-installation)
- [Manual Installation](#manual-installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Frequently Asked Questions](#faq)
- [License](#license)

---

## Description

**Wi-Fi Camera Hunter** is a powerful tool for automatically detecting, analyzing, and connecting to IP surveillance cameras in wireless networks. It is designed for testing the security of your own networks and auditing your Wi-Fi infrastructure.

### Key Features:
- 🔍 Scanning Wi-Fi networks within range
- 🎯 Automatic device manufacturer detection by MAC (OUI)
- 📊 Traffic analysis and camera detection
- 🔐 Capturing and cracking WPA/WPA2 handshake
- 🎥 Searching for RTSP streams with default passwords
- 📝 Saving results to a database

---

## Features

| Function | Description | Status |
|---------|---------|--------|
| **Wi-Fi Scan** | Detect all networks in range |
| **OUI Detection** | Database of 1000+ manufacturers |
| **Client Analysis** | Show Connected Devices |
| **Handshake Capture** | Collect Handshakes for Hacking |
| **Password Cracking** | Aircrack-ng + Dictionaries |
| **Camera Search** | ONVIF, RTSP, HTTP |
| **Auto-Connect** | To a Hackered Network |
| **Save Results** | To Files and Database |
| **Telegram notifications** | When a camera is found |
| **Web interface** | Remote control |

---

## Requirements

### System Requirements
| Component | Minimum |
|-----------|-----------|
| **OS** | Linux (Kali, Ubuntu, Arch, BlackArch) |
| **Python** | 3.10+ |
| **Wi-Fi Adapter** | With monitor mode and packet injection support |
| **RAM** | 512 MB |
| **Disk Space** | 1 GB |

### Supported Wi-Fi Chipsets
| Manufacturer | Models |
|---------------|--------|
| **Atheros** | AR9271, AR9287, AR9285 |
| **Ralink** | RT3070, RT5370, RT5572 |
| **Realtek** | RTL8812AU, RTL8814AU |
| **Intel** | AX200, AX210, 8265 |

---

## Installation

1. copy the repository
```bash
git clone https://github.com/Ray1N-0x/Offensive-Tools/Wi-Fi-camera-hunter 
cd Wi-Fi-camera-hunter
```
2. Installing system dependencies

Arch Linux / Manjaro / BlackArch:
```bash

sudo pacman -S aircrack-ng nmap vlc ffmpeg wpa_supplicant dhclient net-tools wireless_tools
```
Ubuntu / Debian / Kali:
```bash

sudo apt update
sudo apt install aircrack-ng nmap vlc ffmpeg wpasupplicant isc-dhcp-client net-tools wireless-tools
```
3. Downloading a cracking dictionary
```bash

# Download rockyou.txt (password dictionary)
sudo wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt -O /usr/share/wordlists/rockyou.txt

# Or unzip an existing one
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
```
4. Installing Python Libraries
```bash

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

change paths to dictionaries

# Install dependencies
pip install -r requirements.txt
```
Usage
Basic Launch
```bash

# With root privileges (required!)
sudo python3 auto_hunter.py --iface wlan0

# For the wlan1 interface
sudo python3 auto_hunter.py --iface wlan1
```
---

## Contacs
Name: Ray1N
Telegram: https://t.me/Ray1N_0x
Email: Ray1N_0x@proton.me
