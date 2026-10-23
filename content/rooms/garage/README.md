# Le garage — home workshop draft

Claim: **Codex**, `R_garage`, `B05_maison`. Claude's market is outside this package.

Nine items come from the existing `R_garage.words` inventory; none are borrowed from the tool-shelf zoom. The garage is under the house in the source hierarchy. The small stone outbuilding beside the windmill opens directly into this garage; the rest of the home sector remains closed.

The room has a curved teal roof truss and round daylight window, a village-facing doorway, two workbenches, a stone niche and a cupboard. Feminine nouns occupy the left half; masculine nouns occupy the right. Props vary in height and depth. Plain meaning depictions are rated honestly rather than presented as strong sound links.

## Edit one thing cheaply

- `background.jpg`: immutable empty painting; no vocabulary baked in.
- `assets/<name>.webp`: independent source sprites, preserving alpha.
- `room.json`: the complete placement, slot, hook and card source. Change this small file to move an object or fix text.
- `../../../scripts/build_garage.py`: builds the derived scene assets and cards; it never regenerates the background or calls a model.
- `review/room-proof.jpg` and `review/item-crops.jpg`: deterministic composition and per-item proofs, not browser screenshots.

Run from the repository root:

```sh
python scripts/build_garage.py
python scripts/qa/check_garage.py
python -m http.server 8000 --directory village
```

Open `/garage-preview.html#/garage`. The village map links the small stone outbuilding beside the windmill to `#/garage`. The painted courtyard door and Back return to the existing village map. Both mouse and touch handling use the established viewer. Cards reuse their room sprite rather than relying on the shared word-image directory.

## Release status

**Approved by the user for merge.** Independent visual review and package checks pass. The room is linked from the village map and also available through `garage-preview.html`. See the package review log for performed checks and unverified gates. The repository has no current repaint queue or canonical release-gate tooling from the older skill references, so those checks are not claimed as passed. The planned tool-shelf zoom is deferred; no fake zoom entry is present.

Artwork generated with OpenAI's built-in image tool for this project. French source vocabulary attribution remains in `LICENSE-DATA.md` and `data/source/CREDITS.md`; new card explanations and dialogue are original. Source prompts and slot specifications are recorded alongside the room.
