# Room workflow tools

Python 3 and Pillow are required; precheck OCR also uses tesseract (eng+fra). Missing OCR is reported, never silently counted as reviewed. Use the existing checkout, not a fresh clone for every room. See each tool's `--help` for its actual arguments.

| Stage | Tool | Result |
|---|---|---|
| Inventory | `unbuilt.py --repo . --building <id>` | Source assignments compared with live word IDs across the village |
| Context | `room_context.py <bld> --room <key> --limit 20 --offset 0` | Target IDs/hooks/IPA/geometry, short siblings and paged unbuilt inventory; supports unpainted buildings |
| Plan | `manifest_template.json` | Complete small syntax example; replace all facts and use limits.json for production density |
| Before images | `plan_check.py --manifest <manifest>` | Required fields, IDs, counts, verb markers, interactions, planned pixel boxes/sides, zoom contract |
| Before images | `plan_check.py --layout <layout> --room <key>` | Draft links, zoom crop/backlink and main-to-room reachability |
| Compile | `build_prompt.py <manifest> --write --output /tmp/room-prompt.txt` | Validates before writing; stores exact prompt_text and prints a short summary |
| Staleness | `build_prompt.py <manifest> --check` | Fails if invalid or compiled prompt no longer matches |
| After images | `precheck.py [IMAGE] --data village/data/<bld>.js --room <key> --manifest <manifest> --json <report>` | Image size, exact built geometry/labels, OCR flags and shared manifest/prompt checks |
| Visual packet | `contact_sheet.py --data village/data/<bld>.js --room <key> --out <dir>` | Painting overlay and item/exit crops; does not replace 2× anatomy/count/hook inspection |
| Continuity | `zoom_sheet.py --data village/data/<bld>.js --out <new-dir>` | Actual parent crop vs child plus hashes in continuity.json; review status starts pending |
| Language | `hook_lint.py [bld ...]` | Mechanical hook heuristics, report only unless --fail; cannot judge phonetics |
| Skill paths | `skills_paths.py` | References name real tracked or new repo files |

Structural validity is not visual or linguistic approval. Review literal cues, coherent scene, real anatomy, exact counts, pronunciation/sense, zoom continuity and user decisions yourself; changed art needs independent sign-off. Keep reports/images in files and summarize failures in chat. All generation is integrated whole-scene art.

Run workflow regression fixtures with `python3 -m unittest discover -s tools/tests -v`. Global release checks remain in `.github/workflows/checks.yml` and `scripts/qa/`; task-specific acceptance is in `skills/memory-palace-release-gates/`.
