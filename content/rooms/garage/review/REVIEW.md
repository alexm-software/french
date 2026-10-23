# Garage expansion — pre-merge review

Base: `dac80bfe9b41d98b9b64c8367dc84e119c1ddd7e`. Independent reviewer: `garage_review`, separate from the painter.

**Pass in reviewed scope:** 21 source assets and matching hooks, both final composition proofs, French tables/plurals, image decoding, package geometry and static navigation. User already authorized merge. Actual browser/mobile/fullscreen and whole-site gates are not certified by this pre-merge review.

## User feedback addressed

- Garage was sparse and noun-only: expand from nine words to21 across main room10 and workbench zoom11. Add scier and réparer, with red-beret Monsieur Verbe, full seven-tense cards, participles, auxiliary and examples. Keep all nineteen planned garage/tool nouns; move bricolage into the close-up through an explicit assignment update.
- Trou had a weak meaning-only hook: replace the mole/golf-ball sprite with a TROOP of wind-up toys marching into a HOLE. TROOP without final p gives TROO. Redraw the asset and replace its hook together.

## Fixes during review

- Remove accidental miniature benches from ficelle, vis, clou, marteau, ciseau and assemblage sprites; enlarge the isolated tools and helpers.
- Remove manivelle's colored/opaque halo.
- Ground the sawing plank/clamp on the actual bench, with lower-body furniture occlusion and tight post-occlusion hotspots.
- Hang attache and outil from their peg positions; move the outil label to expose its tea-cup cue.
- Correct marteau → les marteaux and ciseau → les ciseaux.
- Preserve whole source sprites; generate smaller 384px card crops and write outputs atomically so no reader sees an empty file.

## Checks

- Exact explicit assignment: 21 unique IDs =19 original garage/tool nouns +2 relevant verbs from superseded verb streets. Other sector assignments are preserved.
- Feminine nouns left and masculine nouns right; two red-beret -er verbs.
- All seven tense tabs and six-person forms (three imperative forms), including scier sciions/sciiez; correct participles and avoir auxiliary.
- Alpha and decoding of all referenced images; no empty files. Hotspot separation, fallback-font label estimates, margins, doorway clearance and zoom badge clearance pass.
- Independent native-size crop/scene review passes. No accidental furniture, wrong hooks or floating assets remain in the reviewed proofs.
- JavaScript syntax, Python package checker and diff whitespace checks pass.
- Static village-map → garage → tools → garage and painted garage-door → village wiring pass. Tense choices now wrap.

Minor findings: the two mime faces differ slightly (one moustache); zoom density11 is within the warning range. Neither obscures a word or changes the grammar convention.

Browser checks are performed after deployment and reported separately; a composition proof is not a browser screenshot. No mobile/fullscreen or whole-site verdict is inferred from these package checks.

## Reviewed proofs

- `room-proof.jpg`: SHA-256 `eef8b510a4be4e62e6f3ddd3f63af258f1db4cd57d57f214a17e6e46ea85c5a2`
- `tools-proof.jpg`: SHA-256 `491a49cbfe11eb6075540b9f38b9a2cb9a99610bd26461f5955318f148ad6373`
- `item-crops.jpg`: SHA-256 `a3d3e05fbb6b940967c3f0608207962c29d99af32a685301a9a9ce49c3b7b376`
- `tools-crops.jpg`: SHA-256 `e2dc0c88bcd82051b7a4d4ef756a730e64880b9e2b647eafd1f38d47f5a37d78`
