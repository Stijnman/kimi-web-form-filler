#!/usr/bin/env python3
"""Basic form field analyzer (works on HTML snapshots or accessibility dumps)."""

import re
import sys
from html.parser import HTMLParser
from typing import List, Dict

class FormFieldParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.fields = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("input", "textarea", "select"):
            field = {
                "tag": tag,
                "type": attrs.get("type", "text" if tag == "input" else tag),
                "name": attrs.get("name"),
                "id": attrs.get("id"),
                "placeholder": attrs.get("placeholder"),
                "required": "required" in attrs,
                "value": attrs.get("value"),
            }
            self.fields.append(field)

def analyze(html: str) -> List[Dict]:
    parser = FormFieldParser()
    parser.feed(html)
    return parser.fields

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8", errors="ignore") as f:
            html = f.read()
    else:
        html = sys.stdin.read()
    fields = analyze(html)
    for i, f in enumerate(fields, 1):
        print(f"{i:2}. {f['tag']:8} type={f['type'] or '-':12} name={f['name'] or '-':20} id={f['id'] or '-'} required={f['required']}")
