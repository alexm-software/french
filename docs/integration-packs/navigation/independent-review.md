# Independent review — integrated navigation

**Verdict: PASS for final navigation artwork, edited teaching cues/anatomy, and fitted interaction geometry.**

Reviewed the six installed paintings against their navigation manifests and current layouts. Compared the three edited teaching paintings with the standalone source paintings. Unchanged teaching-room art retains its prior independent review.

| Painting | Reviewed SHA-256 |
| --- | --- |
| restaurant/accueil.jpg | `048ae0ff24f62bad2909d68211fe9bed7f00c0c4292e676cba3933034ee809f8` |
| maths/accueil.jpg | `3586c3935ebdb621a6ed9da3327bcb343aadc87d49113d03aefe0fc33e3fa267` |
| caserne/accueil.jpg | `471629b9b1ef7ba433af6fc3001f471d56f3bf6d32c5828fbf215f3201db6985` |
| restaurant/preparation.jpg | `28a998d2c6a5df97d4ea9461a1889d052cd5dea6265572d5d6e4f9fc4cdf1691` |
| maths/quantites.jpg | `c668ab8c236fc036ac33c432c18ceef7fb269fb8c7cbf71f7d511616d038faf2` |
| maths/modeles.jpg | `d90b1b395f547be381e050b630426a65a7def07b1934518fb3762469815eb014` |

## Navigation and measured hit recommendations

Rectangles below are conservative clickable portions of actual painted openings, in 1280 × 720 pixels as [x,y,width,height]. They avoid adjacent walls, door leaves and target groups.

| Room | Destination | Recommended hit |
| --- | --- | --- |
| restaurant/accueil | cuisine_chef | [325,250,210,250] |
| restaurant/accueil | degustation | [642,245,217,255] |
| restaurant/accueil | preparation | [974,245,235,260] |
| restaurant/accueil | map | [80,245,120,270] |
| maths/accueil | mesures | [341,414,99,151] |
| maths/accueil | quantites | [545,215,110,125] |
| maths/accueil | modeles | [1006,210,114,133] |
| maths/accueil | map | [70,294,106,300] |
| caserne/accueil | entree | [978,280,231,250] |
| caserne/accueil | map | [90,253,205,300] |
| maths/quantites | maths | [950,525,225,150] |
| maths/modeles | maths | [727,510,105,150] |
| restaurant/preparation | restaurant | [1020,325,145,290] |

Restaurant courtyard arches are walkable at floor level and preview three recognizably different workrooms with matching sage-green trim, white tile, copper utensils and chef-hat architecture. The street gateway is distinct from the workroom arches. The mathematics hub has a ground-floor laboratory, a continuous oak staircase with slate-blue rails reaching both upper door thresholds, and a separate campus exit. Its two teaching scenes now show descending oak stairs with matching rails. The museum vestibule has a distinct town-square exit and a clear tall stone passage into the display gallery. Its planned forward museum circuit is coherent with arrival behind the viewer in the teaching scenes.

## Teaching-art comparison

Inspected the edited people and animals at 2×, including kitchen hands/tools, cat limbs/tail and cow muzzle/horns; the three quantities presenters and their hands; and the mathematician’s hands, legs, shoes and stool. No new extra limbs, detached anatomy, unsupported figures or clipped target cues were found. The bread halves/1⁄2, quartered disk with one blue quarter/25%, ≈20 estimate, three-piece ration, five cubes split three-plus-two/5−2=3, and 4×3=12 remain correct. The equation, 2×2 matrix, complete suspended three-shape mobile and seated mathematician remain complete. Existing target positions and sides are retained.

The models edit removes the globe’s former crank while preserving its globe, axis, complete pedestal and directional equator arrow. That visible combination clearly depicts rotation, and the runtime hook now accurately names those visible cues. No extra prop is needed for the intended meaning.

The final preparation revision raises the complete cow/bean/colander group above a taller courtyard door. The horns, muzzle, bean and colander remain complete; the door has a clear continuous threshold and plausible proportions. Checked all seven groups again against the installed final image. Six existing word boxes remain valid; the haricot box is refitted to [1014,88,205,198]. The doorway’s safe opening hit is [1020,325,145,290]. Those two fields were updated directly in restaurant/layout.json. All seven groups are complete and nonoverlapping, and the return-door rectangle intersects no target rectangle.

Recomputed interaction geometry from the current layouts for preparation, quantites and modeles: zero positive-area item/item intersections and zero door/item intersections in all three. Enlarged final preparation anatomy and meaningful cues remain correct. No further artwork changes are required.

No image edits were made by this reviewer. Only the final preparation haricot box and return-door hit were changed in the layout, as requested by the implementing agent. Browser navigation, final renderer labels and route execution remain separate implementation checks.
