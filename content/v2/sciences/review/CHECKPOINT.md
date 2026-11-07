# Checkpoint — science hall parked

Independent review: **global FAIL**. The candidate stays parked.

- Image sha256 `0a345ffe2c358edf8c4fc37b6d16c9136930c3bbeb990b276f75d994b232eb88`
- Submitted prompt sha256 `2b6740d39c678d9f3abe45d6f36e124bbdbb2767275e8778ff5bf58096decb86`
- Base `bdb6ae97`. No edit to the painting. No integration. No merge. Source `vocab.jsonl` and `rooms.json` unchanged.
- Image calls stated in total: 24. This science pilot: 1. Repairs: 0. Ready: 0/30.
- PR 272 and PR 273 were not touched.

## Independent measurements

Group center, not a band across the box. Mouse, ladybird, and worm anatomy pass. No local repair fixes the set.

| group | verified |
|---|---|
| pierre | x 19–238, y 300–470. A second mine. No pier and no dressed block. |
| terre | left edge 22, bottom 681 |
| mine | center x 612.5 (48%) |
| minéral | center x 828, inside 30–70% |
| sol | overlaps the crystal and the crucible |
| cristal | right edge 1228 |
| creuset | right edge 1265; overlaps sol and the pendulum |
| pendule | bottom 712 |
| doorway | red brick. The manifest asked for this faculty's tan stone. `village/map/university.jpg` was not attached. |

## Why the inputs did that

Attached files were `village/lycee/lycee.jpg` and `content/v2/sciences/hall-layout.png`. The lycée painting is red brick. The prompt told the doorway to match "this faculty exterior" in words only. The template already said to match the destination's appearance, and it already said a path written in the prompt is not an attachment. The campus map was never in `prompt.refs` and was never attached, so the red-brick style photo supplied the doorway.

The item lines already named a dressed stone plus a pier, and a separate mine. The model painted two tunnels. `FIGURES` already required distinct figures. It did not say that two near-synonym objects must not share a shape.

`PLACEMENT` already requires the group center, the 6% edge, and one non-overlapping box around the whole helper. The empty box sheet and the tight envelopes did not make the model obey them. `composition.md` already says a floor plan is not a painted pass. That part is an execution failure.

## Next

`PROPOSAL.md` is the revised composition. It is not a painting and it is not approval to generate.
