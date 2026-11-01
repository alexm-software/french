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

## After a painting

Run `tools/precheck.py` with the manifest, data and room. Fix FAILs before eyes; OCR flags require judgment, not automatic rejection. Generate one `tools/contact_sheet.py` output per room and `tools/zoom_sheet.py` for every changed parent/child relationship. Inspect the actual paintings: shared story, recognizable literal hooks, placement, palette, contact shadows, exits and no pasted-on appearance. Inspect every hook, exact count, person and animal at 2×, including background anatomy. Trace hands to shoulders; contact-sheet thumbnails do not replace this.

Compare parent and zoom side by side: object silhouette, opening direction, orientation, contents, surroundings, colors/materials, relative arrangement and gender bands. A crop and a completely different interior fail even if each looks attractive alone. Review all existing child zooms when their parent changes. Compare sibling thumbnails for distinctive layouts, not only stylistic consistency.

An independent reviewer checks changed art and open queue rows; self-review is pending. Browser review follows the actual navigation path from village/sector to building to room/zoom, and back. Check all controls/dialogs of the affected type at desktop and narrow mobile widths and in fullscreen. No console errors, clipped items, overlapping labels or hidden tense tabs. Match approved UI, don't add features during validation.

For final install follow release-gates `reference/deploy.md`, including rebuild and same-name image/card cache busting. Report changed spaces/files, checks actually performed, unresolved blockers and release/PR link. When a failure reveals a reusable principle, edit its canonical rule and add a small regression check if mechanical; remove conflicting instructions instead of appending another numbered anecdote.
