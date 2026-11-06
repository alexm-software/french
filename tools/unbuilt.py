#!/usr/bin/env python3
"""unbuilt.py - what is painted in its planned building, by word id (run this FIRST).

Reads this checkout. Pass --sync to shallow-fetch public main into a temp dir instead
(no credentials). A planned word counts as integrated only when a live copy is in the
destination building: the building named by the plan, or a painted building whose
layout claims that source room. A copy that exists only somewhere else does not make
the room built.

  python3 tools/unbuilt.py --building B31_ferme
  python3 tools/unbuilt.py --repo /path/checkout
  python3 tools/unbuilt.py --sync                 # compare a fresh public main clone
  python3 tools/unbuilt.py --json out.json

A room is "built" when every planned word is in the destination building and nowhere
else, "extra" when all are there but at least one copy remains elsewhere, "partial"
when some are there, and "unbuilt" when none are. An unbuilt room can still name
words that are painted only in another building. Live ids the plan does not know
are strays.
"""
import argparse, json, os, re, subprocess, sys, tempfile
from collections import defaultdict
from pathlib import Path

URL = "https://github.com/alexm-software/french.git"
ID = re.compile(r'"id":\s*"(fr_[^"]+)"')
BUILDING_SLUG = re.compile(r"^B\d+_(.+)$")
ROOT = Path(__file__).resolve().parents[1]


def sync(dest, url, branch):
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_ASKPASS="/bin/true")
    g = ["git", "-c", "credential.helper=", "-c", "core.askPass=/bin/true"]
    if (dest / ".git").exists():
        subprocess.run(g + ["-C", str(dest), "fetch", "-q", "--depth", "1", "origin", branch], check=True, env=env)
        subprocess.run(g + ["-C", str(dest), "reset", "-q", "--hard", "FETCH_HEAD"], check=True, env=env)
    else:
        subprocess.run(g + ["clone", "-q", "--depth", "1", "--branch", branch, url, str(dest)], check=True, env=env)
    return git_sha(dest)


def git_sha(repo):
    sha = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short=8", "HEAD"], capture_output=True, text=True).stdout.strip()
    return sha or "?"


def load_payload(p):
    s = p.read_text(encoding="utf-8")
    match = re.search(r'\]\s*=\s*(\{)', s)
    if not match:
        raise ValueError(f"not a building payload: {p}")
    return json.loads(s[match.start(1):].rstrip().rstrip(";"))


def live_ids(repo):
    """{fr_id: [(building, room_key), ...]} from every village/data/*.js room item."""
    out = defaultdict(list)
    for p in sorted((repo / "village" / "data").glob("*.js")):
        if p.name in ("map.js", "live.js", "index.js", "listening.js", "prayers.js"):
            continue
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


