```
  ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
  ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
  ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
  ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
  recon-suite.py  |  by Ray1N_0x
```

![Python](https://img.shields.io/badge/python-3.10%2B-red?style=flat-square&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-active-red?style=flat-square)

> Automated passive reconnaissance tool. Subdomain enum, DNS records, WHOIS, port scan — structured JSON output.

---

## OVERVIEW

`recon-suite.py` is a passive recon automation script built for penetration testers and CTF players. It chains multiple reconnaissance techniques into a single run and outputs a clean, structured JSON report — ready for further analysis or documentation.

No heavy frameworks. No bloat. Pure Python.

---

## MODULES

```
  [subdomain]   Certificate Transparency via crt.sh
  [dns]         A · AAAA · MX · NS · TXT · CNAME records
  [whois]       Registrar · creation/expiry dates · nameservers
  [portscan]    Top ports · banner grabbing · threaded
```

---

## INSTALL

```bash
git clone https://github.com/Ray1N-0x/recon-suite
cd recon-suite
pip install -r requirements.txt
```

**requirements.txt**
```
requests
dnspython
python-whois
```

> All dependencies are optional — the tool runs with graceful fallback if any are missing.

---

## USAGE

```bash
# Basic recon
python3 recon-suite.py -t example.com

# Save output to JSON
python3 recon-suite.py -t example.com -o report.json

# Full scan with port scan
python3 recon-suite.py -t example.com -o report.json --ports

# Skip WHOIS, custom timeout
python3 recon-suite.py -t example.com --no-whois --timeout 2
```

---

## FLAGS

```
  -t,  --target          Target domain                  (required)
  -o,  --output          Output JSON file path          (optional)
       --ports           Enable port scan
       --timeout         Socket timeout in seconds      (default: 1.5)
       --threads         Concurrent threads             (default: 50)
       --no-subdomains   Skip subdomain enumeration
       --no-whois        Skip WHOIS lookup
```

---

## OUTPUT

```json
{
  "meta": {
    "tool": "recon-suite.py",
    "author": "Ray1N_0x",
    "target": "example.com",
    "timestamp": "2024-11-01T14:32:01Z"
  },
  "subdomains": [
    "api.example.com",
    "dev.example.com",
    "mail.example.com"
  ],
  "dns": {
    "A":   ["93.184.216.34"],
    "MX":  ["10 mail.example.com."],
    "NS":  ["ns1.example.com.", "ns2.example.com."],
    "TXT": ["v=spf1 include:_spf.example.com ~all"]
  },
  "whois": {
    "registrar":        "ICANN",
    "creation_date":    "1995-08-14",
    "expiration_date":  "2025-08-13",
    "name_servers":     ["NS1.EXAMPLE.COM", "NS2.EXAMPLE.COM"]
  },
  "ports": [
    { "port": 80,  "state": "open" },
    { "port": 443, "state": "open", "banner": "nginx/1.24.0" }
  ]
}
```

---

## DISCLAIMER

This tool is intended for **authorized penetration testing and educational use only**.
Do not use against systems you do not have explicit permission to test.
The author is not responsible for any misuse or damage caused by this tool.

---

## LICENSE

```
MIT License

Copyright (c) 2025 Ray1N

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

© Ray1N_0x — All Rights Reserved
```
