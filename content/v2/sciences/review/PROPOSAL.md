# Revised composition — no image

Same eight words. Same hooks. Not a generation request.

The stone is one solid dressed block with no hole and no cart. A small wooden pier model leans on its outer face. The mine is the only tunnel, and it stays small. Those two shapes cannot be swapped.

Three pairs, with open floor between the pairs:

- The torn sack spills against the stone. The pier leans on the block.
- The small mine stands on the left. The mineral cluster is on its own stand nearer the middle. They do not share a table.
- The boot stands in its soil tray. The crucible heats on a separate stand farther forward. The crystal and its mouse are high on the right. The pendulum stands in its own frame, clear of the pot.

The only picture to attach is `village/map/university.jpg`. The open doors show this faculty on that map: tan stone, glass roof, telescope. The red-brick lycée on the same map is a different building. Do not attach `village/lycee/lycee.jpg`. Do not attach an empty box diagram.

Planning envelopes, with slack past the lines the candidate missed (45%, 55%, and the 6% edge). They are not a claim about pixels.

| word | envelope | center |
|---|---|---|
| pierre | x 120–320, y 90–260 | 17% |
| mine | x 160–350, y 320–460 | 20% |
| terre | x 120–340, y 500–640 | 18% |
| minéral | x 540–700, y 440–570 | 48% |
| sol | x 800–940, y 200–330 | 68% |
| cristal | x 1030–1170, y 100–280 | 86% |
| creuset | x 800–950, y 480–590 | 68% |
| pendule | x 1050–1170, y 400–630 | 87% |

`plan_check.py --manifest review/proposal.manifest.json` reports 0 fail and 0 warn. That is a plan check. It is not a visual pass.

## What changes in the inputs

The failed call attached a red-brick interior and an empty rectangle map, and described the faculty only in words. The next call attaches the campus map and no other picture, and the compiled prompt now says the doorway's materials come from that attached image. The stone line now says the block has no hole. The mine and the mineral, and the boot and the crucible, are no longer described as sharing one piece of furniture. The envelopes sit about 120 px inside the edges and about 25 points away from the 45% and 55% lines.

## Unresolved risk

The campus map also contains the red-brick lycée, and it is drawn in isometric. The model can still copy that brick or tilt the room into the map's perspective. Slack makes a modest drift survivable. It does not force the model to obey a center. An empty diagram is not being used as that force. A future painting still needs an independent review. This proposal does not authorize one.
