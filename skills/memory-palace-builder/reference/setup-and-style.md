# Setup, art style and colour

Read when starting a palace, choosing the art pipeline, or checking colour and style.

## Settings to fix up front

A generic recipe for building an explorable memory palace (a world of places where each fact is pinned to a vivid image at a fixed location). For language learning, also load the language memory palace skill, which layers on top of this one. <!-- B9 -->

- **Subject and scope**: what body of knowledge, and its levels (e.g. beginner to expert). <!-- B12 -->
- **Setting**: the overall world (village, castle, ship, campus). Prefer an idyllic, real-life-plausible place so layout feels natural. <!-- B13 -->
- **Style slider** from 1 (very cartoonish) to 5 (realistic). Record the chosen value and use it in every image prompt so rooms stay consistent. Example: 3 = respectful, slightly realistic painterly with cartoony elements. <!-- B14 -->
- **Art style (ask, don't assume)**: before painting anything, ask what art style the person wants. Cover the medium and look (painted storybook, watercolour, flat cartoon, realistic), the colour feel (natural true colours vs a stylised palette), lighting, and how whimsical the characters should be. Generate 1-2 sample scenes in the chosen style and get a yes before making all the art. <!-- B15 -->
- **Site look (ask, and mock it up)**: ask what feel they want for the website itself (e.g. whimsical storybook vs clean and minimal), then show a mock-up image of a real screen, such as a scene with an item card open, and one for each distinct card type (noun, verb). Iterate on the mock-up until they approve, then hand the approved image to the site builder as the style reference. <!-- B16 -->
- **Output**: static site (e.g. GitHub Pages), print, or images only. <!-- B19 -->
- Sacred/cultural respect and audience: see sensitive-content.md.

## Art pipeline and asset structure

Choose between generated illustrations (richer, harder to keep consistent and edit) and hand-coded SVG (each item a separate <g> with an id, class, and title, so it is clickable, consistent across map/sector/room, and editable). Show the user one example room in each candidate pipeline before committing. A generator script that emits SVG from the room data keeps token use low. <!-- B67 -->

Current preferred method (user review, Oct 23): keep the painted empty room as the fixed scene, then draw each item's asset to fit its exact slot (surface, angle, light, size, pose, occlusion) and composite it with code harmonisation. A single item can then be fixed without repainting the room. See gate H in the release-gates skill. The notes below are older lessons. <!-- B70 -->

Lessons from testing: flat vector SVG looked noticeably uglier than painted art, and painted cutouts composited onto a painted room looked jarring (different brushwork and lighting, sticker effect) even with shadows and color matching. Prefer one full painting per room plus a hotspot data file (polygon or box per item) for clickability; edit by regenerating the room with the previous image as a reference. If you do composite, generate objects with the room as a style and lighting reference. <!-- B71 -->

Alternative: keep each item as its own asset (one file per object) and each room as an empty background plus a layout data file (object id, position, scale, z-order, category side). A build script composes rooms, sector views, and the world map from these, so edits touch one small file, objects are reused consistently across views, and token use stays low. Shared style rules (palette, outline weight, light direction) plus an auto-added ground shadow make objects sit naturally in the scene. Large fixed features that interact deeply with the architecture can stay part of the background. <!-- B72 -->

## Consistency

- Each object has one canonical position stored in data; the map, sector, and room views all read from it. <!-- B75 -->
- Keep a style guide (style slider value, palette, line weight, lighting) and reuse the same prompt preamble for every image. <!-- B76 -->

## Colour (merged)

- **Natural true colour.** Every scene uses natural true colours in clear neutral daylight with no overall tint, filter or colour grade (off-white walls, white whites, varied clothing), so items stay easy to see. Image models drift toward a golden, orange, sepia or amber "cozy" cast, especially in warm interiors: prompt explicitly for neutral daylight and true colours, avoid orange, terracotta and peach interior walls, and reject warm-cast images. Grade back to neutral daylight where that works, but post-hoc colour correction only softens a cast, so repaint when a scene still reads orange. Make sectors distinct through setting, materials, architecture and time of day, NOT colour grading, and keep the realism level constant across sectors. Before release compare each painting with the approved reference / palette sheet; an amber, sepia or orange cast over a whole room or street fails, and any drift is flagged. <!-- B161 B169 B212 G42 -->
- A "no gender tint" rule bans an overall pink or blue wash, not natural blue sky, water, or blossoms. Don't let painters strip every blue. <!-- B213 -->
