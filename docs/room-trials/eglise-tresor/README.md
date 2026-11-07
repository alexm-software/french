# Treasury pilot — design proposal, not a painting

Status: **generated and rejected.** See `RESULT.md`. Nothing in `content/v2/eglise`, `village/eglise`, or `village/sw.js` changes here.

Base: `main` `331ca5a5` (`village-v52`). Live room: 12 words, 5 verbs, doors to `choeur` and `salle`, no zoom. Dialogue `V_eglise_tresor_01` ("Le grand nettoyage du trésor") already exists.

Inspected painting: `village/eglise/tresor.jpg`
`15ff7e7687998dce31e54f606aa6d0905080dab12cfa75430afac425bdf56501`

## What the pixels show

The November audit's seven "box far from planned x" notes compared hotspots with the old manifest. They were not pixel proof. Crops of the live hotspots show a different set of problems:

- Beret colors are already right in the paint: red on culpabiliser, prôner, sanctifier, and consacrer (`-er`); green on convertir (`-ir`). The hooks never name the color. That was a text gap.
- `retable` hotspot is the right-hand flower panels only. The restorer and ladder sit outside it. The altarpiece itself is centered, so the masculine object is not clearly right of 55%. The hotspot was parked on the right panels.
- `consacrer` hotspot is an 80px-wide strip of the mime's back. The red beret, face, cloth, and polishing action are outside it. The ambo's own hotspot is the lectern body.
- `eucharistique` hotspot is the banner. The embroiderer is outside it.
- `missel` hotspot is the book and the hands. The binder's head is outside it.
- `culpabiliser` hotspot is the face. The plaster angel is not in it. The angel stands upright beside the thumbs-up mime, so the dialogue line about knocking it over is not what is painted.
- `prôner` hotspot contains the thumbs-up mime and that standing angel. "PRO YAY" is a gesture, and "yay" is the wrong vowel for `proh-NAY`.
- `patène`, `custode`, `convertir`, `ambon`, and `ciboire` hotspots contain their main objects. Convertir's green beret and crate-shelf are inside the box. No two hotspots overlap.

Door match fails both ways:

- Treasury left door is oak, with organ pipes in the opening. `choeur.jpg` does have organ pipes, so that glimpse is a real choir element. The choir's door back to the treasury shows a gold shrine and a piano, which is not this room, and the door leaf does not match.
- Treasury right door is blue and opens onto people at a table. The parish hall's door back is a brown studded oak door. Its glimpse is a parrot and a notice, not this treasury. `salle.jpg` is the bread-and-chalice poster, the candle banner, and the lesson tables.

## Inventory kept

All 12 live words stay. The room is over `room_target` 10 and under `room_max` 15. It has no zoom. Splitting it would invent one. Five verbs in twelve words stay, because each one acts in the restoration. That is not a canonical cap.

| Word | Sense kept | Side | Beret | Cue in this proposal |
|---|---|---|---|---|
| patène | paten; empty plate, Host not depicted | feminine left | | pat + wooden ten-pin |
| custode | pyx for the sick | feminine left | | cues stowed (form) |
| culpabiliser | feel guilty; also guilt-trip | any | red -er | partial CULPABLE (form) |
| prôner | extol; also recommend | any | red -er | pro-neigh (form) |
| convertir | convert; also bring around | any | green -ir | tear a slat, crate becomes a shelf |
| sanctifier | make holy | any | red -er | sanctify; halo ring beside the king |
| retable | altarpiece | masculine right | | re-table, whole piece on the right wall |
| consacrer | devote; also consecrate | any | red -er | consecrate the morning to the ambo |
| ambon | reading stand | masculine right | | hambone (form) |
| eucharistique | eucharistic | center | | banner of wheat, grapes, chalice, teak hoop |
| ciboire | lidded cup | masculine right | | see boar |
| missel | Mass book | masculine right | | me, cell (form) |

`HOOK_FORM.tsv` is the editable sheet for the five cues that are partial or that need a reverence check. Do not paint those five until the sheet is accepted or rewritten. The other seven are the working proposal.

Preserved from the live room: the vaulted stone treasury, morning daylight, the paten being dried, the pyx being closed, the crate becoming a shelf, the flower altarpiece, the ambo, the wheat-and-grape banner, the lidded ciborium, the red missal, and the cast Inès, Mme Lefort, Père Antoine, Monsieur Verbe. Dropped as false hooks: the sleeping cat, the upright angel used as a knockdown, the centered altarpiece, the blue door.

The king statue stays a generic crowned wooden figure with no glow, no wounds, and no sacred monogram. The mime gilds a separate brass ring and does not touch the statue. The paten stays empty. No children stand in the treasury. The ham bone, toy boar, cues, golf club, toy horse, and honeycomb sit beside the sacred objects and do not touch them.

## Envelopes

`envelopes.png` is the plan, not art. Boxes do not overlap, stay inside the 6% margin, and clear the two door rectangles `[45,48,140,250]` and `[1165,48,100,260]`. Feminine centers are 22% and 36%. Masculine centers are 69% to 86%. The adjective is at 51%. `plan_check.py` reports 0 failures and the expected warning that 12 exceeds target 10. Simulated labels do not overlap. `grid_check` on these envelopes passes.

`sanctifier` (170×231, mime plus small statue plus stand) and `ciboire` (130×190, jeweler plus cup plus toy boar) are the tight groups. If a future candidate clips either one, recompose. Do not slide the hotspot off the figure.

## Prompt

`prompt.txt` is the compiled prompt (`build_prompt.py --check` matches the manifest). Attach `tresor.jpg`, `choeur.jpg`, and `salle.jpg`. One composition candidate, then at most one focused repair. A third failure means change this spec.

When the painting is accepted, update the dialogue in the same change. These live lines will be false: the knocked angel, the halo painted on the king, and the thumbs-up. The green-beret crate line can stay if the torn slat is added. Choir and parish-hall paint-backs that fix their return glimpses belong to the next church stage, not to this pilot.

## Hashes

See `HASHES.txt`.
