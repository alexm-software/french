# Checks and evidence

## Before buying an image

Use `tools/unbuilt.py --repo .` and `tools/room_context.py` on the existing checkout. Fill `tools/manifest_template.json`, run `tools/plan_check.py --manifest <manifest>`, and check the draft layout with `--layout <layout> --room <key>`. Compile using `tools/build_prompt.py <manifest> --write --output /tmp/room-prompt.txt`; `--check` rejects stale text. Warnings require judgment; structural FAILs stop generation. These tools do not verify language or visual quality.

## After painting

Run `tools/precheck.py <image> --data village/data/<bld>.js --room <key> --manifest <manifest>` (see `--help` for flags). Then run canonical `scripts/qa/check_v2.py --strict --placement` and applicable `scripts/qa/grid_check.py`/text checks. Use `--browser` with a local server for rendered checks; port actual viewer geometry into checkers, never estimate it. Keep failures and OCR flags in a file; summarize them in chat.

`tools/contact_sheet.py` provides the room overlay, item/exit crops and optional browser shot. It supports one coherent visual pass, but does not replace mandatory 2× inspection of all hook details, counts and human/animal anatomy, even outside boxes. Additional full-size views are only needed for other ambiguities. `tools/zoom_sheet.py --data village/data/<bld>.js --out <new-review-directory>` compares actual parent crops with zoom paintings and writes `continuity.json` with both hashes and pending verdicts. Have the reviewer record identity/orientation/content/layout/material/placement findings and verdict; rerun when either input changes.

Use a fresh output path for each revision, so image-viewer caching cannot conceal a change. Record commit, relevant image hashes, reviewer, checks, findings and pending items. Mechanical output and a pending review file are never visual sign-off. Reuse unchanged evidence, not a verdict from stale inputs. For room similarity, a CLIP-free run is only a smoke test; compare actual sibling thumbnails too.

## Integration

Keep one canonical checker per rule. Run global CI on the combined build, plus cache-base checks for image/card changes and browser checks for UI/navigation. Review scope is in builder `reference/validation.md`; art acceptance is in `scene-contract.md`, `item-gates.md` and `space-gates.md`. Repository tool usage lives in `tools/README.md`.
