#!/usr/bin/env python3
"""Compile a validated room/zoom manifest into the canonical painting prompt.

python tools/build_prompt.py manifest.json --write --output /tmp/room-prompt.txt
python tools/build_prompt.py manifest.json --check

Invalid input never writes output or prompt_text. --write prints only a summary;
without --write/--output print the prompt. prompt_extra maps known section names
into additional room-specific instructions. Empty siblings/motifs lists are valid.
"""
import argparse, json, re, sys
from plan_check import validate_plan
from walkthrough import read_json, room_brief, validate as validate_walkthrough
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TPL = ROOT / "skills" / "memory-palace-builder" / "reference" / "prompt-template.md"
LIMITS = json.loads((ROOT / "skills" / "limits.json").read_text(encoding="utf-8"))
W, H = 1280, 720
BERET = {"er": "red -er", "ir": "green -ir", "re": "purple -re", "irr": "gold irregular", "irregular": "gold irregular"}


def template():
    s = TPL.read_text(encoding="utf-8")
    return s.split("```text", 1)[1].split("```", 1)[0].strip("\n")


def build(M, layout=None):
    P = M.get("prompt") or {}
    kind = P.get("kind", "room")
    items = M.get("items", [])
    missing = []

    def v(key, label=None):
        x = P.get(key)
        if x in (None, "", []):
            missing.append(label or key)
            return "{" + (label or key) + "}"
        return ", ".join(x) if isinstance(x, list) else str(x)

    def item_line(n, it):
        f = lambda k: it.get(k) if it.get(k) not in (None, "") else (missing.append(f"{it.get('id')}.{k}") or "{" + k + "}")
        cnt = it.get("count")
        where = ", ".join(x for x in (it.get("side"), it.get("zone"), it.get("depth")) if x) or f("zone")
        s = (f"{n}. {f('word')} = {f('gloss')}: chosen hook {f('hook')}; literal cue {f('hook_object')}; shown as {f('shown')}; "
             f"pose/action {f('pose_action')}; count {cnt if cnt not in (None, '') else '-'}; at {where}; "
             f"interacts with {f('interacts_with')}; planned pixel envelope {it.get('box_hint')}")
        if it.get("pos") == "verb":
            s += f"; beret {BERET.get(it.get('beret'), 'INVALID')}; where it acts: {f('verb_acts_on')}"
        return s + "."

    out = []
    for line in template().splitlines():
        if line.startswith("DOORS AND EXITS:") and kind == "zoom" and not M.get("doors"):
            line = f"DOORS AND EXITS: no painted passage in this close-up. Existing viewer Back returns to {P.get('parent')}. Do not invent a door, portal or painted back arrow. Preserve the parent's surrounding surfaces."
        if line.startswith("[zoom only]"):
            if kind != "zoom": continue
            line = line[len("[zoom only] "):]
            c = M.get("continuity", {})
            line += f" Parent reference {c.get('parent_image')}, pixel crop {c.get('parent_box')}; preserve: " + "; ".join(c.get("preserve", [])) + "."
        if line.startswith("[repaint only]"):
            if not M.get("repaint_rows"): continue
            line = line[len("[repaint only] "):]
        if line.startswith("{n}. "):
            if kind == "hub" and not items:
                out.append("Circulation only. Keep the routes, thresholds and arrival landmarks legible; no vocabulary figures.")
            else:
                out += [item_line(i + 1, it) for i, it in enumerate(items)]
            continue
        if line.startswith("(repeat per item"):
            continue
        if line.startswith("Verbs:"):
            verbs = [it for it in items if it.get("pos") == "verb"]
            if not verbs: continue
            berets = sorted({BERET.get(str(it.get("beret", "")).lower(), "") for it in verbs} - {""})
            line = line.replace("{red -er | green -ir | purple -re | gold irregular}", " or ".join(berets) or "{beret}")
            if not berets: missing.append("items.beret (er, ir, re or irregular) on each verb")
            line = line.replace("{noun}", "what its line above names")
        out.append(line)
    t = "\n".join(out)

    groups = M.get("interactions") or []
    gtxt = "; ".join(f"{', '.join(g.get('who', []))}: {g.get('doing', '')}" for g in groups) or ("circulation through the visible passages" if kind == "hub" and not items else (missing.append("interactions") or "{interactions}"))
    doors = M.get("doors") or []
    dtxt = "; ".join(f"to {d.get('to')}, {d.get('where')}, painted as {d.get('painted_as')}" for d in doors) or "none"
    texts = M.get("text_in_image") or []
    ttxt = "; ".join(f"\"{x.get('text')}\" on {x.get('where')}" for x in texts) or "none"
    counts = [f"{it.get('word')}: {it.get('count')}" for it in items if isinstance(it.get("count"), int)]
    plaques = [it.get("word") for it in items if str(it.get("sensitive", "")).lower().startswith("plaque")]
    band = LIMITS["centre_band"]
    sub = {
        "{room | zoom}": "zoom" if kind == "zoom" else "room",
        "{camera: eye-level three-quarter from ...}": v("camera"),
        "{building}": M.get("building") or v("building"),
        "{room name}": v("room_name", "room name"),
        "{parent room}": v("parent", "parent room") if kind == "zoom" else "",
        "{object/spot}": v("spot", "object/spot") if kind == "zoom" else "",
        "{rows}": "; ".join(M.get("repaint_rows") or []),
        "{direction}": v("light_from", "direction"),
        "{3: respectful, slightly realistic painterly with cartoony elements}": P.get("style_slider") or "3: respectful, slightly realistic painterly with cartoony elements",
        "{refs}": v("refs"),
        "{building's exterior | sector}": P.get("look") or "building's exterior",
        "{walls, floor, roof, wood/stone, palette}": v("materials"),
        "{time of day / light / dominant color}": v("set_apart", "time of day / light / dominant color"),
        "{place}": v("place"),
        "{landmark}": v("landmark"),
        "{playful architectural feature}": v("whimsy", "playful architectural feature"),
        "{named situation, e.g. feeding time in the school farmyard}": M.get("scene_situation") or (missing.append("scene_situation") or "{scene_situation}"),
        "{group 1: who, doing what with whom}; {group 2: ...}; {group 3: ...}": gtxt,
        "{sibling rooms and how they look}": "; ".join(M.get("siblings") or []) or "none yet",
        "{item_count}": str(len(items)),
        "{alphabet, number list, article table | none}": P.get("reference_board") or "none",
        "{count list}": ", ".join(counts) or "none",
        "{list or \"none\"}": ", ".join(plaques) or "none",
        "{door 1: to X, where, painted as a door that looks like X with a glimpse of it}; {door 2 / map exit: ...}": dtxt,
        "{what lies beyond, per the plan}": P.get("beyond") or (", ".join(f"{d.get('to')}" for d in doors) or "none"),
        "{text_in_image list, e.g. \"CANTINE\" on the sign over the counter | none}": ttxt,
        "{where}": P.get("sign_plates") or "none",
        "{used motifs, e.g. the duck, the red toy car}": ", ".join(M.get("used_motifs") or []) or "none so far",
        "{how this room's camera, layout, focal action and light differ}": v("differ", "how this room differs from its siblings"),
        "{unless hook}": "unless the animal is itself the hook",
        "central 30-70% band": f"central {band[0]:.0%}-{band[1]:.0%} band",
        "Leave 8 px of clearance for each label from the scene edge":
            f"Leave {LIMITS['label_edge_px']} px of clearance for each label from the scene edge",
        "about 110 px between": f"about {LIMITS['label_gap_px']} px between",
    }
    for a, b in sub.items():
        t = t.replace(a, b)
    for sec, extra in (M.get("prompt_extra") or {}).items():
        t = re.sub(rf"(^{re.escape(sec)}:.*?)(?=\n\n|\Z)", lambda m: m.group(1) + " " + extra, t, count=1, flags=re.S | re.M)
    plan_path = ROOT / "content" / "v2" / M["building"] / "walkthrough.json"
    if plan_path.is_file():
        if layout is None:
            layout = read_json(plan_path.with_name("layout.json"))
        plan = read_json(plan_path)
        model = validate_walkthrough(plan, layout, read_json(ROOT / "content/v2/map.json"))
        brief = room_brief(M["room"], plan, layout, model)
        cues = []
        if "zoom_parent_image" not in brief:
            for passage in brief["passages"]:
                here, there = passage["here"], passage["there"]
                direction = passage.get("direction")
                travel = "one-way arrival" if direction and direction[1] == M["room"] else "painted passage"
                cues.append(f"{passage['id']} ({travel}): {passage['appearance']}. Here: {here['where']}. "
                            f"Other side: {there['where']}, arriving at {there['arrival']}. "
                            f"Match reference {passage['neighbor_image']}.")
            entrance = brief.get("sector_entrance")
            if entrance:
                cues.append(f"Sector threshold: {entrance['appearance']}. Arrival: {entrance['arrival']}.")
        if cues:
            t = re.sub(r"(^DOORS AND EXITS:.*?)(?=\n\n|\Z)",
                       lambda match: match.group(1) + " Shared plan: " + " ".join(cues), t, count=1, flags=re.S | re.M)
    left = sorted(set(re.findall(r"\{[^{}\n]+\}", t)))
    return t, sorted(set(missing)), left


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--layout", help="validate a matching draft layout with the manifest before compiling")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", help="write the prompt to a file instead of stdout")
    a = ap.parse_args()
    p = Path(a.manifest)
    M = json.loads(p.read_text(encoding="utf-8"))
    try:
        layout_path = Path(a.layout) if a.layout else ROOT / "content" / "v2" / M["building"] / "layout.json"
        layout = read_json(layout_path) if a.layout or layout_path.with_name("walkthrough.json").is_file() else None
        fail, warn = validate_plan(M, layout)
        if not fail:
            t, missing, left = build(M, layout)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        print(f"FAIL {error}", file=sys.stderr)
        return 1
    for message in warn:
        print("WARN " + message, file=sys.stderr)
    if fail:
        for message in fail:
            print("FAIL " + message, file=sys.stderr)
        return 1
    if missing or left:
        print("unfilled: " + ", ".join(missing + left), file=sys.stderr)
        return 1
    if a.check:
        same = M.get("prompt_text") == t
        print("prompt_text matches the manifest" if same else "prompt_text is stale: run with --write")
        return 0 if same else 1
    if a.write:
        M["prompt_text"] = t
        p.write_text(json.dumps(M, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Stored prompt_text ({len(t)} characters); manifest valid")
    if a.output:
        Path(a.output).write_text(t + "\n", encoding="utf-8")
        print(f"Wrote prompt: {a.output}")
    elif not a.write:
        print(t)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
