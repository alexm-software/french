(function(){
'use strict';
var MAP={image:'assets/map/village.jpg',
 // polygons in the 1280x720 painting's pixel space (viewBox), so they stay aligned at any size
 live:[
  {id:'boulangerie',name:'La boulangerie',pts:'22,418 55,366 180,340 229,404 222,440 233,470 233,522 150,530 100,524 22,506',tag:[128,338],door:[150,470]},
  {id:'cafe',name:'Le café',pts:'285,447 322,404 415,352 440,400 482,465 500,515 490,560 400,585 300,580 280,520',tag:[385,356],door:[392,508]},
  {id:'eglise',name:"L'église",pts:'80,140 125,88 228,60 247,2 268,60 285,82 320,165 320,240 300,282 185,282 80,228',tag:[205,62],door:[262,232]}
 ],
 soon:[
  {name:'La mairie',pts:'432,40 688,40 688,205 432,205',tag:[560,40]},
  {name:"L'école",pts:'735,40 965,40 965,160 735,160',tag:[850,40]},
  {name:'Le moulin',pts:'1012,8 1128,8 1128,158 1012,158',tag:[1070,10]},
  {name:'La place et la fontaine',pts:'540,280 690,280 690,372 540,372',tag:[615,282]},
  {name:'Le marché',pts:'892,212 1228,300 1228,448 892,330',tag:[1060,238]},
  {name:'La gare',pts:'955,416 1190,416 1190,604 955,604',tag:[1072,418]},
  {name:'Le port',pts:'515,560 745,560 745,705 515,705',tag:[630,562]}
 ]};
var $=function(s,e){return (e||document).querySelector(s)};
var stage=$('#stage'), scroller=$('#scroller'), blur=$('#blur'), back=$('#back'), app=$('#app');
var curTense='present';
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
function fit(){
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
  if(pan&&!scroller.dataset.centred){ignoreScroll=true;scroller.scrollLeft=(w-vw)*(view==='map'?0.05:0.35);scroller.dataset.centred=1;hint.style.opacity=1;setTimeout(function(){ignoreScroll=false},300)}
}
window.addEventListener('resize',fit);
document.addEventListener('pointerdown',function(e){lastPointer=e.pointerType||'mouse'},true);
document.addEventListener('keydown',function(){lastPointer='key'},true);
var ignoreScroll=false;
scroller.addEventListener('scroll',function(){if(ignoreScroll)return;var h=$('#panHint');if(!h.hidden)h.style.opacity=0},{passive:true});
// ---------- map ----------
function renderMap(){
  view='map'; document.title='Le Village · French vocabulary memory village';
  back.hidden=true; blur.style.backgroundImage='url('+MAP.image+')';
  var h='<img class="bg" src="'+MAP.image+'" alt="Cartoon map of the French village: the stone church with its bell tower, town hall, school, windmill, market, station, port, the café with its red-and-white awning and the purple boulangerie with a giant baguette on its roof">';
  h+='<svg viewBox="0 0 1280 720" preserveAspectRatio="none" aria-label="Village map">';
  MAP.soon.forEach(function(b,i){h+='<polygon class="bld soon" data-i="'+i+'" points="'+b.pts+'"><title>'+esc(b.name)+' (bientôt)</title></polygon>'});
  MAP.live.forEach(function(L,i){
    h+='<a href="#/'+L.id+'" class="lnk" data-i="'+i+'" aria-label="Enter '+esc(L.name)+'"><polygon class="bld live" tabindex="-1" points="'+L.pts+'"></polygon></a>';
  });
  h+='</svg>';
  MAP.live.forEach(function(L,i){
    h+='<div class="door" style="left:'+pct(L.door[0]/12.8)+';top:'+pct(L.door[1]/7.2)+'" aria-hidden="true">➜</div>';
    h+='<div class="tag live" id="tagLive'+i+'" style="left:'+pct(L.tag[0]/12.8)+';top:'+pct(L.tag[1]/7.2)+'">'+esc(L.name)+'</div>';
  });
  h+='<div class="tag" id="tagSoon"></div>';
  stage.innerHTML=h;
  var ts=$('#tagSoon');
  stage.querySelectorAll('a.lnk').forEach(function(lnk){
    var poly=$('.bld.live',lnk), tl=$('#tagLive'+lnk.dataset.i);
    function on(){tl.classList.add('show');poly.classList.add('hot')} function off(){tl.classList.remove('show');poly.classList.remove('hot')}
    lnk.addEventListener('mouseenter',on); lnk.addEventListener('mouseleave',off); lnk.addEventListener('focus',on); lnk.addEventListener('blur',off);
  });
  stage.querySelectorAll('.bld.soon').forEach(function(p){
    var b=MAP.soon[+p.dataset.i];
    function show(){ts.innerHTML=esc(b.name)+'<small>bientôt</small>';ts.style.left=pct(b.tag[0]/12.8);ts.style.top=pct(Math.max(b.tag[1],60)/7.2);ts.classList.add('show')}
    p.addEventListener('mouseenter',show); p.addEventListener('mouseleave',function(){ts.classList.remove('show')});
    p.addEventListener('click',function(){show();clearTimeout(p._t);p._t=setTimeout(function(){ts.classList.remove('show')},1600)});
  });
  fit();
}
// ---------- room / zoom ----------
var R=null, B=null;
function renderRoom(bld,key){
  B=bld; var D=window.VILLAGE_DATA[bld]; R=D.rooms[key]; view=R.parent?'zoom':'room'; document.title=R.name+' · Le Village';
  back.hidden=false;
  if(R.parent){ $('#backLabel').textContent=D.rooms[R.parent].name; back.title='Back to '+D.rooms[R.parent].name; }
  else { $('#backLabel').textContent='Le village'; back.title='Back to the village map'; }
  blur.style.backgroundImage='url('+R.image+')';
  var h='<img class="bg" src="'+R.image+'" alt="'+esc(R.alt||'')+'">';
  if(R.sign){ var g=R.sign.box; h+='<img class="signimg" src="'+R.sign.src+'" alt="Sign: '+esc(R.sign.text)+'" style="left:'+pct(g[0]/12.8)+';top:'+pct(g[1]/7.2)+';width:'+pct(g[2]/12.8)+'">'; }
  R.items.forEach(function(it,i){
    var g=it.img,b=it.box,l=it.label;
    h+='<img class="ov" id="ov'+i+'" src="'+R.placed+it.id+'.webp" alt="" style="left:'+pct(g[0])+';top:'+pct(g[1])+';width:'+pct(g[2])+';height:'+pct(g[3])+'">';
    h+='<button class="hot" data-i="'+i+'" style="left:'+pct(b[0])+';top:'+pct(b[1])+';width:'+pct(b[2])+';height:'+pct(b[3])+'" aria-label="'+esc(headword(it))+': '+esc(it.en)+'"></button>';
    h+='<button class="lab'+(it.verb?' verb':'')+'" data-i="'+i+'" tabindex="-1" aria-hidden="true" style="left:'+pct(l[0])+';top:'+pct(l[1])+'">'+esc(headword(it))+'</button>';
  });
  R.zooms.forEach(function(z){
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
  stage.addEventListener('click',function(){ disarm() });
  applyLabelMode();
  fit();
}
function headword(it){ if(it.verb) return it.fr; var a=it.art; return a==="l'"? "l'"+it.fr : a+' '+it.fr }
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
  var h='<button class="x" data-close aria-label="Close">×</button><div class="head"><div class="pic"><img src="assets/words/'+it.id+'.webp" alt=""></div><div class="hw">';
  h+='<h2 id="cardTitle">'+(it.verb?esc(it.fr):(it.art==="l'"?'<span class="art">l\u2019</span>':'<span class="art">'+esc(it.art)+' </span>')+esc(it.fr))+'</h2>';
  h+='<div class="en">'+esc(it.en)+'</div>';
  h+='<div class="pron">'+esc(it.ipa)+' · say <b>'+esc(it.say)+'</b>'+(sp?'<button class="say" data-say="'+esc(hw)+'" aria-label="Listen">🔊 Listen</button>':'')+'</div>';
  if(it.verb) h+='<div class="gram beret">'+beretSvg(BERET[it.beret])+' '+esc(GROUP[it.beret])+(it.reflexive?' · <span aria-hidden="true">🪞</span> hand mirror: reflexive verb':'')+'</div>';
  else h+='<div class="gram">'+(it.g==='f'?'feminine':'masculine')+' noun · '+esc(it.ind)+' '+esc(it.fr)+(it.plural?' · plural: '+esc(it.plural):'')+(it.fem?' · woman: '+esc(it.fem):'')+'</div>';
  h+='</div></div>';
  h+='<div class="sec"><h3>Memory hook</h3><p>'+esc(it.hook)+'</p>'+(it.note?'<div class="note">'+esc(it.note)+'</div>':'')+'</div>';
  var exH='<div class="sec ex"><h3>Example</h3><p class="fr">'+esc(it.ex[0])+(sp?' <button class="say" data-say="'+esc(it.ex[0])+'" aria-label="Listen to the example">🔊</button>':'')+'</p><p class="tr">'+esc(it.ex[1])+'</p></div>';
  h+=exH;
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
back.addEventListener('click',function(){ location.hash=(view==='zoom'&&R&&R.parent)?'#/'+B:'#/' });
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
  else if(e.key==='Backspace'&&(view==='room'||view==='zoom')){back.click();e.preventDefault()}
});
function route(){ closeCard(); delete scroller.dataset.centred; stage.classList.remove('hl'); $('#hl').setAttribute('aria-pressed','false');
  var m=location.hash.match(/^#\/([a-z]+)(?:\/([a-z]+))?$/), bld=m&&m[1], live=MAP.live.some(function(L){return L.id===bld});
  if(!live){ renderMap(); return }
  loadData(bld,function(ok){
    var D=ok&&window.VILLAGE_DATA[bld], key=m[2]||bld;
    if(!D||!D.rooms[key]||(m[2]&&D.rooms[key].parent!==bld)){ location.replace('#/'); return }
    renderRoom(bld,key);
  });
}
var loading={};
function loadData(bld,cb){
  window.VILLAGE_DATA=window.VILLAGE_DATA||{};
  if(window.VILLAGE_DATA[bld]){ cb(true); return }
  if(loading[bld]){ loading[bld].push(cb); return }
  loading[bld]=[cb];
  var sc=document.createElement('script'); sc.src='assets/data/'+bld+'.js'; sc.async=true;
  function done(ok){ var l=loading[bld]; delete loading[bld]; l.forEach(function(f){f(ok)}) }
  sc.onload=function(){done(true)}; sc.onerror=function(){sc.remove(); done(false)};
  document.head.appendChild(sc);
}
window.addEventListener('hashchange',route);
applyLabelMode();
route();
})();
