# Four standalone packs integrated

Base: e8ffce47800c15b837cd67eb2ab362b4b21207a5.

The requested kitchen, upstairs mathematics and two military-history packs now teach all 50 assigned words across eight connected scene paintings. Their original source-room IDs and inventories are preserved. Gender-aware complete-object hotspots, hooks, cards and room-focused dialogues are built from the source data.

- Restaurant: a new courtyard links the existing chef kitchen, tasting pass and preparation kitchen. The earlier kitchen retains its painting and eleven words as `cuisine_chef`.
- Mathematics: a covered entrance court links the existing measures laboratory and oak stairs to two upstairs classrooms. The earlier laboratory retains its painting and nine words as `mesures`.
- Military history: the existing B16 sector marker opens a museum vestibule, then a four-gallery circuit returning to that vestibule. Every transition follows a painted arch. The one-way interpretation sequence is explicit in both source layout and walkthrough; validation checks the real incoming doorway and a painted path back to the hub. It rejects a trapped circuit or a cross-building fake arrival.

Correct senses are explicit: la garde is the body of guards; la solde is military pay; avant-garde is the military vanguard; boulet is a cannonball; incorporation is induction; ration is an allocated portion; matrice is a mathematical matrix. Existing measures meanings remain unchanged.

## Art evidence

The four subdirectories in `docs/integration-packs` preserve the standalone pack manifests, dialogue sources and original reviews. Paths/hashes in those original manifests refer to the standalone pack versions, not the integrated teaching files. Integrated layouts/hooks under `content/v2` are authoritative for the live scenes. Navigation request texts and original hub planning manifests are preserved in `navigation`; its independent review records the final fitted openings and image hashes.

Three circulation paintings are new. Both upstairs classrooms gained painted return stairs; the preparation kitchen gained a full-height courtyard door and its complete bean/cow group moved upward to make space. The rotation hook now describes the visible globe, equatorial arrow and pedestal, without the removed crank. All other standalone teaching paintings are unchanged.

## Validation

- Strict placement/content checks pass for restaurant, maths and caserne: 70 words (50 new and20 existing).
- All649 placed dialogues pass the dialogue checks.
- Whole-site painted reachability:715 spaces reachable,715 can return, zero failures. One-way museum edges are deliberate and reported as warnings.
- The three walkthrough covering walks pass.
- All18 regression cases pass, including three one-way circuit cases; copyright and skill-path checks pass.
- Independent navigation/art review is recorded beside the manifests.
- Service-worker cache advanced from v53 to v54.

Browser interaction was not verified in this executor because Chromium cannot create its required sockets. Repository-wide CI must pass before merge; no browser pass is claimed.
