# Mnemonic hook proposals (October 2026)

Scope: the 183 hooks live in Le Village (`village/assets/data/*.js`) and the 8,000 in `data/source/vocab.jsonl`.
Nothing here is applied yet. Each section says what to change and why; rewrites are ready to paste.

## Where things stand

| | count |
|---|---|
| Corpus hooks rated strong / ok / weak | 1,808 / 5,964 / 228 |
| Weak hooks at A1–A2 (the words learners meet first) | 37 |
| Broken templated hooks (false-friend template, "Hear X in X", fallbacks) | 27 |
| Cognate hooks that spend the hook on a meaning the learner already knows ("Like English…", "same word…") | 3,389 (42%) |
| Live hooks identical to the corpus | 0 of 169 (14 live words are not in the corpus at all) |
| Live nouns placed on their gender's side (la left, le right) | 152 of 152 |
| Places on the live site that tell the learner about that left/right rule | 0 |

The memory method is sound. The biggest gains are in what the hooks *don't* carry: gender, irregular forms, and the end of the word.

---

## 1. Make gender part of the memory (highest value)

Gender is the thing English speakers forget most, and the village already encodes it. Every live noun stands left if feminine, right if masculine. But the old site's guide explained that, and Le Village doesn't load the guide, so the rule is invisible.

**Proposals**

1. **Say the rule once, where it's seen.** Add one line to the map screen or first room: "In every room, *la* words stand on the left and *le* words on the right." Repeat it on the word card: "feminine · left side".
2. **Tint the label pills by gender.** For example, a warm border for *la* and a cool border for *le*. Learners then absorb the pattern without reading anything. Verbs keep their italic label and beret.
3. **Teach the ending rules once, and hook only the exceptions.** About 80% of noun genders follow from the ending. A hook is wasted on a word that obeys the rule, and essential on one that breaks it.

   | ending | gender | exceptions worth a hook |
   |---|---|---|
   | -tion, -sion, -té, -ence, -ance, -ette, -ure | feminine | **le silence**, **l'été**, **le côté**, **le squelette** |
   | -age, -ment, -eau, -isme, -oir | masculine | **la plage**, **la page**, **la cage**, **l'image**, **l'eau**, **la peau** |
   | -ée | feminine | **le musée**, **le lycée** |
   | -ème (Greek origin) | masculine | (rule itself surprises learners: **le problème**, **le système**) |

   Live example: **le silence** currently says "Same word as in English, said see-LAHNS". That spends the hook on the one part the learner already knows. Proposed:
   > A kitten in woolly socks tiptoes past with a paw to its lips: SILENCE! Watch out: almost every *-ence* word is feminine (la patience, la science), but **le silence** is a rebel and stands on the masculine side.

4. **Don't let the scene contradict the gender.** **le maire** is drawn as a MARE, a female horse, which nudges learners towards *la*. That's fine as a sound peg, but add "a *he*-mare in the mayor's sash" or swap to a stallion with "MARE-like mane". It's the clearest live case of a picture arguing against its article.

---

## 2. Repair the broken templated hooks (27 in the corpus)

These are generator output that was never rewritten. Several are wrong, not just weak.

