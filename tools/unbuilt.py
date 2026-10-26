#!/usr/bin/env python3
"""unbuilt.py - what is live vs left, by word id (run this FIRST, every time).

Shallow-clones (or fast-forwards) main of the public repo into a temp dir with a plain public
https clone (no credentials, no prompts), then compares the live fr_ ids found in
village/data/*.js against the plan (data/source/vocab.jsonl room_id + data/source/rooms.json).

  python3 unbuilt.py                       # totals + partial/unbuilt rooms grouped by building
  python3 unbuilt.py --building B12_ecole  # one building (id, or a substring of id/name)
  python3 unbuilt.py --repo /path/checkout # use an existing checkout instead (read-only)
  python3 unbuilt.py --json out.json       # also write the full table

A room is "built" when all its planned words are live, "partial" when some are, "unbuilt" when none.
Live ids that the plan puts in another room or does not know are listed as strays (counts only).
"""
import argparse, json, os, re, subprocess, sys, tempfile
from collections import defaultdict
from pathlib import Path

URL = "https://github.com/alexm-software/french.git"
ID = re.compile(r'"id":\s*"(fr_[^"]+)"')


def sync(dest, url, branch):
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_ASKPASS="/bin/true")
    g = ["git", "-c", "credential.helper=", "-c", "core.askPass=/bin/true"]
    if (dest / ".git").exists():
        subprocess.run(g + ["-C", str(dest), "fetch", "-q", "--depth", "1", "origin", branch], check=True, env=env)
        subprocess.run(g + ["-C", str(dest), "reset", "-q", "--hard", "FETCH_HEAD"], check=True, env=env)
    else:
        subprocess.run(g + ["clone", "-q", "--depth", "1", "--branch", branch, url, str(dest)], check=True, env=env)
    sha = subprocess.run(["git", "-C", str(dest), "rev-parse", "--short=8", "HEAD"], capture_output=True, text=True).stdout.strip()
    return sha


def load_payload(p):
    s = p.read_text(encoding="utf-8")
    return json.loads(s[s.index("]=") + 2:].rstrip().rstrip(";"))


def live_ids(repo):
    """{fr_id: [(building, room_key), ...]} from every village/data/*.js room item."""
    out = defaultdict(list)
    for p in sorted((repo / "village" / "data").glob("*.js")):
        try:
            D = load_payload(p)
        except Exception:  # not a building payload: fall back to a plain id scan
            for m in ID.finditer(p.read_text(encoding="utf-8")):
                out[m.group(1)].append((p.stem, "?"))
            continue
        for key, R in (D.get("rooms") or {}).items():
            for it in R.get("items", []):
                if str(it.get("id", "")).startswith("fr_"):
                    out[it["id"]].append((p.stem, key))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--building", help="building id or substring of id/name (case-insensitive)")
    ap.add_argument("--repo", help="existing checkout to read instead of cloning")
    ap.add_argument("--dest", default=str(Path(tempfile.gettempdir()) / "mp_unbuilt_main"), help="clone dir (default %(default)s)")
    ap.add_argument("--url", default=URL)
    ap.add_argument("--branch", default="main")
    ap.add_argument("--all", action="store_true", help="also list fully built rooms")
    ap.add_argument("--json", help="write the per-room table here")
    a = ap.parse_args()

    if a.repo:
        repo = Path(a.repo)
        sha = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short=8", "HEAD"], capture_output=True, text=True).stdout.strip() or "?"
    else:
        repo = Path(a.dest)
        sha = sync(repo, a.url, a.branch)

    src = repo / "data" / "source"
    vocab = [json.loads(l) for l in (src / "vocab.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    vocab = [v for v in vocab if str(v.get("id", "")).startswith("fr_")]
    rooms = {r["id"]: r for r in json.loads((src / "rooms.json").read_text(encoding="utf-8"))["rooms"]}
    blds = {b["id"]: b for b in json.loads((src / "buildings.json").read_text(encoding="utf-8"))["buildings"]}
    live = live_ids(repo)

    plan = defaultdict(list)  # room_id -> [fr ids]
    for v in vocab:
        plan[v.get("room_id") or "(no room)"].append(v["id"])
    vid = {v["id"]: v for v in vocab}
    n_live = sum(1 for v in vocab if v["id"] in live)
    strays = [i for i in live if i not in vid]

    rows = []
    for rid, ids in plan.items():
        R = rooms.get(rid, {})
        b = R.get("building_id") or "(no building)"
        got = [i for i in ids if i in live]
        where = sorted({f"{x[0]}/{x[1]}" for i in got for x in live[i]})
        state = "built" if len(got) == len(ids) else ("partial" if got else "unbuilt")
        rows.append(dict(room=rid, name=R.get("name", ""), building=b, building_name=blds.get(b, {}).get("name", ""),
                         planned=len(ids), live=len(got), left=len(ids) - len(got), state=state, live_in=where,
                         left_ids=[i for i in ids if i not in live]))

    if a.building:
        q = a.building.lower()
        rows = [r for r in rows if q in r["building"].lower() or q in r["building_name"].lower()]
        if not rows:
            sys.exit(f"no building matches {a.building!r}")

    print(f"main @ {sha}  ({repo})")
    print(f"TOTAL live {n_live:,} of {len(vocab):,} planned words ({100 * n_live / len(vocab):.1f}%), left {len(vocab) - n_live:,}; "
          f"live ids not in plan: {len(strays)}")
    st = defaultdict(int)
    for r in rows:
        st[r["state"]] += 1
    if a.building:
        p_, l_ = sum(r["planned"] for r in rows), sum(r["live"] for r in rows)
        print(f"FILTER {a.building!r}: {len(rows)} rooms, live {l_} of {p_}, left {p_ - l_}")
    print(f"rooms: built {st['built']}, partial {st['partial']}, unbuilt {st['unbuilt']}")

    byb = defaultdict(list)
    for r in rows:
        byb[r["building"]].append(r)
    order = sorted(byb, key=lambda b: (-sum(r["left"] for r in byb[b]), b))
    for b in order:
        rs = byb[b]
        P, Lv = sum(r["planned"] for r in rs), sum(r["live"] for r in rs)
        show = [r for r in rs if a.all or r["state"] != "built"]
        if not show:
            continue
        print(f"\n== {b}  {blds.get(b, {}).get('name', '')}  live {Lv}/{P}, left {P - Lv}")
        for state in ("partial", "unbuilt", "built"):
            for r in sorted((x for x in show if x["state"] == state), key=lambda x: x["room"]):
                extra = f"  in {', '.join(r['live_in'])}" if r["live_in"] else ""
                print(f"  {state:<8} {r['room']:<28} live {r['live']:>3}/{r['planned']:<3} left {r['left']:>3}{extra}")
    if a.json:
        Path(a.json).write_text(json.dumps(dict(sha=sha, live=n_live, planned=len(vocab), strays=strays, rooms=rows), indent=1, ensure_ascii=False))
        print(f"\nwrote {a.json}")


if __name__ == "__main__":
    main()
