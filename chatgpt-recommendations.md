# ChatGPT recommendations

Review date: 2026-10-28  
Reviewed revision: `d859bac75c044bf1ac1d58bacf7a20a46b427426`

These are recommendations only. This review did not change the site or skills.
Counts describe the reviewed revision, not necessarily later commits.

## Scope and main finding

Reviewed the current repository, all three memory-palace skills and relevant
references, and sampled the live world map, home district, garage, tool close-up,
campus, lycée entrance hall, and a garage verb card. This was a targeted review,
not a complete visual audit of every room or a full mobile/fullscreen test pass.

The biggest opportunity is to make better use of content already built. The
village has grown substantially, but several learning features described in the
skills have not reached the current viewer.

## Site improvements

| Priority | Finding | Recommended improvement |
|---|---|---|
| High | **711 written conversations exist**, but the current viewer has no dialogue player. No recorded audio files are present. | Expose each room's existing conversations with a transcript, translation toggle, whole-conversation playback, and line replay. Store generated audio separately. |
| High | Only **13 of 357 spaces outside verb streets contain verbs**. | Gradually bring suitable verbs into their natural settings: people repairing, ordering, carrying, and opening. Preserve established locations during a planned migration. |
| High | **67 of 477 spaces exceed 12 items**, reaching 26; the skills say more than 12 fails. | Visually review the densest spaces first. Split crowded scenes into meaningful rooms or close-ups rather than shrinking objects. These counts identify candidates, not proof that every scene is crowded. |
| High | The current viewer lacks the skills' **placement guide and interface-language switch**. | Add a compact guide explaining gender sides, mime/beret conventions, mirrors, and zooms. Connect the existing translation data to the viewer. |
| Medium | Exploration currently leads mainly to opening cards; there is no recall/review flow in the viewer. | Add an optional room-recall mode: hide labels, prompt a word or image, then reveal. Keep practice tied to the room. |
| Medium | Startup probes every registered building by loading its JavaScript. The **74 available building payloads total approximately 4.1 MB**, before images. | Generate a small availability index and load building content only when entered. |
| Medium | Painted exits can be difficult to discover without hovering. The lycée also offers both painted stairs and a room-navigation list. | Choose one consistent navigation convention, with subtle visible exit cues and clear orientation. |
| Medium | The modal declares itself accessible, but the code lacks focus trapping/background isolation. The document language is French while much UI text is English. | Improve keyboard focus handling and language annotations; respect reduced-motion preferences. |

## Skill and workflow improvements

| Priority | Finding | Recommended improvement |
|---|---|---|
| High | **Conflicting art instructions:** the builder prefers separate assets, another paragraph prefers integrated paintings, and v2 documentation requires integrated paintings. | Declare one current approach: separate editable source assets plus a composed room image where useful. Mark older guidance as superseded. This preserves the user's token-saving preference. |
| High | The release-gates references name **six tools/procedure files that are not in the repo**. | Replace those references with actual commands. Clearly distinguish automated checks from human visual judgments. |
| High | The deployment workflow checks only that five files exist. It does not enforce the skills' content/layout gates. | Define a small, reliable set of checks for changed buildings, with a separate periodic whole-site audit. |
| Medium | Rules conflict about breadcrumbs versus Back, room lists, natural painted text, and density targets. | Consolidate each policy into one canonical rule referenced by the other skills. |
| Medium | Audio guidance still specifies browser speech synthesis. | Add a recorded-dialogue workflow covering consistent speaker voices, exact script matching, pronunciation review, timestamps, licensing, and browser-speech fallback. |
| Medium | The root README describes an obsolete café-only site and build process. | Rewrite it around the currently deployed v2 site, authoritative data sources, and actual build/deploy commands. |

## Suggested order

1. Resolve skill contradictions and stale tool references.
2. Connect existing conversations to the live viewer.
3. Add the placement guide.
4. Review verb coverage and crowded rooms.

These changes would improve the learning experience before another large
expansion.

## Evidence and locations

- `data/source/conversations.json`: 722 conversation records; 711 marked
  `written` and 11 marked `premise_only`.
- `content/v2/*/layout.json`: 477 spaces and 3,930 item slots; 357 spaces outside
  verb streets, of which 13 contain a verb item. Counts use item IDs ending in
  `_verb` and building IDs starting with `st_` for verb streets.
- `village/app.js`: `probeAll()` loads registered building payloads;
  `speak()` uses browser speech synthesis. The viewer contains no dialogue,
  quiz, guide, or interface-language-switch implementation. `openCard()` and
  the modal handlers provide initial focus and focus restoration but no focus
  trap or background isolation.
