# Setup, art style and color

Read when starting a palace, choosing the art pipeline, or checking color and style.

## Settings to fix up front

A generic recipe for building an explorable memory palace (a world of places where each fact is pinned to a vivid image at a fixed location). For language learning, also load the language memory palace skill, which layers on top of this one. <!-- B9 -->

- **Subject and scope**: what body of knowledge, and its levels (e.g. beginner to expert). <!-- B12 -->
- **Setting**: the overall world (village, castle, ship, campus). Prefer an idyllic, real-life-plausible place so layout feels natural. <!-- B13 -->
- **Style slider** from 1 (very cartoonish) to 5 (realistic). Record the chosen value and use it in every image prompt so rooms stay consistent. Example: 3 = respectful, slightly realistic painterly with cartoony elements. <!-- B14 -->
- **Art style (ask, don't assume)**: before painting anything, ask what art style the person wants. Cover the medium and look (painted storybook, watercolor, flat cartoon, realistic), the color feel (natural true colors vs a stylized palette), lighting, and how whimsical the characters should be. Generate 1-2 sample scenes in the chosen style and get a yes before making all the art. <!-- B15 -->
- **Site look (ask, and mock it up)**: ask what feel they want for the website itself (e.g. whimsical storybook vs clean and minimal), then show a mock-up image of a real screen, such as a scene with an item card open, and one for each distinct card type (noun, verb). Iterate on the mock-up until they approve, then hand the approved image to the site builder as the style reference. <!-- B16 -->
- **Output**: static site (e.g. GitHub Pages), print, or images only. <!-- B19 -->
- Sacred/cultural respect and audience: see sensitive-content.md.

## Art pipeline

Each room or zoom is one integrated painting plus a hotspot data file (a polygon or box per item) for clickability; word-card images are cropped from the finished painting. Flat vector SVG looked noticeably uglier than painted art. Edit by regenerating the room with the previous image as a reference, or by editing a region with the whole painting as context. <!-- B71 -->

## Consistency

- Each object has one canonical position stored in data; the map, sector, and room views all read from it. <!-- B75 -->
- Keep a style guide (style slider value, palette, line weight, lighting) and reuse the same prompt preamble for every image. <!-- B76 -->

## Color (merged)

- **Natural true color.** Every scene uses natural true colors in clear neutral daylight with no overall tint, filter or color grade (off-white walls, white whites, varied clothing), so items stay easy to see. Image models drift toward a golden, orange, sepia or amber "cozy" cast, especially in warm interiors: prompt explicitly for neutral daylight and true colors, avoid orange, terracotta and peach interior walls, and reject warm-cast images. Grade back to neutral daylight where that works, but post-hoc color correction only softens a cast, so repaint when a scene still reads orange. Make sectors distinct through setting, materials, architecture and time of day, NOT color grading, and keep the realism level constant across sectors. Before release compare each painting with the approved reference / palette sheet; an amber, sepia or orange cast over a whole room or street fails, and any drift is flagged. <!-- B161 B169 B212 G42 -->
- A "no gender tint" rule bans an overall pink or blue wash, not natural blue sky, water, or blossoms. Don't let painters strip every blue. <!-- B213 -->
