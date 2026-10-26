# Site features and UI

Read when building or reviewing the site shell, dialogs, cards or controls.

## Site features (typical)

World map, sector views, rooms, detail cards, a beginner/start area, an about page, quiz mode, full screen mode, and keyboard navigation. <!-- B84 -->

## Site UI rules (lessons from user review)

- The core test: a user can wander the whole place immersively in fullscreen, learning items in their locations so the place itself aids memory, with real visual variety from space to space. Keep the UI simple, and don't add gadget features (collections, mini-maps) the user didn't ask for. <!-- B87 -->
- The look should be whimsical and storybook-like, not stuffy or formal. Use soft natural UI colours, never orange or amber chrome. <!-- B88 -->
- The painting is the whole experience. Fullscreen must really fill the screen with the image (Fullscreen API) and everything must stay usable there. <!-- B89 -->
- Don't use a side panel, and put no text below the image. Item details and any other info open as centred dialogs over the picture (close with X, Esc, or the backdrop). <!-- B90 -->
- Add a toggle (also a key, e.g. H) that highlights all clickable areas, plus a hover effect and a pointing-hand cursor on every clickable area. Users can't otherwise tell what's clickable. <!-- B91 -->
- Make every door, arch, stair and path visibly enterable even with highlights off: a small always-visible badge showing the walking direction, plus a hover glow and the destination name. Keep this cue distinct from the zoom icon. <!-- B92 -->
- Mark every zoom-in spot with a small always-visible icon (e.g. a magnifying-glass badge) so learners know it opens a closer look at another little area. <!-- B93 -->
- Every space has a back control to the space above it (room to building, building to sector, sector to village), so no view is a dead end. <!-- B94 -->
- Navigation is walking: click painted paths, doors, stairs, and arches, shown with subtle on-image arrows. Never make users pick the next space from a list or signpost menu. <!-- B95 -->
- Rooms in the same building connect directly (stairs or doors painted in the room). Never force a trip outside to get between them. <!-- B96 -->
- Label every building with its name (a painted sign with overlay text, plus a hover name on its door). <!-- B97 -->
- Keep the top bar minimal: no current-place name and no topic sections such as prayers. Those live inside the world. <!-- B98 -->
- Keep cards lean: no level badge and no placement notes (e.g. "left side"), because the scene already shows that. Show every option rather than hiding some behind a "more" button (e.g. all tense tabs on a verb card). <!-- B99 -->
- Keep control buttons in a slim strip outside the painting, never on top of it. <!-- B100 -->
- Include a site guide (an overlay opened from the top strip) explaining every placement convention: what sectors, buildings, floors, sides, tiers, plaques, mirrors, signs, and mnemonic characters mean. Keep it out of item cards, and in one editable data file that stays in sync with the skill's rules. <!-- B101 -->
- Drop explanatory "how this memory works" boxes on cards. The mnemonic/hook explanation is enough. <!-- B102 -->
- Audit every hotspot so it lands on the right thing (crop each box and check it). A click that leads to the wrong place breaks trust. <!-- B103 -->
- **Cards show all options at once.** All tense tabs or similar choices are visible at every screen size by wrapping or a grid, never by sideways scrolling. <!-- G103 -->

## Navigation pattern notes (from the gates rounds)

- Prefer orientation cues that highlight an existing exit (a brief glow on the way you came in, progress dots along a short street) over new buttons, because they add no second control to any destination. <!-- G57 -->
- Navigation pattern: the breadcrumb is the hierarchy control, painted exits show a hover or first-tap preview of the destination with its name, and an optional Plan panel shows the top-down plan with a you-are-here dot. <!-- G58 -->