- `village/data/*.js`, excluding `map.js`: 74 building payloads, totaling
  4,133,866 bytes at the reviewed revision.
- `village/index.html`: document language and modal markup.
- `village/style.css`: navigation, card, and animation styles.
- `skills/language-memory-palace/SKILL.md` and
  `skills/language-memory-palace/reference/cards-and-site.md`: conversations,
  audio, guide-related conventions, interface language, and quiz expectations.
- `skills/memory-palace-builder/reference/setup-and-style.md`: competing art
  pipeline instructions, including the separate-assets preference.
- `skills/memory-palace-builder/reference/site-ui.md` and
  `skills/memory-palace-release-gates/reference/process.md`: competing
  navigation guidance.
- `skills/memory-palace-release-gates/SKILL.md`: the stated density limit.
- `skills/memory-palace-release-gates/reference/tools-and-logs.md`: references
  these absent paths:
  - `scripts/qa/release_gates.py`
  - `scripts/qa/package_gates.py`
  - `scripts/qa/label_overlap.py`
  - `scripts/qa/hook_sheets.py`
  - `scripts/qa/label_fix.py`
  - `scripts/qa/hook_image_match.md`
- `.github/workflows/pages.yml`: five file-existence checks before uploading
  the static `village/` directory.
- `README.md`, `village/README.md`, and `content/v2/README.md`: outdated root
  instructions and the current v2 documentation.

No tests were run and no recommendations were implemented as part of this review.

## Follow-up visual audit: rooms that miss the current style

Visual snapshot: `4b4c2ac01b5530ab7b9aa1c922140bd2f023e05c`.
All 477 room/zoom paintings were screened on contact sheets; 28 selected views
were examined at larger size. This is a style/composition audit, not a complete
per-item content, anatomy, hotspot, or mobile validation. The list below contains
23 clear mismatches; it is not a claim that every other room passes.

The current guides call for one coherent everyday situation, small interacting
groups, varied poses and depth, natural neutral colour, and distinct sibling
compositions. The main failures are isolated mnemonic demonstrations and
catalogue-like arrangements, rather than a lack of illustration quality.

| Room or zoom | Observed mismatch |
|---|---|
| `atelier_couleurs/mesures` | A literal lineup of figures across the floor, with a strong amber treatment. |
| `atelier_couleurs/tableau` | Disconnected figures and objects arranged as separate demonstrations. |
| `banque/tableau` | Objects spread along a sideboard like catalogue entries. |
| `banque/tiroir` | Three isolated demonstrations against a flat backdrop, with little scene depth or interaction. |
| `cafe/comptoir` | Two shelves of unrelated mnemonic figures and a strong orange background. |
| `mairie/conseil` | People and animals stacked in display-like tiers instead of participating in a council meeting. |
| `garage/tools` | Two rows of miniature mnemonic props, with little shared workshop activity. |
| `zone_artisanale/bureau` | A desktop filled with isolated miniature scenes against an orange wall. |
| `fontaine/pupitre` | Figurines presented in rows on a desk, with a heavy amber cast. |
| `horloge/semaines` | Separate gags distributed around an orange room instead of one shared situation. |
| `horloge/calendrier` | Symbols and figures arranged as a mnemonic diagram, including a foreground procession. |
| `cirque/clowns` | Evenly distributed figures performing separate demonstrations around a ring. |
| `cirque/menagerie` | Animals and helpers arranged as an inventory inside a pen. |
| `cirque/magie` | Another stage-and-foreground arrangement of isolated gags, repeating the circus composition. |
| `hercule/calme` | Strongmen, animals, and props presented as a compact display, with dark amber lighting. |
| `concours/concours` | A tiered wall of prize objects and figures dominates the room. |
| `concours/rates` | A shelf-like arrangement of separate demonstrations instead of a shared activity. |
| `cabinet/organes` | A dense collection of unrelated figures and anatomical props, with no clear shared situation. |
| `maison/salon` | Many disconnected gags and a dark warm treatment instead of the requested neutral daylight. |
| `st_bricoleurs/reveillematin` | Six mimes doing independent gags in evenly spaced positions. |
| `st_habitudes/chaussons` | Separate mime demonstrations around a courtyard, with little interaction. |
| `st_souffle/coiffeur` | A particularly clear lineup of mimes across the foreground. |
| `st_soupirs/sourire` | Separate mime poses distributed around a garden instead of one shared event. |

Thumbnail-screening candidates requiring closer review before a definite verdict:

