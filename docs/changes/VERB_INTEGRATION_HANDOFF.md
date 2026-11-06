# Verb integration handoff — 2026-11-01

Base: `10da19dc38252949b05041f277461dedf5853e38`. **25 verbs assigned to 17 existing ordinary rooms.** These are actual source assignments. Integrated so far: nourrir and seller in ferme/ferme; coucher and dormir in maison/chambre; planter, cultiver, and germer in ferme/coteau. Every other row is still pending art. Read the per-word TSV before resuming other room work.

## Files changed

- data/source/vocab.jsonl: only 25 word records changed (room_id, old street fields removed, building_theme_hint updated). Hooks, pronunciation, examples and conjugation metadata were preserved.
- data/source/rooms.json: moved those IDs between source lists, removed old tier membership, updated affected counts/side counts. No rooms deleted.
- data/source/relocations.tsv and docs/changes/RELOCATIONS_REWORK.tsv: every assignment appended with exact old/new rooms and rework.
- docs/changes/VERB_INTEGRATION_2026-11-01.tsv: precise target view, live origin, current hook/beret/mirror snapshot, action and status.
- Skills: staged fact/composition/finished-art review; overview/sector/building/floor/hub planning; connected passages and post-edit regression review. No viewer behavior changed.

## Live status

Nourrir, seller, coucher, dormir, planter, cultiver, and germer are live in their destination paintings, with the donor figure removed in the same pack. The other assigned verbs stay on their donor streets until their own art is accepted. `unbuilt.py` counts a word as integrated only when it is live in the planned building (or a layout that claims that source room). A copy that remains only on the donor street counts as `elsewhere` and does not mark the target room built; a copy in both places is `extra`. Do not install a half-painted move through a broad generated-data rebuild.

## Target worklist

| Target | Live → reserved total | Assigned verbs |
|---|---:|---|
| cabinet/barbier | 6 → 7 | raser |
| cabinet/organes | 6 → 8 | inspirer, respirer |
| camping/camping | 9 → 10 | brûler |
| couture/atelier | 12 → 13 | coudre |
| ecole/bibliotheque | 8 → 9 | feuilleter |
| ferme/coteau | 7 → 10 | planter, cultiver, germer (integrated) |
| ferme/ferme | 9 → 10 | nourrir (integrated), seller (integrated) |
| garage/garage | 10 → 12 | clouer, bricoler |
| gare/etage | 8 → 9 | transporter |
| jeux/fete | 8 → 9 | offrir |
| maison/bains | 11 → 13 | laver, doucher |
| maison/chambre | 10 → 12 | coucher, dormir (integrated) |
| maison/cuisine | 11 → 12 | cuisiner |
| maison/dressing | 10 → 12 | habiller, chausser |
| maison/jeux | 10 → 11 | ranger |
| port/bateau_pirate | 11 → 12 | naviguer |
| rue_commercante/fleuriste | 13 → 14 | tailler |

Totals over target 10 require a composition decision before painting; none exceeds hard max 15. Split/redesign if figures cannot fit naturally. The TSV targets ordinary room IDs, not zooms, and may distinguish views sharing a broad source room ID.

## Per-move integration checklist

1. Fetch/rebase main and check other work before painting. Resolve actual current word data using builder v1/vocab selection, global corrections and building overrides. The TSV preserves current hooks, not a phonetic approval; review weak/foreign-word cues. Preserve user choices.
2. Integrate the verb into the shared activity, with correct beret/reflexive mirror among nouns. No new standalone verb street or mime lineup. Confirm label space, physical passages and parent/zoom constraints.
3. Review composition, then every cue/count/anatomy at 2×. Fit boxes to accepted art; do not make a box miss its figure to pass a checker.
4. In the same integration pack, remove/recompose the donor hook/box/card/override and update donor/target alt, dialogue/pins/used_words, neighbors, passage hints and parent miniatures. Donors often have only a few words: do not strip below baseline/floor. Assign remaining donor verbs first if needed, then merge/retire the whole street scene with repaired routes.
5. Run placement/grid/dialogue/browser/continuity/cache checks and independent art review. Bump service-worker version for same-name image/card changes. Update the TSV status and this log with the actual commit and any remaining work.

## Trial result

One farm/nourrir candidate was generated and independently rejected: the mime landed outside its planned region and conflicts with the mule hotspot; calf placement conflicts remain; protected details were redrawn; the existing stump parent/zoom already disagree. Feeding action and green beret read clearly. No live farm assets were changed. See docs/room-trials/ferme-nourrir/README.md, review.json, independent-review.md, exact manifest/prompt and the historical candidate link in the trial README (the rejected PNG was removed from the current tree during unused-file cleanup). Seller is assigned to this room but was not painted in the trial.

## Scope cautions

The older source plan already differs from live v2 layouts outside this batch. Only these 25 IDs were reassigned; no wholesale reconciliation was attempted. Ordinary Back remains the outside shortcut; physical local hubs use real adjacent passages, not extra global Hub buttons. Circulation-only planning does not create a new runtime feature.


## Farm retry — 2026-11-02

Nourrir now appears in the main farm painting among the nouns, with its green beret and visible bottle-feeding action. Existing eight main words and all routes remain. Repaired the inherited stump miniature mismatch and actual group clearances; fitted full hook boxes, rebuilt cards/data/search/dialogue and bumped offline cache to v47. The original rejected trial remains historical. See retry-manifest.json, retry-independent-review.md and retry-review.json in docs/room-trials/ferme-nourrir/. Seller remains pending; no live donor was removed for nourrir.
