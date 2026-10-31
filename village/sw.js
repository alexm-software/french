// Offline support: the app shell is cached on install; everything else (paintings, card crops, room data)
// is cached the first time it is opened, so rooms you have visited work without a connection.
// Every GET is network-first (revalidated with the server, so a repainted image that keeps its filename is
// picked up at once; page navigations are fetched as-is, a navigate Request cannot take an init); the cache is
// only the offline fallback.
// Bump V whenever a deploy changes an existing image/card (check_v2.py --cache-base enforces this at pack time):
// the new worker deletes every older cache on activate and takes over open pages at once.
var V='village-v4', SHELL=['./','index.html','app.js','extras.js','practice.js','style.css','icons.js','data/map.js','data/live.js','manifest.webmanifest','icon.svg'];
self.addEventListener('install',function(e){ e.waitUntil(caches.open(V).then(function(c){return c.addAll(SHELL.map(function(u){return new Request(u,{cache:'reload'})}))}).then(function(){return self.skipWaiting()})) });
self.addEventListener('activate',function(e){ e.waitUntil(caches.keys().then(function(k){return Promise.all(k.filter(function(n){return n!==V}).map(function(n){return caches.delete(n)}))}).then(function(){return self.clients.claim()})) });
self.addEventListener('fetch',function(e){ var r=e.request; if(r.method!=='GET'||new URL(r.url).origin!==location.origin) return;
  e.respondWith(fetch(r.mode==='navigate'?r:new Request(r,{cache:'no-cache'})).then(function(res){ if(res.ok){ var c=res.clone(); caches.open(V).then(function(x){x.put(r,c)}) } return res })
    .catch(function(){ return caches.match(r).then(function(hit){ return hit||Response.error() }) })) });
