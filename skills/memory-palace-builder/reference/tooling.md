# Tooling and token economy

Read when setting up scripts, data edits, worker split or review loops.

## Save tokens with tooling

- Store content in data files and generate pages from templates rather than hand-writing each room. <!-- B79 -->
- Write small scripts for: validating data (missing fields, duplicates, room size limits, placement rules), checking text fits signs (measure text against sign boxes), checking links (every room reachable and links back), and building the site. <!-- B80 -->
- Batch-generate items from the data file and only hand-review the flagged ones. <!-- B81 -->
- **Cheap checks before eyes.** Run the automated checks first (`tools/precheck.py`: OCR text flags, label/box overlap and contact, manifest counts), fix every FAIL, then review visually from ONE downscaled contact sheet per room (`tools/contact_sheet.py`) and open full-size crops only where the sheet raises a doubt. See the release-gates reference/tools-and-logs.md. <!-- N3 -->
- **Reuse one worker per workstream.** Keep one worker (helper agent) per workstream, such as one building's repaint, the hooks merge or the deploy pack, and give it the next task in that stream instead of starting a fresh worker that has to re-read the skills, data and history. <!-- N7 -->

## Data edits

- **Units and overlap.** Know which files store boxes in px and which in %. A wrong-unit edit silently moves a hotspot. After every box edit, re-run the placement and pairwise-overlap check. <!-- B226 -->
- **Tooling hygiene.** Use a new filename for every view crop, because image reads can be cached by path. Build the pack from the uncommitted working tree before committing, and pass building lists in the form the packer expects (here comma-separated). An empty pack means the order or the list format was wrong. Supersede it with a new READY line; don't edit history. <!-- B237 -->
