# Le Village: a French vocabulary memory palace

A French vocabulary memory palace from A1 to C2. You walk a painted map of sixteen quarters, go into buildings, and find each word as an object or a person in a room. Feminine nouns stand on the left of a room and masculine nouns on the right; adjectives and adverbs stand in the middle. Verbs are acted out by Monsieur Verbe, a mime whose beret color gives the verb group and who holds a hand mirror for reflexive verbs. Click anything to open its card: meaning, pronunciation (IPA and an English-style respelling), gender and plural, a memory hook, an example, false-friend warnings, and full conjugation tables with the prepositions each verb takes.

The live site is the static folder `village/`, published with GitHub Pages.

## Layout of the repo

| Path | What it holds |
|---|---|
| `village/` | The site: `index.html`, `app.js`, `style.css`, the paintings (`village/<building>/*.jpg`, card crops in `cards/`), the maps (`map/`) and the generated data (`data/<building>.js`, `data/map.js`). See `village/README.md`. |
| `content/v2/<building>/` | Per-building inputs: `layout.json` (hotspot boxes in painting pixels, doors, zooms) and `hooks.json` (hook and text overrides for that building). |
| `content/v2/vocab_fixes.json` | Text corrections for every building: article and gender, respelling, gloss, example, plural, note. |
| `data/source/` | The plan: `vocab.jsonl` (8,000 words), `rooms.json`, `buildings.json`, `sectors.json`, the dialogues (`village_dialogues.json`, `conversations.json`) and credits. |
| `data/curated/` | Hand-written tables, e.g. `verb_patterns.json` (the prepositions each verb takes). |
| `data/cache/conjugations.json` | Verb tables (seven tenses), read by the build. |
| `data/v1-payloads/` | Card text from the first village; the build still reads it. |
| `data/hooks/qa/`, `docs/` | Review notes, proposals and change logs. |
| `skills/` | The memory-palace build skills (builder, language, release gates). Start with each `SKILL.md`. |
| `tools/` | Cheap checks before review: `unbuilt.py`, `precheck.py`, `contact_sheet.py`, the manifest template. See `tools/README.md`. |
| `scripts/v2/`, `scripts/qa/` | The build (`build_v2.py`, `build_map.py`, `build_extras.py`) and the gate checks (`check_v2.py`, `placement.py`). |

## Build and check

Needs Python 3 and Pillow.

```bash
python3 -m pip install pillow
python3 scripts/v2/build_v2.py              # every building; or name some: build_v2.py ecole mairie
python3 scripts/v2/build_v2.py --no-cards   # text-only rebuild: keeps the existing card crops
python3 scripts/v2/build_map.py
python3 scripts/v2/build_extras.py         # live buildings, search index, room conversations
python3 scripts/qa/check_v2.py              # add --strict --placement before a release; -v for word counts
python3 tools/hook_lint.py                  # mechanical hook checks (report only)
```

Every pull request runs `check_v2.py --strict --placement`, `tools/skills_paths.py` and the hook lint (`.github/workflows/checks.yml`). Room-size and spacing numbers live in `skills/limits.json`.

Preview by serving the folder, e.g. `cd village && python3 -m http.server`, and open the printed address.

Text changes (a hook, a gloss, an example, a plural) go in `content/v2/<building>/hooks.json` or `content/v2/vocab_fixes.json`, never in the generated `village/data/*.js`; then rebuild.

## Adding or repainting a room

Follow the skills in `skills/`: run `tools/unbuilt.py`, write the item manifest, build the painting prompt from the template, paint, run `tools/precheck.py`, review one contact sheet per room, then add the room to `content/v2/<building>/layout.json` and rebuild. `content/v2/README.md` explains how a building goes live on the map.

## Conjugations

`data/cache/conjugations.json` holds the verb tables. The build stops with a message if a new verb has no table; add its table to the cache, checking irregular verbs against an open reference.

## Pages

`.github/workflows/pages.yml` publishes `village/` to GitHub Pages when a change lands on `main`.

## Credits

Word lists, glosses, examples and dialogues are CC BY-SA 4.0. See `LICENSE-DATA.md` and `data/source/CREDITS.md`. A license for the site code has not been chosen yet, so there is no code `LICENSE` file.
