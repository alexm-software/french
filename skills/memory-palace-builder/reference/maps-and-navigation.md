# Overview, regions and connected views

Read for map/exterior authoring or changes to physical routes. Use `building-walkthrough.md` for interior floor plans and hubs; `site-ui.md` owns current Back/Hub controls.

## Give each view a job

| View | Purpose | Must agree with |
|---|---|---|
| Village overview | Recognize regions and the roads/water connecting them | Every sector's footprint, buildings and landmarks |
| Region/sector | Walk streets/paths, recognize buildings and choose entrances | Its overview miniature, adjacent sectors and building exteriors |
| Building entrance/main room | Establish arrival, function and routes into the building | Exterior entrance, footprint, floors and interior plan |
| Local hub/landing | Orient at an actual floor/wing junction where useful | Adjacent doors, stairs and room landmarks |
| Activity room | Learn its vocabulary in a distinctive shared situation | Building plan, neighboring views, style and word manifest |
| Zoom | Inspect a real local cluster more closely | The actual parent crop's object, orientation and contents |

A hub is an ordinary physical scene with a navigation role, not a mandatory extra map layer. Do not force a small building through an empty lobby or force every interior trip back through its entrance.

## Author the structure before the views

1. Establish the region footprints, roads, terrain/water, building positions, silhouettes and entrances in one spatial plan. Every room belongs to one building and every building to one sector; stable IDs/names agree across plans, map labels, cards and translations.
2. Group building vocabulary into room activities, then plan floors, neighbors, shared passages and optional hubs using `building-walkthrough.md`. Check the complete walk before painting individual rooms.
3. Draft representative connected views: sector/exterior/entrance and main room/zoom. Fix topology and identity discrepancies before finished images.
4. Paint detailed regions and connected interior scenes using the shared plan and references. Compose the overview from those approved region references in one integrated painting. Use rough maps as planning evidence; do not paint detailed levels independently and hope they match.
5. Review every parent/child and adjacent pair, then browser-walk every branch. After a shared feature changes, review all views showing it.

## Map continuity and expansion

The overview is a zoomed-out view of the same world: same building count/arrangement, recognizable silhouettes, names, entrances, paths, waterways, terrain, season and materials. Minor props may disappear at distance; buildings may not. A generic college standing in for a multi-building campus fails. Building exteriors show their function and visually support the interior's scale and floors.

Compare actual overview crops with sectors, exterior with arrival view, and zoom with parent crop. Keep the overview one coherent painting: continuous roads, water, scale, perspective and light across region boundaries. Do not assemble pasted tiles. Repaint inconsistent overview content as one integrated scene from the complete reference/layout guide; retain only coherent regional edits.

Expand approved maps outward at the existing scale rather than squeezing, shrinking or shifting approved districts. Roads and water continue naturally through the extension. Roads have a clear main-road/lane/footpath hierarchy, natural T/Y junctions and terrain-following curves. Every route has a real destination; no decorative ribbon loops, roads into water without bridges, or straight roads up mountains. Inspect the painted routes, not only the graph.

## Passage and reachability acceptance

Check all targets exist and that every place is reachable from the village start and can return. The physical route must work without relying on Back/Hub shortcuts; an ordinary terminal room with an obvious return is valid. Match visible passage design, architectural position, floor and destination glimpse at both ends. Camera rotation can change a doorway's screen edge; the floor-plan relationship must remain consistent.

Use real doors/arches/stairs inside and paths/gates/bridges outside. Only ground-floor entrances go outside; upper/cellar floors use stairs that point the correct way at both ends. Windows are views, never exits. Never draw a freestanding door in open ground to fake a route. Each region connects to the overview and real neighboring regions where paths meet.

Click areas cover the painted passage, not just its label, and avoid word boxes. Cues must read with highlights off: destination name on hover/focus/first tap and a clear walking badge distinct from the zoom magnifier. Suppress duplicate visible controls to the same destination. A sign or room list is not a physical passage. Click every route in desktop/mobile/fullscreen and confirm arrival, return and destination cues against the plan.
