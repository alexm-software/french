#!/usr/bin/env python3
"""QA for the village (village/). Static checks on the built payloads, then (with --browser)
a Playwright pass that measures the rendered page.

Static rules (per building/room):
  * every planned word is present exactly once (planned = vocab room in data/source, or v1 room items)
  * hotspot boxes are inside the painting and never overlap each other
  * no hotspot or label overlaps a door / map-exit hit box, zoom badge or nameplate
  * every room has a 'zooms' list ([] if none); --strict: the nameplate touches no door, hotspot or zoom badge
  * verb streets (map 'streets', id ST_x) go live like buildings: data/st_x.js with building_id ST_x
  * labels carry an article (nouns), are in bounds and never overlap each other
  * feminine words sit on the LEFT half, masculine on the RIGHT (box centre); epicene words 30-70%
  * main room has a painted map exit + a door to every sub-room; each sub-room has backTo=main and
    a door back; every door/zoom target exists; zooms belong to a room and their object rect
    ('obj') in the parent contains the badge
  * verbs have all 7 tenses; card crops and scene images exist; content word blocklist
  * no respelling that reads as pee/poo: say/f_say never contain 'pee'/'poo'; hook/example words pee(s/d/ing), poo(s/p/h)
  * adjectives: no article, centre band 30-70%, gram line 'adjective · m/f' on the card (browser)
  * adverbs: no article, no gender, centre band 30-70%, gram line 'adverb · invariable' (browser)
  * maps (data/map.js): no rect overlap within the world map or within any sector map; world
    sectors with "poly" overlap only when the polygons themselves overlap (4 px sample). Every
    layout building has a rect on its sector map (by the payload's building_id/sector_id, else by id)
  * --browser: world-map signposts stay 6% inside the painting, 3 px apart, and each label centre
    lies inside its own click polygon. Sector hover labels (live and bientôt) stay 6% inside the
    painting at desktop and phone widths
  * placement (scripts/qa/placement.py): a word whose English gloss shares an ambiguous word (bank, firm, fire, star,
    band, scale, lead, stage, race...) with its room's theme is printed as PLACE: it may sit there only through the
    shared English word (river bank in the bank). Kept placements go in data/hooks/qa/placement_ok.tsv with a reason.
    PLACE lines are reports; --placement makes them failures (--strict alone does not, so other packs are not blocked)
  * room size: a room holds at most room_max items (skills/limits.json), except rooms listed with their current
    count in data/hooks/qa/room_size_ok.tsv (the baseline; a listed room may not grow)
  * one hook per word: an id may not carry two different hook texts across rooms, except ids listed in
    data/hooks/qa/two_hooks_ok.tsv (each copy describes its own painting)
  * --browser: the sector maps discover buildings at runtime; the union of live links over all
    sector maps == village/data/<bld>.js files; the main room's exit and Back go to its sector map
Browser rules (--browser, needs a server on --base): rendered hotspot and label rectangles do not
overlap, every route renders with no JS error, Back goes to the right place, verb cards have no
sideways scroll. Screenshots go to --shots.
"""
import argparse, json, re, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
import placement

ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "village"
W, H = 1280, 720
BLOCK = [r"\bgod the father\b", r"dieu le p[eè]re", r"\bdrunk", r"\bbeer\b", r"\bcigar", r"\bsmok(e|ing)\b(?!.*(incense|censer|chimney|smoke rises))",
         r"\bfart", r"\bpoo+\b", r"\bpee\b", r"\bbutt\b", r"\bvomit", r"\bsexy\b", r"\bkill", r"\btobacc"]
SMOKE = BLOCK[5]
TOBACC = BLOCK[-1]
# Narrow exemptions. These nouns use a blocked English word in the planned gloss for a non-smoking sense.
# "la fumée" (fr_fumee_noun, gloss "smoke") is campfire / chimney smoke: the generic smoke pattern is skipped on
# every field. "le tabac" (fr_tabac_noun, gloss "tobacco") is a blank wooden notice board: the generic tobacco
# pattern is skipped on the gloss and example only. For both, hook/scene/note must still be free of any smoking or
# tobacco depiction (TOBACCO below), and every other BLOCK pattern still applies to all fields.
SMOKE_NOUNS = {"fr_fumee_noun"}
TABAC_NOUNS = {"fr_tabac_noun"}
# "le smoking" (fr_smoking_noun, gloss "tuxedo, dinner jacket") is a garment: the French example necessarily contains
# the headword, so the generic smoke pattern is skipped on the example (ex) only; hook/scene/note/en are still checked
# with every BLOCK pattern plus TOBACCO, so the hook must not use the English word.
TUXEDO_NOUNS = {"fr_smoking_noun"}
TOBACCO = r"\b(smoking|smokers?|smokes? (a|his|her|their)\b|cigar\w*|tobacc\w*|pipe ?smoke|puff(s|ing)? on|light(s|ing)? up)\b"
ROOMS_JSON = {r["id"]: r for r in json.loads((ROOT / "data" / "source" / "rooms.json").read_text(encoding="utf-8"))["rooms"]}
LIMITS = json.loads((ROOT / "skills" / "limits.json").read_text(encoding="utf-8"))
QA = ROOT / "data" / "hooks" / "qa"


