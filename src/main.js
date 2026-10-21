const BASE = import.meta.env.BASE_URL;
const PROGRESS_KEY = "memory-village-v1";

const state = {
  index: null,
  routeId: "suggested",
  menu: false,
  talkLang: "fr",
  showEn: true,
  quiz: null,
  speechNote: "",
  signpost: false,
};

const cache = new Map();

function url(path) {
  return BASE + String(path).replace(/^\//, "");
}

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[ch]));
}

async function getJSON(path) {
  if (cache.has(path)) return cache.get(path);
  const pending = fetch(url(path)).then((res) => {
    if (!res.ok) throw new Error(path);
    return res.json();
  });
  cache.set(path, pending);
  try {
    return await pending;
  } catch (error) {
    cache.delete(path);
    throw error;
  }
}

function loadProgress() {
  try {
    return JSON.parse(localStorage.getItem(PROGRESS_KEY)) || { quizzes: {} };
  } catch {
    return { quizzes: {} };
  }
}

function saveProgress(data) {
  localStorage.setItem(PROGRESS_KEY, JSON.stringify(data));
}

function quizRecord(id) {
  return loadProgress().quizzes?.[id] || null;
}

function recordQuiz(id, correct, total) {
  const all = loadProgress();
  all.quizzes = all.quizzes || {};
  const prev = all.quizzes[id] || { attempts: 0, correct: 0, asked: 0, best: 0 };
  prev.attempts += 1;
  prev.correct += correct;
  prev.asked += total;
  prev.best = Math.max(prev.best || 0, total ? correct / total : 0);
  prev.last = { correct, total, at: Date.now() };
  all.quizzes[id] = prev;
  saveProgress(all);
}

function speak(text, lang) {
  return new Promise((resolve) => {
    const synth = window.speechSynthesis;
    if (!synth || !text) {
      resolve({ ok: false, reason: "unsupported" });
      return;
    }
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = lang;
    utter.rate = 0.92;
    const voices = synth.getVoices();
    const wanted = lang.slice(0, 2).toLowerCase();
    const voice = voices.find((item) => item.lang.toLowerCase().startsWith(wanted));
    if (voice) utter.voice = voice;
    let settled = false;
    const finish = (ok, extra = {}) => {
      if (settled) return;
      settled = true;
      resolve({ ok, voice: Boolean(voice), ...extra });
    };
    utter.onend = () => finish(true);
    utter.onerror = (event) => finish(false, { reason: event.error || "error" });
    synth.cancel();
    synth.resume();
    synth.speak(utter);
    window.setTimeout(() => finish(false, { reason: "timeout" }), 20000);
  });
}

function speechHint(lang) {
  const synth = window.speechSynthesis;
  if (!synth) return "This browser has no speech playback. The respelling is here so you can still say the word.";
  const wanted = lang.slice(0, 2).toLowerCase();
  const voice = synth.getVoices().find((item) => item.lang.toLowerCase().startsWith(wanted));
  if (!voice && wanted === "fr") {
    return "No French voice is installed in this browser. You can still read the respelling aloud.";
  }
  return "";
}

function parseRoute() {
  const raw = (location.hash || "#/").slice(1) || "/";
  const path = raw.split("?")[0];
  return path.split("/").filter(Boolean);
}

function genderClass(word) {
  if (!word || word.pos !== "noun") return "na";
  if (word.gender === "f") return "f";
  if (word.gender === "m") return "m";
  if (word.gender === "mf") return "mf";
  return "na";
}

function genderLabel(word) {
  if (word.gender === "f") return "feminine";
  if (word.gender === "m") return "masculine";
  if (word.gender === "mf") return "masculine or feminine";
  return "";
}

function shell(body, current) {
  const index = state.index;
  const open = index?.open_sectors?.[0];
  const openSector = index?.sectors?.find((sector) => sector.id === open);
  const nav = [
    ["/", "Map"],
    openSector ? [`/sector/${openSector.id}`, openSector.fr_name] : null,
    ["/prayers", "Prayers"],
    ["/about", "About"],
    ["/credits", "Credits"],
  ].filter(Boolean);
  return `
    <div class="shell">
      <header class="top ${state.menu ? "open" : ""}">
        <a class="brand" href="#/">Memory Village<small>French, kept in places</small></a>
        <button class="menu-btn" type="button" data-menu aria-expanded="${state.menu ? "true" : "false"}">Menu</button>
        <nav class="nav">
          ${nav.map(([href, label]) => `<a href="#${href}" ${current === href ? 'aria-current="page"' : ""}>${esc(label)}</a>`).join("")}
          <button class="fs-btn" type="button" data-fs>Full screen</button>
        </nav>
      </header>
      <main id="main">${body}</main>
      <footer class="site">${index?.featured?.kind === "sector"
        ? "Rue des Saveurs is painted: the café, the restaurant, and eleven alleys off the square. The other quarters are coming soon."
        : index?.featured
        ? "The upstairs of Café de la Place is a finished painting. The other rooms are coming soon."
        : "Placeholder paintings hang until the finished art arrives. Words, genders and places already follow the village plan."}</footer>
    </div>`;
}

function crumbs(items) {
  return `<nav class="crumbs">${items.map((item, index) => {
    if (!item.href || index === items.length - 1) return `<span>${esc(item.label)}</span>`;
    return `<a href="${item.href}">${esc(item.label)}</a><span aria-hidden="true">/</span>`;
  }).join("")}</nav>`;
}

function scoreLine(id) {
  const record = quizRecord(id);
  if (!record?.last) return "";
  return `<p class="meta">Quiz so far: last ${record.last.correct}/${record.last.total}, best ${Math.round((record.best || 0) * 100)}%.</p>`;
}

