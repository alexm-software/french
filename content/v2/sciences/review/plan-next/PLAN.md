# Faculty plan checkpoint

No new painting. The finds image `080d7f5e` is rejected. The hall at `abb996da` stays release-ready and unmerged. Art calls stay 36.

## Topology

The campus map has one sciences entrance: `B35_sciences` on `village/map/university.jpg` at `[950, 245, 320, 255]`, crop `review/six/sciences-faculty-crop.png` (`e5212a33…`). The click opens the hall. The hall's only way out is those glass doors, back to Campus. Back uses the same destination. Hub stays hidden.

The accepted hall (`d1d59540`, `village/sciences/sciences.jpg`) has no other opening.

- Left wall, crop `hall-left.jpg`: tan panels behind the mine table and the earth cart. No door.
- Right wall, crop `hall-right.jpg`: tan panels beside the crystal, and the edge of the campus glass. No side door.
- Back, crop `hall-doors.jpg`: the campus doors and the telescope. That opening is already the Campus exit.

A second campus entrance is not on the map. A new map building would be a different building, and these words belong to B35. A hub between the campus and the hall would change the accepted route. A zoom can only show a cluster already in the hall. The remaining rock words are not those objects, so a zoom would be the wrong parent. A one-object zoom is not the plan.

An interior room therefore needs a new opening in the hall. That is a new painting of the accepted hall, not a small patch: the left wall is filled by the mine and the cart, the right wall by the crystal and the boot, and the back wall by the Campus doors. Adding a door moves at least one accepted group or the Campus exit. It would drop the hall's art pass and its release-ready status. This plan does not do that.

`plan_check.py` on this manifest reports one failure: an ordinary room needs a way out. That failure is the blocker. The prompt below has no door.

## géologue

Source: `fr_geologue_noun`, noun, gender `mf`, article `le/la`, gloss geologist, room `R_geology`. `scripts/qa/check_v2.py` already rejects an epicene noun whose centre is outside 30–70%. The prompt template now says the same. No new side was added to fill the middle.

## Next room, not for generation

One oak table. She sorts finds at the middle. A prospector pans at the left end. Four small objects sit on the tabletop. No life-size animal and no volcano landscape.

| id | g | band | hook kept | envelope |
|---|---|---|---|---|
| fr_prospection_noun | f | left, centre 230 (18%) | prospector, pan, one flake | [80, 220, 300, 400] |
| fr_geologue_noun | mf | centre 580 (45%) | she taps a gray rock shaped like a log | [450, 180, 260, 440] |
| fr_volcan_noun | m | right, centre 860 (67%) | fist-sized model, white foam, no animal | [780, 150, 160, 120] |
| fr_minerai_noun | m | right, centre 1075 (84%) | hand-sized mole figurine and one ore lump | [1000, 160, 150, 120] |
| fr_filon_noun | m | right, centre 880 (69%) | thin gold line on a split rock, not a nugget | [790, 420, 180, 120] |
| fr_caillou_noun | m | right, centre 1105 (86%) | one pebble, no coyote | [1040, 430, 130, 110] |

The boxes do not overlap. Edges sit inside 77 and 1203 horizontally and inside 43 and 677 vertically. Labels fit under the people (about y 624–660) and under the small objects (about y 280–300 and y 545–580), clear of the other boxes.

Queued, not in this design: gisement, dureté, creuset (smelting), pendule (forces), and every other unpainted science id. The rejected finds list is not deleted from the inventory.

Prompt `d1f0bb5136bdf9be2af219bc945d6c32c842d10cda657b4b891e072345ca88ed`. Reference for a future paint: the faculty crop only, plus the hall crops above as the proof that no door exists. Do not generate from this prompt until a reviewed hall opening exists.
