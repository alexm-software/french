#!/usr/bin/env python3
"""build_audio.py - record the site's French with ElevenLabs voices, so the Listen buttons play real speech.

  python3 scripts/audio/build_audio.py --dry-run                 # what is still to record, and how many characters (no key needed)
  python3 scripts/audio/build_audio.py --check                   # can the key use every voice in data/source/voices.json? (free)
  python3 scripts/audio/build_audio.py --only words --budget 20000
  python3 scripts/audio/build_audio.py --only talk --buildings cafe boulangerie
  python3 scripts/audio/build_audio.py --index                   # only rewrite village/audio/index.js from the files present
  python3 scripts/audio/build_audio.py --prune                   # delete recordings whose text is no longer on the site

The key comes from the ELEVENLABS_API_KEY environment variable (or a GitHub secret of that name, see
.github/workflows/audio.yml). It is never written to a file and never reaches the browser.

Kinds, in the order they are recorded:
  words     each card's headword ("la pomme"), the alphabet letters and number words
  phrases   the Expressions on cards and the verb Patterns examples
  examples  each card's example sentence
  talk      every conversation line, in the speaker's own voice
  listening the listening passages, one file per sentence (the page highlights sentence by sentence)
  prayers   the prayer book, one file per sentence
Each text is recorded once per voice. A file is named after a hash of its text, so a recording is reused for as long
as the text is unchanged, and an edited text is simply recorded again. Re-running never pays twice for a file
that exists. Characters are what ElevenLabs bills: one credit per character on the multilingual v2 model.

The browser computes the same hash (village/app.js, akey) and plays audio/<voice>/<hash>.mp3 when
audio/index.js lists it; otherwise it falls back to the device's own French voice.
"""
import argparse, json, os, re, sys, time, unicodedata, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "village" / "data"
OUT = ROOT / "village" / "audio"
VOICES = ROOT / "data" / "source" / "voices.json"
KINDS = ["words", "phrases", "examples", "talk", "listening", "prayers"]
API = "https://api.elevenlabs.io/v1"
KEYLEN = 12


# ---------- the text key, identical to akey() in village/app.js ----------
def norm(t):
    return " ".join(str(t).split())


def fnv(b, h):
    for x in b:
        h ^= x
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def akey(t):
    b = norm(t).encode("utf-8")
    return (f"{fnv(b, 2166136261):08x}{fnv(b, 84696351):08x}")[:KEYLEN]


def slug(role):
    s = unicodedata.normalize("NFKD", role).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "n"


# ---------- the same sentence split as practice.js sentences() ----------
SENT = re.compile(r'[^.!?…]+[.!?…]+["»”]?\s*|[^.!?…]+$')


def sentences(t):
    return [s.strip() for s in SENT.findall(t) if s.strip()]


def payload(path, marker):
    s = path.read_text(encoding="utf-8")
    return json.loads(s[s.index(marker) + len(marker):].rstrip().rstrip(";"))


def headword(it):  # as app.js headword()
    if it.get("verb") or it.get("adj") or it.get("adv"):
        return it["fr"]
    a = it.get("art")
    if a is None:
        return None
    return "l'" + it["fr"] if a == "l'" else f"{a} {it['fr']}"


