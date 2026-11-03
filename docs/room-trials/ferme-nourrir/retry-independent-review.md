# Farm final candidate — independent review

**PASS for current artwork and proposed item-envelope geometry: feeding anatomy, real calf masculine placement, donkey/horse clearance, scene preservation and stump continuity.** **UI/release acceptance remains pending** because labels, hotspots and runtime navigation have not yet been fitted or tested. This is independent validation, not publishing approval or an assertion that every inherited hook detail has been improved.

Reviewer: independent `farm_review` agent, 2026-11-03. Actual candidate inspected: `generated_images/exec-ec689970-32cf-4dfb-83ba-33caf7fd3f98.png` (1672×941), SHA-256 `9ffbb99bb99657e4d587e7ecd788a042866fd5e97f39664951144f9cc002b485`.

Compared against `farm-input/ferme.jpg` (SHA-256 `7d50103caeac0ced0a077b4d7691ec8a45a487f2b4ce8cb7078d3ff70c1aca85`) and unchanged `farm-input/souche.jpg` (`9df5518ee2a21a28512bf7646fe8842c090a4a445dec4d357288b6238192efe1`). Applied the release-gates skill and item/space/scene references already read, plus current room data/layout and retry manifest. Re-inspected actual final full scene and 2× detail crops of left animals/people and chickens, both riders, stable group, stump figures, feeding group, calf group, shepherd/dog. Earlier verdicts were not reused as pixel evidence.

## Suggested complete character/prop envelopes

Approximate manually measured `[x,y,width,height]` in normalized **1280×720** coordinates; allow a few pixels of fitting tolerance after normalization. These are starting envelopes for actual overlay fitting, not measured rendered-label rectangles. Supporting ground, pasture and architecture are contextual rather than whole-object requirements; the berger envelope includes the entire shepherd, dog, burger and crook with visible supporting hay, not the whole bale.

| ID | Suggested box | Center x | Band |
|---|---:|---:|---|
| fr_corne_noun | [45,207,133,105] | 8.7% | F pass |
| fr_mule_noun | [118,315,292,180] | 20.6% | F pass |
| fr_cavalier_noun | [754,168,116,121] | 63.4% | M pass |
| fr_ane_noun | [885,160,115,130] | 73.6% | M pass |
| fr_taureau_noun | [827,306,154,125] | 70.6% | M pass |
| fr_cheval_noun | [1044,275,224,216] | 90.3% | M pass |
| fr_berger_noun | [842,442,184,207] | 73.0% | M pass |
| fr_veau_noun | [611,494,208,155] | 55.9% | M pass |
| fr_nourrir_verb | [256,505,181,145] | 27.1% | Verb unrestricted |

Explicitly computed all 36 unordered item-box pairs with positive-area rectangle intersection: **zero intersections**. Computed fields hit `[650,160,95,65]` against all nine item boxes: **zero intersections**. Prior candidate rectangles did have âne/cheval and cheval/berger intersections; actual donkey/horse recomposition in this candidate fixes those pairs. The earlier visual-only nonoverlap claim was incorrect and is superseded by this explicit computation. The calf center has limited spare room above the >55% boundary: retain its actual left farmer and right calf; do not enlarge disproportionately to the left. One tight feeding box includes beret, head, both arms/hands, bottle, both knees/feet and entire lamb. Its upper edge is separated from the mule group's bottom. Donkey feet now sit above the bull horns with clear ground between their envelopes.

If the entire supporting hay bale is treated as part of berger's hotspot, its leftmost straw reaches approximately x810 and competes with the calf's right extent near x819. Do not use a bale-wide rectangular hotspot that overlaps the calf; the proposed berger box correctly retains all its characters and held hook props with enough hay to show the seat. No underlying artwork is hidden or altered by this recommendation.

## Per-hook and anatomy result

