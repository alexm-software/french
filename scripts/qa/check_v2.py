#!/usr/bin/env python3
"""QA for the v2 village (village/v2/). Static checks on the built payloads, then (with --browser)
a Playwright pass that measures the rendered page.

Static rules (per building/room):
  * every planned word is present exactly once (planned = vocab room in data/source, or v1 room items)
  * hotspot boxes are inside the painting and never overlap each other
  * no hotspot or label overlaps a door / map-exit hit box, zoom badge or nameplate
  * labels carry an article (nouns), are in bounds and never overlap each other
  * feminine words sit on the LEFT half, masculine on the RIGHT (box centre); epicene words 30-70%
  * main room has a painted map exit + a door to every sub-room; each sub-room has backTo=main and
    a door back; every door/zoom target exists; zooms belong to a room and their object rect
    ('obj') in the parent contains the badge
  * verbs have all 7 tenses; card crops and scene images exist; content word blocklist
  * adjectives: no article, centre band 30-70%, gram line 'adjective · m/f' on the card (browser)
  * maps (data/map.js): no rect overlap within the world map or within any sector map; every
    layout building has a rect on its sector map (by the payload's building_id/sector_id, else by id)
  * --browser: the sector maps discover buildings at runtime; the union of live links over all
    sector maps == village/v2/data/<bld>.js files; the main room's exit and Back go to its sector map
Browser rules (--browser, needs a server on --base): rendered hotspot and label rectangles do not
overlap, every route renders with no JS error, Back goes to the right place, verb cards have no
sideways scroll. Screenshots go to --shots.
"""
import argparse, json, re, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "village" / "v2"
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
TOBACCO = r"\b(smoking|smokers?|smokes? (a|his|her|their)\b|cigar\w*|tobacc\w*|pipe ?smoke|puff(s|ing)? on|light(s|ing)? up)\b"
ART = re.compile(r"^(le|la|les|l'|le/la|un|une) ?", re.I)


def load_payload(bld):
    s = (V2 / "data" / f"{bld}.js").read_text(encoding="utf-8")
    return json.loads(s[s.index("]=") + 2:].rstrip().rstrip(";"))


def inter(a, b):
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


def vocab_rooms():
    out = {}
    for line in open(ROOT / "data" / "source" / "vocab.jsonl", encoding="utf-8"):
        if line.strip():
            w = json.loads(line)
            out.setdefault(w["room_id"], []).append(w["id"])
    return out


def v1_room(bld, room):
    s = (ROOT / "village" / "assets" / "data" / f"{bld}.js").read_text(encoding="utf-8")
    d = json.loads(s[s.index("]=") + 2:].rstrip().rstrip(";"))
    return [it["id"] for it in d["rooms"][room]["items"]]


def badge_rect(z):
    w = len(z["label"]) * 10 + 50
    return [z["at"][0] - w / 2, z["at"][1] - 17, w, 34]


