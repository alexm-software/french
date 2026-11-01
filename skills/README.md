# Memory palace skills

Start with `memory-palace-builder/SKILL.md`; read only the references selected by its task router. Add `language-memory-palace/SKILL.md` for French conventions and `memory-palace-release-gates/SKILL.md` for acceptance and shipping.

- Builder owns plan → compiled prompt → integrated painting → integration.
- Language owns vocabulary, sense, pronunciation, mnemonic and verb conventions.
- Release gates own mechanical/visual evidence and acceptance.
- `limits.json` is the canonical density/spacing configuration; do not copy competing limits into documents.

Use `tools/room_context.py` instead of reading whole generated building payloads, and run `tools/plan_check.py` before image generation. `tools/README.md` lists the commands. Whole-scene painting is mandatory; reduce tokens through bounded context, compiled prompts and early checks.
