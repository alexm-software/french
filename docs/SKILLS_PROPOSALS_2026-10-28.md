# Proposals: fewer build errors and fewer tokens in the memory-palace skills (28 October 2026)

These are proposals only. No skill, script or data file has been changed.

**What was reviewed:**
- the three skills in `skills/`: the `SKILL.md` checklists and their 30 reference files, plus `PROMPT_AUDIT.md` and `COVERAGE.md`;
- `tools/` and `scripts/qa/`, and the GitHub workflow;
- the live data on main (PR #176), to see which rules actually hold on the site.

## Summary

The skills are thorough: 357 traced rules, a planning gate, a prompt template, and cheap checks before anyone looks at images. Most errors that still reach main come from five gaps:

1. **Rules written down but not enforced.**
   - 67 of the 477 live rooms exceed the 12-item gate.
   - 28 word ids still have two different hooks.
   - 554 hooks quote a respelling that differs from their card's.

   The gate scripts pass anyway, because they don't check these things.
2. **Nothing runs on a pull request.** The only workflow deploys to Pages after a merge, and its check is that 5 files exist.
3. **Seven scripts the skills tell you to run aren't in the repo**, along with several files they tell you to read.
4. **The skills contradict themselves** on the art pipeline, and give room-size numbers six different ways.
5. **Hand transcription:** the 15-section prompt, the sibling and motif lists, and the hooks are all typed by hand from data that already exists.

**Tokens.**
- About 170 KB of audit files sit inside `skills/`.
- Planning a room means reading data files of up to 128 KB each.
- The prompt template (about 2,400 tokens) is re-typed for every room.
- Every repaint re-reviews every crop.

The proposals below would cut most of that and remove whole classes of errors. They're in priority order.

---

## A. Reducing errors

### A1. Enforce the rules the skills already state (highest value)
Rules that say "script-check" or "fails" but that no script fails on, with evidence from main today:

| Rule | Where | Now on main | Proposal |
|---|---|---|---|
| At most about 10 items; more than 12 fails | gates SKILL.md §C.12 | **67 rooms over 12.** Highest: `ecole/tableau` 26, `cabinet/organes` 18, `route/carrefour` 18, `eglise/eglise` 17, `monde/monde` 17. All 10 `cirque` rooms are at 15–16. | FAIL in `check_v2.py`, with an explicit allowlist file for real reference boards (the alphabet blackboard) |
| One hook per word everywhere; "script-check that no id has two different hook texts" | builder hooks.md | **28 ids** have two hook texts | FAIL in `check_v2.py` |
| Hook pre-screens (G28): "Like English" with no twist rated strong, sound-alike equal to the gloss, meta or placement openers, openings shared by more than 5 hooks | item-gates.md | Done by eye, if at all | A `tools/hook_lint.py` (A5) |
| Respelling in the hook matches the card's `say` | implied by "derive the sound-alike from the pronunciation" | **554 mismatches** (e.g. *actuel*: card 2 syllables, hook 3) | Lint check; a script fixes the spelling-style ones automatically |
| Placement by meaning, not by a shared English gloss word | language placement-and-senses.md | `placement.py` exists, but its findings only fail with `--placement`, which the documented build line doesn't pass | Pass `--placement` in the release and pull-request runs, with the existing `placement_ok.tsv` as the allowlist |

### A2. Run the gates on every pull request
Add `.github/workflows/checks.yml`. On every pull request it would run:
- `scripts/v2/build_v2.py`, then `check_v2.py --strict --placement`;
- the new lints (A1 and A5);
- a check that every path the skills mention exists (A3).

Today, several agents (Cursor, Codex, Claude) merge into main, and nothing stops a pull request that breaks a gate. One automated reviewer catches what each agent's own checks miss, and it's the cheapest error-reducer here.

### A3. Commit the missing scripts, or stop pointing at them
The skills tell you to run these, but none is in the repo:
- `scripts/qa/release_gates.py`
- `scripts/qa/package_gates.py`
- `scripts/qa/label_overlap.py`
- `scripts/qa/hook_sheets.py`
- `scripts/qa/label_fix.py`
- `scripts/qa/hook_image_match.md`
- `reflexive_mirror_check.py`

They also mention `user_hooks_need_repaint.tsv`, `qa_020` / `qa_100`, `REPAINT_QUEUE` and "MKTA PROMPTS.md", none of which exist here.

An agent following the skills either wastes tokens looking for them or quietly skips the gate. **Proposal:** commit the scripts if they live in another workspace, or rewrite those lines to name what replaces them (`check_v2.py`, `precheck.py`, `contact_sheet.py`). Then let the A2 path check keep it that way.

### A4. Remove the contradictions
- **Which art pipeline?**
  - *Separate assets placed into an empty room:* the builder SKILL.md line "painted empty room as the fixed scene, each item drawn to fit its slot", gates E and F, and G99 "scene first, then assets drawn to fit".
  - *One integrated painting with the objects painted in:* the prompt template, `village/README.md`, and N8.

  An agent can follow either one and pass half the gates. **Proposal:** state the current pipeline in one line at the top of the builder skill. Move the other pipeline's rules to a clearly marked "legacy: composited scenes" file that loads only when someone repairs an old composited room.
- **Room-size numbers** appear in six forms:

  | Source | Main rooms | Zooms |
  |---|---|---|
  | language SKILL.md | "about 10-12" | "about 6" |
  | gates | "at most about 10 (more than 12 fails)" | — |
  | prompt template | "10 or fewer" | "4-6" |
  | planning.md | "8 to 12 or more" | "6 to 12" |
  | N6 | — | "fold under about 4" |

  **Proposal:** one `skills/limits.json` (room max, room target, zoom min and max, edge margin 6%, label gap 110 px, center band 30–70%) that `precheck.py` and `check_v2.py` read. The skills quote the file instead of repeating numbers.
- **Alphabet:** the gates say "one blackboard zoom… no per-letter mnemonics". This conflicts with my own proposal in `docs/PROPOSALS_2026-10-28.md` §1.5 (puns for tricky letters). I withdraw that proposal: the rule should win.

### A5. A hook linter (`tools/hook_lint.py`)
It would check every hook in the build output against `vocab.jsonl`:
- the bracketed respelling matches `say`;
- "Like English" or "Same as English" only on words with `cognate_type: true_cognate`;
- no "Linked to …", "Think of …", "Latin", "root" or etymology wording;
- no placement opener, and no opening phrase on more than 5 hooks;
- the meaning appears in CAPS;
- the sound-alike isn't the gloss and isn't the French word;
- puns of more than two chunks are flagged (counting quoted segments joined by "+" or "-");
- the hook names the same figure as the room's `alt` text, as a cheap stand-in for G24.

It would also check the example sentence: the example's English contains the card's first gloss. Severity: WARN while the existing hooks are cleaned up, FAIL for new and repainted rooms. This turns the mechanical half of gate 5 into a script, and leaves the eye pass for what scripts can't judge.

### A6. Generate instead of transcribe
These are the steps where facts are re-typed by hand, which is where mismatches creep in:
- **The prompt:** `tools/build_prompt.py manifest.json` writes the full template text from the manifest. `precheck.py` then checks that `prompt_text` equals the generated text (plus any declared free-text additions). That removes "unfilled `{field}`", "item missing from the prompt" and "item line doesn't match the manifest" as possible errors.
- **Siblings and used motifs:** `tools/room_context.py --building ecole` reads the building's layout, alt texts and hooks and lists the sibling rooms (camera, light, focal action from the alt), the motifs already used, the open repaint rows and the planned words still unbuilt. The manifest pre-fills from it.
- **Layout and hooks:** `tools/manifest_to_layout.py` writes the `layout.json` item skeleton (ids, sides, bands) and the hook rows from the manifest. The painter then only adds pixel boxes, in one unit, which removes the px-versus-% hazard (B226).

### A7. A cheap automatic look at each crop before human review
The most common miss in the gate history is the **sound-clue object not painted** (G24: "no viola for violet, no boar for boire"). Before the contact-sheet review, ask a small vision model one yes/no question per 256 px crop: "Is there a {hook object} in this picture?" The objects come from the manifest's `hook object`. Show the misses on the contact sheet in red. A miss is a question for the reviewer, not a verdict, like OCR flags. A yes/no answer is cheap, and the reviewer's attention goes where it's needed.

### A8. Make the history readable, or move it out
The reference files mix rules with incident history:
- "Refined at 12:25 UTC after 1216Z"
- "the 0951Z review missed 7 missing mirrors"
- "(v13.1)" and "CHANGED in v13" tags (13 of them)
- 16 "Once, …" stories

The stories help, but timestamps and internal names mean nothing to a fresh agent and can be misread as current instructions. **Proposal:** keep one short example per rule. Move the dated history to `skills/CHANGELOG.md`. Rewrite references to internal names (`qa_020`, `REPAINT_QUEUE`) as the file or tool to use.

### A9. Independent review with a fixed rubric
G47 (another worker signs off on each crop review) is a good gate. Make it checkable:
- the reviewer writes `review.json`: space, gate, pass or fail, note, reviewer id, commit;
- `package` refuses to build when the reviewer id equals the painter id, or when any row is "pending".

It's the same rule, but a script holds it, not memory.

---

## B. Reducing token use

| # | Proposal | Saving (rough) |
|---|---|---|
| B1 | **Move `PROMPT_AUDIT.md` (78 KB) and `COVERAGE.md` (91 KB) out of `skills/`** to `docs/skills-history/`. They're generated audit tables, not instructions, but an agent that loads or searches the skills folder pays for them. | Up to about 42,000 tokens whenever the folder is read whole |
| B2 | **A task router at the top of each `SKILL.md`**: "Paint a new room → planning.md, prompt-template.md, item-gates.md §A, space-gates.md §C and §G. Fix labels only → text-and-labels.md, space-gates.md §B. Hook rewrite → hooks.md, language hooks.md." Today "read only when relevant" is vague, so agents read most references. | 30–60% of reference reading per task |
| B3 | **Generate the prompt (A6).** The agent writes about 20 short manifest fields instead of re-typing a ~2,400-token template, and the fixed sections become a constant prefix that can be prompt-cached. | ~2,000 output tokens per room or repaint |
| B4 | **Compact room context (A6, `room_context.py`)**, about 1–2k tokens, instead of reading `village/data/<bld>.js` (up to 128 KB, mostly card text and verb tables), `layout.json` (44 KB for the école) and `hooks.json` (25 KB). | ~40,000+ tokens per building job |
| B5 | **Review only what changed.** Store a hash of each item crop with its last passing review. On a repaint, the contact sheet shows only new or changed crops in full, and unchanged items as a small "unchanged since …" strip. G52's whole-site re-audit stays scripted; the eye pass covers only rooms touched by the new gate. | Most vision tokens on repaints |
| B6 | **Quiet scripts.** `check_v2.py` prints 75 lines on a pass (every building's word counts). Default to one summary line plus FAILs and WARNs, with `--verbose` for the rest; same for `precheck.py` and `unbuilt.py`. | Small per run, but they run constantly |
| B7 | **Slim the references.** Short anecdotes, version tags and repeated cross-references ("see builder reference/…" in three places) are an estimated 15–20% of the reference text. With A8, the references shrink without losing a rule. | ~15–20% of every reference read |
| B8 | **A stream state file** to go with N7 (one worker per workstream): `streams/<name>.md` with the stream's current task, open queue rows and last commit, about 20 lines. A replacement worker reads that instead of the chat history. | Large when a worker is replaced |
| B9 | **Hook batches with only the fields needed:** lemma, respelling, gloss in this room's sense, the room's situation and the motifs already used. Not whole `vocab.jsonl` records, which carry the CEFR source, the Wiktionary gloss, notes and examples. | ~70% of input per hook batch |

---

## Suggested order
1. **A2:** add the pull-request workflow, starting with `check_v2.py --strict --placement`.
2. **A1:** add the item-count and one-hook FAILs. Tidy the 67 rooms and 28 ids, or add allowlist entries for them.
3. **A3 and A4:** commit or rewrite the missing scripts, choose one pipeline, and add `limits.json`.
4. **B1 and B2:** move the audit files out, and add task routers. These are minutes of work for an immediate token saving.
5. **A5 and A6:** the hook linter, then prompt and context generation (this also delivers B3 and B4).
6. **A7, A9, B5:** the yes/no vision pre-check, review files, and change-only review.
