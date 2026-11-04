# Room workflow tools

Python 3 and Pillow are required; precheck OCR also uses tesseract (eng+fra). Missing OCR is reported, never silently counted as reviewed. Use the existing checkout, not a fresh clone for every room. See each tool's `--help` for its actual arguments.

| Stage | Tool | Result |
|---|---|---|
| Inventory | `unbuilt.py --repo . --building <id>` | Source assignments compared with live word IDs across the village |
| Lookup | `lookup.py <text> [--id fr_...] [--room R_...] [--building <slug>] [--rebuild] [--check]` | One line per source-plan hit from `data/source/vocab.index.jsonl` and `data/source/rooms.index.jsonl` (gender, cefr, beret, room, building, say, gloss). Does not scan vocab.jsonl or rooms.json |
| Context & scaffold | `room_context.py <bld> --room <key> [--vocab-room R_...] [--init-manifest <manifest>]` | Resolved word records (gender, IPA, say, hook, verb beret/mirror, live locations), short siblings, optional pre-populated manifest |
| Plan | `manifest_template.json` | Complete small syntax example; replace all facts and use limits.json for production density |
| Before images | `plan_check.py --manifest <manifest>` | Required fields, canonical source/beret/gender/respelling/content/hook-lint preflight, Gate 25 grid check, simulated label placement, zoom contract |
| Before images | `plan_check.py --layout <layout> --room <key>` | Draft links, zoom crop/backlink, main-to-room reachability, Gate 25 grid check, in-memory label collision simulation |
| Compile | `build_prompt.py <manifest> --write --output /tmp/room-prompt.txt` | Validates before writing; stores exact prompt_text and prints a short summary |
| Staleness | `build_prompt.py <manifest> --check` | Fails if invalid or compiled prompt no longer matches |
| After images | `precheck.py [IMAGE] --data village/data/<bld>.js --room <key> --manifest <manifest> --json <report>` | Image size, exact built geometry/labels, OCR flags and shared manifest/prompt checks |
| Visual packet | `contact_sheet.py --data village/data/<bld>.js --room <key> --out <dir> [--grid] [--anatomy-2x] [--sync-manifest <manifest>]` | Painting overlay, item/exit crops, coordinate grid for 1-pass box fitting, 2× anatomy quadrants, and manifest box sync |
| Continuity | `zoom_sheet.py --data village/data/<bld>.js --out <new-dir>` | Actual parent crop vs child plus hashes in continuity.json; review status starts pending |
| Language | `hook_lint.py [bld ...]` | Mechanical hook heuristics, report only unless --fail; cannot judge phonetics |
| Skill paths | `skills_paths.py` | References name real tracked or new repo files |

Structural validity is not visual or linguistic approval. Review literal cues, coherent scene, real anatomy, exact counts, pronunciation/sense, zoom continuity and user decisions yourself; changed art needs independent sign-off. Keep reports/images in files and summarize failures in chat. All generation is integrated whole-scene art.

Run workflow regression fixtures with `python3 -m unittest discover -s tools/tests -v`. Global release checks remain in `.github/workflows/checks.yml` and `scripts/qa/`; task-specific acceptance is in `skills/memory-palace-release-gates/`.
