# Proposals: text, mnemonics, site design and features (28 October 2026)

These are proposals only. Nothing else in the repo has changed.

**What was reviewed:** the live site on main as of PR #176. That's 74 buildings and streets, and 3,930 word placements (3,876 different words). It was checked in a desktop browser (1366×800) and at phone size (390×844), with keyboard-only use and network requests, and every card's text was run through scripts. Items already covered in `data/hooks/qa/RECOMMENDED_CHANGES.md`, or since applied through `relocations.tsv`, aren't repeated here.

## Summary

- **Text:**
  - Hooks and cards use two different respelling systems: 554 hooks quote a respelling that doesn't match the card's "say" line, and a few disagree on the actual sound.
  - About 100 verbs are called "regular" while their tables show spelling changes (*j'achète*, *nous mangeons*).
  - Some notes and plural lines are wrong or empty of content.
- **Mnemonics:**
  - 15 church hooks are "Linked to …" lines with no pun.
  - A handful still lean on Latin or obscure English.
  - The 26 alphabet cards have no hooks.
- **Design:**
  - On a phone, the painting uses only about 60% of the screen.
  - Sector maps hide building names until you hover, so touch users see only a small arrow.
  - Each map load fires 58 failed requests.
- **Features:** the site is a beautiful place to *look up* words, but it has no way to *practise* them. The biggest wins are, in order:
  - a recall mode
  - saved progress with spaced review
  - search
  - deep links to cards
  - showing the 63 dialogues that already exist

---

## 1. Text on the cards

### 1.1 One respelling system, not two
The card's "say" line uses one system (koh-, ah, ew, ehr). 554 hooks quote an older one in brackets (ko-, a, u, air). A learner sees two spellings of the same sound on one card:
- *commun*: card **koh-MUN**, hook "ko-MAN"
- *brun*: card **BRUN**, hook "BRUHN"
- *actuel*: card **ahk-TWEHL** (2 syllables), hook "ak-TU-el" (3 syllables)
- *immuable*: card **ee-MWAHBL**, hook "ee-mu-ABL"
- *existant*: card **ehg-zees-TAHN**, hook "eg-zee-STAHN"

**Proposal:** a script that rewrites the bracketed respelling in each hook to match the card's "say" line, and lists the cards where the two disagree on a vowel or the syllable count for a person to check. Most are only spelling style, but *actuel*, *immuable* and *commun* teach a different sound.

### 1.2 Verb notes

**a) The note repeats the beret line.** 576 verb cards have a note that just repeats the beret line printed right above it ("RED beret = regular -er verb."). Use the note for something the card doesn't already say:
- the auxiliary when it's *être*
- the usual object or preposition pattern
- one common phrase

**b) "Regular" verbs whose table shows a change.** About 100 red-beret verbs are called regular, but their table shows a spelling change:
- *acheter* → *j'achète*
- *appeler* → *j'appelle*
- *manger* → *nous mangeons*
- *commencer* → *nous commençons*
- *préférer*, *répéter*, *transférer* → *è*
- *payer* → *paie / paye*

The learner is told one thing and shown another. **Proposal:** keep the red beret and add a small "spelling change" badge (a tiny accent mark on the beret). Then give the note the rule in one line: "*è* before a silent ending: j'achète, but nous achetons."

**c) Preposition tags.** 42 verbs have tags like "acheter + à", "chercher + à", "avoir + à", "habiter + à". Without an object, these mislead: *chercher* almost always takes a direct object, and *chercher à* means "to try to". **Proposal:** write the full pattern:
- *acheter quelque chose à quelqu'un* (buy from, or for, someone)
- *chercher quelque chose* · *chercher à* + verb = to try to
- *avoir à* + verb = to have to

### 1.3 Plural line
- **Wrong for some compounds:** *les rez-de-chaussées* should be *les rez-de-chaussée*. *Prie-dieu* doesn't change in traditional spelling. *Sud-ouest*, *sud-est* and *ping-pong* shouldn't show a plural at all.
- **Shown for mass nouns, where it's unhelpful or wrong:** *les santés*, *les faims*, *les argents* (money), *les ors*, *les pétroles*, *les aviations*. Mark these nouns as uncountable, and show "usually no plural" instead.
- **Add the sound when the plural changes it.** *Œuf* already does this well ("les œufs: the f goes silent"). Do the same for *os* (plural said OH) and *bœuf* (plural said BUH).

### 1.4 Examples that use another sense
- *verre d'eau*: the example is "Tu veux un verre **de jus** ?". Use a glass of water.
- *quête*: the room is about the church collection, but the example is "Il part en quête d'aventure" (a quest). Use "La quête passe pendant la messe."

