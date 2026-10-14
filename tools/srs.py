#!/usr/bin/env python3
"""Spaced-repetition store. stdlib only. Data lives in data/*.json.

  srs.py add WORD -m MEANING [-e EXAMPLE] [-t TOPIC]
  srs.py due [--limit N]        words due today or earlier
  srs.py grade WORD pass|fail   advance or reset the interval
  srs.py log [-n NOTE]          mark today as studied (streak)
  srs.py stats                  totals by stage + streak
  srs.py brief                  short session-start summary (used by hook)
"""
import argparse, json, sys
from datetime import date, timedelta
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data"
VOCAB, PROG = D / "vocab.json", D / "progress.json"
INTERVALS = [1, 3, 7, 14, 30, 60]  # days after each successful review


def load(p, default):
    return json.loads(p.read_text()) if p.exists() else default


def save(p, obj):
    D.mkdir(exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1))


def today():
    return date.today()


def due_items(vocab, limit=None):
    t = today().isoformat()
    items = sorted((v for v in vocab if v["due"] <= t), key=lambda v: v["due"])
    return items[:limit] if limit else items


def streak(days):
    s, d = 0, today()
    if d.isoformat() not in days:
        d -= timedelta(days=1)
    while d.isoformat() in days:
        s, d = s + 1, d - timedelta(days=1)
    return s


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add"); a.add_argument("word")
    a.add_argument("-m", "--meaning", default=""); a.add_argument("-e", "--example", default="")
    a.add_argument("-t", "--topic", default="")
    d = sub.add_parser("due"); d.add_argument("--limit", type=int)
    g = sub.add_parser("grade"); g.add_argument("word"); g.add_argument("result", choices=["pass", "fail"])
    l = sub.add_parser("log"); l.add_argument("-n", "--note", default="")
    sub.add_parser("stats"); sub.add_parser("brief")
    x = ap.parse_args()

    vocab, prog = load(VOCAB, []), load(PROG, {"days": {}})
    key = lambda w: w.strip().lower()

    if x.cmd == "add":
        if any(key(v["word"]) == key(x.word) for v in vocab):
            print("exists:", x.word); return
        vocab.append({"word": x.word.strip(), "meaning": x.meaning, "example": x.example,
                      "topic": x.topic, "added": today().isoformat(), "stage": 0,
                      "due": (today() + timedelta(days=1)).isoformat(), "fails": 0})
        save(VOCAB, vocab); print("added:", x.word, "-> first review tomorrow")
    elif x.cmd == "due":
        for v in due_items(vocab, x.limit):
            print(f'{v["word"]} | {v["meaning"]} | stage {v["stage"]} | fails {v["fails"]} | {v["example"]}')
    elif x.cmd == "grade":
        v = next((v for v in vocab if key(v["word"]) == key(x.word)), None)
        if not v: sys.exit("not found: " + x.word)
        if x.result == "pass":
            v["stage"] = min(v["stage"] + 1, len(INTERVALS))
            days = INTERVALS[v["stage"] - 1]
        else:
            v["stage"], v["fails"], days = 0, v["fails"] + 1, 1
        v["due"] = (today() + timedelta(days=days)).isoformat()
        save(VOCAB, vocab); print(f'{v["word"]}: next review in {days}d ({v["due"]})')
    elif x.cmd == "log":
        prog["days"][today().isoformat()] = x.note or "studied"
        save(PROG, prog); print("logged, streak:", streak(prog["days"]))
    elif x.cmd == "stats":
        st = {}
        for v in vocab: st[v["stage"]] = st.get(v["stage"], 0) + 1
        print("words:", len(vocab), "| by stage:", dict(sorted(st.items())),
              "| streak:", streak(prog["days"]), "days")
    elif x.cmd == "brief":
        du = due_items(vocab)
        print(f"[english-learn] streak {streak(prog['days'])}d | words {len(vocab)} | due today {len(du)}")
        if du: print("Due:", ", ".join(v["word"] for v in du[:15]))
        print("Run /start-session to begin.")


main()
