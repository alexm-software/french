---
name: memory-palace-builder
description: Design, populate, repaint or repair illustrated memory-palace buildings, rooms and zooms. Use for room art, word placement, hooks, navigation and related site data. Routes to planning and visual checks without loading the entire repo.
---
# Memory palace builder

Build one integrated 1280×720 painting per room or zoom: architecture, objects, people, interactions, lighting and shadows together. The site adds labels/hotspots; cards crop the final painting. Never generate separate word figures for assembly onto a background.

## Start with the smallest useful context

1. Read current task/user decisions and check the working tree and room ownership. Reuse the existing checkout; fetch main once, preserve concurrent work. Do not clone again per tool or room.
2. Run `python3 tools/unbuilt.py --repo . --building <building_id>` before selecting inventory, and `python3 tools/room_context.py <building> --room <key>`. The latter prints target hooks/IPA and compact siblings; page planned words with `--offset`/`--limit`. Word IDs across the whole village establish whether something is live.
3. Use source assignments for new inventory; for a repaint preserve current v2 room inventory and resolved hooks. Reconcile stale source/live differences before moving anything. Reuse the approved building look. Do not invent a new style or repeat setup questions for this French village. User decisions override older notes. The limits source is `skills/limits.json`; do not duplicate numeric limits in plans.
4. Read only the row needed below, plus the language skill for French work. Release-gates owns acceptance rules; this skill owns the workflow.

| Change | Read on demand |
|---|---|
| New building or changed floors/connections | `reference/building-walkthrough.md`, `reference/maps-and-navigation.md`, then the room row below |
| New room/zoom | `reference/planning.md`, `reference/composition.md`, `reference/prompt-template.md` |
| Repaint or move words | above plus `reference/moving-words.md` |
| Hook text | `reference/hooks.md`; language `reference/hooks.md` |
| Labels/hotspots | `reference/text-and-labels.md` |
| Map/navigation | `reference/maps-and-navigation.md`, `reference/site-ui.md` |
| New project, copyright, sensitive content | corresponding `reference/setup-and-style.md`, `reference/copyright.md`, `reference/sensitive-content.md` |
| Validation/release | `reference/validation.md`; release-gates skill |

## Verify facts → review composition → paint → integrate

Start with `reference/building-walkthrough.md` for a new building: room word groups → footprint/floors → physical passages and optional hubs → view compositions. Overview and sectors follow `reference/maps-and-navigation.md`. Follow `reference/planning.md` for each word room's manifest using `tools/manifest_template.json`. Resolve the words, hooks, exact counts, verb markers, interaction groups, candidate boxes and all destinations. For a zoom, pin the actual parent image/crop and the features it must preserve.

Check the manifest against the actual resolved word data, not just its own fields (`reference/planning.md`). Run `python3 tools/plan_check.py --manifest <manifest>` and the draft layout check. For a new or substantially recomposed scene, review a rough whole-scene composition before requesting finished detail (`reference/composition.md`). A valid list or box diagram does not establish visual quality.

Compile each draft/final request with `python3 tools/build_prompt.py <manifest> --write --output /tmp/room-prompt.txt`; record draft intent in `prompt_extra` and attach actual references. Fix FAILs first; warnings require judgment. Pilot one room and its zoom together, then review each finished painting immediately, scene first and details second (`reference/validation.md`). Do not batch unreviewed paintings or build cards/labels around rejected art.

Fit boxes to the finished hooks; do not move boxes away from art to satisfy a checker. Rebuild data/cards with the repo's existing tools. Keep hooks, dialogue, alt text, cards and zoom miniatures consistent with the final painting. Release only after the gates appropriate to the changed files pass.

## Token and retry budget

Keep one compact manifest and a short checkpoint (base commit, completed steps, changed paths, next action, blockers). Save tool output/review evidence in files; report counts and failures, not full payloads or repeated prompts. Do not read bundled JS, conjugation tables, historical audits or every reference by default. Reuse accepted facts and references; load a hook's overrides only when needed. After two failed image edits, diagnose the hook/layout instead of repeating the same request. Fold new lessons into the existing rule; do not append case histories. Efficiency comes from shorter context and earlier decisions while preserving whole-scene painting and visual review.
