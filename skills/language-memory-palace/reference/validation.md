# Language checks and validation

Read at the end of every room and when validating.

## Extra language checks per room (in addition to the generic room checks)

- Gender placement is correct for every noun. <!-- L89 -->
- Articles, accents, and spelling are correct (validate with a script against the data file). <!-- L90 -->
- Mnemonic truly connects the native-language sound (or, where flagged, the spelling) to the target meaning. <!-- L91 -->
- False cognates are flagged. <!-- L92 -->
- Conjugation tables are complete for every verb in the room, and each verb is acted by the verb character with the right colour code. <!-- L93 -->

## Validation (language-specific checks for validator bots)

Run these in addition to the generic Validation section of the Memory palace builder skill. <!-- L99 -->

- **Words:** spelling, accents and grammatical properties (gender, class, etc. where the language has them) are correct. Each word sits where the project's placement scheme says a word with its properties belongs (check zoom spots too). <!-- L100 -->
- **Glosses:** they are accurate and cover the common sense first. They are written in our own words or properly credited. <!-- L101 -->
- **Example sentences:** every word has one, in natural, grammatical target-language text that actually uses the word in the sense being taught. The translation is faithful. <!-- L102 -->
- **Verb cards:** every tense tab is present and the conjugations are correct (spot-check irregular verbs fully). The verb character's colour code (and reflexive mirror) matches the verb's class. <!-- L103 -->
- **Conversations:** they are realistic everyday dialogues, with no template or quiz lines. Each `used_words` entry really appears in the lines. Unwritten conversations are hidden. <!-- L104 -->
- **Mnemonics:** the sound link works for a native speaker of the learner's language. Hooks contain no crude or slang sound-alikes. <!-- L105 -->
- **Pronunciation:** if there is audio or speech synthesis, check that the target-language voice is used. <!-- L106 -->
- **Quoted texts:** prayers and other quoted texts use the public-domain or licensed wording recorded in the audit. Required entries are present, and similar texts are clearly named. <!-- L107 -->
