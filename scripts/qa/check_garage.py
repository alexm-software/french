#!/usr/bin/env python3
"""Package checks. Visual and browser review are recorded separately, never inferred."""
import json,re
from pathlib import Path
from PIL import Image, ImageFont
root=Path(__file__).resolve().parents[2]
src=root/'content/rooms/garage'
spec=json.loads((src/'room.json').read_text())
planned=next(r for r in json.loads((root/'data/source/rooms.json').read_text())['rooms'] if r['id']=='R_garage')['words']
assert sorted(planned)==sorted(x['id'] for x in spec['items']), 'Assignment differs from inventory'
payload=(root/'village/assets/data/garage.js').read_text()
data=json.loads(payload.split('["garage"]=',1)[1].rstrip(';\n'))
room=data['rooms']['garage']; items=room['items']; assert len(items)==9
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',17)
def overlap(a,b):return min(a[0]+a[2],b[0]+b[2])>max(a[0],b[0])+.01 and min(a[1]+a[3],b[1]+b[3])>max(a[1],b[1])+.01
labels=[]
for i in items:
 x,y,w,h=i['box']; assert x>=6 and y>=6 and x+w<=94 and y+h<=94,(i['id'],'edge')
 assert (x+w/2<50)==(i['g']=='f'),(i['id'],'gender side')
 assert i['ex'][0] and i['ex'][1] and i['ipa'] and i['hook']
 for path in [i['cardSrc'],room['placed']+i['id']+'.webp']:
  f=root/'village'/path; assert f.exists(),str(f)
  im=Image.open(f);assert im.mode=='RGBA' and im.getchannel('A').getextrema()[0]==0,(path,'alpha')
 text=i['art']+('' if i['art'].endswith("'") else ' ')+i['fr']
 width=(font.getlength(text)+22)/12.8
 labels.append([i['label'][0]-width/2,i['label'][1],width,29/7.2])
for n,a in enumerate(items):
 for m,b in enumerate(items):
  if n<m: assert not overlap(a['box'],b['box']),(a['id'],b['id'],'hotspots overlap')
  if n!=m:
   assert not overlap(labels[n],b['box']),(a['id'],b['id'],'label touches other asset')
   assert not overlap(labels[n],labels[m]),(a['id'],b['id'],'labels overlap')
 assert not overlap(a['box'],room['mapExit']['box']),(a['id'],'door obstruction')
 assert not overlap(labels[n],room['mapExit']['box']),(a['id'],'label blocks door')
print('PASS: exact 9 planned words, articles/gender sides, alpha, cards/examples, hotspot separation, estimated label rectangles, door clearance and 6% asset margins.')
print('LIMIT: label metrics use DejaVu Serif fallback; actual-browser desktop/mobile/fullscreen checks remain separate. No release claim.')
