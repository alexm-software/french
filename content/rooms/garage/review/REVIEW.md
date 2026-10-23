# Garage package review

Base: `09d0b3c8681f34172510428070aa599294974606`. Claim commit: `6d7e0434c956ba58cf3d656972dd038e651dd910`. Independent reviewer: `garage_review` (separate agent, required by the repository release-gates skill).

Verdict: **independent visual and package checks pass; user approved merge**. No unresolved asset/hook/content findings in the nine reviewed sprites. Browser/integration gates are pending, not certified.

| Word | Source asset / hook / anatomy | Final composition proof |
|---|---|---|
| la clé | Pass | Pass |
| la planche | Pass | Pass |
| l'échelle | Pass | Pass |
| la réparation | Pass | Pass |
| le garage | Pass | Pass |
| le verrou | Pass | Pass |
| le bricolage | Pass | Pass |
| l'atelier | Pass | Pass |
| le trou | Pass | Pass |

## Findings resolved

- Brick collage originally showed a landscape: replaced only its sprite with physical colored bricks.
- Garage model initially floated above its niche: moved onto the stone sill.
- Adult craft figures were too small: enlarged and reflowed them.
- Plank and ladder contact with surfaces corrected; ladder lower legs occluded behind workbench.
- The independent reviewer found an empty derived atelier card: rebuilt it, reran checks and independently verified its nonzero size.
- Label/hotspot collisions found during layout were cleared and the package checker now passes.

## Checks performed

- Exact inventory equality: 9/9 planned R_garage words, no duplicates or borrowed zoom words.
- Gender halves, French articles/plurals, original example pairs and honest hook ratings.
- Separate alpha sprites; item/hotspot separation, 6% asset margins and clear courtyard doorway.
- Conservative label rectangles in the explicit DejaVu Serif fallback font; no overlaps with other labels/assets/door.
- Every source sprite and final composition proof visually inspected independently.
- JavaScript syntax, Python package checker and `git diff --check` pass.
- Independent map review confirms the upper-right outbuilding polygon is separate from the windmill and market. Normal map routing, lazy-loaded garage data, main-entry stylesheet and return-door wiring pass static checks. The hover tag is inset to avoid right-edge clipping.

## Not checked / release limits

- Actual browser interaction, fullscreen and phone rendering: no browser binary was available; the Chromium download returned an invalid archive. The proof is a deterministic composition, not a browser screenshot.
- Exact browser font metrics, every live-site control, whole-palace CLIP similarity and full-site release gates remain unverified. Canonical historical gate tools named by the skill are absent from this checkout.
- The existing top-strip Home and Back controls were not globally redesigned. The village map now links its small stone outbuilding beside the windmill to `#/garage`; the room door returns to the map. The standalone `garage-preview.html` entry is also retained.
- The user reviewed the direction during work and explicitly authorized merge. No further approval is pending. Browser limits above remain documented.

## Reviewed proof hashes

- `room-proof.jpg`: `dbde543738551b818beff5a26f714362f4e302dc80e62a805eac86a10b784b29`
- `item-crops.jpg`: `5a644eb18caa1814ad10d3d7e29637fb61142a20ecb4693d7d35c0f48e6ba811`
