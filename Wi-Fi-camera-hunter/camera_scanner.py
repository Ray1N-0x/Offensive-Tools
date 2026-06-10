import nmap
import requests
from zeep import Client
from zeep.exceptions import Fault

def scan_subnet(subnet="192.168.1.0/24"):
    nm = nmap.PortScanner()
    print(f"Scanning subnet {subnet}...")
    nm.scan(hosts=subnet, arguments='-p 80,443,554,8000,8080,37777,34567 --open')

    cameras = []
    for host in nm.all_hosts():
        for port in nm[host]['tcp']:
            if nm[host]['tcp'][port]['state'] == 'open':
                cameras.append((host, port))
    return cameras

def check_rtsp(ip, port=554):
    try:
        r = requests.get(f"http://{ip}:{port}/", timeout=3)
        if "RTSP" in r.text or r.status_code in (200, 401):
            return True
    except:
        pass
    return False

def try_default_credentials(ip, port=554):
    creds = [("admin", ""), ("admin", "admin"), ("admin", "12345"), ("root", "root")]
    for user, pwd in creds:
        try:
            print(f"Trying {user}:{pwd} on {ip}")
            return f"rtsp://{user}:{pwd}@{ip}:{port}/Streaming/Channels/101"
        except:
            continue
    return None
