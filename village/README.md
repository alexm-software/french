# Village v2 — painted scenes

Served at `/french/`. `/french/v2/` redirects here and keeps the hash.

* Every room is ONE integrated ink-and-gouache painting (1280×720); the mnemonic objects are painted in,
  and the page only adds invisible hotspots, a soft glow and white label pills (with articles).
* Text (glosses, hooks, examples, verb tables) is **not forked**: `scripts/v2/build_v2.py` reads the v1
  payloads in `data/v1-payloads/*.js` and `data/source/vocab.jsonl` at build time.
* Per building: `content/v2/<bld>/layout.json` (hotspot boxes in painting px, doors, zooms), optional
  `content/v2/<bld>/hooks.json` (v2 hook overrides), `village/<bld>/*.jpg` (paintings + `cards/` crops),
  `village/data/<bld>.js` (generated). Maps: `#/` = world map of the 16 memory-palace sectors (`map/world.jpg`),
  `#/quartier/<slug>` = painted sector map (`map/<slug>.jpg`) with every building and `ST_` verb street.
  Buildings are discovered at runtime: each sector map probes `data/<id>.js` (id = building_id without
  `Bnn_`) for every building in `data/map.js`; it is live if the file loads, otherwise "bientôt". A main
  room's exit and Back lead to its sector map.
  Adding a building never touches the shared shell — see `content/v2/README.md`.
* Rules checked by `scripts/qa/check_v2.py [--browser]`: no overlapping hotspots/labels/doors, F left / M right,
  articles on labels (adjectives: none, centre band), painted exit in every main room, painted door for every passage, Back from a sub-room
  goes to the main room, zoom objects visible in their parent, 7-tense verb cards without sideways scroll,
  content blocklist, planned word coverage.

Build: `python3 scripts/v2/build_v2.py && python3 scripts/v2/build_map.py && python3 scripts/qa/check_v2.py`
