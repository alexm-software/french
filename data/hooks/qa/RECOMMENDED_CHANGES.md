# Recommended changes: room placement and mnemonics (25 October 2026)

This file only makes proposals. Nothing in the word list, the room data or the hooks has been changed.

**What was reviewed**
- **The painted village (v2):** all 71 buildings and verb streets, 445 rooms, 3,705 word placements, read room by room.
- **The rest of the plan:** the 428 rooms in `data/source/rooms.json` (4,366 words) that v2 hasn't built yet.
- **Hooks:** the hook on every live word, checked against `data/source/vocab.jsonl`.

The S01 list in `MISFITS.md` is not repeated here. Those suggestions still stand.

Room references use `building/room`, the keys in `village/v2/data/*.js`. Unbuilt rooms use their plan id, such as `B06_marche/R_vegetables`.

## Summary

1. **Most misplaced words were placed by their English gloss, not their meaning.** The gloss shares a word with the room's theme:
   - *berge* (river **bank**) is in the bank.
   - *éleveur* (**stock**breeder) is with investments.
   - *polonais* (**Polish**) is in the repair shop.
   - *licencier* (to **fire** someone) is beside *embraser* (to set on **fire**).

   This one pattern explains most of the misfits, and fixing it is mechanical.
2. **Some glosses show the wrong sense for their room.**
   - The weather station teaches *éclair* as a pastry.
   - The forest teaches *feuille* as "sheet of paper".
   - The sacristy teaches *aube* as "dawn" when it means the alb.

   These need a gloss fix or a separate entry for the second sense, not a move.
3. **Overflow rooms.** Several "stump", "attic" and "rack" sub-rooms hold leftover abstract words with no tie to the building, so they can't be painted as a scene.
4. **A few grave or sensitive words sit in light-hearted places.**
   - *se suicider* is on **Rue du Soulagement** (Relief Street).
   - *tuer* is on the **hairdresser's** alley.
   - *gitan* is in the farmyard.
   - *racisme* is in the stadium.

   These should move first.
5. **Mnemonics.** 33 words have two different hooks in two rooms. Many hooks invent a pun where the word's own parts would do better (*toujours* = *tous les jours*), and 164 *-ment* adverbs each get a full scene when one rule would cover them. Part 2 has 10 worked rewrites.

---

## Part 1: Placement

### 1.1 Patterns behind the misfits

| Pattern | Examples (word: English gloss → room it landed in) | Fix |
|---|---|---|
| **English-gloss pun** | *berge* bank, *rivage* bank → bank; *éleveur* stockbreeder, *gisement* deposit, *générique* credits, *utilisateur* / *usager* user → bank; *ferme* "firm" → offices; *cocher* coachman → stadium; *béquille* kickstand → stadium; *lieue* league → stadium; *race* race → stadium; *parti* party → party hall; *gibier* game → games room; *atout* trump → council chamber; *foire* fair → civic hall; *vedette* star → sky; *écaille* scale → measures room; *plomb* lead → power room; *oubli* oversight → power room; *habillé* smart → quiz studio; *tir* shot → cinema; *étape* stage → theatre; *bande*, *bandeau*, *rabat* band → music hall; *manche* handle, *sonnette* handbell → hands room; *rubrique* heading → body room; *plaine* plain → sewing room; *polonais* Polish → repair shop; *obus* shell → beach; *parcelle* parcel → post office; *feuilleter* to leaf through → harvest street; *émouvoir* to move (emotionally) → removals street; *licencier* to fire → beside *embraser*; *sympathiser* to hit it off → hammer street | Move each word to the room of its actual meaning (tables below). Add a check that flags a word whose only link to its room is a shared English gloss word. |
| **Wrong sense glossed for the room** | §1.4 | Fix the gloss, or split the homograph into two entries |
| **Overflow sub-rooms** | `gare/aiguillage` and `gare/bagages` (cause, sorte, type, comparaison…), most of `couture/*` (coutume, ruse, révélation…), `labyrinthe/coeur` (socialement, idem, incognito…), `zone_artisanale/cabane` (tâche, reproche, complicité…) | Either rename the room to an honest abstract theme and paint it as one, or move the words to the abstract buildings that already exist: B34 humanités, B47 stade trophy hall, B63 pompiers problems room |
| **Grave or sensitive word in a light-hearted room** | §1.2 table A | Move to the text galleries (`B44_musee/R_text_*`) or a sober street, and use the plain wall-text treatment |
| **One id, two senses in two rooms** | *éclair* (pastry in the bakery, lightning at the weather station); *serviette* (napkin in the café, towel in the bathroom); *caisse* (till in the bakery, crate in the attic); *crêpe* (pancake, crêpe fabric); *croissant* (pastry, "increasing" in the Hercule tent) | Give each sense its own word id and card, so each one gets its own hook |

### 1.2 Live village (v2): proposed moves

**A. Move first: sensitive words in the wrong setting**

