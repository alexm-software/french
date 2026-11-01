# Painting prompt template (mandatory for every room and zoom painting)

Build every room or zoom painting prompt from the block below, with every `{field}` filled in. Generate it from the item manifest (builder reference/planning.md) with `tools/build_prompt.py manifest.json --write`, which fills every field it can and stores the text as the manifest's `prompt_text`; edit the manifest, not the prompt, and add free text per section with `prompt_extra` (precheck.py --manifest FAILS a manifest without it, a prompt_text missing any of the 15 section headings, an unfilled `{field}`, or an item word the prompt never names). Keep every line, even when a field is "none". The template only prevents rework: every gate still applies, strictly, to the finished painting. Delete only the bracketed hints. Each line traces to a gate (docs/skills-history/PROMPT_AUDIT.md); dropping one means repaints. The spacing numbers come from `skills/limits.json`.

```text
IMAGE: one integrated {room | zoom} painting, 1280x720 (16:9), {camera: eye-level three-quarter from ...}, of {building} / {room name}.
[zoom only] This is a close-up of {parent room}'s {object/spot}, a real spot where these objects belong: same object, materials, colors, contents and arrangement as in the parent painting (crop attached); the same gender sides and bands as the parent.
[repaint only] Fix these open repaint-queue rows: {rows}. Keep everything else that passed.

STYLE: storybook ink and gouache, dark ink contours, style slider {3: respectful, slightly realistic painterly with cartoony elements}. Same line weight, saturation and texture as the reference scenes {refs}. Matches this {building's exterior | sector} look and materials: {walls, floor, roof, wood/stone, palette}. Fully painted to every edge, no unpainted patches.

LIGHT AND COLOR: clear natural neutral daylight from {direction}, natural true colors (off-white walls, white whites, varied clothing). No golden, amber, orange, sepia or "cozy" cast; no orange, terracotta or peach walls; no pink or blue wash (natural blue sky, water and blossoms are fine). Set this room apart by {time of day / light / dominant color}, not by a color grade.

SETTING: a real {place} with its own walls, floor and depth, and one big nameable landmark: {landmark}. Only enough setting to be believable. Whimsy is tied to what the place holds: {playful architectural feature}. Use the whole frame (walls, windows, beams, stairs, ground), not just a foreground strip. The scene is lively but not too busy to read, with little non-item clutter.

SITUATION: one coherent everyday situation that everyone takes part in: "{named situation, e.g. feeding time in the school farmyard}". The hook props are part of this shared activity, used for it, not separate gags.

COMPOSITION: a natural scene, like a storybook illustration that still makes sense with every label removed. People and animals stand in small interacting groups of 2-4: {group 1: who, doing what with whom}; {group 2: ...}; {group 3: ...}. They look at, hand things to, help and react to each other. Facing directions vary (profile, three-quarter, back view, some toward the viewer). Depth varies, with foreground, middle and background figures, partial overlaps and changes of scale. Clusters with open floor between them. NOT a lineup, row, grid or evenly spaced arrangement; NOT everyone facing the viewer; NOT one isolated figure per gag. Items are in use (carried, cooked, sold, worn, repaired, argued over), not displayed in shelves, cubbies, pigeonholes, stall rows or display cases (at most one shelf as an element). The composition, camera angle, focal action and dominant light differ from the sibling rooms {sibling rooms and how they look}.

ITEMS: exactly {N (10 or fewer; zooms 4-6)}. One clear concept each. Each hook object is LARGE, prominent and unambiguous, and it touches or is acted on by the figure:
{n}. {word} = {gloss, in the sense this room teaches}: hook object {sound-alike thing}; shown as {what is shown, the same character and gender as the hook}; pose/action {pose}; count {exact integer or "-"}; at {side, zone, depth}; interacts with {group / neighbor}.
(repeat per item: the mnemonic action is visibly shown, not implied; no item could be read as an ordinary furnishing)
Verbs: Monsieur Verbe (cheerful mime: striped shirt, suspenders, white gloves, motion lines; beret {red -er | green -ir | purple -re | gold irregular}; holding a hand mirror when pronominal), at human scale, inside the scene and acting on {noun} as part of the situation. Verbs are spread among the nouns, not bunched in one zone or lined along an edge.
Non-verbs: ordinary people, creatures or objects with no mime look (no striped shirt with white gloves and beret).
Reference-board items {alphabet, number list, article table | none}: one board or poster, not a picture per letter.
Every hook element is visible: the sound-alike object AND the meaning, with any counted things shown exactly ({count list}), and each easy to count.
Plaque-only words {list or "none"}: a blank museum-style plaque on a stand, with nothing depicted.

PLACEMENT AND SPACING: feminine nouns clearly in the left half and masculine in the right half, with no divider. Adjectives and adverbs in the central 30-70% band; opposites may face each other. Each item, figure and key prop is fully in frame. Every item and its helper are compact enough for one tight box, at least 77 px from the left and right edges and 43 px from the top and bottom (6%). There are about 110 px between neighboring items and room under each figure for its label. No item overlaps or hides another.

DOORS AND EXITS: {door 1: to X, where, painted as a door that looks like X with a glimpse of it}; {door 2 / map exit: ...}. Keep every opening clear: no figure or prop overlaps a door frame, leaf or opening, or seems to grow out of it. Views through doors and windows show {what lies beyond, per the plan}, and the interior fits the exterior. Stairs go the way they lead; only ground-floor doors lead outside. Direction signs sit at the edges or overhead, never like an item's prop.

GROUNDING AND ANATOMY: every prop is held, mounted or resting on a surface, with a contact shadow. Nothing floats; a thrown thing is just leaving the hand with motion lines. Buttons, levers and taps are mounted on a machine, with the figure touching them. Correct anatomy (two arms, two hands, five fingers, normal faces). No severed body parts as props, no duplicated objects, nothing garbled or half-formed.

FIGURES: every figure is either a word's figure or the helper its hook names, beside that item, or plainly background scenery. Scenery is small or further back, takes part in the shared situation, is not the focus, does no gag of its own and holds no prop that could read as a word. Helpers are never bigger than their item. Each word figure is unique in character, age, profession, pose and scale. Animals are not anthropomorphic unless the animal is the hook. No decorative props that stand for no word.

TEXT: scene text only where it naturally belongs: {text_in_image list, e.g. "CANTINE" on the sign over the counter | none}, spelled correctly and clear of every item. Otherwise no letters or words, no symbols or currency signs on props, no digits (no shirt numbers, clocks or prices that could compete with a count), no speech or thought bubbles, no captions, and no labels naming items. Name signs are left as blank plates: {where}.

CONTENT: suitable for all ages. No crude or potty humor. Nobody drinks or smokes; alcohol and tobacco appear only as closed, untouched objects, with no child anywhere in such a room. No weapons. No child romance cues or children in unsafe spots. No depiction of God the Father; sacred things are shown reverently, with no whimsy on or touching them and no animals on crosses or altars. No cultural-costume shorthand or caricature (e.g. feathered headbands). Grave or mature words are never drawn. Harmless whimsy and cartoon slapstick are fine.

VARIETY: no repeated motifs across rooms: do not reuse a motif already painted in a sibling room or elsewhere in this building ({used motifs, e.g. the duck, the red toy car}). The composition is unique among the sibling rooms: {how this room's camera, layout, focal action and light differ}.

AVOID: lineup, row of figures, grid, evenly spaced, everyone facing the camera, one gag per person, isolated figures, sticker look, catalog, shelves of items, cubbies, display case, floating objects, props attached to nothing, figure in a doorway, amber/orange/sepia cast, warm grade, garbled text, random letters, numbers, speech bubbles, labels, captions, extra limbs, merged hands, severed body parts, duplicates, unpainted patches, items cut by the frame edge, drinking, smoking, cigarettes, weapons, potty humor, costume stereotypes, anthropomorphic animals {unless hook}.
```

