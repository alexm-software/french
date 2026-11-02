# Building walkthrough: plan before painting

Read for a new building, new floor, or changed physical connections. Use the same building/room IDs as the vocabulary and layout. This is an authored planning contract; the current viewer and plan checker do not automatically consume or fully validate it.

## One hierarchy, two kinds of relationship

Overview → region/sector → building entrance → connected interior spaces → local zooms. "Region" and "sector" name the same map level. Each ordinary room belongs to one building and one floor/wing; a zoom belongs to a specific spot in its parent. Hubs are real spaces serving a navigation role, not another mandatory hierarchy level.

Ownership determines where a space belongs; physical adjacency determines where you can walk. A hierarchy tree alone is not a floor plan. A second floor belongs to the building but is reached by stairs, not by clicking the building name.

## Build the plan from the vocabulary

For an entirely new building, register its building/sector and source word-room assignments before running inventory helpers; they cannot find an unregistered provisional ID. A concept plan may precede registration, but inventory verification stays pending until IDs exist.

1. Group assigned words into coherent room activities; include fitting verbs. Give each room a distinct purpose and landmark. Split for theme/readability, not arbitrary numbering. Settle hooks before allocating their space.
2. Choose the entrance from the sector and an architectural footprint/floors that can hold the rooms. Place public/arrival functions near the entrance, related functions together and upper/cellar functions at appropriate levels. Establish the building silhouette at this stage.
3. Draw a simple top-down block plan per floor, then connect the actual doors, stairs and outside paths. Record which wall/side each passage occupies. Show floors and stair endpoints; do not confuse screen-left with architectural west after rotating the camera.
4. Walk the route on paper: enter, visit every room, visit zooms, return from a terminal room and exit. Add natural alternate routes where architecture supports them. A terminal room is fine if its return is obvious; do not force a loop or an outside detour.
5. Choose view anchors and match connections before composing vocabulary figures. Then draft a representative room and its zoom; accept composition before buying finished detail. Review the whole building's distinct silhouettes/layouts together.

## When to use hubs

Small buildings can open straight into the main activity room and connect adjacent rooms directly. Add a foyer, courtyard, corridor or stair landing when it provides a real junction, separates wings/floors or makes branching choices easier to read. Do not use a universal all-doors hall solely to reach a large inventory.

Large buildings can have one main entrance hub and local floor/wing hubs. Each hub has a distinct landmark and only the passages physically adjacent to it. Neighboring rooms still connect directly where appropriate. A local hub is an ordinary painted space reached by walking, not an extra global Hub button.

A circulation-only landing may have no vocabulary. Do not add filler or force room-density/interaction rules onto it. It still needs recognizable architecture, readable exits and visual review. If it teaches words, apply normal room/manifest rules. Current word-painting prompt compilation assumes items; record an empty circulation view as a navigation scene and review it manually rather than inventing word entries to pass the tool.

## Compact building record

Keep one plan beside the building layout; reuse it for every room prompt. Record:
- Building/sector IDs, entry room, footprint, floors/wings and approved exterior/style references.
- Each space's ID, purpose, floor/wing, role (activity/main hub/local hub/circulation), assigned word IDs, landmark, camera direction and zoom parent/spot.
- Each physical connection ONCE: ID, both endpoints, passage kind, wall/side and floor at each end, shared appearance (frame, leaf count/color, material, open state), expected destination glimpse and return. Give a real reason for any intentional one-way connection; routine doors/stairs are bidirectional.
- A short start-to-finish walk covering all spaces; draft/final image references and unresolved decisions.

Map these connections to the actual room doors/zooms in the layout. Never infer targets from a remembered room name or from whichever image happens to exist. Do not duplicate the entire vocabulary payload or verb tables in the plan.

## Paint as connected views

Use each connection's shared description and the neighboring reference in BOTH endpoint prompts. A stair goes up in the lower view and down in the upper view; its landing/materials agree. Door glimpses show the real destination, not a generic invented room. A return doorway need not appear on the same screen edge when cameras differ; its architectural position must still agree with the plan. Keep passages clear of hook groups and labels.

A zoom is closer inspection, not travel into another room; a passage inside it must be explicitly planned. Preserve the actual parent's object, contents and orientation. Changes to an exterior, shared passage, parent or landmark trigger review of every view showing that feature.

## Walk and accept

Verify the full route from the village overview, through the sector and entrance, between adjacent rooms and floors, into zooms and back out. At each transition, confirm the visible destination cue, actual target, reciprocal return and recognizable arrival landmark. Check every branch, not only the main route. A newcomer should be able to explain where they are and how to leave without memorizing an arbitrary click sequence.

Use painted passages for the normal walk. Preserve the current control behavior in `site-ui.md`: ordinary-room Back is an outside shortcut, zoom Back returns to parent, and the single Hub shortcut targets building main. These shortcuts must not conceal missing physical routes. Any future control redesign requires a viewer change and corresponding checks; this plan does not implement one.
