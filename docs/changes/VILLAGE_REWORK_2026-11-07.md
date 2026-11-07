# Village rework — stage 1 checkpoint (2026-11-07)

Authorized scope, in order: (1) treasury pilot, (2) remaining church and other-faiths repairs, (3) fantasy verbs into themed rooms, (4) museum split, (5) overview and navigation. This checkpoint is stage 1 only: reconcile main, write the plan, prepare the treasury design. No painting, no live move, no merge, no deploy.

## Current base

`main` `331ca5a5767376da85954b41c661cfcd67bf19f9`, cache `village-v52`.

The 5 Nov snapshot `2d2985a5` was `village-v49`. Four commits have landed since:

| Commit | Cache | What changed |
|---|---|---|
| `fcd94493` #267 | v49 | A planned word counts as built only in its destination building. `unbuilt.py` gained `elsewhere` vs `absent`. Skill lines that said "live IDs anywhere" now say a donor-building copy is not integrated. |
| `b867ec0a` #268 | v50 | Seller moved into the farm courtyard. |
| `545084cb` #269 | v51 | coucher, dormir, planter, cultiver, germer moved into their rooms. |
| `331ca5a5` #270 | v52 | habiller, laver, offrir, ranger, brûler, inspirer, respirer, coudre, raser, tailler moved into their rooms. |

PRs 259–266 were already in `2d2985a5`. The canonical workflow is `skills/`, `tools/README.md`, and `skills/limits.json`. PR #265 ("Add a slim source index for room lookups") is still **open**. Main does not have that index. `room_context.py --compact` works without it.

Other open PR: #206, dialogue-review notes from 31 Oct. Not touched.

Cloud agents seen from this run, all idle except this one: seller-walkthrough review, maison-verb recheck, and the unbuilt-destination agent whose PR #267 already merged. No other agent is on the church or the treasury. Farm, maison, and that branch were not edited.

## Stage 1 — treasury

Design: `docs/room-trials/eglise-tresor/`. The five open hooks were resolved by the agent and recorded in `HOOK_FORM.tsv` (not a user signature). Ham bone was dropped. Four `GenerateImage` candidates were reviewed and rejected. See `RESULT.md`. Live treasury, choir, and parish-hall paintings are unchanged. Do not start stage 2 until a treasury candidate passes placement, counts, striped-shirt mimes, and both door glimpses.

## Stage 2 — church and faiths, after the treasury is accepted

Recounted on this base. Do not repaint a room just because the November data audit flagged it. Inspect pixels first, the way the treasury was inspected.

| Building | Rooms | Notes from live layout |
|---|---|---|
| église | 16 | treasury is the pilot. `armoire` is a doorless zoom of the sacristy. |
| cathédrale | 2 | main room has no doors. `credence` is a doorless zoom. |
| abbaye | 6 | two cloister zooms are doorless. `prophète` is still in the scriptorium. |
| presbytère | 3 | `catechism` is at the hard cap of 15. |
| concorde | 6 | courtyard plus five prayer rooms, doors back to the courtyard. |

Inherited door debt from the treasury: `choeur`'s return glimpse and `salle`'s return door get their paint-backs in this stage, with the treasury's oak arch and brown studded door as the contract.

One room at a time. Same budget as the pilot: hooks and envelopes first, one candidate, one repair, then stop.

## Stage 3 — fantasy verbs

Verified on this base. `cour_chateau` is 9 verbs and `grande_salle` is 8 verbs. The four story rooms still have none:

| Room | Now | Proposed | Verbs to add |
|---|---|---|---|
| tour_sorcier | 8 | 12 | enchanter, invoquer, prédire, maudire |
| bal_costume | 7 | 11 | tromper, ruser, trahir, douer |
| vallee_geants | 6 | 12 | venger, redevenir, destiner, advenir, entrevoir, pressentir |
| contes | 9 | 12 | hanter, pervertir, matérialiser |

That accounts for all 17. Every room stays at or under 12, inside the hard cap of 15. The old sheet that filled the tower to 15 is not followed.

`vallee_geants` door hit `[8,380,240,160]` still opens `cour_chateau`, which opens `grande_salle`. Do not delete those rooms or that door until the 17 words, cards, and dialogue have new homes and the valley painting shows a castle glimpse instead of a passage. venger, maudire, trahir, and pervertir stay non-violent: inanimate props only, no one hurt.

## Stage 4 — museum split

Recounted: still 36 rooms. Counts match the earlier inventory, including `mots_delits` 15 and `mots_deuil` 15. Re-count again before moving anything.

- Beaux-Arts: musee, atelier, peinture, sculpture, vernissage, couleurs, lumières, optique. Move atelier's illness and injury words to the hospital only when that corridor is ready.
- Historical château, separate from the contes fairy-tale castle: chateau, chevaliers, armes, noblesse, trone, plus a council room from assemblée and chartes, and archives from dirigeants.
- Guild hall: guildes, on the market square.
- Municipal library: enquete, mysteres, caracteres. Sensitive crime and death entries stay plaque-only. Justice gets the non-sensitive crime plaques; the hospital gets illness and death plaques.
- Maison des Sens, in the park: sens, sons, voix, parfums, saveurs, toucher, matieres, labo, emotions, jardin.
- médecine to the hospital as a history corridor. fete, classe, and cantine wait for a sort into the school buildings.

Donor paintings stay until the replacement is accepted. Move word, doors, cards, dialogue, source, and live layout in one change. Do not delete local files to save disk.

## Stage 5 — overview

After the new buildings exist: Colline du Château, Bibliothèque, Maison des Sens on the park, guild hall on the market, and a smaller Beaux-Arts footprint. One map painting from a signed sector sketch, then reachability. Not in this stage.

## Budget

This stage: 0 images. Next stage, only after the hook sheet is settled: one treasury candidate and at most one repair. Do not start stage 2 in that same run.

## Skill conflicts, not edited

Parent edits global skills. No skill file changes in this stage.

- `skills/memory-palace-builder/reference/sensitive-content.md` says whimsy never touches a sacred object. The 7 Nov instruction allows an everyday sound-alike beside one, without mockery. The treasury prompt uses beside-and-not-touching. Suggested tightening of that existing sentence: the sound-alike may sit beside the sacred object and may not be attached to it, parody it, or replace it.
- `skills/language-memory-palace/reference/hooks.md` still says a real cognate may stay plain, and also says a cognate needs a twist when the sound differs. This design follows the stricter reading: a close sound can stay, with the French stress noted; a look-alike that sounds different gets a cue or a form row.

## Tests this stage

`plan_check.py` on the treasury manifest: 0 fail, 1 warn (12 over target 10). `build_prompt.py --check`: prompt matches. Envelope script: no overlaps, margins held, `grid_check` passed. Live painting, hotspot crops, 2× quadrants, and both door directions were inspected. No browser pass, no new image, no independent review of a new painting.
