# Treasury generation — not accepted (2026-11-07)

`GenerateImage` is available and was used. No candidate is installed. Live `village/eglise/tresor.jpg` is unchanged. Choir and parish-hall paintings were not edited, because neither treasury candidate is a scene those doors can match yet.

## Hook decisions (agent, not a user signature)

Recorded in `HOOK_FORM.tsv`.

- custode: one billiard cue stood beside the pyx. `stood` is near `/tɔd/`, not exact.
- culpabiliser: stem CULPABLE only. A full five-syllable pun would be more than two chunks.
- prôner: golf club + neighing toy horse. `pro` + `neigh` matches `proh-NAY`.
- ambon: a trombone a step away, not a ham bone and not touching the lectern. `trom-` is an extra syllable; the stressed `-bohn` is the rhyme.
- missel: one dry-cell battery. Stressed `SEHL` matches `cell`. The first syllable is not given a second pun.

## What was generated

| File | SHA-256 | Result |
|---|---|---|
| candidate-01.jpg | `2f409971a7c036701985d7160c0d989011b383af034d8af1f82abe43418c3b7c` | Centered altarpiece, extra mimes, halos on the embroiderer and the king, duplicate boar, parish door was a poster. |
| candidate-02.jpg | `60da052ef20aa2b0f00443f234680b8b522bb34fdbff01757915de792fe7a65d` | Repair of 01. Altarpiece stayed centered. Halos mostly gone. Parish glimpse gained people and a candle, but `LE TRÉSOR` is on that poster. Ring landed on the book. Trombone disappeared. |
| candidate-03.jpg | `7049ca900d83aa2e943fbb1eb67cb7091b95a4670e465289ebc7a5690233a732` | Recompose, no reference image. Altarpiece is on the right wall. Center is a window. Sign, green-chasuble glimpse, parish glimpse, battery, boar, golf club, and trombone are present. Fails: six mimes (the ladder man wears a red beret), three books, horse is only a head, guilt mime rests his chin, no clear billiard cue, king holds a cross, ring is inspected rather than gilded. |
| candidate-04.jpg | `12fe5803458bc476a487088c97af016012273036397020e53731355b4319e7fc` | Repair of 03. Ladder man is correctly in white. Altarpiece stays on the right. Collateral: the presenting, gilding, and lectern mimes lost their striped shirts. Books, horse head, chin-on-hand, and the king's cross remain. |

Stopped here. Another patch of 04 would be a third edit of this composition. 2× quadrants of each candidate were inspected. This is not an independent sign-off, and it is not an acceptance.

## Next generation, for a fresh budget

Use `prompt-recompose.txt` (337 words) and add this block at the top. Do not attach candidate 01 or 02. Attaching 03 is optional and only if the striped-shirt line is explicit.

Every mime wears a black-and-white striped shirt, a beret, suspenders, and white gloves. The ladder restorer alone wears white, with no beret. Exactly five mimes. Exactly two books in the crate. The guilt mime covers his mouth with both hands. The horse is a whole toy horse. One billiard cue stands beside the nun. The king holds nothing: no cross, no halo. The brass ring is on a stand and is gilded with a brush. The trombone does not touch the reading stand.

Door paint-backs on `choeur` and `salle` wait until a treasury candidate passes.