def load_tsv(name):
    f = QA / name
    if not f.exists():
        return []
    return [l.rstrip("\n").split("\t") for l in f.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]


def site_gates(blds, errs):
    """Room size and one hook per word, with the baseline allowlists."""
    size_ok = {(r[0], r[1]): int(r[2]) for r in load_tsv("room_size_ok.tsv")}
    two_ok = {r[0] for r in load_tsv("two_hooks_ok.tsv")}
    hooks = {}
    for bld in blds:
        if not (V2 / "data" / f"{bld}.js").exists():
            continue
        D = load_payload(bld)
        for key, R in D["rooms"].items():
            n = sum(1 for it in R["items"] if not it.get("noMnemonic"))
            cap = max(LIMITS["room_max"], size_ok.get((bld, key), 0))
            if n > cap:
                errs.append(f"{bld}: {key}: {n} items, more than {cap}" + (" (its allowlisted count in room_size_ok.tsv)" if (bld, key) in size_ok else f" (room_max in skills/limits.json)"))
            for it in R["items"]:
                if it.get("hook"):
                    hooks.setdefault(it["id"], {}).setdefault(it["hook"], f"{bld}/{key}")
    for wid, h in sorted(hooks.items()):
        if len(h) > 1 and wid not in two_ok:
            errs.append(f"{wid}: {len(h)} different hook texts ({', '.join(sorted(h.values()))}); one hook per word, or list it in two_hooks_ok.tsv")


PLACE_OK = placement.load_ok(ROOT / "data" / "hooks" / "qa" / "placement_ok.tsv")
ART = re.compile(r"^(?:(?:le|la|les|le/la|un|une) |l['’])", re.I)  # 'las', 'lent', 'unique' are not articles


def load_payload(bld):
    s = (V2 / "data" / f"{bld}.js").read_text(encoding="utf-8")
    return json.loads(s[s.index("]=") + 2:].rstrip().rstrip(";"))


def inter(a, b):
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


def inside(x, y, ring):
    c = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1): c = not c
    return c


def overlap(a, b):
    """rect overlap, or (when both give "poly") polygon overlap sampled on a 4 px grid"""
    if not inter(a["rect"], b["rect"]): return False
    if not (a.get("poly") and b.get("poly")): return True
    ra, rb = a["rect"], b["rect"]
    x0, y0, x1, y1 = max(ra[0], rb[0]), max(ra[1], rb[1]), min(ra[0] + ra[2], rb[0] + rb[2]), min(ra[1] + ra[3], rb[1] + rb[3])
    for y in range(int(y0) + 2, int(y1), 4):
        for x in range(int(x0) + 2, int(x1), 4):
            if any(inside(x, y, r) for r in a["poly"]) and any(inside(x, y, r) for r in b["poly"]): return True
    return False


def vocab_rooms():
    out = {}
    for line in open(ROOT / "data" / "source" / "vocab.jsonl", encoding="utf-8"):
        if line.strip():
            w = json.loads(line)
            out.setdefault(w["room_id"], []).append(w["id"])
    return out


def v1_room(bld, room):
    s = (ROOT / "data" / "v1-payloads" / f"{bld}.js").read_text(encoding="utf-8")
    d = json.loads(s[s.index("]=") + 2:].rstrip().rstrip(";"))
    return [it["id"] for it in d["rooms"][room]["items"]]


def badge_rect(z):
    w = len(z["label"]) * 10 + 50
    return [z["at"][0] - w / 2, z["at"][1] - 17, w, 34]


