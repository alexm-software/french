# Painting prompt

Compile from the manifest with `python3 tools/build_prompt.py manifest.json --write --output /tmp/room-prompt.txt`. This validates the plan first; failed plans do not overwrite files. Edit the manifest, not `prompt_text`; use `prompt_extra` only for necessary room-specific constraints under a named section. `--check` detects stale prompts. Attach the actual style references and, for zooms, the parent painting and crop. Reference paths in text are not image attachments.

```text
IMAGE: one integrated {room | zoom} painting, 1280x720, {camera: eye-level three-quarter from ...}, of {building} / {room name}.
[zoom only] Close-up of {parent room}'s {object/spot}: preserve the attached parent's object identity, materials, colors, contents, orientation and arrangement; same placement conventions. Add detail without replacing the object.
[repaint only] Fix: {rows}. Preserve all accepted details.

STYLE: storybook ink and gouache, dark contours; style slider {3: respectful, slightly realistic painterly with cartoony elements}. Match attached references {refs}, this {building's exterior | sector}, and materials {walls, floor, roof, wood/stone, palette}. Fully painted to the edges.

LIGHT AND COLOR: natural true colors and neutral daylight from {direction}; white whites, varied clothing. No whole-room amber, orange, sepia, pink or blue cast. Distinctive local light/palette: {time of day / light / dominant color}.

SETTING: {place}; landmark {landmark}; architectural whimsy {playful architectural feature}. Believable walls, floor and depth, with breathing room; no arbitrary clutter.

SITUATION: {named situation, e.g. feeding time in the school farmyard}. All hook actions belong to this shared moment.

COMPOSITION: interacting groups: {group 1: who, doing what with whom}; {group 2: ...}; {group 3: ...}. Angled, layered foreground/middle/back; varied facing, scale and box-bottom heights. Neither a lineup nor two bands nor a grid; no isolated display of gags. Read as one scene with labels removed. Distinguish these siblings: {sibling rooms and how they look}.

ITEMS: exactly {N (10 or fewer; zooms 4-6)} concepts, each with its entire recognizable sound cue and meaning visible together:
{n}. {word}: {gloss}; {shown}; {pose}.
Verbs: Monsieur Verbe, cheerful striped mime with suspenders and white gloves; berets {red -er | green -ir | purple -re | gold irregular}, as individually specified above. Pronominal verbs hold a mirror. Act on {noun} at human scale, distributed among nouns. Non-verbs have no mime costume.
Exact visible counts: {count list}. Reference board: {alphabet, number list, article table | none}. Plaque-only words: {list or "none"}, depict nothing beyond a blank plaque.

PLACEMENT AND SPACING: feminine noun centers left of 45%, masculine right of 55%; adjectives/adverbs in central 30-70% band. No dividing line. Whole item plus helper fits one tight nonoverlapping box, at least 77 px from the left and right edges and 43 px from the top and bottom (6%). Leave about 110 px between neighboring long labels and space below each item for its label. Do not hide key props.

DOORS AND EXITS: {door 1: to X, where, painted as a door that looks like X with a glimpse of it}; {door 2 / map exit: ...}. Clear floor-level thresholds at human scale; no props in openings. Beyond: {what lies beyond, per the plan}. Match the destination's actual appearance and reciprocal door design; plausible stairs and outdoor paths.

GROUNDING AND ANATOMY: held, mounted or supported props with contact shadows; no floating controls. Correct heads, limbs, hands, fingers and faces; hands connect to their own shoulders. No duplicates, merged bodies or severed parts.

FIGURES: word figures and their named helpers are distinct and recognizable. Background figures participate plainly, without separate gags or confusing props. Helpers never dominate their item. Animals behave naturally unless the hook explicitly requires otherwise.

TEXT: only declared natural scene text {text_in_image list, e.g. "CANTINE" on the sign over the counter | none}. Blank sign plates: {where}. No item captions, garbled lettering, speech bubbles, stray symbols or digits competing with counts. Labels are added by the site.

CONTENT: all ages; no crude humor, drinking, smoking, child romance, unsafe children or costume stereotypes. Alcohol/tobacco only closed untouched objects, with no children nearby. Grave/mature terms use plaques. Sacred subjects reverent: no depiction of God the Father, no whimsical props touching sacred things. Harmless playful hooks are welcome.

VARIETY: do not repeat existing hook motifs {used motifs, e.g. the duck, the red toy car}. This room differs by {how this room's camera, layout, focal action and light differ}.

AVOID: pasted-on figures, seams, lineup, shelves of separate gags, repeated motifs, blocked doors, clipped hooks, amber cast, stray text, floating props, merged or extra limbs, unexplained figures.
```

Review the compiled prompt once against the manifest. Numbers and positions are planning hints, not permission to distort boxes after painting. The final painting still needs visual review; see `validation.md`. For a repair, pass the whole painting as context, identify the target by appearance and location, specify accepted neighbors to preserve, and make at most one or two related changes. Reject reframing or collateral damage. After two failures, revisit the hook/composition before buying another attempt. Never assemble separately generated figures onto a background.