| Building | Room keys |
|---|---|
| `hercule` | `arene`, `podium`, `gradins`, `agres`, `coulisses`, `grenier` |
| `concours` | `confitures`, `potager`, `gateaux`, `jury`, `espoirs`, `sante` |
| `banque` | `pupitre`, `comptoir` |
| `mairie` | `tribune` |
| `zone_artisanale` | `etabli`, `comptoir`, `pupitre`, `table` |
| `brocante` | `cabinet`, `casier`, `vitrine` |

Suggested first composition fixes: `cafe/comptoir`, `garage/tools`,
`fontaine/pupitre`, `mairie/conseil`, and the four named verb-street scenes.
The current `ecole/bibliotheque` and `ecole/fete` paintings are closer to the
interacting-group guidance; historical complaints alone should not keep them on
the composition repaint list. A room may pass composition and still fail zoom
continuity, as the next section shows.

Applicable references: builder `reference/composition.md`,
`reference/setup-and-style.md`, and release-gates `reference/space-gates.md`
(natural-scene rule N8; catalogue/liveliness G128; distinct-room G129; colour
and style rules).

## Follow-up visual audit: parent-to-zoom continuity

Visual snapshot: the same `4b4c2ac` revision. All 137 declared zoom links were
screened as parent painting / declared object crop / destination painting.
Twenty-one suspect pairs were examined at larger size. Eighteen clearly change
the scene or its contents. This is a visual comparison of the authored images,
not a browser interaction test of all links.

| Parent -> zoom, within the named building | Observed continuity mismatch |
|---|---|
| `balance/balances -> cageot` | A crate topped with figurines and a long paper becomes a vegetable-framed display table. |
| `balance/grenier -> caisse` | An apple crate gains prominent miniature people, animals, and a circus tent absent from the parent. |
| `banque/commerce -> comptoir` | The man with oranges and accompanying figures are replaced or rearranged; a large woman appears. |
| `banque/finances -> tableau` | The sideboard gains a cow on an arrow, a large bird, bees, and other prominent elements. |
| `brocante/souvenirs -> vitrine` | A glass display cabinet becomes a tent scene with people and an open cabinet behind a table. |
| `brocante/grenier -> casier` | A tall compartment cabinet becomes a smaller cabinet behind a large activity table. |
| `brocante/fouilles -> cabinet` | The cabinet's contents are replaced with different objects, plus children and a train. |
| `bureaux/etage -> classeur` | A small filing cabinet becomes a tall cabinet and a whole room of people. |
| `bureaux/metiers -> comptoir` | A bear and teapot display expands into a different arrangement with an owl, machinery, and a mechanic. |
| `bureaux/services -> guichet` | A woman pointing at a chart becomes a framed family-and-service scene. |
| `bureaux/apprentis -> etabli` | A factory model and worker figurines become a different tabletop workshop. |
| `cirque/cirque -> cirque_guichet` | A ticket booth with largely empty windows fills with characters; additional figures appear outside. |
| `cirque/clowns -> clowns_malle` | A trunk of costume pieces becomes a scene containing people, clowns, and different props. |
| `concours/potager -> potager_casier` | Produce under glass covers becomes a family gathered around an uncovered cake and vegetables. |
| `concours/gateaux -> gateaux_casier` | Cake shelves gain a table, people, chicken, vehicle, and other foreground objects. |
| `ecole/fete -> gateaux` | The cake table moves from the school courtyard to a grassy garden; people and tabletop arrangements change. |
| `lycee/lycee -> paillasse` | A male scientist becomes a woman; laboratory equipment becomes eggs and a balance; the boys on the stairs change positions. |
| `monde/cartes -> bagages` | The lower shelf's mouse and other objects are replaced by a large hand, marbles, and different props. |

Three additional pairs need continuity cleanup, although the core subject is
recognizable:

- `horloge/horloge -> place`: courtyard architecture and background change.
- `reparation/attente -> cageot`: furniture and surrounding structure change.
- `serre/serre -> souche`: plants, background, and lighting change markedly.

The garage workbench is comparatively consistent before and after zooming. Its
composition issue is separate from continuity. Many other zoom pairs closely
preserve their parent crops; a zoom is not a failure simply because it reveals
more detail or uses a closer viewpoint. Deliberate doorways to another room also
need a different review from a magnification of the same object.

These failures are covered already by G109, "Zoom matches parent", and G145,
"Parent miniature and zoom hint". Several look like a zoom was repainted without
updating its parent miniature; that is an inference from the images, not a
verified history of each edit. Often the smallest fix would be to update the
parent region to preview the finished zoom. Choose the authoritative version
first; do not propagate a flawed zoom into an otherwise correct parent.

