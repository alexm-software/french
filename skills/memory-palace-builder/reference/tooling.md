# Tooling and token economy

Use `room_context.py` (with `--init-manifest` for new rooms) for a resolved target brief and `unbuilt.py --repo . --building <id>` for live IDs. Do not repeatedly clone main, print entire building payloads, write ad-hoc one-liner scripts to join `vocab.jsonl`, load all skill references, or paste generated prompts into chat. `build_prompt.py --write --output` stores the exact prompt and prints a short summary; `--check` detects drift.

One building plan + one manifest per room is the reusable context. Keep IDs, final hooks, geometry, references and decisions in those files, not repeated prose. Checkpoint only base commit, touched files, completed checks, next action and blockers. Avoid launching a new worker for each tiny revision; if work is delegated, give a bounded task and the manifest, not every audit ever written.

Cheap structural and preflight checks (`plan_check.py`) precede image calls: source metadata agreement, verb beret/mirror verification, respelling/content/hook lint, Gate 25 depth/baseline distribution, and simulated label placement all run in memory before any image is generated. See `planning.md`; quality checks after painting are in `validation.md`. `contact_sheet.py --grid --anatomy-2x --sync-manifest` produces the room overlay, coordinate grid for 1-pass box fitting, and 2× quadrant crops for anatomy/count/hook inspection in one pass. `zoom_sheet.py` builds actual parent-crop/zoom pairs with image hashes; a pending record is not a pass.

Generate whole scenes with shared style references. Reduce prompt/context repetition and retries, never visual coherence by generating the background separately from its figures. Each retry names a diagnosed failure and accepted details to preserve. Stop after two unsuccessful edits to revisit the plan.

Use unique review output paths per revision. Layout boxes are pixels, built `box` values are percentages and `boxPx` values are pixels. Rebuild generated data from authoritative layout; never hand-fix generated payloads. Run placement after geometry changes. Reuse existing scripts and render geometry rather than inventing a second implementation.
