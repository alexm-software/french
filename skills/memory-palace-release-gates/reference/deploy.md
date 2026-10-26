# The deploy pipeline

Read before building any pack or asking for a deploy.

## Batch deploys (v13)

- **One combined pack per batch of rooms.** Group the rooms finished in a work batch into one slim pack (one base SHA, one file list, one CHANGES note, before/after and browser shots kept outside the pack), and ask for one deploy. The deploy reports once, when the batch is live; no per-room deploy pings. <!-- N4 -->
- **Exception kept from gate D:** a user-reported issue or a P0/P1 fix that has passed independent review still ships as its own small hotfix in the next deploy window (it may ride in a batch only if that batch goes out in the same window); it never waits for an unrelated combined build (process.md, G50). "Pack small increments" (B227) now means: keep each batch to the rooms of one work batch. <!-- N4 B227 -->

## Pack rules

- **Hand-off discipline.** When buildings belong to other workers, send them data and hook patches with repaint notes, and don't repaint their art. Pack small increments, each with base SHA, file list, change notes and before/after plus browser shots. <!-- B227 -->
- **Rebuild after every repaint.** If a scene painting changes, rebuild that building's cards and data js with the project's build script in the same pack. A painting shipped with stale cards or zoom thumbnails is a failed pack; it needs a hotfix. <!-- G144 -->
- **Ownership before paint.** Before painting a room, check the other workers' packs and the live site for a more recent repaint of the same file. A pack built on an older version of a repainted image must be dropped and redone on current main, never merged over the newer art. <!-- G148 -->
- **Shared data merges.** When two packs touch the same building's data js or cards, regenerate those files from the merged layout with the build script. Don't hand-merge them. <!-- G149 -->
- **Deploy attachment limit.** Keep every deploy tarball under 25 MB. Keep screenshots and review sheets outside the tarball, and slim any pack that's too big by re-packing without them. <!-- G150 -->
- Tooling hygiene for packs (new filename per view crop, pack from the working tree before committing, building list format, supersede with a new READY line): builder reference/tooling.md.
