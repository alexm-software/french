# Planning before image generation

## Resolve the building once

Use `tools/unbuilt.py --repo .` and `tools/room_context.py` in the existing checkout. Check ownership/claims before choosing a room. For new spaces, source assignments choose the inventory; live IDs may already be elsewhere, so reconcile before adding. For a repaint, current v2 layout and resolved hook overrides define the existing room. If older source rooms disagree, record that discrepancy rather than restoring stale inventory or silently moving live words. An authorized move updates both sources and live layout. Read only the target rows of `data/source/vocab.jsonl`, `data/source/rooms.json` and the relevant `content/v2/<bld>/hooks.json`/overrides. Never add easy-to-draw filler or silently move a word.

For a new building or changed adjacency, complete `building-walkthrough.md` before painting: group the word rooms, draw per-floor blocks and actual connections, choose entrance/local hubs where useful, and walk all branches on paper. Record shared passage designs for both endpoint prompts. Reuse this one building plan for each room; do not invent architecture independently in separate prompts. Existing local repairs reuse accepted topology. Map levels follow `maps-and-navigation.md`; controls follow `site-ui.md`.

Read `skills/limits.json` for density and spacing. Target its room count; split overloaded plans before painting. Zooms hold a real cluster within their parent, normally zoom_min–zoom_max words; fold sparse zooms into the parent. Alphabet/reference boards are one coherent board, not one picture per symbol. Moving live words must also satisfy `moving-words.md`.

## Verify facts before composition

Build a compact per-room list from current data: exact IDs/senses, chosen hooks, pronunciation, gender/side, verb group/beret, reflexive mirror and any required counts. Use the same precedence as `scripts/v2/build_v2.py`: its v1/vocab selection, global corrections and building overrides. Record source paths and unresolved discrepancies once; preserve user decisions. Do not infer a verb's marker from spelling or copy an older hook just because it is nearby.

Use scripts to parse/filter/join the lists; return only the target inventory and findings to the model. Check unknown/duplicate IDs, missing or extra assigned words, existing live locations, room/building references and conflicting metadata. Explicitly account for intentional repeats or moves. Then review sense fit, sound cues and literal paintability; structural validity cannot establish those.

The current tools are partial: `unbuilt.py` reports live coverage; `room_context.py` summarizes current data; `plan_check.py` checks internal manifest/layout structure. It does NOT cross-check word metadata against the canonical sources. Until a shared resolver/preflight exists, do that comparison explicitly and record it as manual, never claim it was automated. A valid beret code can still be wrong for its word.

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

Before finished detail, follow the composition checkpoint in `composition.md`. Attach the approved exterior/style reference, a visually distinct sibling if useful, and any parent crop. Compile instead of manually retyping the template. Pilot one room and its zoom together before batch work; independent visual review must confirm the devices and scene work. Continue autonomously within the user's existing authorization; ask only for genuinely missing decisions.
