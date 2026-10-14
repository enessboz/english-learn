#!/usr/bin/env python3
"""Regenerate apps/vocab.html with a snapshot of data/vocab.json embedded.

  python3 tools/build_vocab_app.py                 # writes apps/vocab.html
  python3 tools/build_vocab_app.py --fragment OUT  # also writes the wrapper-less
                                                   # page used for Artifact publishing
Reads data/vocab.json only; never modifies it.
"""
import argparse, json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "tools" / "vocab_app_template.html"
MARK = '/*VOCAB_JSON*/ {"generated":"","words":[]}'
WRAP = ('<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<style>:root{color-scheme:light}body{margin:0}[hidden]{display:none!important}</style>\n'
        '</head>\n<body>\n%s\n</body>\n</html>\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fragment", help="also write the page without html/head/body wrapper")
    ap.add_argument("-o", "--out", default=str(ROOT / "apps" / "vocab.html"))
    x = ap.parse_args()
    vp = ROOT / "data" / "vocab.json"
    words = json.loads(vp.read_text()) if vp.exists() else []
    snap = {"generated": date.today().isoformat(), "words": words}
    blob = json.dumps(snap, ensure_ascii=False).replace("</", "<\\/")
    tpl = TEMPLATE.read_text()
    assert MARK in tpl, "placeholder missing in template"
    page = tpl.replace(MARK, blob)
    Path(x.out).parent.mkdir(exist_ok=True)
    Path(x.out).write_text(WRAP % page)
    if x.fragment:
        Path(x.fragment).write_text(page)
    print(f"wrote {x.out} with {len(words)} words")


main()
