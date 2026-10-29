// Offline support: the app shell is cached on install; everything else (paintings, card crops, room data)
// is cached the first time it is opened, so rooms you have visited work without a connection.
// Pages are fetched network-first so a new deploy is picked up; other files cache-first.
var V='village-v2', SHELL=['./','index.html','app.js','extras.js','practice.js','style.css','icons.js','data/map.js','data/live.js','manifest.webmanifest','icon.svg'];
self.addEventListener('install',function(e){ e.waitUntil(caches.open(V).then(function(c){return c.addAll(SHELL)}).then(function(){return self.skipWaiting()})) });
self.addEventListener('activate',function(e){ e.waitUntil(caches.keys().then(function(k){return Promise.all(k.filter(function(n){return n!==V}).map(function(n){return caches.delete(n)}))}).then(function(){return self.clients.claim()})) });
self.addEventListener('fetch',function(e){ var r=e.request; if(r.method!=='GET'||new URL(r.url).origin!==location.origin) return;
  var code=/\.(html|js|css|webmanifest)$|\/$/.test(new URL(r.url).pathname);
  if(code){ e.respondWith(fetch(r).then(function(res){ var c=res.clone(); caches.open(V).then(function(x){x.put(r,c)}); return res }).catch(function(){ return caches.match(r) })) }
  else e.respondWith(caches.match(r).then(function(hit){ return hit||fetch(r).then(function(res){ if(res.ok){ var c=res.clone(); caches.open(V).then(function(x){x.put(r,c)}) } return res }) })) });
