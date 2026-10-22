(function(){
'use strict';
var D=window.VILLAGE, R=D.rooms.boulangerie;
var MAP={image:'assets/map/village.jpg',
 // polygons in the 1280x720 painting's pixel space (viewBox), so they stay aligned at any size
 live:{id:'boulangerie',name:'La boulangerie',pts:'22,418 55,366 180,340 229,404 222,440 233,470 233,522 150,530 100,524 22,506',tag:[128,338],door:[150,470]},
 soon:[
  {name:"L'église",pts:'88,14 312,14 312,288 88,288',tag:[205,14]},
  {name:'La mairie',pts:'432,40 688,40 688,205 432,205',tag:[560,40]},
  {name:"L'école",pts:'735,40 965,40 965,160 735,160',tag:[850,40]},
  {name:'Le moulin',pts:'1012,8 1128,8 1128,158 1012,158',tag:[1070,10]},
  {name:'La place et la fontaine',pts:'540,280 690,280 690,372 540,372',tag:[615,282]},
  {name:'Le café',pts:'283,360 486,360 486,520 283,520',tag:[384,362]},
  {name:'Le marché',pts:'892,212 1228,300 1228,448 892,330',tag:[1060,238]},
  {name:'La gare',pts:'955,416 1190,416 1190,604 955,604',tag:[1072,418]},
  {name:'Le port',pts:'515,560 745,560 745,705 515,705',tag:[630,562]}
 ]};
var $=function(s,e){return (e||document).querySelector(s)};
var stage=$('#stage'), scroller=$('#scroller'), blur=$('#blur'), back=$('#back'), app=$('#app');
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
  stage.style.width=Math.round(w)+'px'; stage.style.height=Math.round(h)+'px';
  scroller.classList.toggle('pan',pan);
  var hint=$('#panHint'); hint.hidden=!pan;
  if(pan&&!scroller.dataset.centred){ignoreScroll=true;scroller.scrollLeft=(w-vw)*(view==='map'?0.05:0.35);scroller.dataset.centred=1;hint.style.opacity=1;setTimeout(function(){ignoreScroll=false},300)}
}
window.addEventListener('resize',fit);
var ignoreScroll=false;
scroller.addEventListener('scroll',function(){if(ignoreScroll)return;var h=$('#panHint');if(!h.hidden)h.style.opacity=0},{passive:true});
// ---------- map ----------
function renderMap(){
  view='map'; document.title='Le Village · French vocabulary memory village';
  back.hidden=true; blur.style.backgroundImage='url('+MAP.image+')';
  var h='<img class="bg" src="'+MAP.image+'" alt="Cartoon map of the French village: church, town hall, school, windmill, market, café, station, port and the purple boulangerie with a giant baguette on its roof">';
  h+='<svg viewBox="0 0 1280 720" preserveAspectRatio="none" aria-label="Village map">';
  MAP.soon.forEach(function(b,i){h+='<polygon class="bld soon" data-i="'+i+'" points="'+b.pts+'"><title>'+esc(b.name)+' (bientôt)</title></polygon>'});
  var L=MAP.live;
  h+='<a href="#/'+L.id+'" class="lnk" aria-label="Enter '+esc(L.name)+'"><polygon class="bld live" tabindex="-1" points="'+L.pts+'"></polygon></a></svg>';
  h+='<div class="door" style="left:'+pct(L.door[0]/12.8)+';top:'+pct(L.door[1]/7.2)+'" aria-hidden="true">➜</div>';
  h+='<div class="tag live" id="tagLive" style="left:'+pct(L.tag[0]/12.8)+';top:'+pct(L.tag[1]/7.2)+'">'+esc(L.name)+'</div>';
  h+='<div class="tag" id="tagSoon"></div>';
  stage.innerHTML=h;
  var poly=$('.bld.live',stage), tl=$('#tagLive'), ts=$('#tagSoon');
  var lnk=$('a.lnk',stage);
  function on(){tl.classList.add('show');poly.classList.add('hot')} function off(){tl.classList.remove('show');poly.classList.remove('hot')}
  lnk.addEventListener('mouseenter',on); lnk.addEventListener('mouseleave',off); lnk.addEventListener('focus',on); lnk.addEventListener('blur',off);
  stage.querySelectorAll('.bld.soon').forEach(function(p){
    var b=MAP.soon[+p.dataset.i];
    function show(){ts.innerHTML=esc(b.name)+'<small>bientôt</small>';ts.style.left=pct(b.tag[0]/12.8);ts.style.top=pct(Math.max(b.tag[1],60)/7.2);ts.classList.add('show')}
    p.addEventListener('mouseenter',show); p.addEventListener('mouseleave',function(){ts.classList.remove('show')});
    p.addEventListener('click',function(){show();clearTimeout(p._t);p._t=setTimeout(function(){ts.classList.remove('show')},1600)});
  });
  fit();
}
// ---------- room ----------
function renderRoom(){
  view='room'; document.title=R.name+' · Le Village';
  back.hidden=false; $('#backLabel').textContent='Le village'; back.title='Back to the village map';
  blur.style.backgroundImage='url('+R.image+')';
  var h='<img class="bg" src="'+R.image+'" alt="Inside the boulangerie: yellow walls, a blue door, a big stone oven and a long wooden counter">';
  h+='<div class="sign" aria-hidden="true"><span class="board">Boulangerie</span></div>';
  R.items.forEach(function(it,i){
    var g=it.img,b=it.box;
    h+='<img class="ov" id="ov'+i+'" src="assets/room/placed/'+it.id+'.webp" alt="" style="left:'+pct(g[0])+';top:'+pct(g[1])+';width:'+pct(g[2])+';height:'+pct(g[3])+'">';
    h+='<button class="hot" data-i="'+i+'" style="left:'+pct(b[0])+';top:'+pct(b[1])+';width:'+pct(b[2])+';height:'+pct(b[3])+'" aria-label="'+esc(headword(it))+': '+esc(it.en)+'" title="'+esc(headword(it))+'"></button>';
  });
  stage.innerHTML=h;
  stage.querySelectorAll('.hot').forEach(function(btn){
    var ov=$('#ov'+btn.dataset.i);
    btn.addEventListener('mouseenter',function(){ov.classList.add('on')});
    btn.addEventListener('mouseleave',function(){ov.classList.remove('on')});
    btn.addEventListener('focus',function(){ov.classList.add('on')});
    btn.addEventListener('blur',function(){ov.classList.remove('on')});
    btn.addEventListener('click',function(){openCard(R.items[+btn.dataset.i],btn)});
  });
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
  if(it.verb) h+='<div class="gram beret">'+beretSvg(BERET[it.beret])+' '+esc(GROUP[it.beret])+'</div>';
  else h+='<div class="gram">'+(it.g==='f'?'feminine':'masculine')+' noun · '+esc(it.ind)+' '+esc(it.fr)+(it.plural?' · plural: '+esc(it.plural):'')+(it.fem?' · woman: '+esc(it.fem):'')+'</div>';
  h+='</div></div>';
  h+='<div class="sec"><h3>Memory hook</h3><p>'+esc(it.hook)+'</p>'+(it.note?'<div class="note">'+esc(it.note)+'</div>':'')+'</div>';
  if(it.verb){
    h+='<div class="sec"><h3>Present tense</h3><table class="conj">'+it.conj.map(function(r){return '<tr><td>'+esc(r[0])+'</td><td>'+esc(r[1])+'</td></tr>'}).join('')+'</table>'+(it.conj_note?'<div class="small">'+esc(it.conj_note)+'</div>':'')+'</div>';
  }
  h+='<div class="sec ex"><h3>Example</h3><p class="fr">'+esc(it.ex[0])+(sp?' <button class="say" data-say="'+esc(it.ex[0])+'" aria-label="Listen to the example">🔊</button>':'')+'</p><p class="tr">'+esc(it.ex[1])+'</p></div>';
  card.innerHTML=h; cardWrap.hidden=false; card.scrollTop=0; card.focus();
}
function closeCard(){ if(cardWrap.hidden)return; cardWrap.hidden=true; if('speechSynthesis' in window)speechSynthesis.cancel(); if(lastFocus&&lastFocus.focus)lastFocus.focus() }
cardWrap.addEventListener('click',function(e){ var t=e.target;
  if(t.closest('[data-close]'))closeCard(); var s=t.closest('[data-say]'); if(s)speak(s.dataset.say) });
// ---------- controls ----------
back.addEventListener('click',function(){ location.hash='#/' });
$('#hl').addEventListener('click',toggleHL);
function toggleHL(){ var on=!stage.classList.contains('hl'); stage.classList.toggle('hl',on); $('#hl').setAttribute('aria-pressed',on) }
$('#fs').addEventListener('click',toggleFS);
function toggleFS(){ var d=document; if(!d.fullscreenElement){ (app.requestFullscreen||app.webkitRequestFullscreen||function(){}).call(app) } else { (d.exitFullscreen||d.webkitExitFullscreen).call(d) } }
document.addEventListener('fullscreenchange',function(){ $('#fs').title=document.fullscreenElement?'Exit full screen (F)':'Full screen (F)'; setTimeout(fit,50) });
document.addEventListener('keydown',function(e){
  if(e.key==='Escape'){ if(!cardWrap.hidden){closeCard();e.preventDefault()} return }
  if(!cardWrap.hidden||e.ctrlKey||e.metaKey||e.altKey)return;
  if(e.key==='h'||e.key==='H')toggleHL(); else if(e.key==='f'||e.key==='F')toggleFS();
  else if(e.key==='Backspace'&&view==='room'){location.hash='#/';e.preventDefault()}
});
function route(){ closeCard(); delete scroller.dataset.centred; stage.classList.remove('hl'); $('#hl').setAttribute('aria-pressed','false');
  if(location.hash==='#/boulangerie') renderRoom(); else renderMap(); }
window.addEventListener('hashchange',route);
route();
})();
