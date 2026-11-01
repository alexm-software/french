---
name: memory-palace-release-gates
description: Check and release memory-palace rooms, zooms, maps or related site changes. Use for independent art review, mechanical checks, integration and deployment; distinguish automated checks from visual evidence.
---
# Memory palace release gates

A painting is complete only when structural checks AND visual acceptance pass. Scripts do not judge sound-alikes, anatomy or parent/zoom identity. Read the builder skill for execution, and only the references needed below.

| Work | Acceptance references |
|---|---|
| Room/zoom art, new or repainted | `reference/item-gates.md`, `reference/scene-contract.md`, `reference/space-gates.md` |
| Numbers/reference board | also `reference/number-and-count-rooms.md` |
| Geometry/labels | `reference/space-gates.md` §B |
| Review evidence | `reference/tools-and-logs.md`, `reference/process.md` |
| Shipping | `reference/deploy.md` |

## Ordered stops

1. Before image generation: builder planning manifest, `tools/plan_check.py`, then `tools/build_prompt.py --write` and `--check`. Use authoritative inventory/overrides and `skills/limits.json`. Resolve hook quality, interaction, floor plan and zoom identity now.
2. After generation: `tools/precheck.py` with manifest and built room data; canonical `scripts/qa/check_v2.py --strict --placement` and applicable room/grid/text checks. Fix every relevant FAIL. OCR is a human-review flag. Checkers must match the viewer's geometry.
3. Review the room contact sheet, labels-off painting and every item/exit. Inspect EVERY hook cue and exact count, and EVERY person/animal at 2×, including scenery. Count limbs and trace hands; no thumbnail-only anatomy verdict. Literal recognizable hooks, grounded props, no stray objects, natural neutral colors, no garbled text, no lineup/grid or pasted-on figures.
4. Run `tools/zoom_sheet.py` for changed parent/zoom pairs. Compare actual parent crop with child: identity, shape, orientation, contents, arrangement, materials, light and placement. Added detail must agree with what the parent shows. Compare sibling thumbnails for distinct compositions. A changed parent requires re-review of all its zooms.
5. Independent art review and relevant open queue rows must pass. Self-review is pending. Evidence names input commit/image hashes and reviewer; a prior pass becomes stale when either image changes. No automated tool invents a visual pass.
6. Integrate and rebuild data/cards together; verify village/sector entry, painted passages, zooms, Back and Hub in the browser for changed navigation. Ordinary-room Back goes outside; zoom Back goes parent; Hub goes building main and is hidden there. One visible control per destination.
7. Run existing global CI/release checks on the combined build. Same-name image/card changes require the service-worker version bump and `check_v2.py --strict --placement --cache-base <base>`. Follow deploy reference; use existing user authorization.

Review scope follows builder `reference/validation.md`: local iterations check changed work and dependencies; shared renderer changes widen scope. Retain global CI. Report what was checked, pending or failed. Content/copyright failures block release; other failed art gates also require correction. Never make a box miss its painted figure just to get a green check.

All ages, American English, usage warnings for negative/sensitive senses, respectful sacred content and credited/licensed texts remain mandatory (builder sensitive-content/copyright references). Plain depictions beat forced sound-alikes. Preserve user-selected hooks. Fold new failures into the canonical rule or regression fixture; do not grow a second history of repeated gates.