def check_building(bld, errs, warns, places=None):
    L = json.loads((ROOT / "content" / "v2" / bld / "layout.json").read_text(encoding="utf-8"))
    D = load_payload(bld)
    VR = vocab_rooms()
    main = D["main"]
    rooms = D["rooms"]
    keys_in_list = [r["key"] for r in D["roomList"]]
    E = lambda m: errs.append(f"{bld}: {m}")
    if main not in rooms or main not in keys_in_list:
        E(f"main room {main} missing")
    seen = {}
    counts = {}
    for key, R in rooms.items():
        tag = f"{key}"
        img = V2 / R["image"]
        if not img.exists():
            E(f"{tag}: image missing {R['image']}")
        elif Image.open(img).size != (W, H):
            E(f"{tag}: image not {W}x{H}")
        # planned words
        plan = (L.get("planned") or {}).get(key)
        ids = [it["id"] for it in R["items"]]
        counts[key] = len(ids)
        if plan:
            want = plan.get("only") or (VR.get(plan["vocabRoom"], []) if "vocabRoom" in plan else v1_room(*plan["v1"].split("/")))
            miss = [w for w in want if w not in ids]
            extra = [w for w in ids if w not in want]
            if miss: E(f"{tag}: missing planned words {miss}")
            if extra: E(f"{tag}: words not planned for this room {extra}")
        else:
            warns.append(f"{bld}/{tag}: no 'planned' list in layout.json; word coverage not checked")
        if places is not None:
            for wid, tok, en in placement.flags(L, key, R, ROOMS_JSON, PLACE_OK):
                places.append(f"{bld}/{tag}: {wid} ('{en}') may be here only through the English word '{tok}'")
        for w in ids:
            if w in seen: E(f"{tag}: {w} also in {seen[w]}")
            seen[w] = key
        if not isinstance(R.get("zooms"), list):
            E(f"{tag}: room has no 'zooms' list (use [] when it has no zoom; app.js iterates R.zooms)")
        # fixed rects
        fixed = [("door->" + d["to"], d["hit"]) for d in R.get("doors", [])]
        if R.get("mapExit"):
            fixed.append(("mapExit", R["mapExit"]["boxPx"]))
        for z in R.get("zooms", []):
            fixed.append(("zoom->" + z["to"], badge_rect(z)))
        boxes = [(it["fr"], it["boxPx"]) for it in R["items"]]
        labs = [(it["fr"], it["labelPx"]) for it in R["items"]]
        for n, b in boxes + labs + fixed:
            if b[0] < 0 or b[1] < 0 or b[0] + b[2] > W + 0.5 or b[1] + b[3] > H + 0.5:
                E(f"{tag}: {n} out of bounds {b}")
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                if inter(boxes[i][1], boxes[j][1]): E(f"{tag}: hotspots overlap: {boxes[i][0]} / {boxes[j][0]}")
        for i in range(len(labs)):
            for j in range(i + 1, len(labs)):
                if inter(labs[i][1], labs[j][1]): E(f"{tag}: labels overlap: {labs[i][0]} / {labs[j][0]}")
        for n, f in fixed:
            for m, b in boxes:
                if inter(f, b): E(f"{tag}: hotspot {m} overlaps {n}")
            for m, b in labs:
                if inter(f, b): E(f"{tag}: label {m} overlaps {n}")
        for (m, b), (_, l) in zip(boxes, labs):
            for (m2, b2) in boxes:
                if m2 != m and inter(l, b2): warns.append(f"{bld}/{tag}: label {m} touches hotspot {m2}")
        # items
        for it in R["items"]:
            cx = (it["boxPx"][0] + it["boxPx"][2] / 2) / W
            g = it.get("g")
            if it.get("adj"):
                if not 0.3 <= cx <= 0.7: E(f"{tag}: adjective {it['fr']} not in the centre band ({cx:.0%})")
                if it.get("art") or ART.match(it["fr"] + " "): E(f"{tag}: adjective {it['fr']} carries an article")
            elif it.get("adv"):
                if not 0.3 <= cx <= 0.7: E(f"{tag}: adverb {it['fr']} not in the centre band ({cx:.0%})")
                if it.get("art") or it.get("g") != "adv": E(f"{tag}: adverb {it['fr']} carries an article/gender")
            elif not it.get("verb"):
                if g == "f" and cx >= 0.5: E(f"{tag}: feminine {it['fr']} not on the left ({cx:.0%})")
                if g == "m" and cx <= 0.5: E(f"{tag}: masculine {it['fr']} not on the right ({cx:.0%})")
                if g == "mf" and not 0.3 <= cx <= 0.7: E(f"{tag}: epicene {it['fr']} far from centre ({cx:.0%})")
                hw = (("l'" + it["fr"]) if it["art"] == "l'" else f"{it['art']} {it['fr']}")
                if not ART.match(hw): E(f"{tag}: label without article: {hw}")
            else:
                if len(it.get("tenses") or []) != 7: E(f"{tag}: verb {it['fr']} has {len(it.get('tenses') or [])} tenses, need 7")
            if not (V2 / it["cardSrc"]).exists(): E(f"{tag}: card image missing for {it['fr']}")
            # alphabet exception: letters on the blackboard zoom carry no mnemonic (noMnemonic "alphabet", letters only)
            alpha = it.get("noMnemonic") == "alphabet"
            if alpha and not (it.get("gramLine") or "").startswith("letter of the alphabet"): E(f"{tag}: noMnemonic on a non-letter {it['fr']}")
            if not it.get("hook") and not alpha: E(f"{tag}: no memory hook for {it['fr']}")
            # "plaque": true (set from hooks.json) = the word appears only as text on a blank museum plaque, nothing is
            # depicted: the gloss (en) is not content-filtered for that item; hook/scene/note/ex still are.
            plaque = it.get("plaque") is True
            text = " ".join(str(it.get(k) or "") for k in ("hook", "scene", "note") + (() if plaque else ("en",))) + " " + " ".join(it.get("ex") or [])
            depict = " ".join(str(it.get(k) or "") for k in ("hook", "scene", "note"))
            smoke_noun = it["id"] in SMOKE_NOUNS and not it.get("verb") and it.get("en", "").strip().lower() == "smoke"
            tabac_noun = it["id"] in TABAC_NOUNS and not it.get("verb") and "tobacco" in (it.get("en") or "").strip().lower()
            tux_noun = it["id"] in TUXEDO_NOUNS and not it.get("verb") and "tuxedo" in (it.get("en") or "").lower()
            for pat in BLOCK:
                if smoke_noun and pat == SMOKE: continue
                if tux_noun and pat == SMOKE:
                    if re.search(pat, text[:len(text) - len(" ".join(it.get("ex") or []))], re.I): E(f"{tag}: content flag /{pat}/ in {it['fr']}")
                    if re.search(TOBACCO, depict, re.I): E(f"{tag}: content flag /{TOBACCO}/ (smoking) in {it['fr']}")
                    continue
                if tabac_noun and pat == TOBACC:
                    if re.search(pat, depict, re.I): E(f"{tag}: content flag /{pat}/ in {it['fr']}")
                    continue
                if re.search(pat, text, re.I): E(f"{tag}: content flag /{pat}/ in {it['fr']}")
            if smoke_noun or tabac_noun:
                if re.search(TOBACCO, depict, re.I): E(f"{tag}: content flag /{TOBACCO}/ (smoking) in {it['fr']}")
            # respellings must not read as "pee"/"poo" (fix in content/v2/vocab_fixes.json "say"/"f_say"/"hook")
            for k in ("say", "f_say"):
                if re.search(r"p(ee|oo)", it.get(k) or "", re.I): E(f"{tag}: {k} '{it.get(k)}' of {it['fr']} contains pee/poo")
            for tok in re.findall(r"[A-Za-z]+", text):
                if re.fullmatch(r"p(ee|oo)(s|ss|d|p|h|ng|ing)?", tok, re.I): E(f"{tag}: respelling '{tok}' in {it['fr']} reads as pee/poo")
        # routes
        for d in R.get("doors", []):
            if d.get("building"):  # door into another building's room
                if not (V2 / "data" / f"{d['building']}.js").exists(): E(f"{tag}: door to unknown building {d['building']}")
                elif d["to"] not in load_payload(d["building"])["rooms"]: E(f"{tag}: door to unknown room {d['building']}/{d['to']}")
            elif d["to"] not in rooms: E(f"{tag}: door to unknown room {d['to']}")
            if not d.get("hit"): E(f"{tag}: door to {d['to']} has no painted hit box")
        for z in R.get("zooms", []):
            Z = rooms.get(z["to"])
            if not Z: E(f"{tag}: zoom to unknown {z['to']}")
            elif Z.get("parent") != key: E(f"{tag}: zoom {z['to']} parent is {Z.get('parent')}")
            o = z.get("obj")
            if not o: E(f"{tag}: zoom {z['to']} has no 'obj' rect (object visible in parent)")
            elif not (o[0] <= z["at"][0] <= o[0] + o[2] and o[1] <= z["at"][1] <= o[1] + o[3]): E(f"{tag}: zoom badge not on its object")
        if R.get("parent"):
            P = rooms.get(R["parent"])
            if not P or P.get("parent"): E(f"{tag}: zoom parent invalid")
            if not any(z["to"] == key for z in (P or {}).get("zooms", [])): E(f"{tag}: parent has no badge to this zoom")
        elif key == main:
            if not R.get("mapExit"): E(f"{tag}: main room has no painted exit to the village")
            for k2 in keys_in_list:
                if k2 != main and rooms.get(k2, {}).get("backTo", main) == main and not any(d["to"] == k2 for d in R.get("doors", [])): E(f"{tag}: no painted door to sub-room {k2}")
        else:
            if key not in keys_in_list: E(f"{tag}: room not in roomList")
            # a sub-room is entered from main, or from another listed sub-room (nested, e.g. maths -> recre);
            # Back goes to the room it was entered from, and both rooms need a real painted door.
            bt = R.get("backTo")
            if bt != main and (bt not in keys_in_list or rooms.get(bt, {}).get("backTo") != main):
                E(f"{tag}: Back goes to {bt}, should be {main} (or a sub-room of {main})")
            elif bt != main and not any(d["to"] == key for d in rooms[bt].get("doors", [])):
                E(f"{tag}: {bt} has no painted door to sub-room {key}")
            if not any(d["to"] == bt for d in R.get("doors", [])): E(f"{tag}: no painted door back to {bt}")
    return counts


