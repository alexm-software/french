# Independent review: sciences hall gallery-view candidate

- Image sha256: d2d9522da43789388b76ff200d245acdd9fcdc66e4cc56a37dce141369b0a4da (verified)
- Zip sha256: dc9f1c06585f0480def8bd005773b0f8b9402e65edd687d755f772b68c1fd155
- Prompt sha256: 2206ed68d6704f3183ba20de7825b69d988eb2001ee568905f68f0bff2f5ff48 (verified, read in full)
- Hooks: source/hooks.json (0fd2ff8f…). The pierre hook is now plain: "one dressed building STONE, a sawn block".
- Reviewer: Grok Bot independent reviewer
- Written: 2026-11-07, about 11:15 PM CST
- 2x crop: my_people2x.png
- Boxes are word + named helper, x0-x1 / y0-y1 at 1280x720, about ±8 px. Tables, stands, cart and tray-as-floor are support.
- Margins: x 77..1203, y 43..677.

## VERDICT: FAIL

The base composition is valid. It needs one integrated correction pass.

## Groups

| word | box | centre | margin | cue |
|---|---|---|---|---|
| pierre | — | — | — | **FAIL: absent.** No sawn stone anywhere. The worker's claim is confirmed. |
| terre (sack, spill, seedling) | 156-456 / 400-631 | 24% L | ok | PASS |
| mine (mound, tunnel, rails, cart, lantern) | 19-448 / 138-356 | 18% L | **FAIL: left 19.** The mound itself crosses the margin. | PASS |
| minéral (geologist + lamp + cluster) | 525-788 / 278-528 | 51% (inside the 30-70 band) | ok | Mostly PASS: cluster, lamp and rainbow are there. The geologist handles the cluster with both hands and does not tilt the lamp, which differs slightly from the hook wording. |
| cristal (crystal + mouse; the cup is incidental) | 1010-1165 / 94-381 | 85% R | ok | PASS. The mouse is at the base of the crystal, on the stand. |
| sol (boot + tray + worm) | 835-1175 / 398-688 | 78% R | **FAIL: bottom 688**, 11 px over | **Sound cue weak.** The boot stands upright, so the SOLE is hidden in the soil. The hook says "sole pressed into", which matches literally, but the sound object is not visible (G104/G115). The worker's claim is confirmed. |

- **Overlaps:** none among the target groups. The mine table bottom and the sack top are both support or edges.
- **Anatomy at 2x:**
  - Geologist: two arms, two hands on the cluster, two legs and shoes, normal face. PASS.
  - Mouse: one head, two ears, forepaw, body. PASS.
- **Cup:** a teacup of coffee beside the mouse. It is a literal "teacup-sized" prop, ungated and harmless. It adds clutter but is not a stray word.

## Prompt and source disagreements
- The prompt asks for a 35° gallery view. The painting is near eye-level, about 15-20°. Acceptable.
- The prompt asks for the telescope "seen through the glass … windows above". The painting shows a telescope standing outside on the path through the doors. The faculty identity is weaker: it reads as a telescope in the park.
- The prompt asks for doors "open". The centre glass doors read as closed. The exit is visible but not clearly open.
- Stone missing; boot sole hidden (see table).

## Can one focused integrated edit fix it?
Plausibly yes, as ONE integrated pass. All semantic groups stay. The corrections are local:
1. **Add pierre:** a sawn stone block on the open floor in the front-centre-left, about x 340-540, y 560-650. That gives a centre of about 35% (feminine side). It must stay clear of the sack spill (which ends at about x 456, y 631), so put it right of the spill or nudge it to x≥470.
2. **Tilt the boot** so its tread shows while touching the soil. Or lay the boot on its side, sole facing the viewer, pressed into the soil.
3. **Slight zoom-out or reframe** (about 6%) so the mine mound clears x77 and the tray clears y677.
4. **Optional:** doors visibly open; telescope above or through the roof glass.

## Highest risk
The edit tool has no mask. Past edits redrew the whole scene and lost groups (butcher, downstairs). Collateral risk is HIGH.

## Must preserve (re-check all after the edit)
- mine mound with tunnel, lantern and cart
- cart + torn sack + seedling
- geologist + lamp + rainbow cluster in the centre (centre 30-70%)
- crystal + mouse back right
- worm in the tray
- centre-door view

## Note
The external ChatGPT reservations (R_cafe_02, R_resto_kitchen_02, R_measures_01, R_emo_joy_01) do not affect this science room.
