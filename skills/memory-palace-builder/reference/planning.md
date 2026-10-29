# Planning: hierarchy, assignment, the unbuilt check and the item manifest

Read before planning a sector, a building or a room, and before every paint job (the planning gate).

## Hierarchy

World map, then sectors (districts), then sites (buildings or outdoor spots), then rooms, then zoom spots: desks, tables, shelves, cabinets, or altars modeled as first-class small rooms (type zoom, with a parent room, their own sign and theme, a position in the parent, and about 6 to 12 small items). Users zoom in and back out. They keep parent rooms uncluttered and reduce the number of full rooms; count them separately. Some map areas can open a site directly. Every room links back to its sector, and may link to related rooms. Sectors connect to each other both from the world map and from neighboring sectors. <!-- B22 -->

- **No one-object zooms.** A zoom that shows a single object or word is not a room. Fold thin zooms (well under the ~6-word target, in practice fewer than about 4 words) into a fuller scene: the parent room or a sibling zoom with a real shared spot. precheck.py fails a 1-word zoom and warns under 4. <!-- N6 -->

## Build order (always in this sequence)

1. **Inventory**: list every item to memorize with its metadata (level, category, sub-category). Keep it in a machine-readable data file (JSON/YAML/CSV), not prose. <!-- B25 -->
2. **Assign items to rooms** by theme, once, in the data file. Every later build takes each room's items from this assignment and never re-picks items ad hoc for being unused or easy to draw (see gate G in the release-gates skill). Set density targets per room type and record them (e.g. 8 to 12 or more for rooms of simple items, scaled by object size; 4 to 6 for rooms of complex items that carry lots of attached detail). Split a room or add zoom spots before it gets crowded. <!-- B26 -->
3. **Group rooms into sectors** by common theme or real-life layout (e.g. a house holds kitchen, bedroom, bathroom). <!-- B27 -->
4. **Lay out the world map**: place sectors, connect them, and define a starting point plus mostly-linear suggested paths that still allow free roaming. <!-- B28 -->
5. **Design each room**, then run the room checks below before moving on. <!-- B29 -->
6. **Build navigation, extras, and the site shell** (about page, quiz, audio, full screen). <!-- B30 -->

## Run the unbuilt-by-word-id script first, every time

- **First step of every build or repaint job:** run `tools/unbuilt.py` (fresh main, by word id) and read the target building's partial/unbuilt rooms before choosing what to paint. Never trust a remembered count or a room id alone. <!-- N5 -->
- **"Unbuilt" is checked by word id.** Before building a planned room as new, search every live data file for its word ids. Room ids drift between the plan and the site, so a planned room can already be live under another name. <!-- G156 -->

## Planning gate: write the item manifest, check it, only then paint

- **Manifest before paint.** Before any painting, write an item manifest for the room (`tools/manifest_template.json`): for each word its id and headword, what is shown, its pose or action, exact counts, where and on what each verb acts, the sensitive-word treatment, and the side/zone it occupies; plus the room's doors and exits (where each is painted and where it leads), zooms with their words, and any intended scene text. Check the manifest line by line against the builder, language and gates checklists (placement band and side, theme fit, one concept per object, label budget, adult/child separation, counts), fix it, and only then paint. The prompt is written from the manifest, and precheck.py --manifest checks the finished room against it. <!-- N2 -->
- **Prompt from the template.** Every room or zoom painting prompt (and every repaint or paint-back prompt) is built from `reference/prompt-template.md` with every field filled from the manifest: the named situation, the interacting groups, one line per item, the siblings and motifs already used, doors, scene text. Store the exact text sent as the manifest's `prompt_text`, beside `scene_situation`, `interactions`, `siblings` and `used_motifs`; precheck.py --manifest fails a manifest missing any of them, a prompt missing a template section, an unfilled `{field}`, or an item the prompt never names. The template only prevents rework; every gate still applies strictly to the finished painting. <!-- N9 -->

## Encode meaning in placement, not only in images

Use fixed spatial rules so position itself carries information. Decide them once and apply everywhere, and show a legend on the about page. Examples: <!-- B33 -->

- Left vs right side of the room for a binary category (e.g. grammatical gender). <!-- B34 -->
- Do not tint the scene itself by category (it looked unnatural); if a color cue is wanted, apply it to the item's label or card text instead. <!-- B35 -->
- Height (floor, table, shelf, ceiling) for frequency or level. <!-- B36 -->
- A recurring prop for a property (e.g. a mirror for a reflexive form, a door plaque for associated rules). <!-- B37 -->
- Distinct building types or streets for distinct item classes. <!-- B38 -->
- Everything that belongs to one item stays together in one place (one building, one object). <!-- B39 -->

## Side placement in paintings

- A rough left/right split is enough. Use the scene's natural composition; a center pillar or other hard divider is optional, not required. <!-- B106 -->

## Place fit

- Don't leave a catch-all sector for abstract items. Give every room a concrete, drawable setting whose theme the items really fit, such as a courthouse, a fairground, or a clock tower, and flag low-fit items for review. When a room is short, leave it smaller rather than topping it up with items that don't belong. <!-- B113 -->
- **Planned assignments are law.** Every space takes its words from the project's planned item-to-room assignment (the inventory's room id and the room list's theme). Never pick words because they are unused or easy to draw. If a planned room has no space yet, build that space; don't borrow its words. Words that leave a space go to a reserve file tagged with their planned room. (Once a parish hall got an umbrella, a coat and knitting words, and the plan already had a home for each of them.) <!-- G92 -->
- **Every word suits the place.** A teacher reading the room's name would expect each item there. Furniture that isn't needed (a random table) is never a reason to hold unrelated items. <!-- G93 -->
- **A close-up is a real spot where its objects belong:** a coat peg, a knitting basket, an easel, a vestment cupboard. It's never a generic table. <!-- G94 -->
- **A close-up looks like the same place as its parent:** the same piece of furniture, walls, light and style, just closer. The object it zooms into is visible in the parent painting, and its hotspot opens the zoom. (Once a desk zoom looked like a desk in a different building, and a classroom had no desk until you zoomed in.) <!-- G95 -->
- Placement by meaning, senses, homonyms and no-overflow rooms (language palaces): see the language skill, reference/placement-and-senses.md.
