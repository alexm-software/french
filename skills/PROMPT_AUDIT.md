# Prompt vs gate audit (v13.1)

Every rule in the three memory-palace skills (the 357 v12 rule lines, IDs as in COVERAGE.md, plus the v13/v13.1 new rules N1–N10), checked against the painting prompt.
Class: **a** = fully preventable at generation, so it must be in the prompt; **b** = data, geometry, overlay, tooling, process or deploy only; **c** = partly both (the prompt prevents it, a tool or post-paint check still verifies it).
Section = where in `PROMPT_TEMPLATE.md` (builder reference/prompt-template.md) it is covered. "In prompt before" = whether the pre-template prompts (MKTA PROMPTS.md style: preamble, style, daylight, no lettering) explicitly required it.
The template is prevention only: every gate still applies, strictly, to the finished painting. The only gate relaxed is G27 (natural background figures allowed).

## Summary
- v12 rules: 357: class a 87, class b 187, class c 83.
- New rules N1–N10: a 4 (N6, N8, N9, N10), b 4 (N3, N4, N5, N7), c 2 (N1, N2).
- Prompt-relevant rules (a + c): 170 v12 + 6 new; all are now in the template.
- Already explicit in the prompt before: 7 (B14 style slider, B76 shared preamble, B161/G42 neutral daylight, G99 sprite slot spec, B71 room as style reference, B235 text on small props; earlier prompts also said 'no lettering').
- Missing from the prompt before: 163 v12 rules + N6, N8, N9, N10 (every a/c row marked NO below). Most consequential: no named situation or interaction groups, nothing against lineups/grids/even spacing/everyone facing the viewer (G39, G98, G128, B170, N8: the ecole basse_cour/preau/bibliotheque/fete problem); placement sides/bands and 6% edge margins (B33, L-placement rules, G39); exact counts and the verb marker (L-verbs, G-number rooms); grounding/anatomy/no strays (G24–G27); doors and exits; content/sensitivity; distinct rooms and repeated motifs (G129, N10).

- Template-only extras (prevention, no gate of their own): no weapons, no potty humour, no mime look on non-verbs, figures face varied directions; they tighten existing gates (B63 all ages, L-verb marker, N8).
- Method: classes assigned rule by rule; the section column is keyword-assisted with hand overrides for the composition, figure and grounding rules, so read it as "where to look", not an exhaustive list.

## By template section (a + c rows; a rule can count in several)
- ITEMS: 87
- PLACEMENT AND SPACING: 53
- SETTING: 36
- TEXT: 35
- COMPOSITION: 33
- LIGHT AND COLOUR: 26
- STYLE: 26
- FIGURES: 26
- CONTENT: 23
- DOORS AND EXITS: 21
- GROUNDING AND ANATOMY: 15
- VARIETY: 9
- SITUATION: 2
- AVOID: 2
- IMAGE: 1

## Table