| Word | Now | Why | Proposed home |
|---|---|---|---|
| se suicider | `st_remedes/soulagement` (Rue du Soulagement) | A suicide verb on "Relief Street" reads as endorsement | Remove from the streets; plain wall text in `B44_musee/R_text_death`, or drop from the course |
| tuer | `st_souffle/coiffeur` (hairdresser's alley) | Killing in a comic hair salon | `ST_conflict` street (with *assassiner*, *massacrer*), wall text |
| gitan | `ferme/souchebasse` | An ethnic term in the farmyard | `B51_portraits/R_appearance_02` (peoples and regions), neutral treatment |
| prostitué | `bureaux/gardes` | In a gallery of babysitters and carpenters | `B44_musee/R_text_*`, wall text |
| mendiant | `camping/camping` | A beggar at the campfire | `B51_portraits/R_people_03` |
| virilité | `couture/atelier` | You excluded it from mnemonic hooks | Wall text in a sober gallery |
| viril, sensuel | `hercule/calme_guichet`, `hercule/arene_guichet` | Same | Same |
| accoucher (to give birth) | `st_navigateurs/balade` (a stroll) | No link | `hopital` or a body street (`ST_body`) |
| mutiler, périr | `st_liens/lambris` (wood panelling) | Grave verbs in a carpentry lane | `ST_conflict` |
| empoisonner | `st_reflets/miroirs` | No link | `ST_conflict` |
| sein | `monde/bagages` | It means breast and is used as *au sein de* (within); a luggage rack is the wrong place | Key it as the phrase *au sein de* in a prepositions room (`B02_ecole/R_prepositions_03`) |

**B. Other live misfits, by building**

| Building/room | Word: what it means | Proposed home |
|---|---|---|
| aeroport/aeroport | enlèvement: kidnapping (also removal or collection) | `B14_tribunal/R_police_04` |
| aeroport/aeroport | bond: a leap | `st_departs/galopins` (beside *bondir*) |
| aeroport/aeroport | essor: a boom or rapid growth | `banque/finances` |
| atelier_couleurs/mesures | carreau: a tile; diamonds (cards) | `maison/bains`, or the games room for the card suit |
| balance/combles | diplômé: a graduate | `bureaux/apprentis` (beside *diplôme*) |
| balance/combles | participe: a participle | `B02_ecole/R_grammar_verbs` |
| balance/combles | mi-temps: half-time; part-time work | `B47_stade/R_sports_03`, or `bureaux/table` |
| balance/combles | trimestre: a quarter or term | `horloge/calendrier` |
| balance/comptes | faculté: a university faculty (also a capacity) | `B33_lycee/R_school_02` (beside *fac*) |
| banque/guichet | grève: a strike | `bureaux/table` (with *chômage*, *congé*) |
| banque/guichet | épingle: a pin | `couture/atelier`, or `maison/penderie` |
| banque/guichet | profil: a profile | `B51_portraits` |
| banque/bureau | berge: a river bank | `riviere/crues` (with *rive*) |
| banque/bureau | rivage: a shore | `plage/plage` |
| banque/prets | contre-courant: a countercurrent | `riviere/crues` |
| banque/prets | générique: film credits | `B45_theatre/R_cinema_03` |
| banque/prets | gisement: a mineral deposit | `B35_sciences/R_geology` |
| banque/prets | utilisateur: a user | `informatique/etage` |
| banque/prets | débit | Keep; change the gloss to "debit; rate of flow" |
| banque/pupitre | usager: a user of a public service | `route/station` or `gare/gare` |
| banque/placements | hypermarché: a hypermarket | `rue_commercante/magasin` |
| banque/placements | éleveur: a livestock breeder | `ferme/manege` (beside *élevage*) |
| banque/placements | prospection: prospecting (mining) | `B35_sciences/R_geology` |
| bureaux/etage | ferme | It means a farm; move to `ferme/ferme` with the gloss "farm" |
| bureaux/classeur | reportage: a news report | `B49_kiosque/R_media_02` |
| bureaux/classeur | préfet: a prefect | `B13_mairie/R_admin_01` |
| bureaux/direction | compère: a sidekick or accomplice | `cirque/magie` |
| bureaux/direction | résignation: resigned acceptance, not resigning from a job | `B50_pavillons/R_emo_sad_02` |
| bureaux/services | charrette: a cart | `ferme/bassecour` |
| bureaux/services | tube: a tube; a hit song | `B46_conservatoire/R_music_01` (*un tube*) |
| bureaux/services | ambassadeur: an ambassador | `B13_mairie/R_admin_01` (beside *ambassade*) |
| bureaux/guichet | magicien: a magician | `cirque/magie` |
| bureaux/guichet | épicier: a grocer | `rue_commercante/reserve` |
| bureaux/guichet | psychiatre: a psychiatrist | `hopital` |
| bureaux/guichet | bourgeoisie: the middle class | `B34_humanites/R_history_02` |
| bureaux/apprentis | pompier: a firefighter | `B63_pompiers` |
| bureaux/gardes | forgeron, menuisier: a blacksmith, a carpenter | `zone_artisanale/atelier` |
| bureaux/gardes | inventeur: an inventor | `ingenierie/etabli` |
| bureaux/gardes | caniveau: a gutter | `route/carrefour` |
| bureaux/gardes | demoiselle: a young lady (also a damselfly) | `B51_portraits/R_people_01` |
| bureaux/tablette | canalisation: pipes | `maison/bains_buanderie` |
| bureaux/tablette | garderie: a nursery | `B33_lycee/R_school_02` (beside *crèche*) |
| bureaux/tablette | promoteur: a property developer | `maison/grenier_lucarne` (beside *immobilier*) |
| bureaux/savants | aristocrate | `B34_humanites/R_history_02` |
| bureaux/savants | diplomatie | `B13_mairie/R_admin_02` |
| bureaux/savants | résumé: a summary | `B34_humanites/R_literature_02` |
| cabinet/cabinet | fond: the bottom (of something) | `monde/cartes` (place words) |
| cabinet/mains | coiffure, coiffeur: a hairstyle, a hairdresser | `rue_commercante/mode` |
| cabinet/mains | foulard: a headscarf | `maison/dressing` |
| cabinet/mains | canne: a walking stick | `hopital/etage` |
| cabinet/mains | sonnette: a doorbell | `maison/jardin_facade` |
| cabinet/mains | manche: a handle | `garage/tools` (and see the homograph note in §1.4) |
| cabinet/mains | habileté: skill | `B51_portraits/R_character_05` |
| cabinet/mains | menotte: a little hand; usually handcuffs (plural) | `B14_tribunal/R_police_01` |
| cabinet/combles | rubrique: a newspaper section | `B49_kiosque/R_media_02` |
| cabinet/combles | manchette: a headline; a cuff | `B49_kiosque/R_media_02` |
| cabinet/combles | réticence: reluctance | `B50_pavillons` |
| cabinet/combles | complément: a complement (grammar) | `B02_ecole/R_grammar_general` |
| cabinet/combles | lifting: a facelift | `hopital/plateau` |
| cabinet/combles | facette: a facet | `atelier_couleurs/formes` |
| cabinet/combles | natte: a plait | `cabinet/visage` (hair) |
| cabinet/docteur | ardeur: fervour | `B50_pavillons/R_emo_love_01` |
| cabinet/bureau | filiation: descent, parentage | `maison/famille_album` |
| camping/camping | explosion | `B35_sciences/R_chemistry_01` |
| camping/camping | fumeur: a smoker | `B08_cafe/R_cafe_02` (beside *non-fumeur*) |
| camping/camping | incendie: a large fire | `B63_pompiers` |
| camping/camping | boucle: a buckle, a loop, a curl | `maison/penderie` (belt buckle) |
| camping/tentes | traîne: the train of a dress | `maison/dressing_malle` |
| camping/tentes | démarche: an administrative step; a gait | `B13_mairie/R_admin_01` |
| camping/souche | chamois | `montagne/glacier` |
| camping/souche | retrait: a cash withdrawal | `banque/bureau` |
| camping/souche | compartiment: a train compartment | `gare/etage` |
| camping/souche | littoral: the coastline | `plage/dunes` |
| ciel/souche | aura | `B44_musee/R_abs_senses_02` |
| ciel/souche | agitation | `B50_pavillons/R_emo_fear_04` |
| ciel/etoiles | déesse, divinité: a goddess, a divinity | `B34_humanites/R_literature_04` (mythology) |
| ciel/etoiles | sérénité: serenity | `B50_pavillons/R_emo_joy_02` |
| ciel/intemperies | pare-brise: a windscreen | `route/station` |
| concours/rates | septième, huitième: seventh, eighth | `B02_ecole/R_numbers2` (ordinals) |
| concours/potager_casier | reçu: a receipt | `rue_commercante/caisse` |
| concours/sante | usagé, vieillot: worn, old-fashioned | `brocante/casier` |
| concours/sante | illicite: illicit | `B14_tribunal` |
| couture/couture | curiosité: curiosity | `brocante/cabinet` (the *cabinet de curiosités*) |
| couture/couture | coutume: a custom | `B48_jeux/R_celebrations_01` (beside *tradition*) |
| couture/couture | ruse, révélation | `B34_humanites` |
| couture/vitrine | clin: only used in *clin d'œil* | Key it as *clin d'œil* in `cabinet/visage`; the proverb is already in `proverbes/theatre` |
| couture/vitrine | scrupule | `B14_tribunal/R_abs_moral_03` |
| couture/boudoir | merci: thank you | Already in `fontaine/politesse`; drop the duplicate |
| couture/theatre | plaine: a plain (flat land) | `ferme/champs` |
| couture/theatre | abord | `B44_musee/R_abs_senses_01` |
| couture/atelier | parure: a matching jewellery set | `rue_commercante/bijouterie` |
| couture/atelier | porte-bonheur: a lucky charm | `B48_jeux/R_games_01` (with *chance*) |
| couture/atelier | snobisme: snobbery | `B51_portraits/R_character_07` (beside *snob*) |
| couture/malle | aubaine: a windfall | `banque/placements` |
| couture/malle | avant-goût: a foretaste | `B09_restaurant/R_resto_kitchen_01` |
| couture/malle | vécu: lived experience | `horloge/fresque` |
| ferme/ferme | comte: a count (nobleman) | `B44_musee/R_heraldry_01` |
| ferme/souche | porcelaine: porcelain, china | `maison/cuisine` |
| ferme/souche | cavalerie: cavalry | `B16_caserne/R_military_02` |
| ferme/souche | corrida: a bullfight | Wall text, or drop |
| ferme/bassecour | pêcheur: a fisherman | `port/port` |
| ferme/souchebasse | donnée: a piece of data | `informatique/etage` |
| ferme/manege | clown | `cirque/clowns` |
| ferme/manege | chameau: a camel | `plage/dunes` (with *oasis*) |
| ferme/manege | dinosaure | `foret/soucheanimaux` |
| ferme/manege | aboiement: a bark | `maison/salon_panier` (the dog) |
| ferme/manege | paillette: a sequin | `rue_commercante/mode` |
| ferme/manege | argile: clay | `zone_artisanale/etabli` |
| ferme/manege | humus | `foret/souche` |
| ferme/manege | bourgade: a small town | `monde/monde` |
| ferme/coteau | agglomération: a built-up area | `monde/haut` |
| ferme/coteau | villageois: a villager | `monde/monde` |
| ferme/coteau | socle: a plinth | `B44_musee/R_art_02` |
| ferme/coteau | famine | Wall text (`B44_musee/R_text_*`) |
| ferme/coteau | éperon: a spur | `ferme/manege` |
| ferme/souchecoteau | extraction | `zone_artisanale/atelier` |
| ferme/souchecoteau | bailleur: a landlord | `B05_maison/R_entrance_03` (beside *loyer*, *locataire*) |
| foret/soucheloups | pic: a woodpecker (glossed "peak") | `foret/oiseaux` with the gloss "woodpecker", or a separate "peak" entry in `montagne/glacier` |
| foret/soucheloups | aventurier: an adventurer | `hotel/terrasse` |
| foret/oiseaux | bouge: a hovel | `maison/grenier_lucarne` (housing words) |
| foret/soucheoiseaux | cerf: a stag (not a bird) | `foret/loups` |
| foret/insectes | démon: a demon | `B41_presbytere/R_ch_catechism` (beside *diable*) |
| foret/insectes | pendule: a pendulum | `B35_sciences/R_physics_02` (*le pendule*; *la pendule*, the clock, is already in `horloge/cadran`) |
| foret/soucheinsectes | antichambre: an anteroom | `maison/maison` |
| foret/soucheinsectes | péripétie: a twist in a story | `B34_humanites/R_literature_03` |
| foret/soucheinsectes | betterave: a beetroot | `B06_marche/R_vegetables` |
| gare/gare | tribune: a grandstand | `B47_stade/R_sports_04` (beside *gradin*) |
| gare/gare | carrosse: a royal coach | `B44_musee/R_heraldry_01` |
| gare/gare | char: a carnival float; a tank | `B48_jeux/R_celebrations_02` (beside *carnaval*) |
| gare/etage | landau: a pram | `maison/famille` |
| gare/etage | dressage: horse training | `ferme/manege` |
| gare/etage | télégraphe | `mairie/poste` |
| gare/aiguillage, gare/bagages | 24 abstract nouns (cause, sorte, effet, comparaison…) | Structural; see §1.6 |
| hercule/* | funèbre: funereal | `B44_musee/R_text_death` |
| hercule/* | numérique, portable: digital, portable | `informatique` |
| hercule/* | conjugal | `maison/famille_portraits` |
| hercule/* | potable: drinkable | `riviere/riviere` |
| hercule/* | polaire: polar | `ciel/observatoire` |
| hercule/* | rocheux: rocky | `montagne/pentes` |
| hercule/* | frisé: curly | `B51_portraits/R_appearance_07` (beside *bouclé*) |
| hercule/* | épileptique | `hopital` |
| hercule/* | militant | `B13_mairie/R_politics_03` |
| hopital/plateau | exploitation: a farm business; exploitation | `ferme/coteau` |
| hopital/plateau | opérateur: an operator | `ingenierie/etabli` |
| hopital/etage | dérision: derision | `B50_pavillons/R_emo_fear_05` |
| hopital/etage | vétérinaire: a vet | `ferme/bassecour` |
| hopital/chariot | préjudice, dam: harm, detriment | `B14_tribunal/R_court_02` |
| hopital/chariot | déjection: droppings | `ferme/bassecour` (with *fumier*) |
| hopital/dentiste | illusion, perspective | `B44_musee/R_art_03` |
| hopital/dentiste | crête: a crest or ridge | `montagne/glacier` |
| hopital/dentiste | correspondance: a train connection; letters | `gare/gare` |
| hopital/dentiste | interlocuteur: the person you're talking to | `B49_kiosque/R_abs_speech_02` |
| hopital/optique | gomme: an eraser | Already in `ecole/trousse`; drop the duplicate |
| hopital/optique | girofle: clove (*clou de girofle*) | `B09_restaurant/R_resto_kitchen_02` (spices), keyed as *clou de girofle* |
| horloge/semaines | canicule: a heatwave | `ciel/intemperies` |
| horloge/salon | intérim: temping; an interim | `bureaux/table` |
| hotel/etage | tripe | `B06_marche/R_butcher_01` |
| hotel/etage | restauration: catering; restoration | `B09_restaurant/R_resto_room` |
| hotel/terrasse | émigration | `monde/etage` (beside *immigration*) |
| hotel/terrasse | récepteur: a receiver | `informatique/etage` |
| hotel/terrasse | pèlerinage: a pilgrimage | `B40_abbaye` |
| informatique/etage | safari: a safari (not the browser) | `foret/animaux` (with *savane*) |
| informatique/etage | mandataire: an agent or proxy | `B13_mairie/R_admin_02` (beside *procuration*) |
| ingenierie/ingenierie | puits: a well | `ferme/champs` |
| labyrinthe/coeur, labyrinthe/tour | intimement, socialement, séparément, exclusivement, spécifiquement, idem, incognito (not place words) | The opinion and manner adverbs in `B13_mairie/R_adv_logic_*`, or `cirque/*` |
| labyrinthe/tour | ci-joint: enclosed | `mairie/poste` |
| maison/cuisine_tiroir | brin: a blade of grass, a sprig | `maison/jardin` |
| maison/dressing_armoire | masque: a mask | `B45_theatre/R_theatre_02` |
| maison/penderie | corridor | `maison/maison` (beside *couloir*) |
| maison/penderie_commode | casque: a helmet | `route/parking` |
| maison/penderie_commode | fragment | `brocante/fouilles` |
| maison/penderie_portant | lien: a link | `st_liens` |
| maison/penderie_etagere | sueur: sweat | `B47_stade/R_sports_02` |
| maison/bains_buanderie | pipe: a tobacco pipe | Sober treatment, with *tabac* |
| maison/bains_buanderie | boue: mud | `route/carrefour` |
| maison/bains_buanderie | cendre: ash | `camping/camping` |
| maison/bains_buanderie | fouet: a whisk; a whip | `B09_restaurant/R_resto_kitchen_01` (whisk) |
| maison/grenier_lucarne | fondement: a basis | `B34_humanites/R_philosophy_02` |
| maison/jeux | jet: a jet (of water); a throw | `riviere/crues` |
| maison/jardin_voisins | passe: a pass (sport) | `B47_stade/R_sports_03` |
| maison/jardin_voisins | installation, établissement | `zone_artisanale/usine` |
| miroirs/* | douloureux: painful | `hopital` |
| miroirs/* | électrique, électromagnétique | `ingenierie` |
| miroirs/* | oriental: eastern | `monde/cartes` (beside *est*) |
| miroirs/* | conformiste, contraignant | `B51_portraits` |
| monde/bagages | mise: a stake; putting | `B48_jeux/R_games_01` (beside *pari*) |
| monde/etage | application: an app; diligence | `informatique/pause` |
| monde/boussole | cage | `maison/salon_panier` |
| monde/boussole | cachette: a hiding place | `maison/jeux` |
| monde/valises | metteur: only used in *metteur en scène* | Key it as the phrase in `B45_theatre/R_theatre_03` |
| monde/valises | aménagement: fitting out | `maison/grenier_lucarne` |
| monde/haut | berline: a saloon car | `route/parking` |
| montagne/pentes | tentation: temptation | `B41_presbytere/R_ch_catechism` |
| montagne/pentes | stand: a stall | `rue_commercante/ventes` |
| montagne/pentes | comble: the height of; *les combles*, the attic | `maison/grenier` |
| montagne/glacier | pique: a pike; spades (cards) | `B44_musee/R_heraldry_01` |
| montagne/etang | stratagème: a stratagem | `cirque/magie` |
| pharmacie/etagere | cohorte: a cohort | `B34_humanites/R_social_science_02` |
| pharmacie/etagere | filon: a seam of ore | `B35_sciences/R_geology` |
| pharmacie/etagere | appelant: an appellant | `B14_tribunal/R_court_03` |
| pharmacie/etagere | ponction: drawing fluid with a needle | `hopital/plateau` |
| plage/plage | obus: an artillery shell | `B16_caserne/R_military_04` |
| plage/plage | phase: a phase (of the moon) | `ciel/observatoire` |
| plage/plage | écho: an echo | `montagne/montagne` |
| plage/plage | cape: a cloak | `maison/dressing_malle` |
| plage/cap | vice | `B14_tribunal/R_abs_moral_04` (vices) |
| plage/cap | peignoir: a bathrobe | `maison/bains` |
| plage/dunes | glacier: a glacier; an ice-cream maker | `montagne/glacier` |
| plage/dunes | exode, contrée: an exodus, a land | `monde/etage` |
| port/bagages | antenne: an aerial | `B49_kiosque/R_media_01` (radio) |
| reparation/reparation | polonais: Polish | `B13_mairie/R_adj_relation_08` (nationalities) |
| reparation/cageot | lyonnais: from Lyon | `B13_mairie/R_adj_relation_08` |
| reparation/cageot | oral | `B02_ecole` |
| reparation/cageot | aride: arid | `plage/dunes` |
| reparation/cageot | pacifique: peaceful | `B50_pavillons/R_emo_joy_02` |
| reparation/cageot | terrien: earthling; landowning | `monde/monde` |
| reparation/pannes | infidèle: unfaithful | `B50_pavillons/R_emo_love_02` |
| route/route | dehors: outside | `labyrinthe/labyrinthe` (place adverbs) |
| route/parking | pétrolier: an oil tanker | `port/jetee` |
| route/consigne | ducat: a gold coin | `banque/banque` |
| route/consigne | colporteur: a pedlar | `rue_commercante/ventes` |
| rue_commercante/jouets | bourg: a market town | `monde/monde` |
| rue_commercante/fleuriste | fée: a fairy | `B34_humanites/R_literature_01` (*conte*) |
| rue_commercante/fleuriste | cocarde: a rosette | `mairie/mairie` (beside *drapeau*) |
| rue_commercante/cagette | marmotte: a marmot | `montagne/glacier` |
| rue_commercante/quincaillerie | enceinte | Usually means pregnant; the "enclosure" sense is rare. Move to `B51_portraits/R_people_04` (beside *grossesse*) |
| rue_commercante/quincaillerie | adhésion: membership | `B13_mairie/R_society_02` |
| rue_commercante/bac | adhérent: a member | `B13_mairie/R_society_02` |
| rue_commercante/bac | sabot: a clog; a hoof | `ferme/manege` |
| rue_commercante/ferronnerie | couchage: bedding | `camping/tentes` |
| rue_commercante/ferronnerie | rayure: a stripe; a scratch | `atelier_couleurs/toile` |
| rue_commercante/ferronnerie | liaison | `B34_humanites/R_linguistics_03` (French liaison) |
| rue_commercante/imprimerie | rêne: a rein | `ferme/manege` |
| rue_commercante/imprimerie | essuie-glace: a windscreen wiper | `route/station` |
| rue_commercante/imprimerie | correspondant: a pen pal | `mairie/poste` |
| rue_commercante/bijouterie | sonnerie: a ringtone; a bell's chime | `horloge/cadran` |
| rue_commercante/bijouterie | lustre: a chandelier | `maison/salon` |
| rue_commercante/bijouterie | poignet: a wrist | `cabinet/mains` |
| rue_commercante/bijouterie | éventail: a fan | `couture/boudoir` |
| rue_commercante/bijouterie | ronde: a patrol; a round | `B14_tribunal/R_police_01` |
| rue_commercante/mode | bourse: a grant; the stock exchange | `banque/placements` |
| rue_commercante/mode | composition | `B46_conservatoire/R_music_04` |
| rue_commercante/mode | pureté: purity | `B14_tribunal/R_abs_moral_02` |
| rue_commercante/parfumerie | palette | `atelier_couleurs/teintures` |
| rue_commercante/parfumerie | rondelle: a slice; a washer | `garage/tools` |
| rue_commercante/parfumerie | faction | `B13_mairie/R_politics_03` |
| rue_commercante/parfumerie | veilleur: a night watchman | `st_habitudes/veilleurs` |
| rue_commercante/parfumerie | icône: an icon | `informatique/pause`, or `eglise` |
| rue_commercante/coffre | enchanteur: an enchanter | `cirque/magie` |

**C. Verb streets: verbs with no link to their street's theme**

| Street | Verb | Proposed street |
|---|---|---|
| st_bagages/demenageurs | émouvoir: to move someone emotionally | `st_soupirs` |
| st_bagages/vacanciers | démissionner: to resign | A work street (`ST_making`) |
| st_bagages/lambins | entonner: to strike up a song | `ST_faith` (beside *psalmodier*) |
| st_bricoleurs/st_bricoleurs | conjuguer: to conjugate | `ST_cognition` (learning) |
| st_bricoleurs/selliers | siéger: to sit (on a council) | `ST_rule` |
| st_campeur/bouchons | ruer: to kick (of a horse) | A farm or animal street |
| st_ciel/moissons | feuilleter: to leaf through | `ST_communication` (reading) |
| st_ciel/jardiniers | exaspérer, chérir | `ST_emotion` |
| st_ciel/inondations | piloter: to pilot | `st_navigateurs` |
| st_flaneurs/st_flaneurs | prescrire: to prescribe | `ST_body` (remedies) |
| st_ingenieurs/vitraux | chiner: to hunt for bargains | `st_brocante` |
| st_lavoir/repasser | hériter: to inherit | `ST_existence` (with *léguer*) |
| st_navigateurs/balade | ficher: to file | `ST_communication` |
| st_paquets/yeux | injecter: to inject | `ST_body` |
| st_riviere/graines | enfanter, bronzer, carburer | `ST_body`, `st_campeur`, `route` |
| st_souffle/soigneurs | couronner, sacrer: to crown | `ST_rule` (rulers) |
| st_reflets/soupcons | scier: to saw | Already in `garage/garage`; drop the duplicate |

### 1.3 Unbuilt plan rooms: fix before they're painted

These rooms aren't in v2 yet, so moving words now costs nothing.

| Plan room | Word: what it means | Proposed home |
|---|---|---|
| B05_maison/R_bathroom | égout: a sewer | Road room |
| B05_maison/R_bathroom | germe: a germ | `B35_sciences/R_biology` |
| B05_maison/R_bedroom_01 | velours, satin | Fabrics (`rue_commercante/quincaillerie`) |
| B05_maison/R_laundry_01 | boudoir | `couture/boudoir` |
| B05_maison/R_laundry_01 | éboueur: a bin man | `zone_artisanale/centrale` |
| B05_maison/R_living | câble: a cable | `informatique` |
| B06_marche/R_bakery_01 | fric: money (slang) | `banque` |
| B06_marche/R_bakery_01 | couturier: a fashion designer | `couture` |
| B06_marche/R_bakery_02 | chalet | `montagne` |
| B06_marche/R_bakery_02 | lut: a lute | `B46_conservatoire` |
| B06_marche/R_bakery_02 | repli: a fallback; a fold | Abstract |
| B06_marche/R_butcher_01 | galop: a gallop | `ferme/manege` |
| B06_marche/R_butcher_02 | mousquetaire: a musketeer | `B44_musee/R_heraldry_02` |
| B06_marche/R_fruits_02 | apogée, benne, cantatrice, macadam, monstruosité, variante | Heights, `zone_artisanale`, `B46_conservatoire`, road room, `B50_pavillons`, abstract room |
| B06_marche/R_grocery_01 | bibelot: a knick-knack | `brocante` |
| B06_marche/R_grocery_01 | quille: a skittle | `B48_jeux` |
| B06_marche/R_grocery_01 | diabète | `B44_musee/R_text_medical` |
| B06_marche/R_grocery_01 | sucrerie | The gloss says "sugar refinery"; *les sucreries* (sweets) is the useful sense |
| B06_marche/R_grocery_02 | sieste: a nap | `maison/chambre` |
| B06_marche/R_vegetables | mèche: a wick; a lock of hair | Church candles or `B51_portraits` |
| B06_marche/R_vegetables | kiosque: a kiosk | `B49_kiosque` |
| B06_marche/R_vegetables | souplesse: suppleness | `B47_stade` |
| B06_marche/R_vegetables | tic: a tic | `B51_portraits` |
| B06_marche/R_vegetables | fuseau: a spindle; *fuseau horaire*, a time zone | `couture`, or `horloge` |
| B13_mairie/R_adj_relation_* | réfléchi: reflexive | Grammar |
| B13_mairie/R_adj_relation_* | paternel | Family |
| B13_mairie/R_adj_relation_* | piéton: pedestrian | Road room |
| B13_mairie/R_adj_relation_* | dixième: tenth | Ordinals |
| B13_mairie/R_adj_relation_* | gêné, misérable: embarrassed, wretched | `B50_pavillons` |
| B13_mairie/R_admin_01 | marque: a brand | `rue_commercante` |
| B13_mairie/R_admin_01 | certitude | `B14_tribunal` logic |
| B13_mairie/R_admin_01 | empreinte: a fingerprint | Police |
| B13_mairie/R_admin_02 | étendard: a banner | `B44_musee/R_heraldry` |
| B13_mairie/R_politics_01–05 | prince, reine, duc, princesse, vicomte, sénéchal, tsar, césar | `B34_humanites/R_history_*` or heraldry |
| B13_mairie/R_politics_01–05 | atout: a trump card | `B48_jeux` |
| B13_mairie/R_politics_01–05 | diva | `B46_conservatoire` |
| B13_mairie/R_politics_01–05 | podium | `B47_stade` |
| B13_mairie/R_politics_01–05 | commissariat: a police station | Police |
| B13_mairie/R_society_02 | foire: a fair | `B48_jeux/R_celebrations_02` |
| B14_tribunal/R_abs_moral_02 | fraîcheur, trésor | Elsewhere |
| B14_tribunal/R_abs_moral_02 | devise | Means a motto here, but the everyday sense is a currency; gloss both |
| B14_tribunal/R_abs_moral_05 | label, sceau: a quality label, a seal | `B13_mairie/R_admin_01` |
| B14_tribunal/R_adj_logic_04 | londonien, provençal | Nationality and region adjectives |
| B14_tribunal/R_adj_logic_04 | nuageux: cloudy | `ciel` |
| B14_tribunal/R_court_03 | effluve: a whiff | Senses cabinet |
| B15_poste/R_post_01 | philtre: a potion | `B34_humanites` (tales) |
| B15_poste/R_post_01 | parcelle: a plot of land, not a parcel | `ferme/champs` |
| B15_poste/R_post_01 | choc: a shock | Abstract |
| B33_lycee/R_school_02 | bourgeois | History |
| B33_lycee/R_school_03 | caste | Society, sober treatment |
| B34_humanites/R_history_03 | belote: a card game | `B48_jeux` |
| B34_humanites/R_social_science_01 | assurance: insurance | `banque` |
| B35_sciences/R_chemistry_* | concession, aspiration | Elsewhere |
| B35_sciences/R_geology | monseigneur | `B42_cathedrale` |
| B36_maths/R_measures_03 | écaille: a fish scale | `B06_marche/R_butcher_02` |
| B36_maths/R_measures_03 | baromètre | `ciel` |
| B44_musee/R_abs_power_* | plomb: lead (the metal) | Chemistry |
| B44_musee/R_abs_power_* | télécommande: a remote control | `maison/salon` |
| B44_musee/R_abs_power_* | oubli: forgetting | `B34_humanites/R_abs_mind_01` (memory) |
| B44_musee/R_abs_power_* | hâte: haste | `st_departs/presses` |
| B44_musee/R_adj_senses_* | canadien, téléphonique, syndical, départemental, consultatif | The rooms of their own topics |
| B44_musee/R_adj_senses_* | racial | Society, sober treatment |
| B44_musee/R_adj_senses_* | ivre, saoul: drunk | Café or wine cellar |
| B44_musee/R_text_crime_* | battement: a heartbeat; a drumbeat | `cabinet` or music |
| B44_musee/R_text_crime_* | impasse: a dead end | Road room |
| B44_musee/R_text_crime_* | abattage: felling (trees) | `foret` |
| B44_musee/R_text_crime_* | stabilité: stability | Abstract |
| B44_musee/R_text_death | tortueux: winding | Road or river |
| B44_musee/R_text_medical | tension: blood pressure | `hopital` |
| B45_theatre/R_adj_mind_03 | habillé: dressed up | `maison/dressing` |
| B45_theatre/R_adj_mind_03 | chrétien | `B43_concorde` |
| B45_theatre/R_cinema_* | record | `B47_stade` |
| B45_theatre/R_cinema_* | torrent | Mountain or river |
| B45_theatre/R_cinema_* | tir: a shot (firing) | Military |
| B45_theatre/R_cinema_* | réclusion: imprisonment | `B14_tribunal` |
| B45_theatre/R_theatre_02 | cirque | `cirque` |
| B45_theatre/R_theatre_02 | étape: a stage of a journey | Road room |
| B45_theatre/R_theatre_02 | sorcier: a sorcerer | Tales |
| B45_theatre/R_theatre_03 | samba | Music |
| B45_theatre/R_theatre_03 | revendication: a demand | Society |
| B45_theatre/R_theatre_03 | rebut: scrap | `brocante` |
| B46_conservatoire/R_music_* | bandeau: a headband | Dressing room |
| B46_conservatoire/R_music_* | pionnier: a pioneer | History |
| B46_conservatoire/R_music_* | bande | Means a tape or a gang |
| B47_stade/R_sports_02 | race: breed; ethnic race, never a running race | Animals (breed sense), with a false-friend note |
| B47_stade/R_sports_02 | racisme | Society, sober treatment |
| B47_stade/R_sports_02 | cocher: a coachman | Next to *fiacre* in `route/parking` |
| B47_stade/R_sports_03 | lieue: a league (distance) | `B36_maths/R_measures_03` (beside *aune*) |
| B47_stade/R_sports_04 | béquille: a crutch | `hopital` |
| B47_stade/R_sports_04 | faïence: earthenware | Kitchen |
| B48_jeux/R_celebrations_02 | parti: a political party | `B13_mairie/R_politics_03` |
| B48_jeux/R_games_01 | gibier: game meat | `foret/loups` |
| B48_jeux/R_games_02 | biscotte: a rusk | Grocery |
| B48_jeux/R_games_02 | échelon: a rung; a grade | Offices |
| B49_kiosque/R_media_02 | serre: a greenhouse | The `serre` building already exists |
| B49_kiosque/R_media_03 | cadran: a dial | Already in `horloge/cadran` |
| B49_kiosque/R_media_03 | parasite | Biology |
| B50_pavillons/* | optimisme | Out of the fear room, into joy |
| B50_pavillons/* | gladiateur | `hercule/arene` |
| B50_pavillons/* | banderole: a protest banner | Society |
| B50_pavillons/* | merci: mercy | `B39_eglise/R_ch_confessional` |
| B50_pavillons/* | résurrection | Catechism |
| B51_portraits/R_character_09 | 9 medical adjectives (cardiaque, respiratoire, chirurgical, clinique…) | `hopital` |
| B51_portraits/* | climatique | `ciel` |
| B51_portraits/* | fumé: smoked | Butcher |
| B51_portraits/* | laitier: dairy | Grocery |
| B51_portraits/* | raciste | Sober treatment |
| B63_pompiers/R_abs_problem_* | coffre-fort: a safe | `banque` |
| B63_pompiers/R_abs_problem_* | caution: a deposit | `banque` (and add a false-friend note) |
| B63_pompiers/R_abs_problem_* | amende: a fine | Police |
| ST_conflict | taper: to type | `ST_communication` |
| ST_conflict | garer: to park | Road street |
| ST_conflict | freiner: to brake | Road street |
| ST_conflict | déshabiller: to undress | `st_sommeil` |
| ST_conflict | sympathiser: to hit it off | `ST_social` |
| ST_conflict | décrypter: to decode | `ST_communication` |
| ST_communication | ramer: to row | `port` |
| ST_communication | enfiler: to thread | `couture` |
| ST_communication | tripler: to triple | Maths |
| ST_communication | miauler: to meow | Pets |
| ST_communication | rémunérer: to pay | Offices |
| ST_body | hypothéquer: to mortgage | `st_ecus` |
| ST_play | noyer: to drown | Sober street |
| ST_play | carreler: to tile | Building trades |
| ST_play | coloniser: to colonise | History |
| ST_play | harceler: to harass | `ST_conflict` |
| ST_rule | licencier: to fire (from a job) | Offices; it sits beside *embraser* (to set on fire) only through the English word "fire" |
| ST_rule | enflammer, embraser: to set on fire | Fire verbs |
| ST_possession/seg011 ("Rue des Pharmaciens") | exciter, implorer | No link to pharmacies; regroup |

### 1.4 Gloss or sense fixes (keep the room, fix the word)

| Word | Room | Shown as | Should be |
|---|---|---|---|
| éclair | `ciel/ciel` | éclair (cream pastry) | lightning: give it its own entry, separate from the pastry |
| feuille | `foret/arbres` | sheet of paper | leaf (paper is the post-office sense) |
| pic | `foret/soucheloups` | peak | woodpecker (or move it, see §1.2) |
| aube | `eglise/armoire` | dawn | alb (vestment) |
| bise | `ciel/souche` | kiss on the cheek | the north wind (*la bise*) |
| hôtel | `hotel/hotel` | mansion, town house | hotel (the mansion sense is *hôtel particulier*) |
| vacance | `hotel/hotel` | vacancy | key it as *vacances* (holidays) |
| serviette | `maison/bains` | napkin | towel (needs a separate sense entry from the café napkin) |
| caisse | `maison/grenier` | till | crate, box |
| ferme | `bureaux/etage` | firm | farm (move it, §1.2) |
| capteur | `ingenierie/etabli` | catcher | sensor |
| emprise | `serre/etage` | expropriation | hold, grip, influence |
| débit | `banque/prets` | flow | debit; rate of flow |
| croissant | `hercule/grenier` | increasing | Fine, but it shares the pastry's spelling; make sure the card can't be mistaken for the pastry's |
| peine | B14 R_court_01 | sorrow | (legal) sentence, penalty; also sorrow |
| parquet | B14 R_court_02 | parquet | the public prosecutor's office (and parquet flooring) |
| tampon | B13 R_admin_02 | plug | rubber stamp |
| faisceau | B35 R_physics_02 | fasces | beam (of light) |
| facteur | B36 R_math_01 | postman | factor (maths); postman belongs in the post office |
| répétition | B45 R_theatre_02 | repetition | rehearsal |
| cascade | B45 R_cinema_02 | waterfall | stunt (in film); waterfall belongs by the river |
| peloton | B47 R_sports_04 | small ball | the pack (cycling); a platoon |
| régime | B34 R_history_02 | diet | regime (history sense); diet elsewhere |
| vierge | B39 R_ch_lady_chapel | blank | Keep only *la Vierge*; drop the "blank page" duplicate |
| office | B40 R_ab_choir | pantry (second entry) | Drop the pantry sense here, or move it to the kitchen |

**Words that only exist inside one phrase:** *marre, guère, clin, par-ci, metteur, tombée, lors, afin, affût*, and *sein* in the sense "within". Teach and hook each as its phrase: *en avoir marre, ne… guère, clin d'œil, par-ci par-là, metteur en scène, la tombée de la nuit, lors de, afin de, à l'affût, au sein de*.

The same goes for verbs that are only ever reflexive: *s'acharner, s'adonner, se démener, se dévouer, s'endetter, s'enrhumer, s'approprier, s'avérer, se cramponner*. Show them with *se*.

### 1.5 The same word painted in two rooms

59 words appear in two v2 rooms; 33 of those have a different hook in each room. Examples:
- *chiffre* in `balance` and `ecole/pupitre`.
- *ligne* in `atelier_couleurs/formes` and `ecole/pupitre`.
- *four*, *tablier*, *boîte*, *réveil*, *tranche* in the bakery and in `maison`.

Pick one home per word, or keep both placements and share a single hook (see Part 2, rule 1).

### 1.6 Structural suggestions

- **Rooms that are lists, not scenes.** `gare/aiguillage` and `gare/bagages` hold 24 abstract nouns (cause, sorte, effet, comparaison…). The switching-yard metaphor ("points = choices") only works if the room says so. Alternatively, move these into `B34_humanites/R_philosophy_*` and `R_linguistics_01`, and give the station real station words. The same applies to most of `couture/*`: its abstract nouns (manner, charm, curiosity…) don't belong in a sewing room. Bring in the plan's actual sewing words (*coudre, fil, aiguille, dé à coudre, ourlet, patron* in its sewing sense) and send the abstract ones to B34 and B50.
- **Adverb buildings.** `cirque` (10 rooms) and `balance` hold most of the 164 *-ment* adverbs in v2. That's fine as a building, but each one doesn't need its own scene. See rule 3 below.
- **Add a placement check** to `scripts/qa/check_v2.py`. It would flag a word whose room theme matches its English gloss only through a shared word (bank, stock, firm, coach, fire, party, star, band, scale, lead, shot, stage, league, race…). It would have caught most of the table above.

---

## Part 2: Mnemonics

`HOOK_PROPOSALS.md` already covers gender, broken templates and irregular verbs. These rules come from reading every live v2 hook.

1. **One hook per word, everywhere.** 33 words have different hooks in different rooms. A learner who meets *chiffre* twice learns two unrelated pictures. Keep the better one, and adapt only the setting when the room changes.
2. **Use the word's own parts before inventing a pun.** Compounds and transparent words remember themselves:
   - *tou-jours* (all days)
   - *main-tenant* (holding in the hand)
   - *au-jour-d'hui*
   - *pour-boire* (already done well)
   - *d'avantage*
3. **Teach the *-ment* rule once.** feminine adjective + *-ment* = *-ly*. Hook the adjective (*lent* → *lentement*), not each adverb. That replaces 164 separate scenes with one rule plus the adjective hooks the learner mostly already has.
4. **Real cognates get a plain card:** the cognate, the sound trap and the gender. Don't force a pun. A forced pun on a cognate (*période* as an accordion "PAY-RYOD") is harder to remember than the English word it already resembles.
5. **Phrases get a chunk-by-chunk translation, not a whole-phrase pun.** Puns built from the whole sound of a phrase ("COME ON, TALLY, VOO") don't hold.
6. **The sound-alike and the meaning must meet in one action.** Many hooks put the sound object and the meaning object side by side, like a stingray named Ray beside an elephant's ear. Make one act on the other.
7. **A moved word needs its hook redrawn.** Many hooks describe their room's painting ("in the bank hall", "on the chart"), so moving a word means rewriting that sentence.

### 2.1 Ten hooks to improve

| # | Word (room) | Current hook | What's wrong | Proposed hook |
|---|---|---|---|---|
| 1 | **chiffre** (`balance/balance`, `ecole/pupitre`) | Balance: *"SHEEFR" ≈ "CHEF + R": a CHEF counts on his fingers, one DIGIT at a time.* École: *The wooden DIGIT 7 wears a CHEF's hat.* | Two different hooks, and both are rated weak. "Chef + r" doesn't point to digits. | **Same root as English CIPHER** (both come from the Arabic for "zero"). A spy's codebook: a page of nothing but DIGITS, a secret cipher. *Un chiffre* is a single digit (0–9); 25 is *un nombre* with *deux chiffres*. Say SHEEFR. |
| 2 | **maintenant** (`horloge/escalier`) | *"MAN-TEN-NAN" ("mant-NAHN"): Nan slams the big red button with her stopwatch held up. NOW!* | The respelling disagrees with the card (man-tuh-NAHN), and the pun is three unrelated sounds. | **MAIN (hand) + TENANT (holding):** what you're holding in your hand is happening NOW. A hand holds up a stopwatch reading 0:00: *maintenant!* Say man-tuh-NAHN (in speech often mant-NAHN). |
| 3 | **aujourd'hui** (`horloge/alcove`) | *"OH, SURE, DWEE!": a girl with fresh-picked daisies and a sunny mug. This very day, TODAY.* | "Dwee" means nothing, and daisies don't say "today". | **You already know *jour* from *bonJOUR*.** *Au jour d'hui* = "on the day of today", today said twice. A tear-off calendar shows one page stamped JOUR, with today's date circled in red. Say oh-zhoor-DWEE. |
| 4 | **toujours** (`horloge/escalier`) | *"TWO, SURE" ("too-ZHOOR"): two old sweethearts on a bench, holding hands as they ALWAYS have.* | Rated weak. "Two, sure" has no link to "always", and the "still" sense is missing. | ***Tous les jours* (all the days) squeezed into one word = ALWAYS.** A calendar with every single day ticked. Second sense: *il pleut toujours* = it's STILL raining (the rain on every day). Say too-ZHOOR. |
| 5 | **comment allez-vous ?** (`fontaine/salutations`) | *"COME ON, TALLY, VOO?": a gentleman tips his top hat to a lady holding a TALLY counter.* | A whole-phrase pun with a tally counter in it. Learners need the parts. | **Chunk it:** *comment* (how) + *allez* (go) + *vous* (you) = "How go you?", like old English "How goes it?". The *t* of *comment* links: koh-mahn-tah-lay-VOO. Picture: a gentleman tips his hat at the fountain. *Vous* is the polite form; *ça va ?* is the casual one. |
| 6 | **davantage** (`balance/cageot`) | *The little girl licks her ice cream by DA VAN: MORE, from the ice-cream VAN!* | Rated weak, and it misses the real link. | **Hear ADVANTAGE inside it** (it comes from *d'avantage*). The side with the ADVANTAGE has MORE: a tug-of-war where one team has more players. *Davantage de temps* = more time. Say dah-vahn-TAHZH. |
| 7 | **mise** (`monde/bagages`) | *A grey mouse carefully PUTS DOWN a wedge of CHEESE on the chart: "chEESE" with an M, "MEEZ".* | Rated weak. A respelling trick on "cheese", and no link to the bet sense. | **From *mettre* (to put): *mis, mise* = put.** A chef's MISE EN PLACE, everything PUT in place. At the card table, *la mise* is the stake you PUT down. (Move the word to the games room; see §1.2.) |
| 8 | **ciel** (`ciel/ciel`) | *Look up at the SKY: you can see an L-shaped ("SYEL") cloud floating in the blue.* | The letter-shape pun is weak, and the link to English is ignored. | **Same Latin root as CEILING and CELESTIAL:** the SKY is the world's ceiling. Paint the observatory's ceiling as open sky. Also heaven: *au ciel*. Say SYEHL. |
| 9 | **doucement** (`cirque/cirque`) | *A circus strongman cradles a baby lion GENTLY ("doo-suh-MAHN"), rocking it softly to sleep.* | Rated weak: there's no sound link at all, only the meaning. | ***Doux/douce* (soft, sweet; think DULCET) + *-ment* (-ly) = SOFTLY, GENTLY.** The strongman whispers "*douce*-MENT" as he lowers the lion cub into its basket. This is the model for rule 3: hook *doux* once, and every *-ment* adverb follows. |
| 10 | **oreille** (`cabinet/visage`) | *A friendly stingray RAY ("oh-REHY") watches from its glass tank beside a baby elephant fanning out one huge floppy EAR.* | Sound object and meaning object side by side (rule 6), and two animals to remember. | **"OH, RAY?"** Ray cups his hand behind his EAR: "Oh, Ray? Speak up, I can't hear you!" One person, one action, and the same root as English *aural*. Say oh-REHY. |

**Others that would benefit from the same treatment:**
- *période*: a forced pun on a true cognate (rule 4). The trap worth teaching is the gender: LA période.
- *demain*: the hook needs a "tomorrow" anchor, for example an alarm clock set for the MORNING; *demain* comes from *de mane*, "from the morning".
- *secteur*: rated weak; the pizza slice works, but the hook could be cut to a plain cognate card.
- *vol*: the hook covers only "flight". Add the second sense (theft), which shares the spelling and the hook's vole.
- *lentement*: it should follow from *lent* (rule 3).

---

## Suggested order

1. **Move the words in §1.2 A.** That means 11 sensitive placements, *se suicider* first.
2. **Make the gloss fixes in §1.4.** Each is one line of data and needs no repainting.
3. **Settle §1.3 before those buildings are painted.** It costs nothing now.
4. **Add the placement check** described in §1.6.
5. **Rule 1 (one hook per word):** merge the 33 double hooks.
6. **Rule 3 (*-ment* adverbs):** decide whether to pursue it, since it changes how `cirque` and `balance` are painted.
7. **Work through the rest of §1.2 B and C building by building** whenever a building is next repainted.