## Proposals to reduce construction errors

Skill/tool review revision: `3a332c0fabb2aaf7de835f7540019647a2ff61cd`.
These proposals extend the existing skills; none has been implemented here.
The useful shift is from adding more prose rules after each failure to making
the existing rules executable, traceable, and easy to review.

| ID | Proposal | Where it belongs | Concrete acceptance criterion |
|---|---|---|---|
| E1 | **One versioned rules registry.** Give each rule a stable ID, scope, severity, check method, and canonical reference. Generate the short skill checklists from it. Archive superseded instructions instead of leaving competing imperatives active. Record the approved style profile and reference-image hashes. | All three skills; builder setup/style; release gates. | A job names one ruleset version; contradictory active instructions and broken tool/reference links are reported before work starts. |
| E2 | **A typed room manifest validated before generation.** Store word/sense IDs, composition groups, surfaces, counts, placement, doors, zoom links, and source assets in a schema. Declare coordinate units explicitly rather than mixing pixels and percentages. Separate planned geometry from final measured geometry. | Planning, manifest template, precheck, build tooling. | Missing IDs, duplicate assignments, bad units, impossible counts, invalid targets, and inconsistent geometry stop the job before an image request. A required manifest cannot silently become optional. |
| E3 | **Make zoom continuity a linked contract.** Record the parent region, landmark geometry, materials, contents, relative arrangement, and allowed changes. Classify a link as magnification, opening a container, or entering another room. Generate the zoom using the actual parent crop as a reference; preserve visible landmarks even when revealing hidden detail. | Planning, moving-words, prompt template, G109/G145. | Every changed zoom has a dated parent/crop/zoom comparison. A parent or child image change invalidates the pair's review. A badge-inside-box check alone cannot count as a continuity pass. |
| E4 | **Ship dependent changes atomically.** Track dependencies from a word/hook to its sprite, room painting, parent miniature, card crop, alt text, manifest, and generated payload. A zoom repaint should name every parent that previews it. | Build pipeline, moving-words, release process. | A proposed change produces an explicit affected-file list; stale dependants block that change. The whole dependency set lands together. |
| E5 | **Review composition before detailed painting.** Make a cheap layout/rough showing the actual groups, surfaces, perspective, label budget, and focal action. Store one ordinary sentence describing the shared activity and what each group contributes. For sprites, write the surface, angle, scale, light, and occlusion slot before generation. | Composition, planning, prompt template. | The rough passes the labels-off storybook test and has room for every label before detailed assets are generated. Merely naming two IDs in an interaction group is insufficient. |
| E6 | **One authoritative word/sense/hook record with explicit override provenance.** Resolve legacy payloads, source vocabulary, shared corrections, building overrides, and user edits in a documented field-level order. Emit which source supplied each final field. Keep patch edits surgical. | Hook rules, language validation, build_v2 data assembly. | A word's final sense, pronunciation, hook, and example are inspectable together; silent replacement of a newer correction is detected. Hook/image mismatches remain pending until the linked art and text agree. |
| E7 | **Share rendering geometry between viewer and checker.** Use the same coordinate conversion, label measurement, anchor, badge, and door placement functions. Add a few known-good and known-bad fixtures for recurrent errors. | Viewer, precheck, check_v2, release-gates tooling. | Fixtures catch px/% mistakes, detached labels, overlapping controls, clipped items, and narrow-screen tab failures. A viewer change cannot leave the checker modelling an older layout. |
| E8 | **Evidence tied to content, not a remembered PASS.** Record image, manifest, ruleset, build, and relevant renderer hashes with each verdict. Use pass/fail/not-checked/not-applicable; record the exact reason and crop for a failure. | Review logs and release process. | Repainting or changing geometry invalidates the relevant evidence. A static check, thumbnail screen, and full visual review have distinct statuses. |
| E9 | **Explicit room-type rules and exceptions.** Define separate density/count policies for rooms, tool close-ups, reference boards, and doorways. Count semantic reference boards separately from their letter/number controls. Allow a plain hook when appropriate. | Language representation, density rules, precheck. | An alphabet board with 26 letter controls is not automatically treated as 26 competing scene objects. An exception names its reason and applicable rule rather than silently weakening every gate. |
| E10 | **A building-level composition and motif index.** Record a thumbnail, camera, landmark, situation, lighting, and distinctive hook motifs for each sibling room. Use image similarity and colour statistics only to nominate comparisons. | Composition, G129/N10, contact-sheet tooling. | Every new room is compared against its siblings; a reviewer judges flagged look-alikes. Repeated grammatical markers such as the mime are distinguished from accidental repeated hook motifs. |
| E11 | **Bounded, change-aware validation.** Run cheap structural checks, changed-room visual review, linked parent/zoom checks, then a small navigation/card smoke pass. Run whole-site audits periodically or when shared rules/rendering change. Keep every changed item in the visual review even when scripts pass. | Validation and release process. | A small sprite correction does not trigger an unbounded tour of 477 rooms; a shared renderer change expands the scope automatically. Required checks have real commands and record skipped checks honestly. |
| E12 | **Control concurrent edits and retries.** Start from a recorded main SHA, declare owned paths and shared dependencies, merge narrow patches with an expected-head check, and rebuild derived data from the combined sources. After repeated failed image attempts, revisit the slot/hook/layout instead of resending the same prompt. | Planning, hook merge, build and deploy process. | No whole-file hook replacement erases another correction; stale-base updates are rejected safely; each regeneration states the specific failure it is correcting. |

