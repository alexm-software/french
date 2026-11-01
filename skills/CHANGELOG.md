# Skills changelog

## 1 November 2026
- **FANTASY2 failure rules** (builder reference/prompt-template.md): stagger depths instead of two rows of cells; shrink or move figures by full erase plus composite with contact shadow (partial edits are ignored); small props on middle-depth furniture; door openings and thresholds kept clear of figures; new hub doors on clear wall, move items rather than shrink doors; label-height strip below small high props.
- **MAIRIE6 failure rules** (builder reference/prompt-template.md): rehomed words go on an unhooked prop or empty band slot and re-run grid_check; non-square crops are sent squared and resized back before pasting; dense rooms trim boxes to the hook and set labelAt by hand when strict label checks fail; no toilet-word respellings (PEA, PEAK); hooks, shown text, alt and dialogue are rewritten to match the final painting; gate 25 baselines are fixed by growing or trimming a box over its own figure, and touched built rooms are re-gated.
- **MAIRIE5 failure rules** (builder reference/prompt-template.md): check below a mask that stops above a door base for frame remnants; move figures with an erase edit plus an anchored add edit; low poses for tight slots; paste masks clear of shifted crop edges; named filler furniture for outer strips; no contradictory placement sentences; split rooms with too many large foreground figures; paint out doors to unbuilt rooms; leave label-wide gaps or plan labelAt spots; record pixel-copy retouches like edits; run grid_check on the planned boxes before painting.
- **More accumulated failure rules** (builder reference/prompt-template.md, from MAIRIE4): hotspots sit on the hook itself, set by hand (no auto solver; use labelAt for crowded labels) and pass grid_check before the build; crop-edits use wide crops and say "same size, same place"; doors are audited at zoom on the final painting; replace-figure edits are checked for erased bystanders; patterned-floor paste seams get a cleanup edit; no crop or paste while an edit of the same painting is in flight; pose edits ask for a low pose and keep heads below door thresholds; inherited vocab examples are run through the content check and overridden when they flag.
- **Accumulated failure rules** (builder reference/prompt-template.md): door glimpses show the planned destination, door pairs match on both sides, doors stand on the floor, door edits remove what is in the way completely, no text or people in glimpses, dropped words' figures are painted out, figures stay clear of doors, edge masks run to the edge and union masks overlap, edits are checked at 2x, and every mask and prompt is recorded.

## 31 October 2026
- **Gate 23, angled layered scenes.** Each room is composed as an angled, layered scene (foreground, middle, back) around one named situation; a frontal one- or two-row lineup fails.
- **Gate 24, one generated painting.** Each room is ONE generated painting (square-centre generation plus one outpaint, or a crop-edit of that painting); no cut-out or green-screen sprites on a background plate and no code-drawn marks.

## 29 October 2026
- **Room cap 15.** `room_max` in `skills/limits.json` is now 15 (was 12), owner decision for the verb migration. Rooms are not split just to stay under 12; zooms stay 4-6. Verb-street side rooms are kept as homes for leftover verbs with no natural room.
- **Hook-crop gate.** For every repainted room, crop each item's hotspot at 2x and confirm every concrete detail its hook names is painted inside the box; fix mismatches before packing.
- **Asset-per-word pipeline deleted.** Removed release gates E (per-word assets) and G99 (sprites drawn to fit), the B70/B72 empty-background and per-asset alternatives, the sprite line of the prompt template and the feathered-paste compositing rule. F is now a final-scene check for integrated paintings (G83: no seams or pasted patches). Local fixes edit a region with the whole painting as context; otherwise repaint the room.
- **Copyright gate for quoted texts** (builder reference/copyright.md, release gates, language skill): dated public-domain edition or our own translation, recorded source and usage, named in CREDITS.md, and `tools/copyright_check.py` on every pull request.

## 28 October 2026
- **One pipeline.** The builder skill now states the current pipeline at the top: one integrated painting per room or zoom, objects painted in. The composited rules (release gates E and F, "Scene first, then assets drawn to fit") are marked legacy: they apply only when repairing an old composited room.
- **One set of numbers.** Room target and maximum, zoom size, room floor, edge margin, label gap and center band now live in `skills/limits.json`. The skills quote it; `check_v2.py`, `precheck.py` and `build_prompt.py` read it. Before, the room size was given six different ways.
- **Gates held by scripts.** `check_v2.py` fails a room over `room_max` and a word with two different hooks, each with a baseline allowlist (`data/hooks/qa/room_size_ok.tsv`, 66 rooms; `two_hooks_ok.tsv`, 28 ids) for what was live before the gate. `tools/hook_lint.py` does the mechanical hook checks. `.github/workflows/checks.yml` runs the gates, the hook lint and `tools/skills_paths.py` on every pull request.
- **No missing tools.** Lines that named scripts not in this repo (`release_gates.py`, `package_gates.py`, `label_overlap.py`, `hook_sheets.py`, `label_fix.py`, `hook_image_match.md`, `reflexive_mirror_check.py`) and internal names (`qa_020`, `qa_100`, `user_hooks_need_repaint.tsv`, `REPAINT_QUEUE`) now name what replaces them.
- **Generated, not typed.** `tools/build_prompt.py` writes the painting prompt from the manifest; `tools/room_context.py` gives a compact brief of a building.
- **Task routers** at the top of each `SKILL.md`.
- **Audit tables moved** to `docs/skills-history/`.
- **Version tags removed** from the rules ("(v13)", "(v13.1)", "CHANGED in v13"). Everything they marked is current.

## Incident history moved out of the rules
- User-hook coverage gate (builder hooks.md, G63): refined at 12:25 UTC after the 1216Z review, so that a hook mismatching its painting can never go live while a build no worse than live is not blocked.
- Integration mirror check (release gates process.md, G64): the 0951Z review missed 7 missing hand mirrors because it trusted the package verdicts.
