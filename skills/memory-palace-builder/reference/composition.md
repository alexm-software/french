# Room composition

Read when designing or reviewing a room's painting. Gate wording for scenes: release-gates reference/space-gates.md.

## Mnemonic images

- **Natural scene first.** Compose the room as one named everyday situation with small interacting groups, varied facing and depth, clusters and open floor, never a lineup or grid of isolated hook figures each doing its own gag; with labels hidden it must read as a storybook moment. The prompt carries this via `reference/prompt-template.md` (SITUATION, COMPOSITION); the gate is release-gates reference/space-gates.md (natural-scene gate). <!-- N8 -->
- Each item is a zany, whimsical object, character, or creature that both sounds like the item (when said aloud in the learner's language) and visually represents its meaning. <!-- B42 -->
- Props that carry the sound cue must be large, prominent, and unambiguous. <!-- B43 -->
- A helper character that carries the sound cue must sit right next to (visibly interacting with or pointing at) the item it helps with, never far across the room. <!-- B44 -->
- Keep one clear concept per object; avoid scenes where the prop could be read as an ordinary furnishing. <!-- B47 -->
- Vary designs so rooms, buildings, and sectors never start to look the same: change shapes, palettes, eras, and architecture. <!-- B48 -->

## Each room must have

- A sign naming the room's theme. <!-- B51 -->
- Clickable items opening a detail card with the full information. <!-- B52 -->
- A link back to the sector, and links to related rooms where they make sense. <!-- B53 -->
- Optional extras: scenes or dialogues, audio, quiz entries. <!-- B54 -->

## Room checks (run at the end of every room, before moving on)

1. Nothing important is conveyed only by hidden or tiny text; every item is visible as an image (except mature items deliberately shown as text). <!-- B57 -->
2. Sign, label and in-image text: see text-and-labels.md (natural scene text may stay).
3. Copyright: see copyright.md.
4. Every mnemonic actually works: say the sound-alike aloud, confirm it resembles the target, and confirm the picture also points to the meaning. Reject weak ones and redesign. <!-- B60 -->
5. Placement rules are obeyed (correct side, band, prop) and positions match between the world map, sector view, and room. <!-- B61 -->
6. Room density is within the target range; overflow goes to a new room or zoom spot. <!-- B62 -->
7-8. Age-appropriate, reverent content: see sensitive-content.md.

## Painting checks (lessons from user review)

- Every whimsical figure or creature must stand for a specific item in that space. No decorative whimsy, and cognates get no creature. <!-- B199 -->
- Give each item exactly one clickable box, covering the item and its mnemonic helper together. Compose them side by side so a single tight box works, and never add a second mnemonic box. <!-- B201 -->
- Keep hotspot boxes from overlapping: spread items into separate zones when you compose the scene, draw tight boxes, never put one item's box fully inside another's, and compute pairwise overlap before calling a space done. <!-- B202 -->
- Make sure the mnemonic action is actually visible, not just implied (e.g. "fracture" needs a bandaged jaw, not just a surprised face). <!-- B203 -->
- Make every figure unique: vary characters (ages, professions, animals, fantasy figures that fit the hook), poses, scale, and actions. A row of the same person in the same pose (e.g. chef after chef at a counter) is unmemorable and must be repainted. <!-- B204 -->
- Buildings need whimsy too. Plain realistic houses are forgettable, so give each building a memorable, playful shape or feature tied to what it holds (a house shaped like a pot, a crooked tower, a door like a giant loaf), while the scene still reads as a natural place. <!-- B205 -->
- Balance natural against efficient. Architecture, negative space and shared activity make a place memorable. Give hooks enough separation and depth; do not fill every empty patch with another word. <!-- B206 -->
- Props are hooks too. Don't add decorative ornaments, like a teapot or cheese on a rooftop, that don't stand for an item. <!-- B207 -->
- Zoomed-in sub-spaces follow the same placement rules (e.g. gender sides) as their parent room. <!-- B208 -->
- Sign text and signs never covering items: see text-and-labels.md.

## Local edits and paint-backs

- **Local edits in context.** Edit a region (a paint-back, a hook fix) with the whole painting as the input image and a mask, asking to change only that region and keep everything else. Never paste in a separately generated figure or object, and never use a low-frequency color correction. If the edit shows a seam or a light or brushwork mismatch, repaint the room. <!-- B233 -->