def map_home(M, bld, D):
    """(slug, entry) of a building on the sector maps: payload building_id/sector_id first, then registry id."""
    pid = lambda b: b.get("id") or re.sub(r"^B\d+_", "", b["building_id"])
    slug = next((w["slug"] for w in M["world"]["sectors"] if w["id"] == D.get("sector_id")), None)
    for sl, S in M["sectors"].items():
        # verb streets: data id = street id lowercased (ST_priere -> data/st_priere.js), as in app.js
        for b in S["buildings"] + [{"id": t["id"].lower(), **{k: v for k, v in t.items() if k != "id"}} for t in S["streets"]]:
            if pid(b) == bld and (slug is None or sl == slug):
                return sl, b
    return slug, None


MAP_LABEL_EDGES = r"""
() => {
  const stage = document.getElementById('stage');
  const sr = stage.getBoundingClientRect();
  const m = 0.06, L = sr.width * m, T = sr.height * m, R = sr.width * (1 - m), B = sr.height * (1 - m);
  const bad = [];
  const judge = (el) => {
    if (el.classList.contains('pin')) return;
    el.style.transition = 'none';
    const r = el.getBoundingClientRect();
    const b = {l: r.left - sr.left, t: r.top - sr.top, r: r.right - sr.left, b: r.bottom - sr.top};
    if (b.l < L - 0.5 || b.t < T - 0.5 || b.r > R + 0.5 || b.b > B + 0.5) {
      bad.push((el.innerText || '').replace(/\s+/g, ' ').trim() + ' @' + [b.l, b.t, b.r, b.b].map(n => Math.round(n)).join(','));
    }
  };
  document.querySelectorAll('#stage .tag.live').forEach(el => { el.classList.add('show'); judge(el); el.classList.remove('show'); });
  document.querySelectorAll('#stage .bld.soon').forEach(p => {
    p.dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
    const ts = document.getElementById('tagSoon');
    if (ts && ts.classList.contains('show')) judge(ts);
    p.dispatchEvent(new MouseEvent('mouseleave', {bubbles: true}));
  });
  return bad;
}
"""


