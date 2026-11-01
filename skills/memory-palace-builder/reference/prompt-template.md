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
- Every hotspot box must tightly frame its painted item; if the band rules conflict with where the item is painted, repaint the item into the band instead of moving the box.
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

- When a liturgical cross must be patriarchal (two bars), name "patriarchal Cross of Lorraine with two horizontal bars, upper shorter" in the prompt and verify both bars at 2x on every cross in the crop before accepting; a single-bar Latin or Greek cross is a reject when the double-bar was required.
- Soft paste feathers on limb silhouettes against flat walls are defects: after any paste near a figure edge, check the silhouette at 2x for gray bleed into the wall and restore a clean opaque edge before packing.
- Bright remnant strips left by earlier clones or masks (a wall patch lighter than its neighbors) must be matched to local wall tone by cloning from adjacent clean wall, then checked at 2x so no lighter band remains.
- Leaf or foliage tips painted muddy olive-brown when the hook needs fresh green are defects: boost tip green (raise G, ease R) or repaint tips, and verify tip G>R at 2x before accepting.

- Respellings must stay age-appropriate in every reading, not only as whole tokens: reject a respelling if any syllable or hyphen chunk can be read as pee/piss/poo (or crude look-alikes such as "pist" → piss). Prefer a clean override (e.g. trappiste: trah-PEAST, never TRA-pist). Extend the pee/poo check to these substring and sound-alike cases before install.

- Hotspots are non-overlapping boxes on the hook itself (the object or gesture that carries the sound-alike), not on the whole figure; set them by hand from a zoomed view and check the bottoms with grid_check before building.
- Do not let an automatic box solver place hotspots: it shrinks boxes off the hook. Set boxes by hand and move a crowded label with a layout labelAt instead.
- Crop-edits zoom in on tight crops: use a crop at least twice the size of the change and say 'same size, same place' for every kept figure.
- Audit every door at zoom on the final painting (opening, frame and threshold clear of figures and props), not only after the first generation.
- A replace-figure edit can erase bystanders inside the crop: check every figure's extent before choosing paste rects, and paste only the changed figure.
- Paste seams on a checkered or patterned floor need a cleanup edit; compare the pattern at 2x across every seam.
- Never run a crop or paste script while a GenerateImage edit of the same painting is in flight; finish one edit before cutting the next crop.
- A pose edit can lift a figure into a door opening: ask for the lower pose explicitly (seated, kneeling) and check the head stays below the threshold line.
- Inherited vocab examples can trip content flags: run check_v2 content on every new word and override the example sentence when it flags.

