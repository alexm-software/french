# Planning before image generation

## Resolve the building once

Use `tools/unbuilt.py --repo .` and `tools/room_context.py` in the existing checkout. Check ownership/claims before choosing a room. For new spaces, source assignments choose the inventory; live IDs may already be elsewhere, so reconcile before adding. For a repaint, current v2 layout and resolved hook overrides define the existing room. If older source rooms disagree, record that discrepancy rather than restoring stale inventory or silently moving live words. An authorized move updates both sources and live layout. Read only the target rows of `data/source/vocab.jsonl`, `data/source/rooms.json` and the relevant `content/v2/<bld>/hooks.json`/overrides. Never add easy-to-draw filler or silently move a word.

Write the building plan in its existing layout: main entrance, sector/village link, rooms, actual neighboring doors, stairs, zoom parents and ways out. A small floor-plan sketch may help; do not invent a floor-plan image if a graph suffices. Ground-floor doors go outside; interiors fit the exterior; outdoor connections are paths/gates/bridges, not freestanding doors. Back/Hub behavior is in `site-ui.md`.

Read `skills/limits.json` for density and spacing. Target its room count; split overloaded plans before painting. Zooms hold a real cluster within their parent, normally zoom_min–zoom_max words; fold sparse zooms into the parent. Alphabet/reference boards are one coherent board, not one picture per symbol. Moving live words must also satisfy `moving-words.md`.

## One manifest per room, complete before paint

Copy `tools/manifest_template.json` as a schema/example, then replace ALL example facts. Its two items demonstrate syntax, not recommended room density or production hooks. Resolve each ID's exact sense, pronunciation and final hook from current data. Never invent IPA or accept a strained pun to fill a field: a clear plain depiction is allowed. Preserve user-chosen hooks.

Record: setting/theme fit; one named everyday situation; interaction groups (IDs or explicit `background:` roles); word/gloss/hook; literal sound-cue object AND meaning; visible action; count or null; gender/side, zone/depth; sensitive treatment; verb beret and action target. Each candidate `box_hint` is [x,y,width,height] in **1280×720 pixels**, declared by `coordinate_space`. These are composition envelopes; final boxes must fit the art. They must not overlap. Leave space for labels and exits. Every item belongs to an activity, not a lineup.

Also record every painted passage/exit with destination, location and design (doors=[] is valid for a doorless zoom; its existing viewer Back supplies return, never invent a portal to fill metadata); outgoing zooms with word IDs; intended natural scene text; siblings and used motifs ([] is valid for a new building). Read full sibling hooks only to resolve a suspected repeated motif, not entire card payloads.

For a zoom add `continuity`: `parent_image` (actual path), `parent_box` (pixel rectangle), `preserve` (a nonempty list of descriptions covering identity, orientation, materials/colors, relative contents, surroundings and placement conventions). Set prompt.kind=zoom and prompt.parent/spot. Attach the full parent AND its crop. New detail can explain an object; it must not replace its shape, facing, contents or gender side. If more space is needed, redesign the parent/zoom pair before painting.

## Cheap stop before expensive generation

```sh
python3 tools/plan_check.py --manifest /tmp/room-manifest.json
python3 tools/plan_check.py --layout content/v2/<bld>/layout.json --room <key>
python3 tools/build_prompt.py /tmp/room-manifest.json --write --output /tmp/room-prompt.txt
python3 tools/build_prompt.py /tmp/room-manifest.json --check
```

Run the layout command when the draft exists; do not fabricate a live payload to use the tools. The manifest checker catches missing/duplicate fields, unknown interaction IDs, invalid counts/markers, box units/overlap/sides and missing zoom contracts. The layout checker catches broken targets, zoom backlinks and unreachable rooms. Neither proves phonetics, architectural plausibility or visual composition. Review those once before generation.

Attach the actual approved exterior/style reference, a visually distinct sibling if useful, and any parent crop. Compile instead of manually retyping the template. Pilot one room and its zoom before batch work; independent visual review must confirm the devices and scene work. Continue autonomously within the user's existing authorization; ask only for genuinely missing decisions.
