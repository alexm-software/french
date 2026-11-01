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
| New building/room/zoom | `reference/planning.md`, `reference/composition.md`, `reference/prompt-template.md` |
| Repaint or move words | above plus `reference/moving-words.md` |
| Hook text | `reference/hooks.md`; language `reference/hooks.md` |
| Labels/hotspots | `reference/text-and-labels.md` |
| Map/navigation | `reference/maps-and-navigation.md`, `reference/site-ui.md` |
| New project, copyright, sensitive content | corresponding `reference/setup-and-style.md`, `reference/copyright.md`, `reference/sensitive-content.md` |
| Validation/release | `reference/validation.md`; release-gates skill |

## Plan → compile → paint → integrate

Follow `reference/planning.md`. Before paying for an image, record the building's physical connections and a room manifest using `tools/manifest_template.json`. Resolve the words, hooks, exact counts, verb markers, interaction groups, candidate boxes and all destinations. For a zoom, pin the actual parent image/crop and the features it must preserve.

Run `python3 tools/plan_check.py --manifest <manifest>` and the layout check if drafted, then `python3 tools/build_prompt.py <manifest> --write --output /tmp/room-prompt.txt`. Fix FAILs before painting; warnings require judgment. Attach the real references. Work on one representative room first; once its composition and language devices pass, continue the building. Do not buy a batch of unreviewed paintings.

Fit boxes to the finished hooks; do not move boxes away from art to satisfy a checker. Rebuild data/cards with the repo's existing tools. Keep hooks, dialogue, alt text, cards and zoom miniatures consistent with the final painting. Release only after the gates appropriate to the changed files pass.

## Token and retry budget

Keep one compact manifest and a short checkpoint (base commit, completed steps, changed paths, next action, blockers). Save tool output/review evidence in files; report counts and failures, not full payloads or repeated prompts. Do not read bundled JS, conjugation tables, historical audits or every reference by default. Reuse accepted facts and references; load a hook's overrides only when needed. After two failed image edits, diagnose the hook/layout instead of repeating the same request. Fold new lessons into the existing rule; do not append case histories. Efficiency comes from shorter context and earlier decisions while preserving whole-scene painting and visual review.
