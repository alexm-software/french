#!/usr/bin/env python3
"""Verify declared coverage, geometry, files and verb cards; browser review stays separate."""
import json
from pathlib import Path
from PIL import Image, ImageFont
root=Path(__file__).resolve().parents[2];src=root/'content/rooms/garage';spec=json.loads((src/'room.json').read_text())
planned=json.loads((root/'content/assignment.json').read_text());original=json.loads((root/'data/source/rooms.json').read_text())['rooms']
base=set(next(r['words'] for r in original if r['id']=='R_garage'));tools=set(next(r['words'] for r in original if r['id']=='R_garage_z1'))
expected=base|tools|{'fr_scier_verb','fr_reparer_verb'}
assert set(planned['R_garage'])|set(planned['R_garage_z1'])==expected,'Coverage loss or unplanned addition'
assert len(planned['R_garage'])+len(planned['R_garage_z1'])==len(expected),'Duplicate room assignments'
payload=(root/'village/assets/data/garage.js').read_text();data=json.loads(payload.split('["garage"]=',1)[1].rstrip(';\n'));font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',17)
def overlap(a,b):return min(a[0]+a[2],b[0]+b[2])>max(a[0],b[0])+.01 and min(a[1]+a[3],b[1]+b[3])>max(a[1],b[1])+.01
seen=[];nverbs=0
for key,room in data['rooms'].items():
 rid='R_garage' if key=='garage' else 'R_garage_z1';items=room['items'];assert sorted(planned[rid])==sorted(i['id'] for i in items)
 assert len(items)<=12,'Crowded view';labels=[]
 for i in items:
  seen.append(i['id']);x,y,w,h=i['box'];assert x>=5.99 and y>=5.99 and x+w<=94.01 and y+h<=94.01,(key,i['id'],'edge')
  if not i.get('verb'):assert (x+w/2<50)==(i['g']=='f'),(key,i['id'],'gender')
  else:
   nverbs+=1;assert i['beret']=='red' and i['group']=='-er'
   assert {t['key'] for t in i['tenses']}=={'present','pc','imparfait','futur','cond','subj','imper'}
   assert all(len(t['rows'])==(3 if t['key']=='imper' else 6) for t in i['tenses'])
   assert i['parts']['aux']=='avoir' and i['parts']['past']
  assert i['ex'][0] and i['ex'][1] and i['ipa'] and i['hook']
  for path in [i['cardSrc'],room['placed']+i['id']+'.webp']:
   f=root/'village'/path;assert f.exists() and f.stat().st_size>0,path
   im=Image.open(f);im.load();assert im.mode=='RGBA' and im.getchannel('A').getextrema()[0]==0,(path,'alpha')
  text=i['fr'] if i.get('verb') else i['art']+('' if i['art'].endswith("'") else ' ')+i['fr'];width=(font.getlength(text)+22)/12.8
  labels.append([i['label'][0]-width/2,i['label'][1],width,29/7.2]);assert labels[-1][0]>=0 and labels[-1][0]+width<=100 and labels[-1][1]+labels[-1][3]<=100,(i['id'],'label edge')
 for n,a in enumerate(items):
  for m,b in enumerate(items):
   if n<m:assert not overlap(a['box'],b['box']),(key,a['id'],b['id'],'hotspots overlap')
   if n!=m:
    assert not overlap(labels[n],b['box']),(key,a['id'],b['id'],'label touches asset')
    assert not overlap(labels[n],labels[m]),(key,a['id'],b['id'],'labels overlap')
  if key=='garage':
   assert not overlap(a['box'],room['mapExit']['box']),(a['id'],'door obstruction')
   assert not overlap(labels[n],room['mapExit']['box']),(a['id'],'label blocks door')
   for z in room['zooms']:
    badge=[(z['at'][0]-60)/12.8,(z['at'][1]-20)/7.2,120/12.8,40/7.2]
    assert not overlap(a['box'],badge),(a['id'],'zoom overlaps asset')
    assert not overlap(labels[n],badge),(a['id'],'zoom overlaps label')
assert set(seen)==expected and len(seen)==21 and nverbs==2
assert data['rooms']['tools']['parent']=='garage' and data['rooms']['garage']['zooms'][0]['to']=='tools'
for room in data['rooms'].values():Image.open(root/'village'/room['image']).load()
print('PASS: 21 unique assigned words, two complete verb cards, gender sides, alpha/decoding, tight hotspots, label estimates, 6% margins, zoom and return wiring.')
print('LIMIT: geometry uses fallback-font estimates; native browser/mobile/fullscreen checks remain unverified.')