### Why these proposals follow from the current implementation

- `scripts/qa/check_v2.py` checks that a zoom has an `obj` rectangle and that
  its badge lies inside that rectangle. It does not establish visual equality
  between the object and the destination painting. E3 fills that gap.
- `tools/precheck.py` supports a manifest but loads it only when `--manifest`
  is supplied. Prompt-heading and word-presence checks show that text is present;
  they cannot prove the image follows it. E2 and E5 separate structural
  completeness from actual visual compliance.
- `tools/contact_sheet.py` already provides a useful room/item review format.
  Extend it with parent/zoom and sibling comparisons rather than inventing a
  second unrelated review pipeline.
- `reference/moving-words.md` already requires matching the parent miniature
  after a zoom repaint. The 18 clear failures above support enforcing this as
  a dependency, rather than adding another equivalent sentence to a skill.
- The skills already require exact viewer geometry, but the review material
  also refers to missing historical scripts. E1, E7, and E11 make the operative
  path unambiguous.

## Proposals to reduce token use and repeated work

At the skill-review revision, the 32 Markdown files under `skills/` total about
303 KB. This is a byte count, not a measured token count or a recommendation to
load all files. The skills already use progressive references; preserve that
design and make the task-specific context smaller and more reliable.

| ID | Proposal | Practical saving and limit |
|---|---|---|
| T1 | **A short task router plus focused briefs.** Keep a compact entry checklist and map tasks such as new room, hook correction, zoom repaint, or UI change to the minimum relevant references and rules. | Reduces repeated reading of unrelated policies. Each brief still includes common invariants and the ruleset version; load full detail when an issue requires it. |
| T2 | **Compile prompts from approved data.** A small tool expands a style-profile ID, room manifest, slot spec, and relevant constraints into the full generation prompt. Save the exact expanded prompt as an artifact. | Avoids manually restating the 15-section template for each item and prevents transcription omissions. An image generator does not know repository rule IDs: the compiler must expand the needed instructions before sending them. This reduces authoring/context repetition, not necessarily image-provider prompt tokens. |
| T3 | **Keep editable assets separate from rooms.** Store one background, slot-specific assets, masks/occlusion, and a canonical layout; compose the published painting and crops deterministically. | A one-item correction needs the failing asset and its local reference region, rather than a whole-room regeneration. Deep architectural changes can still require an integrated edit. |
| T4 | **Generate compact task packets.** Export only the target room's resolved words, relevant pronunciation/hooks, slots, parent crop, sibling thumbnails, ownership, and outstanding findings. | Avoids repeatedly opening the full vocabulary, every legacy payload, long conversation files, or historical review logs. The packet records source SHAs so omitted context can be retrieved deliberately. |
| T5 | **One small visual review packet per change.** Show the affected room with item crops, the parent/zoom pair, and relevant sibling thumbnails together. Open large images only for uncertain details. | Builds on the existing contact-sheet workflow. Keep counts, sound-cue props, and small text large enough to judge; thumbnail size is not evidence that a tiny detail passes. |
| T6 | **Cache builds and reviews by their real dependencies.** Key generated crops, sheets, OCR results, and evidence by source hashes, ruleset, renderer, and review type. Give changed images new content-derived filenames. | Avoids repeated OCR, image inspection, and cached-path confusion. Reuse evidence only when every relevant dependency is unchanged; a changed rule may require a new judgment of the same image. |
| T7 | **Use incremental builds and affected-room checks.** Build cards/data only for changed rooms and their dependants. Cache the global word-coverage index and update it from the diff. Reuse an existing checkout with `unbuilt.py --repo`. | Avoids repeated clone/full-build/global-review cycles. Shared data or rendering changes widen the dependency scope; scheduled whole-site audits remain useful. |
| T8 | **Let scripts return structured, concise findings.** Emit stable rule IDs, affected items, exact coordinates, counts, and a short proposed next action; keep raw logs and image bytes out of model context. | Saves diagnostic tokens and makes fixes easier to target. The model still reads evidence for semantic and visual judgments. |
| T9 | **Preserve a compact resumable work record.** Save base SHA, file ownership, approved choices, completed steps, open findings, asset hashes, and the next action. | Reduces re-reading long chat histories or restarting work after a pause. Reuse task context when available; do not require extra agents for a small job. If agents are explicitly requested, give them narrow packets and retain one owner per stream. |
| T10 | **Prevent expensive retries with cheap preflight.** Validate schema, assignment, counts, layout, and prompt completeness before generating; inspect a rough before a batch; regenerate only failing regions/assets. | The largest likely saving is avoiding rework, not shortening a few sentences. Measure attempts, bytes/context supplied, generation cost, and accepted rooms before claiming a percentage saving. |
| T11 | **Archive history outside the active skill path.** Keep the current normative rule once; move superseded lessons and long incident narratives to searchable history. Generate summaries instead of accumulating equivalent gates. | Reduces contradictory context and repeated instructions while retaining the evidence behind a rule. Never discard current user preferences or unresolved findings. |

