---
name: memory-palace-builder
description: Design, populate, repaint or repair illustrated memory-palace buildings, rooms and zooms. Use for room art, word placement, hooks, navigation and related site data. Routes to planning and visual checks without loading the entire repo.
---
# Memory palace builder

Build one integrated 1280×720 painting per room or zoom: architecture, objects, people, interactions, lighting and shadows together. The site adds labels/hotspots; cards crop the final painting. Never generate separate word figures for assembly onto a background.

## Start with the smallest useful context

1. Reuse the checkout, fetch main once, check room ownership and preserve concurrent work.
2. Run `python3 tools/unbuilt.py --building <building_id>` and `python3 tools/room_context.py <building> --room <key> --compact`. It reads this checkout. A planned word is integrated only when a live copy is in that building (or a layout that claims the source room). A copy that is still only on the donor street does not make the room built; page planned words only as needed.
3. Use source assignments for new inventory and current v2 inventory/resolved hooks for repaints. Reconcile disagreements before moving words. Reuse approved style and user decisions; do not repeat setup questions.
4. Read only the relevant row and language references. `skills/limits.json` owns numeric limits; release-gates owns acceptance, this skill owns execution.

| Change | Read on demand |
|---|---|
| New building or changed floors/connections | `reference/building-walkthrough.md`, `reference/maps-and-navigation.md`, then the room row below |
| New room/zoom | `reference/planning.md`, `reference/composition.md`, `reference/prompt-template.md` |
| Repaint or move words | above plus `reference/moving-words.md` |
| Hook text | `reference/hooks.md`; language `reference/hooks.md` |
| Labels/hotspots | `reference/text-and-labels.md` |
| Map/navigation | `reference/maps-and-navigation.md`, `reference/site-ui.md` |
| New project, copyright, sensitive content | corresponding `reference/setup-and-style.md`, `reference/copyright.md`, `reference/sensitive-content.md` |
| Validation/release | `reference/validation.md`, `reference/tooling.md`; release-gates skill |

## Plan → compose → review → integrate

1. **One task brief.** Record base commit, target inventory, resolved hooks/verb markers, actual reference images, dependencies and the intended change. Use `reference/tooling.md` to choose an available build, browser and publishing route once. Fetch only the needed inputs.
2. **Resolve the entire repair before painting.** Follow `reference/planning.md`; include inherited defects that block this room, parent/zoom disagreements and complete figure/helper envelopes. Compute all pairwise and passage/control intersections, side bands and label space. If the groups cannot fit, simplify poses or recompose now. A legacy hotspot or valid manifest is not proof of painted clearance.
3. **Composition checkpoint.** For a new/recomposed scene, inspect one rough integrated draft or use the first candidate as the draft (`reference/composition.md`). Check the shared activity, depth, every group, passages and parent/zoom agreement before paying for detail. A genuinely local repair may reuse a verified composition.
4. **Focused generation.** Compile the manifest with `python3 tools/build_prompt.py <manifest> --layout <layout> --write --output /tmp/room-prompt.txt`. Use the whole-scene specification for composition; local edits use a short delta from that specification: target appearance, one related repair, visible landmarks, invariants and references. Save the exact submitted delta beside the manifest; do not send stale full-scene instructions that contradict it. Never assemble standalone figures.
5. **Cheap screen, then final review.** Inspect each result immediately and reject obvious scene/placement/anatomy regressions. Measure actual full groups and run geometry before building the final review pack. Once it passes, make one contact sheet and parent/zoom comparison; obtain independent finished-art review under `reference/validation.md` and release-gates. Never fit dishonest boxes to rescue failed art.
6. **Integrate once.** Rebuild accepted art, cards and data together. Update hooks, alt text, dialogue, navigation and cache version as needed. Run targeted checks during iteration; run existing global CI/release checks once on the combined change. Repeat checks only for changed inputs or unresolved failures. Publish through the working route using existing user authorization; report what actually passed.

For changed buildings/floors, use `reference/building-walkthrough.md`; overview/sectors use `reference/maps-and-navigation.md`. Pilot one room and its zoom together before expanding the batch.

## Token and retry budget

Default to one composition candidate and one focused repair, not a succession of detail edits. After two failed finished-image edits of the same interaction/composition, write one diagnosis and revise its pose, space allocation or parent/zoom contract before generating again. Do not reset this rule by naming each hand, animal or position a separate defect. Continue the authorized task with the revised plan; never lower acceptance criteria to meet a call budget.

Keep one manifest and a short checkpoint: base, changed paths, accepted revision, failures, next action. Load references on demand; process payloads and tool responses programmatically and print only findings/counts. Reuse unchanged evidence and the same review context. Fold lessons into the canonical rule rather than adding case histories.
