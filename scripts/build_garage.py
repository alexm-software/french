#!/usr/bin/env python3
"""Build garage and workbench zoom from independent sources; no image-model calls."""
import json, math, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'content/rooms/garage'; OUT=ROOT/'village/assets/garage'
d=json.loads((SRC/'room.json').read_text()); W,H=d['size']
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'; font=ImageFont.truetype(FONT,17); namefont=ImageFont.truetype(FONT,24)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
def save(im,path,**kwargs):
    path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_name('.building-'+path.name)
    im.save(tmp,**kwargs);tmp.replace(path) # readers never see a zero-byte output

def head(c):return c['fr'] if c.get('verb') else c['art']+('' if c['art'].endswith("'") else ' ')+c['fr']
def build(rd,key):
    sub='' if key=='garage' else key+'/'; out=OUT/sub; (OUT/'cards').mkdir(parents=True,exist_ok=True)
    bg=Image.open(SRC/rd['background']).convert('RGB').resize((W,H),Image.Resampling.LANCZOS);save(bg,out/'background.jpg',quality=93)
    proof=bg.convert('RGBA'); items=[]; tiles=[]
    for spec in rd['items']:
        source=Image.open(SRC/'assets'/spec['asset']).convert('RGBA'); bbox=source.getchannel('A').getbbox()
        if not bbox:raise ValueError('Empty source '+spec['id'])
        source=source.crop(bbox); card=source.copy();card.thumbnail((384,384),Image.Resampling.LANCZOS);save(card,OUT/'cards'/f"{spec['id']}.webp",quality=92)
        sprite=source.copy()
        if spec.get('rotation'):
            sprite=sprite.rotate(spec['rotation'],Image.Resampling.BICUBIC,expand=True);sprite=sprite.crop(sprite.getchannel('A').getbbox())
        x,y,w,h=spec['rect'];px,py=round(x*W/100),round(y*H/100);mw,mh=round(w*W/100),round(h*H/100)
        sprite.thumbnail((mw,mh),Image.Resampling.LANCZOS);px+=(mw-sprite.width)//2;py+=mh-sprite.height
        if spec.get('occlusion_polygons'):
            cut=Image.new('L',(W,H)); cd=ImageDraw.Draw(cut)
            for poly in spec['occlusion_polygons']:cd.polygon([(round(a*W/100),round(b*H/100)) for a,b in poly],fill=255)
            sprite.putalpha(ImageChops.subtract(sprite.getchannel('A'),cut.crop((px,py,px+sprite.width,py+sprite.height))))
            # Tight visible bounds after occlusion drive both hotspot and card alignment.
            box=sprite.getchannel('A').getbbox()
            if not box:raise ValueError('Occlusion removed '+spec['id'])
            px+=box[0];py+=box[1];sprite=sprite.crop(box)
        save(sprite,out/'placed'/f"{spec['id']}.webp",quality=94)
        if not spec.get('occlusion_polygons') and spec['id']!='fr_verrou_noun' and 'wall' not in spec['surface']:
            sh=Image.new('RGBA',(W,H));sd=ImageDraw.Draw(sh);sd.ellipse((px+sprite.width*.15,py+sprite.height-3,px+sprite.width*.9,py+sprite.height+3),fill=(19,33,35,55));proof=Image.alpha_composite(proof,sh.filter(ImageFilter.GaussianBlur(2)))
        proof.alpha_composite(sprite,(px,py));c=spec['card']
        it=dict(c,id=spec['id'],img=[px/W*100,py/H*100,sprite.width/W*100,sprite.height/H*100],box=[px/W*100,py/H*100,sprite.width/W*100,sprite.height/H*100],label=spec['label'],side='V' if c.get('verb') else ('L' if c['g']=='f' else 'R'),surface=spec['surface'],cardSrc='assets/garage/cards/'+spec['id']+'.webp');items.append(it)
        tile=Image.new('RGB',(400,440),'#f3f5ef');ci=source.copy();ci.thumbnail((360,270));tile.paste(ci,((400-ci.width)//2,10),ci);td=ImageDraw.Draw(tile);td.text((14,286),head(c),font=font,fill='#183d40');td.multiline_text((14,313),'\n'.join(textwrap.wrap(c['hook'],46)),font=small,fill='#223032',spacing=3);tiles.append(tile)
    pd=ImageDraw.Draw(proof)
    for it in items:
        text=head(it);tw=pd.textlength(text,font=font);cx,top=it['label'][0]*W/100,it['label'][1]*H/100
        pd.rounded_rectangle((cx-tw/2-10,top,cx+tw/2+10,top+29),radius=14,fill='#fff8e6',outline='#3a2a1c',width=2);pd.text((cx-tw/2,top+4),text,font=font,fill='#2b1d14')
    cx,cy=rd['nameplate'][0]*W/100,rd['nameplate'][1]*H/100;tw=pd.textlength(rd['name'],font=namefont);pd.rounded_rectangle((cx-tw/2-24,cy-23,cx+tw/2+24,cy+23),radius=5,fill='#285453',outline='#193c3d',width=4);pd.text((cx-tw/2,cy-15),rd['name'],font=namefont,fill='#eef5e9')
    if key=='garage':
        for z in d.get('zooms',[]):
            at=z['zoom_from']['at'];pd.rounded_rectangle((at[0]-53,at[1]-17,at[0]+53,at[1]+17),radius=16,fill='#2f5a5e',outline='#16292b',width=2);pd.ellipse((at[0]-43,at[1]-7,at[0]-33,at[1]+3),outline='#fff8e6',width=2);pd.line((at[0]-34,at[1]+2,at[0]-29,at[1]+8),fill='#fff8e6',width=2);pd.text((at[0]-24,at[1]-10),'Les outils',font=font,fill='#fff8e6')
    for stale in (out/'placed').glob('*.webp'):
        if stale.stem not in {i['id'] for i in items}:stale.unlink()
    proofname='room-proof.jpg' if key=='garage' else key+'-proof.jpg';save(proof.convert('RGB'),SRC/'review'/proofname,quality=94)
    sheet=Image.new('RGB',(1200,440*math.ceil(len(tiles)/3)),'white')
    for n,tile in enumerate(tiles):sheet.paste(tile,((n%3)*400,(n//3)*440))
    save(sheet,SRC/'review'/('item-crops.jpg' if key=='garage' else key+'-crops.jpg'),quality=93)
    room={'key':key,'name':rd['name'],'image':'assets/garage/'+sub+'background.jpg','placed':'assets/garage/'+sub+'placed/','parent':None if key=='garage' else 'garage','layered':True,'nameplate':rd['nameplate'],'alt':rd.get('alt',"A storybook garage workshop with a curved teal truss, round daylight window and clear courtyard door."),'items':items,'zooms':[]}
    if key=='garage':room['mapExit']=d['exit'];room['zooms']=[dict(z['zoom_from'],to=z['key']) for z in d.get('zooms',[])]
    return room
rooms={'garage':build(d,'garage')}
for z in d.get('zooms',[]):rooms[z['key']]=build(z,z['key'])
payload={'building':'garage','rooms':rooms};(ROOT/'village/assets/data/garage.js').write_text('(window.VILLAGE_DATA=window.VILLAGE_DATA||{})["garage"]='+json.dumps(payload,ensure_ascii=False,separators=(',',':'))+';\n')
print('Built',len(rooms),'views,',sum(len(r['items']) for r in rooms.values()),'words; source sprites and room paintings stay independent.')