### Suggested compact job record

A future job record could contain the following fields, with large content kept
in referenced files rather than copied repeatedly into conversation:

```json
{
  "base_commit": "<sha>",
  "ruleset": "<version>",
  "style_profile": "<approved-profile-and-reference-hashes>",
  "task": "zoom-repair",
  "room": "lycee/paillasse",
  "manifest": "<path>",
  "parent_region": "<path-and-box-in-declared-units>",
  "owned_paths": ["<paths>"],
  "affected_dependants": ["<parent-miniature>", "<cards>", "<payload>"],
  "open_findings": ["G109: equipment and characters differ"],
  "evidence": "<review-record-path>",
  "next_action": "<one concrete step>"
}
```

This is a proposal, not a newly introduced repository schema.

## Coordination and implementation order for these follow-ups

Related proposals are also recorded in `docs/PROPOSALS_2026-10-28.md`. Resolve
policy differences before implementation rather than applying both documents
literally. For example, that document proposes individual alphabet hooks and
placement notes on cards, while the active skills prescribe one alphabet board
without per-letter mnemonics and keep placement explanations in the guide.
Likewise, hiding labels or adding a level filter does not fix a crowded painting.

Recommended construction-workflow order:

1. Resolve the active rules and source precedence (E1/E6), then define the small
   task briefs (T1). This gives every worker the same current instructions.
2. Add typed manifests and zoom dependency/review records (E2-E4). Use one of the
   clear parent/zoom mismatches as a pilot; include the parent miniature in the
   same change.
3. Extend the existing contact sheets and implement dependency-aware evidence
   and incremental checks (E7-E8/E11, T5-T8).
4. Standardize the separate-asset composition path and prompt compiler
   (E5, T2-T3), using one pilot room before any bulk migration.
5. Repair the named continuity/style failures in small coherent batches, using
   measured retry counts and review scope to refine the workflow.

An initial success criterion is practical: one small repair updates every
dependent artifact, passes the applicable checks, has a readable before/after
comparison, and does not require a new whole-site read or whole-room repaint.
No site, skill, tool, image, or data changes are implemented by this document.

## Candidate mnemonic improvements

Reviewed live card text at `3b1072f054df736ee58cef9bf17fb14896923294`.
These are proposed hooks and painting directions, not applied corrections.
They have not been tested with learners or independently signed off. English
keywords are retrieval aids, not substitutes for the French IPA and audio.
Room locations below describe the reviewed site; they do not override planned
relocations or establish that the current placement is appropriate.

The best opportunities are not necessarily the longest or most complicated
French words. Fix obvious sound mismatches, make the English cue visible, and
make it physically interact with the thing being learned. Keep an existing good
hook rather than replacing it just for novelty.

### Close sound cues and more concrete scenes

