---
name: Memory palace release gates
description: >-
  Use together with the Memory palace builder skill whenever painting,
  installing, reviewing or shipping any memory palace space: mandatory per-item
  and per-space gates that must all pass before a space counts as done. A
  one-page gate checklist; procedures live in reference/*.md, read when
  relevant.
---
# Memory palace release gates

A space is NOT done until every gate passes, and the checker must actually look at the images. Each line is one gate. The file named in a section heading holds the full procedure and examples. Record each result in a dated gates log (space | gate | pass/fail | note) with the site commit. Gate 6 (content) failures block release; any other failure is a major.

**Read only what the task needs:** new or repainted room: item-gates.md, space-gates.md, tools-and-logs.md · labels only: space-gates.md §B · number or count room: number-and-count-rooms.md · shipping: deploy.md · final scene: space-gates.md §F. Gates that scripts hold: `scripts/qa/check_v2.py --strict --placement` (geometry, sides, room size, one hook per word), `tools/precheck.py`, `tools/hook_lint.py`; all run on every pull request (`.github/workflows/checks.yml`).

## Order of work (reference/tools-and-logs.md)
- 0. Run `tools/unbuilt.py` (by word id, fresh main) before choosing what to paint.
- 1. Write the item manifest and check it against all the gates below before painting (builder reference/planning.md); build the prompt from builder reference/prompt-template.md, every field filled (it prevents rework; every gate below still applies strictly).
- 2. After painting, run `tools/precheck.py --manifest` and fix every FAIL (size, overlaps, touching, detached labels, counts, verb targets, doors, the prompt fields).
- 3. Judge each OCR FLAG by eye; scene text that makes sense may stay, and OCR never auto-rejects.
- 4. Run the project's gate scripts (the canonical copies in scripts/qa/); a non-zero exit blocks release.
- 5. Review ONE contact sheet per room (`tools/contact_sheet.py`), opening full-size crops only where a tile raises doubt.
- 6. Open a 2x crop of every hotspot box and confirm the hook's sound-clue details are painted inside the box (section I).
- A checker that disagrees with the viewer is a blocker: port the viewer's geometry and re-run after any viewer change.
- A doubt you would list in your report is a FAIL to fix before packing, not a note to ship with.

## A. Every item and exit crop, at 256 px or more with the headword and hook under it (reference/item-gates.md)
- 1. Hook match: the figure shows exactly the hook scene; check the sound-clue object first.
- 2. Anatomy: limbs, hands, fingers and faces are right; no severed parts as props; no duplicated objects.
- 3. Clean rendering: nothing garbled or half-formed; regenerate rather than accept it.
- 4. Grounded props, no strays: nothing floats; no prop or figure stands for no word or reads as an unlabeled word; plain background figures are fine as scenery.
- 5. Hook strength: the sound-alike comes from the real pronunciation and is an English word, never the target word or its meaning.
- 6. Content, in the art and the hook text: adult items appear only as objects, no child is near them, and nobody drinks or smokes.
- Every hook element is visible; the hook acts on or touches the item; no anthropomorphic animals unless the animal is the hook.
- Operated props are mounted, with the figure touching them; open repaint-queue rows are fixed by the repaint.

## B. Labels and controls (reference/space-gates.md)
- 7. Rendered label rectangles are computed by the exact render path; no label overlaps or touches anything, at every viewport.
- 8. One control per destination, never two to the same place.
- 9. Exits look like their destination, show a glimpse of it, and name it.
- 10. Every space has a painted way out plus the way up; door views match the plan; stairs go the right way.

## C. Setting and layout (reference/space-gates.md)
- 11. A rich, real setting with its own walls, floor, depth and one nameable landmark.
- 12. At most `room_target` items (more than `room_max` fails; skills/limits.json, checked by check_v2), each box at least `edge_margin` from every edge, figures grounded, no rows on shelves.
- 13. No look-alike spaces: run a similarity measure, then compare the flagged pairs by eye.
- 14. One style per building or street, matching its exterior.
- 15. Color: natural neutral daylight, matching the palette sheet; a whole-room amber or orange cast fails.

## I. Navigation sense and hook crops (added Oct 2026 from user reports)
- 16. Physical layout makes sense: draw the building or area as a floor plan or walk before painting. Interiors connect by real doors in walls; outdoor scenes connect by paths, steps, gates or footbridges at the scene edge, never by huts, sheds or freestanding doors in open ground.
- 17. Shared scenery is consistent across a building or area: the same pond, river, bridge, sky and season wherever it appears, and each scene links to its real neighbours, not only back to a hub.
- 18. Doors and exits are big enough to read at 900 px width (roughly 80 px tall or more at 1280) and look like a way through.
- 19. In any room, Back goes straight outside to the street or map the building stands on, never to the previous room; moving between rooms is by painted doors only, and a room with two entrances shows both doors. Next to Back sits a second '⌂ Hub' button (tooltip = the hub room's name) that jumps to the first room / hub of the current building or area; it is hidden in the hub itself.
- 20. No two hooks in the same building share the same picture or object (for example two hooks both drawn as a walnut, or two spore/mushroom hooks); pick a distinct sound-alike instead.
- 21. A hotspot box frames its own hook figure and does not cut through an unrelated prop; the hook's props sit wholly inside its box.
- 22. The intended object must read as itself at 2x (a ball must look like a ball, not a nut); if it could be named as something else, repaint it.
- 23. Compose each room as an angled, layered scene (foreground, middle, back) around one named situation before assigning boxes; a frontal view with figures standing in one or two rows along the wall and floor fails, even when every hook is right.
- 24. Each room is ONE generated painting (a square-centre generation plus one outpaint, or a crop-edit of that painting). Never paste cut-out or green-screen figure sprites onto a background plate, and never draw marks with code; sprite rooms look like stickers on an empty set and fail even when every other gate passes.
- 25. No grid of hook figures: spread the figures over at least three depths (foreground, middle, back), with box bottoms at varied heights. If more than three boxes share a baseline (box bottoms within about 40 px) or the boxes form two horizontal bands, the room fails. Check the box overlay, not just the painting.
- 26. Anatomy check on every person and animal at 2x: count heads, arms, hands, legs and fingers one figure at a time, and trace every hand back to its own shoulder. An extra or missing limb, a hand that belongs to nobody, merged bodies or a twisted face is a FAIL, even outside a hook box. Image models often add a third arm when a figure both holds something and balances something, so check those poses twice. A thumbnail overview is not this check.

## Text in the image (builder reference/text-and-labels.md)
- Natural scene text that makes sense passes (shop sign, book spine, poster), if it covers no item and can't be read as a label.
- Stray or garbled text, prop symbols, speech bubbles and count-breaking digits fail.

## F. Final scene (reference/space-gates.md)
- F: no overlapping boxes or labels; objects grounded with contact shadows; one coherent painting with no seams or pasted patches; hotspots line up.

## G, H and rounds 5-10: scene gates (reference/space-gates.md)
- The planned assignment is law; every word suits the place; close-ups are real spots that look like their parent.
- No rows of stickers; nothing grows out of a door frame.
- Natural scene: one named situation, small interacting groups, varied facing and depth; a lineup or grid of isolated hook figures fails, and so does the labels-off storybook test.
- Verbs are acted at human scale by the language's marker, spread through the scene among the nouns.
- A zoom matches its parent side by side; the style matches the references; no unpainted patches.
- Theme, naming, clutter and liveliness gates pass; no room is mostly shelves or cubbies (periodic shelf audit).
- Distinct rooms: put a building's thumbnails side by side, and each needs its own composition and light, with no repeated motifs.
- No one-object zooms; zooms under about 4 words are folded into a fuller scene.
- Alphabet = one blackboard zoom with all letters in chalk; no per-letter mnemonics, never multiple rooms (language reference/representation.md).
- Maps: exteriors show their function, overview and inner maps agree, and the overview is one painting (builder reference/maps-and-navigation.md).
- Placement-by-meaning, sense, no-overflow and sensitive-setting gates pass (language reference/placement-and-senses.md).
- One-hook and forced-pun gates pass (builder reference/hooks.md).

## Number and count rooms (reference/number-and-count-rooms.md)
- Every number item shows exactly that many easy-to-count things; count each at 2x before packing.
- The manifest holds the count, and painted digits never compete with it.

## Process (reference/process.md)
- Crop sign-off comes from someone other than the painter; a self-certified review counts as pending and never ships.
- Queued problems block their space; staged fixes are re-checked on the combined build.
- Show the user clean screenshots before shipping, and fix what they flag first.
- At checkpoints, re-run every gate on the whole live site plus the queue; re-audit live spaces whenever a gate is added.
- Each new kind of user-reported issue becomes a numbered gate, with a script where possible.

## Copyright (builder reference/copyright.md)
- Every quoted text has a dated public-domain source or is our own translation, says how it may be used, and is named in CREDITS.md; `tools/copyright_check.py` passes. A copyright failure blocks the release like gate 6.

## Deploy (reference/deploy.md)
- Make one combined pack per batch of rooms; the deploy reports once, when live.
- User-reported, P0 and P1 fixes still ship as small hotfixes in the next window.
- Rebuild cards and data after every repaint, in the same pack.
- Gate 27, cache busting (pack-time rule): a repaint or rebuilt card that keeps its filename must reach returning visitors. `village/sw.js` answers every GET network-first (cache = offline fallback only), uses skipWaiting/clients.claim, and extras.js registers it with updateViaCache 'none'. If any existing image or card changed since the deploy base, bump `V='village-vN'` in sw.js in the same pack. Before packing run `python3 scripts/qa/check_v2.py --strict --placement --cache-base <base commit or tree>`; a cache FAIL blocks the pack.
- Check ownership before painting; regenerate shared data from the merged layout.
- Keep each tarball under 25 MB with no screenshots; account for removals (plan-only words, sparse rooms) at every stop.
