#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}[+] Starting Privilege Escalation Enumeration${NC}"
echo "=============================================="

echo -e "${GREEN}[*] Current user and groups:${NC}"
id
echo ""

echo -e "${GREEN}[*] Kernel version:${NC}"
uname -a
cat /etc/os-release 2>/dev/null | grep -E "PRETTY_NAME|NAME|VERSION"
echo ""

echo -e "${GREEN}[*] SUID binaries:${NC}"
find / -perm -4000 -type f -exec ls -la {} \; 2>/dev/null
echo ""
echo -e "${GREEN}[*] SGID binaries:${NC}"
find / -perm -2000 -type f -exec ls -la {} \; 2>/dev/null
echo ""

echo -e "${GREEN}[*] Writable directories in PATH:${NC}"
echo "$PATH" | tr ':' '\n' | while read dir; do
    if [ -w "$dir" ]; then
        echo -e "${RED}[W] $dir is writable${NC}"
    fi
done
echo ""
echo -e "${GREEN}[*] Sudo privileges (user may be prompted for password):${NC}"
sudo -l 2>/dev/null || echo "Unable to run sudo -l (no sudo or password required)"
echo ""

echo -e "${GREEN}[*] Checking sudoers for NOPASSWD entries:${NC}"
grep -r "^[^#]*NOPASSWD" /etc/sudoers /etc/sudoers.d/ 2>/dev/null || echo "No NOPASSWD entries found"
echo ""

echo -e "${GREEN}[*] Cron jobs (system and user):${NC}"
ls -la /etc/cron* 2>/dev/null
cat /etc/crontab 2>/dev/null
for user in $(cut -f1 -d: /etc/passwd); do
    crontab -u "$user" -l 2>/dev/null | head -n 5
done
echo ""

echo -e "${GREEN}[*] Writable files in /etc (potential config hijack):${NC}"
find /etc -writable -type f 2>/dev/null | head -20
echo ""

echo -e "${GREEN}[*] Writable directories in /var, /tmp, /dev/shm:${NC}"
ls -ld /tmp /var/tmp /dev/shm 2>/dev/null
echo ""

echo -e "${GREEN}[*] Capabilities (getcap):${NC}"
getcap -r / 2>/dev/null || echo "getcap not found or no capabilities"
echo ""

echo -e "${GREEN}[*] Processes owned by root (top 20 CPU/mem):${NC}"
ps aux | grep -E "^root" | head -20
echo ""

echo -e "${GREEN}[*] Package managers (search for outdated):${NC}"
if command -v dpkg &>/dev/null; then
    dpkg -l | head -20
elif command -v rpm &>/dev/null; then
    rpm -qa | head -20
elif command -v pacman &>/dev/null; then
    pacman -Q | head -20
else
    echo "No known package manager found"
fi
echo ""

echo -e "${GREEN}[*] Checking for readable sensitive files:${NC}"
files=("/etc/passwd" "/etc/shadow" "/etc/sudoers" "/root/.bash_history" "/home/*/.bash_history" "/home/*/.ssh/id_rsa" "/root/.ssh/id_rsa")
for f in "${files[@]}"; do
    if ls $f 2>/dev/null | head -1; then
        if [ -r "$f" ]; then
            echo -e "${RED}[R] $f is readable${NC}"
        else
            echo "   $f exists but not readable"
        fi
    fi
done
echo ""

echo -e "${GREEN}[*] Writable systemd service files:${NC}"
find /etc/systemd/system /lib/systemd/system -type f -writable 2>/dev/null | head -10
echo ""

echo -e "${GREEN}[*] Dangerous environment variables:${NC}"
env | grep -E "LD_PRELOAD|LD_LIBRARY_PATH|PATH|SUDO"
echo ""

echo -e "${GREEN}[*] Listening ports (possible service exploitation):${NC}"
ss -tulpn 2>/dev/null || netstat -tulpn 2>/dev/null || echo "netstat/ss not available"
echo ""

echo -e "${GREEN}[*] Container / VM detection:${NC}"
if [ -f /.dockerenv ]; then echo "Inside Docker container"; fi
if grep -q docker /proc/1/cgroup 2>/dev/null; then echo "Docker cgroup detected"; fi
if [ -f /proc/1/environ ]; then strings /proc/1/environ | grep -i container; fi
echo ""

echo -e "${YELLOW}[+] Enumeration complete. Review highlighted findings manually.${NC}"