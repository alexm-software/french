// Le Village extras: search, recall mode, progress and review, words list and export, conversations,
// level filter, settings, help, card additions and offline install. Loaded after app.js and built only on
// its small API (window.Village); nothing here changes a painting or where a word lives.
(function(){
'use strict';
var V=window.Village; if(!V) return;
var $=function(s,e){return (e||document).querySelector(s)};
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function load(k,d){ try{ var v=localStorage.getItem(k); return v?JSON.parse(v):d }catch(e){ return d } }
function save(k,v){ try{ localStorage.setItem(k,JSON.stringify(v)) }catch(e){} }
var LEVELS=['A1','A2','B1','B2','C1','C2'];
var S=load('village.settings',{rate:0.85,level:'all'}); V.rate=S.rate;
var P=load('village.progress',{}); // id -> {b: box 0-5, d: due time (ms), n: times graded}
var DAY=864e5, GAP=[0,1,3,7,16,35];
var recall=false, review=null, find=null, XM=[], XA=[]; // XM/XA: menu items and after-menu hooks added by practice.js
var card=$('#card'), cardWrap=$('#cardWrap'), stage=V.stage(), app=$('#app');

// ---------- data loading ----------
var scripts={};
function need(src,cb){ if(scripts[src]===true){cb();return} if(scripts[src]){scripts[src].push(cb);return}
  scripts[src]=[cb]; var sc=document.createElement('script'); sc.src=src; sc.async=true;
  sc.onload=function(){var l=scripts[src]; scripts[src]=true; l.forEach(function(f){f()})};
  sc.onerror=function(){var l=scripts[src]; delete scripts[src]; l.forEach(function(f){f(true)})};
  document.head.appendChild(sc) }
function withIndex(cb){ need('data/index.js',function(){cb(window.V2_INDEX||[])}) }
function hrefFor(b,k,id){ return V.roomHref(b,k)+(id?'?w='+id:'') }

// ---------- progress ----------
function grade(id,g){ // g: 2 knew, 1 almost, 0 no
  var p=P[id]||{b:0,d:0,n:0}, now=Date.now();
  if(g===2){ p.b=Math.min(5,p.b+1); p.d=now+GAP[p.b]*DAY }
  else if(g===1){ p.b=Math.max(1,p.b); p.d=now+DAY }
  else { p.b=0; p.d=now+10*6e4 }
  p.n=(p.n||0)+1; P[id]=p; save('village.progress',P); updateBadge() }
function due(){ var now=Date.now(); return Object.keys(P).filter(function(id){return P[id].d<=now}) }
function known(id){ return P[id]&&P[id].b>=2 }

// ---------- header buttons ----------
var right=$('.strip-right');
function mkBtn(id,icon,title,label){ var b=document.createElement('button'); b.id=id; b.className='btn icon'; b.title=title;
  b.innerHTML='<span aria-hidden="true">'+icon+'</span><span class="sr">'+label+'</span>'; right.insertBefore(b,right.firstChild); return b }
var menuBtn=mkBtn('menuBtn','☰','Menu: recall mode, review, words, settings, help (M)','Menu');
var searchBtn=mkBtn('searchBtn','⌕','Search for a word (/)','Search');
var badge=document.createElement('span'); badge.className='duebadge'; badge.hidden=true; menuBtn.appendChild(badge);
function updateBadge(){ var n=due().length; badge.hidden=!n; badge.textContent=n>99?'99+':n }
updateBadge();
var recallTag=document.createElement('div'); recallTag.id='recallTag'; recallTag.hidden=true; $('#viewport').appendChild(recallTag);

// ---------- panels (share the card dialog) ----------
function panel(html,cls){ card.className=cls||''; card.innerHTML='<button class="x" data-close aria-label="Close">×</button>'+html;
  cardWrap.hidden=false; card.scrollTop=0; card.focus() }
cardWrap.addEventListener('click',function(e){ var a=e.target.closest('[data-act]'); if(a){ e.preventDefault(); ACT[a.dataset.act](a) } });
V.onCard.push(function(){ card.className='' });

// ---------- menu ----------
function menu(){
  var h=V.here(), inRoom=h.view==='room'||h.view==='zoom', n=due().length;
  var key=inRoom?h.bld+'/'+h.key:null;
  var html='<h2 class="ptitle">Menu</h2><div class="menu">';
  html+='<button data-act="recall" class="mi"><b>'+(recall?'Leave recall mode':'Recall mode')+'</b><span>Labels hide. Tap an object and name it in French, then check yourself. (R)</span></button>';
  if(inRoom) html+='<button data-act="find" class="mi"><b>Find it</b><span>A word is called out; tap the object it belongs to.</span></button>';
  html+='<button data-act="review" class="mi"'+(n?'':' disabled')+'><b>Review '+(n?'('+n+' due)':'(nothing due)')+'</b><span>Walks you back to each due word, in its own room.</span></button>';
  if(inRoom) html+='<button data-act="words" class="mi"><b>Words in this room</b><span>The list, with your progress; export to Anki or print.</span></button>';
  XM.forEach(function(f){ html+=f(h,key,inRoom)||'' });
  html+='<button data-act="hl" class="mi"><b>Show what you can click</b><span>Outlines everything you can click; choose it again to turn it off. (H)</span></button>';
  html+='<button data-act="settings" class="mi"><b>Settings</b><span>Speech speed, word level, progress.</span></button>';
  html+='<button data-act="help" class="mi"><b>How the village works</b><span>Sides, berets, mirrors, flags and keys. (?)</span></button>';
  html+='</div>';
  panel(html,'panel');
  XA.forEach(function(f){ f(h,key,inRoom) });
}
menuBtn.addEventListener('click',menu);

// ---------- help ----------
function help(){
  panel('<h2 class="ptitle">How the village works</h2><div class="help">'+
  '<p>Every word lives in a place where you would meet it. Walk in through the painted doors, click anything, and its card opens.</p>'+
  '<h3>Where things stand</h3><ul><li><b>Feminine nouns</b> (la, une) stand on the <b>left</b> of every room; <b>masculine nouns</b> (le, un) on the <b>right</b>.</li>'+
  '<li><b>Adjectives and adverbs</b> stand in the middle band: they have no gender of their own.</li>'+
  '<li>A <b>magnifier badge</b> 🔍 opens a close-up (a desk, a shelf); painted doors lead to other rooms.</li></ul>'+
  '<h3>Verbs: Monsieur Verbe</h3><ul><li>Every verb is acted out by a mime. His <b>beret</b> gives the group: <span class="bdot" style="background:#d8322f"></span> red = -er, <span class="bdot" style="background:#3c8a3a"></span> green = -ir (nous …issons), <span class="bdot" style="background:#7b3fa0"></span> purple = -re, <span class="bdot" style="background:#e8b32a"></span> gold = irregular.</li>'+
  '<li>A <b>hand mirror</b> 🪞 means a reflexive verb (se laver). A <b>spelling change</b> badge means the stem changes in some forms (j’achète, nous achetons).</li>'+
  '<li>The verb card shows seven tenses and a <b>Patterns</b> section: the prepositions the verb takes (penser à / penser de).</li></ul>'+
  '<h3>On the cards</h3><ul><li>The <b>memory hook</b> links the sound of the word to the picture. Say it aloud.</li>'+
  '<li>A red <b>False friend</b> flag means the word does not mean what it looks like in English; amber means partly.</li></ul>'+
  '<h3>Practice</h3><ul><li><b>Recall mode</b> hides the labels: tap an object, name it, and grade yourself. <b>Review</b> brings back each word when it is due, in its own room.</li>'+
  '<li><b>Quiz</b> asks ten questions on the room: pictures, meanings, le or la, listening, verb forms and gaps in the room’s conversations.</li>'+
  '<li><b>Conversations</b> use the room’s words: tap a highlighted word to open its card, tap a line for the English, or play the whole scene.</li>'+
  '<li><b>Listening</b> plays a short paragraph; answer the questions, then read along.</li>'+
  '<li>The <b>prayer book</b> 📖 holds the common Catholic prayers in French, with English beside them.</li>'+
  '<li><b>Search</b> finds any word, French or English, and takes you to it.</li></ul>'+
  '<h3>Keys</h3><p class="keys"><kbd>/</kbd> search · <kbd>M</kbd> menu · <kbd>R</kbd> recall mode · <kbd>L</kbd> labels · <kbd>H</kbd> show clickable things · <kbd>F</kbd> full screen · <kbd>?</kbd> this help · <kbd>Esc</kbd> close</p>'+
  '</div>','panel');
  save('village.seenHelp',1);
}

// ---------- search ----------
function fold(s){ return String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[’']/g,"'") }
function search(){
  panel('<h2 class="ptitle">Search</h2><input id="sq" type="search" autocomplete="off" spellcheck="false" placeholder="A French or English word" aria-label="Search for a word"><div id="sres" class="sres" role="list"></div>','panel');
  var q=$('#sq'), out=$('#sres'); setTimeout(function(){q.focus()},30);
  out.innerHTML='<p class="small">Loading the word list…</p>';
  withIndex(function(IX){
    function run(){ var t=fold(q.value.trim()); if(!t){ out.innerHTML='<p class="small">'+IX.length+' words. Accents are optional.</p>'; return }
      var hits=[]; IX.forEach(function(r){ var fr=fold(r[1]), bare=fr.replace(/^(le |la |les |l')/,''), en=fold(r[2]);
        var sc=fr===t||bare===t?0:bare.indexOf(t)===0?1:(' '+en+' ').indexOf(' '+t)>=0?2:fr.indexOf(t)>=0?3:en.indexOf(t)>=0?4:9;
        if(sc<9) hits.push([sc,r]) });
      hits.sort(function(a,b){return a[0]-b[0]||a[1][1].length-b[1][1].length});
      out.innerHTML=hits.slice(0,40).map(function(x){ var r=x[1];
        return '<a role="listitem" class="sr1" href="'+hrefFor(r[3],r[4],r[0])+'"><b lang="fr">'+esc(r[1])+'</b> <span>'+esc(r[2])+'</span><small>'+esc(r[5])+' · '+esc(r[3].replace(/_/g,' '))+'</small></a>' }).join('')||'<p class="small">No match.</p>' }
    q.addEventListener('input',run); run();
    q.addEventListener('keydown',function(e){ if(e.key==='Enter'){ var a=out.querySelector('a'); if(a){ location.hash=a.getAttribute('href') } } });
  });
}
searchBtn.addEventListener('click',search);
cardWrap.addEventListener('click',function(e){ var a=e.target.closest('a.sr1,a.goto'); if(a){ V.closeCard() } });

// ---------- recall mode ----------
function setRecall(on){ recall=on; stage.classList.toggle('recall',on); recallTag.hidden=!on;
  recallTag.innerHTML=on?'Recall mode: tap an object and name it · <button data-x="1">leave</button>':''; }
recallTag.addEventListener('click',function(e){ if(e.target.dataset.x){ setRecall(false); stopReview(); stopFind() } });
function norm(s){ return fold(s).replace(/[.!?…]/g,'').replace(/\s+/g,' ').trim() }
function ask(it,i,onDone){
  var hw=V.headword(it), bare=it.fr;
  panel('<div class="ask"><div class="apic"><img src="'+esc(it.cardSrc||'')+'" alt="The object to name"></div>'+
    '<h2 class="ptitle">What is this in French?</h2><p class="small">'+(it.verb?'A verb: give the infinitive.':it.adj||it.adv?'No article needed.':'Include the article (le, la, l’…).')+'</p>'+
    '<form id="askf"><input id="aq" autocomplete="off" spellcheck="false" aria-label="Your answer" placeholder="Type it, or say it aloud and press Show"><button class="btn2" type="submit">Check</button> <button class="btn2 ghost" type="button" data-act="showans">Show</button></form>'+
    '<div id="ares"></div></div>','panel');
  var f=$('#askf'), res=$('#ares'); setTimeout(function(){ $('#aq').focus() },30);
  function reveal(guess){ var g=norm(guess||''), ok=g&&(g===norm(hw)||(it.lab&&g===norm(it.lab))), close=g&&!ok&&(g===norm(bare)||norm(hw).indexOf(g)>=0&&g.length>2);
    var msg=!g?'':ok?'<p class="good">✓ Right!</p>':close?'<p class="near">Almost: '+(g===norm(bare)?'remember the article.':'check the spelling.')+'</p>':'<p class="bad">Not quite.</p>';
    res.innerHTML=msg+'<p class="ans"><b lang="fr">'+esc(hw)+'</b> · '+esc(it.en)+(V.hasVoice()?' <button class="say" data-say="'+esc(hw)+'" aria-label="Listen">🔊</button>':'')+'</p>'+
      (it.hook?'<p class="small">'+esc(it.hook)+'</p>':'')+
      '<div class="grades"><span>How did you do?</span> <button data-act="g2" class="g g2">Knew it</button><button data-act="g1" class="g g1">Almost</button><button data-act="g0" class="g g0">Didn’t know</button></div>';
    if(V.hasVoice()) V.speak(hw);
    var sug=ok?2:close?1:g?0:-1; if(sug>=0) res.querySelector('.g'+sug).classList.add('sug');
    f.querySelector('button[type=submit]').disabled=true; $('#aq').disabled=true }
  f.addEventListener('submit',function(e){ e.preventDefault(); reveal($('#aq').value) });
  ACT.showans=function(){ reveal('') };
  [0,1,2].forEach(function(g){ ACT['g'+g]=function(){ grade(it.id,g); markRoom(); if(onDone) onDone(g); else V.closeCard() } });
}
stage.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('.hot,.lab'); if(!b) return;
  var R=V.here().room; if(!R) return; var i=+b.dataset.i, it=R.items[i];
  if(find){ e.stopPropagation(); e.preventDefault(); findTap(i,b); return }
  if(!recall) return;
  e.stopPropagation(); e.preventDefault();
  ask(it,i,review?function(){ nextReview(true) }:null);
},true);

// ---------- find it ----------
function stopFind(){ find=null; var t=$('#findTag'); if(t) t.remove(); stage.querySelectorAll('.hot.ok,.hot.no').forEach(function(x){x.classList.remove('ok','no')}) }
function startFind(){ V.closeCard(); var R=V.here().room; if(!R) return;
  var order=R.items.map(function(_,i){return i}).filter(function(i){return !R.items[i].noMnemonic&&!hiddenByLevel(R.items[i])});
  order.sort(function(){return Math.random()-.5});
  find={order:order,k:0,right:0,R:R}; if(!recall) setRecall(true); showFind() }
function showFind(){ var t=$('#findTag'); if(!t){ t=document.createElement('div'); t.id='findTag'; $('#viewport').appendChild(t) }
  if(find.k>=find.order.length){ t.innerHTML='Done: '+find.right+' of '+find.order.length+' first time · <button data-a="again">again</button> <button data-a="stop">stop</button>'; return }
  var it=find.R.items[find.order[find.k]], hw=V.headword(it);
  t.innerHTML='Find: <b lang="fr">'+esc(hw)+'</b>'+(V.hasVoice()?' <button data-a="say">🔊</button>':'')+' <span class="small">'+(find.k+1)+'/'+find.order.length+'</span> <button data-a="skip">skip</button> <button data-a="stop">stop</button>';
  if(V.hasVoice()) V.speak(hw);
  t.onclick=function(e){ var a=e.target.dataset.a; if(a==='stop'){stopFind()} else if(a==='skip'){find.k++;find.miss=0;showFind()} else if(a==='again'){startFind()} else if(a==='say'){V.speak(hw)} } }
function findTap(i,b){ if(find.k>=find.order.length) return; var want=find.order[find.k], hot=stage.querySelector('.hot[data-i="'+i+'"]');
  if(i===want){ if(!find.miss) find.right++; grade(find.R.items[i].id,find.miss?1:2); hot.classList.add('ok'); setTimeout(function(){hot.classList.remove('ok')},700); find.k++; find.miss=0; showFind() }
  else { find.miss=1; hot.classList.add('no'); setTimeout(function(){hot.classList.remove('no')},600) } }

// ---------- review: walk back to each due word ----------
function stopReview(){ review=null; var t=$('#revTag'); if(t) t.remove(); stage.querySelectorAll('.hot.target').forEach(function(x){x.classList.remove('target')}) }
function startReview(){ var ids=due(); if(!ids.length){ V.closeCard(); return }
  withIndex(function(IX){ var where={}; IX.forEach(function(r){ if(!where[r[0]]) where[r[0]]=r });
    var list=ids.filter(function(id){return where[id]}).map(function(id){return where[id]});
    list.sort(function(a,b){ return (a[3]+a[4]).localeCompare(b[3]+b[4]) }); // room by room
    review={list:list,k:0}; setRecall(true); V.closeCard(); goReview() }) }
function goReview(){ if(!review) return; if(review.k>=review.list.length){ var n=review.list.length; stopReview(); setRecall(false); panel('<h2 class="ptitle">Review done</h2><p>'+n+' word'+(n>1?'s':'')+' reviewed. They will come back when they are due.</p>','panel'); return }
  var r=review.list[review.k], h=V.here(), target=V.roomHref(r[3],r[4]);
  if(h.bld===r[3]&&h.key===r[4]) markTarget(); else location.hash=target }
function markTarget(){ if(!review) return; var r=review.list[review.k], R=V.here().room; if(!R) return;
  var i=-1; R.items.forEach(function(x,j){ if(x.id===r[0]) i=j });
  stage.querySelectorAll('.hot.target').forEach(function(x){x.classList.remove('target')});
  var hot=i>=0&&stage.querySelector('.hot[data-i="'+i+'"]'); if(hot){ hot.classList.add('target'); try{hot.scrollIntoView({block:'nearest',inline:'center'})}catch(e){} }
  var t=$('#revTag'); if(!t){ t=document.createElement('div'); t.id='revTag'; $('#viewport').appendChild(t) }
  t.innerHTML='Review '+(review.k+1)+'/'+review.list.length+': name the glowing object · <button data-a="skip">skip</button> <button data-a="stop">stop</button>';
  t.onclick=function(e){ var a=e.target.dataset.a; if(a==='stop'){ stopReview(); setRecall(false) } else if(a==='skip'){ nextReview(false) } } }
function nextReview(){ if(!review) return; review.k++; V.closeCard(); goReview() }

// ---------- level filter ----------
function hiddenByLevel(it){ if(!S.level||S.level==='all'||!it.cefr) return false; return LEVELS.indexOf(it.cefr)>LEVELS.indexOf(S.level) }
function applyLevel(){ var R=V.here().room; if(!R) return;
  R.items.forEach(function(it,i){ var h=hiddenByLevel(it);
    [stage.querySelector('.hot[data-i="'+i+'"]'),stage.querySelector('.lab[data-i="'+i+'"]'),document.getElementById('ov'+i)].forEach(function(el){ if(el) el.classList.toggle('lvlhide',h) }) }) }

// ---------- words in this room, export ----------
function words(){
  var h=V.here(), R=h.room; if(!R) return;
  var rows=R.items.map(function(it,i){ var p=P[it.id], st=!p?'':p.b>=2?'known':'learning';
    return '<li class="'+(hiddenByLevel(it)?'dim':'')+'"><a href="#" data-act="open" data-i="'+i+'"><b lang="fr">'+esc(V.headword(it))+'</b>'+(recall?'':' <span>'+esc((it.en||'').split(/[;(]/)[0])+'</span>')+'</a>'+(it.cefr?'<small>'+esc(it.cefr)+'</small>':'')+(st?'<i class="st '+st+'">'+(st==='known'?'known':'learning')+'</i>':'')+'</li>' }).join('');
  var k=R.items.filter(function(it){return known(it.id)}).length;
  panel('<h2 class="ptitle">'+esc(R.name)+'</h2><p class="small">'+R.items.length+' words · '+k+' known'+(recall?' · English hidden in recall mode':'')+'</p><ol class="wlist">'+rows+'</ol>'+
    '<p class="wbtns"><button class="btn2" data-act="csv">Export for Anki (.tsv)</button> <button class="btn2 ghost" data-act="print">Print</button></p>','panel');
}
function csv(){ var h=V.here(), R=h.room; if(!R) return;
  var lines=R.items.map(function(it){ return [V.headword(it),it.en,it.ipa,it.say,(it.ex||[])[0],(it.ex||[])[1],it.hook,R.name].map(function(x){return String(x||'').replace(/[\t\n]+/g,' ')}).join('\t') });
  var blob=new Blob(['#separator:tab\n#columns:French\tEnglish\tIPA\tSay\tExample\tExample (English)\tMemory hook\tRoom\n'+lines.join('\n')+'\n'],{type:'text/tab-separated-values'});
  var a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='le-village-'+h.bld+'-'+h.key+'.tsv'; document.body.appendChild(a); a.click(); setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},500) }

// ---------- settings ----------
function settings(){
  var nP=Object.keys(P).length, nK=Object.keys(P).filter(known).length;
  panel('<h2 class="ptitle">Settings</h2><div class="set">'+
    '<label>Speech speed <input id="srate" type="range" min="0.6" max="1.1" step="0.05" value="'+S.rate+'"> <span id="srv">'+S.rate+'</span></label>'+
    '<label>Show words up to <select id="slev"><option value="all">every level</option>'+LEVELS.map(function(l){return '<option'+(S.level===l?' selected':'')+'>'+l+'</option>'}).join('')+'</select></label>'+
    '<p class="small">Words above the chosen level are hidden in every room (labels and click areas).</p>'+
    '<p>Progress: '+nP+' words practiced, '+nK+' known, '+due().length+' due now. <button class="btn2 ghost" data-act="reset">Reset progress</button></p>'+
    '<p class="small">Progress and settings are kept in this browser only.</p></div>','panel');
  $('#srate').addEventListener('input',function(e){ S.rate=+e.target.value; V.rate=S.rate; $('#srv').textContent=S.rate; save('village.settings',S) });
  $('#slev').addEventListener('change',function(e){ S.level=e.target.value; save('village.settings',S); applyLevel() });
}

var ACT={
  recall:function(){ setRecall(!recall); V.closeCard() }, find:function(){ startFind() }, review:function(){ startReview() },
  words:words, hl:function(){ V.closeCard(); var b=$('#hl'); if(b) b.click() }, settings:settings, help:help, csv:csv, print:function(){ window.print() },
  reset:function(){ if(confirmReset()) { P={}; save('village.progress',P); updateBadge(); settings() } },
  open:function(a){ var R=V.here().room, it=R&&R.items[+a.dataset.i]; if(!it) return; if(recall) ask(it,+a.dataset.i,null); else V.openCard(it) },
  prev:function(){ step(-1) }, next:function(){ step(1) }, k2:function(a){ grade(a.dataset.id,2); a.parentNode.innerHTML='<span class="small">Marked as known.</span>'; markRoom() },
  k0:function(a){ grade(a.dataset.id,0); a.parentNode.innerHTML='<span class="small">It will come back in review.</span>'; markRoom() }
};
// small API for practice.js (quizzes, conversations, listening, prayer book)
window.VillageX={panel:panel,grade:grade,ACT:ACT,esc:esc,hrefFor:hrefFor,known:known,settings:S,hiddenByLevel:hiddenByLevel,need:need,
  withIndex:withIndex,fold:fold,markRoom:function(){markRoom()},menuItems:XM,afterMenu:XA,menu:function(){menu()}};
function confirmReset(){ var b=card.querySelector('[data-act="reset"]'); if(b&&!b.dataset.sure){ b.dataset.sure=1; b.textContent='Click again to erase all progress'; return false } return true }

// ---------- card additions ----------
var cur=null;
function step(d){ var R=V.here().room; if(!R||!cur) return; var i=R.items.indexOf(cur); if(i<0) return;
  for(var n=1;n<=R.items.length;n++){ var j=(i+d*n+R.items.length*2)%R.items.length; if(!hiddenByLevel(R.items[j])){ V.openCard(R.items[j]); return } } }
V.onCard.push(function(it){
  cur=it;
  var en=card.querySelector('.en'); if(en&&it.cefr) en.insertAdjacentHTML('beforeend',' <span class="lvl" title="CEFR level">'+esc(it.cefr)+'</span>');
  var gram=card.querySelector('.gram'); if(gram&&!it.verb&&!it.adj&&!it.adv&&(it.g==='f'||it.g==='m')) gram.insertAdjacentHTML('beforeend',' · <span class="side">stands on the '+(it.g==='f'?'left':'right')+'</span>');
  var pic=card.querySelector('.pic'); if(pic){ pic.title='Tap to enlarge'; pic.addEventListener('click',function(){ pic.classList.toggle('big') }) }
  var R=V.here().room, inRoom=R&&R.items.indexOf(it)>=0;
  var p=P[it.id], foot='<div class="cfoot">';
  if(inRoom) foot+='<button class="btn2 ghost" data-act="prev" aria-label="Previous word">‹ prev</button>';
  foot+='<span class="kn">'+(p&&p.b>=2?'<span class="small">You know this one.</span>':'<button class="btn2 ghost" data-act="k2" data-id="'+esc(it.id)+'">I know this</button> <button class="btn2 ghost" data-act="k0" data-id="'+esc(it.id)+'">Practice it</button>')+'</span>';
  if(inRoom) foot+='<button class="btn2 ghost" data-act="next" aria-label="Next word">next ›</button>';
  card.insertAdjacentHTML('beforeend',foot+'</div><div class="also" hidden></div>');
  withIndex(function(IX){ if(cur!==it) return; var h=V.here(), other=IX.filter(function(r){return r[0]===it.id&&!(r[3]===h.bld&&r[4]===h.key)});
    if(other.length){ var a=card.querySelector('.also'); a.hidden=false; a.innerHTML='Also in: '+other.map(function(r){return '<a class="goto" href="'+hrefFor(r[3],r[4],r[0])+'">'+esc(r[3].replace(/_/g,' ')+(r[4]!==r[3]?' · '+r[4].replace(/_/g,' '):''))+'</a>'}).join(', ') } });
});

// ---------- room hooks ----------
function markRoom(){ var R=V.here().room; if(!R) return; R.items.forEach(function(it,i){ var o=document.getElementById('ov'+i), hot=stage.querySelector('.hot[data-i="'+i+'"]'); if(hot) hot.classList.toggle('known',known(it.id)) }) }
V.onRoom.push(function(){ applyLevel(); markRoom(); if(recall) stage.classList.add('recall'); if(review) markTarget(); if(find&&find.R!==V.here().room) stopFind() });
V.onView.push(function(){ if(find) stopFind() });

// ---------- keys ----------
document.addEventListener('keydown',function(e){
  if(e.ctrlKey||e.metaKey||e.altKey) return; var t=e.target, typing=t&&(t.tagName==='INPUT'||t.tagName==='SELECT'||t.tagName==='TEXTAREA');
  if(typing) return;
  if(e.key==='/'){ e.preventDefault(); search() }
  else if(!cardWrap.hidden) return;
  else if(e.key==='m'||e.key==='M') menu(); else if(e.key==='r'||e.key==='R') setRecall(!recall); else if(e.key==='?') help();
});

// ---------- first visit, offline ----------
// first-visit help: only if the visitor is still on the village map and has not clicked, tapped or typed yet
// (it used to pop up 0.9 s after load over whatever page they had already opened and swallow their next click)
if(!load('village.seenHelp',0)){ var helpT=setTimeout(function(){ if(cardWrap.hidden&&(location.hash==='#/'||location.hash===''||location.hash==='#')) help() },900);
  var noHelp=function(){ clearTimeout(helpT); ['pointerdown','keydown','hashchange'].forEach(function(ev){ window.removeEventListener(ev,noHelp,true) }) };
  ['pointerdown','keydown','hashchange'].forEach(function(ev){ window.addEventListener(ev,noHelp,true) }) }
// service worker: check for a new sw.js on every load; when a new one takes over a page that an older one
// controlled (a returning visitor after a deploy), reload once so paintings already on screen are not stale
if('serviceWorker' in navigator && (location.protocol==='https:'||location.hostname==='localhost')){
  var hadSW=!!navigator.serviceWorker.controller, swReloaded=false;
  navigator.serviceWorker.addEventListener('controllerchange',function(){ if(hadSW&&!swReloaded){ swReloaded=true; location.reload() } });
  navigator.serviceWorker.register('sw.js',{updateViaCache:'none'}).then(function(reg){ reg.update() }).catch(function(){}) }
})();