**Fields to fill, all required:** camera, refs, materials, light, landmark, the named situation, the groups and their interactions, siblings, N, one line per item, the verb beret colors, plaque words, doors, text_in_image, sign plates, used motifs. The manifest holds the same facts as `scene_situation`, `interactions`, `siblings`, `used_motifs` and `prompt_text`.

**Before sending:** read the filled prompt against the manifest. Check that the item lines match exactly, the counts match `count`, every door is listed, and the scene text matches `text_in_image`. Then check it against the labels-off storybook test: would someone who has never seen the word list describe this as one believable moment?

## Accumulated failure rules

General rules learned from fixes. Each states a principle, not a case; check every new painting and every edit against all of them before packing.

- A door glimpse shows its destination room as planned and as painted: look up in the room plan where the door leads, then name that room's walls, floor, seating, furniture and colors in the prompt. Never a generic or invented room.
- A door pair matches on both sides: the same leaf count (single or double), leaf color, paneling, style and open state. Pass the other side's door as a reference image when painting or editing either side.
- Doors stand on the floor: the frame, the opening and the threshold run down to the baseboard line. A door may be partly hidden behind figures, but never floats above furniture or ends in mid-wall.
- A door edit removes everything in its way completely (furniture, remnants, shadows), and keeps every other door in the crop exactly as it was, including its open or closed state and its glimpse.
- Glimpses through doors and windows carry no digits, text, signs or people.
- No unexplained figures: when a word is dropped, its painted figure is painted out in the same pack, or the word gets a new fitting hook and spot. A figure with no word and no role in the situation is a defect.
- New or moved figures stay clear of door leaves and openings: name the door in the prompt and state that it stays completely clear.
- An edit mask that touches the frame edge runs to the edge. Rects in a union mask overlap, so no strip of the old painting is left between them.
- Edits must not introduce artifacts: compare every pasted edit with its base at 2x and fix seams, tone shifts, dents and remnants before packing.
- Record as you go: every crop box, mask, feather, base, result and sent prompt, rejected tries included, goes into the manifests.
- A door is painted at real door scale: a doorway taller than the grown-ups beside it, standing on the floor, with a leaf hung in the opening. An arch high in a wall, a niche, a flight of steps or a small picture of a door is not a door. Paint both sides with the same frame, leaf and hinge description, and name the destination room's signature features for each glimpse.
- Verb beret colors are stated explicitly in the prompt for every mime (red for -er, green for -ir, purple for -re, gold for irregular), with gold described as metallic and contrasted against yellow, mustard and brown. After painting, check every mime's beret against its verb's group before accepting.
- A mnemonic must be painted exactly as the hook says. Name the key animal or object unambiguously with its telltale features and negatives (a lamb: thick curly white wool, no horns, no beard). Check at 2x that a stranger would name it the same way, and keep the hook, the alt text and the dialogue naming the same thing.
- The hook object stays fully visible. No figure, prop or label may cover it. When adding, moving or resizing a figure, name the nearby hook props in the prompt and state that they stay clear.
- Check the gender bands and the label distances on every version, not only at the end: feminine box centres at or below 45%, masculine at or above 55%, adjectives and epicene words between 30% and 70%, and every label beside its own box.
- One idea per hook across the whole village. Before writing or keeping a hook, search all hooks.json files for its key object or pun. If another word already uses it, give the newer word a distinct hook and repaint to match.
- Solemn words (death, funerals, grief) get a hook only when it is vivid, literal and respectful. Otherwise give them a calm plain picture of the thing itself and put them on the hook form with their glosses. Never use a weak tag or a false etymology as a hook.
- An object that appears in more than one room (a hearse, a door, a person) is painted the same way and in a consistent place in each, and every alt text mentions it.
- A new vocabulary entry carries the full schema (gloss, IPA, respelling with the pee/poo check, CEFR, examples, related words). It goes in the room whose situation it fits, gets a picture of the word itself, and is added to that room's pinned dialogue.
- Write material colors in lowercase prose. Capitalized color words get painted as text, so add "nothing written on" the object.
- State the exact number of costumed figures (mimes), and describe every other figure as plainly not one of them: a normal face, no stripes, no beret.
- Costume markers belong only to the figures that carry a hook. Say who wears them and that nobody else does.
- Once a version is close, prefer a small edit to a full repaint, because repaints drift boxes, bands and details.
- Count every counted hook detail (candles, steps, figures) in a 2x crop before accepting a version.
- To add a hook figure to a crowd, transform one distinct existing figure instead of adding a new one, and name the neighbors that must stay unchanged.
- Identify an edit target by a unique position plus a unique appearance, never by role alone.
- Describe zones in running prose, never as headed sections. Headings get painted as separate panels.
- Limit an edit to one or two changes. More changes make the model drop or alter details elsewhere.
- Give each similar figure a distinct prop and posture. If a figure still fails after two tries, move its word to another room rather than forcing it.
- After every edit, re-check every hook in the room, not only the edited one. Edits can delete or alter neighbors.
- Check face paint and beret color against the manifest on every version.
- In every edit prompt, name the nearby props that must stay visible, especially hook props next to the edited figure.
- Doors and glimpses are fixed in the first painting. Big landmarks (doors, arches, windows) rarely move or rescale through edits, so state their scale and position up front.
- Run the pee/poo respelling check on every new word before install. Use a say override rather than a respelling that contains them.
- Dialogue wording must not trip the content filters. Describe objects plainly (a censer, not smoke) and run dialogue_check after every dialogue edit.
- After adding or moving doors or items, re-run strict placement on the whole building. Use labelAt when no automatic label spot is clear.
- Run grid_check right after any box tuning, before the strict build.
- Write dialogue and alt-text details from the room's hooks.json and the final painting, never from memory, and update them whenever a painting changes.
- Union masks are drawn as one shape and then eroded or feathered, so no seam or strip of the old painting survives where rects meet.
- When an edit moves or rescales figures that must stay, paste a clean-plate edit (the background without them) and restore the figures from the base with a keep-polygon. Keep the dark-keep zones tight, so no halo appears and no edge is lost.
- For small crop-edits, add "Keep the exact same framing, scale and camera position: do not zoom, crop or move anything." Verify alignment by mapping two or three landmarks (scale = output size / crop size). Reject a reframed result instead of trying to fit it.
- Inspect every new crop or result under a new view filename, because viewers cache by path.
