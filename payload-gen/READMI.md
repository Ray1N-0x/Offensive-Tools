# payload-gen.py – Dynamic Payload Generator

**No external dependencies.**  
Generate thousands of unique injection payloads for **SQLi, XSS, SSTI, and Command Injection** on the fly using combinatorial rules and user‑controlled parameters.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey

---

## Features

- **Fully dynamic generation** – builds payloads from basic building blocks (operators, delimiters, functions, etc.), not from a static list.
- **4 injection types** – SQL, XSS, SSTI, Command Injection.
- **Context‑aware** – choose between generic, value, numeric (SQL) or HTML, attribute, URI (XSS).
- **Bypass techniques** – random case, comment injection, IFS substitution, null‑byte insertion, event handler alternatives, and more.
- **Encoding chains** – apply multiple encodings in sequence: URL, double URL, Base64, hex, Unicode, HTML entities, reverse, ROT13, null‑byte, random case.
- **User‑controlled volume** – generate exactly as many payloads as you need (1 to 100,000+).
- **Output formats** – plain text (one per line) or JSON.
- **Zero dependencies** – pure Python 3.6+ standard library

---

## Installation

```bash
git clone https://github.com/yourusername/payload-gen.git
cd payload-gen
chmod +x payload-gen.py
python payload-gen.py -h
```
**The tool will work on any system with Python 3.6+ without installing additional packages. This tool is intended for authorised security testing, education, and research only. The user assumes all responsibility for compliance with applicable laws and regulations.**

---

## Usage

payload-gen.py -t <type> [options]

Required argument
Argument	Description
-t, --type	Injection type: sql, xss, ssti, cmd
Optional arguments
Argument	Description
-n, --limit	Number of payloads to generate (default: 100)
--context	Injection context (depends on type, see table below)
--bypass	Apply evasion / obfuscation techniques
--encode	Chain of encodings (space‑separated, order matters)
--command	Command to inject for cmd type (default: whoami)
-o, --output	Save output to file
--json	Output as JSON array instead of plain text

Supported contexts
Type	Context values	Description
sql	generic, value, numeric	Generic (anywhere), quoted string, numeric value
xss	html, attribute, uri	HTML tag injection, attribute injection, javascript: URI
ssti	(ignored)	–
cmd	(ignored)	–
Available encodings (orderable chain)

url durl b64 hex unicode html rev rot13 nullbyte randcase
---


