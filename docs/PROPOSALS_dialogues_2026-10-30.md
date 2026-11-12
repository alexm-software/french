# Conversations review: proposed improvements (30 October 2026)

Nothing here has been changed yet. Each item says what is wrong, an example, and the fix proposed.

## What was reviewed

The sources are the 778 written conversations, holding 6,878 lines in all:

| Source | Conversations | Written by |
|---|---|---|
| `data/source/village_dialogues.json` (V_) | 63 | for the village cast |
| `data/source/conversations.json`, C_R_ | 423 | per room |
| `data/source/conversations.json`, C_ST_ | 292 | one per street "segment" verb list |

Three kinds of review were done:
- **Mechanical checks** on all 778 conversations: levels, cast names, fillers, typography, English, alcohol, duplicates.
- **Read in full:** the 408 conversations that were on the site at review time.
- **Read in part:** every third one of the 370 that are written but not shown (124 conversations).

The English was checked mechanically, plus spot checks.

**What works:** the 63 village scenes (V_) are the model to follow. They have:
- one recurring cast;
- consistent facts across scenes (the baguette costs €1.20 in two scenes, M. Blanc fixes the church clock);
- natural A1–A2 French and small jokes that land;
- cultural touches, such as the Fête des Lumières lanterns and the salad you fold rather than cut.

The problems are almost all in the bulk-written C_ sets.

## The main problems, in order of impact

### 1. About half the written conversations never reach the site

- **The count:** 370 of 778 written conversations are not placed in any room. A rebuild now shows 410, because the two chapel scenes became placeable when the chapel was built.
  - 335 are waiting for rooms that aren't built yet. That's expected: they'll appear as those rooms are built.
  - 33 can never be placed. `build_extras.py` puts a conversation in the room that holds at least two of its words, and these have at most one per live room. For example, the fruit-market scene `C_R_fruits_01` has only "pomme" live.
- **Fix:** place a conversation by its `room_id` when that room is live, and only then by word overlap. Re-target the 33 at words that are live.
- **Also:** the talk data had gone stale after the chapel rooms were built. Add `build_extras.py` to the build steps that run after any room is built.

### 2. Cast names are reused for other people (155 conversations, 71 on the site)