def check_building(bld, errs, warns):
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
        for w in ids:
            if w in seen: E(f"{tag}: {w} also in {seen[w]}")
            seen[w] = key
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
            elif not it.get("verb"):
                if g == "f" and cx >= 0.5: E(f"{tag}: feminine {it['fr']} not on the left ({cx:.0%})")
                if g == "m" and cx <= 0.5: E(f"{tag}: masculine {it['fr']} not on the right ({cx:.0%})")
                if g == "mf" and not 0.3 <= cx <= 0.7: E(f"{tag}: epicene {it['fr']} far from centre ({cx:.0%})")
                hw = (("l'" + it["fr"]) if it["art"] == "l'" else f"{it['art']} {it['fr']}")
                if not ART.match(hw): E(f"{tag}: label without article: {hw}")
            else:
                if len(it.get("tenses") or []) != 7: E(f"{tag}: verb {it['fr']} has {len(it.get('tenses') or [])} tenses, need 7")
            if not (V2 / it["cardSrc"]).exists(): E(f"{tag}: card image missing for {it['fr']}")
            if not it.get("hook"): E(f"{tag}: no memory hook for {it['fr']}")
            text = " ".join(str(it.get(k) or "") for k in ("hook", "scene", "note", "en")) + " " + " ".join(it.get("ex") or [])
            depict = " ".join(str(it.get(k) or "") for k in ("hook", "scene", "note"))
            smoke_noun = it["id"] in SMOKE_NOUNS and not it.get("verb") and it.get("en", "").strip().lower() == "smoke"
            tabac_noun = it["id"] in TABAC_NOUNS and not it.get("verb") and "tobacco" in (it.get("en") or "").strip().lower()
            for pat in BLOCK:
                if smoke_noun and pat == SMOKE: continue
                if tabac_noun and pat == TOBACC:
                    if re.search(pat, depict, re.I): E(f"{tag}: content flag /{pat}/ in {it['fr']}")
                    continue
                if re.search(pat, text, re.I): E(f"{tag}: content flag /{pat}/ in {it['fr']}")
            if smoke_noun or tabac_noun:
                if re.search(TOBACCO, depict, re.I): E(f"{tag}: content flag /{TOBACCO}/ (smoking) in {it['fr']}")
        # routes
        for d in R.get("doors", []):
            if d["to"] not in rooms: E(f"{tag}: door to unknown room {d['to']}")
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
                if k2 != main and not any(d["to"] == k2 for d in R.get("doors", [])): E(f"{tag}: no painted door to sub-room {k2}")
        else:
            if key not in keys_in_list: E(f"{tag}: room not in roomList")
            if R.get("backTo") != main: E(f"{tag}: Back goes to {R.get('backTo')}, should be {main}")
            if not any(d["to"] == main for d in R.get("doors", [])): E(f"{tag}: no painted door back to {main}")
    return counts


def map_home(M, bld, D):
    """(slug, entry) of a building on the sector maps: payload building_id/sector_id first, then registry id."""
    pid = lambda b: b.get("id") or re.sub(r"^B\d+_", "", b["building_id"])
    slug = next((w["slug"] for w in M["world"]["sectors"] if w["id"] == D.get("sector_id")), None)
    for sl, S in M["sectors"].items():
        for b in S["buildings"]:
            if pid(b) == bld and (slug is None or sl == slug):
                return sl, b
    return slug, None