def layout_index(repo):
    """Top-level building aliases and source rooms a layout explicitly claims.

    A door or nested object that names another building_id does not alias this file.
    """
    aliases, claims = defaultdict(set), defaultdict(set)
    base = repo / "content" / "v2"
    if not base.is_dir():
        return aliases, claims
    for path in sorted(base.glob("*/layout.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict):
            continue
        slug = data.get("building") if isinstance(data.get("building"), str) and data.get("building") else path.parent.name
        bid = data.get("building_id")
        if isinstance(bid, str) and bid:
            aliases[bid].add(slug)
        planned = data.get("planned") if isinstance(data.get("planned"), dict) else {}
        for spec in planned.values():
            if isinstance(spec, dict) and isinstance(spec.get("vocabRoom"), str) and spec.get("vocabRoom"):
                claims[spec["vocabRoom"]].add(slug)
        rooms = data.get("rooms") if isinstance(data.get("rooms"), dict) else {}
        for room in rooms.values():
            if isinstance(room, dict) and isinstance(room.get("room_id"), str) and room.get("room_id") and not room.get("parent"):
                claims[room["room_id"]].add(slug)
    return aliases, claims


def destination_slugs(building_id, aliases, claimed=()):
    """Painted building folders that count as this plan building."""
    if not isinstance(building_id, str) or not building_id:
        return set(claimed)
    match = BUILDING_SLUG.fullmatch(building_id)
    slugs = {match.group(1).lower()} if match else {building_id.lower()}
    slugs.update(s for s in aliases.get(building_id, ()) if isinstance(s, str) and s)
    slugs.update(s for s in claimed if isinstance(s, str) and s)
    return slugs


def classify_room(word_ids, live, dest):
    """Split planned ids into at-destination, only-elsewhere, and absent.

    An empty dest means the plan names no building, so any live copy counts as here.
    """
    here_ids, elsewhere_ids, absent_ids, also_ids = [], [], [], []
    here_in, elsewhere_in = set(), set()
    known_dest = bool(dest)
    for wid in word_ids:
        locs = list(dict.fromkeys(tuple(x) for x in live.get(wid, [])))
        if not locs:
            absent_ids.append(wid)
            continue
        at = [f"{b}/{r}" for b, r in locs if not known_dest or b in dest]
        out = [f"{b}/{r}" for b, r in locs if known_dest and b not in dest]
        if at:
            here_ids.append(wid)
            here_in.update(at)
            if out:
                also_ids.append(wid)
                elsewhere_in.update(out)
        else:
            elsewhere_ids.append(wid)
            elsewhere_in.update(out)
    if not here_ids:
        state = "unbuilt"
    elif elsewhere_ids or absent_ids:
        state = "partial"
    elif also_ids:
        state = "extra"
    else:
        state = "built"
    return dict(planned=len(word_ids), here=len(here_ids), elsewhere=len(elsewhere_ids),
                absent=len(absent_ids), also=len(also_ids), state=state,
                here_ids=here_ids, elsewhere_ids=elsewhere_ids, absent_ids=absent_ids, also_ids=also_ids,
                here_in=sorted(here_in), elsewhere_in=sorted(elsewhere_in))


def _place_list(places, limit=6):
    shown = places[:limit]
    extra = len(places) - len(shown)
    return ", ".join(shown) + (f" +{extra}" if extra else "")


def format_row(row):
    bits = [f"{row['state']:<9} {row['room']:<28} here {row['here']:>3}/{row['planned']:<3} "
            f"elsewhere {row['elsewhere']:>3} absent {row['absent']:>3}"]
    if row["also"]:
        bits.append(f"also {row['also']}")
    if row["here_in"]:
        bits.append("at " + _place_list(row["here_in"]))
    if row["elsewhere_in"]:
        bits.append("other " + _place_list(row["elsewhere_in"]))
    return "  " + "  ".join(bits)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--building", help="building id or substring of id/name (case-insensitive)")
    ap.add_argument("--repo", help="existing checkout to read (default: this repo)")
    ap.add_argument("--sync", action="store_true", help="shallow-fetch public main instead of reading this checkout")
    ap.add_argument("--dest", default=str(Path(tempfile.gettempdir()) / "mp_unbuilt_main"), help="clone dir for --sync (default %(default)s)")
    ap.add_argument("--url", default=URL)
    ap.add_argument("--branch", default="main")
    ap.add_argument("--all", action="store_true", help="also list fully built rooms")
    ap.add_argument("--json", help="write the per-room table here")
    a = ap.parse_args()

    if a.repo:
        repo, label = Path(a.repo), "checkout"
        sha = git_sha(repo)
    elif a.sync:
        repo, label = Path(a.dest), "main"
        sha = sync(repo, a.url, a.branch)
    else:
        repo, label = ROOT, "checkout"
        sha = git_sha(repo)

    src = repo / "data" / "source"
    vocab = [json.loads(l) for l in (src / "vocab.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    vocab = [v for v in vocab if str(v.get("id", "")).startswith("fr_")]
    rooms = {r["id"]: r for r in json.loads((src / "rooms.json").read_text(encoding="utf-8"))["rooms"]}
    blds = {b["id"]: b for b in json.loads((src / "buildings.json").read_text(encoding="utf-8"))["buildings"]}
    live = live_ids(repo)
    aliases, claims = layout_index(repo)

    plan = defaultdict(list)  # room_id -> [fr ids]
    for v in vocab:
        plan[v.get("room_id") or "(no room)"].append(v["id"])
    vid = {v["id"]: v for v in vocab}
    strays = [i for i in live if i not in vid]

    rows = []
    for rid, ids in plan.items():
        R = rooms.get(rid, {})
        b = R.get("building_id") or "(no building)"
        dest = destination_slugs(b if b != "(no building)" else "", aliases, claims.get(rid, ()))
        placed = classify_room(ids, live, dest)
        where = sorted({f"{x[0]}/{x[1]}" for i in ids if i in live for x in live[i]})
        rows.append(dict(room=rid, name=R.get("name", ""), building=b, building_name=blds.get(b, {}).get("name", ""),
                         live=placed["here"] + placed["elsewhere"], left=placed["absent"], live_in=where,
                         left_ids=placed["absent_ids"], dest=sorted(dest), **placed))

    def tally(items):
        return dict(here=sum(r["here"] for r in items), elsewhere=sum(r["elsewhere"] for r in items),
                    absent=sum(r["absent"] for r in items), planned=sum(r["planned"] for r in items))

    totals = tally(rows)
    if a.building:
        q = a.building.lower()
        rows = [r for r in rows if q in r["building"].lower() or q in r["building_name"].lower()]
        if not rows:
            sys.exit(f"no building matches {a.building!r}")

    shown = tally(rows)
    print(f"{label} @ {sha}  ({repo})")
    print("A room is built only when every planned word is painted in its destination building and nowhere else. "
          "other = planned words still painted outside that building.")
    print(f"TOTAL on site {totals['here'] + totals['elsewhere']:,} of {totals['planned']:,} planned words; "
          f"at destination {totals['here']:,}; only elsewhere {totals['elsewhere']:,}; not painted {totals['absent']:,}; "
          f"live ids not in plan: {len(strays)}")
    st = defaultdict(int)
    for r in rows:
        st[r["state"]] += 1
    if a.building:
        print(f"FILTER {a.building!r}: {len(rows)} rooms, here {shown['here']} of {shown['planned']}, "
              f"elsewhere {shown['elsewhere']}, absent {shown['absent']}")
    print(f"rooms: built {st['built']} (hidden without --all), partial {st['partial']}, "
          f"extra {st['extra']} (also painted elsewhere), unbuilt {st['unbuilt']}")

    byb = defaultdict(list)
    for r in rows:
        byb[r["building"]].append(r)
    order = sorted(byb, key=lambda b: (-sum(r["elsewhere"] + r["absent"] for r in byb[b]), b))
    for b in order:
        rs = byb[b]
        P = sum(r["planned"] for r in rs)
        show = [r for r in rs if a.all or r["state"] != "built"]
        if not show:
            continue
        print(f"\n== {b}  {blds.get(b, {}).get('name', '')}  "
              f"here {sum(r['here'] for r in rs)}/{P}, elsewhere {sum(r['elsewhere'] for r in rs)}, "
              f"absent {sum(r['absent'] for r in rs)}")
        for state in ("partial", "extra", "unbuilt", "built"):
            for r in sorted((x for x in show if x["state"] == state), key=lambda x: (-x["elsewhere"], x["room"])):
                print(format_row(r))
    if a.json:
        Path(a.json).write_text(json.dumps(dict(sha=sha, label=label, at_destination=totals["here"],
                                                only_elsewhere=totals["elsewhere"], not_painted=totals["absent"],
                                                live=totals["here"] + totals["elsewhere"], planned=totals["planned"],
                                                strays=strays, rooms=rows), indent=1, ensure_ascii=False))
        print(f"\nwrote {a.json}")


if __name__ == "__main__":
    main()