function mapView() {
  const index = state.index;
  const byId = Object.fromEntries(index.sectors.map((sector) => [sector.id, sector]));
  const legs = [];
  index.adjacency && Object.entries(index.adjacency).forEach(([from, tos]) => {
    tos.forEach((to) => {
      if (from < to) legs.push([from, to]);
    });
  });
  const routeIds = state.routeId === "suggested"
    ? index.route.map((step) => step.sector_id)
    : (index.alternatives.find((route) => route.id === state.routeId)?.sectors || []);
  const point = (id) => {
    const sector = byId[id];
    return sector ? [sector.x * 10, sector.y * 7.2] : [0, 0];
  };
  const lines = legs.map(([from, to]) => {
    const [x1, y1] = point(from);
    const [x2, y2] = point(to);
    return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#c3b295" stroke-width="3" />`;
  }).join("");
  let route = "";
  for (let i = 0; i < routeIds.length - 1; i += 1) {
    const [x1, y1] = point(routeIds[i]);
    const [x2, y2] = point(routeIds[i + 1]);
    route += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#7c2f38" stroke-width="5" stroke-linecap="round" />`;
  }
  const start = byId[index.start];
  const [sx, sy] = start ? point(start.id) : [0, 0];
  const pins = index.sectors.map((sector) => `
    <a class="pin ${sector.open ? "open" : "soon"}" style="left:${sector.x}%; top:${sector.y}%" href="#/sector/${sector.id}">
      <strong>${esc(sector.fr_name)}</strong>
      <em>${esc(sector.entry_level)} · ${sector.word_count}</em>
      <span class="seal">${sector.open ? "Open" : "Coming soon"}</span>
    </a>`).join("");
  const routes = [
    ["suggested", "Suggested walk"],
    ...index.alternatives.map((route) => [route.id, route.label]),
  ];
  return shell(`
    <p class="kicker">The whole village</p>
    <h1>Sixteen quarters, one walk</h1>
    <p class="lede">${esc(index.featured?.kind === "sector"
      ? "Rue des Saveurs is open. Step into the square: the café and the restaurant have doors, and the lane lists eleven short alleys. Every other quarter is still coming soon."
      : index.featured
      ? "The upstairs room of Café de la Place is hung and ready to walk. Every other room on the map is drawn, and still coming soon."
      : `${index.tagline} Rue des Saveurs is open: the café, the restaurant and the little cooking street. The other quarters are drawn on the map and still being painted.`)}</p>
    ${index.featured ? `<p><a class="btn primary" href="${index.featured.kind === "sector" ? `#/sector/${esc(index.featured.id)}` : `#/room/${esc(index.featured.id)}`}">Enter ${esc(index.featured.sign)}</a></p>` : ""}
    <div class="routes">
      ${routes.map(([id, label]) => `<button type="button" data-route="${esc(id)}" aria-pressed="${state.routeId === id ? "true" : "false"}">${esc(label)}</button>`).join("")}
    </div>
    <div class="map-wrap">
      <svg viewBox="0 0 1000 720" aria-hidden="true">
        ${lines}
        ${route}
        <polygon points="${sx - 10},${sy - 28} ${sx + 10},${sy - 28} ${sx},${sy - 48}" class="star" />
      </svg>
      ${pins}
    </div>
    <p class="note">The gold mark is where the long walk begins, in the beginner quarter. That quarter is still coming soon. The open door today is the café quarter.</p>
  `, "/");
}

function sectorView(sector) {
  const places = sector.buildings.map((building) => {
    const rooms = building.floors.reduce((sum, floor) => sum + floor.rooms.length, 0);
    const detail = building.type === "verb_street"
      ? `${building.verb_count || "Several"} verbs in ${rooms} alleys off the square. ${building.architectural_theme || ""}`
      : `${rooms} room${rooms === 1 ? "" : "s"}.`;
    const anyOpen = building.floors.some((floor) => floor.rooms.some((room) => room.open));
    const kicker = building.type === "verb_street" ? "Alleys" : "Place";
    if (!sector.open || !anyOpen) {
      return `<article class="card-link locked"><p class="kicker">${esc(kicker)}</p><h2>${esc(building.name)}</h2><p>${esc(detail)}</p><p class="meta">Coming soon</p></article>`;
    }
    if (building.type === "verb_street") {
      return `<button class="card-link" type="button" data-signpost="1"><p class="kicker">${esc(kicker)}</p><h2>${esc(building.name)}</h2><p>${esc(detail)} Choose one. It comes back to the square.</p></button>`;
    }
    return `<a class="card-link" href="#/building/${building.id}"><p class="kicker">${esc(kicker)}</p><h2>${esc(building.name)}</h2><p>${esc(detail)}</p></a>`;
  }).join("");
  const neighbors = sector.neighbors.map((neighbor) => `<a class="chip" href="#/sector/${neighbor.id}">${esc(neighbor.fr_name)}${neighbor.open ? "" : " · soon"}</a>`).join("");
  const stage = stageFor(sector.scene, [], [], sector.fr_name);
  const body = sector.open ? `
    <p class="lede">${esc(sector.description)} The café and the restaurant are the two fronts. The lane opens a signpost of short alleys. Each alley returns here.</p>
    ${stage}
    ${signpostHtml(sector)}
    ${scoreLine(`sector:${sector.id}`)}
    <div class="row">
      <a class="btn primary" href="#/quiz/sector/${sector.id}">Quiz this quarter</a>
      ${sector.prev_sector ? `<a class="chip" href="#/sector/${sector.prev_sector.id}">Previous quarter: ${esc(sector.prev_sector.fr_name)}</a>` : ""}
      ${sector.next_sector ? `<a class="chip" href="#/sector/${sector.next_sector.id}">Next quarter: ${esc(sector.next_sector.fr_name)}</a>` : ""}
    </div>
    <div class="grid places" style="margin-top:1rem">${places}</div>
    <h2 style="margin-top:1.2rem">Neighbouring quarters</h2>
    <div class="row">${neighbors}</div>
  ` : `
    <p class="lede">${esc(sector.description)}</p>
    <p>This quarter is drawn on the map. Its paintings are not hung yet, so the rooms stay closed. The café quarter is the one you can walk today.</p>
    <a class="btn primary" href="#/sector/${state.index.open_sectors[0]}">Go to the open quarter</a>
    <div class="grid places" style="margin-top:1rem">${places}</div>
    <h2 style="margin-top:1.2rem">Neighbours</h2>
    <div class="row">${neighbors}</div>
  `;
  return shell(`
    ${crumbs([{ href: "#/", label: "Map" }, { label: sector.fr_name }])}
    <p class="kicker">${sector.open ? `Open · ${esc(sector.entry_level)} · stop ${sector.order || ""}` : `Coming soon · ${esc(sector.entry_level)}`}</p>
    <h1>${esc(sector.fr_name)}</h1>
    ${sector.en_name ? `<p class="meta">${esc(sector.en_name)} · ${sector.word_count} words</p>` : ""}
    ${body}
  `, `/sector/${sector.id}`);
}

