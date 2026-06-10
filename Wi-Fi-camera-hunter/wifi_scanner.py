from scapy.all import *
from colorama import Fore
import os
import time


def scan_wifi(iface, timeout=15):

    print(f"{Fore.CYAN}Scanning Wi-Fi networks on interface {iface}...")

    networks = {}

    def pkt_handler(pkt):

        if not pkt.haslayer(Dot11):
            return

        if pkt.type == 0 and pkt.subtype in [5, 8]:

            bssid = pkt.addr2

            if not bssid:
                return

            ssid = "<hidden>"

            try:
                if hasattr(pkt, "info") and pkt.info:
                    ssid = pkt.info.decode(errors="ignore")
            except Exception:
                pass

            channel = "unknown"

            try:
                elt = pkt.getlayer(Dot11Elt)

                while elt:
                    if getattr(elt, "ID", None) == 3:
                        if len(elt.info) > 0:
                            channel = elt.info[0]
                        break

                    elt = elt.payload.getlayer(Dot11Elt)

            except Exception:
                pass

            signal = getattr(pkt, "dBm_AntSignal", "N/A")

            networks[bssid] = {
                "SSID": ssid,
                "BSSID": bssid,
                "Channel": channel,
                "Signal": signal,
            }

    channels = [1, 6, 11]

    per_channel = max(3, timeout // len(channels))

    for ch in channels:

        print(f"{Fore.YELLOW}Scanning channel {ch}...")

        os.system(f"iw dev {iface} set channel {ch} >/dev/null 2>&1")

        sniff(
            iface=iface,
            prn=pkt_handler,
            timeout=per_channel,
            store=0
        )

    result = list(networks.values())

    print(f"{Fore.GREEN}Found networks: {len(result)}")

    return result