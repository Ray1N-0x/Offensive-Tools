from scapy.all import *
from colorama import Fore
from collections import defaultdict

OUI_CAMERA = {
    "Hikvision": ["44:8A:5B", "B4:2A:39", "F4:8E:38"],
    "Dahua": ["3C:EF:8C", "E0:50:8B"],
    "Axis": ["AC:CC:8E", "00:1B:DD"]
}

def passive_monitor(iface, timeout=30):
    print(f"{Fore.CYAN}Passive monitoring ({timeout} sec)...")
    devices = defaultdict(set)
    mdns = []
    upnp = []

    def handler(pkt):
        if pkt.haslayer(Dot11):
            if pkt.addr2:
                devices[pkt.addr2].add("src")
            if pkt.addr1:
                devices[pkt.addr1].add("dst")

        if pkt.haslayer(UDP) and pkt[UDP].dport == 5353:
            try:
                if b"_rtsp._tcp" in bytes(pkt) or b"_onvif._tcp" in bytes(pkt):
                    mdns.append(pkt.summary())
            except:
                pass

        if pkt.haslayer(UDP) and pkt[UDP].dport == 1900:
            upnp.append(pkt.summary())

    sniff(iface=iface, prn=handler, timeout=timeout, store=0)

    camera_macs = []
    for mac in devices:
        oui = mac[:8].upper().replace(":", "")
        for vendor, prefixes in OUI_CAMERA.items():
            if any(oui.startswith(p.replace(":", "")) for p in prefixes):
                camera_macs.append((mac, vendor))

    return {"camera_macs": camera_macs, "mdns": mdns[:10], "upnp": upnp[:5]}