def collect(only, buildings):
    """[(kind, role, text, building)] in recording order, without repeats of (role, text)."""
    rows = []
    rooms = []
    for f in sorted(DATA.glob("*.js")):
        s = f.read_text(encoding="utf-8")
        if '"building"' not in s[:400]:
            continue
        d = payload(f, "]=")
        if buildings and d["building"] not in buildings:
            continue
        for r in d["rooms"].values():
            for it in r["items"]:
                rooms.append((d["building"], it))
    for b, it in rooms:
        hw = headword(it)
        if hw:
            rows.append(("words", "n", hw, b))
        for x in (it.get("alphabet") or {}).get("letters", []):
            rows.append(("words", "n", x["l"], b))
        for x in (it.get("alphabet") or {}).get("accents", []):
            rows.append(("words", "n", x["name"], b))
        for x in (it.get("numbers") or {}).get("items", []):
            rows.append(("words", "n", x["word"], b))
        for n in (it.get("numbers") or {}).get("notes", []):
            for e in n.get("ex") or []:
                rows.append(("words", "n", e["word"], b))
    for b, it in rooms:
        for p in it.get("phrases") or []:
            rows.append(("phrases", "n", p["fr"], b))
        for p in it.get("patterns") or []:
            if p.get("ex"):
                rows.append(("phrases", "n", p["ex"], b))
    for b, it in rooms:
        if it.get("ex"):
            rows.append(("examples", "n", it["ex"][0], b))
    for f in sorted((DATA / "talk").glob("*.js")):
        if f.name == "index.js" or (buildings and f.stem not in buildings):
            continue
        for convs in payload(f, "]=").values():
            for c in convs:
                for l in c["lines"]:
                    rows.append(("talk", l["speaker"], l["fr"], f.stem))
    if (DATA / "listening.js").exists():
        for p in payload(DATA / "listening.js", "="):
            bld = p.get("room", "").split("/")[0]
            if buildings and bld not in buildings:
                continue
            for s in sentences(p["fr"]):
                rows.append(("listening", "n", s, bld))
    if (DATA / "prayers.js").exists() and not buildings:
        for p in payload(DATA / "prayers.js", "="):
            for s in sentences(re.sub(r"\b[VR]\.\s", "", p["fr"], flags=re.A)):
                rows.append(("prayers", "n", s, "eglise"))
    seen, out = set(), []
    for k, role, text, b in rows:
        text = norm(text)
        if not text or (only and k not in only):
            continue
        if (role, text) in seen:
            continue
        seen.add((role, text))
        out.append((k, role, text, b))
    return out