async def map_label_edges(pg, where, errs):
    for item in await pg.evaluate(MAP_LABEL_EDGES):
        errs.append(f"{where}: map label crosses the 6% margin: {item}")


async def browser_checks(blds, base, shots, errs, strict=False, M=None, maps_only=False):
    from playwright.async_api import async_playwright
    shots.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for vw, vh in ((1400, 860), (900, 1200)):
            pg = await b.new_page(viewport={"width": vw, "height": vh})
            jserr = []
            pg.on("pageerror", lambda e: jserr.append(str(e)))
            await pg.goto(base + "#/")
            try:
                await pg.wait_for_function("document.getElementById('stage').dataset.probed==='1'", timeout=8000)
            except Exception:
                errs.append(f"map @{vw}: building discovery never finished (stage.dataset.probed)")
            await pg.wait_for_timeout(400)
            WH = M["world"].get("h", 720)
            wl = await pg.evaluate("[...document.querySelectorAll('a.lnk')].map(a=>a.getAttribute('href'))")
            if sorted(wl) != sorted(f"#/quartier/{w['slug']}" for w in M["world"]["sectors"]):
                errs.append(f"world map @{vw}: sector links {wl}")
            # world signposts: inside the painting with a 6% margin, centred inside their own click polygon, touching nothing
            pins = await pg.evaluate("""(()=>{const S=document.getElementById('stage').getBoundingClientRect();
              return [...document.querySelectorAll('.tag.pin')].map(e=>{const r=e.getBoundingClientRect();
                return {t:e.textContent,x0:(r.left-S.left)/S.width*1280,y0:(r.top-S.top)/S.height*%d,x1:(r.right-S.left)/S.width*1280,y1:(r.bottom-S.top)/S.height*%d}})})()""" % (WH, WH))
            for k, p in enumerate(pins):  # tall world (world.h): same 43.2-unit top/bottom margin as a 720 painting
                if p["x0"] < 76.8 or p["y0"] < 43.2 or p["x1"] > 1203.2 or p["y1"] > WH - 43.2:
                    errs.append(f"world map @{vw}: label '{p['t']}' is within 6% of the painting edge")
                for q in pins[k + 1:]:
                    if p["x0"] < q["x1"] + 3 and q["x0"] < p["x1"] + 3 and p["y0"] < q["y1"] + 3 and q["y0"] < p["y1"] + 3:
                        errs.append(f"world map @{vw}: label '{p['t']}' touches '{q['t']}'")
            for w in M["world"]["sectors"]:
                if w.get("poly") and not any(inside(w["tag"][0], w["tag"][1], r) for r in w["poly"]):
                    errs.append(f"world map: {w['name']} label centre is outside its click area")
            await pg.screenshot(path=str(shots / f"map_{vw}.png"))
            if M["world"].get("h"):  # tall world: scroll to each district, click its painted area (not the label), Back must restore the scroll
                await pg.screenshot(path=str(shots / f"map_{vw}_full.png"), full_page=False)
                for w in M["world"]["sectors"]:
                    x, y = w["door"]
                    st = await pg.evaluate(f"""(()=>{{const sc=document.getElementById('scroller'),S=document.getElementById('stage'),k=S.offsetWidth/1280;
                      sc.scrollTop=Math.max(0,{y}*k-sc.clientHeight/2); sc.scrollLeft=Math.max(0,{x}*k-sc.clientWidth/2); return sc.scrollTop}})()""")
                    await pg.wait_for_timeout(120)
                    pt = await pg.evaluate(f"""(()=>{{const S=document.getElementById('stage').getBoundingClientRect(),k=S.width/1280;return [S.left+{x}*k,S.top+{y}*k]}})()""")
                    await pg.mouse.click(pt[0], pt[1]); await pg.wait_for_timeout(250)
                    if await pg.evaluate("location.hash") != f"#/quartier/{w['slug']}":
                        errs.append(f"world map @{vw}: click on {w['slug']} area at {w['door']} went to {await pg.evaluate('location.hash')}"); await pg.goto(base + "#/"); continue
                    await pg.click("#back"); await pg.wait_for_timeout(300)
                    st2 = await pg.evaluate("document.getElementById('scroller').scrollTop")
                    if abs(st2 - st) > 4: errs.append(f"world map @{vw}: scroll not restored after {w['slug']} ({st} -> {st2})")
            live = []
            for w in M["world"]["sectors"]:
                await pg.goto(base + f"#/quartier/{w['slug']}")
                await pg.wait_for_function("document.getElementById('stage').dataset.probed==='1'", timeout=8000)
                await pg.wait_for_timeout(250)
                if await pg.evaluate("location.hash") != f"#/quartier/{w['slug']}":
                    errs.append(f"sector {w['slug']}: route redirected"); continue
                ln = await pg.evaluate("[...document.querySelectorAll('a.lnk')].map(a=>a.getAttribute('href').slice(2))")
                nsoon = await pg.evaluate("document.querySelectorAll('.bld.soon').length")
                S = M["sectors"][w["slug"]]
                if len(ln) + nsoon != len(S["buildings"]) + len(S["streets"]):
                    errs.append(f"sector {w['slug']} @{vw}: {len(ln)} live + {nsoon} soon != {len(S['buildings'])} buildings + {len(S['streets'])} streets")
                live += ln
                if ln or vw == 1400: await pg.screenshot(path=str(shots / f"sector_{w['slug']}_{vw}.png"))
                await map_label_edges(pg, f"sector {w['slug']} @{vw}", errs)
                await pg.click("#back"); await pg.wait_for_timeout(200)
                if await pg.evaluate("location.hash") not in ("#/", ""): errs.append(f"sector {w['slug']}: Back does not go to the village map")
            have = sorted(p.stem for p in (V2 / "data").glob("*.js") if p.stem not in ("map", "live", "index", "listening", "prayers"))
            if sorted(live) != have:
                errs.append(f"maps @{vw}: live buildings {sorted(live)} != data files {have}")
            if maps_only:
                for e in jserr: errs.append(f"JS error @{vw}: {e}")
                await pg.close()
                continue
            for bld in blds:
                D = load_payload(bld)
                for key, R in D["rooms"].items():
                    route = f"#/{bld}" if key == D["main"] else f"#/{bld}/{key}"
                    await pg.goto(base + route)
                    await pg.wait_for_timeout(700)
                    if await pg.evaluate("location.hash") != route:
                        errs.append(f"{bld}/{key}: route {route} redirected"); continue
                    rects = await pg.evaluate("""()=>{const r=e=>{const b=e.getBoundingClientRect();return [b.left,b.top,b.width,b.height]};
                      return {hot:[...document.querySelectorAll('.hot')].map(r),lab:[...document.querySelectorAll('.lab')].map(r),
                              door:[...document.querySelectorAll('.doorway')].map(r)}}""")
                    for kind in ("hot", "lab"):
                        A = rects[kind]
                        for i in range(len(A)):
                            for j in range(i + 1, len(A)):
                                if inter(A[i], A[j]):
                                    errs.append(f"{bld}/{key} @{vw}: rendered {kind} {R['items'][i]['fr']} overlaps {R['items'][j]['fr']}")
                    # doors into another building link to that building's room
                    hrefs = await pg.evaluate("[...document.querySelectorAll('a.doorway:not(.mapexit)')].map(a=>a.getAttribute('href'))")
                    for d, hr in zip(R.get("doors", []), hrefs):
                        b2 = d.get("building") or bld
                        want_d = f"#/{b2}" if d["to"] == b2 else f"#/{b2}/{d['to']}"
                        if hr != want_d: errs.append(f"{bld}/{key}: door to {d['to']} links {hr}, expected {want_d}")
                    for i, d in enumerate(rects["door"]):
                        for j, h in enumerate(rects["hot"]):
                            if inter(d, h): errs.append(f"{bld}/{key} @{vw}: door/exit {i} overlaps hotspot {R['items'][j]['fr']}")
                        for j, h in enumerate(rects["lab"]):
                            if inter(d, h): errs.append(f"{bld}/{key} @{vw}: door/exit {i} overlaps label {R['items'][j]['fr']}")
                    if strict:
                        ex = await pg.evaluate("""()=>{const r=e=>{const b=e.getBoundingClientRect();return [b.left,b.top,b.width,b.height]};
                          const st=document.getElementById('stage').getBoundingClientRect();
                          return {zoom:[...document.querySelectorAll('.zoombadge')].map(r),plate:[...document.querySelectorAll('.room-nameplate')].map(r),
                                  stage:[st.left,st.top,st.width,st.height],
                                  nav:[...document.querySelectorAll('#rooms:not([hidden])')].map(r)}}""")
                        g = 3  # px: "touching" another thing = closer than this
                        ge = 8  # px: minimum clear gap between a label and the scene edge
                        grow = lambda a: [a[0] - g, a[1] - g, a[2] + 2 * g, a[3] + 2 * g]
                        L, H = rects["lab"], rects["hot"]
                        nm = lambda i: R['items'][i]['fr']
                        for i in range(len(L)):
                            for j in range(i + 1, len(L)):
                                if inter(grow(L[i]), L[j]): errs.append(f"{bld}/{key} @{vw}: label {nm(i)} touches label {nm(j)}")
                            for j in range(len(H)):
                                if j != i and inter(grow(L[i]), H[j]): errs.append(f"{bld}/{key} @{vw}: label {nm(i)} touches hotspot {nm(j)}")
                            for j, d in enumerate(rects["door"]):
                                if inter(grow(L[i]), d): errs.append(f"{bld}/{key} @{vw}: label {nm(i)} touches door/exit {j}")
                            for z in ex["zoom"] + ex["plate"]:
                                if inter(grow(L[i]), z): errs.append(f"{bld}/{key} @{vw}: label {nm(i)} touches a zoom badge/nameplate")
                            S_, l = ex["stage"], L[i]
                            if l[0] < S_[0] + ge or l[1] < S_[1] + ge or l[0] + l[2] > S_[0] + S_[2] - ge or l[1] + l[3] > S_[1] + S_[3] - ge:
                                errs.append(f"{bld}/{key} @{vw}: label {nm(i)} is closer than {ge}px to the scene edge")
                        # the room list (when it drops below the strip) must not cover any label, door or zoom badge
                        for n_ in ex["nav"]:
                            for i in range(len(L)):
                                if inter(n_, L[i]): errs.append(f"{bld}/{key} @{vw}: room list covers label {nm(i)}")
                            for j, d in enumerate(rects["door"] + ex["zoom"] + ex["plate"]):
                                if inter(n_, d): errs.append(f"{bld}/{key} @{vw}: room list covers door/badge/nameplate {j}")
                        # nameplate: must not touch doors/exits, hotspots or zoom badges either
                        for p_ in ex["plate"]:
                            for j, d in enumerate(rects["door"]):
                                if inter(grow(p_), d): errs.append(f"{bld}/{key} @{vw}: nameplate touches door/exit {j}")
                            for j in range(len(H)):
                                if inter(grow(p_), H[j]): errs.append(f"{bld}/{key} @{vw}: nameplate touches hotspot {nm(j)}")
                            for z in ex["zoom"]:
                                if inter(grow(p_), z): errs.append(f"{bld}/{key} @{vw}: nameplate touches a zoom badge")
                    await pg.screenshot(path=str(shots / f"{bld}_{key}_{vw}.png"))
                    # back target
                    await pg.click("#back")
                    await pg.wait_for_timeout(300)
                    home = "#/quartier/" + map_home(M, bld, D)[0]
                    bt = R.get("parent") or R.get("backTo")
                    want = f"#/{bld}/{bt}" if bt and bt != D["main"] else (f"#/{bld}" if bt else home)
                    got = await pg.evaluate("location.hash")
                    if got != want: errs.append(f"{bld}/{key}: Back went to {got}, expected {want}")
                    # painted exit of the main room goes to the sector map (or its mapExit.href)
                    await pg.goto(base + route); await pg.wait_for_timeout(500)
                    if key == D["main"]:
                        xh = await pg.evaluate("(document.querySelector('a.mapexit')||{getAttribute:()=>null}).getAttribute('href')")
                        if xh != (R["mapExit"].get("href") or home): errs.append(f"{bld}: map exit goes to {xh}, expected {R['mapExit'].get('href') or home}")
                    # adjective cards: no article, adjective gram line
                    for i, it in enumerate(R["items"]):
                        if not (it.get("adj") or it.get("adv")): continue
                        kind = "adjective" if it.get("adj") else "adverb"
                        lab = await pg.evaluate(f"document.querySelectorAll('.lab')[{i}].textContent")
                        # alphabet board: the label is the item's "lab" ("A — a"), which must start with the letter itself
                        want_lab = it.get("lab") if (it.get("noMnemonic") == "alphabet" and (it.get("lab") or "").startswith(it["fr"] + " ")) else it["fr"]
                        if lab.strip() != want_lab: errs.append(f"{bld}/{key}: {kind} label '{lab}' has an article")
                        await pg.evaluate(f"document.querySelectorAll('.hot')[{i}].click()"); await pg.wait_for_timeout(200)
                        gl = await pg.evaluate("(document.querySelector('#card .gram')||{}).textContent||''")
                        want = "adjective · " if it.get("adj") else (it.get("gramLine") or "adverb · invariable")
                        if not gl.startswith(want): errs.append(f"{bld}/{key}: {kind} card {it['fr']} gram line '{gl}'")
                        await pg.keyboard.press("Escape")
                    # verb cards: no sideways scroll
                    for i, it in enumerate(R["items"]):
                        if not it.get("verb"): continue
                        await pg.evaluate(f"document.querySelectorAll('.hot')[{i}].click()")
                        await pg.wait_for_timeout(200)
                        info = await pg.evaluate("()=>{const c=document.querySelector('#card');return [c.scrollWidth,c.clientWidth,document.querySelectorAll('#card .tab').length]}")
                        if info[0] > info[1] + 1: errs.append(f"{bld}/{key} @{vw}: verb card {it['fr']} scrolls sideways")
                        if info[2] != 7: errs.append(f"{bld}/{key}: verb card {it['fr']} shows {info[2]} tenses")
                        await pg.keyboard.press("Escape")
            for e in jserr: errs.append(f"JS error @{vw}: {e}")
            await pg.close()
        await b.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("buildings", nargs="*")
    ap.add_argument("--browser", action="store_true")
    ap.add_argument("--base", default="http://localhost:8765/index.html")
    ap.add_argument("--shots", default="/tmp/v2_shots")
    ap.add_argument("--strict", action="store_true", help="labels may not touch anything (3 px gap to other things, 8 px to the scene edge) and warnings count as failures")
    ap.add_argument("--maps-only", action="store_true", help="with --browser, check the world map and sector maps and skip room pages")
    ap.add_argument("--placement", action="store_true", help="PLACE lines (word tied to its room only by a shared English gloss word) count as failures")
    ap.add_argument("-v", "--verbose", action="store_true", help="print each building's word counts")
    a = ap.parse_args()
    blds = a.buildings or sorted(p.parent.name for p in (ROOT / "content" / "v2").glob("*/layout.json"))
    errs, warns, places = [], [], []
    nb = nw = 0
    s = (V2 / "data" / "map.js").read_text(encoding="utf-8")
    M = json.loads(s[s.index("=") + 1:].rstrip().rstrip(";"))
    maps = [("world", M["world"]["sectors"])] + [(sl, S["buildings"] + S["streets"]) for sl, S in M["sectors"].items()]
    for nm, allb in maps:
        for i in range(len(allb)):
            for j in range(i + 1, len(allb)):
                if overlap(allb[i], allb[j]): errs.append(f"map {nm}: {allb[i]['name']} overlaps {allb[j]['name']}")
    for w in M["world"]["sectors"]:
        if w["slug"] not in M["sectors"]: errs.append(f"map: sector {w['id']} has no sector map")
        elif not (V2 / M["sectors"][w["slug"]]["image"]).exists(): errs.append(f"map: {w['slug']} painting missing")
    for bld in blds:
        if not (V2 / "data" / f"{bld}.js").exists(): continue
        sl, b = map_home(M, bld, load_payload(bld))
        if not b: errs.append(f"map: {bld} has a layout but no rect on its sector map in content/v2/map.json")
        c = check_building(bld, errs, warns, places)
        nb += 1; nw += sum(c.values())
        if a.verbose: print(f"{bld}: " + ", ".join(f"{k} {n}" for k, n in c.items()) + f" = {sum(c.values())} words")
    site_gates(blds, errs)
    print(f"{nb} buildings, {nw} words checked")
    if a.browser:
        import asyncio
        asyncio.run(browser_checks(blds, a.base, Path(a.shots), errs, a.strict, M, a.maps_only))
    if a.strict: errs += [f"(strict) {w}" for w in warns]; warns = []
    for w in warns: print("WARN", w)
    for p in places: print("PLACE", p)
    if a.placement: errs += [f"(placement) {p}" for p in places]
    for e in errs: print("FAIL", e)
    print("PASS" if not errs else f"{len(errs)} problem(s)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
