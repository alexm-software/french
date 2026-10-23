# Village v2 — painted scenes

Served at `/french/v2/`. The original village (`/french/`) is untouched.

* Every room is ONE integrated ink-and-gouache painting (1280×720); the mnemonic objects are painted in,
  and the page only adds invisible hotspots, a soft glow and white label pills (with articles).
* Text (glosses, hooks, examples, verb tables) is **not forked**: `scripts/v2/build_v2.py` reads the v1
  payloads in `village/assets/data/*.js` and `data/source/vocab.jsonl` at build time.
* Per building: `content/v2/<bld>/layout.json` (hotspot boxes in painting px, doors, zooms, scene notes),
  `village/v2/<bld>/*.jpg` (paintings + `cards/` crops), `village/v2/data/<bld>.js` (generated).
  A building becomes live on the map as soon as its data file exists (`scripts/v2/build_map.py`).
* Rules checked by `scripts/qa/check_v2.py [--browser]`: no overlapping hotspots/labels/doors, F left / M right,
  articles on labels, painted exit in every main room, painted door for every passage, Back from a sub-room
  goes to the main room, zoom objects visible in their parent, 7-tense verb cards without sideways scroll,
  content blocklist, planned word coverage.

Build: `python3 scripts/v2/build_v2.py && python3 scripts/v2/build_map.py && python3 scripts/qa/check_v2.py`
