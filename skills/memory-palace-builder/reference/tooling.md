# Tooling and token economy

Use `room_context.py` for a target brief and `unbuilt.py --repo .` for live IDs. Do not repeatedly clone main, print entire building payloads, load all skill references, or paste generated prompts into chat. `build_prompt.py --write --output` stores the exact prompt and prints a short summary; `--check` detects drift.

One building plan + one manifest per room is the reusable context. Keep IDs, final hooks, geometry, references and decisions in those files, not repeated prose. Checkpoint only base commit, touched files, completed checks, next action and blockers. Avoid launching a new worker for each tiny revision; if work is delegated, give a bounded task and the manifest, not every audit ever written.

Cheap structural checks precede image calls. See `planning.md`; quality checks after painting are in `validation.md`. One contact sheet summarizes the room, but required 2× anatomy/count/hook inspection still applies. `zoom_sheet.py` builds actual parent-crop/zoom pairs with image hashes; a pending record is not a pass.

Generate whole scenes with shared style references. Reduce prompt/context repetition and retries, never visual coherence by generating the background separately from its figures. Each retry names a diagnosed failure and accepted details to preserve. Stop after two unsuccessful edits to revisit the plan.

Use unique review output paths per revision. Layout boxes are pixels, built `box` values are percentages and `boxPx` values are pixels. Rebuild generated data from authoritative layout; never hand-fix generated payloads. Run placement after geometry changes. Reuse existing scripts and render geometry rather than inventing a second implementation.