- **corne:** recognizable rhino horn surrounded by corn. Visible head/face and forelegs normal; rear body/limbs naturally hidden by stalks. No new regression.
- **mule:** four planted legs; carrot-offering farmer has two attached arms/hands and two legs; both carrot bunches and baskets retained. Whole group now clears feeding group.
- **cavalier:** galloping brown pony has four plausible legs; rider's raised arm and rein arm attach normally. Feathered hat/blue clothing preserved. Existing double-hat gag remains (hat worn and another raised); existing blue clothing reads more like a trailing coat than a clear separate cape. These are inherited hook-detail limitations, not repaired by this edit; don't claim the art literally improves those details.
- **âne:** feather-hatted green-clad boy, donkey and basket retained. Four donkey legs and normal head/ears, plausible riding pose and attached hands. Feet no longer collide with bull envelope.
- **taureau:** horned bull lies among daisies holding an open star-marked book. Visible limbs/holding hoof plausible; the anthropomorphic reading action is its named hook. Book still carries a conspicuous single star rather than many stars, an inherited limitation.
- **cheval:** four separate horse legs, attached head/tail, normally posed helper with two legs and plausible two-arm arrangement (far arm partly obscured). Stable/coaxing/reins remain readable.
- **berger:** two attached arms/hands, burger and crook, plausible seated legs, white dog with normal visible limbs and naturally obscured far hind leg. Hay supports both figures. Sharing scene remains legible.
- **veau:** farmer's two arms/two hands and crouched legs trace correctly. Calf has four anatomically plausible legs, with one partly occluded; wobbly stance/motion marks and farmer's open-mouthed reaction remain. Actual full-group center now passes >55%.
- **nourrir:** adult white-faced striped mime with green beret; one attached arm/hand holds the bottle, the other clearly rests on own knee. Bottle nipple visibly touches lamb mouth. Lamb has four separate readable legs. No disconnected glove, extra limb or mirror. Manifest should describe free hand on knee (parent reports this update completed).

All inspected background chickens and the stump's three herd cattle, two baton children and plowing ox have plausible anatomy at available detail; no clear missing/extra limb or merged body found. Natural occlusions were not counted as missing limbs. No stray additional mime or lamb appeared.

## Scene, continuity and routes

The final painting remains one layered farm courtyard with animals being tended, arriving riders, resting shepherd, central stump and red barn; figures sit at varied depths and scales, with no pasted seams or garbled writing. The feeding group is grounded at human scale and linked to the nearby calf-care action. Original eight main word identities and prominent props remain.

Parent/child **passes**: teapot in left shelf, saddle/stand beside it, exactly three cattle behind, two children with one relay baton at right, tan ox/plow at front-right. Materials, orientation, arrangement, light and miniature-versus-close-up identity agree. No stray ponies, lamb or sign on stump.

All five physical passage landmarks remain recognizable: red barn doorway, white paddock gate, wooden field gate, vine arch/path and lower-left white outside gate. New feeding and moved calf groups do not block them. Central stump remains recognizable as the zoom locus. Current source retains four room routes plus zoom and outside/Back convention; no browser walk or reciprocal room inspection was performed in this task.

Before integration/release: fit actual item and zoom hotspots, then inspect every crop/label/control overlay at supported viewports. Keep label rectangles clear of the adjacent calf/berger groups and the stump zoom controls. Run canonical placement/cache/release checks and runtime route walk. This review supplies visual evidence for the changed artwork only; it cannot establish those pending UI checks.

## Geometry follow-up

The rendered contact sheet `farm-input/final-review/ferme_ferme_sheetfinal.jpg` was inspected, along with a 4× normalized crop of the fields gate. Fields hit `[650,160,95,65]` truthfully targets the left wooden gate leaf/entrance and clears cavalier x754 by 9 px. It includes adjacent white fence at the left; a tighter leaf-only option is approximately `[675,163,70,59]`. Do not extend the hit right into the rider. The prior two item-box collisions are now cleared by actual group recomposition and the current computed boxes. This latest artwork was independently re-reviewed at full scene and 2× on changed donkey/horse and all protected figures/stump. The proposed current boxes pass pairwise computation; fitted labels/hotspots still require a fresh final review.

