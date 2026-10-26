---
name: Memory palace builder
description: >-
  Use when designing or building any memory palace (method of loci) app, map, or
  illustrated set of rooms for memorizing a body of facts, in any subject. A
  one-page build checklist; detail lives in reference/*.md, read only when relevant.
---
# Memory palace builder

A one-page checklist for building an explorable memory palace. Each line is one checkable rule. The file named in a section heading holds the full rules and lessons; open it only when that topic comes up. Load the release-gates skill too, and the language skill for language palaces.

## Set up once (reference/setup-and-style.md)
- Fix subject, levels, setting, style slider (1-5), art style (ask), site look (ask and mock up), output.
- Record the audience and sacred/cultural sensitivities (reference/sensitive-content.md).
- Choose the art pipeline: painted empty room as the fixed scene, each item drawn to fit its slot.
- One canonical position per object in data; one style guide and prompt preamble for every image.
- Natural true colour in neutral daylight, no tint or cast; sectors differ by setting, never by grade.

## Plan before painting (reference/planning.md)
- Step 0 of every job: run `tools/unbuilt.py` and read the target building's partial/unbuilt rooms.
- "Unbuilt" is checked by word id across all live data, never by room id or memory.
- Build in order: inventory, assign to rooms once, sectors, world map, rooms, then site shell.
- Planned assignments are law; never re-pick words ad hoc.
- Hierarchy: world, sectors, sites, rooms, zoom spots; zooms are real spots where their objects belong.
- No one-object zooms: fold any zoom under about 4 words into a fuller scene.
- Placement encodes meaning (side, height, recurring prop); never tint the scene by category.
- Every word suits its place; no catch-all rooms; place by meaning, not a shared gloss word.
- Write the item manifest (`tools/manifest_template.json`): word, what is shown, pose or action, exact count, where verbs act, sensitive treatment, side or zone, doors and exits, zooms, intended scene text.
- Check the manifest against these checklists, fix it, and only then write the prompt and paint.

## Compose the room (reference/composition.md)
- Every figure or creature stands for one item; no decorative whimsy; props are hooks too.
- The sound-cue prop is large, and its helper touches or acts on the item.
- One clear concept per object; the mnemonic action is visibly shown.
- Exactly one tight hotspot per item (item plus helper); boxes never overlap or nest.
- Figures are unique in character, pose, scale and action; buildings get whimsy tied to their contents.
- Only enough setting to be believable; vary shapes, eras and architecture between rooms.
- Zoom spots follow the parent room's placement rules.
- Each room has a theme sign, clickable items with cards, a link back, and related links.
- Composite with feathered pastes, not low-frequency colour smears.

## Text, signs and labels (reference/text-and-labels.md)
- Labels and sign names are HTML/SVG overlays, styled to the material; they fit their sign at every size.
- Natural scene text that makes sense (shop sign, book spine, poster) may stay in the painting.
- No stray or garbled text, prop symbols ("$", "…"), count-breaking digits or speech bubbles.
- OCR (`tools/precheck.py`) flags text for a human to judge; it never auto-rejects.
- Declare intended scene text in the manifest's `text_in_image`.
- Signs never cover items; sign text is large and high-contrast; one label per thing.
- Every item always shows its label, on or just under its own figure, nearer to it than to any other.
- Budget about 110 px between neighbours with long labels.

## Hooks (reference/hooks.md)
- Store the hook in item metadata and explain it on the card; never drop an item for lack of a hook (fallback: a clear plain picture).
- Rate every hook (strong/ok/weak/plain) and recheck the weak ones; bulk batches run in parallel with exactly one merger.
- No placement phrase opens a hook; position is shown, not written.
- One hook per word everywhere; reject forced puns; weak -ment adverbs reuse the adjective's pun.
- Hook edits change only `hook` and `why`; the user's own hook rows load last in every build.

## Moving words (reference/moving-words.md)
- A move is three edits: inpaint the old spot, update the plan data, redraw the hook and painting in the new room.
- Never strip a live room below about 6 words without painting something back in the same pack.
- Count plan-only moves and sparse rooms with a script; report both counts at every stopping point.
- Paint-backs keep bands and sides; fix stale alt text and the parent miniature.

## Maps and navigation (reference/maps-and-navigation.md)
- Each map level is a zoom of the level above; the overview, sector maps and interiors agree.
- The overview is repainted in one pass, never patched.
- There are no disconnected areas; every place is reachable and has a way back.
- Links are physically plausible (doors, stairs, arches); stairs go the way they lead.
- Sub-rooms are reached through painted doors.

## Site and UI (reference/site-ui.md)
- The painting is the whole experience: true fullscreen, centred dialogs, no side panel.
- A highlight toggle shows clickable areas; doors carry badges; zooms carry a magnifier badge.
- Every space has a back control; navigation is walking; the top bar stays minimal.
- Cards are lean and show every option; a site guide explains the placement conventions.

## Safety and copyright (reference/sensitive-content.md, reference/copyright.md)
- Content suits all ages; mature words appear as text plaques only; sacred content is shown reverently.
- No children near alcohol or tobacco; nobody drinks or smokes; grave words go only to sober rooms.
- Don't over-police harmless whimsy.
- Audit everything that ships: quoted texts, glosses, data, fonts and code are public-domain, original or licensed and credited.

## Validate and run cheaply (reference/validation.md, reference/tooling.md)
- Run the cheap checks first (`tools/precheck.py`), then review one contact sheet per room (`tools/contact_sheet.py`).
- Open full-size crops only where the sheet raises a doubt.
- Run the room checks at the end of every room; validators follow reference/validation.md and report.
- Reuse one worker per workstream; keep content in data and generate pages from templates.
- Know px versus % units; use a new filename for every view crop.
- Add each new kind of issue as a rule (validation.md, "When something new comes up").
