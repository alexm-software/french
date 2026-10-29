# Validation (what any validator bot must do)

Read when acting as a validator for a sector or release.

A validator is a separate reviewer bot or pass that checks a sector or release before it ships. It did not build the work, so it judges against the rules in this skill and the user's recorded feedback, not against the builder's notes. <!-- B125 -->

**How to run**
0. Walk the live site as a learner before anything else: in a normal window and in fullscreen, click into every place and back out, and open and read every card in full. Mechanical checks passing never means the release is ready. <!-- B128 -->
1. Validate one sector or room set at a time, and run the whole checklist every time, not only the parts that changed. <!-- B129 -->
2. Use tooling for the mechanical checks (schema, overlap, links, counts). Look at every painting yourself for the visual checks. Open the live or preview site, not only the data files. <!-- B130 -->
3. Record every finding in a VALIDATION report with: location (room, item or file), the rule broken, severity (blocker, major, minor), evidence (screenshot crop, line or value), and the suggested fix. <!-- B131 -->
4. Blockers stop the release: safety or content problems, copyright problems, broken navigation, wrong links, or a schema or validator error. Majors should be fixed before release. Minors can be listed for later. <!-- B132 -->
5. Don't fix things silently. Report them, or fix them and log each change in the report. Re-run the full checklist after fixes. <!-- B133 -->
6. Never invent facts. If a check can't be done (missing source, no access), mark it "not checked" with the reason. <!-- B134 -->

**Whole-palace structure (check every release, not only the changed sector)**
- Maps agree at every level, no disconnected areas, consistent hierarchy: see maps-and-navigation.md.
- **Consistent conventions.** Placement scheme, sign style, direction cues and transitions (doors, stairs, paths) work the same way in every sector, so a learner who knows one area can read any other. Flag sectors that drift from the shared conventions. <!-- B140 -->
- **Balanced load.** No sector, building or room is overloaded or nearly empty compared with the density rules, and no two places are so alike that they'd blur together in memory. <!-- B141 -->

**Data and pipeline**
- The pipeline validator passes with 0 errors. Every item has its required fields, and no pending or placeholder values (TODO, lorem, empty hooks) remain. <!-- B144 -->
- Counts match: every item in the source list is placed exactly once, with no duplicates or orphans. <!-- B145 -->

**Content and safety**
- Age-appropriate content, mature words as plaques, sacred respect, usage warnings: see sensitive-content.md.
- Facts, definitions and examples are correct. Spot-check at least 10% of items, plus every item flagged weak. <!-- B151 -->
- Every item belongs where it is placed. For each room, read its theme and check every item against it in the item's main or most useful sense, the way a teacher would, never by string or embedding similarity alone. Typical misses: an item placed by a rare sense (a caretaker's lodge in a restaurant), a near-synonym used where the everyday word is different (an invoice word for a restaurant bill when the restaurant word sits elsewhere), and filler topped up into a short room. Every misfit is a major. Also check the reverse: the words a learner most needs in that setting are actually in it. <!-- B152 -->

**Mnemonics**
- No template or filler wording reaches a card (e.g. 'Picture the plain object', 'label glowing'). Count repeated phrases across all hooks: any sentence that appears on more than a handful of items is a template and must be rewritten, whatever strength rating it was given. <!-- B155 -->
- Each hook's sound link and image actually match the item. The image is concrete, visible in the painting, and shows the action. <!-- B156 -->
- Every whimsical figure or prop stands for an item, and no hook relies on an offensive stereotype. <!-- B157 -->
- The hook text describes what is actually painted: the same figure (gender and pronouns, age, kind of character or creature), the same action and the same key props. Crop each box and compare. Whenever a painting is redone, update the hook to match the new art. <!-- B158 -->

**Paintings**
- Color: see setup-and-style.md (merged color rule).
- Placement means what the project says it means. Read the project's placement scheme (its site guide or placement notes, e.g. which side, height, floor, plaque or mirror stands for what). Then check each object in each painting, zoom spots included, against the meaning its spot is supposed to carry, and flag any object whose position contradicts the scheme. <!-- B162 -->
- Nothing in an item's box that isn't in its hook. No stray animals or props: every element is either the sound cue or the meaning. <!-- B164 -->
- Exactly one clickable box per item, covering the item and its mnemonic helper. Hotspot overlap is 0, and signs never cover items. <!-- B165 -->
- Figures are varied and unique, with no repeated poses or characters. Buildings carry whimsy tied to their items. <!-- B166 -->
- Every figure belongs to one coherent scene. People and animals stand on the floor, sit, or work at a real surface, at a consistent scale and perspective with contact shadows. They are never stacked in rows behind counters, perched on shelves, or floating like stickers. If a space can't hold its words naturally, split it or add a zoom instead of crowding. The learner walk-through flags any figure that looks pasted on. <!-- B170 -->
- Every item is fully in frame. No item, figure or key prop may be cropped by the image edge or hidden under the UI strips. Keep item boxes at least ~6% in from each edge. The viewer must never crop the painting to fill the screen (use contain-fit with a blurred or parchment surround, and put strips outside the image rect). The release check verifies every item and exit box is inside the visible viewport at several screen sizes. The fix for an edge item is to repaint or recompose, not to shrink the box. <!-- B171 -->
- Scenery is balanced: natural, but with little non-item clutter. <!-- B173 -->
- Labels, signs, sign text: see text-and-labels.md.

**Navigation and UI**
- Press every strip button and open every dialog in BOTH windowed and fullscreen modes. Overlays must render inside the fullscreen element. Button labels are plain and self-explanatory (e.g. 'Exit fullscreen', not 'Leave'). <!-- B181 -->
- True fullscreen works, with centred card dialogs and no side panel or text below the image. Control buttons sit outside the painting. The highlight toggle works. <!-- B182 -->
- Cards follow the approved mock-up: lean fields and every required field present. <!-- B183 -->
- **Text formatting and layout.** Put screenshots of each kind of dialog or card (e.g. noun, verb, place, guide, dialogue, credits) next to the approved mock-up and compare them. Check: generous inner padding so no text touches or crowds an edge; comfortable line height and clear spacing between sections; a clear type hierarchy (headword largest, then meaning, then details); consistent alignment and fonts matching the mock-up; and no overflow, clipping, awkward wrapping or orphaned single words, using the longest word, gloss, example and dialogue in the data. Repeat at desktop, small laptop and narrow mobile widths, and in every interface language (translations run longer). Also check that on-image labels and signs are readable against their background. Any visible drift from the approved mock-up is a major. <!-- B184 -->
- The language toggle switches all UI and meta text and leaves the item content alone. The site guide matches what the site actually does. <!-- B185 -->
- The site works on desktop and on a narrow mobile width, and the browser console shows no errors. <!-- B186 -->
- Hotspots, links, exits, plausible links and transitions: see maps-and-navigation.md.
**Copyright**: see copyright.md.

**Report back**
Give a verdict (ship, ship after fixes, or do not ship), counts by severity, the full findings list, and what was checked versus not checked. <!-- B192 -->

## When something new comes up

Read user feedback for its spirit. When they describe an experience ("walk through it, pick up words"), improve that experience; don't turn each phrase into a literal new feature. <!-- B195 -->

If a snag or a new user idea would help future palaces, fold it back into this skill (or the subject-specific one). <!-- B196 -->
