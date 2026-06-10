from colorama import Fore
import subprocess
import os

def connect_to_network(ssid, password=None, iface="wlan0"):
    print(f"Connecting to {ssid}...")

    subprocess.run(["ip", "link", "set", iface, "down"])
    subprocess.run(["iwconfig", iface, "mode", "managed"])
    subprocess.run(["ip", "link", "set", iface, "up"])

    conf = f"""ctrl_interface=DIR=/var/run/wpa_supplicant
network={{
    ssid="{ssid}"
    psk="{password}"
    key_mgmt=WPA-PSK
}}""" if password else f"""ctrl_interface=DIR=/var/run/wpa_supplicant
network={{
    ssid="{ssid}"
    key_mgmt=NONE
}}"""

    with open("temp/wpa.conf", "w") as f:
        f.write(conf)

    subprocess.run(["wpa_supplicant", "-B", "-i", iface, "-c", "temp/wpa.conf"])
    subprocess.run(["dhclient", iface])
    print(f"{Fore.GREEN}Connected. IP: {subprocess.check_output(['ip', 'addr', 'show', iface]).decode()}")
