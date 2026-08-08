#!/usr/bin/env python3
"""Analyze and store website form patterns for auto-learning."""

import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime, timezone

LEARNED_DIR = Path("/home/workdir/artifacts/skills/kimi-web-form-filler/learned")

def site_key(url: str) -> str:
    """Create a stable key from a URL (domain + path)."""
    from urllib.parse import urlparse
    p = urlparse(url)
    base = f"{p.netloc}{p.path}".rstrip("/")
    return hashlib.sha256(base.encode()).hexdigest()[:16]

def save_pattern(url: str, fields: list, extra: dict = None):
    LEARNED_DIR.mkdir(parents=True, exist_ok=True)
    key = site_key(url)
    data = {
        "url": url,
        "key": key,
        "learned_at": datetime.now(timezone.utc).isoformat(),
        "fields": fields,
        "extra": extra or {},
    }
    path = LEARNED_DIR / f"{key}.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Learned pattern saved: {path}")
    return path

def load_pattern(url: str):
    key = site_key(url)
    path = LEARNED_DIR / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: learn_website.py <url> [fields_json_file]")
        sys.exit(1)
    url = sys.argv[1]
    fields = []
    if len(sys.argv) > 2:
        fields = json.loads(Path(sys.argv[2]).read_text())
    save_pattern(url, fields)
