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

ITEMS: exactly {item_count} concepts, each with its entire recognizable sound cue and meaning visible together. Near-synonym items stay visually unambiguous and do not share a shape:
{n}. {word}: {gloss}; {shown}; {pose}.
Verbs: Monsieur Verbe, cheerful striped mime with suspenders and white gloves; berets {red -er | green -ir | purple -re | gold irregular}, as individually specified above. Pronominal verbs hold a mirror. Act on {noun} at human scale, distributed among nouns. Non-verbs have no mime costume.
Exact visible counts: {count list}. Reference board: {alphabet, number list, article table | none}. Plaque-only words: {list or "none"}, depict nothing beyond a blank plaque.

PLACEMENT AND SPACING: feminine noun centers left of 45%, masculine right of 55%; adjectives, adverbs, and epicene nouns (article le/la) in the central 30-70% band. No dividing line. Whole item plus helper fits one tight box. Boxes may touch but must not overlap. An object may touch the picture edge when its box stays inside the frame. Leave 8 px of clearance for each label from the scene edge, and about 110 px between neighboring long labels. Do not hide key props.

DOORS AND EXITS: {door 1: to X, where, painted as a door that looks like X with a glimpse of it}; {door 2 / map exit: ...}. Clear floor-level thresholds at human scale; no props in openings. Beyond: {what lies beyond, per the plan}. Match the destination's actual appearance from its attached image, including materials and silhouette; a style reference must not replace them. Reciprocal door design; plausible stairs and outdoor paths. Paint a door only when both ends show that opening. Do not invent a door into an accepted room that has none. A glimpse through an opening shows that room's real floor, walls, and the exhibits the facing direction would see, and it adds no exit the room does not have.

GROUNDING AND ANATOMY: held, mounted or supported props with contact shadows; no floating controls. Correct heads, limbs, hands, fingers and faces; hands connect to their own shoulders. No duplicates, merged bodies or severed parts.

FIGURES: word figures and their named helpers are distinct and recognizable. Background figures participate plainly, without separate gags or confusing props. Helpers never dominate their item. Animals behave naturally unless the hook explicitly requires otherwise. A model, toy, or figurine cue sits at object scale on the shared surface with the people. It is not a life-size animal or a landscape.

TEXT: only declared natural scene text {text_in_image list, e.g. "CANTINE" on the sign over the counter | none}. Blank sign plates: {where}. No item captions, garbled lettering, speech bubbles, stray symbols or digits competing with counts. Labels are added by the site.

CONTENT: all ages; no crude humor, drinking, smoking, child romance, unsafe children or costume stereotypes. Alcohol/tobacco only closed untouched objects, with no children nearby. Grave/mature terms use plaques. Sacred subjects reverent: no depiction of God the Father, no whimsical props touching sacred things. Harmless playful hooks are welcome.

VARIETY: do not repeat existing hook motifs {used motifs, e.g. the duck, the red toy car}. This room differs by {how this room's camera, layout, focal action and light differ}.

AVOID: pasted-on figures, seams, lineup, shelves of separate gags, repeated motifs, blocked doors, clipped hooks, amber cast, stray text, floating props, merged or extra limbs, unexplained figures.
```

## Accumulated failure rules

Fold a repeated painting failure into the compiled template or into `plan_check`. Do not add an incident note.

- A passage that shows another place takes that place's materials and silhouette from its attached image. A style reference does not replace them. When the room returns to its sector, `prompt.refs` must name the sector map, or a crop whose pixels are that building's rectangle on it. The check does not look at the room painting.
- Near-synonym items do not share a shape. Each item's whole recognizable cue and meaning were already required together (ITEMS). The named helper must be that cue, with the item, and not a second figure that can be mistaken for it (FIGURES). Painting the named cue as a different object is an execution failure of those lines. Two-part hooks stay allowed.
- Group center (feminine under 45%, masculine over 55%, adjective, adverb, or epicene le/la noun inside 30–70%) and one box around the whole helper are already in PLACEMENT. Boxes may touch and may meet the frame; labels need 8 px from the edge. Judge the center of the painted group, not a band across the box. An empty placement diagram does not prove those rules were painted (`composition.md`). Epicene centre placement is the viewer's existing check, not a new side.
- A model, toy, or figurine cue is object-scale on the shared surface (FIGURES). A door is painted only when both ends show that opening, and a glimpse matches the facing view of the real room (DOORS AND EXITS).

Review the compiled prompt once against the manifest. Numbers and positions are planning hints, not permission to distort boxes after painting. The final painting still needs visual review; see `validation.md`. For a repair, pass the whole painting as context, identify the target by appearance and location, specify accepted neighbors to preserve, and make at most one or two related changes. Reject reframing or collateral damage. After two failures, change the method. If the new method fails, park the item and record why. Do not buy a third attempt of the same approach. Never assemble separately generated figures onto a background.
