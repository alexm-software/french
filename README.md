# Memory Village

A French vocabulary memory palace, from A1 to C2. You walk a map of sixteen quarters. Each word lives in a room, on a piece of furniture, or along a verb street, so the place brings the word back.

Rue des Saveurs (S04, cafés and restaurants) is the open quarter: the square, Café de la Place, Restaurant Le Bon Goût, and four tiered cooking places along Ruelle des Gourmets. The other quarters are on the map and marked coming soon. The long walk still begins in the beginner quarter; that door is drawn, and it is not open yet.

You walk by the painted doors, paths and stairs. Forward and back (and left or right, when the picture has them) stay on the painting as `exits`. The cooking walk is square, étape 1, étape 2, étape 3, étape 4, and back to the square. Rooms in one building connect by the painted stairs and doors. Do not hard-code the verb list. Each painted item has one clickable box: if a `mnemonic_box` is still present, it widens that box and is not a second target.

`content/assignment.json` decides which words are drawn in a painting. A word that `rooms.json` still lists, but the painting does not draw, stays in that room’s word list and is marked as not in the painting. Street paintings store prev/next under `exits`. Building fronts and the sector view store doors under `links`. The build accepts both.

## Run it

```bash
python3 -m pip install pillow
npm install
npm run build
npm run preview
```

`npm run build` paints any missing placeholder scenes, splits the vocabulary into per-room files, and writes `dist/`. Open the preview and the hash routes do the rest.

`npm test` checks the built data: the open quarter, floor order, the bar-counter zoom, conjugation tables, and the church hotspot specimen used only as a format test.

## What is open

`content/site.json` lists `open_sectors`. Only those sectors get full word cards, quizzes, conversations and paintings. To open another quarter later, add its id and rebuild. Rooms outside that list stay on the map as coming soon and are not loaded as word files.

Street contents are not hard-coded. Ruelle des Gourmets is read from `rooms.json` and `vocab.jsonl`. The live street is four étapes (`ST_cooking_seg001` to `seg004`), laid out in tiers: street, balcony, upper and roof, with `-er` verbs on the left and `-ir` / `-re` verbs on the right. Replace those paintings and data files, then rebuild, when a later street arrives.

## Add a room’s painting

For each space, drop a text-free 16:9 painting and a hotspot file:

```
content/art/<room_id>/base.jpg
content/art/<room_id>/hotspots.json
```

Then delete `content/art/<room_id>/placeholder.json`. While that marker is present, the next build repaints the placeholder and overwrites `base.jpg`.

`hotspots.json` uses pixel coordinates on the painting. The page scales them with an SVG viewBox. The church files in `content/examples/eglise/` are the older specimen (item boxes or polygons, `text_areas.sign` and `text_areas.plaque`, helper `mnemonic_box`). They are for checking the format. They are not a live room.

A hotspot may include:

- `word_id` — a vocabulary id from `vocab.jsonl`
- `box` — `[x0, y0, x1, y1]`, and `polygon` when the clickable shape is not a rectangle
- `text_areas.sign` and `text_areas.plaque` — each with `box` and `text_box`
- `mnemonic_box` — optional. The build unions it into `box` so the page has one hotspot. New paintings can omit it
- `links` — doors, stairs and windows (`target`, `box`, `label`, `name`)
- `exits` — `forward` / `back`, and `left` / `right` when the painting has them. Older files may still say `prev` / `next`
- `text_areas` may set `role` to `building_name`, `street_name`, `room_name`, `verb_sign` or `direction`. Direction signs include the small arrow boards and the `-er` / `-ir / -re` side markers. A verb place may set `layout` to `tiered`
- `door_plaque` or `door_plaque_box` — where a verb’s preposition is set in type
- `mirror_box` — a reflexive verb
- `zoom_from` — a closer view, such as the bar counter (`room_id`, `box`, `label`)

Do not paint signs or labels into the image. The site draws them in the text boxes.

Optional French names for the hanging sign live in `content/signs.json`. A verb street uses the street’s name from `buildings.json` on the sign, and numbers the stretches from the room records.

Rebuild:

```bash
python3 scripts/placeholder_art.py
python3 scripts/build_data.py
npm run build
```

`placeholder_art.py` only fills rooms that still have no real painting.

## Conjugations

Verb tables (présent, passé composé, imparfait, futur, conditionnel, impératif, subjonctif) are generated once and stored in `data/cache/conjugations.json`. The site build reads that cache and does not need the conjugator installed. To refresh it after new verbs arrive:

```bash
python3 -m pip install -r scripts/requirements.txt
python3 scripts/build_data.py
```

A cache miss calls the conjugator and writes the new tables back. The group printed in the source data is not shown; the tables are.

## Pages

`.github/workflows/pages.yml` builds the site and deploys `dist/` with GitHub Pages when this lands on `main`. The workflow does not run from a pull request. In the repository settings, Pages needs to be set to GitHub Actions.

## Credits

Word lists, glosses, examples and dialogues are CC BY-SA 4.0. See `LICENSE-DATA.md` and the Credits page (`data/source/CREDITS.md`). The prayers are public-domain editions, named on each prayer page; the project’s own Divine Mercy translations stay with the word data. Baloo 2 and Patrick Hand are SIL Open Font License; the licence texts sit beside the font files in `src/fonts/`. A licence for the site code has not been chosen yet, so there is no code `LICENSE` file.

Interface copy is in `data/i18n.json` (`en` and `fr`). The Village guide is `data/guide.json`. Place records may add `name_fr` and `description_fr`; the build prints any that are still missing and the page falls back to English. The language switch defaults to English.
