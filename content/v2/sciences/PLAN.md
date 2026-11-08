# Faculté des Sciences — floor note

Base: `main` `bdb6ae97`. Source bins are not room designs. All 136 science words stay in `data/source`. The parked eight-word painting is unchanged. The current hall plan is six words.

The hall painting `d1d59540` is release-ready and integrated. It is not merged and not live. Do not repaint it. Live data still opens the hall from Campus. The planned root is the outdoor Cour des sciences.

## Stop

Work boundary t428u, 8 Nov 2026, 00:07 CST: continue the requested science-room work until that work is done, or until 06:00 CST (12:00 UTC) on 8 Nov 2026, whichever is sooner. Saving this plan is not the end of the 30-room task and is not an early stop. After 06:00 CST, start no new generation, room, investigation, or batch; finish only a clean save already underway. The finds image is rejected. Do not paint `review/plan-next/` until its topology is reviewed. No merge.

## Connections

Planned route: Campus opens the Cour. The Cour's glass doors open the hall. The hall's painted doors return to the Cour. Ordinary-room Back still says Campus. Hub is hidden when a painted door already goes to the Cour. West wing, arcade, and east stair leave the Cour. No second Campus door. The finds picture `080d7f5e` is rejected. The bench is not painted until the Cour is accepted. Master plan: `review/cour/walkthrough.json`.

## Finds candidate, rejected

`080d7f5e` is not an edit base. It is not in the live layout. Its words stay queued. The next plan is `review/plan-next/` and is not for painting.

## Hall plan

`hall` (ground floor, campus return through the glass doors at back center):

| id | sense kept |
|---|---|
| fr_pierre_noun | plain dressed stone. PYEHR is the pronunciation, not a sound-alike. |
| fr_terre_noun | earth in the torn sack on the cart |
| fr_mine_noun | mine model with a tunnel mouth |
| fr_mineral_adj | mineral cluster. The standing geologist holds it in both hands. |
| fr_sol_noun | boot sole in a soil tray, with one worm. No person in this group. |
| fr_cristal_noun | crystal, with one mouse at the base |

## Queued, not removed

| id | next room |
|---|---|
| fr_pendule_noun_m | Forces, with the other force words. Source room `R_physics_02`. Masculine. Unpainted hook: a pendulum in its own frame, one ladybird on the bob. |
| fr_creuset_noun | Smelting, with minerai and filon, inside More rocks. Source `vocab.jsonl` room `R_geology`; `rooms.json` also lists it on `R_geology_z1`. Unpainted hook: an orange pot on a trivet. |

No verb is in the 136 science words. `extraire` and `observer` stay on their own streets.

## Not our rooms

The user reserved these for a ChatGPT sideload (t426u). They are excluded from this build queue: `R_cafe_02`, `R_resto_kitchen_02`, `R_measures_01`, `R_emo_joy_01`.

## Later rooms (not painted, not validated)

One activity each, 6–10 words, concrete before abstract. Add a real door in a later paint; do not cut one into this hall after the fact without repainting the opening.

- More rocks: caillou, volcan, minerai, filon, gisement, prospection, géologue, dureté.
- Shakes and layers: tremblement, séisme, glissement, volcanique, géologique, catastrophe, calcul.
- Forces: force, poussée, impulsion, frappe, onde, gravité, énergie, résistance.
- Light and current: rayon, faisceau, signal, spot, courant, vibration, intensité, mécanique.
- Particles: atome, électron, particule, nickel, physicien, accélération, trajectoire, interférence, relativité, propagation, atomique.
- Bench chemistry: gaz, substance, réaction, pression, oxygène, plomb, soufre, carbone, molécule, chimie.
- Upstairs chemistry: acide, fusion, hormone, synthèse, composant, chimiste, épuration, enrichissement, oxyde, méthane, moléculaire, élément, élémentaire, chimique, laboratoire, labo, explosion.
- Living things: cellule, gène, bactérie, germe, organisme, évolution, création, reproduction, biologique, spécifique, extinction, parasite, biologie, embryon, neurone, écologie, biodiversité, physiologie, clonage, cellulaire, biologiste, émergence.
- Methods, upstairs: the `R_abs_study_02`, `R_abs_study_02_z1`, and `R_abs_study_03` words (recherche through expérimental). They are mostly abstract and wait until a concrete lab is accepted.

Image calls: 37. The hall `d1d59540` is call 35 and is release-ready, not merged. Call 36 `080d7f5e` is rejected. Call 37 is the Cour candidate `4adf12ed`, not integrated. The campus map is unchanged.
