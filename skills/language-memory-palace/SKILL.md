---
name: language-memory-palace
description: >-
  Use when building a memory palace for learning a foreign language's vocabulary
  and grammar; load together with the Memory palace builder skill. A one-page
  language checklist; detail lives in reference/*.md, read only when relevant.
---
# Language memory palace

The language layer on top of the Memory palace builder skill. Each line is one checkable rule. The file named in a section heading holds the full rules, examples and lessons; open it only when that topic comes up.

**Read only what the task needs:** new room: scope-and-levels.md, representation.md, verbs.md (if it holds verbs), placement-and-senses.md · hooks only: hooks.md · moving a word: placement-and-senses.md · card text or site: cards-and-site.md · checks: validation.md.

## Scope, levels and density (reference/scope-and-levels.md)
- Tag every word with its level (e.g. CEFR A1-C2) and build the inventory from openly licensed lists, credited.
- Cross-check noisy level lists against corpus frequency, and boost concrete everyday words.
- Keep every requested word; rare words may get a home and a card now and a picture later.
- The core village holds beginner to intermediate words; advanced words go upstairs, in back rooms or in an advanced area.
- Each main painting holds about `room_target` of its commonest words (never more than `room_max`), verbs among them; zoom spots hold `zoom_min` to `zoom_max` (numbers in skills/limits.json).
- No one-object zooms: fold a zoom of fewer than about 4 words into a fuller scene.
- The beginner area holds greetings, the alphabet on one board, sounds, articles, numbers, pronouns and basic grammar.
- Sectors are thematic and fit the culture.

## Representation spec before any painting (reference/representation.md)
- Write a short spec covering each word class, each grammatical feature and its single visual channel, reference props, rare words and sensitive words.
- Reuse this village's approved devices. For a new language/project, agree on one representative sample before bulk painting; do not repeat setup approvals for existing French rooms.
- Check the devices against each other for clashes, and put each device's meaning on the card.
- Gender: feminine clearly left, masculine clearly right (neuter in the middle), with no physical divider; zooms too.
- Adjectives and adverbs sit in the 30-70% center band; opposites may face each other.
- Sensitive or mature words appear as museum wall text, never drawn.

## Verbs (reference/verbs.md)
- Choose one recurring, culturally fitting verb marker; each verb feature gets its own visual channel on it.
- French uses Monsieur Verbe: red -er, green -ir, purple -re, gold irregular beret; reflexives hold a hand mirror. Keep each verb action visible at human scale.
- Verbs live in themed rooms, acting on that room's nouns at human scale.
- Verbs are spread through the scene, never bunched in one zone or lined along an edge.
- Verb streets only where they truly make sense; a repaint brings fitting street verbs back into its rooms.
- The verb card shows tense tabs with full conjugation tables; all tabs are visible at every size.

## Hooks (reference/hooks.md; generic rules in the builder's reference/hooks.md)
- Keyword method: a native-language sound-alike of the word said aloud, painted literally, that also shows the meaning.
- Derive the sound-alike from the pronunciation (IPA or respelling), never from the meaning or the spelling alone.
- Use only English the learner knows: no etymology and no other target-language word (except one certainly known).
- A cognate counts only if it looks AND sounds close; it still gets a twist or stays plain, with any false friend noted.
- No template or meta wording on cards; both the sound cue and the meaning are painted.
- Audit new hooks aloud against IPA/respelling before art. Preserve user-selected hooks; plain depiction is better than a strained pun.
- Replace vulgar auto-glosses, and add an age-appropriate usage_warning to such words.
- One hook per word everywhere; reject forced puns (wrong vowel, more than 2 chunks, pun beside the meaning).

## Placement by meaning (reference/placement-and-senses.md)
- Place by meaning, never by a shared English gloss word ("rive" is not money); the script flags these and a teacher checks each one.
- Gloss the sense the room teaches; a homograph with two senses gets two word ids, cards and hooks.
- No overflow rooms: every room's words share an honest, paintable theme.
- Grave or sensitive words never go in light-hearted rooms.

## Cards and site (reference/cards-and-site.md)
- Every word has an example sentence with a translation, a definition in our own words, and IPA plus a respelling.
- Every room has realistic hand-written dialogues with speech, a transcript and a translation toggle; no template or quiz lines.
- Every item has a label (article included); a remembered switch chooses always-on or hover.
- All UI text has a native/target-language toggle, from one i18n file.
- Quiz modes are filterable by room, sector and level.
- Prayers, scripture and other quoted texts follow the copyright gate (builder reference/copyright.md): a pre-1929 edition or our own translation from the original, never the current liturgical translations.

## Checks (reference/validation.md)
- In every room, check gender sides, articles, accents and spelling (by script), the mnemonic sound link, false cognates, and verb tables and codes.
- Validators also check glosses, examples, conversations, pronunciation voice and quoted texts.
