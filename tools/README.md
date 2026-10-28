# tools/: cheap checks before eyes

Run them in this order on every build or repaint job. They need Python 3 and Pillow; precheck's OCR also needs `tesseract-ocr` and `tesseract-ocr-fra` (eng+fra). Without tesseract, precheck skips OCR and says so.

| step | tool | what it does |
|---|---|---|
| 0 | `unbuilt.py [--building ecole] [--all] [--json out.json]` | Shallow-clones or updates `main` into /tmp/mp_unbuilt_main (no credentials, no prompts). It counts live vs planned words **by word id** against data/source/{rooms,buildings}.json and vocab.jsonl, and lists each building's built / partial / unbuilt rooms, with the live room keys that hold them. `--repo DIR` uses an existing checkout. |
| 1 | `manifest_template.json` | The planning gate. Copy it to `<bld>_<key>.manifest.json` and fill one entry per word: what is shown, pose/action, exact `count`, `verb_acts_on`, sensitive treatment, side/zone, plus doors/exits, zooms and intended `text_in_image`, and the room-level prompt fields `scene_situation`, `interactions` (groups of 2+ `who` with a `doing`), `siblings`, `used_motifs` and the `prompt` object (camera, light, landmark...). Generate `prompt_text` with `build_prompt.py` (step 1b). Check it against the skills, then paint. |
| 1a | `room_context.py <bld> [--room key]` | A 1-2k token brief of the building for the manifest: each room's alt text, words and sides, doors and zooms; the motifs already used; planned words not live yet; open notes in RECOMMENDED_CHANGES.md. Read it instead of `village/data/<bld>.js`. |
| 1b | `build_prompt.py m.json [--write] [--check]` | Fills builder reference/prompt-template.md from the manifest (spacing numbers from `skills/limits.json`) and prints it; `--write` stores it as `prompt_text`, `--check` fails if `prompt_text` was edited away from it. Exit 1 while any `{field}` is left. |
| 2 | `precheck.py [IMAGE] --data village/data/<bld>.js --room <key or R_id> [--manifest m.json] [--json]` | Cheap automated checks, using check_v2 / build_v2 geometry. **FAIL** (exit 1): size not 1280x720, out of bounds, hotspot or label overlap, a hotspot or label over a door / mapExit / zoom badge / nameplate, a one-object zoom, manifest gaps (missing or extra ids, no `shown`/`pose_action`/`sensitive`, a count missing, a verb without `verb_acts_on`, doors not covered; prompt gate: no `scene_situation`/`interactions`/`siblings`/`used_motifs`/`prompt_text`, an interaction with fewer than 2 `who`, a `prompt_text` missing any of the 15 template section headings, an unfilled `{field}`, or an item word the prompt never names). **WARN**: labels within 3 px, a label touching another hotspot, under 8 px from the edge, more than 12 px from its own box, an adjective/adverb outside the centre band, more than `room_target` items (FAIL over `room_max`; numbers from `skills/limits.json`), a zoom under 4 words, a word in no interaction group (isolated figure), a `prompt_text` that doesn't quote the situation. **FLAG**: OCR text runs for a human to judge (declared / undeclared / DIGIT), never a reject. |
| 2b | `hook_lint.py [bld ...] [-v] [--fail]` | The mechanical hook checks: respelling in the hook vs the card, "Like English" on a false friend, etymology or "Think of" wording, placement openers, shared openings, no capitals, three-chunk puns, example sense. Reports only; `--fail` with building names fails on any finding (new and repainted rooms). |
| 3 | `contact_sheet.py --data village/data/<bld>.js --room <key> [--precheck pre.json] [--image new.jpg] [--shots DIR] [--out DIR --tag _v2]` (or `--all` rooms) | ONE downscaled review sheet per room. It shows the painting with boxes, labels, doors, badges, the nameplate and OCR flags, beside the browser shot (or the hook list). Below that, a 256 px card-crop tile per item and per exit, with the headword and hook (gate A). Open full-size crops only where a tile raises doubt. |

**OCR limits.** OCR runs on tiles (480x360, upscaled 3x, psm 11, conf ≥80 and ≥3 characters, or a lone digit at conf ≥90). It reliably catches clear sign text: a test "CANTINE" sign was found at conf 96. It misses small or low-contrast text, such as 22 px "Menu du jour" or a faint painted "7". The sheet review must still look for text, and a flag is a question, not a verdict: natural scene text may stay (builder reference/text-and-labels.md).

## Sample output (main @ d9cb8cd8, Oct 26)

```
$ unbuilt.py
TOTAL live 3,752 of 8,004 planned words (46.9%), left 4,252; live ids not in plan: 12
rooms: built 241, partial 137, unbuilt 338
$ unbuilt.py --building ecole
== B02_ecole  Petite École (first schoolhouse)  live 60/187, left 127
  partial  R_pronouns_02                live   8/13  left   5  in ecole/cantine
  ...
$ precheck.py --data village/data/ecole.js --room cantine          # ~5 s
  FLAG  ocr: '4' conf 91 at [304, 249, 18, 22] [DIGIT - can break a count]
  FLAG  ocr: 'NOR' conf 81 at [1077, 658, 16, 8] [undeclared]
summary: 0 fail, 0 warn, 2 flag  -> ready for the contact-sheet review
$ precheck.py --data village/data/mairie.js --room cour            # ~3 s
summary: 0 fail, 0 warn, 0 flag  -> ready for the contact-sheet review
$ precheck.py (label moved + incomplete manifest)                   # exit 1
  FAIL  labels overlap: vous / on
  FAIL  manifest: fr_te_pron is in the room but not in the manifest
  FAIL  manifest: fr_vous_pron has no 'shown'
  WARN  label on is 82px from its own box (detached)
summary: 3 fail, 1 warn, 2 flag  -> fix FAILs before visual review
$ contact_sheet.py --data village/data/ecole.js --room cantine --precheck pre.json
ecole_cantine_sheet.jpg  (355 KB; 8 word tiles + 1 exit tile)
```

## Repo checks

`skills_paths.py` fails if a skill names a repo path or script (in backticks) that does not exist. It runs on every pull request with `scripts/qa/check_v2.py --strict --placement` and `hook_lint.py` (see `.github/workflows/checks.yml`).