Current 2× detail evidence: `farm-input/spaced-riders-detail.png`, `spaced-stable-detail.png`, `spaced-calf-detail.png`, `spaced-mime-detail.png`, `spaced-stump-detail.png`, `spaced-shepherd-detail.png`, `spaced-left-detail.png`. These crops were actually opened with view_image, not merely generated. No new anatomy, hook identity, passage or parent/child regression found. Labels/zoom-object control fitting and all-control collision checks remain pending.

## Final integrated JPEG and built-data acceptance

**PASS: final JPEG, nine item crops, fitted static labels/hotspot rectangles, all four doors, outside gate and parent/child continuity.** This supersedes the earlier provisional geometry wording above for this exact integrated build. Browser runtime control behavior remains with the parent reviewer's scoped browser check; no publishing authorization is implied.

Actually opened with view_image:

- `audit-source/village/ferme/ferme.jpg`, final 1280×720 integrated JPEG.
- `farm-input/final-review/ferme_ferme_sheetspacing.jpg`, actual built-data contact sheet with labels, item boxes, passage crops and all nine word crops.
- `farm-input/final-review/ferme__souche.jpg`, actual final parent crop beside unchanged child.

Final JPEG SHA-256: `607f92ba0e51c3d766be8c7445af5009abef4d6754ab69a994472c0f2083f296`.
Child JPEG SHA-256: `9df5518ee2a21a28512bf7646fe8842c090a4a445dec4d357288b6238192efe1`.

Read actual final `village/data/ferme.js`. It contains the nine measured rectangles above, with âne `[885,160,115,130]`, cheval `[1044,275,224,216]` and fields gate `[650,160,95,65]`. Independently computed positive-area intersections using its `boxPx`, `labelPx`, door `hit` and `mapExit.boxPx` values:

| Pair category | Result |
|---|---|
| 36 item–item pairs | 0 intersections |
| 36 label–label pairs | 0 intersections |
| Each label vs every other item's box | 0 intersections |
| Nine items vs four doors plus outside gate | 0 intersections |
| Nine labels vs four doors plus outside gate | 0 intersections |

Viewed every word crop against its printed hook and full-scene envelope. Rhino/corn; mule/carrot farmer/baskets; pony/rider/hat; donkey/boy/basket; bull/book/daisies; horse/helper; shepherd/crook/burger/dog; reacting farmer/calf; mime/bottle/lamb are all legible and framed by their actual item rectangles. Some square *presentation tiles* intentionally show adjacent context beyond the tight rectangle; that is not a claim that the hotspot contains the neighboring figure. The feeding group is one complete compact crop, with clearly attached bottle hand and knee-resting free hand. The calf's complete farmer/animal rectangle remains truthfully centered at 55.8594%. No JPEG conversion regression observed.

The noun/verb plates are readable and visibly associated with the correct groups on the static contact sheet. Mule and bull plates sit within their own envelopes on clear painted regions; remaining plates clear adjacent figures and routes. Horse label remains separated from shepherd and right scene edge. Calf/shepherd labels remain separated despite their shared baseline. No new ambiguous label assignment found.

Each physical route crop is truthful: red barn doorway with poultry → basse-cour; white cross-braced paddock gate → manège; narrower wooden grain-field gate → champs; grape-covered arch with continuation of the vineyard path → coteau; lower-left white courtyard gate → La vallée. Original route identities remain. The narrower fields crop removes the cavalier from that control's rectangle.

The zoom comparison passes again using the final JPEG: the actual central stump carries the same five hook groups and counts as the unchanged child, in matching arrangement/materials/light. Its broad `obj` rectangle is context for the parent crop and includes surrounding scenery; this report's item/control collision computation does not treat that whole crop rectangle as a clickable item box. The actual zoom badge and its hover/focus control geometry must be confirmed by the parent's runtime check. No further artwork correction is requested by this independent review.
