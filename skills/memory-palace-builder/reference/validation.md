# Validate the changed work

Mechanical success is not visual acceptance. Release-gates owns the checks and independent art sign-off. State pass/fail/pending/not checked honestly; do not infer visual quality from JSON or mark an old verdict valid after an image changes.

## Scope by change

| Change | Necessary verification |
|---|---|
| Room/zoom painting | manifest + compiled prompt, precheck, strict placement, grid, full visual item/anatomy/count review, parent/zoom comparisons, relevant dialogues/alt/cards |
| Labels/hotspots only | rebuilt data, exact rendered geometry, target room at desktop/mobile/fullscreen; no image regeneration |
| Hook/card/dialogue text | source/override correctness, pronunciation/sense/content, relevant validators and generated output; repaint only if visible hook changed |
| Shared viewer/build rules | affected room types plus broad/global regression and browser checks |
| Skill/tooling only | path/frontmatter checks, meaningful tool fixtures and representative real-data runs; no room art acceptance claims |

Preserve global CI checks. Run fast targeted checks during iterations and the existing global release checks once on the combined build. Wider visual audits are appropriate for shared renderer/style changes or scheduled audits, not repeated whole-site card reading for every local fix. Reuse evidence only when its input files are unchanged; changed parent or child invalidates their continuity verdict. Known unrelated findings are recorded separately, never relabeled as a pass.

## Two main checkpoints, with immediate screening between them

At the composition checkpoint, judge the labels-off shared activity, architecture/depth, group clearance, passages, style and parent/zoom agreement. The first candidate can serve as the draft; do not require another paid sketch when composition is already established. Reject structural failures before detail work.

Screen every intermediate edit immediately: intended fix, affected anatomy/boundaries/neighbors, then a whole-scene regression sweep. State defects by visible region and acceptance condition. Measure actual complete figures/helpers and compute all item/item and item/passage intersections before requesting a finished-art verdict. Hotspot boxes may touch along an edge but must not overlap; an object may touch the picture edge when its box stays inside the frame; labels need 8 px of clearance. If this fails, return to the plan; do not rebuild cards/contact sheets or commission a full independent review yet. Prompts and manifests describe requirements, not observed pixels.

At the finished-art checkpoint, run `tools/precheck.py` on the candidate for size and OCR. Use `tools/contact_sheet.py --layout --image` for fitted geometry and one review packet before rebuilding. Use `tools/zoom_sheet.py` for changed parent/child relationships and the walkthrough passage sheet for changed thresholds. Fix failures before independent review and judge OCR flags. After integration, check actual built data and viewer controls. Inspect the actual paintings: shared story, recognizable literal hooks, placement, palette, contact shadows, exits and no pasted-on appearance. Inspect every hook, exact count, person and animal at 2×, including background anatomy. Trace hands to shoulders; contact-sheet thumbnails do not replace this.

Compare actual parent/zoom silhouette, orientation, contents, surroundings, materials, arrangement and gender bands. Attractive but different interiors fail. A parent change requires reviewing all its child zooms; compare sibling thumbnails for distinctive layouts.

Compare edits against the accepted base for hook/exit, neighbor, framing and light regressions. Recheck affected parent/zoom pairs; preserve the base when a candidate regresses. A prior pass does not transfer to changed pixels. Record revision, defects, acceptance conditions and next action in one compact checkpoint.

Use the same independent reviewer/context for the finished pack and any corrections, providing current image hashes and a concise defect delta. Do not spawn a fresh reviewer per small edit. The reviewer checks changed art and open queue rows; self-review is pending. Browser review follows `building-walkthrough.md`: walk planned physical passages from village to rooms/zooms and outside, then test Back/Hub separately. Check affected controls/dialogs at desktop, mobile and fullscreen for console errors, clipping, overlaps and hidden tense tabs. Preserve the approved UI.

For final install follow release-gates `reference/deploy.md`, including rebuild and same-name image/card cache busting. Report changed spaces/files, checks actually performed, unresolved blockers and release/PR link. When a failure reveals a reusable principle, edit its canonical rule and add a small regression check if mechanical; remove conflicting instructions instead of appending another numbered anecdote.
