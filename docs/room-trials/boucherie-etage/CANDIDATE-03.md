# Butcher candidate 03 — for independent re-review, not installed

sha256 `bb1ea7377a93fa4582c9be2d689fd44dd1fbb51d70c59c95dba508ae3e77e3a0`

One structural edit of candidate 02 (`6d7a6e8f…`). Same people, foods, blank plaque, and descending stair. The fish, shell, and kite are a separate group from the oyster. The sign, shrimp, plaque, and steak are pulled in from the frame. This is not an acceptance.

2× crops: `/opt/cursor/artifacts/butcher-review/c03-q1.jpg` through `c03-q4.jpg`. Margin guide: `/opt/cursor/artifacts/butcher-review/c03-margin-guide.jpg`.

## Publication, blocked until this image passes review

1. Copy the accepted file to `village/boulangerie/poissonnerie.jpg`.
2. Add the room to `content/v2/boulangerie/layout.json` with boxes measured on the painting, not on the old plan.
3. Add a stair in `boucherie.jpg` that goes up to this counter. Do not publish this room with a one-sided door.
4. Add hooks, alt text, and the dialogue below.
5. Rebuild with `python3 scripts/v2/build_v2.py boulangerie`.
6. Bump `village/sw.js` and run the placement checks.
7. Open the PR. Nothing here is live yet.

## Draft dialogue, not live

Mme Roux: Tu manges ici, au-dessus de la boucherie ?
Léa: Oui. Des crevettes, et une huître avec sa perle. Le requin, lui, reste sur la glace.
Mme Roux: Regarde les écailles de ce poisson, et le coquillage à côté.
Léa: Le charcutier coupe le jambon. Mon steak est déjà cuit.
Mme Roux: La plaque là-haut ne montre rien. Tant mieux. On descend ?