| id | problem | proposed hook |
|---|---|---|
| `fr_ranger_verb` | Says it "means 'to order'". *Ranger* means to tidy or put away. **Fix the gloss too.** | A park RANGER (rahn-ZHAY) in her wide hat marches into the messy tent and PUTS EVERYTHING AWAY, pot by pot. *Ranger sa chambre* = to tidy your room. |
| `fr_promoteur_noun` | "looks like promoter but means promoter" | A property DEVELOPER plants a giant PROMO flag on an empty building site (proh-moh-TUHR): *un promoteur immobilier* builds and sells flats. |
| `fr_chandelier_noun` | Sound-alike is "shan't lie, eh?" | A single brass CANDLESTICK holds one candle (shahn-duh-LYAY). The big hanging light everyone calls a chandelier is *un lustre*. |
| `fr_resume_noun` | "looks like résumé but means summary" | A student squeezes a fat novel into one neat page: a SUMMARY, *un résumé* (ray-zew-MAY). Your job CV is *un CV*. |
| `fr_blouse_noun` | Sound-alike is "blues"; no scene | The chemist's white lab coat and the painter's splattered SMOCK are both *une blouse* (BLOOZ). A shirt for a woman is usually *un chemisier*. |
| `fr_stage_noun` | Sound-alike "stahzh" is the word itself | A nervous INTERN takes notes on a theater STAGE (STAHZH) on day one of her TRAINING: *un stage* = an internship or course, never a theater stage (*une scène*). |
| `fr_smoking_noun` | Sound-alike "smo-KING" | A dandy in a black TUXEDO (smo-KEENG) adjusts his bow tie. English once called it a "smoking jacket"; French kept *le smoking*. |
| `fr_commode_noun` | Sound-alike "mod" | A tidy CHEST OF DRAWERS (koh-MOD) with a vase of flowers on top. Not a toilet! *Commode* also means "handy" as an adjective. |
| `fr_supporter_verb` | "means 'to bear'" with no scene | Monsieur Verbe grits his teeth as a goat bleats in his ear: *je ne le supporte pas* (sew-por-TAY), I CAN'T STAND it. To support a team is *soutenir*. |
| `fr_fromage_noun` | "Hear 'from Madge' in 'fromage': picture 'from Madge' tied to 'cheese' in its room." | Madge the cheese lady hands a huge wheel of CHEESE over the counter: everybody buys it FROM MADGE (froh-MAHZH). |
| `fr_huile_noun` | template prose | A squeaky cart WHEEL (WEEL) gets a squirt of OIL and sighs with relief. |
| `fr_creme_noun` | template prose | A jug of CREAM is poured on THEM, the strawberries: KREHM rhymes with *them*, not *cream*. |
| `fr_sel_noun` | template prose (the live room already has a better one: salt in a prison CELL) | Backport the live hook. |
| `fr_degradation_noun` | Gloss reads "removal from office", but the everyday sense is damage or deterioration. | Fix the gloss first: *dégradation* = DAMAGE, wear (*la dégradation de l'environnement*). Then: a statue slowly DEGRADES in the rain (day-grah-dah-SYOHN). |
| `fr_mort_noun_f`, `fr_mort_noun_m` (and `fr_prostitue_noun`, same fallback) | "Plain fallback" prose | **la mort**: a single candle has burned out; there is no MORE (MOR). **le mort**: same sound; a man in the story is no MORE. Keep the tone quiet. |
| `fr_metier_noun`, `fr_concierge_noun`, `fr_job_noun`, `fr_coach_noun`, `fr_pro_noun`, `fr_business_noun`, `fr_baby_sitter_noun`, `fr_bourgeoisie_noun`, `fr_oeuvre_noun_*` | "Twist on a borrowed word" stem left in the text | Strip the template prefix; the scenes after it are usable. For **métier** (A1), use the stronger link: May-TYAY: in MAY the young baker lifts his first loaf and cheers YAY! He has found his TRADE. |

**Generator fix:** the false-friend template takes the French word as its own "looks like" word. Whoever regenerates hooks should drop that template entirely; false friends need a hand-written contrast every time.

---

## 3. Fix live hooks that teach the wrong sound or a weak link

| word (room) | problem | proposed hook |
|---|---|---|
| **la moitié** (math zoom), rated weak | MY TIE + yay. The corpus version, a kiss, was better. | She blows a kiss, MWAH!, and pushes HALF of her cake across the table: mwah-TYAY, *la moitié*. |
| **le chiffre** (math zoom) | CHEF teaches the wrong vowel (eh, not ee). | A SHEAF of wheat whose stalks bend into the DIGITS 1 to 9: SHEEF-r. |
| **le sucre** (comptoir) | SUCKER teaches the "uh" vowel; French *u* is round-lipped "ee". | Little SUE (round your lips) CRUNCHES a SUGAR cube: SEW-kr. |
| **le thé** (café) | A cat's TAIL invites a final L. | An Irish granny pours "a nice cup of TAY". That's how she says TEA, and so does French: *le thé*. |
| **le couteau** (table zoom), rated weak | COO + TOE never touches "knife". | A dove COOs in alarm as the bread KNIFE drops point-first between its TOEs: koo-TOH. |
| **la paix** (église), rated weak | "the start of PEace" | Two squabbling kittens, little PESTS, finally make PEACE and fall asleep together: PEH. Spelling: *paix* is the Latin PAX with an *i*. |
| **le ballon**, **le vent**, **le carton**, **le pinceau**, **le banc** | Keywords end in a spoken N or K (ball-ON, VAN, TON, PAN, BANK), which is exactly the sound French drops. | Keep the scenes, and append a standard tail: "(nasal: stop before the n)". **le banc** already does this ("the c is silent"); make it the house rule. |

**A rule worth adopting:** French stress falls on the **last** syllable. Several verb hooks anchor the start and leave the end as filler. Examples: *ajouter* = "a zoo + tay", *mesurer* = "measure + ray", *mélanger* = "MAY-lahn = melon". Ask each new hook to anchor the final syllable, or at least not to fudge it.

---

## 4. Irregular verbs: put the trap in the hook

The beret color already says "irregular". But only 1 of the 7 gold-beret verbs live today (*boire*: "nous buvons") says *what* is irregular. Learners then reach for the regular form and get it wrong. One extra clause per verb fixes that:

| verb | add to the existing hook |
|---|---|
| **dire** | …and he never says *disez*: it's **vous dites** (DEET), one of only three *-tes* forms in French (with *faites*, *êtes*). |
| **écrire** | …the crier's quill sprouts a V as the scroll grows: **nous écrivons**. |
| **apprendre** | …and once he's learned, the prawn wins a PRIZE: **j'ai appris** (ah-PREE). |
| **s'asseoir** | …once he's down: **il est assis** (ah-SEE), "a SEAT!" |
| **cuire** | …the choir sings one last note, the pancake is done: **c'est cuit** (KWEE). |
| **envoyer** | …in the future the envoy says **j'enverrai**, never *envoierai*. |
| **appeler** (red, stem change) | …the apple phone rings twice, so two L's: **j'appelle**. |
| **acheter** (in the corpus, not yet live) | …the accent appears when the ending goes quiet: **j'achète**, *nous achetons*. |

---

## 5. Cheaper than hooks: patterns and word parts

Some words are better remembered by their parts than by any picture. The A1 function words are the weakest hooks in the corpus, and nearly all of them are transparent:

| word | now (weak) | proposed |
|---|---|---|
| **aujourd'hui** (A1) | "Oh, sure, dwee!" | *au jour d'hui* = "on the day of today". Hook: OH, SURE, it's DEWY: TODAY's grass is still wet. |
| **maintenant** (A1) | "MAN-TEN-NAN" | *main tenant* = "holding in the hand": what you hold right now. Hook: the landlady shouts, "The MAIN TENANT moves in NOW!" |
| **demain** (A1) | "DUH-MAN" | The circus poster: "The MAIN event is TOMORROW!" (duh-MAN, nasal). |
| **peut-être** (A1) | "PERHAPS a puppet" | *peut être* = "can be". It CAN BE true… PERHAPS. |
| **toujours** (A1) | "TWO, SURE" | *tous les jours* = "all the days" = ALWAYS. Keep the old sweethearts: "too-ZHOOR, every day of their lives." |
| **quelquefois** (A2) | "SHELL-KUH-FWAH" | *quelque fois* = "some times". That's it: SOMETIMES. |
| **monsieur** (A1) | "A mess, you say?" | *mon sieur* = "my sire": MON-SIRE becomes SIR. |
| **le jeu** (A1) | grandpa sighs "JEUH" | JEOPARDY! comes from Old French *jeu parti*, a "split GAME" (ZHEUH). |
| **vivre** (A1) | "Eve" | VIVE la France! LONG LIVE…: *vivre* = to LIVE (vivid, revive, survive). |
| **doucement** (A1) | no sound link | *douce* (soft, sweet: Spanish *dulce*) + *-ment* (-ly) = SOFTLY. |

Two spelling patterns unlock hundreds of words and deserve a short "village rule" card each:

- **é at the start often hides an English s:** *étranger* stranger, *école* school, *épice* spice, *éponge* sponge, *état* state, *étable* stable, *écran* screen.
- **ˆ often marks a lost s:** *forêt* forest, *fête* feast, *bête* beast, *hôpital* hospital, *île* isle, *côte* coast, *pâte* paste.

Suffix pairs belong on the same card: *-ment* = -ly, *-té* = -ty, *-eux* = -ous, *-ique* = -ic.

---

## 6. One source of truth for hooks

Every live hook was rewritten by hand per room, and none of them made it back to `vocab.jsonl`. Usually the live text is better (salt in a prison CELL beats "Hear 'sell' in 'sel'"). Sometimes it's worse (*moitié*). The next room will start from the stale corpus text again.

**Proposal:** a one-off reconcile pass. For each live word, keep the better of the two hooks and write it back to `vocab.jsonl`, with the `strength` re-rated. After that, room data reads hooks from the corpus instead of carrying its own copy.

## 7. Measure instead of self-rating

`strength` is the author's guess. A tiny signal would show which hooks actually fail:
- On the word card, add "Got it" / "Didn't stick" buttons stored in `localStorage`, or collected if you want the data.
- Then rewrite the hooks with the most "didn't stick" taps first.

---

## Suggested order

1. Surface the left/right gender rule and tint the labels (§1). Small code change, biggest learning win.
2. Fix the 27 broken templated hooks, including the two wrong glosses (§2).
3. Apply the six live rewrites and the nasal-n rule (§3), and the irregular-verb clauses (§4).
4. Write the two pattern cards and the ten function-word rewrites (§5).
5. Reconcile live and corpus hooks (§6), then add the feedback buttons (§7).