A check worth adding: flag examples whose English translation doesn't contain the card's first gloss. It would catch most of these.

### 1.5 Alphabet cards
The 26 letter cards in the école have no hook. Most letters don't need one, but a few trip up every learner. Proposed puns:
- **E** (UH): "the letter E just shrugs: UH"
- **G** (ZHAY) and **J** (ZHEE): "G and J swapped hats", because G is said like English J and J like English G
- **I** (EE): "I says EE, like a squeak"
- **R** (EHR): "R is AIR, from the throat"
- **U** (EW): "U says EW!, lips pushed out"
- **W** (doo-bluh-VAY): "a DOUBLE V"
- **Y** (ee-GREK): "the GREEK I"
- **Q** (KEW): "Q waits in the QUEUE"
- **H** (AHSH): "H is ASH, and silent in words"

### 1.6 Content that exists but isn't shown
- `data/source/village_dialogues.json` has 63 dialogues for the original 21 rooms, which still exist with the same keys. A cast list with gender and age is included, ready for voices.
- `data/source/conversations.json` has 711 written conversations for the older room plan.

Neither is shown anywhere on the site (see §4.6).

### 1.7 Repo text
The root `README.md` still describes the old build (`npm run build`, `content/site.json`, "Rue des Saveurs is the open quarter"). It should describe the village in `village/`, as `village/README.md` already does.

---

## 2. Mnemonics

These follow the house style agreed for the earlier recommendations: puns first, no Latin, nothing forced.

### 2.1 The church "Linked to …" hooks
15 cards in `eglise` and `cathedrale` use the template "Linked to 'X', said …" with no pun. Proposed puns:

| Word | Now | Proposed |
|---|---|---|
| nef (NEHF) | Linked to "navy" (Latin *navis*) … | **"NEPH-ew"**: your NEPHEW races down the long NAVE between the pews |
| chaire (SHEHR) | Linked to "chair" … | **"SHARE"**: the priest SHARES his sermon from the carved PULPIT |
| quête (KEHT) | Linked to "quest" … | **"KATE"**: Kate passes the COLLECTION plate along the pew |
| fidèle (fee-DEHL) | Linked to "fidelity" … | **"FIDDLE"**: the old fiddler, the most FAITHFUL BELIEVER, has played at every Sunday Mass for fifty years |
| vitrail (vee-TRAHY) | Linked to "vitreous" … | **"V-TRAIL"**: in the STAINED-GLASS WINDOW, geese fly in a V-shaped TRAIL |
| encensoir (ahn-sahn-SWAHR) | Linked to "incense" … | **"IN SUN, SWAY"**: the brass CENSER SWAYS through a beam of SUN |
| bénitier (bay-nee-TYAY) | Linked to "benediction" … | **"BENNY, TEA?"**: Benny dips his fingers in the HOLY-WATER STOUP, thinking it's his TEA |
| portail, cortège, encens | Linked to "portal", "cortege", "incense" | These are real cognates: a plain card is fine ("Like English 'portal'") |

### 2.2 Remove Latin and obscure English
- *aviation*: drop "Latin *avis* = bird". The AVIARY-ON pun works without it.
- *nef*, *pontife*: drop the Latin notes (*navis*, *pontifex*).
- *farine*: "Think of FARINA, the English name for a fine wheat-flour cereal". Few learners know *farina*. Proposed: **"FA-RINSE"** (fah-REEN): the baker tries to RINSE the FLOUR out of his hair.
- *chandelle*: already proposed in RECOMMENDED_CHANGES §2.2: use CHANDELIER.

### 2.3 Let the pun lead on verb hooks
403 of the 711 verb hooks begin with "Monsieur Verbe …". The mascot is a good device, but when hooks start the same way, the opening stops helping: the sound-alike, which is what you need to recall, comes halfway through the sentence. **Proposal for new and rewritten verbs:** open with the pun and keep Monsieur Verbe in the picture. For example: "SHOE-TAY! (ah-shuh-TAY) Monsieur Verbe BUYS a new pair of SHOES" instead of "Monsieur Verbe BUYS a new pair of SHOES: ah, SHOE-TAY!".

### 2.4 Use the data to find weak hooks
Self-rated hook strength isn't a reliable signal. Once the recall mode (§4.1) exists, log the words people get wrong most often, anonymously or just locally. Those are the hooks to rewrite next. The same idea is in `HOOK_PROPOSALS.md` §7; the recall mode is what makes it possible.

---

## 3. Site design