- When an edit mask stops above a door or frame base, check the strip just below the crop at 4x for frame remnants; extend the mask or run a second small cleanup edit.
- To move a figure, use two edits: erase it in one (clean plate), then add it in the new spot anchored "directly beside <named neighbor>"; a single "move it" edit leaves ghosts or drops it.
- When a figure must fit between neighbors above and below it, ask for a low pose (kneeling or seated) so it stays inside its slot.
- Keep paste masks clear of crop edges wherever the edit shifted content, and check every seam at 3-4x.
- Name plain filler furniture for the outer strips of the room (for example "a tall bookcase against the right wall, nobody at it"), so the model does not push hook figures there.
- Before sending a prompt, remove contradictory placement sentences: each figure gets exactly one position.
- A room with many large foreground figures defeats percentage placement: split it into two rooms or cut figures before painting, instead of rerolling.
- A door to a room not built in the same pack is painted out (wall or furniture), never shipped as a dead door; restore the door when the room is built.
- In crowded rows, leave a label-wide gap (about 170 px for long words) between neighboring hotspots, or plan a labelAt spot on clear floor before painting.
- Small retouches that copy the painting's own pixels (no image model) are recorded like edits, with source and target rects, and flagged in the report.
- Run grid_check (gate 25) on the planned boxes in the LAYOUT MAP before the first GenerateImage call: at most three box bottoms per 40 px baseline, bottoms in back, middle and front depths, and no empty 150 px middle; a shelf or counter of hook props, or a front row of tables, is a grid even when each group is lively.
- A centaur is a human torso rising where the horse's neck and head would be: one body, four horse legs, no rider, no saddle, no separate horse head. Name this anatomy in the prompt for any hybrid creature (mermaid tail from the waist, griffin eagle front and lion back).
- Keep every held prop inside the figure's own silhouette and leave clear ground between neighbouring figures, so props never bridge two hotspots.
- Give every hook figure an explicit x/y percent box in the prompt; feminine items at centre x <= 45%, masculine items at centre x >= 55%, adjectives near the centre.
- To move, resize or sink a figure, erase it to a clean plate and composite a separately painted figure; never ask an edit for a pose or depth change of an existing figure.
- To add a creature to a finished painting, send the crop plus a reference cut-out of the creature in the same style, and name the exact spot by its neighbours.
- Plan box bottoms for grid_check (baselines, depths, no empty middle) when writing the layout, before the first generation.
- When removing a figure changes what a room's hook points at, rewrite the hook and the alt to describe what is now painted, then re-check the hook against the painting.
- Base scene prompts use every template section heading (ITEMS, PLACEMENT AND SPACING, DOORS AND EXITS, FIGURES, VARIETY included) and name each item by its French word as well as the English, even when the scene will later be built by composites.
- When a room loses or gains a hotspot, re-check the nameplate rect against every hotspot and the image edges, and move the nameplate onto clear wall or sky rather than trimming a box.
- Never compose hook figures or props as two rows of cells: stagger them over back, middle and front depths so box bottoms spread with no empty band of 150 px or more, and check this on the planned boxes before painting.
- To shrink or move an existing figure, erase it completely with a "remove completely, clean plate" edit and composite the original silhouette back at the new size or spot with its own contact shadow; edits that ask to shorten, tint or remove only part of a figure are ignored by the image model.
- Put small hook props on middle-depth furniture (shelf, lectern, high table) at a planned height, not on low floor tables that fall into the front row or behind a figure.
- Keep every door opening and its threshold clear of furniture and figures, including kneeling, crouching or sitting ones in front of the door.
- When a hub gains a door to a new room, place the door on clear wall away from every item box and move the item, never shrink the door below a ~120 px click target.
- Leave a label-height strip (about 35 px) of clear space below small high props, between their neighbours' boxes and the next figure, or plan a labelAt spot there before painting.
- When a word is rehomed into a finished room, crop-edit it onto an unhooked prop or an empty slot in its band, keep its box clear of every box, label and door, and re-run grid_check and the strict label check on that room.
- Send a non-square crop to the image model squared (padded to 1:1) and resize the result back to the exact crop size before pasting, so the edit stays aligned with the rest of the painting.
- When strict label checks fail in a dense room, trim each box to its hook figure or prop and set labelAt by hand on clear floor or wall, never over another hotspot, door or the nameplate; leave a label-height strip below small high props when painting.
- Sound-alike respellings never land on English toilet words (pee, poo, wee): pick a real word that sounds the same (PEA, PEAK, PEEK) and paint that.
- After any edit changes what is painted (a figure moved, a prop swapped), rewrite the hook, the shown text, the alt and the room's dialogue lines to name exactly what the final painting shows.
- To fix a gate 25 baseline, grow or trim a box only over its own hook figure (never onto a neighbour) so no 40 px window holds four bottoms; when you touch an already built room, run grid_check on it too and fix any failure it had on main.
- Name which figure holds each prop ("the gold-beret mime pushes the mower"), and paint every helper (herald, queen, child) as a separate ordinary person in different clothes, never merged into or dressed like the mime.
- Give each helper figure its own planned open ground inside its item's box, clear of neighbouring boxes; never let a helper stand behind or squeezed between another item's figures.
- For a before-and-after object, state the contrast explicitly (left half worn grey and cracked, right half glossy new) and use clean wood or paint colours; never red blotches, red drips or red goo on objects, heads or clothes, which read as raw meat or blood (use clear blue water for splashes).
- State the maximum figure height in pixels in the scene text and repeat it in each item, so figures do not grow past their depth band.
- A pixel height alone does not make figures small: set the scale with the camera (a high, far-back view of a large space) and say what fraction of the picture height each figure fills, and that groups stand apart like islands with open floor between them.
- Helpers that must look ordinary are described by what they have that the mime lacks (natural skin, no face paint, own clothes), and a counted prop says "exactly one" in the item line itself.
- After every base paint, count the painted item groups against the item list before judging anything else. A dense room (8 or more items) tends to drop one: tie each item to its own named landmark (fireplace, window, curtain, rug corner) in the prompt, and add a missing item with a crop edit onto planned open floor in its zone rather than repainting.
- An edit that removes a prop masks the whole old prop plus its shadow and outline; check the paste at 4x for leftover fragments, and where the mask must stop short of a neighbour, clear the remnant with a small extra rect or an inpaint limited to that strip.
- Whimsical rooms invite faces on scenery (a smiling chimney, a grinning door): add "no faces on objects or scenery" to FIGURES and AVOID unless the face is itself a hook (an invoked cloud), and crop-edit out any painted face that belongs to no word.
- A removal crop must contain the whole figure: measure its full extent on the full image first (beret to shoes, plus furniture legs, stools and shadows) and size the crop to include it; a crop that cuts the figure at its edge leaves legs or a bench behind, which then need a second edit.
- When a crop edit that adds a structure (a gateway, a door in a landscape) recomposes the crop twice, stop asking for an in-place edit: paint the structure as a self-contained patch at large scale from a crop of the destination, then scale it down and composite it with a silhouette mask (sky between battlements excluded, the glimpse through the opening kept) and a feathered base that fades into the ground.
