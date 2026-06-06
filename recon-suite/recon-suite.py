#!/usr/bin/env python3
"""
recon-suite.py — Automated passive reconnaissance tool
Author : Ray1N_0x
License: CC BY-NC-ND 4.0

Modules
-------
  - Subdomain enumeration (crt.sh certificate transparency)
  - DNS records  (A, AAAA, MX, NS, TXT, CNAME)
  - WHOIS lookup
  - Port scan summary (top 1000 via socket probing)
  - JSON report output

Usage
-----
  python3 recon-suite.py -t example.com
  python3 recon-suite.py -t example.com -o report.json
  python3 recon-suite.py -t example.com --ports --timeout 2
"""

import argparse
import json
import socket
import sys
import time
import datetime
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── optional deps (graceful fallback) ───────────────────────────────────────
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import dns.resolver
    HAS_DNSPYTHON = True
except ImportError:
    HAS_DNSPYTHON = False

try:
    import whois as python_whois
    HAS_WHOIS = True
except ImportError:
    HAS_WHOIS = False


# ── constants ────────────────────────────────────────────────────────────────
TOP_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
    587, 631, 993, 995, 1723, 3306, 3389, 5900, 6379, 8080, 8443,
    8888, 27017
]

BANNER = r"""
  ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
  ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
  ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
  ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
  recon-suite.py  |  by Ray1N_0x
"""

RED   = "\033[91m"
GREEN = "\033[92m"
CYAN  = "\033[96m"
DIM   = "\033[2m"
RESET = "\033[0m"
BOLD  = "\033[1m"

def c(text, color): return f"{color}{text}{RESET}"
def ok(msg):   print(f"  {c('[+]', GREEN)} {msg}")
def warn(msg): print(f"  {c('[!]', RED)} {msg}")
def info(msg): print(f"  {c('[*]', CYAN)} {msg}")
def sep():     print(f"  {c('─' * 52, DIM)}")


def enum_subdomains(domain: str) -> list[str]:
    info(f"Querying crt.sh for {domain} ...")
    if not HAS_REQUESTS:
        warn("requests not installed — skipping subdomain enum")
        return []
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        subs = set()
        for entry in data:
            for name in entry.get("name_value", "").split("\n"):
                name = name.strip().lstrip("*.")
                if name.endswith(domain) and name != domain:
                    subs.add(name.lower())
        subs = sorted(subs)
        ok(f"Found {len(subs)} subdomains")
        return subs
    except Exception as e:
        warn(f"crt.sh error: {e}")
        return []


def get_dns(domain: str) -> dict:
    info(f"Resolving DNS records for {domain} ...")
    records: dict = {}

    if HAS_DNSPYTHON:
        rtypes = ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]
        for rtype in rtypes:
            try:
                answers = dns.resolver.resolve(domain, rtype, lifetime=5)
                records[rtype] = [str(r) for r in answers]
                ok(f"{rtype}: {len(records[rtype])} record(s)")
            except Exception:
                records[rtype] = []
    else:
        warn("dnspython not installed — basic A lookup only")
        try:
            ip = socket.gethostbyname(domain)
            records["A"] = [ip]
            ok(f"A: {ip}")
        except Exception as e:
            warn(f"DNS lookup failed: {e}")
            records["A"] = []

    return records


def get_whois(domain: str) -> dict:
    info(f"Running WHOIS for {domain} ...")
    if not HAS_WHOIS:
        warn("python-whois not installed — skipping")
        return {}
    try:
        w = python_whois.whois(domain)
        result = {}
        fields = [
            "registrar", "creation_date", "expiration_date",
            "updated_date", "name_servers", "status",
            "registrant_country", "org"
        ]
        for f in fields:
            val = getattr(w, f, None)
            if val is None:
                continue
            if isinstance(val, list):
                val = [str(v) for v in val]
            else:
                val = str(val)
            result[f] = val
        ok(f"Registrar: {result.get('registrar', 'N/A')}")
        return result
    except Exception as e:
        warn(f"WHOIS error: {e}")
        return {}


def _probe(host: str, port: int, timeout: float) -> tuple[int, bool, str]:
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            banner = ""
            try:
                s.settimeout(0.5)
                banner = s.recv(256).decode(errors="ignore").strip()[:80]
            except Exception:
                pass
            return port, True, banner
    except Exception:
        return port, False, ""

def port_scan(domain: str, ports: list[int], timeout: float, threads: int = 50) -> list[dict]:
    info(f"Scanning {len(ports)} ports on {domain} ...")
    try:
        ip = socket.gethostbyname(domain)
    except Exception:
        warn("Could not resolve host for port scan")
        return []

    open_ports = []
    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = {ex.submit(_probe, ip, p, timeout): p for p in ports}
        for fut in as_completed(futures):
            port, is_open, banner = fut.result()
            if is_open:
                entry = {"port": port, "state": "open"}
                if banner:
                    entry["banner"] = banner
                open_ports.append(entry)

    open_ports.sort(key=lambda x: x["port"])
    ok(f"{len(open_ports)} open port(s) found")
    for p in open_ports:
        b = f"  banner: {p['banner']}" if p.get("banner") else ""
        print(f"    {c(str(p['port']), GREEN)}/tcp  open{b}")
    return open_ports


def build_report(domain, subdomains, dns_records, whois_data, ports) -> dict:
    return {
        "meta": {
            "tool": "recon-suite.py",
            "author": "Ray1N_0x",
            "target": domain,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        },
        "subdomains": subdomains,
        "dns": dns_records,
        "whois": whois_data,
        "ports": ports
    }


def main():
    print(c(BANNER, RED))

    parser = argparse.ArgumentParser(
        description="recon-suite — passive recon automation by Ray1N_0x"
    )
    parser.add_argument("-t", "--target",   required=True, help="Target domain")
    parser.add_argument("-o", "--output",   default=None,  help="Output JSON file (optional)")
    parser.add_argument("--ports",          action="store_true", help="Enable port scan")
    parser.add_argument("--timeout",        type=float, default=1.5, help="Port scan timeout (default: 1.5s)")
    parser.add_argument("--threads",        type=int,   default=50,  help="Port scan threads (default: 50)")
    parser.add_argument("--no-subdomains",  action="store_true", help="Skip subdomain enum")
    parser.add_argument("--no-whois",       action="store_true", help="Skip WHOIS")
    args = parser.parse_args()

    domain = args.target.strip().lower().removeprefix("http://").removeprefix("https://").split("/")[0]

    print(f"  {BOLD}Target :{RESET} {c(domain, CYAN)}")
    print(f"  {BOLD}Started:{RESET} {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    sep()

    t0 = time.time()

    subdomains = [] if args.no_subdomains else enum_subdomains(domain)
    sep()

    dns_records = get_dns(domain)
    sep()

    whois_data = {} if args.no_whois else get_whois(domain)
    sep()

    ports = []
    if args.ports:
        ports = port_scan(domain, TOP_PORTS, args.timeout, args.threads)
        sep()

    report = build_report(domain, subdomains, dns_records, whois_data, ports)

    elapsed = round(time.time() - t0, 2)
    ok(f"Scan completed in {elapsed}s")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2, default=str)
        ok(f"Report saved → {args.output}")
    else:
        print("\n" + json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
