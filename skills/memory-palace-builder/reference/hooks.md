# Mnemonic hooks (generic)

Read when writing, rating, merging or editing hooks. Language-specific hook rules: language skill reference/hooks.md.

## Hook data and fallback

- Store the mnemonic hook in the item metadata (sound-alike, one-line scene, strength, fallback) and always explain it on the item's detail card when clicked. <!-- B45 -->
- Never drop an item because a good or respectful mnemonic is hard. Fallback: depict the item itself clearly and well. Near-identical cognates need no pun, and the plain item is enough. <!-- B46 -->
4. Every mnemonic actually works: say the sound-alike aloud, confirm it resembles the target, and confirm the picture also points to the meaning. Reject weak ones and redesign. <!-- B60 -->

## Bulk hook writing

- Rate every hook honestly (strong/ok/weak/plain) and re-check the weak ones before calling the set done. A hook is weak when the scene only pictures the meaning with no sound link, when the sound link is said by a character instead of shown, or when the sound-alike is not close to how the word is actually said. <!-- B109 -->
- Parallelize big hook batches by slice (level or sector). Helpers write only to their own folder of batch files and mark finished files (e.g. .done.tsv). Exactly one worker merges into the master data file, so nothing gets overwritten. <!-- B110 -->
- Keep a FORMAT note for batch files and a stats script. Progress counts should include written-but-unmerged batches. <!-- B111 -->
- Merge scripts: never let a later line silently undo an earlier correction (e.g. a gloss fix). Fallback templates must not add theme text, like a "sacred setting", to items outside that theme. <!-- B112 -->

## Hook wording

- Hooks never carry meta prefixes ("Twist on a cognate:", "Like English", "False friend:"). Cognate and false-friend notes go in their own card field. <!-- G18 -->
- Hooks never open with a placement phrase ("On the balcony", "At the upper window", "On the roof"), and verb-street hooks never write the balcony, window or roof tier into the hook: the item's position in the painting shows where it is, and the hook describes the action and the sound clue only. <!-- G19 G59 -->

## One hook per word, forced puns, adverbs (merged)

- **One hook per word, everywhere.** A word placed in two rooms shares one hook (keep the better pun); only the setting adapts. Prefer one home per word. Script-check that no id has two different hook texts. <!-- B223 L122 G139 -->
- **Forced puns, to rewrite or reject:** the sound is off (wrong vowel); too many pieces (more than two sound chunks; one chunk on the stressed syllable beats 3-4 unrelated chunks covering every sound); the pun object only sits beside the meaning instead of DOING something to it; no pun at all (just the meaning acted out); or the wrong template ("Like English X" on a non-cognate). Good model: two chunks and one action, with one person or one animal. Use only English the learner knows, no etymology. Real cognates can stay plain. Phrases get one pun on one chunk. <!-- B224 L123 G140 -->
- **Adverbs.** For weak -ment adverbs, reuse the adjective's pun plus "-ly" instead of a new scene, unless that pun's figure already stands beside it for another word. <!-- B225 L126 -->

## Hook edits and user hooks

- **Hook edits are surgical:** when rewriting a word's hook, change only its `hook` and `why` fields. Replacing the whole entry drops the `say`/`f_say` respellings, and strict QA then fails (e.g. unwanted "pee"/"poo" sound flags). Diff the entry before and after. <!-- G125 -->
- **User-hook coverage gate:** every hook the user wrote or asked for must be applied wherever the painting matches it (in this repo, as an entry in `content/v2/<bld>/hooks.json`, which wins over every other source). A user hook whose painting shows a different scene keeps the old matching hook, but only if the word is listed as a repaint in `data/hooks/qa/RECOMMENDED_CHANGES.md`, and it ships no worse than live. Shipping a hook that mismatches its painting always fails, and so does a user hook silently dropped with no repaint row. This keeps a mismatch from going live without blocking a build that is no worse than live. <!-- G63 -->
- **Hooks file apply order:** packages that each ship a whole hooks file must declare a row count, and the build uses the newest superset copy. Note it in the README. <!-- G65 -->
