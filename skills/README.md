# Skills

The memory palace build skills, kept in sync with the bot. Start with each `SKILL.md`: it is a one-page checklist with a task router at the top saying which reference files a task needs.

- `memory-palace-builder/`: building any memory palace (planning, prompts, composition, labels, hooks, maps, site).
- `language-memory-palace/`: the language layer (levels, representation, verbs, hooks, placement, cards).
- `memory-palace-release-gates/`: the gates a room must pass before it ships.
- `limits.json`: the room-size and spacing numbers; the skills quote it and the scripts read it.
- `CHANGELOG.md`: what changed in the skills, and the incident history that used to sit inside the rules.

The generated audit tables (`PROMPT_AUDIT.md`, which traces each prompt line to a gate, and `COVERAGE.md`, which traces each rule to its file) are in `docs/skills-history/`, so reading the skills folder does not load them.
