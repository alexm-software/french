# Rock hall candidate — parked

Status: **independent review global FAIL. Parked.** No further generation, no edit to the painting, no integration, no merge. Do not build `village/data/sciences.js`.

The independent measurements in `CHECKPOINT.md` supersede the estimates below.

Base: `main` `bdb6ae97`. Branch image: `review/candidate.jpg`.
Prompt sha256 `2b6740d39c678d9f3abe45d6f36e124bbdbb2767275e8778ff5bf58096decb86`.
Image sha256 `0a345ffe2c358edf8c4fc37b6d16c9136930c3bbeb990b276f75d994b232eb88`.

The compiled `prompt_text` in `hall.manifest.json` is the text submitted to GenerateImage. Attached references, in order: `village/lycee/lycee.jpg` (style), `content/v2/sciences/hall-layout.png` (empty placement). `village/map/university.jpg` was not attached.

## What the picture is

Interior walls are pale stone, with a glass roof, telescope gantry, and a blank plaque. No people. The open doorway shows a red-brick building. That is the lycée on the campus map. This faculty on that map is tan stone with a glass roof and a telescope. `village/map/university.jpg` was not attached; `village/lycee/lycee.jpg` was.

The eight objects did not land in the planned envelopes. `overlay-planned.jpg` shows the plan boxes on empty wall and floor while the painted objects sit elsewhere.

## Honest centers (whole item, including the named helper)

| word | painted center | gate |
|---|---|---|
| pierre | 10% | left edge inside the 6% margin; painted as a second mine tunnel, not a stone plus a pier |
| terre | 13% | sack and spilled soil cross the left and bottom 6% margins |
| mine | 48% | feminine center is right of 45% |
| minéral | 66% | inside the 30–70 band |
| sol | 76% | masculine side is fine |
| cristal | 90% | mouse crosses the right 6% margin |
| pendule | 78% | base crosses the bottom 6% margin |
| creuset | 92% | pot crosses the right 6% margin |

Honest rectangles also meet: mineral/sol, sol/cristal, cristal/creuset, pendule/creuset. Numbers are in `measurements.json`.

## Other painted facts

- The campus door is clear. Frame about x=230–460, y=90–420. The path, trees, and a brick building show outside. Nothing stands in the opening.
- Plaque over the door is blank. OCR on the whole frame returns line-noise, not words.
- Mouse: two ears, two eyes, sitting, paws together, one tail. Ladybird: head, spotted wing, legs on the string above the bob. Worm: one body in the soil. No extra limbs found.
- Extra iris on the crystal stand is not a word.
- Flame is small, on the trivet, with nobody near it.
- No Monsieur Verbe. None of the 136 science words is a verb.

## Why this is not a local repair

The tool has no mask. The mine would have to move left of 45%, the sack and the left rock would have to come off the edges, and the left rock would have to stop being a mine. That is a new composition. A second full image would be a blind retry. It was not called.

## What to change before another image

Keep the same eight words and the same hall. In the next plan, make the mine a small model whose whole box center is under 40%, draw pierre as one ashlar block with a pier model leaning on it (no tunnel), and keep every object inside x=100–1180 and y=60–660, with gaps wide enough for the labels. Do not reuse this file as an edit base.
