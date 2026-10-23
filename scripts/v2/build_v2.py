#!/usr/bin/env python3
"""Build the v2 village (village/v2/) from the SAME text metadata as v1.

Card text (French word, article, gloss, IPA, respelling, memory hook, example, plural,
notes, verb tables) is read, never rewritten, from:
  1. the live v1 payloads village/assets/data/<building>.js (items matched by id), else
  2. data/source/vocab.jsonl (+ data/source/rooms.json for planned room membership).
A layout entry may set "text": "vocab" to use data/source/vocab.jsonl instead of the v1 payload
(e.g. v1's « le banc » hook is a piggy bank; the source hook is a pew/bench).
v2-specific inputs live in content/v2/<building>/:
  layout.json  painting, hotspot box (1280x720 px), optional "labelAt" [cx, top] px,
               doors, map exit and zooms. Labels are otherwise placed automatically.
  hooks.json   optional {word_id: {"hook": ..., "why": ...}} overrides, used ONLY where the
               v1 hook breaks the content rules or cannot be painted; the painting must show
               the override hook. v1 data is never edited.
               An entry may also (or only) carry "art" and/or "g" to correct the article or
               gender on labels and cards, e.g. {"fr_hammam_noun": {"art": "le"}} (aspirate h)
               or {"fr_container_noun": {"art": "le", "g": "m"}}; a "g" change also moves the
               word's side (f left, m right) and its indefinite article.
  content/v2/vocab_fixes.json  the same art/g corrections for every building (known vocab.jsonl
               errors), so a building package picks them up without editing shared files;
               a building's own hooks.json entry wins.
               An entry may also carry "ex": [french, english] to replace an example sentence that
               breaks the content rules (e.g. a smoking/tobacco example), with a "why".
  layout.json may also carry top-level "building_id" (memory-palace id, e.g. B29_plage),
  "sector_id" (e.g. S09_nature) and "v1_room_id"; they are copied to data/<building>.js and
  the map uses them to put the building on its sector map (see village/v2/README.md).
  Verbs (vocab pos "verb") become v1-style verb cards (beret colour, participles, 7 tenses) from
  data/cache/conjugations.json. vocab "reflexive" only means a pronominal form exists, so the card
  uses it (se trouver, mirror, être) only when the example sentence does; a hooks.json entry
  {"reflexive": true|false} forces it either way.
  Adjectives (vocab pos "adj") get no article, sit in the centre band and show their m/f forms.
  Adverbs (vocab pos "adv") get no article and no gender either, sit in the centre band too
  (genderless words live in the middle) and their card says "adverb · invariable".
Everything is checked by scripts/qa/check_v2.py.

usage: python3 scripts/v2/build_v2.py [building ...]   (default: every content/v2/*/layout.json)
"""
import json, re, sys
from pathlib import Path
from PIL import Image, ImageFont

ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "village" / "v2"
W, H = 1280, 720
FONT = None
for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]:
    if Path(p).exists():
        FONT = ImageFont.truetype(p, 17)
LAB_H = 29
EDGE = 12  # px (1280-wide painting) kept clear between a label and the scene edge
GAP = 5  # px clearance a placed label tries to keep from other labels, hotspots and doors


def label_w(text):
    if FONT:
        return int(FONT.getlength(text)) + 22
    return int(len(text) * 9.5) + 22


def load_v1_items():
    items = {}
    for js in sorted((ROOT / "village" / "assets" / "data").glob("*.js")):
        src = js.read_text(encoding="utf-8")
        m = re.search(r"=\s*(\{.*\})\s*;?\s*$", src, re.S)
        if not m:
            continue
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        for room in (data.get("rooms") or {}).values():
            for it in room.get("items") or []:
                if it.get("id"):
                    items.setdefault(it["id"], it)
    return items


