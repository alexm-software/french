#!/usr/bin/env python3
"""Gate 25 (release gates): no grid of hook figures.

Reads content/v2/<building>/layout.json and checks the item boxes of each room
(1280x720 frame):
  * baseline : FAIL if more than 3 boxes have their bottoms within 40 px of each other
  * bands    : FAIL if the boxes split into two horizontal bands (two groups of
               >=3 boxes whose bottoms each span <= 80 px, with a clear gap between)
  * rows     : FAIL if the sorted box bottoms have an empty gap of >= 150 px with
               >= 3 boxes on each side (a back row plus a front row, empty middle)
  * depths   : FAIL unless box bottoms fall in at least three depths
               (back <= 420, middle 420-580, front > 580)
Usage: grid_check.py [--root REPO] building[/room] ...   (no args = every room)
Exit 1 if any room fails.
"""
import json, os, sys, glob

WIN, BAND, BACK, FRONT = 40, 80, 420, 580

def check(items):
    bots = sorted(b[1] + b[3] for b in items)
    out = []
    best = max((sum(1 for y in bots if x <= y <= x + WIN), x) for x in bots) if bots else (0, 0)
    if best[0] > 3:
        out.append(f"baseline: {best[0]} boxes end within {WIN}px (y {best[1]}-{best[1]+WIN})")
    n = len(bots)
    for i in range(3, n - 2):
        a, b = bots[:i], bots[i:]
        if a[-1] - a[0] <= BAND and b[-1] - b[0] <= BAND and b[0] - a[-1] > WIN:
            out.append(f"bands: two horizontal bands of box bottoms ({a[0]}-{a[-1]} x{len(a)}, {b[0]}-{b[-1]} x{len(b)})")
            break
    for i in range(3, n - 2):
        if bots[i] - bots[i-1] >= 150:
            out.append(f"rows: empty middle between box bottoms {bots[i-1]} and {bots[i]} ({i} boxes above, {n-i} below)")
            break
    depths = {('back' if y <= BACK else 'front' if y > FRONT else 'middle') for y in bots}
    if len(depths) < 3:
        out.append(f"depths: box bottoms only in {sorted(depths)}")
    return bots, out

def main(argv):
    root = '.'
    if argv[:1] == ['--root']:
        root, argv = argv[1], argv[2:]
    targets = []
    if not argv:
        for f in sorted(glob.glob(os.path.join(root, 'content/v2/*/layout.json'))):
            targets += [(os.path.basename(os.path.dirname(f)), r) for r in json.load(open(f))['rooms']]
    for a in argv:
        bld, _, room = a.partition('/')
        rooms = json.load(open(os.path.join(root, f'content/v2/{bld}/layout.json')))['rooms']
        targets += [(bld, r) for r in ([room] if room else rooms)]
    bad = 0
    for bld, r in targets:
        R = json.load(open(os.path.join(root, f'content/v2/{bld}/layout.json')))['rooms'][r]
        bots, probs = check([it['box'] for it in R.get('items', [])])
        st = 'FAIL' if probs else 'PASS'
        bad += bool(probs)
        print(f"{st}\t{bld}/{r}\tbottoms={bots}" + ''.join('\n\t  ' + p for p in probs))
    print(f"grid_check: {len(targets)} rooms, {bad} fail")
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
