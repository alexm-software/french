# Memory Village

A French vocabulary memory palace, from A1 to C2. You walk a map of sixteen quarters. Each word lives in a room, on a piece of furniture, or along a verb street, so the place brings the word back.

Rue des Saveurs (S04, cafés and restaurants) is the quarter under construction: Café de la Place, Restaurant Le Bon Goût, and the verb street Ruelle des Gourmets. The other quarters are on the map and marked coming soon. The long walk still begins in the beginner quarter; that door is drawn, and it is not open yet.

The upstairs room of Café de la Place (`R_cafe_02`) has a finished painting. Set `open_rooms` in `content/site.json` to `["R_cafe_02"]` when that room should be the only one you can walk; leave `open_rooms` out to build every room in the open quarters. A room listed in `content/vocab/*.jsonl` replaces the matching vocabulary entry for its card.

The pictures are placeholders. Signs and word labels are type, set in Cinzel and IM Fell English from the hotspot text areas, so they can be corrected without repainting.

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

Street contents are not hard-coded. Ruelle des Gourmets is read from `rooms.json` and `vocab.jsonl`. When a corrected verb list arrives, replace those files and rebuild. The current segments still show every verb that is in the data today, including a few that do not belong on a cooking street.

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
- `mnemonic_box` — the helper character, separate from the object
- `door_plaque` — where a verb’s preposition is set in type
- `mirror_box` — a reflexive verb
- `zoom_id` — a closer view, such as the bar counter

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

Word lists, glosses and prayers have their own licences. They are on the Credits page, and the source note is in `data/source/CREDITS.md`. Cinzel and IM Fell English are SIL Open Font License; the licence texts sit beside the font files in `src/fonts/`.
