# v2 changes
* Milestone 1: v2 shell (index/app/style), painted village map, l'église (nef 17, parvis 13, sacristie 8,
  armoire 5 = 43 words). Other buildings appear as "bientôt" until their paintings pass QA.
* Maps: world map of the 16 sectors (`#/`) + one painted map per sector (`#/quartier/<slug>`) with click
  areas for all 65 buildings and 67 verb streets (memory-palace registry; cimetière and parc dropped).
  Buildings re-homed by building_id: église S11, mairie S06, école S01, garage S02, boulangerie S03, café S04,
  plage S09. Main-room exit and Back go to the sector map. `build_v2.py` copies building_id / sector_id /
  v1_room_id into the payload. Adjective cards (no article, `adjective · m/f`, centre band).
* La plage (B29_plage, S09): plage 15, cap 6, dunes 11 = 32 words.
* La montagne (B26_montagne, S09): montagne 9, pentes 14, souche 7, glacier 10, etang 6 = 46 words.
* Le camping (B30_camping, S09): camping 14, tentes 14, souche 8 = 36 words.
* check_v2: narrow content exemption for the noun « la fumée » (fr_fumee_noun, gloss "smoke" = campfire
  smoke); its hook/scene/note must still pass a smoking/tobacco pattern; "tobacc" added to the blocklist.
