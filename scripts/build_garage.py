#!/usr/bin/env python3
"""Rebuild only the garage package. Source sprites and background stay independent."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'content/rooms/garage'
OUT=ROOT/'village/assets/garage'
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'placed').mkdir(exist_ok=True)
(OUT/'cards').mkdir(exist_ok=True)
d=json.loads((SRC/'room.json').read_text())
W,H=d['size']
bg=Image.open(SRC/d['background']).convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
bg.save(OUT/'background.jpg',quality=93)
proof=bg.convert('RGBA')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',17)
namefont=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',24)
items=[]; tiles=[]
for spec in d['items']:
    sprite=Image.open(SRC/'assets'/spec['asset']).convert('RGBA')
    alpha=sprite.getchannel('A'); bbox=alpha.getbbox()
    if not bbox: raise ValueError('Empty sprite: '+spec['id'])
    sprite=sprite.crop(bbox)
    sprite.save(OUT/'cards'/f"{spec['id']}.webp",quality=94)
    x,y,w,h=spec['rect']; px,py=round(x*W/100),round(y*H/100)
    maxw,maxh=round(w*W/100),round(h*H/100)
    sprite.thumbnail((maxw,maxh),Image.Resampling.LANCZOS)
    px+=(maxw-sprite.width)//2; py+=maxh-sprite.height
    # Furniture occlusion is specified in scene coordinates. Cut only the sprite;
    # the immutable background supplies the table's pixels, so no room repaint.
    cut=Image.new('L',(W,H),0); cd=ImageDraw.Draw(cut)
    for poly in spec.get('occlusion_polygons',[]):
        cd.polygon([(round(a*W/100),round(b*H/100)) for a,b in poly],fill=255)
    if spec.get('occlusion_polygons'):
        from PIL import ImageChops
        mask=cut.crop((px,py,px+sprite.width,py+sprite.height))
        sprite.putalpha(ImageChops.subtract(sprite.getchannel('A'),mask))
    sprite.save(OUT/'placed'/f"{spec['id']}.webp",quality=94)
    # A small contact shadow directly under each prop; preserve source alpha.
    if not spec.get('occlusion_polygons') and spec['id']!='fr_verrou_noun':
        shadow=Image.new('RGBA',(W,H)); sd=ImageDraw.Draw(shadow)
        sd.ellipse((px+sprite.width*.15,py+sprite.height-4,px+sprite.width*.9,py+sprite.height+3),fill=(19,33,35,65))
        proof=Image.alpha_composite(proof,shadow.filter(ImageFilter.GaussianBlur(2)))
    proof.alpha_composite(sprite,(px,py))
    it=dict(spec['card'],id=spec['id'],img=[px/W*100,py/H*100,sprite.width/W*100,sprite.height/H*100],box=[px/W*100,py/H*100,sprite.width/W*100,sprite.height/H*100],label=spec['label'],side='L' if spec['card']['g']=='f' else 'R',surface=spec['surface'],cardSrc='assets/garage/cards/'+spec['id']+'.webp')
    items.append(it)
    tile=Image.new('RGB',(400,420),'#f3f5ef'); im=Image.open(OUT/'cards'/f"{spec['id']}.webp").convert('RGBA'); im.thumbnail((360,270));tile.paste(im,((400-im.width)//2,10),im)
    td=ImageDraw.Draw(tile);td.text((14,286),spec['card']['art']+('' if spec['card']['art'].endswith("'") else ' ')+spec['card']['fr'],font=font,fill='#183d40')
    import textwrap
    td.multiline_text((14,313),'\n'.join(textwrap.wrap(spec['card']['hook'],46)),font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13),fill='#223032',spacing=3)
    tiles.append(tile)
# Match the preview label renderer's font and pill padding.
pd=ImageDraw.Draw(proof)
for it in items:
    text=it['art']+('' if it['art'].endswith("'") else ' ')+it['fr']; tw=pd.textlength(text,font=font)
    cx,top=it['label'][0]*W/100,it['label'][1]*H/100
    pd.rounded_rectangle((cx-tw/2-10,top,cx+tw/2+10,top+29),radius=14,fill='#fff8e6',outline='#3a2a1c',width=2)
    pd.text((cx-tw/2,top+4),text,font=font,fill='#2b1d14')
cx,cy=d['nameplate'][0]*W/100,d['nameplate'][1]*H/100; tw=pd.textlength(d['name'],font=namefont)
pd.rounded_rectangle((cx-tw/2-24,cy-23,cx+tw/2+24,cy+23),radius=5,fill='#285453',outline='#193c3d',width=4);pd.text((cx-tw/2,cy-15),d['name'],font=namefont,fill='#eef5e9')
proof.convert('RGB').save(SRC/'review/room-proof.jpg',quality=94)
sheet=Image.new('RGB',(1200,1260),'white')
for n,tile in enumerate(tiles):sheet.paste(tile,((n%3)*400,(n//3)*420))
sheet.save(SRC/'review/item-crops.jpg',quality=93)
room={'key':'garage','name':d['name'],'image':'assets/garage/background.jpg','placed':'assets/garage/placed/','parent':None,'layered':True,'nameplate':d['nameplate'],'alt':'A storybook workshop under a curved teal roof truss and a round daylight window; mnemonic projects occupy the benches, cupboard and slate floor.','mapExit':d['exit'],'items':items,'zooms':[]}
payload={'building':'garage','rooms':{'garage':room}}
(ROOT/'village/assets/data/garage.js').write_text('(window.VILLAGE_DATA=window.VILLAGE_DATA||{})["garage"]='+json.dumps(payload,ensure_ascii=False,separators=(',',':'))+';\n')
print('Built garage: 9 separate sprites, 9 card images, fixed background and review proofs.')
