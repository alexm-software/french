# Independent review: sciences hall gallery EDIT

- Edit image sha256: 5c766c72a59a37869fbb41bfeffefa1faa50d25a631643662004b74b52240521 (verified)
- Zip sha256: 4432af82…1fa6
- Edit delta sha256: 8f00e3b0…d921 (verified, read in full)
- Base image: d2d9522d
- Hooks: source/hooks.json f693964c
- Reviewer: Grok Bot independent reviewer
- Written: 2026-11-07, about 11:20 PM CST
- Crops: my_2x.png
- Boxes are word + named helper, at 1280x720, about ±8 px. Margins: x 77..1203, y 43..677. Tables, stands, the cart and the tray floor are support.

## VERDICT: FAIL (2 real cue/geometry defects + 2 small edge overshoots)

| word | box x0-x1 / y0-y1 | centre | margins / overlap | cue |
|---|---|---|---|---|
| pierre (stone) | 328-525 / 388-528 | 33% L | ok, but **rectangle overlaps terre** in [328-400]×[410-528] (empty floor) | **FAIL.** A block with two arched tunnel openings reads as a second mine or a kiln. It is not one plain sawn block (hook "dressed building STONE, a sawn block"). It is ambiguous with mine. |
| terre (sack, spill, seedling) | 106-400 / 410-656 | 20% L | ok. The cart wheel at x≈63 is support, not a helper, so it is not a fail. | PASS |
| mine (mound, tunnel, rails, ore cart, lantern) | 69-381 / 148-328 | 18% L | **left 69 < 77**: the mound's grey toe overshoots by about 8 px. The table is support. | PASS |
| minéral (geologist, lamp, cluster) | 560-835 / 272-550 | 54% (inside 30-70) | ok | PASS. Rainbow, lamp and cluster present. The geologist holds the cluster rather than tilting the lamp (minor wording). |
| cristal (crystal, mouse; the cup is incidental) | 1015-1169 / 102-381 | 85% R | ok | PASS |
| sol (boot, tray, worm) | 858-1190 / 431-~681 | 80% R | **bottom rim ≈680-682 > 677**: about 4 px | **PASS, fixed.** The ridged tread faces the viewer and the heel stays in the soil. The worm is beside it. |

## Anatomy, traced at 2x
- Geologist: two arms and hands, two legs and shoes, normal face. PASS.
- Mouse: head, two ears, body. PASS.
- Worm: one body. PASS.

## Doors and passage
- The centre glass panel is now clearly an open doorway onto the gravel path and trees. This permits a physical entrance and return. PASS.
- The telescope still stands outside on the path. Identity is acceptable but weak. Not a gate fail.

## Edit vs base
The EDIT is the better corrective base. Preserved improvements:
- visible boot sole
- tray lifted (nearly clear)
- open doorway
- every other group retained, counts correct, no new people or animals

Remaining work, all LOCAL and on the left:
1. **Stone:** replace the arched block with a solid sawn rectangular block. No openings, smooth cut faces, roughly the same footprint. Move it about 60-80 px further right/front, e.g. x≈420-600, y≈560-650. Its centre is then about 40% (still feminine) and its box clears the sack/spill box (which ends at x≈400).
2. **Edges:** a tiny additional step-back of about 2% fixes both the mine toe (8 px) and the tray rim (4 px). Alternatively, nudge the mound and tray slightly inward.

## Highest risk
An unmasked edit could regress the boot sole or the doors again. The next delta must restate them as KEEP.

## Must preserve
- boot sole toward the viewer + worm
- open doorway
- geologist / lamp / rainbow
- crystal + mouse
- cart / sack / seedling
- mine with one tunnel, lantern, rails and ore cart
