# Text in images, signs and labels

Read when prompting or reviewing anything with text, signs or labels in or over a painting.

## Text in the painting

- **Labels and names are overlays.** Item labels and sign names are real HTML/SVG text over the image, never baked into the generated painting, so they are legible, correct and translatable; all sign and label text fits inside its sign at all supported screen sizes. Style them to blend into the scene (carved, painted, engraved or chalk lettering matching the material) rather than looking like a UI label. <!-- B58 -->
- **Text in the image is NOT absolutely forbidden (owner, Oct 26).** Natural scene text that makes sense there, such as a shop sign, a book spine, a poster or a station board, may stay when it is spelled correctly, fits the place, covers no item and never stands in for a taught word's picture or label. <!-- N1 G147 -->
- **Still out:** stray, garbled or meaningless letters; symbols or currency signs on props ("$", "…"); painted digits that change or confuse a count (see the release-gates reference/number-and-count-rooms.md); speech or thought bubbles; and any text a learner could mistake for a label. Generated props (mugs, coins, signs, price tags, badges) often come back with these, so check small props and paint them out before shipping. <!-- N1 B235 G147 -->
- **OCR flags, a human decides.** `tools/precheck.py` lists every confident text run with its box as a FLAG for human review; it never auto-rejects. Declare intended scene text in the manifest's `text_in_image` so the reviewer can tell it from strays. OCR misses small or low-contrast text, so the contact-sheet review still looks. <!-- N1 N3 -->

## Signs

1. Nothing important is conveyed only by hidden or tiny text; every item is visible as an image (except mature items deliberately shown as text). <!-- B57 -->
- Sign and building-name text is readable at normal size, and side-split signs are clearly split. <!-- B167 -->
- Signage never looks like an item. Direction and section signs use one signage-only style, sit at the edges or overhead away from item boxes, and are never placed like a figure's prop. Note busy paintings as a minor finding, but don't repaint just for busyness. <!-- B168 -->
- One label per thing. When a door, path or place has a sign naming it, hovering lights up that sign (glow, slight lift, pointer cursor) instead of showing a second tooltip with the same words. A hover name pill appears only for exits with no sign. Sign text is rendered to look painted on the board (fitted serif or engraved lettering, no panel over the board), and the direction badges are icons only. <!-- B172 -->
- Signs and plaques must never cover or overlap an item or its mnemonic. Check text boxes against every hotspot box. <!-- B200 -->
- Sign text must be easy to read: large, high-contrast, on a light flat plate, consistently placed per side. <!-- B209 -->

## Labels

- Budget room for labels. Estimate each label's rendered width (about 0.5 x font size per character, article included) and keep neighboring boxes far enough apart that both labels fit under their own figures, roughly 110 px between neighbors with long words. <!-- G15 -->
- Each label sits on or just under its own figure, clearly closer to it than to any neighbor, with a visible gap between items. Script-check that every label's center lies inside its own box and nearer to it than to any other. <!-- B163 -->
- **Sign text fits its sign, labels always show (user, 14:29 UTC):** a room's name sign is an HTML overlay with its text fitted inside the plaque with padding at every screen size; text overflowing a sign's edges fails. Every placed item carries a visible label (word with article, verbs as the infinitive), always shown, not only on hover. In language palaces, place feminine nouns clearly left and masculine clearly right, in zooms too, with no physical divider; slight overhang of the center line is fine, and any real exception is listed. <!-- G86 -->
- Rendered label rectangles, touching and edge rules (gates 7 and the Round 5 label gate): see the release-gates reference/space-gates.md.