def load_vocab():
    out = {}
    with open(ROOT / "data" / "source" / "vocab.jsonl", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                w = json.loads(line)
                out[w["id"]] = w
    return out


def plural_of(w):
    if w.get("plural_irregular"):
        return w["plural_irregular"] if w["plural_irregular"].startswith("les ") else "les " + w["plural_irregular"]
    lem = w["lemma"]
    if " " in lem:  # compound: pluralise the head noun only
        head, rest = lem.split(" ", 1)
        return "les " + (head if head[-1] in "sxz" else head + "s") + " " + rest
    return "les " + (lem if lem[-1] in "sxz" else lem + "s")


def adj_from_vocab(w):
    """Adjective card: no article, centre band; the gram line shows the m/f forms (or 'same for both')."""
    f = w.get("forms") or {}
    hook = (w.get("mnemonic_hook") or {}).get("scene") or ""
    hook = hook[:1].upper() + hook[1:]
    it = {"id": w["id"], "adj": True, "fr": w["lemma"], "g": "adj",
          "en": w.get("gloss", ""), "ipa": w.get("ipa", ""), "say": w.get("respelling", ""),
          "forms": {k: f[k] for k in ("m_sg", "f_sg", "m_pl", "f_pl") if f.get(k)},
          "invariable": bool(w.get("invariable")) or (f.get("m_sg") and f.get("m_sg") == f.get("f_sg")),
          "hook": hook, "note": w.get("usage_warning"), "ex": [w.get("example_fr", ""), w.get("example_en", "")]}
    if w.get("f_ipa"): it["f_ipa"] = w["f_ipa"]
    if w.get("f_respelling"): it["f_say"] = w["f_respelling"]
    return it


# --- verbs from data/source/vocab.jsonl (verb streets) ------------------------------------
# A vocab verb (pos "verb") becomes a v1-style verb card: Monsieur Verbe's beret colour from
# verb_group/irregular (-er red, -ir green, regular -re purple, irregular gold), "reflexive"
# (he holds a mirror), participles + auxiliary, and the 7 tenses of v1 cards built from the
# conjugation cache data/cache/conjugations.json (filled by scripts/build_data.py / verbecc).
CONJ = None
TENSES = [("present", "Présent", "present"), ("pc", "Passé composé", "passe"),
          ("imparfait", "Imparfait", "imparfait"), ("futur", "Futur simple", "futur"),
          ("cond", "Conditionnel présent", "conditionnel"), ("subj", "Subjonctif présent", "subjonctif"),
          ("imper", "Impératif", "imperatif")]
PRON = re.compile(r"^(que |qu')?(je |j'|tu |il/elle |il |elle |nous |vous |ils/elles |ils |elles )")


def load_conj():
    global CONJ
    if CONJ is None:
        p = ROOT / "data" / "cache" / "conjugations.json"
        CONJ = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    return CONJ


def _clean_pronominal(form):  # same as scripts/build_data.py clean_pronominal: drop "(de)" etc.
    text = re.sub(r"\s+", " ", (form or "").replace("’", "'")).strip()
    while True:
        nxt = re.sub(r"\s*\([^)]*\)", "", text).strip()
        if nxt == text:
            return text
        text = nxt


def uses_pronominal(w, tables):
    """vocab "reflexive": true only says a pronominal form EXISTS (envoyer -> s'envoyer, trouver ->
    se trouver), while gloss and example are often the plain verb ("J'envoie une carte"). A card
    is reflexive only when its example sentence uses a form from the pronominal tables
    ("Il s'est blessé", "Calme-toi", "Hâtons-nous") or the pronominal infinitive ("de te déconnecter")."""
    ex = (w.get("example_fr") or "").replace("\u2019", "'").lower()
    forms = set()
    for k in ("present", "passe", "imparfait", "futur", "conditionnel", "subjonctif", "imperatif"):
        for cell in tables.get(k) or []:
            for part in cell.split(" / "):
                f = _split(part.strip())[1].strip()
                if f:
                    forms.add(f.lower())
    inf = _clean_pronominal(w.get("pronominal_form")).lower()
    bare = inf[3:] if inf.startswith("se ") else inf[2:] if inf.startswith("s'") else None
    if bare:
        elide = inf.startswith("s'")
        forms.update([inf] + [p + bare for p in (("m'", "t'") if elide else ("me ", "te ")) + ("nous ", "vous ")])
    return any(re.search(r"(?<![\w'-])" + re.escape(f) + r"(?!\w)", ex) for f in forms)


def verb_infinitive(w, tables=None):
    """Card infinitive. The pronominal form (se trouver) is used only when the vocab verb is
    reflexive AND the example sentence uses that form (see uses_pronominal); a hooks.json
    "reflexive": true/false entry overrides the test (applied in build())."""
    pf = w.get("pronominal_form")
    if w.get("reflexive") and pf:
        force = w.get("_reflexive")
        if force is True or (force is None and tables is not None and uses_pronominal(w, tables)):
            return _clean_pronominal(pf)
    return w["lemma"]


def _split(cell):
    m = PRON.match(cell)
    if not m:
        return None, cell
    return m.group(0), cell[m.end():]


def _merge_genders(cell):
    """'il est allé / elle est allée' -> ('il / elle', 'est allé / est allée'); 'je suis allé / je suis allée' -> ('je', 'suis allé(e)')."""
    parts = [p.strip() for p in cell.split(" / ")]
    split = [_split(p) for p in parts]
    prons = []
    for pr, _ in split:
        pr = (pr or "").strip()
        if pr not in prons:
            prons.append(pr)
    forms = [f for _, f in split]
    if len(forms) == 2 and forms[1] in (forms[0] + "e", forms[0][:-1] + "es") and len(prons) == 1:
        merged = forms[0] + "(e)" if forms[1] == forms[0] + "e" else forms[0][:-1] + "(e)s"
        return prons[0], merged
    if len(forms) == 2 and len(prons) == 2 and forms[1] in (forms[0] + "e", forms[0][:-1] + "es"):
        return " / ".join(prons), " / ".join(forms)
    return " / ".join(prons), " / ".join(dict.fromkeys(forms))


def _pron_label(pr):
    pr = pr.strip()
    pr = {"il/elle": "il / elle", "ils/elles": "ils / elles", "qu'il/elle": "qu'il / qu'elle",
          "qu'ils/elles": "qu'ils / qu'elles", "il / elle": "il / elle", "ils / elles": "ils / elles"}.get(pr, pr)
    return pr if pr.endswith("'") else pr


def verb_tenses(tables, reflexive):
    out = []
    for key, name, src in TENSES:
        cells = tables.get(src) or []
        rows = []
        if key == "imper":
            for pr, cell in zip(("(tu)", "(nous)", "(vous)"), cells):
                rows.append([pr, cell])
        else:
            for cell in cells:
                if " / " in cell:
                    pr, form = _merge_genders(cell)
                else:
                    pr, form = _split(cell)
                    pr = (pr or "").strip()
                pr = _pron_label(pr.replace("que j'", "que j'"))
                rows.append([pr, form])
        out.append({"key": key, "name": name, "rows": rows, "note": None})
    return out


def _regular_re(lemma, t):
    if not lemma.endswith("re") or lemma.endswith(("indre", "oudre", "aître", "ire")):
        return False
    st = lemma[:-2]
    want = [st + e for e in ("s", "s", "", "ons", "ez", "ent")]
    got = [_split(c)[1] for c in t.get("present") or []]
    return got == want and t.get("participe_passe") == st + "u"


def verb_from_vocab(w):
    pf = _clean_pronominal(w.get("pronominal_form")) if w.get("reflexive") and w.get("pronominal_form") else None
    tp = load_conj().get(pf) if pf else None
    inf = verb_infinitive(w, tp or {})
    t = load_conj().get(inf)
    if not t:
        raise SystemExit(f"no conjugation for {inf} ({w['id']}): add it to data/cache/conjugations.json")
    grp, irr = w.get("verb_group"), w.get("irregular")
    if grp == 1 and not irr:
        group, beret = "-er", "red"
    elif grp == 2 and not irr and w["lemma"].endswith("ir") and [_split(c)[1] for c in t.get("present") or [""] * 4][3:4] == [w["lemma"][:-1] + "ssons"]:
        group, beret = "-ir", "green"  # checked on the table: vocab marks some 3rd-group verbs (partir) as group 2
    elif grp == 3 and _regular_re(w["lemma"], t):
        group, beret = "-re", "purple"
    else:
        group, beret = "irregular", "gold"
    mh = w.get("mnemonic_hook") or {}
    hook = mh.get("scene") or ""
    hook = hook[:1].upper() + hook[1:]
    refl = inf != w["lemma"] and inf.startswith(("se ", "s'"))
    aux = "être" if refl else (w.get("auxiliary") or "avoir")
    col = {"red": "RED beret = regular -er verb", "green": "GREEN beret = regular -ir verb (nous …issons)",
           "purple": "PURPLE beret = regular -re verb", "gold": "GOLD beret = irregular: not every tense can be built from the infinitive"}[beret]
    bits = [col + "."]
    if refl:
        bits.append("Mirror = reflexive (se / s').")
    if aux == "être":
        pp, ppf = t.get("participe_passe", ""), t.get("participe_passe_f") or t.get("participe_passe", "") + "e"
        bits.append(f"Passé composé with ÊTRE: the participle agrees ({pp}, {ppf}, {pp}s, {ppf}s)." if pp and not pp.endswith(("e", "s")) else "Passé composé with ÊTRE: the participle agrees with the subject.")
    if w.get("prepositions"):
        bits.append(w["lemma"] + " + " + " / ".join(w["prepositions"]) + ".")
    if w.get("usage_warning"):
        bits.append(w["usage_warning"])
    it = {"id": w["id"], "fr": inf, "verb": True, "group": group, "beret": beret,
          "en": w.get("gloss", ""), "ipa": w.get("ipa", ""), "say": w.get("respelling", ""),
          "hook": hook, "sound": mh.get("sound_alike"), "strength": mh.get("strength"),
          "note": " ".join(bits), "ex": [w.get("example_fr", ""), w.get("example_en", "")],
          "parts": {"present": t.get("participe_present", ""), "past": t.get("participe_passe", ""), "aux": aux},
          "tenses": verb_tenses(t, refl)}
    if refl:
        it["reflexive"] = True
    return it


def adv_from_vocab(w):
    """Adverb card: no article, no gender (centre band); the gram line says 'adverb · invariable'."""
    hook = (w.get("mnemonic_hook") or {}).get("scene") or ""
    hook = hook[:1].upper() + hook[1:]
    it = {"id": w["id"], "adv": True, "fr": w["lemma"], "g": "adv",
          "en": w.get("gloss", ""), "ipa": w.get("ipa", ""), "say": w.get("respelling", ""),
          "hook": hook, "note": w.get("usage_warning"), "ex": [w.get("example_fr", ""), w.get("example_en", "")]}
    if w.get("false_cognate_note"):
        ff = w["false_cognate_note"]
        it["falseFriend"] = {"kind": "false" if w.get("cognate_type") == "false_cognate" else "partial",
                             "note": ff[:1].upper() + ff[1:] + ("" if ff.endswith(".") else ".")}
    return it


def item_from_vocab(w):
    if w.get("pos") == "adj":
        return adj_from_vocab(w)
    if w.get("pos") == "verb":
        return verb_from_vocab(w)
    if w.get("pos") == "adv":
        return adv_from_vocab(w)
    g = w.get("gender")
    art = w.get("article") or ("la" if g == "f" else "le")
    ind = {"f": "une", "m": "un", "mf": "un/une"}.get(g, "un")
    hook = (w.get("mnemonic_hook") or {}).get("scene") or ""
    hook = re.sub(r"^Reverent:\s*", "", hook)
    hook = hook[:1].upper() + hook[1:]
    note = w.get("gender_note") or w.get("usage_warning")
    it = {
        "id": w["id"], "fr": w["lemma"], "art": art, "ind": ind, "g": g,
        "en": w.get("gloss", ""), "ipa": w.get("ipa", ""), "say": w.get("respelling", ""),
        "plural": plural_of(w), "hook": hook, "note": note,
        "ex": [w.get("example_fr", ""), w.get("example_en", "")],
    }
    if w.get("false_cognate_note"):  # shown as a flag on the card; partial = shares a sense with English
        ff = w["false_cognate_note"]
        it["falseFriend"] = {"kind": "false" if w.get("cognate_type") == "false_cognate" else "partial",
                             "note": ff[:1].upper() + ff[1:] + ("" if ff.endswith(".") else ".")}
    return it


def headword(it):
    if it.get("verb") or it.get("adj") or it.get("adv"):
        return it["fr"]
    a = it.get("art")
    return ("l'" + it["fr"]) if a == "l'" else f"{a} {it['fr']}"


def apply_grammar_fix(it, fix):
    """Article/gender correction from hooks.json or vocab_fixes.json (nouns only)."""
    if it.get("verb") or it.get("adj") or it.get("adv"):
        return
    if fix.get("g"):
        assert fix["g"] in ("m", "f", "mf"), fix
        it["g"] = fix["g"]
        it["ind"] = {"f": "une", "m": "un", "mf": "un/une"}[fix["g"]]
    if fix.get("art"):
        assert fix["art"] in ("le", "la", "l'", "les"), fix
        it["art"] = fix["art"]


def side_of(it):
    return {"f": "L", "m": "R"}.get(it.get("g"), "C")


def inter(a, b, pad=0):
    return a[0] < b[0] + b[2] + pad and b[0] < a[0] + a[2] + pad and a[1] < b[1] + b[3] + pad and b[1] < a[1] + a[3] + pad


def ov_area(a, b):
    x = max(0, min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]))
    y = max(0, min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]))
    return x * y


