# Course correction — three layout attempts, none accepted

Independent review of `d10e421c` stands. Mouse anatomy passes. The reddish shape is the near ear. No cat and no stool. The stone and the water-jetty are recognizable. The jetty does not touch the stone. The sack intersects the stone-and-pier group. The man's box encloses the crystal. Margins fail. Mine, mineral, the sole and worm, anatomy, and the faculty door pass.

This run made three fresh paintings. Stated calls are now 30. Repairs: 0. Ready: 0/30. None is accepted.

| try | image | prompt | result |
|---|---|---|---|
| 1 split | `ccd2bb0635c4cd4732e6dce4f41f2642c8f8895858f808cdbed0dc7012b31408` | `ac3845c7be4bf70d5227e7607c16e3d6a8447956a406a9570b3448b49c5d4070` | Crystal is above the man and the mouse holds the crystal. The stone is solid. A second sack sits on the stone group because the stone-and-pier reference still showed the sack. The jetty does not touch the stone. |
| 2 one sack | `d4eab32d0260356d48ec2be00c77c3f92c5c3bbf850b8d88d172e40c3d1a3a3e` | `c8f3264828e32250f1683f2973e14dcc583319ce2c02a1050b5748293c8404c8` | A blank diagram panel returns. The stone has a hole. The sole leaves the tray. |
| 3 continuous | `b09bc144ebe933cc275c728cd7b1efd758edd853e8b4cef212f87694856c4ab6` | `951a8bd75454a75dfb871ed66a6f315c3449463358c183fae0460767c5b8db5d` | One room, one sack, the mouse holds the crystal, and the man is below it. The stone is a block with an opening and a waterfall. Both boots stay on the floor. The worm is alone in the tray. |

Faculty crop on every call: `e5212a33bc34f13892e042cce5d3e35bfcf31ecf04fc991d90fd7b30f40eb33a`.

## What the inputs did

Putting the jetty against the stone makes the model open a hole and pour water out of it. A separate pan keeps the block solid, and then the jetty does not touch it. A reference crop that still contains the sack paints that sack again. An empty-margin instruction paints a blank panel. Forcing the new spacing without the jetty picture drops the sole out of the tray.

The spacing, the whole cue, and the single helper are already in the compiled rules. These three results are execution. Two-part hooks stay allowed. No new checker was added.

Pendule and creuset stay queued. `village/data/sciences.js` was not built.

The untried input is the full jetty painting as a cue reference, with a move-only instruction that leaves the pier's gap alone and only shrinks the man and lifts the crystal. That was not spent in this run.