# ---------- the manifest the page reads ----------
def write_index(cfg):
    roles = {r: slug(r) for r in cfg["voices"]}
    h = {}
    for d in sorted(OUT.iterdir()) if OUT.exists() else []:
        if d.is_dir():
            keys = sorted(p.stem for p in d.glob("*.mp3") if len(p.stem) == KEYLEN)
            if keys:
                h[d.name] = "".join(keys)
    OUT.mkdir(parents=True, exist_ok=True)
    js = "// Built by scripts/audio/build_audio.py: which texts have a recording, per voice (12-character text hashes).\n"
    js += "window.V2_AUDIO=" + json.dumps({"r": roles, "h": h}, ensure_ascii=False, separators=(",", ":")) + ";\n"
    (OUT / "index.js").write_text(js, encoding="utf-8")
    return sum(len(v) // KEYLEN for v in h.values())


# ---------- ElevenLabs ----------
class Stop(Exception):
    pass


def request(url, key, body=None, tries=5):
    data = json.dumps(body).encode() if body is not None else None
    for n in range(tries):
        req = urllib.request.Request(url, data=data, method="POST" if data else "GET",
                                     headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:400]
            if e.code == 429 or e.code >= 500:
                time.sleep(min(60, 4 * 2 ** n))
                continue
            if e.code == 401 or "quota_exceeded" in msg or "insufficient" in msg.lower():
                raise Stop(f"ElevenLabs refused the request ({e.code}): {msg}")
            raise RuntimeError(f"{e.code}: {msg}")
        except (urllib.error.URLError, TimeoutError) as e:
            time.sleep(4 * 2 ** n)
            last = e
    raise RuntimeError(f"no answer from ElevenLabs after {tries} tries")


def check(cfg, key):
    bad = []
    for role, v in cfg["voices"].items():
        try:
            request(f"{API}/voices/{v['id']}", key, tries=2)
            print(f"  ok       {role:14} {v['name']}")
        except Stop as e:
            raise
        except RuntimeError as e:
            bad.append(role)
            print(f"  MISSING  {role:14} {v['name']} ({v['id']}): {str(e)[:120]}")
    if bad:
        print("Voices marked MISSING are not usable with this key. Add each one to your account (ElevenLabs > Voices >\n"
              "Voice Library > search the name > Add to my voices), or change its id in data/source/voices.json.\n"
              "Their lines are read by the narrator voice until then.")
    return bad


def tts(cfg, key, voice_id, text, english=False):
    body = {"text": text, "model_id": cfg["model"], "voice_settings": cfg.get("settings") or {}}
    if not english and re.search(r"(2_5|v3)", cfg["model"]):
        body["language_code"] = "fr"
    return request(f"{API}/text-to-speech/{voice_id}?output_format={cfg.get('output_format', 'mp3_22050_32')}", key, body)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", default="", help="comma list of: " + ", ".join(KINDS) + " (default: all)")
    ap.add_argument("--buildings", nargs="*", default=[], help="only these buildings")
    ap.add_argument("--budget", type=int, default=20000, help="most characters to spend in this run (default 20000)")
    ap.add_argument("--workers", type=int, default=2, help="requests at once (your plan's concurrency limit)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--index", action="store_true")
    ap.add_argument("--prune", action="store_true")
    a = ap.parse_args()
    cfg = json.loads(VOICES.read_text(encoding="utf-8"))
    only = [k.strip() for k in a.only.replace(" ", ",").split(",") if k.strip() and k.strip() != "all"]
    for k in only:
        if k not in KINDS:
            sys.exit(f"unknown kind '{k}': use " + ", ".join(KINDS))
    voices = cfg["voices"]

    def role_of(r):
        return r if r in voices else "n"

    rows = collect(only, set(a.buildings))
    todo, have, by = [], 0, {}
    for k, role, text, b in rows:
        r = role_of(role)
        path = OUT / slug(r) / f"{akey(text)}.mp3"
        st = by.setdefault(k, [0, 0, 0])
        st[0] += 1
        if path.exists():
            have += 1
            st[1] += 1
        else:
            st[2] += len(text)
            todo.append((k, r, text, path))

    if a.prune:
        want = {OUT / slug(role_of(r)) / f"{akey(t)}.mp3" for _, r, t, _ in collect([], set())}
        gone = [p for p in OUT.glob("*/*.mp3") if p not in want]
        for p in gone:
            p.unlink()
        print(f"pruned {len(gone)} recording(s) no longer on the site; {write_index(cfg)} listed")
        return
    if a.index:
        print(f"audio/index.js lists {write_index(cfg)} recording(s)")
        return

    print(f"{'kind':10} {'texts':>6} {'recorded':>9} {'chars to go':>12}")
    for k in KINDS:
        if k in by:
            print(f"{k:10} {by[k][0]:6} {by[k][1]:9} {by[k][2]:12,}")
    total = sum(len(t) for _, _, t, _ in todo)
    print(f"{len(todo)} text(s), {total:,} characters still to record; {have} already recorded")
    if a.dry_run:
        return

    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key:
        sys.exit("Set ELEVENLABS_API_KEY first (ElevenLabs > Developers > API keys). It is read from the environment only.")
    print("Checking the voices:")
    missing = set(check(cfg, key))
    batch, spent = [], 0
    for k, r, text, path in todo:
        if r in missing:
            r = "n"
            path = OUT / "n" / path.name
            if path.exists() or "n" in missing:
                continue
        if spent + len(text) > a.budget:
            break
        spent += len(text)
        batch.append((k, r, text, path))
    print(f"Recording {len(batch)} text(s), {spent:,} characters (budget {a.budget:,})")

    done, failed, stop = [0], [], []

    def one(job):
        k, r, text, path = job
        if stop:
            return
        try:
            mp3 = tts(cfg, key, voices[r]["id"], text, english=(r == "Le touriste"))
        except Stop as e:
            stop.append(str(e))
            return
        except Exception as e:
            failed.append(f"{r}: {text[:50]}: {e}")
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".part")
        tmp.write_bytes(mp3)
        tmp.replace(path)
        done[0] += 1
        if done[0] % 100 == 0:
            print(f"  {done[0]} / {len(batch)}", flush=True)

    try:
        with ThreadPoolExecutor(max_workers=max(1, a.workers)) as ex:
            list(ex.map(one, batch))
    finally:
        n = write_index(cfg)
    print(f"recorded {done[0]}, failed {len(failed)}; audio/index.js lists {n} recording(s)")
    for f in failed[:20]:
        print("  FAILED", f)
    if stop:
        print("STOPPED:", stop[0])
        sys.exit(2)


if __name__ == "__main__":
    main()