| id | summary | class | where the template covers it | in prompt before |
|---|---|---|---|---|
| B9 | A generic recipe for building an explorable memory palace (a world of places where each fact is pinned to a v… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B12 | Subject and scope: what body of knowledge, and its levels (e.g. beginner to expert). | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B13 | Setting: the overall world (village, castle, ship, campus). Prefer an idyllic, real-life-plausible place so l… | a | LIGHT AND COLOUR, SETTING | NO |
| B14 | Style slider from 1 (very cartoonish) to 5 (realistic). Record the chosen value and use it in every image pro… | a | STYLE, SETTING | yes |
| B15 | Art style (ask, don't assume): before painting anything, ask what art style the person wants. Cover the mediu… | c | LIGHT AND COLOUR, FIGURES, COMPOSITION — plus post-paint check | NO |
| B16 | Site look (ask, and mock it up): ask what feel they want for the website itself (e.g. whimsical storybook vs … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B17 | Sacred and cultural respect: religious content is depicted reverently. Never mock sacred figures, objects, or… | a | CONTENT, TEXT, ITEMS | NO |
| B18 | Audience: default to all ages. No crude terms, profanity, or crude mnemonics. Mature-but-necessary items are … | a | CONTENT, TEXT, ITEMS | NO |
| B19 | Output: static site (e.g. GitHub Pages), print, or images only. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B22 | World map, then sectors (districts), then sites (buildings or outdoor spots), then rooms, then zoom spots: de… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B25 | Inventory: list every item to memorize with its metadata (level, category, sub-category). Keep it in a machin… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B26 | Assign items to rooms by theme, once, in the data file. Every later build takes each room's items from this a… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B27 | Group rooms into sectors by common theme or real-life layout (e.g. a house holds kitchen, bedroom, bathroom). | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B28 | Lay out the world map: place sectors, connect them, and define a starting point plus mostly-linear suggested … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B29 | Design each room, then run the room checks below before moving on. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B30 | Build navigation, extras, and the site shell (about page, quiz, audio, full screen). | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B33 | Use fixed spatial rules so position itself carries information. Decide them once and apply everywhere, and sh… | c | PLACEMENT AND SPACING — plus post-paint check | NO |
| B34 | Left vs right side of the room for a binary category (e.g. grammatical gender). | a | PLACEMENT AND SPACING, SETTING | NO |
| B35 | Do not tint the scene itself by category (it looked unnatural); if a color cue is wanted, apply it to the ite… | a | TEXT, LIGHT AND COLOUR, ITEMS | NO |
| B36 | Height (floor, table, shelf, ceiling) for frequency or level. | c | PLACEMENT AND SPACING, COMPOSITION, SETTING — plus post-paint check | NO |
| B37 | A recurring prop for a property (e.g. a mirror for a reflexive form, a door plaque for associated rules). | a | TEXT, DOORS AND EXITS | NO |
| B38 | Distinct building types or streets for distinct item classes. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B39 | Everything that belongs to one item stays together in one place (one building, one object). | a | ITEMS, SETTING | NO |
| B42 | Each item is a zany, whimsical object, character, or creature that both sounds like the item (when said aloud… | a | ITEMS (hook object LARGE, sound-alike AND meaning) | NO |
| B43 | Props that carry the sound cue must be large, prominent, and unambiguous. | a | ITEMS | NO |
| B44 | A helper character that carries the sound cue must sit right next to (visibly interacting with or pointing at… | a | PLACEMENT AND SPACING, ITEMS, FIGURES | NO |
| B45 | Store the mnemonic hook in the item metadata (sound-alike, one-line scene, strength, fallback) and always exp… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B46 | Never drop an item because a good or respectful mnemonic is hard. Fallback: depict the item itself clearly an… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B47 | Keep one clear concept per object; avoid scenes where the prop could be read as an ordinary furnishing. | a | ITEMS, COMPOSITION | NO |
| B48 | Vary designs so rooms, buildings, and sectors never start to look the same: change shapes, palettes, eras, an… | a | VARIETY, LIGHT AND COLOUR, DOORS AND EXITS | NO |
| B51 | A sign naming the room's theme. | c | SETTING — plus post-paint check | NO |
| B52 | Clickable items opening a detail card with the full information. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B53 | A link back to the sector, and links to related rooms where they make sense. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B54 | Optional extras: scenes or dialogues, audio, quiz entries. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B57 | Nothing important is conveyed only by hidden or tiny text; every item is visible as an image (except mature i… | a | CONTENT, TEXT, ITEMS | NO |
| B58 | All sign and label text fits inside its sign at all supported screen sizes. Render text as real HTML/SVG text… | c | CONTENT, TEXT, PLACEMENT AND SPACING — plus post-paint check | NO |
| B59 | No copyright problems: write your own definitions and explanations, or use openly licensed sources with the r… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B60 | Every mnemonic actually works: say the sound-alike aloud, confirm it resembles the target, and confirm the pi… | c | ITEMS — plus post-paint check | NO |
| B61 | Placement rules are obeyed (correct side, tint, prop) and positions match between the world map, sector view,… | c | LIGHT AND COLOUR, PLACEMENT AND SPACING, SETTING — plus post-paint check | NO |
| B62 | Room density is within the target range; overflow goes to a new room or zoom spot. | c | COMPOSITION, SETTING — plus post-paint check | NO |
| B63 | Age-appropriate content only. | a | CONTENT (all ages) | NO |
| B64 | Religious and cultural imagery is reverent and follows the sensitivities recorded for the project. | a | CONTENT | NO |
| B67 | Choose between generated illustrations (richer, harder to keep consistent and edit) and hand-coded SVG (each … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B70 | Current preferred method (user review, Oct 23): keep the painted empty room as the fixed scene, then draw eac… | c | ITEMS, FIGURES, COMPOSITION — plus post-paint check | NO |
| B71 | Lessons from testing: flat vector SVG looked noticeably uglier than painted art, and painted cutouts composit… | c | LIGHT AND COLOUR, ITEMS, COMPOSITION — plus post-paint check | yes |
| B72 | Alternative: keep each item as its own asset (one file per object) and each room as an empty background plus … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B75 | Each object has one canonical position stored in data; the map, sector, and room views all read from it. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B76 | Keep a style guide (style slider value, palette, line weight, lighting) and reuse the same prompt preamble fo… | a | LIGHT AND COLOUR, STYLE | yes |
| B79 | Store content in data files and generate pages from templates rather than hand-writing each room. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B80 | Write small scripts for: validating data (missing fields, duplicates, room size limits, placement rules), che… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B81 | Batch-generate items from the data file and only hand-review the flagged ones. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B84 | World map, sector views, rooms, detail cards, a beginner/start area, an about page, quiz mode, full screen mo… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B87 | The core test: a user can wander the whole place immersively in fullscreen, learning items in their locations… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B88 | The look should be whimsical and storybook-like, not stuffy or formal. Use soft natural UI colours, never ora… | c | LIGHT AND COLOUR, FIGURES — plus post-paint check | NO |
| B89 | The painting is the whole experience. Fullscreen must really fill the screen with the image (Fullscreen API) … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B90 | Don't use a side panel, and put no text below the image. Item details and any other info open as centred dial… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B91 | Add a toggle (also a key, e.g. H) that highlights all clickable areas, plus a hover effect and a pointing-han… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B92 | Make every door, arch, stair and path visibly enterable even with highlights off: a small always-visible badg… | c | VARIETY, DOORS AND EXITS, COMPOSITION — plus post-paint check | NO |
| B93 | Mark every zoom-in spot with a small always-visible icon (e.g. a magnifying-glass badge) so learners know it … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B94 | Every space has a back control to the space above it (room to building, building to sector, sector to village… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B95 | Navigation is walking: click painted paths, doors, stairs, and arches, shown with subtle on-image arrows. Nev… | c | DOORS AND EXITS, COMPOSITION, STYLE — plus post-paint check | NO |
| B96 | Rooms in the same building connect directly (stairs or doors painted in the room). Never force a trip outside… | c | DOORS AND EXITS, PLACEMENT AND SPACING, STYLE — plus post-paint check | NO |
| B97 | Label every building with its name (a painted sign with overlay text, plus a hover name on its door). | c | TEXT, DOORS AND EXITS, STYLE — plus post-paint check | NO |
| B98 | Keep the top bar minimal: no current-place name and no topic sections such as prayers. Those live inside the … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B99 | Keep cards lean: no level badge and no placement notes (e.g. "left side"), because the scene already shows th… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B100 | Keep control buttons in a slim strip outside the painting, never on top of it. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B101 | Include a site guide (an overlay opened from the top strip) explaining every placement convention: what secto… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B102 | Drop explanatory "how this memory works" boxes on cards. The mnemonic/hook explanation is enough. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B103 | Audit every hotspot so it lands on the right thing (crop each box and check it). A click that leads to the wr… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B106 | A rough left/right split is enough. Use the scene's natural composition; a centre pillar or other hard divide… | a | PLACEMENT AND SPACING, COMPOSITION | NO |
| B109 | Rate every hook honestly (strong/ok/weak/plain) and re-check the weak ones before calling the set done. A hoo… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B110 | Parallelize big hook batches by slice (level or sector). Helpers write only to their own folder of batch file… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B111 | Keep a FORMAT note for batch files and a stats script. Progress counts should include written-but-unmerged ba… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B112 | Merge scripts: never let a later line silently undo an earlier correction (e.g. a gloss fix). Fallback templa… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B113 | Don't leave a catch-all sector for abstract items. Give every room a concrete, drawable setting whose theme t… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B116 | Audit everything that ships: quoted texts (prayers, poems, liturgical translations; prefer public-domain vers… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B117 | Lessons from the first audit: | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B118 | Modern official liturgical translations are often copyrighted and need permission (e.g. AELF in French, ICEL … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B119 | Watch for licence clashes: a non-commercial (NC) dataset can't be mixed into share-alike (SA) public data. Ke… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B120 | Rewrite copied dictionary glosses in your own words sector by sector as each sector ships (it also improves q… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B121 | Credit AI image tools and disclose AI generation where their terms ask for it. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B122 | The public repo needs a LICENSE for the code and a data licence file that matches its share-alike sources. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B125 | A validator is a separate reviewer bot or pass that checks a sector or release before it ships. It did not bu… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B128 | Walk the live site as a learner before anything else: in a normal window and in fullscreen, click into every … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B129 | Validate one sector or room set at a time, and run the whole checklist every time, not only the parts that ch… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B130 | Use tooling for the mechanical checks (schema, overlap, links, counts). Look at every painting yourself for t… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B131 | Record every finding in a VALIDATION report with: location (room, item or file), the rule broken, severity (b… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B132 | Blockers stop the release: safety or content problems, copyright problems, broken navigation, wrong links, or… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B133 | Don't fix things silently. Report them, or fix them and log each change in the report. Re-run the full checkl… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B134 | Never invent facts. If a check can't be done (missing source, no access), mark it "not checked" with the reas… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B137 | Maps agree at every level. The overall village or palace map, each sector map and each building or floor plan… | c | STYLE (sector look) / IMAGE zoom line; map paintings outside template scope — plus post-paint check | NO |
| B138 | No disconnected areas. Build the full navigation graph across the whole palace (village, sector, street, buil… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B139 | Consistent hierarchy. Every room belongs to exactly one building, every building to exactly one sector, and e… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B140 | Consistent conventions. Placement scheme, sign style, direction cues and transitions (doors, stairs, paths) w… | c | DOORS AND EXITS, PLACEMENT AND SPACING, STYLE — plus post-paint check | NO |
| B141 | Balanced load. No sector, building or room is overloaded or nearly empty compared with the density rules, and… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B144 | The pipeline validator passes with 0 errors. Every item has its required fields, and no pending or placeholde… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B145 | Counts match: every item in the source list is placed exactly once, with no duplicates or orphans. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B146 | Every hotspot target exists. Every room is reachable from the start and can get back, and every space has a v… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B149 | Everything is age-appropriate. No crude terms or profanity, and no crude mnemonics. Mature items appear as te… | a | CONTENT, TEXT, ITEMS | NO |
| B150 | No depiction of God the Father and nothing likely to cause religious or cultural offense. Vulgar or insulting… | a | CONTENT | NO |
| B151 | Facts, definitions and examples are correct. Spot-check at least 10% of items, plus every item flagged weak. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B152 | Every item belongs where it is placed. For each room, read its theme and check every item against it in the i… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B155 | No template or filler wording reaches a card (e.g. 'Picture the plain object', 'label glowing'). Count repeat… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B156 | Each hook's sound link and image actually match the item. The image is concrete, visible in the painting, and… | c | ITEMS, STYLE — plus post-paint check | NO |
| B157 | Every whimsical figure or prop stands for an item, and no hook relies on an offensive stereotype. | a | CONTENT, ITEMS, FIGURES | NO |
| B158 | The hook text describes what is actually painted: the same figure (gender and pronouns, age, kind of characte… | c | TEXT, ITEMS, FIGURES — plus post-paint check | NO |
| B161 | Natural true colour, with no tint or colour cast (check especially for orange or golden drift). Sectors diffe… | a | LIGHT AND COLOUR, SETTING | yes |
| B162 | Placement means what the project says it means. Read the project's placement scheme (its site guide or placem… | c | TEXT, PLACEMENT AND SPACING, ITEMS — plus post-paint check | NO |
| B163 | Each label sits on or just under its own figure, clearly closer to it than to any neighbour, with a visible g… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B164 | Nothing in an item's box that isn't in its hook. No stray animals or props: every element is either the sound… | a | ITEMS, FIGURES | NO |
| B165 | Exactly one clickable box per item, covering the item and its mnemonic helper. Hotspot overlap is 0, and sign… | c | PLACEMENT AND SPACING, ITEMS — plus post-paint check | NO |
| B166 | Figures are varied and unique, with no repeated poses or characters. Buildings carry whimsy tied to their ite… | a | FIGURES (unique), VARIETY | NO |
| B167 | Sign and building-name text is readable at normal size, and side-split signs are clearly split. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B168 | Signage never looks like an item. Direction and section signs use one signage-only style, sit at the edges or… | c | PLACEMENT AND SPACING, ITEMS, FIGURES — plus post-paint check | NO |
| B169 | Check every painting's colour against the approved reference before release. Generators drift toward an orang… | a | CONTENT, LIGHT AND COLOUR, STYLE | NO |
| B170 | Every figure belongs to one coherent scene. People and animals stand on the floor, sit, or work at a real sur… | a | SITUATION, COMPOSITION, GROUNDING AND ANATOMY | NO |
| B171 | Every item is fully in frame. No item, figure or key prop may be cropped by the image edge or hidden under th… | a | DOORS AND EXITS, GROUNDING AND ANATOMY, PLACEMENT AND SPACING | NO |
| B172 | One label per thing. When a door, path or place has a sign naming it, hovering lights up that sign (glow, sli… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B173 | Scenery is balanced: natural, but with little non-item clutter. | a | ITEMS, COMPOSITION | NO |
| B176 | Click every hotspot, link, exit, door and stair, and confirm each lands on the right target. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B177 | Navigation click areas cover the whole painted passage (the stretch of road ahead, the full doorway or arch),… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B178 | Links are physically plausible. You leave a room through doors, stairs or arches, never through windows or wa… | c | DOORS AND EXITS, GROUNDING AND ANATOMY, PLACEMENT AND SPACING — plus post-paint check | NO |
| B179 | Every painted transition matches where it really leads. Stairs drawn going up must lead to a higher floor, an… | a | DOORS AND EXITS, PLACEMENT AND SPACING, COMPOSITION | NO |
| B180 | Navigation is a natural step-by-step walk, with no list pickers. Rooms in the same building connect directly,… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B181 | Press every strip button and open every dialog in BOTH windowed and fullscreen modes. Overlays must render in… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B182 | True fullscreen works, with centred card dialogs and no side panel or text below the image. Control buttons s… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B183 | Cards follow the approved mock-up: lean fields and every required field present. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B184 | Text formatting and layout. Put screenshots of each kind of dialog or card (e.g. noun, verb, place, guide, di… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B185 | The language toggle switches all UI and meta text and leaves the item content alone. The site guide matches w… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B186 | The site works on desktop and on a narrow mobile width, and the browser console shows no errors. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B189 | Run the copyright check above. Every shipped text, dataset, font, image and piece of code has a known licence… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B192 | Give a verdict (ship, ship after fixes, or do not ship), counts by severity, the full findings list, and what… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B195 | Read user feedback for its spirit. When they describe an experience ("walk through it, pick up words"), impro… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B196 | If a snag or a new user idea would help future palaces, fold it back into this skill (or the subject-specific… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B199 | Every whimsical figure or creature must stand for a specific item in that space. No decorative whimsy, and co… | a | FIGURES (every figure is a word's figure, named helper or plain scenery) | NO |
| B200 | Signs and plaques must never cover or overlap an item or its mnemonic. Check text boxes against every hotspot… | c | TEXT, PLACEMENT AND SPACING, ITEMS — plus post-paint check | NO |
| B201 | Give each item exactly one clickable box, covering the item and its mnemonic helper together. Compose them si… | c | PLACEMENT AND SPACING, ITEMS, FIGURES — plus post-paint check | NO |
| B202 | Keep hotspot boxes from overlapping: spread items into separate zones when you compose the scene, draw tight … | c | PLACEMENT AND SPACING, ITEMS, FIGURES — plus post-paint check | NO |
| B203 | Make sure the mnemonic action is actually visible, not just implied (e.g. "fracture" needs a bandaged jaw, no… | a | PLACEMENT AND SPACING | NO |
| B204 | Make every figure unique: vary characters (ages, professions, animals, fantasy figures that fit the hook), po… | a | VARIETY, ITEMS, FIGURES | NO |
| B205 | Buildings need whimsy too. Plain realistic houses are forgettable, so give each building a memorable, playful… | a | DOORS AND EXITS, FIGURES, COMPOSITION | NO |
| B206 | Balance natural against efficient. Every non-item element is wasted space, so add only enough setting to make… | a | ITEMS, SETTING | NO |
| B207 | Props are hooks too. Don't add decorative ornaments, like a teapot or cheese on a rooftop, that don't stand f… | a | ITEMS, FIGURES | NO |
| B208 | Zoomed-in sub-spaces follow the same placement rules (e.g. gender sides) as their parent room. | a | PLACEMENT AND SPACING, COMPOSITION, SETTING | NO |
| B209 | Sign text must be easy to read: large, high-contrast, on a light flat plate, consistently placed per side. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B212 | Make sectors distinct through setting, materials, architecture, and time of day, NOT colour grading. Image mo… | a | VARIETY, LIGHT AND COLOUR, DOORS AND EXITS | NO |
| B213 | A "no gender tint" rule bans an overall pink or blue wash, not natural blue sky, water, or blossoms. Don't le… | a | LIGHT AND COLOUR, STYLE | NO |
| B217 | Every map level is a zoom of the level above it. A district on the world map shows, in miniature, the same bu… | c | STYLE (sector look) / IMAGE zoom line; map paintings outside template scope — plus post-paint check | NO |
| B220 | Placement check (script + teacher read). Flag any word whose room theme matches its gloss only through a shar… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B221 | Sensitive words go to sensitive-appropriate rooms. Death, crime, violence, illness and similar words never si… | c | CONTENT, TEXT, VARIETY — plus post-paint check | NO |
| B222 | Moving a word = three edits. Remove it from the live room and inpaint its old spot (prompt "edit minimally, r… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B223 | One hook per word, everywhere. A word in two rooms keeps the better pun and only adapts the setting. Script-c… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B224 | Forced puns, to rewrite: the sound is off (wrong vowel); too many pieces (3-4 unrelated chunks; one chunk on … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B225 | Adverbs. For weak -ment adverbs, reuse the adjective's pun plus "-ly" instead of a new scene, unless that pun… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B226 | Units and overlap. Know which files store boxes in px and which in %. A wrong-unit edit silently moves a hots… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B227 | Hand-off discipline. When buildings belong to other workers, send them data and hook patches with repaint not… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B230 | Sparse floor. Never strip a live room below about 6 words, or below its count at base, without painting somet… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B231 | Count plan-only moves. A move that lives only in the data takes the word off the live site until its target r… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B232 | Paint-backs cut both lists. Pick a plan-only word whose meaning fits a sparse room in the same building, or a… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B233 | Compositing. A low-frequency colour correction smears colour when the new content differs a lot from what was… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B234 | Placement bands apply to paint-backs too. Adjectives and adverbs go in the 30–70% centre band, feminine words… | c | PLACEMENT AND SPACING, ITEMS, SETTING — plus post-paint check | NO |
| B235 | Check small props for text. Generated coins, signs and labels often come back with a symbol or letters (e.g. … | a | TEXT | yes |
| B236 | Fix stale alts while you're there. When you paint into a room, re-read its whole alt text and remove figures … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| B237 | Tooling hygiene. Use a new filename for every view crop, because image reads can be cached by path. Build the… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L9 | Layer this on top of the Memory palace builder skill, which covers build order, style slider, room checks, an… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L12 | Cover the target levels (e.g. CEFR A1 to C2). Tag every word with its level so paths and quizzes can filter b… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L13 | Build the inventory from frequency lists and level-based syllabi under open licenses; record sources and attr… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L14 | Level lists are noisy (everyday words can be graded C2). Cross-check level with corpus frequency and boost co… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L15 | Keep the full word list the user asked for, rare words included, but you may defer drawing assets for the rar… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L16 | Organize by level: the core village holds beginner to intermediate words; themed advanced words go on an uppe… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L19 | Each word is drawn as something that, said aloud in the learner's native language, sounds like the target wor… | a | CONTENT, TEXT, ITEMS | NO |
| L22 | The sound-alike must be a real word or phrase in the learner's language that sounds like the target word said… | c | ITEMS, COMPOSITION — plus post-paint check | NO |
| L23 | Examples (French to English) of weak hooks: soif shown as just a thirsty camel, with no sound link; froidemen… | c | ITEMS, STYLE — plus post-paint check | NO |
| L24 | Never use the meaning as the sound-alike. 'cook' for cuisinier or 'cat' for chat (said SHAH) link nothing to … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L25 | Cognates count only when the word both looks AND sounds close (sauce, soupe). Write them plainly ("Same as En… | c | ITEMS, SETTING — plus post-paint check | NO |
| L26 | Cognates still need a playful, memorable twist, ideally one that encodes the target-language pronunciation wh… | c | ITEMS (hook line: playful twist) — plus post-paint check | NO |
| L27 | Never drop a word for lack of a perfect hook; a plain, appealing depiction of the item is fine. | c | ITEMS — plus post-paint check | NO |
| L28 | No template or meta wording on cards ("Picture the plain object", "label glowing"). Every hook is a specific … | c | ITEMS, COMPOSITION, STYLE — plus post-paint check | NO |
| L29 | Before bulk generation, write and get sign-off on a sample room of hooks. After generation, audit by reading … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L30 | Watch automatic glosses for vulgar senses (dictionary data often lists slang first) and replace them with the… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L31 | But do warn the learner: give any word with a vulgar, offensive, or insulting meaning a usage_warning on its … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L34 | Deciding how each kind of item is represented is part of building the palace, not an afterthought. Before any… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L35 | Each word class (nouns, verbs, adjectives, adverbs, function words, phrases): how it is drawn and how a learn… | c | ITEMS, SETTING — plus post-paint check | NO |
| L36 | Each grammatical feature worth remembering (gender, verb group or irregularity, reflexive, plural quirks): wh… | c | CONTENT, LIGHT AND COLOUR, PLACEMENT AND SPACING — plus post-paint check | NO |
| L37 | Items that don't need a mnemonic each (alphabet letters, number lists, article tables, sound rules): one refe… | c | TEXT, ITEMS, STYLE — plus post-paint check | NO |
| L38 | Rare or advanced words: where they live (zooms, upper floors, an advanced area) and whether their pictures ar… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L39 | Sensitive words: as text on a museum wall, never drawn. | a | TEXT, ITEMS, SETTING | NO |
| L40 | Check every device against the others for clashes, put the device's meaning on the word card (for example a b… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L43 | How verbs look is a design decision for each target language and culture. The French build's mime is one exam… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L44 | List what a learner must tell apart in that language: verbs from nouns at a glance, plus the verb features wo… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L45 | Pick one recurring verb marker that's culturally at home in the target country and that nobody else in the wo… | c | CONTENT, PLACEMENT AND SPACING, ITEMS — plus post-paint check | NO |
| L46 | Give each verb feature its own visual channel on that marker (one costume item's colour for the class, a held… | c | CONTENT, LIGHT AND COLOUR, GROUNDING AND ANATOMY — plus post-paint check | NO |
| L47 | The marker acts inside the room's scene with the room's nouns, never bunched with other verbs (see "Verbs liv… | a | CONTENT, PLACEMENT AND SPACING, ITEMS | NO |
| L48 | Show a sample to the user and get sign-off on the marker and its code before bulk painting. Record the choice… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L49 | When a marker doesn't fit at all (for example, a language with few inflected verbs), a simpler cue can carry … | c | ITEMS — plus post-paint check | NO |
| L51 | French reference build: "Monsieur Verbe", a cheerful mime in a striped shirt, suspenders and white gloves wit… | a | TEXT, LIGHT AND COLOUR, ITEMS | NO |
| L54 | Grammatical gender: feminine nouns clearly on the left half of the room, masculine clearly on the right (a mi… | a | TEXT, LIGHT AND COLOUR, PLACEMENT AND SPACING | NO |
| L55 | Verbs sit in the ordinary themed rooms, acted out by the language's chosen verb marker (see "Choosing how ver… | a | PLACEMENT AND SPACING, ITEMS, SETTING | NO |
| L56 | Adjectives, adverbs, opposites, emotions, idioms: place them in themed rooms where they fit, or in their own … | c | ITEMS, SETTING — plus post-paint check | NO |
| L57 | Mature or sensitive words go as text on a museum wall, never drawn. | a | CONTENT, TEXT, ITEMS | NO |
| L60 | Each room's main painting holds about 10 to 12 of its commonest words, well spaced, with the verbs among them… | c | ITEMS, COMPOSITION, SETTING — plus post-paint check | NO |
| L63 | Every word must have at least one natural example sentence with a translation, using the word in its main sen… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L66 | Show tenses as tabs on the word popup. Conjugation tables for at least present, a common past (e.g. passé com… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L69 | Greetings, farewells, polite phrases, the alphabet (on one bulletin board or poster, not a mnemonic per lette… | c | TEXT, ITEMS, SETTING — plus post-paint check | NO |
| L72 | Nature (beach, mountain or ski resort, campsite, farm), university (sciences, math, engineering, computing, h… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L75 | Each room gets one or more short dialogues using its words, playable with browser speech synthesis (one voice… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L76 | Dialogues must be realistic everyday scenes (ordering at a café, booking a table, cooking with a friend, aski… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L77 | Never generate them from a template, and never have characters quiz each other ("Do you know the verb X? It m… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L80 | Every placed item has a label (word with article). Offer a header switch, remembered between visits, between … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L83 | Give all site UI and meta text (guide, place names and descriptions, labels, tooltips, page title) a native/t… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L86 | Image to word, word to image, gender (left or right), verb group (which beret colour), conjugation fill-in, l… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L89 | Gender placement is correct for every noun. | c | PLACEMENT AND SPACING, SETTING — plus post-paint check | NO |
| L90 | Articles, accents, and spelling are correct (validate with a script against the data file). | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L91 | Mnemonic truly connects the native-language sound (or, where flagged, the spelling) to the target meaning. | c | TEXT, ITEMS — plus post-paint check | NO |
| L92 | False cognates are flagged. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L93 | Conjugation tables are complete for every verb in the room, and each verb is acted by the verb character with… | c | LIGHT AND COLOUR, PLACEMENT AND SPACING, ITEMS — plus post-paint check | NO |
| L96 | Separate walk-through verb streets and alleys, with -er verbs on one side and -ir/-re on the other, were trie… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L99 | Run these in addition to the generic Validation section of the Memory palace builder skill. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L100 | Words: spelling, accents and grammatical properties (gender, class, etc. where the language has them) are cor… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L101 | Glosses: they are accurate and cover the common sense first. They are written in our own words or properly cr… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L102 | Example sentences: every word has one, in natural, grammatical target-language text that actually uses the wo… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L103 | Verb cards: every tense tab is present and the conjugations are correct (spot-check irregular verbs fully). T… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L104 | Conversations: they are realistic everyday dialogues, with no template or quiz lines. Each `used_words` entry… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L105 | Mnemonics: the sound link works for a native speaker of the learner's language. Hooks contain no crude or sla… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L106 | Pronunciation: if there is audio or speech synthesis, check that the target-language voice is used. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L107 | Quoted texts: prayers and other quoted texts use the public-domain or licensed wording recorded in the audit.… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L110 | Build each hook from an English sound-alike of the whole word, then paint it literally: talus is a tall loo, … | c | TEXT, ITEMS, COMPOSITION — plus post-paint check | NO |
| L111 | Never lean on another word in the same language (piéger cannot be shown with a piège) or on knowing the targe… | c | ITEMS — plus post-paint check | NO |
| L112 | For abstract or quantity words, show the meaning and the sound together (le grain is a microscope on a tiny g… | a | PLACEMENT AND SPACING, ITEMS | NO |
| L113 | Keep homonyms out of a themed room unless the room fits that sense (tronc the trunk belongs in the forest, tr… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L114 | Verbs: the verb character acts the sound-alike inside a natural scene for the street's setting, with props th… | a | PLACEMENT AND SPACING, ITEMS, FIGURES | NO |
| L117 | Place by meaning, never by a shared English gloss word. Most misfits came from this: berge (river *bank*) in … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L118 | Gloss the sense the room teaches. A forest teaches feuille as *leaf*, not "sheet of paper"; a sky room teache… | c | TEXT, ITEMS, SETTING — plus post-paint check | NO |
| L119 | Grave or sensitive words never sit in light-hearted rooms (no suicide verb on a "Relief Street", no killing i… | c | CONTENT, TEXT, ITEMS — plus post-paint check | NO |
| L120 | No overflow rooms. A leftover "stump", "attic" or "rack" room filled with unrelated abstract nouns can't be p… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L121 | Phrase-only words are taught as their phrase (en avoir marre, ne… guère, clin d'œil, lors de, afin de, au sei… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L122 | One hook per word, everywhere. A word placed in two rooms shares one hook; only the setting adapts. Prefer on… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L123 | What makes a pun forced: the sound is off (wrong vowel), there are too many pieces (one chunk on the stressed… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L124 | Use only English the learner knows. No Latin or word-history hooks, and no obscure English ("chandler"). A Fr… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L125 | A real cognate may stay plain when no natural pun turns up; note any false-friend trap (combustible means *fu… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L126 | Adverbs: where an -ment adverb's own pun is weak, reuse the adjective's pun plus "-ly". | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L127 | A moved word needs its hook and painting redone, because hooks describe the room they're painted in. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L128 | Inner areas match the overview. Every district's sector map, building exteriors and interiors keep the landma… | c | LIGHT AND COLOUR, DOORS AND EXITS, STYLE — plus post-paint check | NO |
| L131 | Most verbs belong in the themed rooms where their action naturally happens, spread across the scene among the… | a | DOORS AND EXITS, ITEMS, COMPOSITION | NO |
| L132 | Avoid pushing verbs aside: don't bunch a room's verbs into one corner or line them along an edge, and don't p… | a | PLACEMENT AND SPACING, ITEMS, SETTING | NO |
| L133 | This is a balance, not an absolute. A verb street or a cluster of related actions is fine where it genuinely … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| L134 | When repainting a building, bring the verbs from its sector's verb street that fit its rooms into those rooms… | c | PLACEMENT AND SPACING, ITEMS, COMPOSITION — plus post-paint check | NO |
| G10 | These gates come from issues users found room after room. A space is NOT done until every gate passes, and th… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G12 | Tools. The automatable gates are scripted where the project has them, e.g. `scripts/qa/release_gates.py` for … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G15 | Budget room for labels. Estimate each label's rendered width (about 0.5 x font size per character, article in… | c | PLACEMENT AND SPACING, ITEMS, FIGURES — plus post-paint check | NO |
| G16 | Rooms that hold adult items (alcohol, tobacco) contain adults and animals only. Children go elsewhere. | a | CONTENT (no child in an alcohol/tobacco room) | NO |
| G17 | Any prop that gets operated (a button, lever or tap) is mounted on a machine or panel, with its figure touchi… | a | GROUNDING AND ANATOMY (operated props mounted and touched) | NO |
| G18 | Hooks never carry meta prefixes ("Twist on a cognate:", "Like English", "False friend:"). Cognate and false-f… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G19 | Hooks never open with a placement phrase ("On the balcony", "At the upper window", "On the roof"). The item's… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G20 | Before repainting a space, read its open rows in the repaint queue; each one must be fixed by the repaint. | c | COMPOSITION — plus post-paint check | NO |
| G23 | Crop each item box AND each exit box out of the final painting, at least 256 px on the long side. Lay them ou… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G24 | Hook match. The figure shows exactly what the hook scene says: the same character, gender, action, props and … | a | ITEMS (hook object, shown, same character and gender) | NO |
| G25 | Anatomy. Count arms, hands, legs and fingers on every figure. Watch for merged hands, missing limbs, extra li… | a | GROUNDING AND ANATOMY, ITEMS, FIGURES | NO |
| G26 | Clean rendering. Nothing garbled, smeared, half-formed or mashed together. Regenerate rather than accept a ba… | a | GROUNDING AND ANATOMY | NO |
| G27 | Grounded props, no strays. Every prop is held by someone, mounted on something or resting on a surface. No fl… | a | GROUNDING AND ANATOMY, FIGURES (scenery vs stray), AVOID | NO |
| G28 | Hook strength. The sound-alike comes from the real pronunciation (read the respelling aloud). It is an Englis… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G29 | Content, in the art AND the hook text. Adult items (alcohol, tobacco) appear only as objects, such as closed … | a | CONTENT, TEXT, PLACEMENT AND SPACING | NO |
| G32 | Rendered label rectangles. Compute every label's on-screen rectangle by the exact render path: the label text… | c | TEXT, PLACEMENT AND SPACING, ITEMS — plus post-paint check | NO |
| G33 | One control per destination. Count every on-screen navigation element per destination: strip Back, strip sect… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G34 | Exits look like their destination and name it. A kitchen door looks like a restaurant kitchen door (swinging,… | c | TEXT, VARIETY, DOORS AND EXITS — plus post-paint check | NO |
| G35 | Way out, sector button and plan. Every space has a painted way back out plus the always-visible way up to its… | c | DOORS AND EXITS, GROUNDING AND ANATOMY, PLACEMENT AND SPACING — plus post-paint check | NO |
| G38 | A rich, real-feeling setting with its own wall colour, floor, depth and one big nameable landmark. Never a pl… | a | SETTING (walls, floor, depth, landmark) | NO |
| G39 | At most about 10 items (11-12 is a warning, more than 12 fails, zoom spots counted separately), well separate… | c | COMPOSITION (no rows), ITEMS (N 10 or fewer), PLACEMENT AND SPACING — plus post-paint check | NO |
| G40 | No look-alikes. Compare every pair of spaces in the same building or street with an image-similarity measure … | c | VARIETY, LIGHT AND COLOUR, PLACEMENT AND SPACING — plus post-paint check | NO |
| G41 | One style per building or street, matching its exterior in every view. | a | STYLE (matches exterior) | NO |
| G42 | Colour. Natural, neutral daylight. Compare each painting with the approved palette sheet; an amber, sepia or … | a | LIGHT AND COLOUR, SETTING | yes |
| G45 | Before painting, write the item layout with label room in mind. | c | ITEMS, SETTING — plus post-paint check | NO |
| G46 | After painting, run A to D, fix and re-run. Ship only on a full pass. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G47 | Independent sign-off. The crop review sign-off for a package is done by someone other than the worker who pai… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G48 | Queued problems block their space. When a package contains a space with an open row in the repaint queue, its… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G49 | Staged fixes must survive the merge. Before a combined build ships, run the text pre-screens (gates 5 and 6) … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G50 | User-reported issues ship as hotfixes. Every review lists each issue the user reported, whether it is still l… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G51 | Every time a user reports a new kind of issue, add it here as a numbered gate with the example, and add an au… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G52 | At review checkpoints, re-run every gate over the whole live site plus everything in the deploy queue and in … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G53 | Never skip a space because someone else is repainting it: run the gates on it, report it, and leave the fix t… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G54 | Try one small navigation or UX improvement per checkpoint, using mockups first. Keep it if it passes the gate… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G57 | Prefer orientation cues that highlight an existing exit (a brief glow on the way you came in, progress dots a… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G58 | Navigation pattern: the breadcrumb is the hierarchy control, painted exits show a hover or first-tap preview … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G59 | Verb-street hooks describe the action and the sound clue only. The balcony, window or roof tier is shown by p… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G62 | Don't over-police (user, 13:12 UTC): harmless whimsy is fine, e.g. a bee on a Bible or cartoonish slapstick d… | c | CONTENT, TEXT, ITEMS — plus post-paint check | NO |
| G63 | User-hook coverage gate: every row the user wrote (qa_020 / qa_100) must be applied in every build, loading l… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G64 | Integration mirror check: run reflexive_mirror_check.py on every combined build's art, not only on packages. … | c | ITEMS (hand mirror for pronominal verbs) — mirror script — plus post-paint check | NO |
| G65 | Hooks file apply order: packages that each ship a whole hooks file must declare a row count, and the build us… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G68 | Mnemonic pictures are now made as separate assets, independent of the room, then placed into an empty painted… | c | STYLE, SETTING — plus post-paint check | NO |
| G70 | E. Per asset (before it may be placed). Check every word's asset on its own, at full size: | c | ITEMS, SETTING — plus post-paint check | NO |
| G71 | Mnemonic represented: the asset shows the hook's sound-alike object AND the meaning, as the hook text describ… | a | TEXT, LIGHT AND COLOUR, PLACEMENT AND SPACING | NO |
| G72 | One word only: nothing in the asset stands for another word or an unnamed extra figure. | a | ITEMS, FIGURES | NO |
| G73 | Clean render and anatomy: gates 2 and 3 apply (limbs, hands, faces, no garbled parts, no stray text, symbols … | a | TEXT, GROUNDING AND ANATOMY, FIGURES | NO |
| G74 | Style match: the same line weight, saturation and cartoon level as the room's style family, lit from the same… | a | LIGHT AND COLOUR, STYLE, SETTING | NO |
| G75 | Clean cutout: a transparent background, no white fringe or halo, no cut-off parts, and the base (feet, bottom… | c | GROUNDING AND ANATOMY, PLACEMENT AND SPACING — plus post-paint check | NO |
| G76 | Perspective fits its spot: the asset is drawn at the angle of the surface it will sit on (an item for a count… | a | ITEMS | NO |
| G77 | Card-ready: the same file reads well alone on the word card. | c | ITEMS — plus post-paint check | NO |
| G79 | F. Final scene (after compositing). Check the finished room at desktop and phone sizes: | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G80 | No overlaps: no asset overlaps another asset, a hotspot box, a label or a control. Each asset is clearly sepa… | c | PLACEMENT AND SPACING, SETTING — plus post-paint check | NO |
| G81 | No confusing labels: each label (or hover highlight) sits on its own asset and can't be read as belonging to … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G82 | Not pasted on: every asset rests on a real surface (floor, counter top, shelf, ledge) with a contact shadow o… | a | LIGHT AND COLOUR, GROUNDING AND ANATOMY, PLACEMENT AND SPACING | NO |
| G83 | Coherent room: the room still reads as one real place with its landmark visible, nothing important is hidden … | a | GROUNDING AND ANATOMY, PLACEMENT AND SPACING, SETTING | NO |
| G84 | Hotspots line up: clicking the centre of each asset opens its own card at every screen size. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G85 | Report the E and F results per word and per room with screenshots or crops, fix and re-check, and only then s… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G86 | Signs are assets, labels always show (user, 14:29 UTC): a room's name sign is its own asset with its text fit… | c | TEXT, PLACEMENT AND SPACING, ITEMS — plus post-paint check | NO |
| G89 | Gates G and H. Each must pass before a space is shown to the user. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G92 | Planned assignments are law. Every space takes its words from the project's planned item-to-room assignment (… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G93 | Every word suits the place. A teacher reading the room's name would expect each item there. Furniture that is… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G94 | A close-up is a real spot where its objects belong: a coat peg, a knitting basket, an easel, a vestment cupbo… | c | IMAGE (zoom: real spot where objects belong) — plus post-paint check | NO |
| G95 | A close-up looks like the same place as its parent: the same piece of furniture, walls, light and style, just… | a | COMPOSITION, STYLE, SETTING | NO |
| G98 | No rows of stickers. Items are never lined up in the foreground of an empty room. Use the whole frame: walls,… | a | COMPOSITION (not a lineup, clusters + open floor), SETTING (whole frame) | NO |
| G99 | Scene first, then assets drawn to fit. Paint the room first, then write a slot spec for every item before gen… | c | LIGHT AND COLOUR, GROUNDING AND ANATOMY, PLACEMENT AND SPACING — plus post-paint check | yes |
| G100 | Nothing merges with architecture. No figure overlaps a door frame, door leaf or exit opening so that it seems… | a | DOORS AND EXITS, PLACEMENT AND SPACING, FIGURES | NO |
| G101 | Verb characters act at human scale in the scene, never as tiny figures in a row. | a | ITEMS, FIGURES, COMPOSITION | NO |
| G102 | Real doors to sub-rooms. A sub-room is reached through a painted door, stair or archway, never a sign on a wa… | a | DOORS AND EXITS, COMPOSITION, STYLE | NO |
| G103 | Cards show all options at once. All tense tabs or similar choices are visible at every screen size by wrappin… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G104 | Every hook element is visible. The sound-alike creature or object is drawn in the item's own picture. (Once, … | a | ITEMS, FIGURES | NO |
| G105 | Show before shipping. Show the user clean screenshots of a redone space before it goes live, and fix what the… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G108 | These are blocking. A space does not ship until each one passes, and the builder looks at the rendered screen… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G109 | Zoom matches parent. For every zoom, render a side-by-side of the zoom next to the crop of the same object in… | a | LIGHT AND COLOUR, DOORS AND EXITS, PLACEMENT AND SPACING | NO |
| G110 | Verbs use the language's chosen verb marker. Every verb is acted out by the recurring verb marker picked for … | a | ITEMS | NO |
| G111 | Labels clear of everything. No label may overlap or touch another label, another item's click box, a door or … | c | DOORS AND EXITS, PLACEMENT AND SPACING, ITEMS — plus post-paint check | NO |
| G112 | Re-audit what is already live. When a new gate is added, audit the spaces already shipped against it and fix … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G115 | Hook gate: every mnemonic is a visible sound-alike of the target word, acted out ON or touching the item. Fai… | c | ITEMS — plus post-paint check | NO |
| G116 | Animal gate: no anthropomorphic animals unless the animal is the hook. Otherwise use an ordinary person carry… | a | ITEMS, FIGURES | NO |
| G117 | Anatomy gate: count the arms, legs, feet and limbs on every figure, check faces look normal, and check for du… | a | GROUNDING AND ANATOMY, ITEMS, FIGURES | NO |
| G118 | Style gate: compare each new or repainted space against the approved reference scenes (palette, saturation, l… | a | LIGHT AND COLOUR, COMPOSITION, STYLE | NO |
| G119 | Theme gate: every word fits its room's theme in the sense taught. Secondary or homonym senses go to a room th… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G120 | Naming gate: room names make sense for their contents, and every place name shows a translation. | c | SETTING — plus post-paint check | NO |
| G121 | Verb-scene gate: verbs are acted out inside natural, unique themed scenes. A row of verb markers on a plain s… | a | PLACEMENT AND SPACING, ITEMS, COMPOSITION | NO |
| G122 | Exterior gate: a building or street seen from the level above shows the landmarks visible inside (and vice ve… | c | STYLE (sector look) / IMAGE zoom line; map paintings outside template scope — plus post-paint check | NO |
| G123 | Clutter gate: no overlapping items, believable layouts (tracks, crossroads, floors), and scenes that aren't t… | a | PLACEMENT AND SPACING, ITEMS, COMPOSITION | NO |
| G125 | Hook edits are surgical: when rewriting a word's hook, change only its `hook` and `why` fields. Replacing the… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G128 | Liveliness gate: a room is a lively scene, not an inventory. A few items lined up is fine where that's natura… | a | SITUATION, COMPOSITION (lively, not an inventory), AVOID | NO |
| G129 | Distinct-room gate: before shipping a building, put all its room thumbnails side by side. Each room needs its… | a | VARIETY (unique composition, camera, focal action, light) | NO |
| G130 | Exterior-character gate: on the overview and sector maps, every building's exterior shows its function at a g… | c | STYLE (sector look) / IMAGE zoom line; map paintings outside template scope — plus post-paint check | NO |
| G131 | Zoom-continuity gate: each district on the overview map is a zoomed-out miniature of the map you get when you… | c | STYLE (sector look) / IMAGE zoom line; map paintings outside template scope — plus post-paint check | NO |
| G132 | Overview-consistency gate: every district's sector map, building exteriors and interior establishing views ma… | c | STYLE (sector look) / IMAGE zoom line; map paintings outside template scope — plus post-paint check | NO |
| G135 | Placement-by-meaning gate: no word sits in a room only because its English gloss shares a word with the room'… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G136 | Sense gate: the gloss and picture show the sense the room teaches; a homograph with two senses in two rooms h… | c | ITEMS, SETTING — plus post-paint check | NO |
| G137 | Sensitive-setting gate: no grave or sensitive word in a light-hearted room; it is plain wall text in a sober … | c | CONTENT, TEXT, ITEMS — plus post-paint check | NO |
| G138 | No-overflow gate: every room's words share an honest theme that can be painted as one scene. Rooms of leftove… | c | PLACEMENT AND SPACING, ITEMS, COMPOSITION — plus post-paint check | NO |
| G139 | One-hook gate: a word that appears in more than one room has the same hook everywhere. | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G140 | Forced-pun gate: reject hooks with the wrong vowel, more than two sound chunks, a pun object that only sits b… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G141 | Integrated-verbs gate: a room's verbs are spread through the scene and interact with its nouns. A room fails … | a | PLACEMENT AND SPACING, ITEMS, COMPOSITION | NO |
| G144 | Rebuild after every repaint. If a scene painting changes, rebuild that building's cards and data js with the … | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G145 | Parent miniature and zoom hint. When a zoom room is repainted, the parent room's miniature (the window, hatch… | c | TEXT, DOORS AND EXITS, ITEMS — plus post-paint check | NO |
| G146 | Shelf audit. Periodically rank every built room by how much of it is shelves, cubbies or rows of figurines, a… | a | PLACEMENT AND SPACING, COMPOSITION, SETTING | NO |
| G147 | No text, including props. The no-text check covers mugs, speech or thought bubbles, coins, signs, price tags … | a | TEXT | NO |
| G148 | Ownership before paint. Before painting a room, check the other workers' packs and the live site for a more r… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G149 | Shared data merges. When two packs touch the same building's data js or cards, regenerate those files from th… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G150 | Deploy attachment limit. Keep every deploy tarball under 25 MB. Keep screenshots and review sheets outside th… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G151 | Removal accounting. Track every word a fix takes off the live site (plan-only moves) and every room left spar… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G154 | Overview is one painting, never patches. When a district on the overview doesn't match its sector map, repain… | c | STYLE (sector look) / IMAGE zoom line; map paintings outside template scope — plus post-paint check | NO |
| G155 | Number rooms count exactly. Every number item shows exactly that many easy-to-count things (onze is 11 footba… | a | ITEMS, SETTING | NO |
| G156 | "Unbuilt" is checked by word id. Before building a planned room as new, search every live data file for its w… | b | — (not a painting instruction: data, geometry, overlay, tooling, process or deploy; still gated after paint) |  |
| G157 | Sensitive words in new rooms. For a grave word that lands in an ordinary room (slavery, poverty), use a blank… | a | CONTENT, TEXT, ITEMS | NO |
| N1 | Text policy: natural scene text OK; no stray/garbled text, count-breaking digits, speech bubbles | c | TEXT | NO |
| N2 | Item manifest before painting | c | Fields + every ITEMS line (filled from manifest) | NO |
| N3 | Cheap checks first, one contact sheet per room | b | — |  |
| N4 | Batch deploys | b | — |  |
| N5 | unbuilt.py first | b | — |  |
| N6 | No one-object zooms (4–6 words per zoom) | a | ITEMS (N; zooms 4–6) | NO |
| N7 | One worker per workstream | b | — |  |
| N8 | Natural-scene gate (new, v13.1) | a | SITUATION, COMPOSITION, FIGURES, AVOID, Before sending (labels-off test) | NO |
| N9 | Prompt built from template (new, v13.1) | a | whole template; precheck FAILs missing fields | NO |
| N10 | No repeated motifs across rooms (new, v13.1) | a | VARIETY (used motifs) | NO |
