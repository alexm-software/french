# Number and count rooms

Read when a room holds numbers or any word whose picture depends on a count.

- **Number rooms count exactly.** Every number item shows exactly that many easy-to-count things (onze is 11 footballers, quatre is 4 cats, and the zéro nest is empty). Count each one at 2x before packing. <!-- G155 -->
- **Counts live in the manifest.** Every number word (and any item whose hook names a count) carries an exact integer `count` in the item manifest before painting; precheck.py fails a missing count. <!-- N2 -->
- **Painted digits break counts.** A digit painted in the scene (a shirt number, a clock, a price) that differs from or competes with the counted things fails; OCR flags digits for the reviewer. A digit that is the natural scene text of the place may stay only when it cannot be read as the answer (text rule: builder reference/text-and-labels.md). <!-- N1 -->
- Duplicated objects that break a count (two teapots, four cups for two people): anatomy gate, item-gates.md.