| Word / live location | Current weakness | Proposed hook and image | Sound match and limits |
|---|---|---|---|
| **la ficelle** `/fi.sɛl/` — `garage/tools` (`fr_ficelle_noun`) | The current card uses fi-CELL(o), although "fi" is not an English keyword and the cello adds an unwanted ending. | **FEE + CELL:** a visitor pays a coin to open a toy prison CELL, then pulls the TWINE that operates its door. Keep the coin payment, recognisable barred cell, and working string together as one compact workbench toy. | FEE + CELL gives a close two-part cue to fee-SEHL, without the cello's final vowel. Payment must be visible; a loose unexplained coin is insufficient. No prison storyline or extra characters are needed. |
| **la boue** `/bu/` — `maison/bains_buanderie` (`fr_boue_noun`) | Muddy boots plus the word "BOO!" in the hook do not give the picture a sound cue. | **BOO:** a friendly ghost climbs out of a muddy boot, its lower half trailing thick MUD back into the boot. The ghost and mud are one event. | BOO is a close whole-word cue. The ghost should be identifiable without a speech bubble. **Motif dependency:** a ghost is already visible in `maison/salon`; `route/casier` also has a ghost in the carburant hook. Resolve the destination and motif conflict before choosing this design; do not simply add another ghost to either building. |
| **la selle** `/sɛl/` — `ferme/souche` (`fr_selle_noun`) | The current seller cue is not actually shown and has an extra syllable. | **CELL:** a miniature prison CELL has a leather SADDLE for its only seat, complete with stirrups projecting outside the bars. Present it as one toy on the existing work surface, with the saddle clearly recognisable. | English CELL is a close whole-word match. This avoids needing a nameless "seller" or a spoken explanation. Check that the image reads as a prison cell rather than a generic cage. |
| **le rideau** `/ʁi.do/` — `maison/salon` (`fr_rideau_noun`) | The existing REDO cue is written as "ree-DOH", but ordinary English redo ends in an oo sound. | **REED + DOUGH:** a child hangs a CURTAIN woven from long REEDS; soft bread DOUGH is visibly wrapped around the lower ends as comical curtain weights. Both materials form the curtain itself. | REED + DOUGH approximates ree-DOH, sharing the d at the join. English dough's vowel and the English r are not identical to French. The raw dough must be unmistakable, not generic round beads. |
| **la chaire** `/ʃɛʁ/` — `eglise/eglise` (`fr_chaire_noun`) | "Linked to chair" encourages the wrong initial English ch sound and shows no distinct sound-cue action. | **SHARE:** two parish speakers respectfully SHARE one broad PULPIT and the same open book, each using one side. Keep the pulpit's raised platform and access steps clear. | SHARE is a close cue, with the French r supplied by pronunciation practice. Sharing must be physically visible, rather than only saying that a priest "shares a sermon". This refines the SHARE proposal already in `docs/PROPOSALS_2026-10-28.md`; it is not a newly discovered keyword. |
| **le fer** `/fɛʁ/` — `rue_commercante/ferronnerie` (`fr_fer_noun`) | The current hook merely says the blacksmith acts "as if" at a FAIR; the fair is not part of the described object. | **FAIR:** the blacksmith assembles a miniature FAIR ride, a Ferris wheel, directly from the IRON bars on his anvil. Show the last straight bar being bent into the wheel. | FAIR is a close accent-dependent cue, not a perfect model of French r. This keeps the existing keyword but makes it visible and makes the iron participate in it. Use a small working model, not a second fairground scene. |
| **le casque** `/kask/` — `maison/penderie_commode` (`fr_casque_noun`) | The current helmet is only described as round like a CASK; the cask is not actually present. | **CASK:** a HELMET is made from a tiny wooden CASK, with curved barrel staves, metal hoops, and a fitted chinstrap. It still has the unmistakable silhouette of wearable head protection. | One simple keyword fused with the meaning. The vowel in English cask varies by accent and differs from French /a/ for many speakers: treat this as an approximate cue, not an exact pronunciation. Coordinate with the existing proposal to relocate casque. |

### Partial cues worth auditioning, with the missing sounds stated

These are candidates for comparison with a plain meaning picture, not automatic
upgrades to "strong". The card must not claim that the full English word is
pronounced like the French word.

