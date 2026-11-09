# Military museum completion — 2026-11-08

Base: `fc456bdebd636475cc59887f845129b021bc28c9` (merged PR 277).

Completes the remaining 33 words in B16_caserne. The four existing teaching galleries and vestibule keep their accepted paintings. Six new integrated paintings, full-object fitted hotspots, crop cards and six natural bilingual dialogues complete all 58 assigned military words.

| New gallery | Source inventory | Words |
| --- | --- | --- |
| La vie de caserne | R_military_02 | caserne, permission, major, adjudant, sergent, uniforme |
| Les officiers et la marine | R_military_02 | marine, commandement, lieutenant, commandant, enseigne |
| Les corps et les traditions | R_military_02 | cavalerie, maréchal, régiment, brigadier, cadet |
| Comprendre les conflits | R_military_03 | attaque, alliance, tranchée, conflit, bataillon, abandon |
| Les conséquences et la mémoire | R_military_03 | révolte, défaite, destruction, combattant, tir |
| Les archives et les distinctions | R_military_03_z1 | légion, élite, invasion, atteinte, attentat, gagnant |

The planned generic clerk-desk zoom was never built. Its six IDs now belong to a full archival gallery, and its source room is explicitly changed from zoom to full room. No parent/zoom painting pair is claimed. Three five-word galleries are deliberate: the masculine rank inventory needs room on the right for complete exhibits, and the memorial room groups five connected interpretation terms without unrelated filler.

## Visitor route

Vestibule → entrance → existing uniforms → service → officers/navy → formations → conflicts → consequences → archives → existing far hall → recruitment → vestibule → town square. The explicit one-way interpretation circuit uses a visible limestone arch and pale continuous floor at every forward transition; arrival is behind the visitor. Back and Hub retain their existing shortcuts.

## Meanings and content

Military permission means authorized leave. French major is a senior NCO, distinct from English major; brigadier is the cavalry equivalent of corporal, distinct from English brigadier general. Masculine enseigne is a naval officer, distinct from feminine shop sign. Commandant is interpreted by context (army rank or naval commanding officer). Maréchal de France is a dignity, not a current rank. Abandon means leaving a position here, not automatically formal surrender. Atteinte is contextual harm/infringement, not a synonym for every attaque or attentat. Illustrative museum costumes do not claim to reproduce precise rank insignia; the cards explain the roles.

Sensitive terms use blank text-only plaques. Trench, cavalry and unit models have no combat. Three mounted models and six figures in each unit model represent units, not their actual personnel strength. Plain depiction replaces weak inherited puns. The legion standard is visibly attached to the wall by two iron collars. Painting is generated as integrated scenes; JPEG normalization to 1280×720 and card crops are the only local image processing.

Sources for sense review: [French Army grades](https://www.defense.gouv.fr/terre/grades-larmee-terre), [Army grades and distinctions](https://www.defense.gouv.fr/sites/default/files/terre/Poster%20grades%20arme%CC%81e%20de%20Terre.pdf), [CNRTL permission](https://www.cnrtl.fr/definition/permission), [CNRTL atteinte](https://www.cnrtl.fr/definition/atteinte). Definitions, notes and dialogue are authored paraphrases, not copied source passages.

## Evidence and release

- Six manifests and compiled prompts pass the planning compiler. Candidate corrections were local uniform clearance, portrait/display clearance, officer-group recomposition, full-model framing, removing unintended visitors, and supporting the legion standard on the wall.
- Six image/manifest/data prechecks pass, with no OCR flags or geometry failures. The documented five-item density warnings remain informational.
- Independent final review in `independent-review.md` pins exact image hashes and covers every item, human/animal at 2×, counts, final geometry, repair collateral changes and all six dialogues.
- `check_v2.py caserne --strict --placement` passes: 58 words. All 657 currently placed site dialogues pass after the concurrent science merge.
- `unbuilt.py --building B16_caserne`: 58/58 at destination, 0 elsewhere, 0 absent.
- Whole-site painted reachability: 723 reachable, 723 returnable, zero failures. Museum one-way edges are intentional.
- Formal walkthrough: 13 places including map hubs, 11 passages pass. The covering walk returns outside.
- All 18 workflow regression cases, copyright and skill-path checks pass. Cache advances the concurrent main v55 → v56.
- Browser interaction is not claimed; the executor's Chromium socket limitation remains. Complete-repository CI is required before merge because the recovered checkout lacks unrelated image files and seven newly added science-test fixtures. Those seven tests cannot run locally; they are not claimed as passed.

Integration base: `28a04109c12489b21ab5633336b88e2147a9460f`. Preserves the concurrently merged science faculty and regenerates the shared index/dialogue registry from the combined payloads.

User request: “finish out the military sections. what parts are left there?” No other worker’s rooms or source word assignments are changed.
