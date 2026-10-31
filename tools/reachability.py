#!/usr/bin/env python3
"""Whole-site reachability check for the village (static, mirrors village/app.js routing).

BFS from the village entry (#/, the world map) through every link a learner can click on the
painting: world-map sector pins, sector-map building doors, room doors (incl. cross-building
`building` doors), zoom badges and the painted mapExit. Then a reverse check: from every
reached space, can the learner get back to the village entry?

Edge kinds
  map      world -> sector pin, sector -> live building door, sector Back -> world
  door     a painted room door (doors[].hit)                      - painted
  mapexit  the painted way out to the sector map (mapExit.box)    - painted
  zoom     a zoom badge into a close-up                           - painted
  zoomback Back button of a close-up (zooms have no painted exit by design)
  backbtn  Back button of a room (street for street side rooms / sector map; gate 19)            - UI only, not painted
  tab      the roomList tab bar                                   - UI only, not painted

A space FAILS when
  UNREACHABLE  no path from #/ using map/door/mapexit/zoom edges (the tab bar and Back
               button do not count: a space only reachable that way has no painted way in)
  NO-WAY-BACK  no path back to #/ using map/door/mapexit/zoomback edges
  BROKEN-LINK  a door/zoom/mapExit points at a room or building the router would reject
WARN lines: ORPHAN-DATA (a room key nobody links to, not even the tab bar), TAB-ONLY (reachable
only through the tab bar / Back button), ONE-WAY door (A->B painted, no painted B->A).

Usage: python3 tools/reachability.py [--root village] [--json out.json] [--building lycee]
Exit 1 if any FAIL.
"""
import argparse, collections, glob, json, os, re, sys