| Word / live location | Proposed scene | Why it may help; required caveat |
|---|---|---|
| **la laine** `/lɛn/` — `maison/penderie_etagere` (`fr_laine_noun`) | A spinner winds thick WOOL around the rim of a giant magnifying LENS, turning the lens into a wool-covered winding wheel. | Use **LENS without its final /z/** as the sound bridge. That leaves /lɛn/. The current LEAN cue has the wrong vowel. The lens must stay recognisable through its clear centre and magnification. This is an explicit sound-subtraction cue, not a claim that lens and laine are identical. |
| **prêt** `/pʁɛ/` — `reparation/attente` (`fr_pret_adj`) | A cyclist waits READY to set off: helmet fastened, foot poised on a pedal, gripping a giant PRETZEL-shaped handlebar. | The opening **PRE- of PRETZEL** is closer to /prɛ/ than English PRAY, whose vowel is different. Only the opening chunk is used; the rest of pretzel is not in prêt. Readiness must be apparent without a written READY sign. Keep the adjective's centre-band placement. |

### Smaller refinements that preserve an existing useful keyword

- **la bague** `/baɡ/`, `rue_commercante/bijouterie`
  (`fr_bague_noun`): keep **BAG**. Instead of a ring merely hidden in a bag,
  make a jeweller's tiny BAG fasten with a giant jewelled RING: the ring passes
  through both handles to close it. This fuses cue and meaning into one object.
  The English vowel varies by accent; retain the French pronunciation separately.
- **vendre** `/vɑ̃dʁ/`, `boulangerie/boulangerie`
  (`fr_vendre_verb`): make the existing **VEND** connection visible through a
  small baguette VENDING machine. Monsieur Verbe accepts a customer's coin and
  operates the machine to SELL a baguette. Treat this as a familiar related-word
  bridge, not a claim that English vend is pronounced like vendre. Preserve the
  correct mime and beret code. This is a possible way to clarify an existing
  lexical connection, rather than inventing another multi-part pun.

### Misleading sound claims to remove before inventing new puns

| Current cue | Problem | Recommendation |
|---|---|---|
| **four** `/fuʁ/` = English FOUR | English four normally has a different vowel. Holding up four fingers does not teach the French sound. | Keep a clear OVEN picture and accurate audio unless a genuinely better cue is found. Do not spell English four as "FOOR" to manufacture a match. |
| **scier** `/sje/` = SEE-SAW | See-saw adds an extra syllable and different final sounds; it does not model the one-syllable French word. | Retain the natural sawing action as a plain meaning picture. The current live strength is already plain; keep that honest classification. |
| **graine** `/ɡʁɛn/` = GREEN | English green has /i:/, whereas graine has /ɛ/. | Keep a distinctive SEED image or find a closer cue. Do not teach the English green vowel. |
| **souris** `/su.ʁi/` = SORRY | The first vowel and overall sound differ, especially in American English. | Use a clear MOUSE/computer-mouse scene and French audio until a better candidate is available. The recent computer-room repaint is not a reason to change its art again for another weak pun. |
| **cage** `/kaʒ/` = GARAGE without "ga" | Removing ga from garage leaves something like /ʁaʒ/, not /kaʒ/. | Drop that derivation. A plain CAGE with its real pronunciation is better. |
| **bûche** `/byʃ/` = BUSH | English bush has a different vowel from French /y/. | If kept, call bush an approximation and teach rounded French u explicitly. Never claim equality. |
| **soif** `/swaf/` = SWADDLED, suggested as a better example in the language skill | Ordinary English swaddled does not contain the full /swaf/ sequence. A skill example can also be weak. | Reassess this example rather than treating its presence in a skill as proof. No replacement pun is asserted here. |

Harder words such as farine, manivelle, and ciseau should not get a longer,
less accurate pun merely to avoid the label plain. The current trou troop-minus-p
cue, clou/CLUE, seau/SEW, and roue/ROO already provide useful compact links;
they do not need a wholesale rewrite for novelty. Each still needs its genuine
French pronunciation and a matching picture.

### How to choose and apply a proposed hook later

1. Say the French word and English keyword aloud separately. Check vowels,
   nasalisation, consonants, and syllable count. Record whether the cue covers
   the whole word, an opening chunk, an explicit subtraction, or a related word.
   Have an independent reviewer or learner audition it; the proposing model's
   confidence is not validation.
2. Check the current building's motif index and the planned word placement.
   The boue ghost conflict above is a concrete reason this matters. Avoid moving
   a word or adding a repeated motif merely to make the new pun convenient.
3. Draw one compact interaction: the English cue acts on, is made from, or
   operates the meaning. Attach it to the room's shared activity. Avoid generic
   helper figures, unexplained coins, name tags, speech bubbles, and cues that
   exist only in narration.
4. Compare candidate versus current hook and plain meaning picture on a small
   sample. A useful check is whether a learner can recover both the French word
   and its meaning later; an attractive image alone is not enough.
5. Only after selection, update the hook and matching asset together, plus any
   parent miniature, card crop, alt text, and derived payload. Preserve unrelated
   fields and current user overrides. Until then these rows remain proposals in
   this file, never a text-only replacement over mismatching live art.

Suggested first auditions: **ficelle (FEE + CELL), selle (CELL), rideau
(REED + DOUGH), and chaire (SHARE)**. The boue/BOO cue has a close sound match,
but its motif/placement conflict should be settled before painting.
