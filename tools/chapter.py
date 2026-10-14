#!/usr/bin/env python3
"""Chapter progress + gate tests. stdlib only.

  chapter.py status             current chapter, requirements, progress
  chapter.py gate pass|fail [-s "speaking=75,writing=70,reading=85,listening=70"] [--force]
  chapter.py html               regenerate roadmap.html from curriculum + state
  chapter.py brief              one-line summary (session hook)
"""
import argparse, json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
CUR, STATE = D / "curriculum.json", D / "chapter_state.json"
PASS_MIN = {"speaking": 70, "writing": 70, "reading": 80, "listening": 70}


def load(p, default=None):
    return json.loads(p.read_text()) if p.exists() else default


def metrics(state):
    vocab = load(D / "vocab.json", [])
    days = load(D / "progress.json", {"days": {}})["days"]
    st = state["started"]
    return {"learned": sum(1 for v in vocab if v["stage"] >= 2),
            "added": len(vocab),
            "days": sum(1 for d in days if d >= st)}


def get_state():
    s = load(STATE)
    if not s:
        s = {"current": 1, "started": date.today().isoformat(), "history": []}
        STATE.write_text(json.dumps(s, indent=1, ensure_ascii=False))
    return s


def status_lines(cur, ch, state, m):
    day = (date.today() - date.fromisoformat(state["started"])).days + 1
    return [
        f'Chapter {ch["id"]}/{len(cur["chapters"])}: {ch["title"]} ({ch["tr"]}) | hafta {ch["weeks"]} | gün {day}',
        f'  Çalışılan gün: {m["days"]}/{ch["min_days"]}',
        f'  Öğrenilen kelime (2+ başarılı tekrar): {m["learned"]}/{ch["vocab_target"]}',
        "  Grammar: " + ", ".join(ch["grammar"]),
        "  Kapı testi: " + " | ".join(f"{k}: {v}" for k, v in ch["gate"].items()),
    ]


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status"); sub.add_parser("html"); sub.add_parser("brief")
    g = sub.add_parser("gate"); g.add_argument("result", choices=["pass", "fail"])
    g.add_argument("-s", "--scores", default=""); g.add_argument("--force", action="store_true")
    x = ap.parse_args()

    cur, state = load(CUR), get_state()
    chs = cur["chapters"]
    ch = next((c for c in chs if c["id"] == state["current"]), None)
    m = metrics(state)

    if x.cmd == "status":
        if not ch: print("Tüm bölümler tamam. Yeni EF SET testine gir."); return
        print("\n".join(status_lines(cur, ch, state, m)))
        ready = m["days"] >= ch["min_days"] and m["learned"] >= ch["vocab_target"]
        print("  Kapıya hazır mı:", "EVET -> /gate-test" if ready else "henüz değil")
    elif x.cmd == "brief":
        if ch:
            print(f'[chapter] {ch["id"]}/{len(chs)} {ch["title"]} | gün {m["days"]}/{ch["min_days"]} | kelime {m["learned"]}/{ch["vocab_target"]}')
    elif x.cmd == "gate":
        scores = {k: int(v) for k, v in (p.split("=") for p in x.scores.split(",") if p)}
        ok_auto = m["days"] >= ch["min_days"] and m["learned"] >= ch["vocab_target"]
        ok_tests = all(scores.get(k, 0) >= PASS_MIN[k] for k in PASS_MIN)
        if x.result == "pass" and not ((ok_auto and ok_tests) or x.force):
            print("Reddedildi: otomatik şartlar veya test puanları yetersiz.",
                  f"auto={ok_auto} tests={ok_tests} scores={scores}. (--force ile geçilebilir)"); return
        state["history"].append({"chapter": ch["id"], "date": date.today().isoformat(),
                                 "result": x.result, "scores": scores})
        if x.result == "pass":
            state["current"] += 1
            state["started"] = date.today().isoformat()
            print("GEÇTİN. Sıradaki:", next((c["title"] for c in chs if c["id"] == state["current"]), "Final"))
        else:
            print("Kalındı. 3 gün zayıf alana çalış, sonra tekrar dene.")
        STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False))
    elif x.cmd == "html":
        tpl = (ROOT / "tools" / "roadmap_template.html").read_text()
        data = {"cur": cur, "state": state, "metrics": m, "pass_min": PASS_MIN,
                "updated": date.today().isoformat()}
        (ROOT / "roadmap.html").write_text(tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False)))
        print("roadmap.html written")


main()
