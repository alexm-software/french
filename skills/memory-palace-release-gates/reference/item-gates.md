# Per-item gates (A, E) and item-level blocking gates

Read when reviewing item crops or assets.

## Before painting

- Label budget: builder reference/text-and-labels.md. Adult-item rooms: builder reference/sensitive-content.md. Hook prefixes and openers: builder reference/hooks.md. Write the item manifest first: builder reference/planning.md.
- Any prop that gets operated (a button, lever or tap) is mounted on a machine or panel, with its figure touching it. <!-- G17 -->
- Before repainting a space, read its open rows in the repaint queue; each one must be fixed by the repaint. <!-- G20 -->

## A. Per item: crop review (every drawn item, every time)

Crop each item box AND each exit box out of the final painting, at least 256 px on the long side. Lay them out on labelled sheets of about 12. Under each tile, print the headword, the hook's sound-alike and the hook scene, taken from the package's own hook rows merged over current data (or the exit's destination). A sheet without hook text can only check gates 2-4 and 6, and gate 1 then stays open. Look at every crop and confirm: <!-- G23 -->

1. **Hook match.** The figure shows exactly what the hook scene says: the same character, gender, action, props and sound-clue object. Check the sound-clue object first, because it is the part most often missing (no viola for violet, no cigar or toy car for le cigare, no plump deer for arrondir). A whole room can drift: after one repaint, 6 of 12 hooks described a different picture. When a room is repainted, every hook in it is rewritten from the new crop in the same pass, or the art is redone. Never ship a hook that describes something else or is still the template line written before painting. A reflexive verb (se dépêcher, se promener...) shows a mirror inside its own box, and the hook mentions it; check it per item on the crop and with a scripted pre-check over the specs (one batch painted 6 reflexives with no mirror, while all 45 live ones had one). <!-- G24 -->
2. **Anatomy.** Count arms, hands, legs and fingers on every figure. Watch for merged hands, missing limbs, extra limbs and melted faces (users found a juggler with one arm). Disembodied or severed body parts used as props also fail (a giant foot on a table for "toe"); show the body part on a whole figure or a toy. <!-- G25 -->
3. **Clean rendering.** Nothing garbled, smeared, half-formed or mashed together. Regenerate rather than accept a bad render. <!-- G26 -->
4. **Grounded props, no strays.** Every prop is held by someone, mounted on something or resting on a surface. No floating buttons, signs or objects (users found a reset button attached to nothing). Thrown or flying things count as grounded only when the motion is unmistakable: the object is just leaving the hand or has motion lines, or the creature visibly has wings and is mid-flap. Anything else hanging in the air is a floating prop. A figure or prop that stands for no word fails too (a pipe, an ashtray, a hose with no vacuum), and so does part of a neighbour's figure poking into a crop so it reads as a floating object. A word's figure may interact with nearby people (looking at, handing to, helping, reacting to them) as part of the room's shared situation; a helper the hook names sits inside the item's box, next to the item, and inside a box any figure the hook doesn't name still fails. Unlabelled background or companion figures outside every box are fine as natural scenery when they are clearly not a word picture: smaller or further back, taking part in the shared situation, doing no gag of their own and holding no prominent prop. Still a stray: an unlabelled person or animal doing its own prominent gag or carrying a hook-like prop so it reads as an unlabelled word (a raven reselling spoons between two unmentioned men; a dog chasing the dépêcher peach), and a helper bigger than the item, which reads as an unlabelled word. <!-- G27 -->
5. **Hook strength.** The sound-alike comes from the real pronunciation (read the respelling aloud). It is an English word or phrase, never the French word said again and never the meaning, and the scene is vivid and specific. Mechanical pre-screen before the eye pass: flag every "Same as English"/"Like English" hook with no twist that's rated strong, every hook rated weak, every sound-alike equal to the gloss, every meta or placement opener, and every opening phrase shared by more than 5 hooks. Re-rate honestly: a flat cognate line is "ok" at best. <!-- G28 -->
6. **Content, in the art AND the hook text.** Adult items (alcohol, tobacco) appear only as objects, such as closed bottles and untouched packs. Nobody drinks or smokes, and hook text never says gulping, sipping or smoking either. No child is near them, meaning not at the same table, counter group, zone or next table, and no child or child-looking worker appears anywhere in a room whose words include alcohol. No romance cue involving a child (a boy giving a woman a rose, children kissing, love hearts between kids), and no child in an unsafe pose (outside a balcony railing, on a roof edge, near knives or medicine); show an adult or change the scene. Words about adult states (such as l'ivresse) may be drawn through a gentle, innocent stand-in like dizzy grape-stomping, never through drinking. Truly mature words are wall text only. <!-- G29 -->

## E. Composited scenes: per-word assets

Mnemonic pictures are now made as separate assets, independent of the room, then placed into an empty painted room. That allows two levels of checks. Both must pass, and the checker looks at the images, not just the json. <!-- G68 -->

**E. Per asset (before it may be placed).** Check every word's asset on its own, at full size: <!-- G70 -->
- **Mnemonic represented:** the asset shows the hook's sound-alike object AND the meaning, as the hook text describes. If the hook is a spelling link, the card says so. A verb asset shows the verb character with the right colour code (and the mirror if reflexive). Rewrite the hook or regenerate until they match. <!-- G71 -->
- **One word only:** nothing in the asset stands for another word or an unnamed extra figure. <!-- G72 -->
- **Clean render and anatomy:** gates 2 and 3 apply (limbs, hands, faces, no garbled parts, no stray text, symbols or currency signs). <!-- G73 -->
- **Style match:** the same line weight, saturation and cartoon level as the room's style family, lit from the same direction as the target room. <!-- G74 -->
- **Clean cutout:** a transparent background, no white fringe or halo, no cut-off parts, and the base (feet, bottom edge) intact so it can rest on a surface. <!-- G75 -->
- **Perspective fits its spot:** the asset is drawn at the angle of the surface it will sit on (an item for a counter follows the counter's angle). Note the intended surface in the asset's metadata. <!-- G76 -->
- **Card-ready:** the same file reads well alone on the word card. <!-- G77 -->

## Item-level blocking gates (rounds 4-6)

- **Every hook element is visible.** The sound-alike creature or object is drawn in the item's own picture. (Once, the boire picture had no boar.) <!-- G104 -->
- Hook gate: every mnemonic is a visible sound-alike of the target word, acted out ON or touching the item. Fail if the hook is a random prop, sits far from the item, needs another target-language word to work (e.g. a trap for piéger), or uses the target language itself. <!-- G115 -->
- Animal gate: no anthropomorphic animals unless the animal is the hook. Otherwise use an ordinary person carrying the hook. <!-- G116 -->
- Anatomy gate: count the arms, legs, feet and limbs on every figure, check faces look normal, and check for duplicated objects (e.g. two teapots or four cups for two people). Any oddity fails. <!-- G117 -->
