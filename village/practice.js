// Le Village practice: room quizzes, conversations, listening passages and the prayer book.
// Loaded after extras.js and built on window.Village (app.js) and window.VillageX (extras.js).
(function(){
'use strict';
var V=window.Village, X=window.VillageX; if(!V||!X) return;
var esc=X.esc, $=function(s,e){return (e||document).querySelector(s)}, card=$('#card'), cardWrap=$('#cardWrap');
var LEVELS=['A1','A2','B1','B2','C1','C2'];
function shuffle(a){ a=a.slice(); for(var i=a.length-1;i>0;i--){ var j=Math.floor(Math.random()*(i+1)), t=a[i]; a[i]=a[j]; a[j]=t } return a }
function pick(a){ return a[Math.floor(Math.random()*a.length)] }
function uniq(a){ var s={}; return a.filter(function(x){ var k=String(x).toLowerCase(); if(s[k]) return false; s[k]=1; return true }) }
function gloss(it){ return String(it.en||'').split(/[;(]/)[0].trim() }
function panel(html){ X.panel(html,'panel') }

// ---------- data ----------
function withTalkIndex(cb){ X.need('data/talk/index.js',function(){ cb(window.V2_TALK_INDEX||{rooms:{},cast:{}}) }) }
function withTalk(bld,cb){ X.need('data/talk/'+bld+'.js',function(){ cb((window.V2_TALK||{})[bld]||{}) }) }
function withListening(cb){ X.need('data/listening.js',function(){ cb(window.V2_LISTENING||[]) }) }
function withPrayers(cb){ X.need('data/prayers.js',function(){ cb(window.V2_PRAYERS||[]) }) }
function itemById(bld,id){ var D=(window.VILLAGE_DATA||{})[bld]; if(!D) return null; var hit=null;
  Object.keys(D.rooms).forEach(function(k){ D.rooms[k].items.forEach(function(it){ if(!hit&&it.id===id) hit=it }) }); return hit }

// ---------- speech: one line, or a queue with a voice per speaker ----------
var synth=window.speechSynthesis, queue=null;
function frVoices(){ if(!synth) return []; var v=synth.getVoices().filter(function(x){return /^fr/i.test(x.lang)});
  v.sort(function(a,b){ return (/^fr[-_]FR/i.test(b.lang)?1:0)-(/^fr[-_]FR/i.test(a.lang)?1:0) }); return v }
function canSpeak(){ return !!synth&&V.hasVoice() }
function stopSpeech(){ queue=null; if(synth) synth.cancel() }
function speakOne(text,voice,rate,done){ if(!synth){ if(done) done(); return }
  var u=new SpeechSynthesisUtterance(text); u.lang='fr-FR'; if(voice) u.voice=voice; u.rate=rate||V.rate||0.85;
  u.onend=function(){ if(done) done() }; u.onerror=function(){ if(done) done() }; synth.speak(u) }
// parts: [{text, who}], onPart(i) before each part, onEnd()
function speakSeq(parts,onPart,onEnd,rate){ stopSpeech(); var q={k:0}; queue=q; var vs=frVoices(), who={}, n=0;
  function voiceFor(w){ if(!vs.length) return null; if(!(w in who)) who[w]=vs[(n++)%vs.length]; return who[w] }
  (function next(){ if(queue!==q) return; if(q.k>=parts.length){ queue=null; if(onEnd) onEnd(); return }
    var p=parts[q.k]; if(onPart) onPart(q.k); q.k++; speakOne(p.text,voiceFor(p.who||''),rate,function(){ setTimeout(next,p.pause||250) }) })() }
function sentences(t){ return (t.match(/[^.!?…]+[.!?…]+["»”]?\s*|[^.!?…]+$/g)||[t]).map(function(s){return s.trim()}).filter(Boolean) }
V.onView.push(stopSpeech);

// ---------- marking a room's words inside a French line ----------
function marked(text,spans){ if(!spans||!spans.length) return esc(text); var h='', at=0;
  spans.forEach(function(s){ if(s[0]<at) return; h+=esc(text.slice(at,s[0]))+'<button class="tw" data-w="'+esc(s[2])+'" lang="fr">'+esc(text.slice(s[0],s[1]))+'</button>'; at=s[1] });
  return h+esc(text.slice(at)) }
var backTo=null, backNow=null;
function openWord(id,back){ var h=V.here(), it=itemById(h.bld,id); if(!it) return; stopSpeech(); backTo=back; V.openCard(it) }
V.onCard.push(function(){ backNow=backTo; backTo=null; if(backNow){ card.insertAdjacentHTML('afterbegin','<button class="btn2 ghost backto" data-act="pBack">‹ Back</button>') } });
X.ACT.pBack=function(){ var f=backNow; backNow=null; if(f) f() };
cardWrap.addEventListener('click',function(e){ var w=e.target.closest('.tw'); if(w&&card.contains(w)&&w.closest('.talkview,.lisview')){ e.preventDefault(); e.stopPropagation(); openWord(w.dataset.w,curBack) } },true);
var curBack=null;

// ---------- menu ----------
X.menuItems.push(function(h,key,inRoom){ if(!inRoom) return '';
  return '<button data-act="pQuiz" class="mi"><b>Quiz this room</b><span>Ten questions: pictures, meanings, le or la, listening, verb forms, gaps in conversations.</span></button>'+
    '<button data-act="pTalks" class="mi" id="miTalks" hidden><b>Conversations</b><span>Scenes that use this room’s words. Tap a word for its card; play the whole scene.</span></button>'+
    '<button data-act="pListenRoom" class="mi" id="miListen" hidden><b>Listening</b><span>A paragraph to listen to, with questions.</span></button>' });
X.menuItems.push(function(){ return '<button data-act="pListenAll" class="mi"><b>Listening practice</b><span>Short paragraphs from around the village, by level, with questions.</span></button>'+
  '<button data-act="pBook" class="mi"><b>Prayer book 📖</b><span>The common Catholic prayers in French, with English.</span></button>' });
X.afterMenu.push(function(h,key){ if(!key) return;
  withTalkIndex(function(T){ var n=T.rooms[key]||0, b=$('#miTalks'); if(b&&n){ b.hidden=false; b.querySelector('b').textContent='Conversations ('+n+')' } });
  withListening(function(L){ var n=L.filter(function(p){return p.room===key}).length, b=$('#miListen'); if(b&&n){ b.hidden=false; b.querySelector('b').textContent='Listening ('+n+')' } }) });
X.ACT.pQuiz=function(){ roomQuiz() }; X.ACT.pTalks=function(){ talkList() };
X.ACT.pListenRoom=function(){ var h=V.here(); listenList(h.bld+'/'+h.key) }; X.ACT.pListenAll=function(){ listenList(null) };
X.ACT.pBook=function(){ book() };
var right=$('.strip-right'), bookBtn=document.createElement('button'); bookBtn.id='bookBtn'; bookBtn.className='btn icon'; bookBtn.title='Prayer book (P)';
bookBtn.innerHTML='<span aria-hidden="true">📖</span><span class="sr">Prayer book</span>'; right.insertBefore(bookBtn,$('#menuBtn')); bookBtn.addEventListener('click',function(){ book() });
document.addEventListener('keydown',function(e){ var t=e.target; if(e.ctrlKey||e.metaKey||e.altKey||(t&&/INPUT|SELECT|TEXTAREA/.test(t.tagName))||!cardWrap.hidden) return;
  if(e.key==='q'||e.key==='Q'){ var h=V.here(); if(h.room) roomQuiz() } else if(e.key==='p'||e.key==='P') book() });

// ============ QUIZ ============
function pool(R){ return R.items.filter(function(it){ return !it.noMnemonic&&!X.hiddenByLevel(it) }) }
function kind(it){ return it.verb?'verb':it.adj?'adj':it.adv?'adv':'noun' }
function buildingPool(bld){ var D=window.VILLAGE_DATA[bld], out=[]; Object.keys(D.rooms).forEach(function(k){ out=out.concat(pool(D.rooms[k])) });
  var seen={}; return out.filter(function(it){ if(seen[it.id]) return false; seen[it.id]=1; return true }) }
function distract(it,all,f,n){ var same=all.filter(function(x){return x.id!==it.id&&kind(x)===kind(it)}), other=all.filter(function(x){return x.id!==it.id&&kind(x)!==kind(it)});
  var want=f(it), opts=uniq(shuffle(same).concat(shuffle(other)).map(f)).filter(function(o){return o&&o.toLowerCase()!==want.toLowerCase()});
  return shuffle([want].concat(opts.slice(0,n||3))) }
var GEN={
  pic:function(it,all){ if(!it.cardSrc) return null; return {it:it,type:'pic',ask:'What is this in French?',img:it.cardSrc,opts:distract(it,all,V.headword),ans:V.headword(it)} },
  fr2en:function(it,all){ var g=gloss(it); if(!g) return null; return {it:it,type:'fr2en',ask:'What does this mean?',fr:V.headword(it),opts:distract(it,all,gloss),ans:g} },
  en2fr:function(it,all){ return {it:it,type:'en2fr',ask:'How do you say it in French?',en:gloss(it),opts:distract(it,all,V.headword),ans:V.headword(it)} },
  gender:function(it){ if(kind(it)!=='noun'||(it.g!=='m'&&it.g!=='f')) return null; var el=it.art==="l'"||/^l['’]/.test(it.art||'');
    var a=el?(it.g==='f'?'une':'un'):(it.g==='f'?'la':'le'), b=el?(it.g==='f'?'un':'une'):(it.g==='f'?'le':'la');
    return {it:it,type:'gender',ask:'Which one?',fr:'___ '+it.fr,opts:shuffle([a,b]),ans:a,why:(it.g==='f'?'Feminine: it stands on the left of the room.':'Masculine: it stands on the right of the room.')} },
  listen:function(it,all){ if(!canSpeak()) return null; return {it:it,type:'listen',ask:'Listen. Which word is it?',say:V.headword(it),opts:distract(it,all,V.headword),ans:V.headword(it)} },
  conj:function(it){ if(!it.verb||!it.tenses) return null; var T=it.tenses.filter(function(t){return /present|pc|futur|imparfait/.test(t.key)});
    if(!T.length) return null; var t=pick(T), rows=t.rows.filter(function(r){return r[1]}); if(rows.length<4) return null;
    var r=pick(rows), ans=r[1].split(/\s*\/\s*/)[0], opts=uniq(shuffle(rows).map(function(x){return x[1].split(/\s*\/\s*/)[0]})).filter(function(o){return o!==ans}).slice(0,3);
    return {it:it,type:'conj',ask:t.name+' of '+it.fr+' ('+gloss(it)+')',fr:r[0]+' ___',opts:shuffle([ans].concat(opts)),ans:ans} }
};
function gapQuestions(talks,all){ var out=[], byId={}; all.forEach(function(it){byId[it.id]=it});
  talks.forEach(function(d){ d.lines.forEach(function(l){ l.spans.forEach(function(s){ var it=byId[s[2]]; if(!it) return;
    var word=l.fr.slice(s[0],s[1]), others=[];
    all.forEach(function(x){ if(x.id!==it.id&&kind(x)===kind(it)) others.push(kind(x)==='noun'?x.fr:x.fr) });
    var opts=uniq(shuffle(others)).filter(function(o){return o.toLowerCase()!==word.toLowerCase()}).slice(0,3);
    if(opts.length<2) return;
    out.push({it:it,type:'gap',ask:'Fill the gap ('+esc(d.title)+')',line:l.fr.slice(0,s[0])+'_____'+l.fr.slice(s[1]),en:l.en,opts:shuffle([word].concat(opts)),ans:word}) }) }) });
  return shuffle(out) }
function makeQuiz(items,all,talks,n){ n=n||10; var qs=[], used={}, gaps=talks?gapQuestions(talks,all):[], order=shuffle(items);
  var types=['pic','fr2en','en2fr','gender','listen','conj','pic','en2fr'];
  for(var k=0;qs.length<n&&k<n*4;k++){
    if(gaps.length&&k%4===3){ var g=gaps.shift(); if(!used[g.it.id+'g']){ used[g.it.id+'g']=1; qs.push(g); continue } }
    var it=order[k%order.length], t=types[(k+Math.floor(k/order.length))%types.length], q=GEN[t](it,all);
    if(!q&&it.verb) q=GEN.conj(it,all); if(!q) q=GEN.fr2en(it,all)||GEN.en2fr(it,all);
    var key=it.id+q.type; if(used[key]) continue; used[key]=1; qs.push(q) }
  return shuffle(qs) }
function roomQuiz(){ var h=V.here(), R=h.room; if(!R) return; var items=pool(R), all=items.length>=6?items:buildingPool(h.bld);
  withTalk(h.bld,function(T){ var qs=makeQuiz(items.length?items:all,all,T[h.bld+'/'+h.key]||[],Math.min(10,Math.max(5,items.length+3)));
    runQuiz(qs,R.name,function(){ roomQuiz() }) }) }
function runQuiz(qs,title,again,onFinish){ var k=0, right=0, missed=[];
  function show(){ if(k>=qs.length) return finish(); var q=qs[k], h='<div class="quiz"><p class="qhead"><b>'+esc(title)+'</b> <span class="small">'+(k+1)+' / '+qs.length+'</span></p>'+
      '<h2 class="ptitle">'+q.ask+'</h2>';
    if(q.img) h+='<div class="apic"><img src="'+esc(q.img)+'" alt="The object to name"></div>';
    if(q.fr) h+='<p class="qfr" lang="fr">'+esc(q.fr)+(canSpeak()&&q.type!=='gender'&&q.type!=='conj'?' <button class="say" data-say="'+esc(q.fr)+'" aria-label="Listen">🔊</button>':'')+'</p>';
    if(q.en) h+= q.type==='gap'?'<p class="qfr" lang="fr">'+esc(q.line)+'</p><p class="small">'+esc(q.en)+'</p>':'<p class="qfr">'+esc(q.en)+'</p>';
    if(q.type==='listen') h+='<p><button class="btn2" data-act="qSay">🔊 Play again</button></p>';
    h+='<div class="qopts">'+q.opts.map(function(o,i){ return '<button class="qo" data-act="qAns" data-i="'+i+'"'+(q.type!=='fr2en'&&q.type!=='en2fr'||q.type==='en2fr'?' lang="fr"':'')+'>'+esc(o)+'</button>' }).join('')+'</div><div id="qres"></div></div>';
    panel(h); if(q.type==='listen') V.speak(q.say) }
  X.ACT.qSay=function(){ var q=qs[k]; if(q) V.speak(q.say) };
  X.ACT.qAns=function(a){ var q=qs[k], o=q.opts[+a.dataset.i], ok=o===q.ans; if(card.querySelector('.qo.right')) return;
    card.querySelectorAll('.qo').forEach(function(b){ b.disabled=true; var t=q.opts[+b.dataset.i]; if(t===q.ans) b.classList.add('right'); else if(b===a) b.classList.add('wrong') });
    if(ok) right++; else missed.push(q.it); X.grade(q.it.id,ok?2:0); X.markRoom();
    var hw=V.headword(q.it);
    $('#qres').innerHTML='<p class="'+(ok?'good':'bad')+'">'+(ok?'✓ Right!':'Not quite: '+esc(q.ans))+'</p>'+(q.why?'<p class="small">'+esc(q.why)+'</p>':'')+
      '<p class="small"><b lang="fr">'+esc(hw)+'</b> · '+esc(gloss(q.it))+(canSpeak()?' <button class="say" data-say="'+esc(hw)+'" aria-label="Listen">🔊</button>':'')+'</p>'+
      '<p><button class="btn2" data-act="qNext">'+(k+1<qs.length?'Next ›':'See your score')+'</button></p>';
    if(canSpeak()&&q.type!=='listen') V.speak(q.type==='conj'||q.type==='gap'?q.ans:hw);
    var nb=card.querySelector('[data-act="qNext"]'); if(nb) nb.focus() };
  X.ACT.qNext=function(){ k++; show() };
  function finish(){ if(onFinish) return onFinish(right,qs.length,missed);
    var h='<div class="quiz"><h2 class="ptitle">'+right+' / '+qs.length+'</h2><p>'+(right===qs.length?'Perfect! ':right>=qs.length*0.7?'Well done. ':'Keep going. ')+'Your answers count toward review: missed words come back soon.</p>';
    if(missed.length) h+='<h3>To review</h3><ul class="wlist">'+uniq(missed.map(function(it){return it.id})).map(function(id){ var it=missed.filter(function(x){return x.id===id})[0];
      return '<li><b lang="fr">'+esc(V.headword(it))+'</b> <span>'+esc(gloss(it))+'</span></li>' }).join('')+'</ul>';
    h+='<p class="wbtns"><button class="btn2" data-act="qAgain">New quiz</button> <button class="btn2 ghost" data-close>Close</button></p></div>';
    panel(h) }
  X.ACT.qAgain=function(){ if(again) again() };
  show() }
X.quiz=runQuiz;

// ============ CONVERSATIONS ============
function talkList(){ var h=V.here(), key=h.bld+'/'+h.key; stopSpeech();
  withTalk(h.bld,function(T){ var L=T[key]||[];
    var html='<h2 class="ptitle">Conversations</h2><p class="small">'+esc(h.room?h.room.name:'')+' · highlighted words are this room’s: tap one for its card.</p><div class="menu">';
    L.forEach(function(d,i){ html+='<button class="mi" data-act="tOpen" data-i="'+i+'"><b lang="fr">'+esc(d.title)+'</b> <small class="lvl">'+esc(d.cefr||'')+'</small><span>'+esc(d.premise||'')+'</span></button>' });
    panel(html+'</div>'); X.ACT.tOpen=function(a){ openTalk(L,+a.dataset.i) } }) }
function openTalk(L,i){ var d=L[i], cast=(window.V2_TALK_INDEX||{}).cast||{}; stopSpeech(); curBack=function(){ openTalk(L,i) };
  var h='<div class="talkview"><p class="qhead"><button class="btn2 ghost" data-act="tList">‹ All conversations</button> <small class="lvl">'+esc(d.cefr||'')+'</small></p><h2 class="ptitle" lang="fr">'+esc(d.title)+'</h2><p class="small">'+esc(d.premise||'')+'</p>'+
    '<p class="tbtns">'+(canSpeak()?'<button class="btn2" data-act="tPlay">▶ Play the scene</button> ':'')+'<button class="btn2 ghost" data-act="tEn">Show all English</button> <button class="btn2 ghost" data-act="tCheck">Check yourself</button></p><ol class="lines">'+
    d.lines.map(function(l,n){ return '<li data-n="'+n+'"><span class="who">'+esc(l.speaker)+'</span> <span class="fr" lang="fr" tabindex="0">'+marked(l.fr,l.spans)+'</span>'+
      (canSpeak()?' <button class="say" data-say="'+esc(l.fr)+'" aria-label="Listen">🔊</button>':'')+'<span class="en" hidden>'+esc(l.en)+'</span></li>' }).join('')+'</ol></div>';
  panel(h);
  card.querySelectorAll('.lines .fr').forEach(function(s){ function t(e){ if(e&&e.target.closest('.tw')) return; var en=s.parentNode.querySelector('.en'); en.hidden=!en.hidden }
    s.addEventListener('click',t); s.addEventListener('keydown',function(ev){ if(ev.key==='Enter') t() }) });
  X.ACT.tList=function(){ stopSpeech(); talkList() };
  X.ACT.tEn=function(a){ var show=a.textContent.indexOf('Show')===0; card.querySelectorAll('.lines .en').forEach(function(e){ e.hidden=!show }); a.textContent=show?'Hide English':'Show all English' };
  X.ACT.tPlay=function(a){ if(queue){ stopSpeech(); a.textContent='▶ Play the scene'; card.querySelectorAll('.lines li').forEach(function(x){x.classList.remove('now')}); return }
    a.textContent='■ Stop';
    speakSeq(d.lines.map(function(l){ return {text:l.fr,who:l.speaker,pause:450} }),function(n){ card.querySelectorAll('.lines li').forEach(function(x){ x.classList.toggle('now',+x.dataset.n===n) }); var li=card.querySelector('.lines li.now'); if(li) li.scrollIntoView({block:'nearest'}) },
      function(){ a.textContent='▶ Play the scene'; card.querySelectorAll('.lines li').forEach(function(x){x.classList.remove('now')}) }) };
  X.ACT.tCheck=function(){ stopSpeech(); talkCheck(L,i) } }
function talkCheck(L,i){ var d=L[i], h=V.here(), qs=[], room=h.room?pool(h.room):[], all=room.length>=4?room:buildingPool(h.bld);
  var g=gapQuestions([d],all).slice(0,2); qs=qs.concat(g);
  var lines=shuffle(d.lines.filter(function(l){return l.fr.split(' ').length>=4}));
  lines.slice(0,2).forEach(function(l){ var others=shuffle(d.lines.filter(function(x){return x!==l})).map(function(x){return x.en}).slice(0,3);
    qs.push({it:null,type:'meaning',ask:'What does this line mean?',fr:l.fr,opts:shuffle([l.en].concat(others)),ans:l.en}) });
  var speakers=uniq(d.lines.map(function(l){return l.speaker}));
  if(speakers.length>1){ var l=pick(lines.length?lines:d.lines); qs.push({it:null,type:'who',ask:'Who says this?',fr:l.fr,opts:shuffle(speakers).slice(0,4).concat([]),ans:l.speaker});
    var q=qs[qs.length-1]; if(q.opts.indexOf(q.ans)<0) q.opts[0]=q.ans }
  qs=qs.map(function(q){ if(!q.it) q.it={id:'',fr:'',en:''}; return q });
  runQuizLite(qs,d.title,function(){ openTalk(L,i) }) }
// like runQuiz, but questions may have no word behind them (no grading for those)
function runQuizLite(qs,title,back){ var k=0, right=0;
  function show(){ if(k>=qs.length){ panel('<div class="quiz"><h2 class="ptitle">'+right+' / '+qs.length+'</h2><p class="wbtns"><button class="btn2" data-act="qlBack">‹ Back</button></p></div>'); return }
    var q=qs[k], h='<div class="quiz"><p class="qhead"><b lang="fr">'+esc(title)+'</b> <span class="small">'+(k+1)+' / '+qs.length+'</span></p><h2 class="ptitle">'+q.ask+'</h2>';
    if(q.type==='gap') h+='<p class="qfr" lang="fr">'+esc(q.line)+'</p><p class="small">'+esc(q.en)+'</p>'; else if(q.fr) h+='<p class="qfr" lang="fr">'+esc(q.fr)+(canSpeak()?' <button class="say" data-say="'+esc(q.fr)+'" aria-label="Listen">🔊</button>':'')+'</p>';
    h+='<div class="qopts">'+q.opts.map(function(o,i){ return '<button class="qo" data-act="qlAns" data-i="'+i+'">'+esc(o)+'</button>' }).join('')+'</div><div id="qres"></div></div>'; panel(h) }
  X.ACT.qlAns=function(a){ var q=qs[k], ok=q.opts[+a.dataset.i]===q.ans; if(card.querySelector('.qo.right')) return;
    card.querySelectorAll('.qo').forEach(function(b){ b.disabled=true; if(q.opts[+b.dataset.i]===q.ans) b.classList.add('right'); else if(b===a) b.classList.add('wrong') });
    if(ok) right++; if(q.it&&q.it.id) X.grade(q.it.id,ok?2:0);
    $('#qres').innerHTML='<p class="'+(ok?'good':'bad')+'">'+(ok?'✓ Right!':'Not quite.')+'</p><p><button class="btn2" data-act="qlNext">'+(k+1<qs.length?'Next ›':'See your score')+'</button></p>' };
  X.ACT.qlNext=function(){ k++; show() }; X.ACT.qlBack=back; show() }

// ============ LISTENING ============
function shuffledQs(p){ var q2=p.questions.map(function(q){ var ord=shuffle(q.options.map(function(_,i){return i}));
    return {q:q.q,explain:q.explain,options:ord.map(function(i){return q.options[i]}),answer:ord.indexOf(q.answer)} });
  var o={}; Object.keys(p).forEach(function(k){o[k]=p[k]}); o.questions=q2; return o }
function listenList(roomKey){ stopSpeech();
  withListening(function(L){ var list=roomKey?L.filter(function(p){return p.room===roomKey}):L;
    var html='<h2 class="ptitle">Listening'+(roomKey?'':' practice')+'</h2><p class="small">Listen first, answer the questions, then read along. '+(canSpeak()?'':'This browser has no French voice, so the text is shown instead.')+'</p>';
    if(!list.length) html+='<p>No passages yet.</p>';
    LEVELS.forEach(function(lv){ var g=list.filter(function(p){return p.cefr===lv}); if(!g.length) return;
      html+='<h3>'+lv+'</h3><div class="menu">'+g.map(function(p){ var done=X.settings.heard&&X.settings.heard[p.id];
        return '<button class="mi" data-act="lOpen" data-id="'+esc(p.id)+'"><b lang="fr">'+esc(p.title)+'</b>'+(done!=null?' <small class="st known">'+done+'/'+p.questions.length+'</small>':'')+'<span>'+esc(p.room?p.room.split('/')[0].replace(/_/g,' '):'')+'</span></button>' }).join('')+'</div>' });
    panel(html); X.ACT.lOpen=function(a){ openPassage(L.filter(function(p){return p.id===a.dataset.id})[0],roomKey) } }) }
function openPassage(p0,roomKey){ stopSpeech(); var p=shuffledQs(p0), sents=sentences(p.fr), showText=!canSpeak(), rate=V.rate||0.85;
  curBack=function(){ openPassage(p0,roomKey) };
  function textHtml(){ // the paragraph, with room words linked, split into sentences for highlighting while it plays
    var out='', at=0; sents.forEach(function(s,n){ var a=p.fr.indexOf(s,at); if(a<0) a=at; var b=a+s.length; at=b;
      var sp=(p.spans||[]).filter(function(x){return x[0]>=a&&x[1]<=b}).map(function(x){return [x[0]-a,x[1]-a,x[2]]});
      out+='<span class="sent" data-n="'+n+'">'+marked(s,sp)+'</span> ' }); return out }
  var h='<div class="lisview"><p class="qhead"><button class="btn2 ghost" data-act="lList">‹ All passages</button> <small class="lvl">'+esc(p.cefr)+'</small></p><h2 class="ptitle" lang="fr">'+esc(p.title)+'</h2>'+
    (canSpeak()?'<p class="tbtns"><button class="btn2" data-act="lPlay">▶ Listen</button> <button class="btn2 ghost" data-act="lSlow" aria-pressed="false">🐢 Slower</button> <button class="btn2 ghost" data-act="lText">Show the text</button></p>':'')+
    '<div class="ptext" lang="fr"'+(showText?'':' hidden')+'>'+textHtml()+'</div><div class="pen" hidden>'+esc(p.en)+'</div>'+
    '<h3>Questions</h3><ol class="lq">'+p.questions.map(function(q,n){ return '<li><p>'+esc(q.q)+'</p><div class="qopts">'+q.options.map(function(o,i){ return '<button class="qo" data-act="lAns" data-q="'+n+'" data-i="'+i+'">'+esc(o)+'</button>' }).join('')+'</div><p class="lexp small" hidden>'+esc(q.explain||'')+'</p></li>' }).join('')+'</ol>'+
    '<p id="lscore"></p></div>';
  panel(h); var answered={}, right=0;
  X.ACT.lList=function(){ stopSpeech(); listenList(roomKey) };
  X.ACT.lText=function(a){ var t=card.querySelector('.ptext'), e=card.querySelector('.pen'); t.hidden=!t.hidden; e.hidden=t.hidden; a.textContent=t.hidden?'Show the text':'Hide the text' };
  X.ACT.lSlow=function(a){ var on=a.getAttribute('aria-pressed')!=='true'; a.setAttribute('aria-pressed',on); rate=on?Math.max(0.55,(V.rate||0.85)-0.25):(V.rate||0.85) };
  X.ACT.lPlay=function(a){ if(queue){ stopSpeech(); a.textContent='▶ Listen'; hl(-1); return } a.textContent='■ Stop';
    speakSeq(sents.map(function(s){return {text:s,who:'n',pause:350}}),hl,function(){ a.textContent='▶ Listen again'; hl(-1) },rate) };
  function hl(n){ card.querySelectorAll('.sent').forEach(function(s){ s.classList.toggle('now',+s.dataset.n===n) }) }
  X.ACT.lAns=function(a){ var qn=+a.dataset.q, q=p.questions[qn]; if(answered[qn]!=null) return; var ok=+a.dataset.i===q.answer; answered[qn]=ok; if(ok) right++;
    var li=card.querySelectorAll('.lq > li')[qn]; li.querySelectorAll('.qo').forEach(function(b){ b.disabled=true; if(+b.dataset.i===q.answer) b.classList.add('right'); else if(b===a) b.classList.add('wrong') });
    var ex=li.querySelector('.lexp'); if(ex.textContent) ex.hidden=false;
    if(Object.keys(answered).length===p.questions.length){ X.settings.heard=X.settings.heard||{}; X.settings.heard[p.id]=right; try{ localStorage.setItem('village.settings',JSON.stringify(X.settings)) }catch(e){}
      var t=card.querySelector('.ptext'), e=card.querySelector('.pen'); t.hidden=false; e.hidden=false; var b=card.querySelector('[data-act="lText"]'); if(b) b.textContent='Hide the text';
      $('#lscore').innerHTML='<b>'+right+' / '+p.questions.length+'</b>. The text and its English are shown above; tap a highlighted word for its card.' } } }

// ============ PRAYER BOOK ============
function book(page){ stopSpeech();
  withPrayers(function(PR){ if(!PR.length){ panel('<p>The prayer book is empty.</p>'); return }
    if(page==null){ var h='<div class="book"><div class="bcover"><p class="bcross" aria-hidden="true">✠</p><h2 lang="fr">Livre de prières</h2><p>Prayer book</p></div>'+
        '<ol class="btoc">'+PR.map(function(p,i){ return '<li><a href="#" data-act="bPage" data-i="'+i+'"><b lang="fr">'+esc(p.title_fr)+'</b> <span>'+esc(p.title_en)+'</span></a></li>' }).join('')+'</ol>'+
        '<p class="small bnote">These are the common Catholic prayers in older public-domain French and English wordings, not the current copyrighted liturgical translations. Each page names its source.</p></div>';
      panel(h); X.ACT.bPage=function(a){ book(+a.dataset.i) }; return }
    var p=PR[page], showEn=X.settings.bookEn!==false;
    function lines(t){ return esc(t).replace(/\s(V\.|R\.)\s/g,'<br>$1 ').replace(/\n+/g,'<br>') }
    var h='<div class="book bpage"><p class="qhead"><button class="btn2 ghost" data-act="bToc">‹ Contents</button> <span class="small">'+(page+1)+' / '+PR.length+'</span></p>'+
      '<h2 class="ptitle" lang="fr">'+esc(p.title_fr)+'</h2><p class="small">'+esc(p.title_en)+'</p>'+
      '<p class="tbtns">'+(canSpeak()?'<button class="btn2" data-act="bSay">🔊 Listen</button> ':'')+'<button class="btn2 ghost" data-act="bEn">'+(showEn?'Hide':'Show')+' English</button></p>'+
      '<div class="bcols'+(showEn?'':' fronly')+'"><div class="bfr" lang="fr">'+lines(p.fr)+'</div><div class="ben">'+lines(p.en||'')+'</div></div>'+
      '<details class="bsrc"><summary>Source</summary><p class="small">'+esc(p.source||'')+'</p></details>'+
      '<p class="bnav"><button class="btn2 ghost" data-act="bPrev"'+(page?'':' disabled')+'>‹ '+(page?esc(PR[page-1].title_fr):'')+'</button><button class="btn2 ghost" data-act="bNext"'+(page<PR.length-1?'':' disabled')+'>'+(page<PR.length-1?esc(PR[page+1].title_fr):'')+' ›</button></p></div>';
    panel(h);
    X.ACT.bToc=function(){ book() }; X.ACT.bPrev=function(){ book(page-1) }; X.ACT.bNext=function(){ book(page+1) };
    X.ACT.bEn=function(){ X.settings.bookEn=!showEn; try{ localStorage.setItem('village.settings',JSON.stringify(X.settings)) }catch(e){} book(page) };
    X.ACT.bSay=function(a){ if(queue){ stopSpeech(); a.textContent='🔊 Listen'; return } a.textContent='■ Stop';
      speakSeq(sentences(p.fr.replace(/\b[VR]\.\s/g,'')).map(function(s){return {text:s,who:'n',pause:300}}),null,function(){ a.textContent='🔊 Listen' },Math.max(0.7,(V.rate||0.85)-0.05)) } }) }
X.book=book;
})();
