# Tooling and token economy

## Load once

Use `tools/lookup.py` for an id, gloss, room or building question (`data/source/vocab.index.jsonl`, `data/source/rooms.index.jsonl`, stamp `data/source/index.stamp.json`). `tools/lookup.py --check` fails when that index is stale; `--rebuild` rewrites it from `data/source/vocab.jsonl`, `data/source/rooms.json`, `content/v2/vocab_fixes.json` and `data/cache/conjugations.json`. Use `room_context.py` (with `--init-manifest` for new rooms) for the resolved target brief and `unbuilt.py --repo . --building <id>` for live IDs. Reuse the checkout and fetch main once. Read target records, required references and affected dependencies; reserve whole-repo inventories for audits. Parse/filter large payloads in code rather than writing ad-hoc one-liner scripts per field. Print findings/counts, never full registries, commit responses, prompts or binary/base64 content.

The static site loads committed `village/data/index.js`, `village/data/live.js` and `village/data/talk/index.js`. Regenerate those with `scripts/v2/build_extras.py` when a room payload changes. Do not hand-merge them.

Keep one building plan, room manifest and checkpoint (base, touched paths, accepted revision, blockers, next action). `build_prompt.py --write --output` saves the specification; `--check` detects drift. Save exact local-edit deltas separately, stating which specification fields they replace.

## Choose working capabilities early

Check required local executables/libraries once before expensive work. Establish a usable fallback or record the test limitation. A remote browser may not reach executor loopback; do not create extra deployments merely to test reachability.

Prefer connected GitHub publishing tools when available. Do not retry command-line pushes with credentials known absent. Reuse one route; upload changed files only, create one tree/commit and PR, verify contents/CI, then merge under existing authorization. Load transfer bytes programmatically without printing them. Preserve concurrent work and obey approval policy; never route around a rejected action.

## Reuse valid evidence

Geometry and `plan_check.py` preflight (source metadata agreement, verb beret/mirror verification, respelling/content/hook lint, Gate 25 baseline distribution, and simulated label placement) precede image calls and final review. Follow SKILL.md's retry rule. Reuse one reviewer/context, passing current paths, manifest and a short defect delta. Screen intermediate edits immediately; `contact_sheet.py --grid --anatomy-2x --sync-manifest` produces the room overlay, coordinate grid, and 2× quadrant crops in one pass, and final acceptance still checks every required hook/count/anatomy detail at 2× and actual parent/zoom agreement (`zoom_sheet.py`).

Use unique review paths per revision. Layout/`boxPx` coordinates are pixels; built `box` values are percentages. Rebuild with existing scripts, never hand-fix generated payloads or invent another geometry implementation. Run targeted iteration checks (`check_v2.py --browser --rooms-only` for room iterations) and global CI on the combined pack; reuse only results with unchanged inputs.
