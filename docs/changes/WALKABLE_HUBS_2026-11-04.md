# Candidate review and walkable hubs

Base reviewed: `5305d134c7408b790cd1708887d75cb1a575be78`. This extends the new manifest preflight, coordinate grid and 2× review tools.

## Generation and validation

- Use compact room context for generation. On the nine-word farm, requesting an already-present move-in yielded 18 word records and 9,987 bytes in the full brief. Compact mode returned nine records and 3,181 bytes, a 68% reduction in output bytes. It carries canonical facts and live geometry together. Vocabulary is parsed once per command.
- Compile a manifest and its linked draft together. Match IDs, boxes, passage/zoom destinations and zoom parent before writing. Simulate labels against actual draft controls and report the shared grid result once. The unknown-ID path produces a diagnostic.
- Use a grid directly on a candidate image to fit the draft. With the draft, the contact sheet checks geometry and records image/layout hashes. The farm produces the packet without rebuilding; its inherited grid warning remains visible. Manifest sync requires the same building and room, exactly the same unique item IDs, valid boxes and a compilable prompt before atomic replacement.

## Hub and passage model

`content/v2/contes/walkthrough.json` is the pilot. Ownership and travel are separate. Overview and sector ownership come from the existing map registry. A building can add nested hubs by naming the containing hub for each place. Each physical passage has one record with shared appearance and two endpoints, including the arrival landmark and architectural location. Existing layout geometry binds each side to the correct door. The reusable skill script validates the tree and reciprocal edges, emits a covering walk, prints a room brief, and generates paired passage crops. The prompt compiler reads the same passage contract. A circulation hub can compile a prompt with zero vocabulary items.

The castle walk enters from the park, crosses the clearing and valley, passes the castle gate, climbs to the hall and returns through the courtyard. The courtyard owns the hall, so the hall's Hub shortcut now leads to the courtyard. The valley remains a physical stop on the route from the clearing. The generated castle payload matches the previous payload apart from hub ownership metadata.

I inspected paired crops for the existing five internal passages and the park entry. The internal pairs show recognizable destination cues. The park uses a storybook castle marker, while the clearing shows a black iron gate. The plan records that difference in map scale. This is a pilot using existing art. Future changes to a threshold should review both endpoint paintings, including door construction and arrival sightlines. Version 1 covers one sector threshold per opted-in building. Shared plans across buildings and additional sector exits need a later schema extension. Existing layouts can adopt the model incrementally.

## Data layout

The audited tracked tree held about 378 MB. Images accounted for 350 MB (93%), generated site data 7.7 MB, source/reference data 14.1 MB, and layout/source content 3.4 MB. The remaining files accounted for about 2 MB. These are tracked file sizes and exclude Git history.

Keep vocabulary and hooks in their current sources, layout geometry in the layout, and shared architectural facts in one walkthrough per building. Generate just the room-to-hub index for the viewer. The browser still loads its existing per-building payload. This avoids introducing a second vocabulary or map registry and keeps room prompts scoped. Further disk savings would mainly come from image formats and history. Further model-context savings would come from compact briefs and resolving shared card data once. Any future runtime deduplication needs to preserve room-specific hook, wording and crop overrides.

## Verification

Existing workflow fixtures plus regressions cover unknown IDs, rejected partial or wrong-room sync, hub cycles, missing return edges, unreachable hub descendants, and compiling a circulation hub with shared passage cues. The farm draft packet and linked prompt were exercised against local source data. Strict castle placement and dialogue checks passed, and the app script passed syntax checking. Browser route expectations were updated for opted-in hubs. Live browser interaction was not exercised locally.
