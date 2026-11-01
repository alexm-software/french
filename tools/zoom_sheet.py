#!/usr/bin/env python3
"""Create parent-crop/zoom comparisons and a pending review record.

python tools/zoom_sheet.py --data village/data/lycee.js --out /tmp/lycee-zoom-review
This does not judge visual agreement. Recreate after either image changes.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
from precheck import load_payload
from plan_check import rectangle


def comparisons(data, root, out, room=None):
    out.mkdir(parents=True, exist_ok=True)
    records = []
    rooms = data['rooms']
    if room and room not in rooms:
        raise ValueError(f'unknown parent room: {room}')
    for key, parent in rooms.items():
        if room and room != key:
            continue
        for z in parent.get('zooms', []):
            target = z['to']
            if target not in rooms or not rectangle(z.get('obj')):
                raise ValueError(f'{key}/{target}: missing child or invalid parent pixel crop')
            child = rooms[target]
            if child.get('parent') != key:
                raise ValueError(f'{key}/{target}: child parent disagrees')
            pp, cp = root / parent['image'], root / child['image']
            with Image.open(pp) as im:
                x, y, w, h = z['obj']
                crop = im.convert('RGB').crop((x, y, x+w, y+h))
            with Image.open(cp) as im:
                zoom = im.convert('RGB')
            canvas = Image.new('RGB', (1300, 450), 'white')
            draw = ImageDraw.Draw(canvas)
            draw.text((10, 10), f'{key}: actual parent crop', fill='black')
            draw.text((660, 10), f'{target}: zoom painting', fill='black')
            canvas.paste(ImageOps.contain(crop, (630, 370)), (10, 40))
            canvas.paste(ImageOps.contain(zoom, (630, 370)), (660, 40))
            draw.text((10, 420), 'Compare identity, orientation, contents, materials, layout, lighting and gender sides.', fill='black')
            pair = f'{key}__{target}'
            canvas.save(out / f'{pair}.jpg', quality=92)
            records.append(dict(parent=key, zoom=target, parent_box=z['obj'],
                                parent_image=str(pp), zoom_image=str(cp),
                                parent_sha256=hashlib.sha256(pp.read_bytes()).hexdigest(),
                                zoom_sha256=hashlib.sha256(cp.read_bytes()).hexdigest(),
                                status='pending', reviewer='', notes='', sheet=f'{pair}.jpg'))
    (out / 'continuity.json').write_text(json.dumps(records, indent=2)+'\n')
    return records


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data', required=True)
    ap.add_argument('--out', required=True, help='use a new directory for each revision')
    ap.add_argument('--room', help='parent room key; default all parents')
    a = ap.parse_args()
    records = comparisons(load_payload(a.data), Path(a.data).resolve().parents[1], Path(a.out), a.room)
    print(f'{len(records)} comparison(s); visual verdicts pending in {a.out}/continuity.json')


if __name__ == '__main__':
    main()