def badge_rect(z):
    w = label_w("🔍 " + z["label"]) + 6
    return [z["at"][0] - w / 2, z["at"][1] - 17, w, 34]


def nameplate_rect(room):
    if not room.get("nameplate"):
        return None
    w = int(FONT.getlength(room["name"]) * 24 / 17) + 56 if FONT else len(room["name"]) * 14 + 56
    cx, cy = room["nameplate"][0] * W / 100, room["nameplate"][1] * H / 100
    return [cx - w / 2, cy - 22, w, 44]


def place_labels(room):
    """Choose a label rectangle for each item: below, above, inside-bottom or inside-top of its box,
    avoiding other labels, other hotspots, doors, the map exit, zoom badges and the nameplate."""
    fixed = []
    for d in room.get("doors", []):
        fixed.append(d["hit"])
    if room.get("mapExit"):
        fixed.append(room["mapExit"]["box"])
    for z in room.get("zooms", []):
        fixed.append(badge_rect(z))
    np_ = nameplate_rect(room)
    if np_:
        fixed.append(np_)
    placed = []
    boxes = [it["box"] for it in room["items"]]
    for i, it in enumerate(room["items"]):
        x, y, w, h = it["box"]
        lw = label_w(it["_hw"])
        if it.get("_labelAt"):
            # manual placement from layout.json: "labelAt": [centre_x_px, top_px]
            c, t = it["_labelAt"]
            best = [c - lw / 2, t, lw, LAB_H]
            placed.append(best)
            it["_lab"] = best
            continue
        cx = x + w / 2
        cands = []
        for top in (y + h + 4, y - LAB_H - 4, y + h - LAB_H - 4, y + 4, y + h / 2 - LAB_H / 2):
            for dx in (0, -0.3, 0.3):
                # keep a clear margin from the scene edge (check_v2 --strict wants >= 8 screen px)
                c = min(max(cx + dx * w, lw / 2 + EDGE), W - lw / 2 - EDGE)
                t = min(max(top, EDGE), H - LAB_H - EDGE)
                cands.append([c - lw / 2, t, lw, LAB_H])
        best, bestscore = None, None
        for r0 in cands:
            # primary score: real overlaps; secondary: overlaps of the label grown by GAP, so that among
            # equally clear spots we prefer one that does not merely touch a neighbour (strict QA: 3 px)
            rg = [r0[0] - GAP, r0[1] - GAP, r0[2] + 2 * GAP, r0[3] + 2 * GAP]
            score = [0, 0]
            for k, r in enumerate((r0, rg)):
                for p in placed:
                    score[k] += 1000 * ov_area(r, p)
                for f in fixed:
                    score[k] += 1000 * ov_area(r, f)
                for jj, b in enumerate(boxes):
                    if jj != i:
                        score[k] += ov_area(r, b)
            if bestscore is None or score < bestscore:
                best, bestscore = r0, score
            if score == [0, 0]:
                break
        placed.append(best)
        it["_lab"] = best
    return placed


