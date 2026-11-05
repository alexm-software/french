# Plan walkable hubs and rooms before painting

The overview and sector maps are hubs. A building's entrance is its root hub. Add a local hub when a real courtyard, landing or corridor gives access to a floor or wing. A hub can also teach words. Use a circulation-only hub when a passage needs space without vocabulary.

## Author two relationships

Use one `walkthrough.json` beside the building's `layout.json`. The castle example is `content/v2/contes/walkthrough.json`.

- **Ownership** is a tree. The overview owns sectors, a sector owns building entrances, and a building or local hub owns places. The map registry supplies the first two levels. Each ordinary place has a `kind` of `hub` or `room`, a `within` hub except at the root, plus `level`, `landmark`, and `camera`. Layout `main` identifies the root. A zoom belongs to its layout parent and uses that parent's actual crop.
- **Travel** is a graph. Write each passage once under `passages`, with a stable ID, `kind`, shared `appearance`, and two `ends`. Each end names its `place`, architectural location in `where`, and the landmark in `arrival`. Supply a reason only for an intentional one-way passage, whose first endpoint is the origin. The separate `entrance` record names the sector threshold with the same location, appearance and arrival facts.

Each building plan starts with `version: 1`. Keep vocabulary, click geometry and image paths in their existing sources. Layout doors bind the visual hit regions to the planned endpoints. The checker rejects missing or extra door edges, unreachable descendants, ownership cycles and missing returns. Each local hub needs routes out and back to its descendants **inside its own subtree**. New shared plans cover buildings with one sector threshold. Cross-building doors and additional sector exits in legacy layouts still use their existing behavior.

## Build in this order

1. Group assigned words into room activities. Choose a footprint, floor levels and recognizable landmarks. Block out the entrance, junctions and routes on a top-down floor plan. Keep doors on the correct architectural wall when the camera rotates.
2. Draft the layout with room IDs, intended image paths and links. Write the walkthrough, then check it before any finished art. Run the reusable commands from the repo root.

```sh
python3 skills/memory-palace-builder/scripts/walkthrough.py contes
python3 skills/memory-palace-builder/scripts/walkthrough.py contes --tree
python3 skills/memory-palace-builder/scripts/walkthrough.py contes --walk
python3 skills/memory-palace-builder/scripts/walkthrough.py contes --room cour_chateau
python3 skills/memory-palace-builder/scripts/walkthrough.py contes --sheet /tmp/castle-passages.jpg
```

3. Use the room brief's neighbor image references on both sides of a passage. Keep the frame, opening direction, step count where relevant, materials and glimpse consistent. Match what the visitor sees on arrival. For a zoom, check the actual parent's shape, contents and orientation. Render one representative hub/room pair before expanding.
4. Compile the room manifest with `tools/build_prompt.py` and `--layout`. The compiler inserts shared passage cues from the walkthrough. Use `prompt.kind: hub`, `items: []` and `interactions: []` for a circulation-only view with planned doors. A teaching hub uses ordinary item requirements.
5. Fit the draft against the actual image, then inspect the generated walk. It covers every directed passage and each zoom return. Verify actual thresholds, destination glimpses and arrival landmarks visually. Revisit both ends when a shared feature changes.

The build emits compact `hubParents` metadata. The single Hub shortcut goes to the nearest containing hub in opted-in buildings. Back retains its sector/street or zoom-parent behavior. Check the walk through painted connections separately from these shortcuts.