function buildingView(sector, building) {
  if (!sector.open) {
    return shell(`
      ${crumbs([{ href: "#/", label: "Map" }, { href: `#/sector/${sector.id}`, label: sector.fr_name }, { label: building.name }])}
      <h1>${esc(building.name)}</h1>
      <p>This place is in a quarter that is still being painted.</p>
      <a class="btn primary" href="#/sector/${sector.id}">Back to the quarter</a>
    `);
  }
  const floors = building.floors.map((floor) => `
    <div class="floor"><span>${esc(floor.label)}</span>
      ${floor.rooms.map((room) => room.open
        ? `<a class="chip" href="#/room/${room.id}" title="${esc(chipTitle(room))}" aria-label="${esc(chipTitle(room))}">${esc(chipLabel(room))}</a>`
        : `<span class="chip soon" title="Coming soon">${esc(chipLabel(room))} · soon</span>`).join("")}
    </div>`).join("");
  const intro = building.type === "verb_street"
    ? `<p class="lede">${esc(building.architectural_theme || "")} These are separate alleys off the square, not one walk. A mirror on a front means the verb is reflexive. The word on the door is the preposition it takes.</p>`
    : `<p class="lede">The doors on the painting open the rooms. Rooms on the ground floor hold the more ordinary words. Upstairs is for the rarer ones. Feminine nouns sit on the left, masculine nouns on the right. The colour is only on the label.</p>`;
  const stage = stageFor(building.scene, [], [], building.name);
  return shell(`
    ${crumbs([{ href: "#/", label: "Map" }, { href: `#/sector/${sector.id}`, label: sector.fr_name }, { label: building.name }])}
    <p class="kicker">${esc(sector.fr_name)}</p>
    <h1>${esc(building.name)}</h1>
    ${intro}
    ${stage}
    <div class="floors">${floors}</div>
  `, `/building/${building.id}`);
}

function fitHits() {
  const svg = document.querySelector(".stage svg");
  if (!svg) return;
  const width = svg.getBoundingClientRect().width || 320;
  const view = svg.viewBox.baseVal.width || 1280;
  const min = Math.max(56, (46 / width) * view);
  svg.querySelectorAll("[data-pad]").forEach((pad) => {
    const cx = Number(pad.dataset.cx);
    const cy = Number(pad.dataset.cy);
    const w = Math.max(Number(pad.dataset.w), min);
    const h = Math.max(Number(pad.dataset.h), min);
    pad.setAttribute("x", String(cx - w / 2));
    pad.setAttribute("y", String(cy - h / 2));
    pad.setAttribute("width", String(w));
    pad.setAttribute("height", String(h));
  });
}

function fittedSize(text, boxWidth, boxHeight, max = 48) {
  const length = Math.max(Array.from(text || "").length, 1);
  const byWidth = boxWidth / (length * 0.58);
  const byHeight = (boxHeight || boxWidth) * 0.72;
  return Math.max(12, Math.min(max, byWidth, byHeight));
}

function labelSize(text, boxWidth) {
  const length = Math.max(Array.from(text).length, 1);
  return Math.max(13, Math.min(22, (boxWidth - 8) / (length * 0.52)));
}

function chipLabel(item) {
  if (!item) return "";
  if (item.kind === "street_segment" && item.chip) return item.chip;
  return item.sign || item.name || "";
}

function chipTitle(item) {
  if (!item) return "";
  if (item.kind === "street_segment" && item.chip) return `segment ${item.chip}`;
  return item.sign || item.name || "";
}

function hashFor(target) {
  const value = String(target || "");
  if (value.endsWith("_sector")) {
    const prefix = value.slice(0, -"_sector".length);
    const sector = (state.index?.sectors || []).find((item) => item.id.startsWith(`${prefix}_`));
    return `#/sector/${sector ? sector.id : value}`;
  }
  if (value.startsWith("B")) return `#/building/${value}`;
  return `#/room/${value}`;
}

function sceneLinks(scene) {
  // Exteriors and the sector view store doors in `links`. Street paintings store
  // prev/next in `exits`. An alley never continues into the next alley: only a
  // return to the square is kept.
  const links = (scene.links || []).filter((link) => !(link.exit && String(link.target || "").startsWith("ST_")));
  const exits = scene.exits || {};
  [exits.prev, exits.next].forEach((exit) => {
    if (!exit?.target || !exit.box) return;
    const target = String(exit.target);
    if (target.startsWith("ST_")) return;
    if (links.some((link) => link.exit && link.target === target)) return;
    links.push({
      target,
      box: exit.box,
      label: "Back to the square",
      exit: true,
    });
  });
  return links;
}

function wrapLines(text, boxWidth, boxHeight) {
  const words = String(text).split(/\s+/).filter(Boolean);
  const widthOf = (value, size) => Array.from(value).length * size * 0.58;
  let size = Math.min(40, Math.max(8, boxHeight * 0.78));
  while (size >= 8) {
    const lines = [];
    let current = "";
    let fits = true;
    for (const word of words) {
      const trial = current ? `${current} ${word}` : word;
      if (widthOf(trial, size) <= boxWidth) {
        current = trial;
      } else if (!current || widthOf(word, size) > boxWidth) {
        fits = false;
        break;
      } else {
        lines.push(current);
        current = word;
      }
    }
    if (current) lines.push(current);
    if (fits && lines.length * size * 1.12 <= boxHeight + 1) return { size, lines };
    size -= 1;
  }
  return { size: 8, lines: [String(text)] };
}

function textBlock(className, text, box) {
  const wrapped = wrapLines(text, box[2] - box[0], box[3] - box[1]);
  const cx = (box[0] + box[2]) / 2;
  const lineHeight = wrapped.size * 1.12;
  const top = (box[1] + box[3]) / 2 - (wrapped.lines.length * lineHeight) / 2 + wrapped.size * 0.75;
  return wrapped.lines.map((line, index) =>
    `<text class="${className}" x="${cx.toFixed(1)}" y="${(top + index * lineHeight).toFixed(1)}" text-anchor="middle" font-size="${wrapped.size.toFixed(1)}">${esc(line)}</text>`
  ).join("");
}

function sceneMarkup(scene, words, zooms) {
  const byId = Object.fromEntries((words || []).map((word) => [word.id, word]));
  const areas = scene.text_areas || {};
  const signed = new Set(Object.keys(areas).filter((key) => key.endsWith("_sign")).map((key) => key.slice(0, -"_sign".length)));
  const parts = [];
  sceneLinks(scene).forEach((link) => {
    const [x0, y0, x1, y1] = link.box;
    const alley = String(link.target || "").startsWith("ST_cooking");
    const attr = alley ? `data-signpost="1"` : `data-target="${esc(link.target)}"`;
    const label = alley ? "The cooking alleys" : (link.label || "Open");
    const caption = link.exit
      ? `<text class="exit-label" x="${(x0 + x1) / 2}" y="${Math.min(y1 - 12, y0 + 36)}" text-anchor="middle">Back to the square</text>`
      : "";
    parts.push(`<g class="hot link${link.exit ? " exit" : ""}" ${attr} tabindex="0" role="button" aria-label="${esc(label)}"><rect class="hit" x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}"></rect>${caption}</g>`);
  });
  (scene.hotspots || []).forEach((hot) => {
    const word = byId[hot.word_id];
    const [x0, y0, x1, y1] = hot.box;
    const cx = (x0 + x1) / 2;
    const pad = `<rect class="hit pad" data-pad data-cx="${cx}" data-cy="${(y0 + y1) / 2}" data-w="${x1 - x0}" data-h="${y1 - y0}" x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}"></rect>`;
    let shape = pad;
    if (hot.polygon) shape += `<polygon class="hit" points="${hot.polygon.map((point) => point.join(",")).join(" ")}"></polygon>`;
    if (hot.zoom_id) {
      const named = (zooms || []).find((zoom) => zoom.id === hot.zoom_id);
      const label = named?.sign || hot.label || "Look closer";
      parts.push(`<g class="hot zoom" data-zoom="${esc(hot.zoom_id)}" tabindex="0" role="button" aria-label="Look closer: ${esc(label)}">${shape}<text class="lbl na" x="${cx}" y="${Math.min(y1 - 16, y0 + 36)}" text-anchor="middle" font-size="${labelSize(label, x1 - x0)}">${esc(label)}</text></g>`);
      return;
    }
    if (!word) return;
    if (hot.helper) {
      const name = hot.mirror ? `Mirror for ${word.head}` : `Memory helper for ${word.head}`;
      parts.push(`<g class="hot helper" data-word="${esc(word.id)}" tabindex="0" role="button" aria-label="${esc(name)}">${shape}</g>`);
      return;
    }
    const klass = genderClass(word);
    const hasPlaque = Boolean(areas[`${word.id}_plaque`]);
    let extra = "";
    if (hot.door_plaque && word.prepositions?.length && !hasPlaque) {
      const [a, b, c, d] = hot.door_plaque;
      extra += `<text class="prep" x="${(a + c) / 2}" y="${(b + d) / 2 + 4}" text-anchor="middle">${esc(word.prepositions.join(" · "))}</text>`;
    }
    const label = signed.has(word.id) ? "" : `<text class="lbl ${klass}" x="${cx}" y="${Math.max(22, y0 - 6)}" text-anchor="middle" font-size="${labelSize(word.head, x1 - x0).toFixed(1)}">${esc(word.head)}</text>`;
    parts.push(`<g class="hot" data-word="${esc(word.id)}" tabindex="0" role="button" aria-label="${esc(`${word.head}, ${word.gloss}`)}">${shape}${label}${extra}</g>`);
  });
  Object.entries(areas).forEach(([key, area]) => {
    const text = area.text || (key === "sign" ? scene.sign_text : "") || (key === "plaque" ? scene.plaque_text : "");
    if (!text) return;
    const box = area.text_box || area.box;
    const klass = key.endsWith("_plaque") || key === "plaque" ? "plaque" : "sign";
    parts.push(textBlock(klass, text, box));
  });
  return `<svg viewBox="0 0 ${scene.width} ${scene.height}">${parts.join("")}</svg>`;
}

function stageFor(scene, words, zooms, alt) {
  if (!scene?.image) return "";
  return `<div class="stage"><img src="${esc(url(scene.image))}" alt="${esc(alt)}">${sceneMarkup(scene, words, zooms)}</div>`;
}

function signpostHtml(sector) {
  if (!state.signpost) return "";
  const alleys = sector.alleys || [];
  return `<div class="signpost-layer">
    <article class="signpost" role="dialog" aria-labelledby="signpost-title">
      <button class="ghost" type="button" data-close-signpost>Close</button>
      <p class="kicker">Off the square</p>
      <h2 id="signpost-title">Ruelle des Gourmets</h2>
      <p>Each alley is its own short lane. It comes back here. It does not run on into the next one.</p>
      <ol class="alleys">${alleys.map((alley) => `<li><a href="#/room/${esc(alley.id)}"><strong>${esc(alley.chip)}</strong> ${esc((alley.verbs || []).join(", "))}</a></li>`).join("")}</ol>
    </article>
  </div>`;
}

function roomView(room, wordId, talk) {
  const words = room.words;
  const active = words.find((word) => word.id === wordId);
  const alley = room.kind === "street_segment";
  const floors = (room.floors || []).filter((floor) => floor.rooms.length);
  const showFloors = !alley && room.kind !== "zoom" && floors.some((floor) => floor.rooms.length > 1 || floors.length > 1);
  const floorHtml = showFloors ? `<div class="floors">${floors.map((floor) => `
    <div class="floor"><span>${esc(floor.label)}</span>
      ${floor.rooms.map((item) => {
        if (item.current) return `<span class="chip current" title="${esc(chipTitle(item))}" aria-current="true">${esc(chipLabel(item))}</span>`;
        if (!item.open) return `<span class="chip soon" title="Coming soon">${esc(chipLabel(item))} · soon</span>`;
        return `<a class="chip" href="#/room/${item.id}" title="${esc(chipTitle(item))}" aria-label="${esc(chipTitle(item))}">${esc(chipLabel(item))}</a>`;
      }).join("")}
    </div>`).join("")}</div>` : "";
  const stage = room.scene?.image ? `
    <div class="stage">
      <img src="${esc(url(room.scene.image))}" alt="${esc(room.scene.placeholder ? `Placeholder view of ${room.sign}. The finished painting will replace it.` : room.sign)}">
      ${sceneMarkup(room.scene, words, room.zooms)}
    </div>
    ${room.scene.placeholder ? `<p class="note">Placeholder scene. The finished painting will hang in this same frame. Signs and labels are set in type, not baked into the picture, so they can be corrected without repainting.</p>` : ""}
  ` : `<p class="note">This room has no painting yet. The words are listed below.</p>`;
  const list = `<ul class="wordlist">${words.map((word) => `
    <li><button type="button" data-word="${esc(word.id)}" class="${word.painted === false ? "unpainted" : ""}"><span class="${genderClass(word)}">${esc(word.head)}</span><small>${esc(word.painted === false ? "Listed, not in this painting" : word.gloss)}</small></button></li>
  `).join("")}</ul>`;
  const zooms = (room.zooms || []).map((zoom) => `<a class="btn" href="#/room/${zoom.id}">Look closer: ${esc(zoom.furniture || zoom.sign)}</a>`).join("");
  const back = room.parent
    ? `<a class="btn" href="#/room/${room.parent.id}">Step back to ${esc(room.parent.sign)}</a>`
    : alley
      ? `<a class="btn" href="#/sector/${room.sector_id}">Back to the square</a>`
      : "";
  const walk = alley ? "" : `<div class="row">
    ${room.prev ? `<a class="chip" href="#/room/${room.prev.id}">Previous: ${esc(chipTitle(room.prev))}</a>` : ""}
    ${room.next ? `<a class="chip" href="#/room/${room.next.id}">Next: ${esc(chipTitle(room.next))}</a>` : ""}
  </div>`;
  const relatedItems = (room.related || []).filter((item) => !(alley && String(item.id).startsWith("ST_")));
  const related = relatedItems.map((item) => item.open
    ? `<a class="chip" href="#/room/${item.id}">${esc(item.sign || item.name)}</a>`
    : `<span class="chip" title="Coming soon">${esc(item.name)} · soon</span>`).join("");
  const talkHtml = room.conversation ? conversationHtml(room) : "";
  const card = active ? cardLayer(active) : "";
  return shell(`
    ${crumbs([
      { href: "#/", label: "Map" },
      { href: `#/sector/${room.sector_id}`, label: room.sector_name },
      { href: `#/building/${room.building_id}`, label: room.building_name },
      { label: room.sign },
    ])}
    <p class="kicker">${esc(room.floor_label || room.kind)} · ${esc(room.cefr_band || "")}</p>
    <h1>${esc(room.sign)}</h1>
    <p class="meta">${esc(room.name)}</p>
    ${floorHtml}
    ${stage}
    <div class="row" style="margin-top:0.8rem">
      ${back}
      ${zooms}
      <a class="btn primary" href="#/quiz/room/${room.id}">Quiz this room</a>
      ${room.conversation ? `<a class="btn" href="#/room/${room.id}/talk">Conversation</a>` : ""}
    </div>
    ${scoreLine(`room:${room.id}`)}
    ${walk}
    <h2>Words in this place</h2>
    ${list}
    ${related ? `<h2>Related rooms</h2><div class="row">${related}</div>` : ""}
    ${(room.prayers || []).length ? `<h2>Prayers kept here</h2><div class="row">${room.prayers.map((prayer) => `<a class="chip" href="#/prayer/${prayer.id}">${esc(prayer.title_fr)}</a>`).join("")}</div>` : ""}
    ${(room.grammar_rules || []).length ? `<h2>Notes on the wall</h2>${room.grammar_rules.map((rule) => `<p>${esc(rule)}</p>`).join("")}` : ""}
    ${talkHtml}
    ${card}
  `, `/room/${room.id}`) + (talk ? "" : "");
}

function conversationHtml(room) {
  const conv = room.conversation;
  const lines = conv.lines.map((line, index) => `
    <article class="line" data-i="${index}" id="line-${index}">
      <div class="who">${esc(line.speaker)}</div>
      <p class="fr">${esc(state.talkLang === "fr" ? line.fr : line.en)}</p>
      ${state.showEn ? `<p class="en">${esc(state.talkLang === "fr" ? line.en : line.fr)}</p>` : ""}
    </article>`).join("");
  return `
    <section class="talk" id="talk">
      <h2>${esc(conv.title || "Conversation")}</h2>
      ${conv.premise ? `<p class="premise">${esc(conv.premise)}</p>` : ""}
      ${conv.generated ? `<p class="note">A practice dialogue built from this room’s scene and its words. When the village notes change, the lines follow.</p>` : ""}
      <div class="row">
        <button class="btn primary" type="button" data-play>Play</button>
        <button class="btn" type="button" data-stop>Stop</button>
        <button class="btn" type="button" data-lang>${state.talkLang === "fr" ? "Reading French" : "Reading English"}</button>
        <button class="btn" type="button" data-en>${state.showEn ? "Hide translation" : "Show translation"}</button>
      </div>
      <p class="note" data-speech-note>${esc(state.speechNote || speechHint(state.talkLang === "fr" ? "fr-FR" : "en-GB"))}</p>
      ${lines}
    </section>`;
}

function cardLayer(word) {
  const klass = genderClass(word);
  const picture = word.display === "museum_text"
    ? `<div class="museum-plaque"><p>${esc(word.head)}</p><p class="meta">A plaque, not a picture</p></div>`
    : word.display === "text_plain"
      ? `<div class="plain-card"><p>${esc(word.head)}</p></div>`
      : (word.hook?.scene ? `<blockquote class="scene">${esc(word.hook.scene)}</blockquote>` : "");
  const cognate = word.cognate_type === "false_cognate"
    ? `<p><span class="badge bad">False friend</span></p>${word.false_cognate_note ? `<p>${esc(word.false_cognate_note)}</p>` : ""}`
    : word.cognate_type === "true_cognate"
      ? `<p><span class="badge ok">True cognate</span> It resembles English. Still learn the gender and the exact sense.</p>${word.false_cognate_note ? `<p>${esc(word.false_cognate_note)}</p>` : ""}`
      : (word.false_cognate_note ? `<p>${esc(word.false_cognate_note)}</p>` : "");
  const links = (title, items) => {
    if (!items?.length) return "";
    return `<h3>${title}</h3><div class="row">${items.map((item) => item.open && item.room_id
      ? `<a class="chip" href="#/room/${item.room_id}/word/${item.id}">${esc(item.lemma)}</a>`
      : `<span class="chip">${esc(item.lemma)}${item.open === false ? " · soon" : ""}</span>`).join("")}</div>`;
  };
  const verb = word.pos === "verb" ? verbBlock(word) : "";
  return `
    <div class="card-layer" data-close>
      <article class="card" role="dialog" aria-labelledby="card-title">
        <div class="row"><button class="ghost" type="button" data-close-card>Close</button>
          <button class="btn" type="button" data-speak="${esc(word.head)}" data-lang="fr-FR">Listen</button>
        </div>
        <p class="kicker">${esc(word.pos)} · ${esc(word.cefr || "")}</p>
        <h2 id="card-title" class="head ${klass}">${esc(word.head)} ${word.reflexive ? mirrorIcon() : ""}</h2>
        ${genderLabel(word) ? `<p><span class="badge ${klass}">${esc(genderLabel(word))}</span>${word.gender_note ? ` ${esc(word.gender_note)}` : ""}</p>` : ""}
        ${word.plural_irregular ? `<p class="meta">Irregular plural: ${esc(word.plural_irregular)}</p>` : ""}
        <p class="meta">${esc(word.respelling || "")} ${word.ipa ? `· ${esc(word.ipa)}` : ""}</p>
        <p class="note" data-speech-note>${esc(speechHint("fr-FR"))}</p>
        <p class="lede">${esc(word.gloss)}</p>
        ${word.literal ? `<p class="meta">Literally: ${esc(word.literal)}</p>` : ""}
        ${word.register ? `<p class="meta">Register: ${esc(word.register)}</p>` : ""}
        ${cognate}
        ${word.usage_warning ? `<p class="caution">${esc(word.usage_warning)}</p>` : ""}
        <h3>The memory</h3>
        ${word.hook?.sound_alike ? `<p>Sound hook: <strong>${esc(word.hook.sound_alike)}</strong></p>` : ""}
        ${picture}
        <h3>How this memory works</h3>
        <p>${esc(word.mnemonic_explain)}</p>
        ${links("Related words", word.related)}
        ${links("Opposites", word.opposites)}
        ${verb}
        ${word.wiktionary ? `<p class="source">English gloss shortened from Wiktionary via kaikki.org, CC BY-SA 4.0.</p>` : ""}
      </article>
    </div>`;
}

function mirrorIcon() {
  return `<span class="mirror" title="Reflexive verb"><svg width="28" height="36" viewBox="0 0 28 36" aria-hidden="true"><ellipse cx="14" cy="16" rx="10" ry="14" fill="#e7eef2" stroke="#1e3a5f" stroke-width="2"/><path d="M8 8l8 16" stroke="#fff" stroke-width="2"/></svg></span>`;
}

function verbBlock(word) {
  const tables = word.conjugations;
  const tenseOrder = [
    ["present", "Présent"],
    ["passe", "Passé composé"],
    ["imparfait", "Imparfait"],
    ["futur", "Futur"],
    ["conditionnel", "Conditionnel"],
    ["imperatif", "Impératif"],
    ["subjonctif", "Subjonctif"],
  ];
  const labels = {
    present: ["je", "tu", "il/elle", "nous", "vous", "ils/elles"],
    passe: ["je", "tu", "il/elle", "nous", "vous", "ils/elles"],
    imparfait: ["je", "tu", "il/elle", "nous", "vous", "ils/elles"],
    futur: ["je", "tu", "il/elle", "nous", "vous", "ils/elles"],
    conditionnel: ["je", "tu", "il/elle", "nous", "vous", "ils/elles"],
    imperatif: ["tu", "nous", "vous"],
    subjonctif: ["je", "tu", "il/elle", "nous", "vous", "ils/elles"],
  };
  const rendered = tables ? tenseOrder.map(([key, title]) => {
    const rows = tables[key];
    if (!rows) return "";
    const names = labels[key];
    return `<h3>${title}</h3><table>${rows.map((row, index) => `<tr><th>${esc(names[index] || "")}</th><td>${esc(row)}</td></tr>`).join("")}</table>`;
  }).join("") : `<p class="note">A conjugation table for this verb is not in the bundle yet.</p>`;
  const prep = word.prepositions?.length
    ? `<p>On the door:</p><div class="door-plaque">${word.prepositions.map((item) => `<span>${esc(item)}</span>`).join("")}</div>`
    : "";
  return `
    <h3>The verb</h3>
    ${word.reflexive ? `<p>${mirrorIcon()} Reflexive${word.pronominal_form ? `: ${esc(word.pronominal_form)}` : ""}.</p>` : ""}
    ${word.auxiliary ? `<p class="meta">Auxiliary: ${esc(word.auxiliary)}</p>` : ""}
    ${prep}
    ${rendered}
  `;
}

function quizView(pack) {
  if (!state.quiz || state.quiz.packId !== `${pack.scope}:${pack.id}`) {
    state.quiz = null;
  }
  const quiz = state.quiz;
  let body;
  if (!quiz) {
    const genders = new Set(pack.items.filter((item) => item.pos === "noun" && (item.gender === "m" || item.gender === "f")).map((item) => item.gender));
    body = `
      <p class="lede">Ten questions from ${esc(pack.title)}. Your score stays in this browser.</p>
      ${scoreLine(`${pack.scope}:${pack.id}`)}
      <div class="choices">
        <button type="button" data-mode="fr-en">French → English</button>
        <button type="button" data-mode="en-fr">English → French</button>
        <button type="button" data-mode="gender" ${genders.size < 2 ? "disabled" : ""}>Gender${genders.size < 2 ? " (this set is all one gender)" : ""}</button>
        <button type="button" data-mode="listen">Listening</button>
      </div>`;
  } else if (quiz.done) {
    body = `
      <p class="score">${quiz.correct} / ${quiz.round.length}</p>
      <p>Saved on this device.</p>
      <button class="btn primary" type="button" data-again>Try again</button>`;
  } else {
    const item = quiz.round[quiz.index];
    const prompt = quiz.mode === "en-fr"
      ? item.gloss
      : quiz.mode === "gender"
        ? item.lemma
        : quiz.mode === "listen"
          ? "Listen, then choose the meaning."
          : item.head;
    body = `
      <p class="meta">${quiz.index + 1} of ${quiz.round.length} · ${esc(modeLabel(quiz.mode))}</p>
      <h2>${esc(prompt)}</h2>
      ${quiz.mode === "listen" ? `<div class="row"><button class="btn" type="button" data-replay>Play again</button>${quiz.reveal ? `<span>${esc(item.head)} · ${esc(item.respelling || "")}</span>` : ""}</div>` : ""}
      ${quiz.mode === "gender" ? `<p class="meta">le or la? If the word takes l’, the article will not tell you.</p>` : ""}
      <div class="choices">
        ${quiz.choices.map((choice, index) => `<button type="button" data-choice="${index}" class="${quiz.picked == null ? "" : choice.ok ? "good" : index === quiz.picked ? "bad" : ""}" ${quiz.picked == null ? "" : "disabled"}>${esc(choice.label)}</button>`).join("")}
      </div>
      ${quiz.picked != null ? `<button class="btn primary" type="button" data-next>${quiz.index + 1 === quiz.round.length ? "See the score" : "Next"}</button>` : ""}
      <p class="note">${esc(state.speechNote)}</p>`;
  }
  const back = pack.scope === "room" ? `#/room/${pack.id}` : `#/sector/${pack.id}`;
  return shell(`
    ${crumbs([{ href: "#/", label: "Map" }, { href: back, label: pack.title }, { label: "Quiz" }])}
    <p class="kicker">Quiz</p>
    <h1>${esc(pack.title)}</h1>
    ${body}
  `, `/quiz/${pack.scope}/${pack.id}`);
}