def card_crop(img, box, out):
    x, y, w, h = box
    s = max(w, h) * 1.18
    cx, cy = x + w / 2, y + h / 2
    l, t = max(0, cx - s / 2), max(0, cy - s / 2)
    r, b = min(W, l + s), min(H, t + s)
    l, t = max(0, r - s), max(0, b - s)
    c = img.crop((int(l), int(t), int(r), int(b)))
    c.thumbnail((420, 420), Image.LANCZOS)
    out.parent.mkdir(parents=True, exist_ok=True)
    c.save(out, "WEBP", quality=84)


def build(bld, v1, vocab):
    L = json.loads((ROOT / "content" / "v2" / bld / "layout.json").read_text(encoding="utf-8"))
    # v2 hook overrides (content/v2/<bld>/hooks.json): {word_id: {"hook": ..., "why": ...}}
    # used where the v1 hook breaks the content rules or does not match the painting; v1 data is never edited.
    hp = ROOT / "content" / "v2" / bld / "hooks.json"
    overrides = json.loads(hp.read_text(encoding="utf-8")) if hp.exists() else {}
    overrides = {k: v for k, v in overrides.items() if not k.startswith("_")}
    fp = ROOT / "content" / "v2" / "vocab_fixes.json"
    fixes = json.loads(fp.read_text(encoding="utf-8")) if fp.exists() else {}
    fixes = {k: v for k, v in fixes.items() if not k.startswith("_")}
    out_rooms = {}
    for key, room in L["rooms"].items():
        img = Image.open(V2 / room["image"]).convert("RGB")
        assert img.size == (W, H), (bld, key, img.size)
        items = []
        for spec in room["items"]:
            wid = spec["id"]
            if wid in v1 and spec.get("text") != "vocab":
                it = {k: v for k, v in v1[wid].items() if k not in ("img", "box", "label", "side", "surface", "cardSrc")}
            elif wid in vocab:
                w = vocab[wid]
                if "reflexive" in overrides.get(wid, {}):  # force a verb card reflexive or plain
                    w = dict(w, _reflexive=bool(overrides[wid]["reflexive"]))
                it = item_from_vocab(w)
            else:
                raise SystemExit(f"{bld}/{key}: unknown word id {wid}")
            fix = dict(fixes.get(wid, {}))
            fix.update({k: v for k, v in overrides.get(wid, {}).items() if k in ("art", "g")})
            apply_grammar_fix(it, fix)
            it["_hw"] = headword(it)
            it["box"] = spec["box"]
            if overrides.get(wid, {}).get("hook"):
                it["hook"] = overrides[wid]["hook"]
            if overrides.get(wid, {}).get("ex"):
                it["ex"] = list(overrides[wid]["ex"])
            if spec.get("labelAt"):
                it["_labelAt"] = spec["labelAt"]
            if spec.get("scene"):
                it["scene"] = spec["scene"]
            items.append(it)
        room = dict(room, items=items)
        place_labels(room)
        out_items = []
        for it in items:
            x, y, w, h = it["box"]
            r = it["_lab"]
            card = f"{bld}/cards/{it['id']}.webp"
            card_crop(img, it["box"], V2 / card)
            o = {k: v for k, v in it.items() if not k.startswith("_")}
            o.update({
                "box": [round(x / 12.8, 4), round(y / 7.2, 4), round(w / 12.8, 4), round(h / 7.2, 4)],
                "label": [round((r[0] + r[2] / 2) / 12.8, 4), round(r[1] / 7.2, 4)],
                "labelPx": [round(v, 1) for v in r],
                "boxPx": it["box"], "side": side_of(it), "cardSrc": card,
            })
            out_items.append(o)
        r2 = {k: v for k, v in room.items() if k != "items"}
        r2["items"] = out_items
        for d in r2.get("doors", []):
            d.setdefault("thumb", L["rooms"][d["to"]]["image"])
        r2.setdefault("parent", None)
        if r2.get("mapExit"):
            b = r2["mapExit"]["box"]
            r2["mapExit"] = dict(r2["mapExit"], boxPx=b, box=[round(b[0] / 12.8, 4), round(b[1] / 7.2, 4), round(b[2] / 12.8, 4), round(b[3] / 7.2, 4)])
        out_rooms[key] = r2
    payload = {"building": bld, "name": L["name"], "main": L["main"], "roomList": L["roomList"], "rooms": out_rooms}
    # memory-palace registry fields: the map places the building on its sector map by these
    for k in ("building_id", "sector_id", "v1_room_id"):
        if L.get(k):
            payload[k] = L[k]
    js = "(window.VILLAGE_DATA=window.VILLAGE_DATA||{})[" + json.dumps(bld) + "]=" + json.dumps(payload, ensure_ascii=False) + ";\n"
    (V2 / "data").mkdir(parents=True, exist_ok=True)
    (V2 / "data" / f"{bld}.js").write_text(js, encoding="utf-8")
    n = sum(len(r["items"]) for r in out_rooms.values())
    print(f"built {bld}: {len(out_rooms)} rooms, {n} words")


def main():
    blds = sys.argv[1:] or sorted(p.parent.name for p in (ROOT / "content" / "v2").glob("*/layout.json"))
    v1, vocab = load_v1_items(), load_vocab()
    for b in blds:
        build(b, v1, vocab)
    unused = []
    for b in blds:
        hp = ROOT / "content" / "v2" / b / "hooks.json"
        if hp.exists():
            ids = {i["id"] for r in json.loads((ROOT / "content" / "v2" / b / "layout.json").read_text(encoding="utf-8"))["rooms"].values() for i in r["items"]}
            unused += [f"{b}:{k}" for k in json.loads(hp.read_text(encoding="utf-8")) if not k.startswith("_") and k not in ids]
    if unused:
        raise SystemExit("hooks.json ids not in layout: " + ", ".join(unused))


if __name__ == "__main__":
    main()
