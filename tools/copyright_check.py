#!/usr/bin/env python3
"""copyright_check.py - every text the site quotes from someone else has a known, allowed source.

  python3 tools/copyright_check.py        # exit 1 and list the problems

Checks (all FAIL):
  prayers   every prayer in data/source/prayers.json has a "source" that names either a dated edition
            published before 1929 (a year 1000-1928 appears) or the project's "own translation", and says
            how it may be used ("public domain", "CC BY-SA" or a named permission). A source that names a
            current liturgical text (AELF, ICEL, Missel romain 2021, Roman Missal 2011) must say it does NOT
            copy it. Every prayer's French title appears in data/source/CREDITS.md.
  modern    no prayer text contains wording known to belong only to the current copyrighted liturgical
            translations (see MODERN below), unless the source line explains why it is allowed.
  credits   data/source/CREDITS.md and LICENSE-DATA.md exist; every font file shipped in village/ or src/fonts/
            has a license file beside it.
  writing   the CREDITS "Written for this project" paragraph mentions the dialogues and listening passages
            (texts we write ourselves and share under CC BY-SA).
Song lyrics, poems and book passages are never copied into the data; a quoted text must be listed here first.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Phrases found only in current copyrighted liturgical translations (AELF 2021 Missal, ICEL 2011). Add to this list.
MODERN = [
    r"\bet avec ton esprit\b",            # AELF 2021 response
    r"\bje confesse à Dieu tout-puissant, je reconnais devant vous, frères et sœurs\b",
    r"\bvraiment, il est juste et bon\b",
    r"\bAnd with your spirit\b",          # ICEL 2011 response
    r"\bI confess to almighty God and to you, my brothers and sisters\b",
]
CURRENT = re.compile(r"\b(AELF|ICEL|Missel romain \(?2021|Roman Missal,? (third edition|2011))", re.I)


def norm(t):
    return re.sub(r"[^\w ]+", " ", t.lower().replace("’", "'").replace("l'", "")).replace("  ", " ")


def main():
    errs = []
    credits = (ROOT / "data" / "source" / "CREDITS.md")
    ctext = credits.read_text(encoding="utf-8") if credits.exists() else ""
    if not ctext:
        errs.append("credits: data/source/CREDITS.md is missing")
    if not (ROOT / "LICENSE-DATA.md").exists():
        errs.append("credits: LICENSE-DATA.md is missing")
    P = json.loads((ROOT / "data" / "source" / "prayers.json").read_text(encoding="utf-8"))["prayers"]
    for p in P:
        pid, src = p["id"], p.get("source") or ""
        if not src:
            errs.append(f"prayers: {pid} has no source"); continue
        dated = re.search(r"\b(1[0-8]\d\d|19[01]\d|192[0-8])\b", src)
        own = re.search(r"own (French and English |French |English )?translations?", src, re.I)
        stated = re.search(r"treated as public domain", src, re.I)
        if not (dated or own or stated):
            errs.append(f"prayers: {pid}: source names no pre-1929 edition and no own translation")
        if not re.search(r"public domain|CC BY-SA|permission", src, re.I):
            errs.append(f"prayers: {pid}: source does not say how the text may be used (public domain, CC BY-SA, permission)")
        if CURRENT.search(src) and not re.search(r"not used|not cop|not the|do not|does not|Replaces|under copyright|treated as public domain", src, re.I):
            errs.append(f"prayers: {pid}: source names a current liturgical translation without saying it is not copied")
        text = (p.get("fr") or "") + " " + (p.get("en") or "")
        for m in MODERN:
            if re.search(m, text, re.I | re.S):
                errs.append(f"prayers: {pid}: contains wording of a current copyrighted liturgical text ({m})")
        key = " ".join(norm(re.sub(r"^(le|la|les|l')\s*", "", p["title_fr"].split(" (")[0], flags=re.I)).split()[:3])
        if ctext and key not in norm(ctext):
            errs.append(f"credits: CREDITS.md does not name the prayer '{p['title_fr']}'")
    written = re.search(r"## Written for this project\s+(.+?)\n\n", ctext, re.S)
    if not written or not all(w in written.group(1) for w in ("dialogues", "listening")):
        errs.append("writing: the 'Written for this project' paragraph of CREDITS.md must mention the dialogues and listening passages")
    for font in list((ROOT / "village").rglob("*.woff2")) + list((ROOT / "village").rglob("*.ttf")) + list((ROOT / "src" / "fonts").rglob("*.ttf")) if (ROOT / "src" / "fonts").exists() else []:
        lic = [x for x in font.parent.iterdir() if re.search(r"(OFL|LICEN[CS]E)", x.name, re.I)]
        if not lic:
            errs.append(f"credits: font {font.relative_to(ROOT)} has no license file beside it")
    for e in errs:
        print("FAIL", e)
    print(f"copyright: {len(P)} prayers checked, {len(errs)} problem(s)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