**What the cast is:** the village cast is fixed in `village_dialogues.json`:
- Léa (9), Tom (11), Inès (Léa's best friend);
- Maman (Claire) and Papa (Marc);
- Papi Henri; Mme Roux, the baker's wife;
- Karim the waiter, Julien the mailman, Sophie at the post office, and so on.

**What goes wrong:** the C_ sets reuse those names for unrelated people.

| Conversation | Who carries a cast name |
|---|---|
| `C_R_adv_place_02` | Léa and Tom (siblings in the cast) are adult roommates "intimement liés au lycée" |
| `C_R_adj_senses_05` | Léa is pregnant |
| `C_R_bank_counter_03` | Léa takes out a mortgage "avec nos deux salaires" |
| `C_R_adj_quality_03`, `C_R_adv_manner_04` | Léa and Inès get married |
| `C_R_school_03` | Inès is Tom's university-student sister |
| `C_R_road_04` | Mme Roux is on vacation with a caravan |
| `C_ST_movement_seg015` | Mme Roux announces that "la boulangère" (herself) gave birth at home |
| `C_R_polite` | Tom is a British exchange student who meets "Mme Roux" in a canteen |
| `C_R_greet` | Karim is a father of a 7-year-old |
| `C_R_shop_general_02` | M. Blanc runs a furniture shop |

- **Generic family names:** "Maman" (35 conversations) and "Papa" (34) are other people's parents. In `C_R_body_04`, "Papa" is an elderly man with a grown daughter.
- **A grandmother who has died:** a living "Mamie" appears in 33 conversations, and "Papi" (not Papi Henri) in more. In the cast, Mamie has died (`V_eglise_eglise_01`).
- **The church:** the village church is given another priest, "le père Michel" (`C_R_ch_sacristy`). The bell-tower clock is fixed by a clockmaker for an unnamed mayor (`C_R_time_clock_02`), while `V_eglise_clocher_02` has M. Blanc fix it for Mme Lefort.

**Why it matters:**
- It breaks the story the learner follows.
- With recorded audio, each speaker name gets one voice. An adult Léa would speak in the child's voice, and every "Maman" would sound like Claire.

**Fix:**
- In C_ conversations that aren't about the village cast, rename each speaker that collides to a fresh name of the same gender and age. This can be scripted, with a name pool and a fixed seed so it is repeatable.
- Where a scene does belong to the village (the bakery, the café, the church, the mayor), make it consistent instead: Mme Lefort for "la maire", Père Antoine for the priest, M. Blanc for repairs.
- Add a check: a cast name may appear only in V_ scenes or in scenes marked `"village": true`, and a cast child only at A1–B1, in a child's situation.

### 3. Level labels measure rare words, not difficulty

**How the label is made:** a C_ conversation's level is the 75th percentile of its words' CEFR levels. So a simple scene with one rare word is labeled high:
- the picnic `C_R_insects` is B2, because of "démon" and "puce";
- the weaving scene `C_ST_making_seg009` is C2, with lines like "On recycle !" and "C'est beau.".

**How often:**
- 62 of the 216 C1/C2 conversations have a median line under 8 words.
- The median line is shorter at C2 (7.6 words) than at A1 (8.7).

**Fix:**
- Label by how hard the language is: line length, tenses (subjunctive, conditional, passé simple), connectors, and the share of words above A2.
- Show rare words as their own tag ("C1 words · A2 language"), or cap the label at language level plus one.
- Learners filter by level, so this matters as much as content.

### 4. Target words are packed one per line, so many scenes read like drills

**What happens:** many scenes force every target word into the dialogue, one per line, often in the last lines, where they become non sequiturs. Worst are the C_ST "segment" scenes (292 in all, 121 on the site):
- eight short lines, each built around a rare verb;
- 111 end on a line of two words or fewer, 80 of them a bare filler ("Merci." / "De rien." / "Bravo !" / "Parfait.").

Examples:
- "Il est moralement fatigué aussi" (`C_R_adv_manner_05`)
- "Je l'ai acheté avec lucidité… c'est un agrément pour tes poignets !" (`C_R_abs_beauty_03`)
- "Au-dedans, je suis un peu nerveux" (`C_R_adv_place_02`)
- "Mon fils pilote un drone… Ma poule couve ses œufs au grenier" (`C_ST_nature_seg005`)
- "Tu essaies de me flatter pour gagner !" (`C_ST_routine_seg007`)
- "Le ciel rosit, regarde le coucher de soleil" (`C_ST_making_seg013`)
- "Il y a une bonne ambiance à l'école sur ce sujet : … la qualité de l'air et la respiration." (`C_R_energy_01`, which ends there with no reply)

**Fix:**
- At most 4–5 target words per scene. A word that doesn't fit the situation goes to another scene or to the card's example.
- Rewrite the C_ST scenes as fewer, longer scenes with a situation and a small turn, as the V_ scenes have. Start with the 121 that are live.
- End on a line that closes the situation, not on a filler.
- Cut the "Ha ha !" reflex: it appears in 235 of 778 conversations (232 of the 715 C_ ones, 3 of the 63 V_ ones).

### 5. French errors and misused words (fix one by one)

Found by reading.

| Conversation | Now | Proposed |
|---|---|---|
| `C_R_pharmacy` | jamais de **drogue** sans ordonnance | jamais de **médicament** (drogue = illegal drugs) |
| `C_R_occupations_05` | le **résumé** du nouveau stagiaire | le **CV** (false friend) |
| `C_R_abs_quantity_02` | Mais **la maison**, c'est meilleur | Mais **le fait maison**, c'est meilleur |
| `C_R_post_01` | l'adresse **au dos de l'enveloppe** (a parcel) | l'adresse **sur le paquet** |
| `C_R_character_01` | notre **principale** contact | notre **principal** contact |
| `C_ST_possession_seg004` | (a lamp) je n'ai plus besoin **d'elle** | je n'**en** ai plus besoin |
| `C_ST_nature_seg009` | la montagne **a enfanté** une souris | la montagne **a accouché d'**une souris |
| `C_ST_movement_seg015` | mon chien **oscille** la queue | **remue** la queue |
| `C_ST_movement_seg021` | Vous **trottez** tous les jours ? / Ne **refoulez** pas la douleur | Vous **courez** / N'**ignorez** pas la douleur |
| `C_ST_rule_seg012` | Le maire a validé **la loi** | Le maire a signé **un arrêté** |
| `C_ST_rule_seg009` | Je vais le **dénoncer** à l'agence | le **signaler** |
| `C_ST_commerce_seg004` | « Vendu ! » **s'écrie-t-il** / il **débat** le prix / il **revendique** une réduction | narration can't be spoken: "Bon, vendu !"; il **marchande**; il **demande** une réduction |
| `C_ST_commerce_seg007` | Vous **monnayez** vos légumes ? | Vous **vendez** |
| `C_ST_change_seg010` | On **reconduit** la leçon mardi ? | On **refait** une leçon mardi ? |
| `C_ST_change_seg007` | Il veut **stopper** le solfège | **arrêter** |
| `C_ST_change_seg012` | Le soleil **s'abaisse** plus tôt | **se couche** plus tôt |
| `C_ST_change_seg018` | Le vent **excède** mes forces | Le vent est **trop fort** pour moi |
| `C_ST_control_seg018` | **Délie** tes muscles | **Échauffe-toi** |
| `C_ST_movement_seg017` | J'ai **immigré** au Canada (said in France) | J'ai **émigré** au Canada / Je suis partie vivre au Canada |
| `C_ST_movement_seg020` | Tu as **musé** dans les villages ? | Tu as **flâné** |
| `C_ST_emotion_seg001` | Ça ne le concerne pas, ça ! | Ce n'est pas une question de déranger ! |
| `C_ST_communication_seg022` | Tu vas **éditer** l'article ? | **publier** |
| `C_ST_communication_seg025` | Je **languis de** voir des changements | **Il me tarde de** voir |
| `C_ST_conflict_seg007` | Le chat s'était **emprisonné** / Il a **ruiné** son pyjama | s'était **enfermé** / Il a **abîmé** son pyjama |
| `C_ST_perception_seg006` | Je **soupçonne qu'il** vient voler | Je **le soupçonne de** venir voler |
| `C_ST_nature_seg001` | on **fait brûler** un bon feu | on **fait** un bon feu |
| `C_ST_movement_seg006` | Tu pars **en** vélo ? | **à** vélo |
| `C_R_adj_state_05` | Il est **gelé**, ou quoi ? (computer) | Il est **planté** ? |
| `C_R_adj_mind_05` | un produit **organique** | un produit **bio** |
| `C_R_adj_relation_05` | ce temps **misérable** | ce temps **pourri** |
| `C_R_linguistics_03` | une **extension** de stage | une **prolongation** de stage |
| `C_R_harbour_01` | un **vaisseau** de la marine | un **navire** de la marine |
| `C_R_harbour_02` | le premier **arrivant** de la course | le premier **arrivé** |
| `C_R_birds_02` | (baby swans) des **poussins** | des **petits** (des cygneaux) |
| `C_R_adj_time_07` / `C_R_adj_time_03` | cuisine **germanique** / vacances **pascales** / salle **obscure** | cuisine **allemande** / vacances **de Pâques** / salle **sombre** (salle obscure = a cinema) |
| `C_R_bank_counter_02` | une **consommation** inhabituelle | des **paiements** inhabituels |
| `C_R_doctor_02` | cette **défaillance** au bureau / le **service sanitaire** de l'entreprise | ce **malaise** / la **médecine du travail** |
| `C_R_kitchen_01` and `_demo` | sur le **comptoir** (home kitchen) | sur le **plan de travail** |
| `C_R_world_03` | parler avec des **autochtones** (Bretons) | avec **les gens du coin** |
| `C_R_bedroom_02` | trop de **fantaisie** dans la tête | trop d'**imagination** |
| `C_R_emo_fear_03` | Ne dis pas de **folie** | Ne dis pas de **bêtises** |
| `C_R_adj_quality_08` | C'est **hasardeux**, ça pollue tout | C'est **dangereux** |
| `C_ST_control_seg016` | (family photo) **Cheese !** | **Ouistiti !**: worth teaching |

Many more lines are correct but stilted, because a rare word was forced in: "Elle se meut difficilement", "j'ai failli défaillir", "Gomme le beurre de la liste", "J'affectionne ces petits pieds". These go away with item 4.

### 6. Logic and continuity slips

- `V_mairie_poste_03`: Léa leaves on 12 July and Sophie replies "En octobre ? Tu es très organisée !". The joke depends on a current month that is never said, so an A1 learner is lost. Proposed: "On est en mai ! Tu es très organisée !".
- `C_R_hospital_01`: "after his operation", but "c'est un miracle que tu sois sorti de la voiture sans rien de cassé".
- `C_R_resto_room`: they order, then the very next line asks for the bill. The waiter offers dessert to Sophie, who ordered the menu with dessert.
- `C_R_exclaim_02`: "Chut ! Le film commence." is followed directly by "Alors, tu as aimé ?".
- `C_R_adj_quality_05`: Maxime tells himself off by name: "Pas de ton moqueur, Maxime... je veux dire, je me tais".
- `C_ST_movement_seg003` sends a boy to buy bread for the ducks. `C_ST_cooking_seg001` rightly says bread makes ducks sick. Keep the second.
- **Premises that don't match the speakers:**
  - `C_R_doctor_02` ("her doctor", but the patient is M. Garnier);
  - `C_R_bank_economy_03` ("A café owner meets her accountant", but the owner is M. Duval);
  - `C_R_emo_joy_01` ("A woman discovers", but it is Antoine).
- **Near-duplicates:** `C_R_ch_sacristy_demo`, `C_R_ch_lady_chapel_demo` and `C_R_kitchen_01_demo` are leftover demos of a scene that already exists. 55 conversations share a title with another one (four are "Le nouveau voisin").

### 7. Lines that can't be read aloud as they stand (matters for audio)

- `C_R_doctor_01_z2`: "(plus tard) Ouf, quel soulagement…". The stage direction is inside the spoken line.
- `C_ST_commerce_seg004`: "« Vendu ! » s'écrie-t-il". This is narration given to a character.
- **Time jumps with no marker:** `C_R_exclaim_02`, `C_R_resto_room`.

**Fix:** allow an optional narrator line, `{"speaker": "", "fr": "Plus tard…", "en": "Later…"}`. The page shows it in italics and the narrator voice reads it. Move stage directions there.

### 8. English that is still British (about 33 lines, 13 of them on the site)

The conversations kept some British forms:

| British form | Times |
|---|---|
| "brilliant" | 9 |
| "marks" (→ grades) | 5 |
| "haven't got" / "hasn't got" / "has got" / "have you got" / "have got" | 8 |
| "autumn" | 2 |
| "holiday" (→ day off / vacation) | 2 |
| "term" (→ semester) | 2 |
| "year 5 and year 6" (→ fourth and fifth grade) | 1 |
| "no lift" | 1 |
| "jumper" | 1 |
| "reckon" | 1 |
| "has got out" | 1 |

**Fix:** rerun the American-words pass on both conversation files. "I've got" alone is fine in American English and stays.

### 9. All-ages content

Alcohol appears in 17 conversations, 6 of them on the site:
- the whole `C_R_wine_01` scene: champagne, wine, whisky, a cigar;
- beer in `C_R_cafe_01`;
- "un apéro" and "le cocktail du jour" in `C_R_cafe_02`;
- "une bouteille d'un grand cru" in `C_R_abs_change_02`;
- "un vin chaud" in `C_ST_nature_seg006`;
- the "Encore un cadavre !" empty-bottle joke in `C_R_text_death`.

No child speaker mentions alcohol. The open question from before still stands: does the all-ages rule allow adults ordering a drink? The scenes are realistic, but if the answer is no, these 17 need a soft drink or a different scene.

## Proposed tooling, so these don't come back

Add a `tools/dialogue_lint.py`, run in CI as report-only at first, that flags:
1. a cast name outside V_ or `village: true` scenes, or a cast child above B1;
2. a level label that is more than one step above the language estimate;
3. filler endings, scenes with more than one "Ha ha", and more than 5 target words in a scene;
4. brackets or parentheses in a spoken line, and narration verbs (s'écrie, dit-il);
5. the British words in item 8;
6. the alcohol words in item 9, until the rule is settled;
7. duplicate titles and `_demo` ids;
8. a premise whose pronouns contradict the speakers' genders, using the gender of the cast or a name list.

Then add a short "Conversations" section to the language skill:
- 4–5 target words a scene;
- one situation with a turn;
- cast rules;
- level by language;
- no narration in spoken lines;
- end on a closing line.

## Suggested order

1. **Quick, safe fixes:**
   - the error table in item 5, the slips in item 6 and the lines in item 7;
   - delete the three `_demo` duplicates;
   - fix the three premises;
   - the American English pass.
2. **Cast:** rename the colliding speakers (scripted), and make the village-bound scenes use the real cast. This should happen before recording any conversation audio.
3. **Levels:** relabel by language difficulty.
4. **Rewrites:** rewrite the 121 live C_ST scenes, then the waiting ones as their rooms are built, following the V_ scenes as the model.
5. **Placement and lint:** fix placement for the 33 conversations that can't be placed, and add the lint.
6. **Your call:** the alcohol rule.

A native speaker should still spot-check whatever is rewritten.