| # | Issue | What happens now | Proposal |
|---|---|---|---|
| 1 | **Painting size on a phone** | In portrait at 390×844, the 16:9 painting fills roughly the middle 60% of the screen, with blurred bands above and below. Labels are small. | Fill the height and pan sideways (the "swipe to look around" hint already exists). Or use the bottom band for a scrollable tray of the room's words, which also helps people who can't find a small object. |
| 2 | **Sector maps hide names** | On a sector map (e.g. `#/quartier/cafes`), building names appear only on hover, even with "Labels: always shown" switched on. Touch users see a small → arrow and no name. Unbuilt buildings show nothing at all. | Follow the Labels switch on sector maps too. Show "bientôt" pills on unbuilt buildings, as the README says. |
| 3 | **58 failed requests per load** | The map checks whether a building exists by requesting `data/<id>.js` for every building, so each unbuilt one returns a 404. | Generate a `data/live.json` list of live buildings at build time and read that instead. |
| 4 | **Dense rooms** | Some rooms carry 18 or more labels (e.g. `cirque/trapezes`). They're readable but crowded. | Add a level filter (§4.7). Show labels in route order with small numbers (§4.5). Default dense rooms to labels-on-hover. |
| 5 | **The palace rules aren't explained** | Nothing on the site says that feminine words sit on the left and masculine on the right, what the beret colours and mirrors mean, or who Monsieur Verbe is. The cards mention berets; the sides aren't mentioned anywhere. | A one-screen "How the village works" panel, shown on the first visit and kept behind a ? button. On each noun card, add a line such as "feminine: lives on the LEFT of the room". |
| 6 | **Card details** | Cards show no level, there's no way to step to the next word, and the picture is small. Long conjugation lines (*s'asseoir*: "m'assieds / m'assois"; *payer*: "paie / paye") show two forms at the same weight. | Add a CEFR badge, previous/next arrows in the room's route order, tap to enlarge the picture, and "also in: …" when a word appears in another room. Show the main form first and the alternative in grey. |
| 7 | **Pronunciation audio** | The browser's own voice (`speechSynthesis`) reads the words. Quality varies by device, and some Android and Linux browsers have no French voice, so the button does nothing. | Pre-generate audio for every word and example with a good neural voice (the dialogue cast already has voice hints). Keep the browser voice as a fallback, and hide the button when neither is available. |
| 8 | **Image weight** | 400 room paintings at about 300 KB each (JPEG, 1280 px). | Serve WebP or AVIF with a smaller size for phones. That roughly halves the data a visitor downloads. |
| 9 | **Screen readers** | Every word hotspot is a keyboard-reachable button with an "la table: table" label. That's good. | Keep it. In recall mode (§4.1), the English must leave the label, or the answer gets read out. |

---

## 4. Features

In order of value for a memory palace, where most of the learning comes from walking the route and *recalling*.

1. **Recall mode.** A switch in the header hides all labels.
   - Tap an object and say or type the French word with its article, then reveal the answer and grade yourself (knew it / almost / no).
   - A second game turns it round: show "*la chaise*" and the learner taps the right object.

   This is the practice the palace exists for, and the site has none of it yet.
2. **Progress and spaced review.**
   - Save each word's grade in the browser.
   - Show a progress ring on each room's sign and each building on the maps.
   - A **Review** button builds today's list and *walks you back to each room* to recall the due words in place.
3. **Search.** French or English, accents optional. Pick a result and you fly to the room with the card open. With 3,900 words, this is the most-asked-for feature on any vocabulary site.
4. **Deep links to a card**, e.g. `#/cafe?w=fr_table_noun`. Needed for search and review, and lets people share a word.
5. **A route through each room.** Give each room's words a fixed order (the "loci"), number the labels, and add previous/next on the card. An optional **Walk** button plays each word and its hook in order, like a guided tour.
6. **Dialogues.** A "Conversations" tab in each room that has them: lines in French with the English hidden until tapped, and audio per line. The data exists for 21 rooms.
7. **Level filter.** Show only A1–A2 words (or up to a chosen level) across the village, so beginners aren't flooded and advanced learners can hide what they know.
8. **Settings:** speech speed, IPA or respelling, and English on labels on or off.
9. **Offline / install.** A web-app manifest and a service worker that caches the rooms you've visited, so the village works on a phone with no signal.
10. **Export.** A room's or a quarter's words as an Anki CSV, or a printable sheet with the picture and the labels.

**Suggested order:**
1. 3.2 and 3.3: small fixes.
2. 1.1, 1.2 and 1.3: data scripts.
3. Features 4.4 and 4.3: deep links, then search.
4. Features 4.1 and 4.2: recall mode, then progress and review.
5. Everything else, as each building is next touched.
