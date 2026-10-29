# Le garage — workshop and tool close-up

**21 words across two views:** ten in the main room, including **scier** and **réparer**, and eleven in the workbench close-up. The village map's stone outbuilding beside the windmill opens `#/garage`; **Les outils** opens `#/garage/tools`. Back returns from the close-up to the main room, whose courtyard door returns to the map.

`content/assignment.json` explicitly assigns the nineteen planned garage/tool nouns and two relevant verbs from superseded verb streets. Bricolage moves to the close-up to give the repairing mime a natural main-room working spot. No planned word is lost and no market words are borrowed. Feminine nouns stay left, masculine nouns right; the red beret identifies the two -er verbs. Each verb card has seven tense tabs, participles and examples.

The main background remains unchanged. Scier works behind the left bench with furniture occlusion; réparer crouches over a broken chair. The closer view shows that same bench, wall, window and slate floor. The revised **trou** asset shows a TROOP of toy soldiers entering a HOLE; troop without final p gives TROO. Its card states the sound cue honestly.

## Edit one source

- `background.jpg` and `tools-background.jpg`: empty paintings, independent of vocabulary.
- `assets/<name>.webp`: individual transparent source sprites.
- `room.json`: assignments, slots, hooks, cards, labels, occlusion and navigation.
- `scripts/build_garage.py`: scoped build of placed sprites, 384px card crops and composition proofs; writes images atomically and removes obsolete derived sprites.
- `review/`: per-view proofs and labeled asset sheets. These are deterministic compositions, not browser screenshots.

Run from the repository root:

```sh
python scripts/build_garage.py
python scripts/qa/check_garage.py
python -m http.server 8000 --directory village
```

The normal village entry and standalone `/garage-preview.html` use the same data and renderer. Full source prompts and corrections are in `PROMPTS.md`; detailed evidence and remaining limits are in `review/REVIEW.md`.

Artwork generated with OpenAI's built-in image tool. French vocabulary attribution remains in `LICENSE-DATA.md` and `data/source/CREDITS.md`; card explanations and dialogue are original.
