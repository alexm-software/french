#!/usr/bin/env python3
"""Validate a building's hub tree and physical paths; print a room brief or walk."""
import argparse
from collections import deque
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text_fields(obj, fields, label):
    require(isinstance(obj, dict), f"{label}: expected an object")
    for key in fields:
        require(isinstance(obj.get(key), str) and obj[key].strip(), f"{label}: missing {key}")


def shortest_walk(graph, start, goal):
    """Find a route through physical edges only."""
    previous = {start: None}
    queue = deque([start])
    while queue and goal not in previous:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in previous:
                previous[neighbor] = node
                queue.append(neighbor)
    require(goal in previous, f"no painted route from {start} to {goal}")
    path = [goal]
    while previous[path[-1]] is not None:
        path.append(previous[path[-1]])
    return list(reversed(path))


def validate(plan, layout, map_data):
    """Check ownership, reciprocal passage bindings and entry/return reachability."""
    building, entry = layout["building"], layout["main"]
    rooms, places = layout["rooms"], plan["places"]
    require(plan.get("version") == 1, "walkthrough version must be 1")
    require(set(places) == {key for key, room in rooms.items() if not room.get("parent")},
            "walkthrough places must match all ordinary layout rooms")
    require(entry in places, "layout main must be an ordinary room")
    text_fields(plan["entrance"], ("where", "appearance", "arrival"), "sector entrance")
    require(rooms[entry].get("mapExit"), "entry needs a painted return to its sector")
    sector = next((s for s in map_data["world"]["sectors"] if s["id"] == layout.get("sector_id")), None)
    require(sector is not None, "building sector is missing from the overview")
    map_sector = map_data["sectors"][sector["slug"]]
    entries = map_sector["buildings"] + map_sector.get("streets", [])
    def map_id(row):
        if row.get("id"):
            return row["id"].lower()
        return row["building_id"].partition("_")[2]
    href = rooms[entry]["mapExit"].get("href")
    require(not href or href == f"#/quartier/{sector['slug']}", "entry return must target its owning sector")
    entrance = [row for row in entries if map_id(row) == building]
    require(len(entrance) == 1, f"{building}: expected one entrance on sector {sector['slug']}")

    parents = {}
    for key, place in places.items():
        text_fields(place, ("level", "landmark", "camera"), key)
        require(place.get("kind") in ("hub", "room"), f"{key}: kind must be hub or room")
        parent = place.get("within")
        if key == entry:
            require(place["kind"] == "hub" and parent is None, "entry must be the root building hub")
        else:
            require(parent in places and places[parent].get("kind") == "hub",
                    f"{key}: within must name an existing hub")
            parents[key] = parent
    ancestors = {}
    for key in places:
        seen = {key}
        current = key
        while current != entry:
            current = parents[current]
            require(current not in seen, f"{key}: hub ownership cycle")
            seen.add(current)
        ancestors[key] = seen

    edges = {}
    graph = {key: [] for key in places}
    for ident, passage in plan["passages"].items():
        text_fields(passage, ("kind", "appearance"), ident)
        require(passage["kind"] in ("door", "gate", "arch", "path", "stairs", "ramp", "lift", "bridge"),
                f"{ident}: unknown passage kind")
        ends = passage.get("ends", [])
        require(isinstance(ends, list) and len(ends) == 2, f"{ident}: requires two endpoints")
        for end in ends:
            text_fields(end, ("place", "where", "arrival"), ident)
            require(end["place"] in places, f"{ident}: endpoint must name an ordinary place")
        a, b = (end["place"] for end in ends)
        require(a != b, f"{ident}: cannot connect a place to itself")
        reason = passage.get("one_way_reason")
        if "one_way_reason" in passage:
            text_fields(passage, ("one_way_reason",), ident)
        for pair in [(a, b)] if reason else [(a, b), (b, a)]:
            require(pair not in edges, f"{ident}: duplicate physical edge {pair}")
            edges[pair] = ident
            graph[pair[0]].append(pair[1])
    actual = []
    for key, room in rooms.items():
        require(key == entry or not room.get("mapExit"), f"{key}: additional sector exits need an explicit boundary plan")
        for door in room.get("doors", []):
            require(door.get("building", building) == building,
                    f"{key}: cross-building door requires a shared plan outside this building")
            actual.append((key, door["to"]))
        if room.get("parent"):
            require(room["parent"] in places, f"{key}: zoom parent must be an ordinary place")
            parent = rooms[room["parent"]]
            require(sum(z["to"] == key for z in parent.get("zooms", [])) == 1,
                    f"{key}: zoom must be attached once to its parent")
        for zoom in room.get("zooms", []):
            require(rooms.get(zoom["to"], {}).get("parent") == key,
                    f"{key}: zoom {zoom['to']} has no matching parent")
    require(len(actual) == len(set(actual)), "layout contains duplicate door edges")
    require(set(edges) == set(actual),
            f"passage/layout mismatch: missing doors {sorted(set(edges) - set(actual))}; unplanned doors {sorted(set(actual) - set(edges))}")
    for hub, place in places.items():
        if place["kind"] != "hub":
            continue
        scope = {key for key in places if hub in ancestors[key]}
        local = {key: [dest for dest in graph[key] if dest in scope] for key in scope}
        for key in scope:
            shortest_walk(local, hub, key)
            shortest_walk(local, key, hub)

    root = f"{building}/{entry}"
    sector_node = f"sector:{sector['slug']}"
    nodes = {"overview": {"kind": "hub"},
             sector_node: {"kind": "hub", "within": "overview"}}
    for key, place in places.items():
        nodes[f"{building}/{key}"] = {
            "kind": place["kind"],
            "within": sector_node if key == entry else f"{building}/{parents[key]}",
        }
    for key, room in rooms.items():
        if room.get("parent"):
            nodes[f"{building}/{key}"] = {"kind": "zoom", "within": f"{building}/{room['parent']}"}
    return {"entry": root, "sector": sector_node, "nodes": nodes, "hubParents": parents,
            "edges": edges, "graph": graph,
            "sector_image": map_sector["image"], "sector_box": entrance[0]["rect"]}