def load_js(path):
    s = open(path, encoding='utf-8').read()
    i = s.index(']=') + 2 if '"]=' in s[:200] else s.index('=') + 1
    return json.loads(s[i:].strip().rstrip(';'))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'village'))
    ap.add_argument('--json')
    ap.add_argument('--building', help='only print lines for this building id')
    ap.add_argument('--door-sheet', help='write a contact sheet (jpg) of every door hit, flattest first, for the '
                    'human "is this a painted door/stairs?" review (static data cannot tell paint from wall)')
    ap.add_argument('--sheet-max', type=int, default=48)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    MAP = load_js(os.path.join(root, 'data', 'map.js'))
    # registry exactly like app.js
    REG, BYBID, SECT = {}, {}, {}
    for w in MAP['world']['sectors']:
        S = MAP['sectors'][w['slug']]; SECT[w['id']] = w['slug']
        for b in S.get('buildings', []):
            bid = b.get('id') or re.sub(r'^B\d+_', '', b['building_id'])
            e = dict(b, id=bid, sector=w['slug']); REG[bid] = e; BYBID.setdefault(b['building_id'], e)
        for t in S.get('streets', []):
            t_bid = t.get('building_id') or t['id']; tid = t_bid.lower()
            e = dict(t, id=tid, building_id=t_bid, sector=w['slug'], street=1); REG[tid] = e; BYBID.setdefault(t_bid, e)
    DATA = {}
    for f in sorted(glob.glob(os.path.join(root, 'data', '*.js'))):
        k = os.path.basename(f)[:-3]
        if k in ('map',): continue
        try:
            d = load_js(f)
        except Exception as ex:
            print('FAIL  BAD-DATA', f, ex); continue
        DATA[k] = d
    LIVE = [k for k in REG if k in DATA]   # probeAll: only registry ids are ever loaded
    for k in DATA:
        if k not in REG: print('WARN  NOT-IN-REGISTRY data/%s.js (never loaded by the app)' % k)
    def home(bld):
        D = DATA.get(bld); e = REG.get(bld)
        if D and D.get('building_id') in BYBID and BYBID[D['building_id']]['id'] == bld: e = BYBID[D['building_id']]
        slug = SECT.get(D.get('sector_id')) if D else None
        return slug or (e and e['sector'])
    def route_ok(bld, key):
        """app.js route(): would #/bld/key render?"""
        if bld not in REG or bld not in DATA: return False
        D = DATA[bld]; R = D['rooms'].get(key)
        if not R: return False
        if key == bld: return True
        if R.get('parent'): P = D['rooms'].get(R['parent']); return bool(P) and not P.get('parent')
        return any(r['key'] == key for r in D.get('roomList', []))
    def href(bld, key): return '#/' + bld if key == bld else '#/' + bld + '/' + key
    E = collections.defaultdict(list)   # node -> [(dst, kind, detail)]
    fails, warns = [], []
    W = '#/'
    for w in MAP['world']['sectors']:
        sh = '#/quartier/' + w['slug']
        E[W].append((sh, 'map', 'world pin')); E[sh].append((W, 'map', 'sector Back'))
    for bld in LIVE:
        slug = home(bld); sh = '#/quartier/' + slug if slug else W
        if bld not in DATA[bld]['rooms']:
            fails.append(('BROKEN-LINK', href(bld, bld), 'sector door #/%s but data has no room "%s"' % (bld, bld))); continue
        E[sh].append((href(bld, bld), 'map', 'sector door'))
    nodes = {}
    for bld in LIVE:
        D = DATA[bld]
        for key, R in D['rooms'].items():
            n = href(bld, key); nodes[n] = (bld, key)
            if not route_ok(bld, key):
                warns.append(('ROUTE-REJECTS', n, 'app.js route() would bounce this URL to #/ (sub-room not in roomList / bad parent)'))
            for d in R.get('doors') or []:
                tb = d.get('building') or bld; t = href(tb, d['to'])
                if not route_ok(tb, d['to']): fails.append(('BROKEN-LINK', n, 'door -> %s (router rejects)' % t)); continue
                E[n].append((t, 'door', d.get('label', '')))
            for z in R.get('zooms') or []:
                t = href(bld, z['to'])
                if not route_ok(bld, z['to']): fails.append(('BROKEN-LINK', n, 'zoom -> %s (router rejects)' % t)); continue
                E[n].append((t, 'zoom', z.get('label', '')))
            if R.get('mapExit'):
                slug = home(bld); t = R['mapExit'].get('href') or ('#/quartier/' + slug if slug else W)
                E[n].append((t, 'mapexit', R['mapExit'].get('label', '')))
            # gate 19: Back goes straight outside (zoom -> its room; street side room -> the street; else the map)
            BT = R.get('parent') or (D['main'] if str(D.get('building_id', '')).startswith('ST_') and key != D['main'] else None)
            if BT and BT in D['rooms']:
                E[n].append((href(bld, BT), 'zoomback' if R.get('parent') else 'backbtn', 'Back'))
            elif not BT:
                slug = home(bld); E[n].append(('#/quartier/' + slug if slug else W, 'backbtn', 'Back'))
            if len(D.get('roomList', [])) > 1 and not R.get('parent'):
                for r in D['roomList']:
                    if r['key'] != key and r['key'] in D['rooms']: E[n].append((href(bld, r['key']), 'tab', r.get('short', '')))
    def bfs(start, kinds, rev=False):
        G = collections.defaultdict(list)
        for s, lst in E.items():
            for t, k, _ in lst:
                if k in kinds: (G[t] if rev else G[s]).append(s if rev else t)
        seen = {start}; q = collections.deque([start])
        while q:
            u = q.popleft()
            for v in G[u]:
                if v not in seen: seen.add(v); q.append(v)
        return seen
    PAINT_IN = {'map', 'door', 'mapexit', 'zoom'}
    PAINT_OUT = {'map', 'door', 'mapexit', 'zoomback'}
    fwd = bfs(W, PAINT_IN)
    fwd_any = bfs(W, PAINT_IN | {'tab', 'backbtn', 'zoomback'})
    back = bfs(W, PAINT_OUT, rev=True)
    for n, (bld, key) in sorted(nodes.items()):
        if n not in fwd:
            how = 'only via tab bar/Back button' if n in fwd_any else 'not even via the tab bar'
            fails.append(('UNREACHABLE', n, 'no painted way in (%s)' % how))
        if n not in back:
            fails.append(('NO-WAY-BACK', n, 'no painted door/mapExit (or zoom Back) path back to the village'))
    # one-way painted doors between non-zoom rooms
    pdoor = {(s, t) for s, l in E.items() for t, k, _ in l if k == 'door'}
    for s, t in sorted(pdoor):
        if (t, s) not in pdoor and t in nodes and not DATA[nodes[t][0]]['rooms'][nodes[t][1]].get('parent'):
            warns.append(('ONE-WAY', s, 'door -> %s has no painted door back' % t))
    linked = {t for l in E.values() for t, k, _ in l}
    for n in nodes:
        if n not in linked and n != href(*[nodes[n][0]] * 2): warns.append(('ORPHAN-DATA', n, 'no link of any kind points here'))
    flt = (lambda n: n.startswith('#/' + a.building + '/') or n == '#/' + a.building) if a.building else (lambda n: True)
    for k, n, m in sorted(set(fails)):
        if flt(n): print('FAIL  %-12s %-34s %s' % (k, n, m))
    for k, n, m in sorted(set(warns)):
        if flt(n): print('WARN  %-12s %-34s %s' % (k, n, m))
    print('spaces %d · painted-reachable %d · can-return %d · FAIL %d · WARN %d · live buildings %d'
          % (len(nodes), len(fwd & set(nodes)), len(back & set(nodes)), len(set(fails)), len(set(warns)), len(LIVE)))
    if a.door_sheet:
        door_sheet(root, DATA, LIVE, a.door_sheet, a.sheet_max, a.building)
    if a.json:
        json.dump({'fails': sorted(set(fails)), 'warns': sorted(set(warns)), 'spaces': sorted(nodes),
                   'edges': {s: l for s, l in E.items()}}, open(a.json, 'w'), indent=1, ensure_ascii=False)
    return 1 if fails else 0

