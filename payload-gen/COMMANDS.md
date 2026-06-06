# All possible commands for payload-gen.py

## Basic commands

| Command | Description |
|---------|----------|
| `./payload-gen.py -t sql` | 100 SQL payloads (generic) |
| `./payload-gen.py -t xss` | 100 XSS payloads (html) |
| `./payload-gen.py -t ssti` | 100 SSTI payloads |
| `./payload-gen.py -t cmd` | 100 CMD payloads with command `whoami` |

## Indicating quantity

| Command | Description |
|---------|----------|
| `-n 10` | 10 payloads |
| `-n 1000` | 1000 payloads |
| `-n 50000` | 50000 payloads |

## With context (for SQL and XSS)

| Command | Description |
|---------|----------|
| `-t sql --context value` | SQL injection in a string value (with quotes) |
| `-t sql --context numeric` | SQL injection on a numeric value (without quotes) |
| `-t sql --context generic` | Common SQL (default) |
| `-t xss --context html` | XSS via HTML tags (default) |
| `-t xss --context attribute` | XSS inside HTML attribute |
| `-t xss --context uri` | XSS via pseudo-protocol `javascript:` |

## With bypass techniques (`--bypass`)

| Command | Action |
|---------|----------|
| `-t sql --bypass` | Inserting comments, case variations |
| `-t xss --bypass` | Escape <>, random case |
| `-t ssti --bypass` | Access `__class__.__mro__`, replacing `{{` with `{%` |
| `-t cmd --bypass` | `$IFS`, comments, redirects |

## With encoding (chain)

| Command | Coding |
|---------|-------------|
| `--encode url` | URL-coding |
| `--encode durl` | two URL-coding |
| `--encode b64` | Base64 |
| `--encode hex` | Hexadecimal |
| `--encode unicode` | Unicode escape `\uXXXX` |
| `--encode html` | HTML entity `&#XX;` |
| `--encode rev` | Reverse line |
| `--encode rot13` | ROT13 |
| `--encode nullbyte` | Insert `%00` every 2 characters |
| `--encode randcase` | Random case |
| `--encode url b64 hex` | Chain: URL → Base64 → Hex |

## Commands for CMD

| Command | Description |
|---------|----------|
| `-t cmd --command "id"` | Command injection `id` |
| `-t cmd --command "cat /etc/passwd"` | Reading a file |
| `-t cmd --command "ping -c 1 127.0.0.1"` | Network commands |
| `-t cmd --command "powershell -c Get-Process"` | Windows Command |

## Saving results

| Command | Format |
|---------|--------|
| `-o файл.txt` | Save to text file (line by line) |
| `--json -o файл.json` | Save as JSON |

## Complete examples

```bash
# SQL with crawling, URL encoding, 500 payloads, saved as sql.txt
./payload-gen.py -t sql --bypass --encode url -n 500 -o sql.txt

# XSS in an attribute, no bypass, 200 instances, JSON output
./payload-gen.py -t xss --context attribute -n 200 --json

# SSTI with bypass and double URL encoding, 50 payloads
./payload-gen.py -t ssti --bypass --encode durl -n 50

# CMD with 'ls -la' command, traversal and Base64 encoding
./payload-gen.py -t cmd --command "ls -la" --bypass --encode b64 -n 100

# SQL numeric context, no traversal, hexadecimal encoding
./payload-gen.py -t sql --context numeric --encode hex -n 300