async def browser_checks(blds, base, shots, errs, strict=False, M=None):
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
            wl = await pg.evaluate("[...document.querySelectorAll('a.lnk')].map(a=>a.getAttribute('href'))")
            if sorted(wl) != sorted(f"#/quartier/{w['slug']}" for w in M["world"]["sectors"]):
                errs.append(f"world map @{vw}: sector links {wl}")
            await pg.screenshot(path=str(shots / f"map_{vw}.png"))
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
                await pg.click("#back"); await pg.wait_for_timeout(200)
                if await pg.evaluate("location.hash") not in ("#/", ""): errs.append(f"sector {w['slug']}: Back does not go to the village map")
            have = sorted(p.stem for p in (V2 / "data").glob("*.js") if p.stem != "map")
            if sorted(live) != have:
                errs.append(f"maps @{vw}: live buildings {sorted(live)} != data files {have}")
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
                    for i, d in enumerate(rects["door"]):
                        for j, h in enumerate(rects["hot"]):
                            if inter(d, h): errs.append(f"{bld}/{key} @{vw}: door/exit {i} overlaps hotspot {R['items'][j]['fr']}")
                        for j, h in enumerate(rects["lab"]):
                            if inter(d, h): errs.append(f"{bld}/{key} @{vw}: door/exit {i} overlaps label {R['items'][j]['fr']}")
                    if strict:
                        ex = await pg.evaluate("""()=>{const r=e=>{const b=e.getBoundingClientRect();return [b.left,b.top,b.width,b.height]};
                          const st=document.getElementById('stage').getBoundingClientRect();
                          return {zoom:[...document.querySelectorAll('.zoombadge')].map(r),plate:[...document.querySelectorAll('.room-nameplate')].map(r),
                                  stage:[st.left,st.top,st.width,st.height]}}""")
                        g = 2  # px: "touching" = closer than this
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
                            S, l = ex["stage"], L[i]
                            if l[0] < S[0] + g or l[1] < S[1] + g or l[0] + l[2] > S[0] + S[2] - g or l[1] + l[3] > S[1] + S[3] - g:
                                errs.append(f"{bld}/{key} @{vw}: label {nm(i)} touches the scene edge")
                    await pg.screenshot(path=str(shots / f"{bld}_{key}_{vw}.png"))
                    # back target
                    await pg.click("#back")
                    await pg.wait_for_timeout(300)
                    home = "#/quartier/" + map_home(M, bld, D)[0]
                    want = f"#/{bld}/{R['parent']}" if R.get("parent") and R["parent"] != D["main"] else (f"#/{bld}" if (R.get("parent") or R.get("backTo")) else home)
                    got = await pg.evaluate("location.hash")
                    if got != want: errs.append(f"{bld}/{key}: Back went to {got}, expected {want}")
                    # painted exit of the main room goes to the sector map (or its mapExit.href)
                    await pg.goto(base + route); await pg.wait_for_timeout(500)
                    if key == D["main"]:
                        xh = await pg.evaluate("(document.querySelector('a.mapexit')||{getAttribute:()=>null}).getAttribute('href')")
                        if xh != (R["mapExit"].get("href") or home): errs.append(f"{bld}: map exit goes to {xh}, expected {R['mapExit'].get('href') or home}")
                    # adjective cards: no article, adjective gram line
                    for i, it in enumerate(R["items"]):
                        if not it.get("adj"): continue
                        lab = await pg.evaluate(f"document.querySelectorAll('.lab')[{i}].textContent")
                        if lab.strip() != it["fr"]: errs.append(f"{bld}/{key}: adjective label '{lab}' has an article")
                        await pg.evaluate(f"document.querySelectorAll('.hot')[{i}].click()"); await pg.wait_for_timeout(200)
                        gl = await pg.evaluate("(document.querySelector('#card .gram')||{}).textContent||''")
                        if not gl.startswith("adjective · "): errs.append(f"{bld}/{key}: adjective card {it['fr']} gram line '{gl}'")
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
    ap.add_argument("--base", default="http://localhost:8765/v2/index.html")
    ap.add_argument("--shots", default="/tmp/v2_shots")
    ap.add_argument("--strict", action="store_true", help="labels may not touch anything (2 px gap, scene edge included) and warnings count as failures")
    a = ap.parse_args()
    blds = a.buildings or sorted(p.parent.name for p in (ROOT / "content" / "v2").glob("*/layout.json"))
    errs, warns = [], []
    s = (V2 / "data" / "map.js").read_text(encoding="utf-8")
    M = json.loads(s[s.index("=") + 1:].rstrip().rstrip(";"))
    maps = [("world", M["world"]["sectors"])] + [(sl, S["buildings"] + S["streets"]) for sl, S in M["sectors"].items()]
    for nm, allb in maps:
        for i in range(len(allb)):
            for j in range(i + 1, len(allb)):
                if inter(allb[i]["rect"], allb[j]["rect"]): errs.append(f"map {nm}: {allb[i]['name']} overlaps {allb[j]['name']}")
    for w in M["world"]["sectors"]:
        if w["slug"] not in M["sectors"]: errs.append(f"map: sector {w['id']} has no sector map")
        elif not (V2 / M["sectors"][w["slug"]]["image"]).exists(): errs.append(f"map: {w['slug']} painting missing")
    for bld in blds:
        if not (V2 / "data" / f"{bld}.js").exists(): continue
        sl, b = map_home(M, bld, load_payload(bld))
        if not b: errs.append(f"map: {bld} has a layout but no rect on its sector map in content/v2/map.json")
        c = check_building(bld, errs, warns)
        print(f"{bld}: " + ", ".join(f"{k} {n}" for k, n in c.items()) + f" = {sum(c.values())} words")
    if a.browser:
        import asyncio
        asyncio.run(browser_checks(blds, a.base, Path(a.shots), errs, a.strict, M))
    if a.strict: errs += [f"(strict) {w}" for w in warns]; warns = []
    for w in warns: print("WARN", w)
    for e in errs: print("FAIL", e)
    print("PASS" if not errs else f"{len(errs)} problem(s)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