def door_sheet(root, DATA, LIVE, out, nmax, only=None):
    """Crop each door hit with 40px context, outline the hit, sort by edge density (flattest first:
    blank walls score low). The score is only a sort key - a reviewer decides."""
    from PIL import Image, ImageDraw, ImageFilter, ImageStat
    rows = []
    for bld in LIVE:
        if only and bld != only: continue
        for key, R in DATA[bld]['rooms'].items():
            p = os.path.join(root, R['image'])
            if not os.path.exists(p) or not R.get('doors'): continue
            im = Image.open(p).convert('RGB').resize((1280, 720)); ed = im.convert('L').filter(ImageFilter.FIND_EDGES)
            for d in R['doors']:
                x, y, w, h = d['hit']
                sc = ImageStat.Stat(ed.crop((x, y, x + w, y + h))).mean[0]
                rows.append((sc, bld, key, d, im))
    rows.sort(key=lambda r: r[0]); rows = rows[:nmax]
    T = 300; cols = 6; sheet = Image.new('RGB', (cols * T, ((len(rows) + cols - 1) // cols) * (T + 30)), 'white')
    dr = ImageDraw.Draw(sheet)
    for i, (sc, bld, key, d, im) in enumerate(rows):
        x, y, w, h = d['hit']; m = 40
        box = (max(0, x - m), max(0, y - m), min(1280, x + w + m), min(720, y + h + m))
        c = im.crop(box).copy(); ImageDraw.Draw(c).rectangle([x - box[0], y - box[1], x - box[0] + w, y - box[1] + h], outline=(255, 0, 0), width=3)
        c.thumbnail((T, T)); X, Y = (i % cols) * T, (i // cols) * (T + 30)
        sheet.paste(c, (X, Y)); dr.text((X + 2, Y + T + 2), '%s/%s->%s e=%.0f' % (bld, key, d.get('building', '') + d['to'], sc), fill='black')
    sheet.save(out, quality=85); print('door sheet:', out, len(rows), 'doors')

if __name__ == '__main__':
    sys.exit(main())
