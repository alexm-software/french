# Final checkpoint — blocked

No further image. No new design. No integration. No merge. The room is not complete.

Independent review rejects candidate `d5770a18` globally. Report sha256 `aa1dbc16cc37464d4489d50461c87bf2d23708308628f68d3614469aedccb1a5`.

Stated image calls: 25. Science: 2 fresh paintings, 0 repairs. Ready: 0/30.

## Hashes

| input | sha256 |
|---|---|
| Six-word prompt (288 words, sent verbatim) | `bdd8e378d9614e9a04f680dc456970f5f3bb6cd391a4cd18cf014ab88082775c` |
| Candidate `review/six/candidate.jpg` | `d5770a18452989a2041f325924b3bd20a323fc577b7b0943e4e317af2350af3d` |
| Planning diagram, attachment 1 | `970e90f9a405a4ab79f78f1c0bea2c8472754ce6fc4da9173f5e0a133f159348` |
| Faculty crop, attachment 2 | `e5212a33bc34f13892e042cce5d3e35bfcf31ecf04fc991d90fd7b30f40eb33a` |
| Parent `village/map/university.jpg` | `fd1d0c93ded43ab8173cc372095336aa07a2c58d1f222064c6e74b473ec36d1b` |
| Crop rect on that parent | `[950, 245, 320, 255]`, pixels match |
| Design pack zip | `dd4a2e62cbe76c40d09e1219c4e3e8d16eaa764d1f81055947bb8f789e628bef` |
| Parked eight-word image, unchanged | `0a345ffe2c358edf8c4fc37b6d16c9136930c3bbeb990b276f75d994b232eb88` |

The full campus map, the lycée painting, and the parked candidate were not attached to the six-word call.

## Independent verdict

Passes: faculty doors, path, trees, glass roof, and telescope. Mine center 29%. Minéral center 49%. Sol passes. At 2× the sole tread is visible, tilted onto the soil tray, with the worm. The whole man is x 731–1194, center 75%. Adult anatomy passes. The cart is the sack's support.

Fails:

- Pierre: the stone is a kiln with two openings. The pier was painted as the empty table. That table is the failed pier, not an extra object.
- Terre: the sack's left edge is 44, inside the 77 px margin.
- Cristal: the group reaches x 1275, past 1203. The rodent is on its own stool at x 1181–1269, not at the crystal's base. A cat face at the base makes the cue ambiguous. The whole crystal group overlaps the geologist.

`fr_pendule_noun_m` stays queued for Forces. `fr_creuset_noun` stays queued for smelting with minerai and filon. Neither was removed from source.

## Rule audit

ITEMS already requires the whole recognizable cue and the meaning together. FIGURES already requires the named helper to be recognizable and forbids a confusing extra figure. PLACEMENT already requires the group center, the 6% edge, and one box around the whole helper. Those lines name the pier, the solid stone, and the mouse at the crystal. The painting did not follow them. That is an execution failure. It is not a reason to treat every two-part hook as impossible. No new check was added.

`village/data/sciences.js` does not exist. This checkpoint blocks release on reliable integrated art.
