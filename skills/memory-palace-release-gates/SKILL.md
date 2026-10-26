---
name: Memory palace release gates
description: >-
  Use together with the Memory palace builder skill whenever painting,
  installing, reviewing or shipping any memory palace space: mandatory per-item
  and per-space gates that must all pass before a space counts as done. A
  one-page gate checklist; procedures live in reference/*.md, read when relevant.
---
# Memory palace release gates

A space is NOT done until every gate passes, and the checker must actually look at the images. Each line is one gate. The file named in a section heading holds the full procedure and examples. Record each result in a dated gates log (space | gate | pass/fail | note) with the site commit. Gate 6 (content) failures block release; any other failure is a major.

## Order of work (reference/tools-and-logs.md)
- 0. Run `tools/unbuilt.py` (by word id, fresh main) before choosing what to paint.
- 1. Write the item manifest and check it against all the gates below before painting (builder reference/planning.md).
- 2. After painting, run `tools/precheck.py --manifest` and fix every FAIL (size, overlaps, touching, detached labels, counts, verb targets, doors).
- 3. Judge each OCR FLAG by eye; scene text that makes sense may stay, and OCR never auto-rejects.
- 4. Run the project's gate scripts (the canonical copies in scripts/qa/); a non-zero exit blocks release.
- 5. Review ONE contact sheet per room (`tools/contact_sheet.py`), opening full-size crops only where a tile raises doubt.
- A checker that disagrees with the viewer is a blocker: port the viewer's geometry and re-run after any viewer change.

## A. Every item and exit crop, at 256 px or more with the headword and hook under it (reference/item-gates.md)
- 1. Hook match: the figure shows exactly the hook scene; check the sound-clue object first.
- 2. Anatomy: limbs, hands, fingers and faces are right; no severed parts as props; no duplicated objects.
- 3. Clean rendering: nothing garbled or half-formed; regenerate rather than accept it.
- 4. Grounded props: everything is held, mounted or resting; nothing floats.
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
- 12. At most about 10 items (more than 12 fails), each box at least 6% from every edge, figures grounded, no rows on shelves.
- 13. No look-alike spaces: run a similarity measure, then compare the flagged pairs by eye.
- 14. One style per building or street, matching its exterior.
- 15. Colour: natural neutral daylight, matching the palette sheet; a whole-room amber or orange cast fails.

## Text in the image (builder reference/text-and-labels.md)
- Natural scene text that makes sense passes (shop sign, book spine, poster), if it covers no item and can't be read as a label.
- Stray or garbled text, prop symbols, speech bubbles and count-breaking digits fail.

## E, F. Composited scenes (reference/item-gates.md, reference/space-gates.md)
- E: each asset shows the hook and the meaning, is one word only, renders cleanly, matches the style, is cleanly cut out and card-ready, and has the right perspective.
- F: no overlaps; labels sit on their own asset; assets rest on surfaces with contact shadows; the room is coherent; hotspots line up.

## G, H and rounds 5-10: scene gates (reference/space-gates.md)
- The planned assignment is law; every word suits the place; close-ups are real spots that look like their parent.
- No rows of stickers; the scene is painted first and assets are drawn to fit; nothing grows out of a door frame.
- Verbs are acted at human scale by the language's marker, spread through the scene among the nouns.
- A zoom matches its parent side by side; the style matches the references; no unpainted patches.
- Theme, naming, clutter and liveliness gates pass; no room is mostly shelves or cubbies (periodic shelf audit).
- Distinct rooms: put a building's thumbnails side by side, and each needs its own composition and light.
- No one-object zooms; zooms under about 4 words are folded into a fuller scene.
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

## Deploy (reference/deploy.md)
- Make one combined pack per batch of rooms; the deploy reports once, when live.
- User-reported, P0 and P1 fixes still ship as small hotfixes in the next window.
- Rebuild cards and data after every repaint, in the same pack.
- Check ownership before painting; regenerate shared data from the merged layout.
- Keep each tarball under 25 MB with no screenshots; account for removals (plan-only words, sparse rooms) at every stop.