function modeLabel(mode) {
  return { "fr-en": "French to English", "en-fr": "English to French", gender: "Gender", listen: "Listening" }[mode] || mode;
}

function shuffle(list) {
  const copy = list.slice();
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function startQuiz(pack, mode) {
  let pool = pack.items.slice();
  if (mode === "gender") {
    pool = pool.filter((item) => item.pos === "noun" && (item.gender === "m" || item.gender === "f"));
  }
  const round = shuffle(pool).slice(0, Math.min(10, pool.length));
  state.quiz = {
    packId: `${pack.scope}:${pack.id}`,
    mode,
    round,
    index: 0,
    correct: 0,
    picked: null,
    choices: makeChoices(pack, round[0], mode),
    done: false,
    reveal: false,
  };
  state.speechNote = "";
}

function makeChoices(pack, item, mode) {
  if (mode === "gender") {
    const answer = item.gender === "f" ? "feminine" : "masculine";
    return shuffle([
      { label: "feminine", ok: answer === "feminine" },
      { label: "masculine", ok: answer === "masculine" },
    ]);
  }
  const field = mode === "en-fr" ? "head" : "gloss";
  const answer = item[field];
  const distractors = shuffle(pack.items.filter((other) => other.id !== item.id && other[field] && other[field] !== answer)).slice(0, 3);
  while (distractors.length < 3) {
    distractors.push({ [field]: "—" });
  }
  return shuffle([
    { label: answer, ok: true },
    ...distractors.map((other) => ({ label: other[field], ok: false })),
  ]);
}

function prayersView(prayers) {
  return shell(`
    <p class="kicker">Parish prayers</p>
    <h1>Prayers</h1>
    <p class="lede">Traditional prayers in French, with an English reading beside them. They are texts to say, not pictures to invent. Listen, then read them in a quiet voice.</p>
    <div class="grid">
      ${prayers.prayers.map((prayer) => `<a class="card-link" href="#/prayer/${prayer.id}"><h2>${esc(prayer.title_fr)}</h2><p class="meta">${esc(prayer.title_en)}</p></a>`).join("")}
    </div>
  `, "/prayers");
}

function prayerView(prayer) {
  return shell(`
    ${crumbs([{ href: "#/prayers", label: "Prayers" }, { label: prayer.title_fr }])}
    <p class="kicker">${esc(prayer.title_en)}</p>
    <h1>${esc(prayer.title_fr)}</h1>
    <div class="row">
      <button class="btn primary" type="button" data-speak-prayer>Listen in French</button>
      <button class="btn" type="button" data-en>${state.showEn ? "Hide English" : "Show English"}</button>
    </div>
    <p class="note">${esc(speechHint("fr-FR"))}</p>
    <p class="prayer" id="prayer-fr">${esc(prayer.fr)}</p>
    ${state.showEn ? `<p class="prayer en">${esc(prayer.en)}</p>` : ""}
    <p class="source">${esc(prayer.source || "")}</p>
  `, `/prayer/${prayer.id}`);
}

function aboutView() {
  return shell(`
    <p class="kicker">How to walk</p>
    <h1>A village you can remember</h1>
    <div class="prose">
      <p class="lede">Memory Village is a French vocabulary palace for learners from the first hello (A1) to the upper floors (C2). You do not memorise a list. You walk through a place, and each word lives somewhere in it.</p>
      <h2>What a memory palace is</h2>
      <p>The method of loci is old and simple. You already remember rooms. If a word is tied to a spot in a room — a cup on the left of the terrace, a bottle in the cellar — coming back to that spot brings the word with it. A sound hook helps: an English word that resembles the French one, pictured in that same place. The explanation under every card tells you how that particular hook works, so you are never left with a joke you cannot unpack.</p>
      <h2>How this village is arranged</h2>
      <p>The map has sixteen quarters. Inside a quarter are buildings and, sometimes, a verb street. Inside a building are rooms. Rarer words live upstairs; the floor switcher moves you between them. Some rooms have a piece of furniture you can step up to — a bar counter, a table — and step back out of.</p>
      <p>Feminine nouns stand on the left. Masculine nouns stand on the right. The room itself is not tinted. If a colour marks gender, it is only on the word’s label: rose for feminine, blue for masculine.</p>
      <p>A few words are needed and still not drawn: they hang as text plaques, the way a museum labels something it will not illustrate. On a verb street, each verb is a little front. A mirror means the verb is reflexive. The preposition is written on the door.</p>
      <h2>How to use it</h2>
      <p>Open a room, tap a word, listen, and read the memory. Then hide the card and see whether the place gives the word back. The quiz can ask French to English, English to French, gender, or a listening question. Scores stay in this browser only.</p>
      <p>The prayers have their own quiet pages, with the French read aloud. Churches and other houses of worship, when their quarters open, are places of respect, not cartoons.</p>
      <p>${state.index?.featured?.kind === "sector"
        ? "Rue des Saveurs is a finished quarter: the square, both buildings, the rooms, and eleven short cooking alleys. Signs and labels are type, set into the picture, so they stay editable. A later street, with fewer two-sided alleys, can replace these eleven when its paintings arrive. The other quarters are coming soon."
        : state.index?.featured
        ? "The upstairs room of Café de la Place is a finished painting. Signs and labels are type, set into the picture, so they stay editable. The other rooms are coming soon."
        : "The pictures you see now are placeholders, except where a finished painting has already been hung. The words are already in their real places. When a finished painting arrives, it hangs in the same frame and the labels stay editable."}</p>
    </div>
  `, "/about");
}

function creditsView(markdown) {
  return shell(`
    <p class="kicker">Sources</p>
    <h1>Credits and licences</h1>
    <div class="credits">${renderMarkdown(markdown)}</div>
    <h2>Type</h2>
    <p>Signs use <strong>Cinzel</strong>. Labels, prayers and dialogue use <strong>IM Fell English</strong>. Both are released under the SIL Open Font License, the same texts shipped with these font files.</p>
    <p class="source">FLELex is CC BY-NC-SA. This site is a free learning project. If it were ever sold, the FLELex fields would have to be removed or relicensed.</p>
  `, "/credits");
}

function renderMarkdown(markdown) {
  const lines = markdown.replace(/\r/g, "").split("\n");
  const out = [];
  let i = 0;
  const inline = (text) => esc(text)
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+)`/g, "<code>$1</code>");
  while (i < lines.length) {
    const line = lines[i];
    if (line.startsWith("|")) {
      const rows = [];
      while (i < lines.length && lines[i].startsWith("|")) {
        const cells = lines[i].split("|").slice(1, -1).map((cell) => cell.trim());
        if (!cells.every((cell) => /^:?-{3,}:?$/.test(cell))) rows.push(cells);
        i += 1;
      }
      out.push(`<table>${rows.map((row, index) => `<tr>${row.map((cell) => `<${index === 0 ? "th" : "td"}>${inline(cell)}</${index === 0 ? "th" : "td"}>`).join("")}</tr>`).join("")}</table>`);
      continue;
    }
    if (line.startsWith("### ")) { out.push(`<h3>${inline(line.slice(4))}</h3>`); i += 1; continue; }
    if (line.startsWith("## ")) { out.push(`<h2>${inline(line.slice(3))}</h2>`); i += 1; continue; }
    if (line.startsWith("# ")) { out.push(`<h2>${inline(line.slice(2))}</h2>`); i += 1; continue; }
    if (line.startsWith("- ")) { out.push(`<p>• ${inline(line.slice(2))}</p>`); i += 1; continue; }
    if (!line.trim()) { i += 1; continue; }
    out.push(`<p>${inline(line)}</p>`);
    i += 1;
  }
  return out.join("");
}

function soonView(title) {
  const open = state.index?.open_sectors?.[0];
  return shell(`
    <h1>${esc(title || "Coming soon")}</h1>
    <p>This part of the village is still being painted.</p>
    ${open ? `<a class="btn primary" href="#/sector/${open}">Walk the open quarter</a>` : ""}
  `);
}

let playToken = 0;

async function playLines(lines) {
  const token = ++playToken;
  for (let index = 0; index < lines.length; index += 1) {
    if (token !== playToken) return;
    document.querySelectorAll(".line").forEach((node) => node.classList.toggle("on", Number(node.dataset.i) === index));
    const line = lines[index];
    const text = state.talkLang === "fr" ? line.fr : line.en;
    const result = await speak(text, state.talkLang === "fr" ? "fr-FR" : "en-GB");
    if (!result.ok) {
      state.speechNote = result.reason === "unsupported"
        ? "Speech playback is not available. Read the line aloud yourself."
        : "The voice stopped. You can keep reading, or press Play to try again.";
      const note = document.querySelector("[data-speech-note]");
      if (note) note.textContent = state.speechNote;
      return;
    }
    state.speechNote = result.voice ? "" : speechHint(state.talkLang === "fr" ? "fr-FR" : "en-GB");
    await new Promise((resolve) => window.setTimeout(resolve, 280));
  }
}

async function render() {
  const app = document.querySelector("#app");
  state.menu = false;
  playToken += 1;
  window.speechSynthesis?.cancel();
  const parts = parseRoute();
  if (parts[0] !== "sector") state.signpost = false;
  let html = "";
  try {
    if (!state.index) state.index = await getJSON("data/index.json");
    const [kind, a, b, c] = parts;
    if (!kind) html = mapView();
    else if (kind === "sector") html = sectorView(await getJSON(`data/sectors/${a}.json`));
    else if (kind === "building") {
      const buildingInfo = state.index.buildings.find((item) => item.id === a);
      if (!buildingInfo) html = soonView("Unknown place");
      else {
        const sector = await getJSON(`data/sectors/${buildingInfo.sector_id}.json`);
        const building = sector.buildings.find((item) => item.id === a);
        html = building ? buildingView(sector, building) : soonView(buildingInfo.name);
      }
    } else if (kind === "room") {
      try {
        const room = await getJSON(`data/rooms/${a}.json`);
        html = roomView(room, b === "word" ? c : null, b === "talk");
        state.currentRoom = room;
      } catch {
        html = soonView("This room is not open yet");
      }
    } else if (kind === "quiz") {
      const pack = await getJSON(`data/quiz/${a}/${b}.json`);
      state.quizPack = pack;
      html = quizView(pack);
    } else if (kind === "prayers") html = prayersView(await getJSON("data/prayers.json"));
    else if (kind === "prayer") {
      const prayers = await getJSON("data/prayers.json");
      const prayer = prayers.prayers.find((item) => item.id === a);
      html = prayer ? prayerView(prayer) : soonView("Prayer");
      state.currentPrayer = prayer;
    } else if (kind === "about") html = aboutView();
    else if (kind === "credits") html = creditsView(await (await fetch(url("data/credits.md"))).text());
    else html = soonView("Not on the map");
  } catch (error) {
    html = shell(`<h1>The path stopped</h1><p>${esc(error.message || "Could not load this part of the village.")}</p>`);
  }
  app.innerHTML = html;
  document.title = "Memory Village";
  fitHits();
  if (parts[1] === "talk" || parts[2] === "talk") {
    document.getElementById("talk")?.scrollIntoView({ block: "start" });
  }
  const quiz = state.quiz;
  if (parts[0] === "quiz" && quiz && quiz.mode === "listen" && quiz.picked == null && !quiz.done) {
    const item = quiz.round[quiz.index];
    speak(item.head, "fr-FR").then((result) => {
      if (!result.ok || !result.voice) {
        quiz.reveal = true;
        state.speechNote = speechHint("fr-FR") || "Playing the French word failed, so the spelling is shown.";
        const note = document.querySelector(".note");
        if (note) note.textContent = state.speechNote;
        const host = document.querySelector("[data-replay]")?.parentElement;
        if (host && !host.querySelector("span")) {
          const span = document.createElement("span");
          span.textContent = `${item.head} · ${item.respelling || ""}`;
          host.appendChild(span);
        }
      }
    });
  }
}

function onClick(event) {
  const menu = event.target.closest("[data-menu]");
  if (menu) {
    state.menu = !state.menu;
    document.querySelector(".top")?.classList.toggle("open", state.menu);
    menu.setAttribute("aria-expanded", state.menu ? "true" : "false");
    return;
  }
  if (event.target.closest("[data-fs]")) {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
    else document.exitFullscreen?.();
    return;
  }
  if (event.target.closest("[data-close-signpost]") || event.target.classList?.contains("signpost-layer")) {
    state.signpost = false;
    render();
    return;
  }
  if (event.target.closest("[data-signpost]")) {
    state.signpost = true;
    render();
    return;
  }
  const jump = event.target.closest("[data-target]");
  if (jump) {
    location.hash = hashFor(jump.dataset.target);
    return;
  }
  const route = event.target.closest("[data-route]");
  if (route) {
    state.routeId = route.dataset.route;
    render();
    return;
  }
  const word = event.target.closest("[data-word]");
  if (word) {
    const parts = parseRoute();
    const roomId = parts[0] === "room" ? parts[1] : null;
    if (roomId) location.hash = `#/room/${roomId}/word/${word.dataset.word}`;
    return;
  }
  const zoom = event.target.closest("[data-zoom]");
  if (zoom) {
    location.hash = `#/room/${zoom.dataset.zoom}`;
    return;
  }
  if (event.target.closest("[data-close-card]") || (event.target.dataset && event.target.dataset.close != null && event.target === event.currentTarget.closest?.(".card-layer"))) {
    // handled below
  }
  if (event.target.closest("[data-close-card]") || event.target.classList?.contains("card-layer")) {
    const parts = parseRoute();
    if (parts[0] === "room") location.hash = `#/room/${parts[1]}`;
    return;
  }
  const speakBtn = event.target.closest("[data-speak]");
  if (speakBtn) {
    speak(speakBtn.dataset.speak, speakBtn.dataset.lang || "fr-FR").then((result) => {
      if (!result.ok || !result.voice) state.speechNote = speechHint("fr-FR");
    });
    return;
  }
  if (event.target.closest("[data-play]") && state.currentRoom?.conversation) {
    playLines(state.currentRoom.conversation.lines);
    return;
  }
  if (event.target.closest("[data-stop]")) {
    playToken += 1;
    window.speechSynthesis?.cancel();
    return;
  }
  if (event.target.closest("[data-lang]")) {
    const keepTalk = Boolean(event.target.closest("#talk"));
    state.talkLang = state.talkLang === "fr" ? "en" : "fr";
    render().then(() => {
      if (keepTalk) document.getElementById("talk")?.scrollIntoView({ block: "start" });
    });
    return;
  }
  if (event.target.closest("[data-en]")) {
    const keepTalk = Boolean(event.target.closest("#talk"));
    const keepPrayer = Boolean(document.getElementById("prayer-fr"));
    state.showEn = !state.showEn;
    render().then(() => {
      if (keepTalk) document.getElementById("talk")?.scrollIntoView({ block: "start" });
      else if (keepPrayer) document.getElementById("prayer-fr")?.scrollIntoView({ block: "center" });
    });
    return;
  }
  if (event.target.closest("[data-speak-prayer]") && state.currentPrayer) {
    speak(state.currentPrayer.fr, "fr-FR");
    return;
  }
  const mode = event.target.closest("[data-mode]");
  if (mode && state.quizPack) {
    startQuiz(state.quizPack, mode.dataset.mode);
    render();
    return;
  }
  const choice = event.target.closest("[data-choice]");
  if (choice && state.quiz && state.quiz.picked == null) {
    const index = Number(choice.dataset.choice);
    state.quiz.picked = index;
    if (state.quiz.choices[index].ok) state.quiz.correct += 1;
    render();
    return;
  }
  if (event.target.closest("[data-next]") && state.quiz) {
    const quiz = state.quiz;
    if (quiz.index + 1 >= quiz.round.length) {
      quiz.done = true;
      recordQuiz(quiz.packId, quiz.correct, quiz.round.length);
    } else {
      quiz.index += 1;
      quiz.picked = null;
      quiz.reveal = false;
      quiz.choices = makeChoices(state.quizPack, quiz.round[quiz.index], quiz.mode);
    }
    render();
    return;
  }
  if (event.target.closest("[data-again]")) {
    state.quiz = null;
    render();
    return;
  }
  if (event.target.closest("[data-replay]") && state.quiz) {
    const item = state.quiz.round[state.quiz.index];
    speak(item.head, "fr-FR");
  }
}

function onKey(event) {
  if (event.key === "Escape") {
    if (state.signpost) {
      state.signpost = false;
      render();
      return;
    }
    const parts = parseRoute();
    if (parts[0] === "room" && parts[2] === "word") location.hash = `#/room/${parts[1]}`;
  }
  const hot = event.target.closest?.(".hot");
  if (hot && (event.key === "Enter" || event.key === " ")) {
    event.preventDefault();
    hot.click();
  }
}

document.querySelector("#app").addEventListener("click", onClick);
window.addEventListener("hashchange", render);
window.addEventListener("keydown", onKey);
window.addEventListener("resize", fitHits);
window.speechSynthesis?.addEventListener?.("voiceschanged", () => {
  if (state.speechNote) return;
  const hint = speechHint("fr-FR");
  document.querySelectorAll("[data-speech-note]").forEach((note) => {
    note.textContent = hint;
  });
});
render();
