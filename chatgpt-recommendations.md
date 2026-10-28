# ChatGPT recommendations

Review date: 2026-10-28  
Reviewed revision: `d859bac75c044bf1ac1d58bacf7a20a46b427426`

These are recommendations only. This review did not change the site or skills.
Counts describe the reviewed revision, not necessarily later commits.

## Scope and main finding

Reviewed the current repository, all three memory-palace skills and relevant
references, and sampled the live world map, home district, garage, tool close-up,
campus, lycée entrance hall, and a garage verb card. This was a targeted review,
not a complete visual audit of every room or a full mobile/fullscreen test pass.

The biggest opportunity is to make better use of content already built. The
village has grown substantially, but several learning features described in the
skills have not reached the current viewer.

## Site improvements

| Priority | Finding | Recommended improvement |
|---|---|---|
| High | **711 written conversations exist**, but the current viewer has no dialogue player. No recorded audio files are present. | Expose each room's existing conversations with a transcript, translation toggle, whole-conversation playback, and line replay. Store generated audio separately. |
| High | Only **13 of 357 spaces outside verb streets contain verbs**. | Gradually bring suitable verbs into their natural settings: people repairing, ordering, carrying, and opening. Preserve established locations during a planned migration. |
| High | **67 of 477 spaces exceed 12 items**, reaching 26; the skills say more than 12 fails. | Visually review the densest spaces first. Split crowded scenes into meaningful rooms or close-ups rather than shrinking objects. These counts identify candidates, not proof that every scene is crowded. |
| High | The current viewer lacks the skills' **placement guide and interface-language switch**. | Add a compact guide explaining gender sides, mime/beret conventions, mirrors, and zooms. Connect the existing translation data to the viewer. |
| Medium | Exploration currently leads mainly to opening cards; there is no recall/review flow in the viewer. | Add an optional room-recall mode: hide labels, prompt a word or image, then reveal. Keep practice tied to the room. |
| Medium | Startup probes every registered building by loading its JavaScript. The **74 available building payloads total approximately 4.1 MB**, before images. | Generate a small availability index and load building content only when entered. |
| Medium | Painted exits can be difficult to discover without hovering. The lycée also offers both painted stairs and a room-navigation list. | Choose one consistent navigation convention, with subtle visible exit cues and clear orientation. |
| Medium | The modal declares itself accessible, but the code lacks focus trapping/background isolation. The document language is French while much UI text is English. | Improve keyboard focus handling and language annotations; respect reduced-motion preferences. |

## Skill and workflow improvements

| Priority | Finding | Recommended improvement |
|---|---|---|
| High | **Conflicting art instructions:** the builder prefers separate assets, another paragraph prefers integrated paintings, and v2 documentation requires integrated paintings. | Declare one current approach: separate editable source assets plus a composed room image where useful. Mark older guidance as superseded. This preserves the user's token-saving preference. |
| High | The release-gates references name **six tools/procedure files that are not in the repo**. | Replace those references with actual commands. Clearly distinguish automated checks from human visual judgments. |
| High | The deployment workflow checks only that five files exist. It does not enforce the skills' content/layout gates. | Define a small, reliable set of checks for changed buildings, with a separate periodic whole-site audit. |
| Medium | Rules conflict about breadcrumbs versus Back, room lists, natural painted text, and density targets. | Consolidate each policy into one canonical rule referenced by the other skills. |
| Medium | Audio guidance still specifies browser speech synthesis. | Add a recorded-dialogue workflow covering consistent speaker voices, exact script matching, pronunciation review, timestamps, licensing, and browser-speech fallback. |
| Medium | The root README describes an obsolete café-only site and build process. | Rewrite it around the currently deployed v2 site, authoritative data sources, and actual build/deploy commands. |

## Suggested order

1. Resolve skill contradictions and stale tool references.
2. Connect existing conversations to the live viewer.
3. Add the placement guide.
4. Review verb coverage and crowded rooms.

These changes would improve the learning experience before another large
expansion.

## Evidence and locations

- `data/source/conversations.json`: 722 conversation records; 711 marked
  `written` and 11 marked `premise_only`.
- `content/v2/*/layout.json`: 477 spaces and 3,930 item slots; 357 spaces outside
  verb streets, of which 13 contain a verb item. Counts use item IDs ending in
  `_verb` and building IDs starting with `st_` for verb streets.
- `village/app.js`: `probeAll()` loads registered building payloads;
  `speak()` uses browser speech synthesis. The viewer contains no dialogue,
  quiz, guide, or interface-language-switch implementation. `openCard()` and
  the modal handlers provide initial focus and focus restoration but no focus
  trap or background isolation.
- `village/data/*.js`, excluding `map.js`: 74 building payloads, totaling
  4,133,866 bytes at the reviewed revision.
- `village/index.html`: document language and modal markup.
- `village/style.css`: navigation, card, and animation styles.
- `skills/language-memory-palace/SKILL.md` and
  `skills/language-memory-palace/reference/cards-and-site.md`: conversations,
  audio, guide-related conventions, interface language, and quiz expectations.
- `skills/memory-palace-builder/reference/setup-and-style.md`: competing art
  pipeline instructions, including the separate-assets preference.
- `skills/memory-palace-builder/reference/site-ui.md` and
  `skills/memory-palace-release-gates/reference/process.md`: competing
  navigation guidance.
- `skills/memory-palace-release-gates/SKILL.md`: the stated density limit.
- `skills/memory-palace-release-gates/reference/tools-and-logs.md`: references
  these absent paths:
  - `scripts/qa/release_gates.py`
  - `scripts/qa/package_gates.py`
  - `scripts/qa/label_overlap.py`
  - `scripts/qa/hook_sheets.py`
  - `scripts/qa/label_fix.py`
  - `scripts/qa/hook_image_match.md`
- `.github/workflows/pages.yml`: five file-existence checks before uploading
  the static `village/` directory.
- `README.md`, `village/README.md`, and `content/v2/README.md`: outdated root
  instructions and the current v2 documentation.

No tests were run and no recommendations were implemented as part of this review.
