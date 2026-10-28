# Skills changelog

## 28 October 2026
- **One pipeline.** The builder skill now states the current pipeline at the top: one integrated painting per room or zoom, objects painted in. The composited rules (release gates E and F, "Scene first, then assets drawn to fit") are marked legacy: they apply only when repairing an old composited room.
- **One set of numbers.** Room target and maximum, zoom size, room floor, edge margin, label gap and centre band now live in `skills/limits.json`. The skills quote it; `check_v2.py`, `precheck.py` and `build_prompt.py` read it. Before, the room size was given six different ways.
- **Gates held by scripts.** `check_v2.py` fails a room over `room_max` and a word with two different hooks, each with a baseline allowlist (`data/hooks/qa/room_size_ok.tsv`, 66 rooms; `two_hooks_ok.tsv`, 28 ids) for what was live before the gate. `tools/hook_lint.py` does the mechanical hook checks. `.github/workflows/checks.yml` runs the gates, the hook lint and `tools/skills_paths.py` on every pull request.
- **No missing tools.** Lines that named scripts not in this repo (`release_gates.py`, `package_gates.py`, `label_overlap.py`, `hook_sheets.py`, `label_fix.py`, `hook_image_match.md`, `reflexive_mirror_check.py`) and internal names (`qa_020`, `qa_100`, `user_hooks_need_repaint.tsv`, `REPAINT_QUEUE`) now name what replaces them.
- **Generated, not typed.** `tools/build_prompt.py` writes the painting prompt from the manifest; `tools/room_context.py` gives a compact brief of a building.
- **Task routers** at the top of each `SKILL.md`.
- **Audit tables moved** to `docs/skills-history/`.
- **Version tags removed** from the rules ("(v13)", "(v13.1)", "CHANGED in v13"). Everything they marked is current.

## Incident history moved out of the rules
- User-hook coverage gate (builder hooks.md, G63): refined at 12:25 UTC after the 1216Z review, so that a hook mismatching its painting can never go live while a build no worse than live is not blocked.
- Integration mirror check (release gates process.md, G64): the 0951Z review missed 7 missing hand mirrors because it trusted the package verdicts.
