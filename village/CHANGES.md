# v2 changes
* Milestone 1: v2 shell (index/app/style), painted village map, l'église (nef 17, parvis 13, sacristie 8,
  armoire 5 = 43 words). Other buildings appear as "bientôt" until their paintings pass QA.
* Maps: world map of the 16 sectors (`#/`) + one painted map per sector (`#/quartier/<slug>`) with click
  areas for all 65 buildings and 67 verb streets (memory-palace registry; cimetière and parc dropped).
  Buildings re-homed by building_id: église S11, mairie S06, école S01, garage S02, boulangerie S03, café S04,
  plage S09. Main-room exit and Back go to the sector map. `build_v2.py` copies building_id / sector_id /
  v1_room_id into the payload. Adjective cards (no article, `adjective · m/f`, center band).
* La plage (B29_plage, S09): plage 15, cap 6, dunes 11 = 32 words.
* La montagne (B26_montagne, S09): montagne 9, pentes 14, souche 7, glacier 10, etang 6 = 46 words.
* Le camping (B30_camping, S09): camping 14, tentes 14, souche 8 = 36 words.
* check_v2: narrow content exemption for the noun « la fumée » (fr_fumee_noun, gloss "smoke" = campfire
  smoke); its hook/scene/note must still pass a smoking/tobacco pattern; "tobacc" added to the blocklist.
* Back button (gate 19, user report Oct 31): Back now always goes straight outside - to the sector map from any room
  of a building, to the street from a side room of an `ST_` verb street - and never to the previous room. Replaces
  8012885f ("Back returns the way you came"); a zoom close-up still closes to its own room. Painted doors are the way
  between rooms. check_v2 --browser and tools/reachability.py follow the same rule.
* Gate 26 anatomy hotfix (Oct 31): 2x audit of every person/animal in Stade, Théâtre, Conservatoire, Jeux and Kiosque;
  10 crop-edit fixes (kiosque hub waiter 3rd arm, radio photographer 3rd hand, interview floating mug, gymnase climber
  extra arm, podium orphan hand, danse sheep missing arm + mime missing hand, théâtre wall painting merged dancers,
  chorale wrong-skin hand, fête farandole tangled arms); paintings, words and hooks kept, cards rebuilt.
* ⌂ Hub button (gate 19, Oct 31): a second strip button next to Back jumps to the first room / hub of the current
  building or verb street (tooltip = hub room name), hidden in the hub itself and on the maps. back_check.py and
  check_v2 --browser assert it.
* Offline cache (gate 27): `sw.js` is now network-first for every file, images and cards included (the cache is only
  the offline fallback), cache version bumped to `village-v3` so returning visitors' old caches are deleted on
  activate; the new worker takes over at once (skipWaiting/clients.claim; registered with updateViaCache 'none';
  the page reloads once if a new worker replaces an older one). Fixes returning visitors seeing old paintings that
  were repainted under the same filename (e.g. the kiosque titre waiter with three arms). `check_v2.py` checks the
  worker always, and with `--cache-base REF` fails a pack whose changed images keep the old cache version.
