---
name: Memory palace builder
description: >-
  Use when designing or building any memory palace (method of loci) app, map, or
  illustrated set of rooms for memorizing a body of facts, in any subject.
---
# Memory palace builder

A generic recipe for building an explorable memory palace (a world of places where each fact is pinned to a vivid image at a fixed location). For language learning, also load the language memory palace skill, which layers on top of this one.

## Settings to fix up front
- **Subject and scope**: what body of knowledge, and its levels (e.g. beginner to expert).
- **Setting**: the overall world (village, castle, ship, campus). Prefer an idyllic, real-life-plausible place so layout feels natural.
- **Style slider** from 1 (very cartoonish) to 5 (realistic). Record the chosen value and use it in every image prompt so rooms stay consistent. Example: 3 = respectful, slightly realistic painterly with cartoony elements.
- **Art style (ask, don't assume)**: before painting anything, ask what art style the person wants. Cover the medium and look (painted storybook, watercolour, flat cartoon, realistic), the colour feel (natural true colours vs a stylised palette), lighting, and how whimsical the characters should be. Generate 1-2 sample scenes in the chosen style and get a yes before making all the art.
- **Site look (ask, and mock it up)**: ask what feel they want for the website itself (e.g. whimsical storybook vs clean and minimal), then show a mock-up image of a real screen, such as a scene with an item card open, and one for each distinct card type (noun, verb). Iterate on the mock-up until they approve, then hand the approved image to the site builder as the style reference.
- **Sacred and cultural respect**: religious content is depicted reverently. Never mock sacred figures, objects, or rites; keep whimsy in nearby props or the mnemonic character, never on or touching sacred objects; follow the tradition's own sensitivities (ask the user which ones apply, e.g. no depictions of God the Father, no animals on crosses or altars). When unsure, show the item as text instead.
- **Audience**: default to all ages. No crude terms, profanity, or crude mnemonics. Mature-but-necessary items are shown as text (e.g. a museum wall plaque), never drawn.
- **Output**: static site (e.g. GitHub Pages), print, or images only.

## Hierarchy
World map, then sectors (districts), then sites (buildings or outdoor spots), then rooms, then zoom spots: desks, tables, shelves, cabinets, or altars modeled as first-class small rooms (type zoom, with a parent room, their own sign and theme, a position in the parent, and about 6 to 12 small items). Users zoom in and back out. They keep parent rooms uncluttered and reduce the number of full rooms; count them separately. Some map areas can open a site directly. Every room links back to its sector, and may link to related rooms. Sectors connect to each other both from the world map and from neighboring sectors.

## Build order (always in this sequence)
1. **Inventory**: list every item to memorize with its metadata (level, category, sub-category). Keep it in a machine-readable data file (JSON/YAML/CSV), not prose.
2. **Assign items to rooms** by theme. Set density targets per room type and record them (e.g. 8 to 12 or more for rooms of simple items, scaled by object size; 4 to 6 for rooms of complex items that carry lots of attached detail). Split a room or add zoom spots before it gets crowded.
3. **Group rooms into sectors** by common theme or real-life layout (e.g. a house holds kitchen, bedroom, bathroom).
4. **Lay out the world map**: place sectors, connect them, and define a starting point plus mostly-linear suggested paths that still allow free roaming.
5. **Design each room**, then run the room checks below before moving on.
6. **Build navigation, extras, and the site shell** (about page, quiz, audio, full screen).

## Encode meaning in placement, not only in images
Use fixed spatial rules so position itself carries information. Decide them once and apply everywhere, and show a legend on the about page. Examples:
- Left vs right side of the room for a binary category (e.g. grammatical gender).
- Do not tint the scene itself by category (it looked unnatural); if a color cue is wanted, apply it to the item's label or card text instead.
- Height (floor, table, shelf, ceiling) for frequency or level.
- A recurring prop for a property (e.g. a mirror for a reflexive form, a door plaque for associated rules).
- Distinct building types or streets for distinct item classes.
- Everything that belongs to one item stays together in one place (one building, one object).

## Mnemonic images
- Each item is a zany, whimsical object, character, or creature that both sounds like the item (when said aloud in the learner's language) and visually represents its meaning.
- Props that carry the sound cue must be large, prominent, and unambiguous.
- A helper character that carries the sound cue must sit right next to (visibly interacting with or pointing at) the item it helps with, never far across the room.
- Store the mnemonic hook in the item metadata (sound-alike, one-line scene, strength, fallback) and always explain it on the item's detail card when clicked.
- Never drop an item because a good or respectful mnemonic is hard. Fallback: depict the item itself clearly and well. Near-identical cognates need no pun, and the plain item is enough.
- Keep one clear concept per object; avoid scenes where the prop could be read as an ordinary furnishing.
- Vary designs so rooms, buildings, and sectors never start to look the same: change shapes, palettes, eras, and architecture.

## Each room must have
- A sign naming the room's theme.
- Clickable items opening a detail card with the full information.
- A link back to the sector, and links to related rooms where they make sense.
- Optional extras: scenes or dialogues, audio, quiz entries.

## Room checks (run at the end of every room, before moving on)
1. Nothing important is conveyed only by hidden or tiny text; every item is visible as an image (except mature items deliberately shown as text).
2. All sign and label text fits inside its sign at all supported screen sizes. Render text as real HTML/SVG text over images, not baked into generated images, so it is legible and correct, and style it to blend into the scene (carved, painted, engraved, or chalk lettering matching the material) rather than looking like a UI label.
3. No copyright problems: write your own definitions and explanations, or use openly licensed sources with the required attribution recorded in a credits file. Generate or draw all images yourself.
4. Every mnemonic actually works: say the sound-alike aloud, confirm it resembles the target, and confirm the picture also points to the meaning. Reject weak ones and redesign.
5. Placement rules are obeyed (correct side, tint, prop) and positions match between the world map, sector view, and room.
6. Room density is within the target range; overflow goes to a new room or zoom spot.
7. Age-appropriate content only.
8. Religious and cultural imagery is reverent and follows the sensitivities recorded for the project.

## Art pipeline
Choose between generated illustrations (richer, harder to keep consistent and edit) and hand-coded SVG (each item a separate <g> with an id, class, and title, so it is clickable, consistent across map/sector/room, and editable). Show the user one example room in each candidate pipeline before committing. A generator script that emits SVG from the room data keeps token use low.

## Asset structure
Lessons from testing: flat vector SVG looked noticeably uglier than painted art, and painted cutouts composited onto a painted room looked jarring (different brushwork and lighting, sticker effect) even with shadows and color matching. Prefer one full painting per room plus a hotspot data file (polygon or box per item) for clickability; edit by regenerating the room with the previous image as a reference. If you do composite, generate objects with the room as a style and lighting reference.
Alternative: keep each item as its own asset (one file per object) and each room as an empty background plus a layout data file (object id, position, scale, z-order, category side). A build script composes rooms, sector views, and the world map from these, so edits touch one small file, objects are reused consistently across views, and token use stays low. Shared style rules (palette, outline weight, light direction) plus an auto-added ground shadow make objects sit naturally in the scene. Large fixed features that interact deeply with the architecture can stay part of the background.

## Consistency
- Each object has one canonical position stored in data; the map, sector, and room views all read from it.
- Keep a style guide (style slider value, palette, line weight, lighting) and reuse the same prompt preamble for every image.

## Save tokens with tooling
- Store content in data files and generate pages from templates rather than hand-writing each room.
- Write small scripts for: validating data (missing fields, duplicates, room size limits, placement rules), checking text fits signs (measure text against sign boxes), checking links (every room reachable and links back), and building the site.
- Batch-generate items from the data file and only hand-review the flagged ones.

## Site features (typical)
World map, sector views, rooms, detail cards, a beginner/start area, an about page, quiz mode, full screen mode, and keyboard navigation.

## Site UI rules (lessons from user review)
- The core test: a user can wander the whole place immersively in fullscreen, learning items in their locations so the place itself aids memory, with real visual variety from space to space. Keep the UI simple, and don't add gadget features (collections, mini-maps) the user didn't ask for.
- The look should be whimsical and storybook-like, not stuffy or formal. Use soft natural UI colours, never orange or amber chrome.
- The painting is the whole experience. Fullscreen must really fill the screen with the image (Fullscreen API) and everything must stay usable there.
- Don't use a side panel, and put no text below the image. Item details and any other info open as centred dialogs over the picture (close with X, Esc, or the backdrop).
- Add a toggle (also a key, e.g. H) that highlights all clickable areas, plus a hover effect and a pointing-hand cursor on every clickable area. Users can't otherwise tell what's clickable.
- Make every door, arch, stair and path visibly enterable even with highlights off: a small always-visible badge showing the walking direction, plus a hover glow and the destination name. Keep this cue distinct from the zoom icon.
- Mark every zoom-in spot with a small always-visible icon (e.g. a magnifying-glass badge) so learners know it opens a closer look at another little area.
- Every space has a back control to the space above it (room to building, building to sector, sector to village), so no view is a dead end.
- Navigation is walking: click painted paths, doors, stairs, and arches, shown with subtle on-image arrows. Never make users pick the next space from a list or signpost menu.
- Rooms in the same building connect directly (stairs or doors painted in the room). Never force a trip outside to get between them.
- Label every building with its name (a painted sign with overlay text, plus a hover name on its door).
- Keep the top bar minimal: no current-place name and no topic sections such as prayers. Those live inside the world.
- Keep cards lean: no level badge and no placement notes (e.g. "left side"), because the scene already shows that. Show every option rather than hiding some behind a "more" button (e.g. all tense tabs on a verb card).
- Keep control buttons in a slim strip outside the painting, never on top of it.
- Include a site guide (an overlay opened from the top strip) explaining every placement convention: what sectors, buildings, floors, sides, tiers, plaques, mirrors, signs, and mnemonic characters mean. Keep it out of item cards, and in one editable data file that stays in sync with the skill's rules.
- Drop explanatory "how this memory works" boxes on cards. The mnemonic/hook explanation is enough.
- Audit every hotspot so it lands on the right thing (crop each box and check it). A click that leads to the wrong place breaks trust.

## Side placement in paintings
- A rough left/right split is enough. Use the scene's natural composition; a centre pillar or other hard divider is optional, not required.

## Bulk hook writing (lessons from testing)
- Rate every hook honestly (strong/ok/weak/plain) and re-check the weak ones before calling the set done. A hook is weak when the scene only pictures the meaning with no sound link, when the sound link is said by a character instead of shown, or when the sound-alike is not close to how the word is actually said.
- Parallelize big hook batches by slice (level or sector). Helpers write only to their own folder of batch files and mark finished files (e.g. .done.tsv). Exactly one worker merges into the master data file, so nothing gets overwritten.
- Keep a FORMAT note for batch files and a stats script. Progress counts should include written-but-unmerged batches.
- Merge scripts: never let a later line silently undo an earlier correction (e.g. a gloss fix). Fallback templates must not add theme text, like a "sacred setting", to items outside that theme.
- Don't leave a catch-all sector for abstract items. Give every room a concrete, drawable setting whose theme the items really fit, such as a courthouse, a fairground, or a clock tower, and flag low-fit items for review. When a room is short, leave it smaller rather than topping it up with items that don't belong.

## Copyright check (before every public release)
Audit everything that ships: quoted texts (prayers, poems, liturgical translations; prefer public-domain versions and check modern official translations), definitions and glosses (dictionary sources such as Wiktionary are CC BY-SA, so either attribute and share-alike or rewrite in your own words), word lists and level data (check whether redistribution is allowed), fonts (ship OFL licence files), and third-party code. Keep a COPYRIGHT_AUDIT file and a shipped CREDITS page.
Lessons from the first audit:
- Modern official liturgical translations are often copyrighted and need permission (e.g. AELF in French, ICEL in English). Use dated public-domain editions (e.g. 19th or early 20th century catechisms and prayer books on Wikisource), record each text's edition and URL in its data, and translate from the original yourself when no PD version exists.
- Watch for licence clashes: a non-commercial (NC) dataset can't be mixed into share-alike (SA) public data. Keep NC values out of the shipped files and use them only internally, with credit.
- Rewrite copied dictionary glosses in your own words sector by sector as each sector ships (it also improves quality), in a separate original-gloss file that takes precedence in the merge.
- Credit AI image tools and disclose AI generation where their terms ask for it.
- The public repo needs a LICENSE for the code and a data licence file that matches its share-alike sources.

## Validation (what any validator bot must do)
A validator is a separate reviewer bot or pass that checks a sector or release before it ships. It did not build the work, so it judges against the rules in this skill and the user's recorded feedback, not against the builder's notes.

**How to run**
0. Walk the live site as a learner before anything else: in a normal window and in fullscreen, click into every place and back out, and open and read every card in full. Mechanical checks passing never means the release is ready.
1. Validate one sector or room set at a time, and run the whole checklist every time, not only the parts that changed.
2. Use tooling for the mechanical checks (schema, overlap, links, counts). Look at every painting yourself for the visual checks. Open the live or preview site, not only the data files.
3. Record every finding in a VALIDATION report with: location (room, item or file), the rule broken, severity (blocker, major, minor), evidence (screenshot crop, line or value), and the suggested fix.
4. Blockers stop the release: safety or content problems, copyright problems, broken navigation, wrong links, or a schema or validator error. Majors should be fixed before release. Minors can be listed for later.
5. Don't fix things silently. Report them, or fix them and log each change in the report. Re-run the full checklist after fixes.
6. Never invent facts. If a check can't be done (missing source, no access), mark it "not checked" with the reason.

**Whole-palace structure (check every release, not only the changed sector)**
- **Maps agree at every level.** The overall village or palace map, each sector map and each building or floor plan describe the same layout. A building appears in the sector the village map puts it in, in the same position and with the same name and entrances. Rooms listed in a building's plan are the rooms you can actually walk into from that building, and the painted views match the maps (a door on the map is a door in the painting, and on the same side).
- **No disconnected areas.** Build the full navigation graph across the whole palace (village, sector, street, building, room, zoom spot) and confirm every place can be reached from the start and can get back to it. Report any orphan room, dead end with no way back, one-way link without a return, or sector reachable only through a hidden or unlabelled hotspot.
- **Consistent hierarchy.** Every room belongs to exactly one building, every building to exactly one sector, and every sector appears on the village map. IDs and names are unique and spelled the same in the data, maps, paintings, signs and site text, in every interface language.
- **Consistent conventions.** Placement scheme, sign style, direction cues and transitions (doors, stairs, paths) work the same way in every sector, so a learner who knows one area can read any other. Flag sectors that drift from the shared conventions.
- **Balanced load.** No sector, building or room is overloaded or nearly empty compared with the density rules, and no two places are so alike that they'd blur together in memory.

**Data and pipeline**
- The pipeline validator passes with 0 errors. Every item has its required fields, and no pending or placeholder values (TODO, lorem, empty hooks) remain.
- Counts match: every item in the source list is placed exactly once, with no duplicates or orphans.
- Every hotspot target exists. Every room is reachable from the start and can get back, and every space has a visible way back to its parent (a back control driven by the hierarchy, not only painted links).

**Content and safety**
- Everything is age-appropriate. No crude terms or profanity, and no crude mnemonics. Mature items appear as text plaques only, never as drawings.
- No depiction of God the Father and nothing likely to cause religious or cultural offense. Vulgar or insulting senses carry a gentle usage warning.
- Facts, definitions and examples are correct. Spot-check at least 10% of items, plus every item flagged weak.
- Every item belongs where it is placed. For each room, read its theme and check every item against it in the item's main or most useful sense, the way a teacher would, never by string or embedding similarity alone. Typical misses: an item placed by a rare sense (a caretaker's lodge in a restaurant), a near-synonym used where the everyday word is different (an invoice word for a restaurant bill when the restaurant word sits elsewhere), and filler topped up into a short room. Every misfit is a major. Also check the reverse: the words a learner most needs in that setting are actually in it.

**Mnemonics**
- No template or filler wording reaches a card (e.g. 'Picture the plain object', 'label glowing'). Count repeated phrases across all hooks: any sentence that appears on more than a handful of items is a template and must be rewritten, whatever strength rating it was given.
- Each hook's sound link and image actually match the item. The image is concrete, visible in the painting, and shows the action.
- Every whimsical figure or prop stands for an item, and no hook relies on an offensive stereotype.
- The hook text describes what is actually painted: the same figure (gender and pronouns, age, kind of character or creature), the same action and the same key props. Crop each box and compare. Whenever a painting is redone, update the hook to match the new art.

**Paintings**
- Natural true colour, with no tint or colour cast (check especially for orange or golden drift). Sectors differ by setting and materials, not by colour grade.
- Placement means what the project says it means. Read the project's placement scheme (its site guide or placement notes, e.g. which side, height, floor, plaque or mirror stands for what). Then check each object in each painting, zoom spots included, against the meaning its spot is supposed to carry, and flag any object whose position contradicts the scheme.
- Each label sits on or just under its own figure, clearly closer to it than to any neighbour, with a visible gap between items. Script-check that every label's centre lies inside its own box and nearer to it than to any other.
- Nothing in an item's box that isn't in its hook. No stray animals or props: every element is either the sound cue or the meaning.
- Exactly one clickable box per item, covering the item and its mnemonic helper. Hotspot overlap is 0, and signs never cover items.
- Figures are varied and unique, with no repeated poses or characters. Buildings carry whimsy tied to their items.
- Sign and building-name text is readable at normal size, and side-split signs are clearly split.
- Signage never looks like an item. Direction and section signs use one signage-only style, sit at the edges or overhead away from item boxes, and are never placed like a figure's prop. Note busy paintings as a minor finding, but don't repaint just for busyness.
- Check every painting's colour against the approved reference before release. Generators drift toward an orange, sepia or amber cast, especially in warm interiors, so grade back to neutral daylight (off-white walls, varied clothing) and flag any drift. Never place children next to alcohol or tobacco props, and nobody drinks or smokes.
- Every figure belongs to one coherent scene. People and animals stand on the floor, sit, or work at a real surface, at a consistent scale and perspective with contact shadows. They are never stacked in rows behind counters, perched on shelves, or floating like stickers. If a space can't hold its words naturally, split it or add a zoom instead of crowding. The learner walk-through flags any figure that looks pasted on.
- Every item is fully in frame. No item, figure or key prop may be cropped by the image edge or hidden under the UI strips. Keep item boxes at least ~6% in from each edge. The viewer must never crop the painting to fill the screen (use contain-fit with a blurred or parchment surround, and put strips outside the image rect). The release check verifies every item and exit box is inside the visible viewport at several screen sizes. The fix for an edge item is to repaint or recompose, not to shrink the box.
- One label per thing. When a door, path or place has a sign naming it, hovering lights up that sign (glow, slight lift, pointer cursor) instead of showing a second tooltip with the same words. A hover name pill appears only for exits with no sign. Sign text is rendered to look painted on the board (fitted serif or engraved lettering, no panel over the board), and the direction badges are icons only.
- Scenery is balanced: natural, but with little non-item clutter.

**Navigation and UI**
- Click every hotspot, link, exit, door and stair, and confirm each lands on the right target.
- Navigation click areas cover the whole painted passage (the stretch of road ahead, the full doorway or arch), not just its text label, without overlapping item boxes.
- Links are physically plausible. You leave a room through doors, stairs or arches, never through windows or walls. Upper floors connect only by stairs, and only ground-floor doors lead outside. Windows can show a view but are never exits.
- Every painted transition matches where it really leads. Stairs drawn going up must lead to a higher floor, and stairs going down to a lower one (an upstairs room shows stairs going down). Cellar steps lead down, and doors and paths face the side the map puts their target on. Arrows and labels must say the same.
- Navigation is a natural step-by-step walk, with no list pickers. Rooms in the same building connect directly, and building names are shown.
- Press every strip button and open every dialog in BOTH windowed and fullscreen modes. Overlays must render inside the fullscreen element. Button labels are plain and self-explanatory (e.g. 'Exit fullscreen', not 'Leave').
- True fullscreen works, with centred card dialogs and no side panel or text below the image. Control buttons sit outside the painting. The highlight toggle works.
- Cards follow the approved mock-up: lean fields and every required field present.
- **Text formatting and layout.** Put screenshots of each kind of dialog or card (e.g. noun, verb, place, guide, dialogue, credits) next to the approved mock-up and compare them. Check: generous inner padding so no text touches or crowds an edge; comfortable line height and clear spacing between sections; a clear type hierarchy (headword largest, then meaning, then details); consistent alignment and fonts matching the mock-up; and no overflow, clipping, awkward wrapping or orphaned single words, using the longest word, gloss, example and dialogue in the data. Repeat at desktop, small laptop and narrow mobile widths, and in every interface language (translations run longer). Also check that on-image labels and signs are readable against their background. Any visible drift from the approved mock-up is a major.
- The language toggle switches all UI and meta text and leaves the item content alone. The site guide matches what the site actually does.
- The site works on desktop and on a narrow mobile width, and the browser console shows no errors.

**Copyright**
- Run the copyright check above. Every shipped text, dataset, font, image and piece of code has a known licence, and the credits page lists every attribution needed.

**Report back**
Give a verdict (ship, ship after fixes, or do not ship), counts by severity, the full findings list, and what was checked versus not checked.

## When something new comes up
Read user feedback for its spirit. When they describe an experience ("walk through it, pick up words"), improve that experience; don't turn each phrase into a literal new feature.
If a snag or a new user idea would help future palaces, fold it back into this skill (or the subject-specific one).

## Painting checks (lessons from user review)
- Every whimsical figure or creature must stand for a specific item in that space. No decorative whimsy, and cognates get no creature.
- Signs and plaques must never cover or overlap an item or its mnemonic. Check text boxes against every hotspot box.
- Give each item exactly one clickable box, covering the item and its mnemonic helper together. Compose them side by side so a single tight box works, and never add a second mnemonic box.
- Keep hotspot boxes from overlapping: spread items into separate zones when you compose the scene, draw tight boxes, never put one item's box fully inside another's, and compute pairwise overlap before calling a space done.
- Make sure the mnemonic action is actually visible, not just implied (e.g. "fracture" needs a bandaged jaw, not just a surprised face).
- Make every figure unique: vary characters (ages, professions, animals, fantasy figures that fit the hook), poses, scale, and actions. A row of the same person in the same pose (e.g. chef after chef at a counter) is unmemorable and must be repainted.
- Buildings need whimsy too. Plain realistic houses are forgettable, so give each building a memorable, playful shape or feature tied to what it holds (a house shaped like a pot, a crooked tower, a door like a giant loaf), while the scene still reads as a natural place.
- Balance natural against efficient. Every non-item element is wasted space, so add only enough setting to make the place believable and fill the rest with items.
- Props are hooks too. Don't add decorative ornaments, like a teapot or cheese on a rooftop, that don't stand for an item.
- Zoomed-in sub-spaces follow the same placement rules (e.g. gender sides) as their parent room.
- Sign text must be easy to read: large, high-contrast, on a light flat plate, consistently placed per side.

## Distinct palettes per sector
- Make sectors distinct through setting, materials, architecture, and time of day, NOT colour grading. Image models drift toward a golden/orange "cozy" cast, so prompt explicitly for neutral daylight, true colours, and white whites, and reject warm-cast images. Avoid orange, terracotta, and peach walls in interiors. Post-hoc colour correction only softens a cast, so repaint when a scene still reads orange. Every scene uses natural true colours and clear lighting with no overall tint or filter, so items stay easy to see. Keep the realism level constant across sectors.
- A "no gender tint" rule bans an overall pink or blue wash, not natural blue sky, water, or blossoms. Don't let painters strip every blue.
