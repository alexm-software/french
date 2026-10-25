(function(){
'use strict';
var MAP=window.V2_MAP; // village/v2/data/map.js: painting + building polygons (1280x720 px)
var $=function(s,e){return (e||document).querySelector(s)};
(function(){ var st=document.createElement('style'); st.textContent=
 '.abcgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));gap:6px;margin:6px 0 12px}'+
 '.abcgrid.numgrid{grid-template-columns:repeat(auto-fill,minmax(108px,1fr))}.numgrid .abcl span{font-size:.8em;text-align:center;overflow-wrap:anywhere}'+
 '.numnotes{margin:6px 0 0;padding-left:1.2em}.numnotes li{margin:0 0 8px}.numnotes .nx{display:inline-block;margin:3px 8px 0 0;padding:1px 6px;border-radius:6px;background:#fff8e6;border:1px solid #d9c4a0;font-size:.9em}'+
 '.abcl{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:58px;padding:4px 2px;border:2px solid #6b4a2b;border-radius:8px;background:#fff8e6;font:inherit;color:#3c2414;cursor:pointer}'+
 '.abcl:nth-child(4n+2){background:#e6f4ff}.abcl:nth-child(4n+3){background:#eaf7e4}.abcl:nth-child(4n){background:#ffeaea}'+
 '.abcl b{font-size:1.45em;line-height:1.1}.abcl span{font-size:.85em}.abcl:hover,.abcl:focus-visible{outline:3px solid #e0a030;outline-offset:1px}'+
 '.abcacc{display:grid;gap:6px;margin-top:6px}.acc{display:grid;grid-template-columns:5.2em 1fr;grid-template-rows:auto auto;column-gap:10px;align-items:center;padding:6px 8px;border-radius:8px;background:#fff8e6;border:1px solid #d9c4a0}'+
 '.acc b{grid-row:1/3;font-size:1.35em;text-align:center}.acc .an{font-weight:600}.acc .ae{font-size:.9em;opacity:.85}'+
 // in-building doorways: a hit area (painted door or a separate plaque) with a preview pill on hover, focus or first tap
 '.doorway{position:absolute;display:block;border-radius:calc(10px*var(--s,1));outline:none;-webkit-tap-highlight-color:transparent;z-index:2}'+
 '.doorimg{position:absolute;pointer-events:none;user-select:none;-webkit-user-drag:none}'+
 '.doorway:hover,.doorway:focus-visible,.doorway.armed,.hl .doorway{box-shadow:0 0 0 calc(3px*var(--s,1)) rgba(255,216,107,.95),0 0 calc(18px*var(--s,1)) rgba(255,216,107,.7)}'+
 '.dpill{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);display:none;align-items:center;gap:calc(6px*var(--s,1));white-space:nowrap;pointer-events:none;font-family:Georgia,serif;font-weight:700;color:#fff8e6;background:#2f5a5e;border:calc(2px*var(--s,1) + .5px) solid #16292b;border-radius:calc(12px*var(--s,1));font-size:calc(16px*var(--s,1));padding:calc(4px*var(--s,1)) calc(10px*var(--s,1)) calc(4px*var(--s,1)) calc(4px*var(--s,1));box-shadow:0 calc(3px*var(--s,1)) 0 rgba(0,0,0,.35)}'+
 '.dpill img{width:calc(96px*var(--s,1));height:calc(54px*var(--s,1));border-radius:calc(7px*var(--s,1));display:block;object-fit:cover}'+
 '.doorway:hover .dpill,.doorway:focus-visible .dpill,.doorway.armed .dpill,.hl .doorway .dpill{display:inline-flex}'+
 '#rooms{display:flex;align-items:center;margin-left:8px;font-family:Georgia,serif;font-size:14px;line-height:1;color:rgba(251,245,230,.55);white-space:nowrap}'+
 '#rooms[hidden]{display:none}'+
 '#rooms a{color:#fbf5e6;text-decoration:none;padding:5px 7px;border-radius:999px;opacity:.75}'+
 '#rooms a:hover,#rooms a:focus-visible{opacity:1;background:rgba(255,255,255,.12);outline:none}'+
 '#rooms a[aria-current="page"]{opacity:1;color:#ffd86b;font-weight:700;cursor:default}'+
 '#rooms .dot{padding:0 1px}'+
 '#app.roomsdrop #rooms{position:absolute;left:8px;top:calc(var(--h) + 6px);margin:0;z-index:6;background:rgba(43,69,73,.88);border:1px solid rgba(0,0,0,.35);border-radius:999px;padding:1px 3px;font-size:13px;box-shadow:0 2px 6px rgba(0,0,0,.3)}'+
 '#app.roomsdrop #scroller{top:36px}'+ // keep the painting clear of the dropped room list so it never hides labels
 '.strip-left{display:flex;align-items:center}';
 document.head.appendChild(st) })();
var stage=$('#stage'), scroller=$('#scroller'), blur=$('#blur'), back=$('#back'), app=$('#app');
var curTense='present';
stage.addEventListener('click',function(e){ if(e.target.closest&&e.target.closest('.doorway'))return; stage.querySelectorAll('.doorway.armed').forEach(function(o){o.classList.remove('armed')}) });
var rooms=document.createElement('nav'); rooms.id='rooms'; rooms.setAttribute('aria-label','Rooms in this building'); rooms.hidden=true;
back.parentNode.appendChild(rooms);
// ---------- label mode: 'always' (default) or 'hover' (show on hover / first tap) ----------
var LKEY='village.labelMode', labelMode='always', lastPointer='mouse', armed=-1;
try{ if(localStorage.getItem(LKEY)==='hover') labelMode='hover' }catch(e){}
function applyLabelMode(){
  stage.classList.toggle('lhover',labelMode==='hover');
  var b=document.getElementById('labMode'), on=labelMode==='always';
  b.setAttribute('aria-checked',on);
  b.title=on?'Labels: always shown. Click to show them only on hover or tap (L)':'Labels: only on hover or tap. Click to always show them (L)';
  b.querySelector('.sr').textContent=on?' always shown':' only on hover or tap';
  disarm();
}
function setLabelMode(m){ labelMode=m; try{localStorage.setItem(LKEY,m)}catch(e){} applyLabelMode() }
function showLab(i,on){ var l=stage.querySelector('.lab[data-i="'+i+'"]'); if(l) l.classList.toggle('show',on) }
function disarm(){ if(armed>=0){ showLab(armed,false); var o=document.getElementById('ov'+armed); if(o)o.classList.remove('on') } armed=-1 }
var cardWrap=$('#cardWrap'), card=$('#card'), lastFocus=null, view=null;
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function pct(v){return v+'%'}
// ---------- layout: aspect-locked 16:9 stage, contain-fit; portrait phones pan sideways ----------
function placeRooms(){
  app.classList.remove('roomsdrop'); if(rooms.hidden)return;
  var strip=$('#strip'), t=$('#title'), side=(strip.clientWidth-t.offsetWidth)/2-14, need=back.offsetWidth+8+rooms.offsetWidth;
  app.classList.toggle('roomsdrop',need>side);
}
function fit(){
  placeRooms();
  var vw=scroller.clientWidth, vh=scroller.clientHeight, ar=16/9, w, h, pan=false;
  if(vw/vh>=ar){h=vh;w=h*ar}else{w=vw;h=w/ar}
  if(vw/vh<0.9){ // tall phone: make the painting taller and let the user swipe across it
    h=Math.min(vh*0.9, vw*1.45); w=h*ar; pan=w>vw+2;
  }
  var pan2=false;
  if(w<900){ // small landscape screens: keep labels readable, let the user pan both ways
    w=900; h=w/ar; pan=w>vw+2; pan2=h>vh+2;
  }
  stage.style.width=Math.round(w)+'px'; stage.style.height=Math.round(h)+'px'; stage.style.setProperty('--s',(Math.round(w)/1280).toFixed(4));
  scroller.classList.toggle('pan',pan); scroller.classList.toggle('pan2',pan2);
  var hint=$('#panHint'); hint.hidden=!pan;
  if(pan&&!scroller.dataset.centred){ignoreScroll=true;scroller.scrollLeft=(w-vw)*(view==='map'||view==='sector'?0.05:0.35);scroller.dataset.centred=1;hint.style.opacity=1;setTimeout(function(){ignoreScroll=false},300)}
  // Sector hover tags only. World signposts (.tag.pin) stay on their authored centres.
  if(stage.querySelector('.tag.live:not(.pin),#tagSoon')) clampMapLabels();
}
window.addEventListener('resize',fit);
document.addEventListener('pointerdown',function(e){lastPointer=e.pointerType||'mouse'},true);
document.addEventListener('keydown',function(){lastPointer='key'},true);
var ignoreScroll=false;
scroller.addEventListener('scroll',function(){if(ignoreScroll)return;var h=$('#panHint');if(!h.hidden)h.style.opacity=0},{passive:true});
// ---------- maps: world (#/) and sector maps (#/quartier/<slug>) ----------
// data/map.js lists every sector and every building / verb street painted on each sector map
// (content/v2/map.json). Buildings are discovered at runtime: a building is live as soon as
// village/v2/data/<id>.js loads (id = building_id without its Bnn_ prefix, or a legacy id given in
// the registry). A loaded payload is placed by its own building_id / sector_id, falling back to the
// registry entry (the école and mairie layouts predate those fields).
var LIVE={}, probed=false, REG={}, BYBID={};
MAP.world.sectors.forEach(function(w){ var S=MAP.sectors[w.slug]; S.buildings.forEach(function(b){
  b.id=b.id||b.building_id.replace(/^B\d+_/,''); b.sector=w.slug; REG[b.id]=b; BYBID[b.building_id]=BYBID[b.building_id]||b });
  // verb streets go live the same way: building_id = the street id (ST_priere), data id = it lowercased (data/st_priere.js)
  S.streets.forEach(function(t){ t.building_id=t.building_id||t.id; t.id=t.building_id.toLowerCase(); t.street=1; t.sector=w.slug;
    REG[t.id]=t; BYBID[t.building_id]=BYBID[t.building_id]||t }) });
function sectorById(sid){ return MAP.world.sectors.filter(function(w){return w.id===sid})[0] }
function homeOf(bld){ // {slug, entry} where the building lives on the maps
  var D=window.VILLAGE_DATA&&window.VILLAGE_DATA[bld], e=REG[bld];
  if(D&&D.building_id&&BYBID[D.building_id]&&BYBID[D.building_id].id===bld) e=BYBID[D.building_id];
  var w=D&&D.sector_id&&sectorById(D.sector_id);
  return {slug:w?w.slug:(e&&e.sector), entry:e} }
function sectorHref(slug){ return slug?'#/quartier/'+slug:'#/' }
function probeAll(cb){ var ids=Object.keys(REG), n=ids.length; if(!n){probed=true;cb();return}
  ids.forEach(function(id){ loadData(id,function(ok){ if(ok&&window.VILLAGE_DATA[id])LIVE[id]=1; if(--n===0){probed=true;cb()} }) }) }
function pts(r){ return r[0]+','+r[1]+' '+(r[0]+r[2])+','+r[1]+' '+(r[0]+r[2])+','+(r[1]+r[3])+' '+r[0]+','+(r[1]+r[3]) }
function tagAt(r){ return [r[0]+r[2]/2, r[1]+Math.min(14,r[3]/4)] }
function doorAt(r){ return [r[0]+r[2]/2, r[1]+r[3]-Math.min(34,r[3]/3)] }
function liveIn(slug){ return Object.keys(LIVE).filter(function(id){ return homeOf(id).slug===slug }) }
// Sector hover tags stay on the painting: at least 6% inside every edge, and off other buildings' click boxes and doors.
// World-map signposts (.tag.pin) are placed by their tag point and are not moved here.
function relRect(el){
  var s=stage.getBoundingClientRect(), r=el.getBoundingClientRect();
  return {l:r.left-s.left, t:r.top-s.top, r:r.right-s.left, b:r.bottom-s.top, w:r.width, h:r.height};
}
function mapFrame(){
  var s=stage.getBoundingClientRect(), m=0.06;
  return {l:s.width*m, t:s.height*m, r:s.width*(1-m), b:s.height*(1-m), w:s.width, h:s.height};
}
function inFrame(a,f){ return a.l>=f.l-0.5 && a.t>=f.t-0.5 && a.r<=f.r+0.5 && a.b<=f.b+0.5 }
function labelObstacles(ownPoly, ownDoor){
  var o=[];
  stage.querySelectorAll('polygon.bld').forEach(function(p){ if(p!==ownPoly) o.push(relRect(p)) });
  stage.querySelectorAll('.door').forEach(function(d){ if(d!==ownDoor) o.push(relRect(d)) });
  return o;
}
function overlapArea(b, obs){
  var a=0;
  for(var i=0;i<obs.length;i++){
    var o=obs[i], x=Math.min(b.r,o.r)-Math.max(b.l,o.l), y=Math.min(b.b,o.b)-Math.max(b.t,o.t);
    if(x>0 && y>0) a+=x*y;
  }
  return a;
}
function nudgeLabel(el, dx, dy){
  var s=stage.getBoundingClientRect();
  if(!s.width||!s.height) return;
  el.style.left=(parseFloat(el.style.left)+dx/s.width*100)+'%';
  el.style.top=(parseFloat(el.style.top)+dy/s.height*100)+'%';
}
function intoFrame(el, f){
  var pad=4, g={l:f.l+pad, t:f.t+pad, r:f.r-pad, b:f.b-pad}, b=relRect(el);
  for(var i=0;i<4;i++){
    var dx=0, dy=0;
    if(b.w>g.r-g.l) dx=g.l-b.l;
    else { if(b.l<g.l) dx=g.l-b.l; if(b.r+dx>g.r) dx=g.r-b.r; }
    if(b.h>g.b-g.t) dy=g.t-b.t;
    else { if(b.t<g.t) dy=g.t-b.t; if(b.b+dy>g.b) dy=g.b-b.b; }
    if(!dx && !dy) break;
    nudgeLabel(el, dx, dy);
    var n=relRect(el);
    if(Math.abs(n.l-b.l)<0.5 && Math.abs(n.t-b.t)<0.5 && Math.abs(n.r-b.r)<0.5 && Math.abs(n.b-b.b)<0.5) break;
    b=n;
  }
  return b;
}
function separateLabel(el, f, obs){
  var b=intoFrame(el, f), best={left:el.style.left, top:el.style.top, area:inFrame(b,f)?overlapArea(b,obs):1e12};
  for(var n=0;n<12;n++){
    if(inFrame(b,f) && overlapArea(b,obs)===0) return true;
    var hit=null, area=0;
    for(var i=0;i<obs.length;i++){
      var o=obs[i], x=Math.min(b.r,o.r)-Math.max(b.l,o.l), y=Math.min(b.b,o.b)-Math.max(b.t,o.t);
      if(x>0 && y>0 && x*y>area){ area=x*y; hit={o:o,x:x,y:y}; }
    }
    if(!hit) break;
    var gap=4, dx=0, dy=0;
    if(hit.x<=hit.y) dx=((b.l+b.r)<(hit.o.l+hit.o.r)?-1:1)*(hit.x+gap);
    else dy=((b.t+b.b)<(hit.o.t+hit.o.b)?-1:1)*(hit.y+gap);
    nudgeLabel(el, dx, dy);
    b=intoFrame(el, f);
    var left=overlapArea(b, obs);
    if(inFrame(b,f) && left<best.area) best={left:el.style.left, top:el.style.top, area:left};
  }
  el.style.left=best.left; el.style.top=best.top;
  b=relRect(el);
  return inFrame(b,f) && overlapArea(b, obs)===0;
}
function clampOne(el, ownPoly, ownDoor){
  if(el.classList.contains('pin')) return;
  if(el.dataset.ox===undefined){ el.dataset.ox=el.style.left; el.dataset.oy=el.style.top; }
  var shown=el.classList.contains('show');
  el.style.transition='none';
  el.classList.add('show');
  el.classList.remove('wrap'); el.style.maxWidth=''; el.style.width=''; el.style.fontSize='';
  el.style.left=el.dataset.ox; el.style.top=el.dataset.oy;
  var f=mapFrame(), obs=labelObstacles(ownPoly, ownDoor);
  var ok=separateLabel(el, f, obs);
  if(!ok){
    var h=relRect(el).h;
    el.style.left=el.dataset.ox; el.style.top=el.dataset.oy;
    nudgeLabel(el, 0, h+8);
    ok=separateLabel(el, f, obs);
  }
  if(!ok) parkOnOwn(el, ownPoly, ownDoor, f);
  el.style.transition='';
  if(!shown) el.classList.remove('show');
}
function parkOnOwn(el, ownPoly, ownDoor, f){
  el.classList.remove('wrap'); el.style.width=''; el.style.maxWidth=''; el.style.fontSize='';
  el.style.left=el.dataset.ox; el.style.top=el.dataset.oy;
  if(!ownPoly){ intoFrame(el, f); return; }
  var p=relRect(ownPoly), door=ownDoor?relRect(ownDoor):null;
  var above=relRect(el);
  nudgeLabel(el, 0, (p.t-6)-above.b);
  above=intoFrame(el, f);
  var obs=labelObstacles(ownPoly, ownDoor);
  if(inFrame(above, f) && overlapArea(above, obs)===0) return;
  el.classList.remove('wrap'); el.style.width=''; el.style.maxWidth=''; el.style.fontSize='';
  el.style.left=el.dataset.ox; el.style.top=el.dataset.oy;
  var L=Math.max(p.l+4, f.l), R=Math.min(p.r-4, f.r), T=Math.max(p.t+4, f.t), B=Math.min(p.b-4, f.b);
  if(door && door.t-4>T+24) B=Math.min(B, door.t-4);
  var span=Math.max(28, R-L), room=Math.max(24, B-T);
  el.classList.add('wrap');
  el.style.width=Math.round(span)+'px'; el.style.maxWidth=el.style.width;
  var size=20, b=relRect(el);
  while(b.h>room && size>9){ size-=1; el.style.fontSize=size+'px'; b=relRect(el); }
  nudgeLabel(el, L-b.l, T-b.t);
  b=relRect(el);
  nudgeLabel(el, L-b.l, T-b.t);
  if(!inFrame(relRect(el), f)) intoFrame(el, f);
}
function clampMapLabels(){
  stage.querySelectorAll('.tag.live:not(.pin)').forEach(function(el){
    var i=el.id.replace('tagLive','');
    var link=stage.querySelector('a.lnk[data-i="'+i+'"]');
    clampOne(el, link?link.querySelector('polygon'):null, stage.querySelector('.door[data-i="'+i+'"]'));
  });
}
// live: [{href,name,rect,aria}], soon: [{name,rect,small}]
function drawMap(img,alt,label,live,soon){
  blur.style.backgroundImage='url('+img+')';
  var h='<img class="bg" src="'+img+'" alt="'+esc(alt)+'">';
  h+='<svg viewBox="0 0 1280 720" preserveAspectRatio="none" aria-label="'+esc(label)+'">';
  soon.forEach(function(b,i){h+='<polygon class="bld soon" data-i="'+i+'" points="'+pts(b.rect)+'"><title>'+esc(b.name)+(b.small?' ('+esc(b.small)+')':'')+'</title></polygon>'});
  live.forEach(function(L,i){
    var rings=L.poly?L.poly.map(function(r){return r.map(function(p){return p.join(',')}).join(' ')}):[pts(L.rect)];
    h+='<a href="'+L.href+'" class="lnk" data-i="'+i+'" aria-label="'+esc(L.aria)+'">'+rings.map(function(r){return '<polygon class="bld live" tabindex="-1" points="'+r+'"></polygon>'}).join('')+'</a>';
  });
  h+='</svg>';
  live.forEach(function(L,i){ var d=L.door||doorAt(L.rect), t=L.tag||tagAt(L.rect);
    if(L.pin){ // world map: an always-on bilingual signpost centred on L.tag; it is a link too, so a click on it opens its own sector
      h+='<a class="tag live pin'+(L.nodoor?' soonpin':'')+'" id="tagLive'+i+'" href="'+L.href+'" tabindex="-1" aria-hidden="true" title="'+esc(L.small||'')+'" style="left:'+pct(t[0]/12.8)+';top:'+pct(t[1]/7.2)+'"><b>'+esc(L.name)+'</b>'+(L.en?'<span class="en"> ·\u00a0'+esc(L.en)+'</span>':'')+'</a>';
      return }
    if(!L.nodoor) h+='<div class="door" data-i="'+i+'" style="left:'+pct(d[0]/12.8)+';top:'+pct(d[1]/7.2)+'" aria-hidden="true">➜</div>';
    h+='<div class="tag live" id="tagLive'+i+'" style="left:'+pct(t[0]/12.8)+';top:'+pct(Math.max(t[1],60)/7.2)+'">'+esc(L.name)+(L.small?'<small>'+esc(L.small)+'</small>':'')+'</div>';
  });
  h+='<div class="tag" id="tagSoon"></div>';
  stage.innerHTML=h;
  var ts=$('#tagSoon');
  stage.querySelectorAll('a.lnk').forEach(function(lnk){
    var polys=lnk.querySelectorAll('.bld.live'), tl=$('#tagLive'+lnk.dataset.i);
    function on(){tl.classList.add('show');polys.forEach(function(p){p.classList.add('hot')})} function off(){tl.classList.remove('show');polys.forEach(function(p){p.classList.remove('hot')})}
    lnk.addEventListener('mouseenter',on); lnk.addEventListener('mouseleave',off); lnk.addEventListener('focus',on); lnk.addEventListener('blur',off);
    if(tl.classList.contains('pin')){ tl.addEventListener('mouseenter',on); tl.addEventListener('mouseleave',off) }
  });
  stage.querySelectorAll('.bld.soon').forEach(function(p){
    var b=soon[+p.dataset.i], t=b.tag||tagAt(b.rect);
    function show(){
      ts.innerHTML=esc(b.name)+(b.small?'<small>'+esc(b.small)+'</small>':'');
      ts.style.left=pct(t[0]/12.8); ts.style.top=pct(Math.max(t[1],60)/7.2);
      ts.dataset.ox=ts.style.left; ts.dataset.oy=ts.style.top;
      ts.classList.add('show');
      clampOne(ts, p, null);
    }
    p.addEventListener('mouseenter',show); p.addEventListener('mouseleave',function(){ts.classList.remove('show')});
    p.addEventListener('click',function(){show();clearTimeout(p._t);p._t=setTimeout(function(){ts.classList.remove('show')},1600)});
  });
  stage.dataset.probed=probed?'1':'0';
  fit();
}
function renderMap(){
  view='map'; curSector=null; document.title='Le Village · French vocabulary memory village';
  back.hidden=true; rooms.hidden=true;
  var W=MAP.world, live=[];
  W.sectors.forEach(function(w){ var n=liveIn(w.slug).length;
    live.push({href:sectorHref(w.slug),name:w.name,en:w.en,poly:w.poly,pin:!!w.poly,rect:w.rect,tag:w.tag,door:w.door,aria:'Open the map of '+w.name+(n?' ('+n+' to visit)':''),nodoor:!n,
      small:probed?(n?n+(n>1?' bâtiments ouverts':' bâtiment ouvert'):'bientôt'):''}) });
  drawMap(W.image,W.alt,'Village map',live,[]);
}
var curSector=null;
function renderSector(slug){
  var S=MAP.sectors[slug]; view='sector'; curSector=slug; document.title=S.name+' · Le Village';
  back.hidden=false; rooms.hidden=true; $('#backLabel').textContent='Le village'; back.title='Back to the village map';
  var live=[], soon=[], here={};
  liveIn(slug).forEach(function(id){ var e=homeOf(id).entry; if(!e||here[e.id||e.building_id])return; here[e.id||e.building_id]=1;
    live.push({href:'#/'+id,name:e.name,rect:e.rect,tag:e.tag,door:e.door,small:e.street?'rue des verbes':'',aria:'Enter '+e.name}) });
  S.buildings.forEach(function(b){ if(!here[b.id||b.building_id]&&!(LIVE[b.id]&&homeOf(b.id).slug===slug)) soon.push({name:b.name,rect:b.rect,tag:b.tag,small:probed?'bientôt':''}) });
  S.streets.forEach(function(t){ if(!here[t.id]&&!(LIVE[t.id]&&homeOf(t.id).slug===slug)) soon.push({name:t.name,rect:t.rect,tag:t.tag,small:'rue des verbes'+(probed?' · bientôt':'')}) });
  drawMap(S.image,S.alt,S.name+' map',live,soon);
}
// ---------- room / zoom ----------
var R=null, B=null;
function roomHref(bld,key){ return key===bld?'#/'+bld:'#/'+bld+'/'+key }
function renderRooms(bld,key){
  var D=window.VILLAGE_DATA[bld], L=D.roomList||[], cur=D.rooms[key];
  rooms.hidden=!(L.length>1&&!cur.parent);
  if(rooms.hidden){ rooms.innerHTML=''; return }
  rooms.innerHTML=L.map(function(r){ var on=r.key===key;
    return '<a href="'+roomHref(bld,r.key)+'"'+(on?' aria-current="page"':'')+'>'+esc(r.short)+'</a>' }).join('<span class="dot" aria-hidden="true">·</span>');
}
function renderRoom(bld,key){
  B=bld; var D=window.VILLAGE_DATA[bld]; R=D.rooms[key]; view=R.parent?'zoom':'room'; document.title=R.name+(key!==bld?' · '+D.rooms[bld].name:'')+' · Le Village';
  back.hidden=false; renderRooms(bld,key);
  var BT=R.parent||R.backTo;
  if(BT){ $('#backLabel').textContent=D.rooms[BT].name; back.title='Back to '+D.rooms[BT].name; }
  else { var H=homeOf(bld), S=H.slug&&MAP.sectors[H.slug]; $('#backLabel').textContent=S?S.name:'Le village'; back.title='Back to the map of '+(S?S.name:'the village'); }
  blur.style.backgroundImage='url('+R.image+')';
  var h='<img class="bg" src="'+R.image+'" alt="'+esc(R.alt||'')+'">';
  if(R.nameplate){ h+='<div class="room-nameplate" style="left:'+pct(R.nameplate[0])+';top:'+pct(R.nameplate[1])+'">'+esc(R.name)+'</div>'; }
  if(R.mapExit){ var e=R.mapExit.box, H0=homeOf(bld), S0=H0.slug&&MAP.sectors[H0.slug], xh=R.mapExit.href||sectorHref(H0.slug);
    h+='<a class="doorway mapexit" href="'+esc(xh)+'" aria-label="'+esc(R.mapExit.label)+'" style="left:'+pct(e[0])+';top:'+pct(e[1])+';width:'+pct(e[2])+';height:'+pct(e[3])+'"><span class="dpill"><img src="'+(S0?S0.image:MAP.world.image)+'" alt="">'+esc(R.mapExit.label)+'</span></a>'; }
  if(R.sign){ var g=R.sign.box; h+='<img class="signimg" src="'+R.sign.src+'" alt="Sign: '+esc(R.sign.text)+'" style="left:'+pct(g[0]/12.8)+';top:'+pct(g[1]/7.2)+';width:'+pct(g[2]/12.8)+'">'; }
  R.items.forEach(function(it,i){
    var g=it.img,b=it.box,l=it.label;
    h+='<div class="v2box" id="ov'+i+'" aria-hidden="true" style="left:'+pct(b[0])+';top:'+pct(b[1])+';width:'+pct(b[2])+';height:'+pct(b[3])+'"></div>';
    h+='<button class="hot" data-i="'+i+'" style="left:'+pct(b[0])+';top:'+pct(b[1])+';width:'+pct(b[2])+';height:'+pct(b[3])+'" aria-label="'+esc(headword(it))+': '+esc(it.en)+'"></button>';
    h+='<button class="lab'+(it.verb?' verb':'')+'" data-i="'+i+'" tabindex="-1" aria-hidden="true" style="left:'+pct(l[0])+';top:'+pct(l[1])+'">'+esc(headword(it))+'</button>';
  });
  (R.doors||[]).forEach(function(d,i){
    var g=d.hit, T=D.rooms[d.to];
    if(d.img){ var q=d.img.box; h+='<img class="doorimg" src="'+d.img.src+'" alt="" style="left:'+pct(q[0]/12.8)+';top:'+pct(q[1]/7.2)+';width:'+pct(q[2]/12.8)+'">'; }
    h+='<a class="doorway" data-d="'+i+'" href="'+roomHref(bld,d.to)+'" title="'+esc(d.hint)+'" aria-label="'+esc(d.label)+': '+esc(d.hint)+'" style="left:'+pct(g[0]/12.8)+';top:'+pct(g[1]/7.2)+';width:'+pct(g[2]/12.8)+';height:'+pct(g[3]/7.2)+'">';
    h+='<span class="dpill" aria-hidden="true">'+(d.thumb?'<img src="'+d.thumb+'" alt="">':'')+'<span>'+esc(d.label)+' ›</span></span></a>';
  });
  (R.zooms||[]).forEach(function(z){
    h+='<a class="zoombadge" href="#/'+bld+'/'+z.to+'" title="'+esc(z.hint)+'" style="left:'+pct(z.at[0]/12.8)+';top:'+pct(z.at[1]/7.2)+'"><span class="mag" aria-hidden="true">🔍</span>'+esc(z.label)+'</a>';
  });
  stage.innerHTML=h;
  var hideT=null;
  stage.querySelectorAll('.hot,.lab').forEach(function(btn){
    var i=+btn.dataset.i, ov=$('#ov'+i);
    function enter(){ if(lastPointer==='touch'||lastPointer==='pen')return; clearTimeout(hideT); stage.querySelectorAll('.lab.show').forEach(function(l){ if(+l.dataset.i!==i&&+l.dataset.i!==armed) l.classList.remove('show') }); ov.classList.add('on'); showLab(i,true) }
    function leave(){ if(armed===i)return; ov.classList.remove('on'); hideT=setTimeout(function(){ if(armed!==i) showLab(i,false) },140) }
    btn.addEventListener('mouseenter',enter); btn.addEventListener('mouseleave',leave);
    btn.addEventListener('focus',function(){ov.classList.add('on');showLab(i,true)});
    btn.addEventListener('blur',function(){ov.classList.remove('on'); if(armed!==i) showLab(i,false)});
    btn.addEventListener('click',function(e){
      e.stopPropagation();
      if(labelMode==='hover'&&(lastPointer==='touch'||lastPointer==='pen')&&armed!==i){ // first tap: just show the label
        disarm(); armed=i; ov.classList.add('on'); showLab(i,true); return }
      disarm(); openCard(R.items[i],btn);
    });
  });
  stage.querySelectorAll('.doorway').forEach(function(a){
    a.addEventListener('click',function(e){ e.stopPropagation(); // touch: the first tap shows where the door leads, the second goes through
      if((lastPointer==='touch'||lastPointer==='pen')&&!a.classList.contains('armed')){ e.preventDefault(); disarm(); stage.querySelectorAll('.doorway.armed').forEach(function(o){o.classList.remove('armed')}); a.classList.add('armed') }
    });
  });
  applyLabelMode();
  fit();
}
function headword(it){ if(it.verb||it.adj||it.adv) return it.fr; var a=it.art; return a==="l'"? "l'"+it.fr : a+' '+it.fr }
// ---------- speech (browser built-in, French voice) ----------
var frVoice=null;
function pickVoice(){ if(!('speechSynthesis' in window))return; var v=speechSynthesis.getVoices();
  frVoice=v.filter(function(x){return /^fr[-_]FR/i.test(x.lang)})[0]||v.filter(function(x){return /^fr/i.test(x.lang)})[0]||null }
if('speechSynthesis' in window){pickVoice(); speechSynthesis.onvoiceschanged=pickVoice}
function speak(t){ if(!('speechSynthesis' in window))return; speechSynthesis.cancel(); var u=new SpeechSynthesisUtterance(t); u.lang='fr-FR'; if(frVoice)u.voice=frVoice; u.rate=0.85; speechSynthesis.speak(u) }
var BERET={red:'#d8322f',green:'#3c8a3a',purple:'#7b3fa0',gold:'#e8b32a'};
var GROUP={red:'-er verb: red beret',green:'-ir verb: green beret',purple:'-re verb: purple beret',gold:'irregular verb: gold beret'};
function beretSvg(c){return '<svg viewBox="0 0 34 22" aria-hidden="true"><ellipse cx="17" cy="13" rx="15" ry="7.5" fill="'+c+'" stroke="#2b1d14" stroke-width="2"/><path d="M15 6 q2 -5 4 0" fill="'+c+'" stroke="#2b1d14" stroke-width="2"/><path d="M5 15 q12 5 24 0" fill="none" stroke="rgba(0,0,0,.25)" stroke-width="2"/></svg>'}
function openCard(it,from){
  lastFocus=from||document.activeElement;
  var hw=headword(it), sp='speechSynthesis' in window;
  var h='<button class="x" data-close aria-label="Close">×</button><div class="head"><div class="pic"><img src="'+esc(it.cardSrc||('assets/words/'+it.id+'.webp'))+'" alt=""></div><div class="hw">';
  h+='<h2 id="cardTitle">'+(it.verb||it.adj||it.adv?esc(it.fr):(it.art==="l'"?'<span class="art">l\u2019</span>':'<span class="art">'+esc(it.art)+' </span>')+esc(it.fr))+'</h2>';
  h+='<div class="en">'+esc(it.en)+'</div>';
  h+='<div class="pron">'+esc(it.ipa)+' · say <b>'+esc(it.say)+'</b>'+(sp?'<button class="say" data-say="'+esc(hw)+'" aria-label="Listen">🔊 Listen</button>':'')+'</div>';
  if(it.adj){ var F=it.forms||{}; h+='<div class="gram">adjective · '+(it.invariable?esc(it.fr)+' (same for both)':esc(F.m_sg||it.fr)+'/'+esc(F.f_sg||it.fr))+(F.m_pl?' · plural: '+esc(F.m_pl)+(F.f_pl&&F.f_pl!==F.m_pl?'/'+esc(F.f_pl):''):'')+'</div>';
    if(it.f_ipa&&!it.invariable) h+='<div class="pron small">feminine '+esc(F.f_sg||'')+': '+esc(it.f_ipa)+(it.f_say?' · say <b>'+esc(it.f_say)+'</b>':'')+'</div>'; }
  else if(it.adv) h+='<div class="gram">'+esc(it.gramLine||'adverb · invariable')+'</div>';
  else if(it.verb) h+='<div class="gram beret">'+beretSvg(BERET[it.beret])+' '+esc(GROUP[it.beret])+(it.reflexive?' · <span aria-hidden="true">🪞</span> hand mirror: reflexive verb':'')+'</div>';
  else h+='<div class="gram">'+(it.g==='f'?'feminine':it.g==='mf'?'masculine or feminine':'masculine')+' noun · '+esc(it.ind)+(/[\u2019']$/.test(it.ind)?'':' ')+esc(it.fr)+(it.plural?' · plural: '+esc(it.plural):'')+(it.fem?' · woman: '+esc(it.fem):'')+'</div>';
  var ff=it.falseFriend;
  if(ff) h+='<div class="ffbadge '+(ff.kind==='partial'?'part':'full')+'"><span aria-hidden="true">\u2691</span> '+(ff.kind==='partial'?'Partly a false friend':'False friend')+' \u00b7 <i lang="fr">faux ami</i></div>';
  h+='</div></div>';
  if(ff) h+='<div class="sec ffnote '+(ff.kind==='partial'?'part':'full')+'"><h3>Watch out</h3><p>'+esc(ff.note)+'</p></div>';
  h+='<div class="sec"><h3>Memory hook</h3><p>'+esc(it.hook)+'</p>'+(it.scene?'<p class="scene"><b>In the picture:</b> '+esc(it.scene)+'</p>':'')+(it.note?'<div class="note">'+esc(it.note)+'</div>':'')+'</div>';
  var exH='<div class="sec ex"><h3>Example</h3><p class="fr">'+esc(it.ex[0])+(sp?' <button class="say" data-say="'+esc(it.ex[0])+'" aria-label="Listen to the example">🔊</button>':'')+'</p><p class="tr">'+esc(it.ex[1])+'</p></div>';
  h+=exH;
  if(it.alphabet){
    h+='<div class="sec abc"><h3>L\u2019alphabet</h3><p class="small">Tap a letter to hear its French name.</p><div class="abcgrid">';
    it.alphabet.letters.forEach(function(x){ h+='<button class="abcl" '+(sp?'data-say="'+esc(x.l)+'" ':'')+'aria-label="'+esc(x.l)+': '+esc(x.name)+'"><b>'+esc(x.l)+'</b><span>'+esc(x.name)+'</span></button>' });
    h+='</div><h3>Les accents</h3><div class="abcacc">';
    it.alphabet.accents.forEach(function(x){ h+='<div class="acc"><b>'+esc(x.chars)+'</b><span class="an">'+esc(x.name)+(sp?' <button class="say" data-say="'+esc(x.name)+'" aria-label="Listen: '+esc(x.name)+'">🔊</button>':'')+'</span><span class="ae">'+esc(x.ex)+'</span></div>' });
    h+='</div></div>';
  }
  if(it.numbers){
    h+='<div class="sec abc nums"><h3>Les nombres</h3><p class="small">Tap a number to hear it in French.</p><div class="abcgrid numgrid">';
    it.numbers.items.forEach(function(x){ h+='<button class="abcl" '+(sp?'data-say="'+esc(x.word)+'" ':'')+'aria-label="'+esc(x.n)+': '+esc(x.word)+'"><b>'+esc(x.n)+'</b><span>'+esc(x.word)+'</span></button>' });
    h+='</div><h3>How French numbers work</h3><ul class="numnotes">';
    it.numbers.notes.forEach(function(x){ h+='<li><b>'+esc(x.t)+'</b> \u2014 '+esc(x.d)+'<br>'; (x.ex||[]).forEach(function(e){ h+='<span class="nx">'+esc(e.n)+' = '+esc(e.word)+(sp?' <button class="say" data-say="'+esc(e.word)+'" aria-label="Listen: '+esc(e.word)+'">🔊</button>':'')+'</span>' }); h+='</li>' });
    h+='</ul></div>';
  }
  if(it.verb&&it.tenses){
    var cur=it.tenses.some(function(t){return t.key===curTense})?curTense:'present';
    h+='<div class="sec conjsec"><h3>Conjugation</h3>';
    h+='<div class="parts"><span><b>participe présent</b> '+esc(it.parts.present)+'</span><span><b>participe passé</b> '+esc(it.parts.past)+'</span><span><b>auxiliaire</b> '+esc(it.parts.aux)+'</span></div>';
    h+='<div class="tabs" role="tablist" aria-label="Tenses">';
    it.tenses.forEach(function(t){var on=t.key===cur;
      h+='<button class="tab" role="tab" id="tab-'+t.key+'" data-tense="'+t.key+'" aria-controls="tp-'+t.key+'" aria-selected="'+on+'" tabindex="'+(on?0:-1)+'">'+esc(t.name)+'</button>'});
    h+='</div>';
    it.tenses.forEach(function(t){
      h+='<div class="tpanel" role="tabpanel" id="tp-'+t.key+'" aria-labelledby="tab-'+t.key+'"'+(t.key===cur?'':' hidden')+'><table class="conj">'+t.rows.map(function(r){return '<tr><td>'+esc(r[0])+'</td><td>'+esc(r[1])+'</td></tr>'}).join('')+'</table>'+(t.note?'<div class="small">'+esc(t.note)+'</div>':'')+'</div>';
    });
    h+='</div>';
  }
  card.innerHTML=h; cardWrap.hidden=false; card.scrollTop=0; card.focus(); var st=card.querySelector('.tab[aria-selected="true"]'); if(st)revealTab(st);
}
function closeCard(){ if(cardWrap.hidden)return; cardWrap.hidden=true; if('speechSynthesis' in window)speechSynthesis.cancel(); if(lastFocus&&lastFocus.focus)lastFocus.focus() }
function revealTab(b){ var tl=b.parentNode, x=b.offsetLeft-tl.offsetLeft, w=tl.clientWidth;
  if(x<tl.scrollLeft+8||x+b.offsetWidth>tl.scrollLeft+w-8) tl.scrollLeft=Math.max(0,x-(w-b.offsetWidth)/2) }
function selectTense(key,focus){ curTense=key; card.querySelectorAll('.tab').forEach(function(b){var on=b.dataset.tense===key; b.setAttribute('aria-selected',on); b.tabIndex=on?0:-1; if(on){ if(focus)b.focus({preventScroll:true}); revealTab(b) }});
  card.querySelectorAll('.tpanel').forEach(function(p){p.hidden=p.id!=='tp-'+key}) }
card.addEventListener('keydown',function(e){ var t=e.target; if(!t.classList||!t.classList.contains('tab'))return;
  var tabs=[].slice.call(card.querySelectorAll('.tab')), i=tabs.indexOf(t), j=-1;
  if(e.key==='ArrowRight')j=(i+1)%tabs.length; else if(e.key==='ArrowLeft')j=(i-1+tabs.length)%tabs.length; else if(e.key==='Home')j=0; else if(e.key==='End')j=tabs.length-1;
  if(j>=0){e.preventDefault(); selectTense(tabs[j].dataset.tense,true)} });
cardWrap.addEventListener('click',function(e){ var t=e.target; var tb=t.closest('.tab'); if(tb){selectTense(tb.dataset.tense);return}
  if(t.closest('[data-close]'))closeCard(); var s=t.closest('[data-say]'); if(s)speak(s.dataset.say) });
// ---------- controls ----------
back.addEventListener('click',function(){
  if(view==='sector'){ location.hash='#/'; return }
  var t=R&&(view==='zoom'||view==='room')&&(R.parent||R.backTo);
  location.hash=t?roomHref(B,t):(view==='room'?sectorHref(homeOf(B).slug):'#/') });
$('#hl').addEventListener('click',toggleHL);
$('#labMode').addEventListener('click',function(){ setLabelMode(labelMode==='always'?'hover':'always') });
function toggleHL(){ var on=!stage.classList.contains('hl'); stage.classList.toggle('hl',on); $('#hl').setAttribute('aria-pressed',on) }
$('#fs').addEventListener('click',toggleFS);
function toggleFS(){ var d=document; if(!d.fullscreenElement){ (app.requestFullscreen||app.webkitRequestFullscreen||function(){}).call(app) } else { (d.exitFullscreen||d.webkitExitFullscreen).call(d) } }
document.addEventListener('fullscreenchange',function(){ $('#fs').title=document.fullscreenElement?'Exit full screen (F)':'Full screen (F)'; setTimeout(fit,50) });
document.addEventListener('keydown',function(e){
  if(e.key==='Escape'){ if(!cardWrap.hidden){closeCard();e.preventDefault()} return }
  if(!cardWrap.hidden||e.ctrlKey||e.metaKey||e.altKey)return;
  if(e.key==='h'||e.key==='H')toggleHL(); else if(e.key==='l'||e.key==='L')$('#labMode').click(); else if(e.key==='f'||e.key==='F')toggleFS();
  else if(e.key==='Backspace'&&(view==='room'||view==='zoom'||view==='sector')){back.click();e.preventDefault()}
});
function route(){ closeCard(); delete scroller.dataset.centred; stage.classList.remove('hl'); $('#hl').setAttribute('aria-pressed','false');
  var m=location.hash.match(/^#\/([a-z0-9_]+)(?:\/([a-z0-9_]+))?$/), bld=m&&m[1];
  if(bld==='quartier'){ if(m[2]&&MAP.sectors[m[2]]) renderSector(m[2]); else location.replace('#/'); return }
  if(!bld||!REG[bld]){ renderMap(); return }
  loadData(bld,function(ok){
    var D=ok&&window.VILLAGE_DATA[bld], key=m[2]||bld;
    var Rk=D&&D.rooms[key], ok2=Rk&&(!m[2]||(key!==bld&&(Rk.parent?!!D.rooms[Rk.parent]&&!D.rooms[Rk.parent].parent:(D.roomList||[]).some(function(r){return r.key===key}))));
    if(!ok2){ if(location.hash!=='#/')location.replace('#/'); else renderMap(); return }
    renderRoom(bld,key);
  });
}
var loading={};
function loadData(bld,cb){
  window.VILLAGE_DATA=window.VILLAGE_DATA||{};
  if(window.VILLAGE_DATA[bld]){ cb(true); return }
  if(loading[bld]){ loading[bld].push(cb); return }
  loading[bld]=[cb];
  var sc=document.createElement('script'); sc.src='data/'+bld+'.js'; sc.async=true;
  function done(ok){ var l=loading[bld]; delete loading[bld]; l.forEach(function(f){f(ok)}) }
  sc.onload=function(){done(true)}; sc.onerror=function(){sc.remove(); done(false)};
  document.head.appendChild(sc);
}
window.addEventListener('hashchange',route);
applyLabelMode();
route();
probeAll(function(){ if(view==='map')renderMap(); else if(view==='sector')renderSector(curSector) });
})();