def room_brief(key, plan, layout, model):
    room = layout["rooms"][key]
    place = room.get("parent") or key
    connections = []
    for passage_id, passage in plan["passages"].items():
        a, b = passage["ends"]
        if b["place"] == place:
            a, b = b, a
        if a["place"] == place:
            connections.append({"id": passage_id, "kind": passage["kind"],
                                "appearance": passage["appearance"], "here": a, "there": b,
                                "neighbor_image": layout["rooms"][b["place"]]["image"],
                                **({"one_way_reason": passage["one_way_reason"],
                                    "direction": [end["place"] for end in passage["ends"]]}
                                   if passage.get("one_way_reason") else {})})
    result = {"room": key, "place": plan["places"][place], "passages": connections,
              "walk_in": shortest_walk(model["graph"], layout["main"], place),
              "walk_out": shortest_walk(model["graph"], place, layout["main"])}
    if place == layout["main"]:
        result["sector_entrance"] = plan["entrance"]
    if place != key:
        result["zoom_parent_image"] = layout["rooms"][place]["image"]
        result["zoom_parent_box"] = next(z["obj"] for z in layout["rooms"][place]["zooms"] if z["to"] == key)
    return result


def covering_walk(layout, model):
    entry = layout["main"]
    walk = [entry]
    seen = set()
    def visit_zooms(key):
        if key in seen:
            return
        seen.add(key)
        for zoom in layout["rooms"][key].get("zooms", []):
            walk.extend((zoom["to"], key))

    def advance(key):
        walk.append(key)
        visit_zooms(key)

    visit_zooms(entry)
    for a, b in model["edges"]:
        for step in shortest_walk(model["graph"], walk[-1], a)[1:]:
            advance(step)
        advance(b)
    for step in shortest_walk(model["graph"], walk[-1], entry)[1:]:
        advance(step)
    return ["overview", model["sector"], *(f"{layout['building']}/{key}" for key in walk),
            model["sector"], "overview"]


def load_model(root, layout):
    path = root / "content" / "v2" / layout["building"] / "walkthrough.json"
    if not path.is_file():
        return None
    return validate(read_json(path), layout, read_json(root / "content/v2/map.json"))


def passage_sheet(plan, layout, model, output):
    """Pair the painted endpoints for visual review without rebuilding art or cards."""
    from PIL import Image, ImageDraw, ImageOps

    rooms = layout["rooms"]
    entry = layout["main"]
    pairs = [("sector entrance", [(model["sector"], model["sector_image"], model["sector_box"]),
                                  (entry, rooms[entry]["image"], rooms[entry]["mapExit"]["box"])])]
    for ident, passage in plan["passages"].items():
        tiles = []
        for here, there in (passage["ends"], reversed(passage["ends"])):
            key = here["place"]
            room = rooms[key]
            door = next((door for door in room.get("doors", []) if door["to"] == there["place"]), None)
            label = key if door else f"{key} (one-way arrival)"
            tiles.append((label, room["image"], door["hit"] if door else None))
        pairs.append((ident, tiles))
    canvas = Image.new("RGB", (1000, 225 * len(pairs)), "#f5f3ed")
    draw = ImageDraw.Draw(canvas)
    for row, (ident, tiles) in enumerate(pairs):
        y = row * 225
        draw.text((12, y + 5), ident, fill="black")
        for col, (label, image, box) in enumerate(tiles):
            x = col * 500 + 12
            draw.text((x, y + 23), label, fill="black")
            with Image.open(ROOT / "village" / image) as source:
                if box:
                    left, top, width, height = box
                    source = source.crop((left, top, left + width, top + height))
                tile = ImageOps.contain(source.convert("RGB"), (474, 178))
                canvas.paste(tile, (x, y + 40))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, quality=92)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("building", help="v2 building slug")
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--room", help="emit compact two-sided painting brief for this room")
    output.add_argument("--walk", action="store_true", help="emit a covering walk with returns")
    output.add_argument("--tree", action="store_true", help="emit the hub ownership tree")
    output.add_argument("--sheet", type=Path, help="write paired crops of actual passage endpoints")
    args = parser.parse_args()
    folder = ROOT / "content" / "v2" / args.building
    try:
        layout = read_json(folder / "layout.json")
        plan = read_json(folder / "walkthrough.json")
        model = validate(plan, layout, read_json(ROOT / "content/v2/map.json"))
        if args.room:
            result = room_brief(args.room, plan, layout, model)
        elif args.walk:
            result = covering_walk(layout, model)
        elif args.tree:
            result = model["nodes"]
        elif args.sheet:
            passage_sheet(plan, layout, model, args.sheet)
            print(args.sheet)
            return
        else:
            print(f"{args.building}: {len(model['nodes'])} places including map hubs, {len(plan['passages'])} passages checked")
            return
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        parser.exit(1, f"FAIL {args.building}: {error}\n")


if __name__ == "__main__":
    main()
