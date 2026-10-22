const BASE = import.meta.env.BASE_URL;
const PROGRESS_KEY = "memory-village-v1";
const HITS_KEY = "memory-village-hits";
const LANG_KEY = "memory-village-lang";

const state = {
  index: null,
  i18n: null,
  guide: null,
  routeId: "suggested",
  menu: false,
  talkLang: "fr",
  showEn: true,
  quiz: null,
  speechNote: "",
  hits: localStorage.getItem(HITS_KEY) === "1",
  wordsOpen: false,
  guideOpen: false,
  tense: "present",
  lang: localStorage.getItem(LANG_KEY) === "fr" ? "fr" : "en",
  currentScene: null,
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

function lookup(pack, key) {
  return key.split(".").reduce((obj, part) => (obj == null ? obj : obj[part]), pack);
}

function t(key) {
  const value = lookup(state.i18n?.[state.lang], key);
  if (typeof value === "string") return value;
  const fallback = lookup(state.i18n?.en, key);
  return typeof fallback === "string" ? fallback : key;
}

function tf(key, vars) {
  return t(key).replace(/\{(\w+)\}/g, (_, name) => (vars[name] ?? ""));
}

function applyChrome() {
  document.documentElement.lang = state.lang === "fr" ? "fr" : "en";
  document.title = t("meta.title");
  const meta = document.querySelector('meta[name="description"]');
  if (meta) meta.setAttribute("content", t("meta.description"));
  const skip = document.querySelector(".skip");
  if (skip) skip.textContent = t("skip");
}

function setLang(lang) {
  state.lang = lang === "fr" ? "fr" : "en";
  localStorage.setItem(LANG_KEY, state.lang);
  applyChrome();
  render();
}

function localizedName(record) {
  if (!record) return "";
  if (state.lang === "fr") return record.name_fr || record.fr_name || record.name || record.en_name || "";
  return record.name_en || record.en_name || record.name || record.fr_name || "";
}

function localizedDescription(record) {
  if (!record) return "";
  if (state.lang === "fr") return record.description_fr || record.description || record.setting || "";
  return record.description || record.setting || record.description_fr || "";
}

function hoverLabel(item, fallbackKey) {
  if (!item) return t(fallbackKey);
  if (state.lang === "fr") return item.name_fr || item.label_fr || item.name || item.label || t(fallbackKey);
  return item.label_en || item.name_en || item.name || item.label || t(fallbackKey);
}

function doodle(name) {
  const paths = {
    book: '<path d="M5 4.5h7.2A2.2 2.2 0 0 1 14.4 6.7V20H7.2A2.2 2.2 0 0 0 5 22.2V4.5z"/><path d="M5 4.5H3.6A2.2 2.2 0 0 0 1.4 6.7V19a2.2 2.2 0 0 1 2.2-2.2H5"/>',
    compass: '<circle cx="12" cy="12" r="8"/><path d="M14.8 9.2 13 13l-3.8 1.8L11 11l3.8-1.8z"/>',
    house: '<path d="M4 11.5 12 5l8 6.5"/><path d="M6.5 10.5V19h11v-8.5"/>',
    halves: '<path d="M4 5h7v14H4z"/><path d="M13 5h7v14h-7z" opacity=".45"/>',
    street: '<path d="M4 18h16"/><path d="M7 18V8h3v10"/><path d="M14 18V6h3v12"/>',
    creature: '<circle cx="12" cy="13" r="4.2"/><path d="M9 9.2 8 6M12 8.6V5M15 9.2 16 6M8.2 16.2 6.5 19M15.8 16.2 17.5 19"/>',
    twins: '<circle cx="8" cy="12" r="3.2"/><circle cx="16" cy="12" r="3.2"/>',
    sign: '<path d="M5 6h12l2 3-2 3H5z"/><path d="M8 12v7"/>',
    frame: '<rect x="4" y="5" width="16" height="14" rx="1.5"/><path d="M8 16.5 11 12l2 2.2 1.4-1.4L16.5 16"/>',
    path: '<path d="M5 18c3-1 3.5-5 6.5-5S14 17 19 14"/><path d="M16.5 12.2 19 14l-1.2 2.8"/>',
    star: '<path d="M12 4.5 13.8 9l4.7.4-3.6 3.1 1.1 4.6L12 14.8 8 17.1l1.1-4.6L5.5 9.4 10.2 9z"/>',
    sprig: '<path d="M12 20V8"/><path d="M12 14c-3-1-5-3.5-5-3.5S10 10 12 12"/><path d="M12 11c3-1 5-3.2 5-3.2S14 8 12 10"/>',
    speaker: '<path d="M4 10h3l4-3v10l-4-3H4z"/><path d="M15 9.5a3.5 3.5 0 0 1 0 5"/><path d="M17 7.5a6 6 0 0 1 0 9"/>',
    spark: '<path d="M12 4v4M12 16v4M4 12h4M16 12h4M6.5 6.5l2.2 2.2M15.3 15.3l2.2 2.2M17.5 6.5l-2.2 2.2M8.7 15.3l-2.2 2.2"/>',
    expand: '<path d="M9 5H5v4M15 5h4v4M9 19H5v-4M15 19h4v-4"/>',
    collapse: '<path d="M9 5v4H5M15 5v4h4M9 19v-4H5M15 19v-4h4"/>',
  };
  return `<svg class="doodle" viewBox="0 0 24 24" aria-hidden="true">${paths[name] || paths.star}</svg>`;
}

function speechHint(lang) {
  const synth = window.speechSynthesis;
  if (!synth) return t("speech.unsupported");
  const wanted = lang.slice(0, 2).toLowerCase();
  const voice = synth.getVoices().find((item) => item.lang.toLowerCase().startsWith(wanted));
  if (!voice && wanted === "fr") return t("speech.noFrench");
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

function toolButton(attrs, icon, label, pressed) {
  const press = pressed == null ? "" : ` aria-pressed="${pressed ? "true" : "false"}"`;
  return `<button class="tool" type="button" ${attrs}${press}><span class="tool-icon">${icon}</span><span class="tool-label">${esc(label)}</span></button>`;
}

function shell(body, current, opts = {}) {
  const nav = [
    ["/", t("nav.map")],
    ["/about", t("nav.about")],
    ["/credits", t("nav.credits")],
  ];
  const fullscreen = Boolean(document.fullscreenElement);
  const fullLabel = fullscreen ? t("tools.leave") : t("tools.fullscreen");
  return `
    <div class="shell ${opts.scene ? "scene-mode" : ""}">
      <header class="top ${state.menu ? "open" : ""}">
        <a class="brand" href="#/">${doodle("compass")}<span><strong>${esc(t("brand"))}</strong><small>${esc(t("tagline"))}</small></span></a>
        <button class="menu-btn" type="button" data-menu aria-expanded="${state.menu ? "true" : "false"}">${esc(t("menu"))}</button>
        ${opts.backNav || ""}
        <nav class="nav">
          ${nav.map(([href, label]) => `<a href="#${href}" ${current === href ? 'aria-current="page"' : ""}>${esc(label)}</a>`).join("")}
          ${opts.extraNav || ""}
        </nav>
        <div class="tools">
          <div class="lang" role="group" aria-label="${esc(t("tools.lang"))}">
            <button type="button" data-lang-set="en" aria-pressed="${state.lang === "en" ? "true" : "false"}">EN</button>
            <button type="button" data-lang-set="fr" aria-pressed="${state.lang === "fr" ? "true" : "false"}">FR</button>
          </div>
          ${toolButton(`data-guide aria-label="${esc(t("tools.guideLabel"))}"`, doodle("book"), t("tools.guide"), state.guideOpen)}
          ${toolButton(`data-hits aria-label="${esc(t("tools.spotsLabel"))}"`, doodle("spark"), t("tools.spots"), state.hits)}
          ${toolButton(`data-fs aria-label="${esc(fullLabel)}"`, doodle(fullscreen ? "collapse" : "expand"), fullLabel)}
        </div>
      </header>
      <main id="main">${body}</main>
      ${opts.scene ? "" : `<footer class="site">${esc(t("footer"))}</footer>`}
    </div>`;
}

function backTarget(place) {
  if (!place) return null;
  if (place.kind === "sector") return { href: "#/", label: t("nav.backMap") };
  if (place.kind === "building") {
    const sector = place.sector;
    if (!sector?.id) return null;
    return { href: `#/sector/${sector.id}`, label: tf("nav.backTo", { place: localizedName(sector) || sector.id }) };
  }
  if (place.kind === "room") {
    const room = place.room;
    if (room?.kind === "zoom" && room.parent?.id) {
      const parent = room.parent;
      const name = state.lang === "fr"
        ? (parent.name_fr || parent.sign || parent.name || parent.id)
        : (parent.name || parent.name_en || parent.sign || parent.id);
      return { href: `#/room/${parent.id}`, label: tf("nav.backTo", { place: name }) };
    }
    if (room?.building_id) {
      const building = (state.index?.buildings || []).find((item) => item.id === room.building_id);
      if (building?.no_building_layer || room.no_building_layer) {
        const sector = (state.index?.sectors || []).find((item) => item.id === room.sector_id);
        const name = localizedName(sector) || room.sector_name || room.sector_id;
        return { href: `#/sector/${room.sector_id}`, label: tf("nav.backTo", { place: name }) };
      }
      const name = localizedName(building) || room.building_name || room.building_id;
      return { href: `#/building/${room.building_id}`, label: tf("nav.backTo", { place: name }) };
    }
  }
  return null;
}

function backNav(place) {
  const target = backTarget(place);
  if (!target) return "";
  return `<a class="back" data-back href="${esc(target.href)}">${esc(target.label)}</a>`;
}

function sceneNav(place) {
  if (!place) return "";
  const room = place.room;
  const quiz = place.kind === "room"
    ? `#/quiz/room/${room.id}`
    : place.kind === "sector"
      ? `#/quiz/sector/${place.sector.id}`
      : "";
  const talk = room?.conversation ? `#/room/${room.id}/talk` : "";
  return `
    ${room ? `<button type="button" data-words>${esc(t("tools.words"))}</button>` : ""}
    ${quiz ? `<a href="${quiz}">${esc(t("tools.quiz"))}</a>` : ""}
    ${talk ? `<a href="${talk}">${esc(t("tools.talk"))}</a>` : ""}
  `;
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
  return `<p class="meta">${esc(tf("quiz.soFar", { correct: record.last.correct, total: record.last.total, best: Math.round((record.best || 0) * 100) }))}</p>`;
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
    route += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#5d6b3c" stroke-width="5" stroke-linecap="round" />`;
  }
  const start = byId[index.start];
  const [sx, sy] = start ? point(start.id) : [0, 0];
  const pins = index.sectors.map((sector) => `
    <a class="pin ${sector.open ? "open" : "soon"}" style="left:${sector.x}%; top:${sector.y}%" href="#/sector/${sector.id}">
      <strong>${esc(localizedName(sector))}</strong>
      <em>${esc(sector.entry_level)} · ${sector.word_count}</em>
      <span class="seal">${sector.open ? esc(t("seal.open")) : esc(t("seal.soon"))}</span>
    </a>`).join("");
  const routes = [
    ["suggested", t("map.suggested")],
    ...index.alternatives.map((route) => [route.id, t(`routes.${route.id}`)]),
  ];
  const lede = index.featured?.kind === "sector"
    ? t("map.ledeOpen")
    : index.featured
      ? t("map.ledeRoom")
      : tf("map.ledeSoon", { tagline: t("tagline") });
  return shell(`
    <p class="kicker">${esc(t("map.kicker"))}</p>
    <h1>${esc(t("map.title"))}</h1>
    <p class="lede">${esc(lede)}</p>
    ${index.featured ? `<p><a class="btn primary" href="${index.featured.kind === "sector" ? `#/sector/${esc(index.featured.id)}` : `#/room/${esc(index.featured.id)}`}">${esc(tf("map.enter", { place: index.featured.sign }))}</a></p>` : ""}
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
    <p class="note">${esc(t("map.note"))}</p>
  `, "/");
}

function sectorView(sector, extraDialog = "") {
  if (!sector.open || !sector.scene?.image) {
    const open = state.index?.open_sectors?.[0];
    return pageShell(`
      <h1>${esc(localizedName(sector))}</h1>
      <p class="lede">${esc(localizedDescription(sector))}</p>
      <p>${esc(t("sector.closed"))}</p>
      ${open && open !== sector.id ? `<a class="btn primary" href="#/sector/${open}">${esc(t("sector.walkOpen"))}</a>` : ""}
    `, `/sector/${sector.id}`, backNav({ kind: "sector", id: sector.id, sector }));
  }
  state.place = { kind: "sector", id: sector.id, sector, extraDialog };
  return null;
}

function buildingView(sector, building, extraDialog = "") {
  if (!sector.open || !building.scene?.image) {
    const back = backTarget({ kind: "building", sector, building });
    return pageShell(`
      <h1>${esc(localizedName(building))}</h1>
      <p>${esc(localizedDescription(building) || t("building.unpainted"))}</p>
      ${back ? `<a class="btn primary" href="${esc(back.href)}">${esc(back.label)}</a>` : ""}
    `, `/building/${building.id}`, backNav({ kind: "building", sector, building }));
  }
  state.place = { kind: "building", id: building.id, sector, building };
  return null;
}

function roomView(room, wordId, talk, extraDialog = "") {
  state.currentRoom = room;
  state.place = { kind: "room", id: room.id, room, wordId, talk, extraDialog };
  return null;
}

function fitHits() {
  const svg = document.querySelector("#walk svg");
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
  placeWayBadges();
  placeSoonMarks();
  placeZoomBadges();
  bindSceneHover();
  toneSigns();
}

function isZoomTarget(target) {
  return /_z\d+$/i.test(String(target || ""));
}

function placeSoonMarks() {
  const frame = document.querySelector("#walk .frame");
  if (!frame) return;
  frame.querySelectorAll(":scope > .soon-pill").forEach((node) => node.remove());
  const svg = frame.querySelector("svg");
  const ctm = svg?.getScreenCTM();
  if (!svg || !ctm) return;
  const frameRect = frame.getBoundingClientRect();
  const toScreen = (x, y) => {
    const point = svg.createSVGPoint();
    point.x = x;
    point.y = y;
    const mapped = point.matrixTransform(ctm);
    return { x: mapped.x - frameRect.left, y: mapped.y - frameRect.top };
  };
  svg.querySelectorAll("[data-soon-box]").forEach((el) => {
    const [x0, y0, x1, y1] = el.dataset.soonBox.split(",").map(Number);
    const screen = toScreen((x0 + x1) / 2, (y0 + y1) / 2);
    const pill = document.createElement("span");
    pill.className = "soon-pill";
    pill.textContent = t("seal.soon");
    pill.style.left = `${screen.x}px`;
    pill.style.top = `${screen.y}px`;
    frame.appendChild(pill);
  });
}

function placeWayBadges() {
  const frame = document.querySelector("#walk .frame");
  if (!frame) return;
  frame.querySelectorAll(":scope > .way-badge, :scope > .way-pill").forEach((node) => node.remove());
  const svg = frame.querySelector("svg");
  const ctm = svg?.getScreenCTM();
  const inverse = ctm?.inverse();
  if (!svg || !ctm || !inverse) return;
  const frameRect = frame.getBoundingClientRect();
  const badgePx = window.matchMedia("(max-width: 700px)").matches ? 20 : 26;
  const toScreen = (x, y) => {
    const point = svg.createSVGPoint();
    point.x = x;
    point.y = y;
    const mapped = point.matrixTransform(ctm);
    return { x: mapped.x - frameRect.left, y: mapped.y - frameRect.top };
  };
  const toSvg = (px) => {
    const origin = svg.createSVGPoint();
    const shifted = svg.createSVGPoint();
    origin.x = frameRect.left;
    origin.y = frameRect.top;
    shifted.x = frameRect.left + px;
    shifted.y = frameRect.top;
    return Math.abs(shifted.matrixTransform(inverse).x - origin.matrixTransform(inverse).x) || badgePx;
  };
  const size = toSvg(badgePx);
  const boxesOf = (selector, attr) => [...svg.querySelectorAll(selector)].map((el) => {
    const [x0, y0, x1, y1] = (el.dataset[attr] || "").split(",").map(Number);
    return { x0, y0, x1, y1 };
  }).filter((box) => Number.isFinite(box.x0));
  const obstacles = [
    ...boxesOf("[data-item-box]", "itemBox"),
    ...boxesOf("[data-sign-box]", "signBox"),
    ...boxesOf("[data-zoom-box]", "zoomBox"),
  ];
  const placed = [];
  const view = svg.viewBox.baseVal;
  const hits = (x, y, rects) => rects.some((rect) => x < rect.x1 && x + size > rect.x0 && y < rect.y1 && y + size > rect.y0);
  svg.querySelectorAll("[data-way-box]").forEach((el) => {
    const [x0, y0, x1, y1] = el.dataset.wayBox.split(",").map(Number);
    const dir = el.dataset.wayDir || "through";
    const midX = (x0 + x1) / 2 - size / 2;
    const midY = (y0 + y1) / 2 - size / 2;
    const inset = Math.max(size * 0.2, 6);
    const spots = {
      through: [[midX, midY], [midX, y1 - size - inset], [midX, y0 + inset], [x0 + inset, midY], [x1 - size - inset, midY]],
      up: [[midX, y0 + inset], [midX, midY], [x0 + inset, y0 + inset], [x1 - size - inset, y0 + inset]],
      down: [[midX, y1 - size - inset], [midX, midY], [x0 + inset, y1 - size - inset], [x1 - size - inset, y1 - size - inset]],
      left: [[x0 + inset, midY], [midX, midY], [x0 + inset, y0 + inset], [x0 + inset, y1 - size - inset]],
      right: [[x1 - size - inset, midY], [midX, midY], [x1 - size - inset, y0 + inset], [x1 - size - inset, y1 - size - inset]],
    }[dir] || [[midX, midY]];
    let x = midX;
    let y = midY;
    const found = spots.some(([sx, sy]) => {
      const cx = Math.max(4, Math.min(sx, (view.width || 1280) - size - 4));
      const cy = Math.max(4, Math.min(sy, (view.height || 720) - size - 4));
      if (hits(cx, cy, obstacles) || hits(cx, cy, placed)) return false;
      x = cx;
      y = cy;
      return true;
    });
    if (!found) {
      x = Math.max(4, Math.min(midX, (view.width || 1280) - size - 4));
      y = Math.max(4, Math.min(midY, (view.height || 720) - size - 4));
    }
    placed.push({ x0: x, y0: y, x1: x + size, y1: y + size });
    const screen = toScreen(x, y);
    const node = document.createElement("button");
    node.type = "button";
    node.className = `way-badge ${el.dataset.wayIcon || "door"} ${dir}`;
    node.dataset.target = el.dataset.target || "";
    const wayName = el.dataset.wayName || "";
    node.setAttribute("aria-label", wayName);
    node.innerHTML = wayIconSvg(el.dataset.wayIcon || "door");
    const origin = toScreen(0, 0);
    const end = toScreen(view.width || 1280, view.height || 720);
    const minX = Math.max(4, Math.min(origin.x, end.x));
    const minY = Math.max(4, Math.min(origin.y, end.y));
    const maxX = Math.max(minX, Math.max(origin.x, end.x) - badgePx - 4);
    const maxY = Math.max(minY, Math.max(origin.y, end.y) - badgePx - 4);
    node.style.left = `${Math.max(minX, Math.min(screen.x, maxX))}px`;
    node.style.top = `${Math.max(minY, Math.min(screen.y, maxY))}px`;
    const light = (on) => {
      el.classList.toggle("glow", on);
      const signId = el.dataset.lightsSign;
      if (!signId || !window.CSS?.escape) return;
      svg.querySelector(`[data-sign-id="${CSS.escape(signId)}"]`)?.classList.toggle("lit", on);
    };
    node.addEventListener("pointerenter", () => light(true));
    node.addEventListener("pointerleave", () => light(false));
    frame.appendChild(node);
    if (!el.dataset.lightsSign && wayName) {
      const pill = document.createElement("span");
      const pillIcon = el.dataset.wayIcon === "stairs" ? "stairs" : "arrow";
      pill.className = `way-pill ${pillIcon} ${dir}`;
      pill.innerHTML = wayIconSvg(pillIcon);
      const caption = document.createElement("span");
      caption.textContent = wayName;
      pill.appendChild(caption);
      const left = Number.parseFloat(node.style.left) || 0;
      const top = Number.parseFloat(node.style.top) || 0;
      const frameW = frame.clientWidth || 320;
      const placeLeft = left > frameW * 0.58;
      pill.style.top = `${top + badgePx / 2}px`;
      if (placeLeft) {
        pill.classList.add("pill-left");
        pill.style.left = `${Math.max(8, left - 6)}px`;
        pill.style.maxWidth = `${Math.max(72, left - 12)}px`;
      } else {
        pill.style.left = `${left + badgePx + 6}px`;
        pill.style.maxWidth = `${Math.max(72, frameW - left - badgePx - 16)}px`;
      }
      const show = (on) => pill.classList.toggle("show-label", on);
      pill.dataset.for = el.dataset.wayBox || "";
      node.addEventListener("pointerenter", () => show(true));
      node.addEventListener("pointerleave", () => show(false));
      frame.appendChild(pill);
    }
  });
}

function wayIconSvg(icon) {
  if (icon === "stairs") {
    return `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 17.5h4.5v-4h4.5v-4H18V5.5"/></svg>`;
  }
  if (icon === "arrow") {
    return `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h12M13 6.5 18.5 12 13 17.5"/></svg>`;
  }
  return `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.2 5.2h8.4v13.6H6.2z"/><path d="M15.8 12h3.4M17.8 10.2 20.2 12l-2.4 1.8"/><circle cx="12.2" cy="12" r="0.85" fill="currentColor" stroke="none"/></svg>`;
}

function bindSceneHover() {
  const svg = document.querySelector("#walk svg");
  if (!svg || svg.dataset.hoverBound || !window.CSS?.escape) return;
  svg.dataset.hoverBound = "1";
  svg.querySelectorAll("[data-lights-sign]").forEach((hot) => {
    const sign = svg.querySelector(`[data-sign-id="${CSS.escape(hot.dataset.lightsSign)}"]`);
    hot.addEventListener("pointerenter", () => {
      hot.classList.add("glow");
      sign?.classList.add("lit");
    });
    hot.addEventListener("pointerleave", () => {
      hot.classList.remove("glow");
      sign?.classList.remove("lit");
    });
  });
  svg.querySelectorAll(".hot.word").forEach((hot) => {
    const sign = svg.querySelector(`.verb-sign[data-word="${CSS.escape(hot.dataset.word || "")}"]`);
    if (!sign) return;
    hot.addEventListener("pointerenter", () => sign.classList.add("lit"));
    hot.addEventListener("pointerleave", () => sign.classList.remove("lit"));
  });
  svg.querySelectorAll("[data-way-box]").forEach((hot) => {
    if (hot.dataset.lightsSign) return;
    const show = (on) => {
      svg.closest(".frame")?.querySelectorAll(".way-pill").forEach((pill) => {
        if (pill.dataset.for === hot.dataset.wayBox) pill.classList.toggle("show-label", on);
      });
    };
    hot.addEventListener("pointerenter", () => show(true));
    hot.addEventListener("pointerleave", () => show(false));
  });
}

function toneSigns() {
  const frame = document.querySelector("#walk .frame");
  const img = frame?.querySelector("img.painting");
  const svg = frame?.querySelector("svg");
  if (!img || !svg) return;
  if (!img.complete || !img.naturalWidth) {
    img.addEventListener("load", toneSigns, { once: true });
    return;
  }
  const scale = Math.min(1, 360 / img.naturalWidth);
  const canvas = document.createElement("canvas");
  canvas.width = Math.max(1, Math.round(img.naturalWidth * scale));
  canvas.height = Math.max(1, Math.round(img.naturalHeight * scale));
  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  if (!ctx) return;
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  svg.querySelectorAll(".painted-sign").forEach((sign) => {
    const parts = (sign.dataset.signBox || "").split(",").map(Number);
    if (parts.length < 4 || parts.some((n) => !Number.isFinite(n))) return;
    const [x0, y0, x1, y1] = parts;
    const sx = Math.max(0, Math.floor(x0 * scale));
    const sy = Math.max(0, Math.floor(y0 * scale));
    const sw = Math.max(1, Math.min(canvas.width - sx, Math.ceil((x1 - x0) * scale)));
    const sh = Math.max(1, Math.min(canvas.height - sy, Math.ceil((y1 - y0) * scale)));
    let pixels;
    try {
      pixels = ctx.getImageData(sx, sy, sw, sh).data;
    } catch {
      return;
    }
    let sum = 0;
    let count = 0;
    for (let i = 0; i < pixels.length; i += 16) {
      sum += 0.2126 * pixels[i] + 0.7152 * pixels[i + 1] + 0.0722 * pixels[i + 2];
      count += 1;
    }
    sign.classList.toggle("ink-gold", sum / Math.max(1, count) < 105);
  });
}

function placeZoomBadges() {
  const frame = document.querySelector("#walk .frame");
  if (!frame) return;
  frame.querySelectorAll(":scope > .zoom-badge").forEach((node) => node.remove());
  const svg = frame.querySelector("svg");
  const ctm = svg?.getScreenCTM();
  const inverse = ctm?.inverse();
  if (!svg || !ctm || !inverse) return;
  const frameRect = frame.getBoundingClientRect();
  const badgePx = window.matchMedia("(max-width: 700px)").matches ? 22 : 30;
  const toScreen = (x, y) => {
    const point = svg.createSVGPoint();
    point.x = x;
    point.y = y;
    const mapped = point.matrixTransform(ctm);
    return { x: mapped.x - frameRect.left, y: mapped.y - frameRect.top };
  };
  const toSvgX = (px) => {
    const origin = svg.createSVGPoint();
    const shifted = svg.createSVGPoint();
    origin.x = frameRect.left;
    origin.y = frameRect.top;
    shifted.x = frameRect.left + px;
    shifted.y = frameRect.top;
    return Math.abs(shifted.matrixTransform(inverse).x - origin.matrixTransform(inverse).x) || badgePx;
  };
  const size = toSvgX(badgePx);
  const items = [...svg.querySelectorAll("[data-item-box]")].map((el) => {
    const [x0, y0, x1, y1] = el.dataset.itemBox.split(",").map(Number);
    return { x0, y0, x1, y1 };
  });
  const hitsItem = (x, y) => items.some((item) => x < item.x1 && x + size > item.x0 && y < item.y1 && y + size > item.y0);
  const view = svg.viewBox.baseVal;
  svg.querySelectorAll("[data-zoom-box]").forEach((el) => {
    const target = el.dataset.zoom || el.dataset.target || "";
    if (!el.dataset.zoom && !isZoomTarget(target)) return;
    const [x0, y0, x1] = el.dataset.zoomBox.split(",").map(Number);
    let x = x1 - size;
    let y = y0;
    for (let step = 0; step < 8 && hitsItem(x, y); step += 1) {
      x -= size * 0.65;
      if (x < x0 - size) {
        x = x1 - size;
        y += size * 0.65;
      }
    }
    const limit = 6;
    x = Math.max(limit, Math.min(x, (view.width || 1280) - size - limit));
    y = Math.max(limit, Math.min(y, (view.height || 720) - size - limit));
    const screen = toScreen(x, y);
    const node = document.createElement("button");
    node.type = "button";
    node.className = "zoom-badge";
    node.title = t("lookCloser");
    node.setAttribute("aria-label", t("lookCloser"));
    if (el.dataset.zoom) node.dataset.zoom = el.dataset.zoom;
    else node.dataset.target = target;
    node.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="5.25"/><path d="M14.4 14.4 19.2 19.2"/></svg>`;
    node.style.left = `${Math.max(4, Math.min(screen.x, frame.clientWidth - badgePx - 4))}px`;
    node.style.top = `${Math.max(4, Math.min(screen.y, frame.clientHeight - badgePx - 4))}px`;
    frame.appendChild(node);
  });
}

function hashFor(target) {
  const value = String(target || "");
  if (value.endsWith("_sector")) {
    const prefix = value.slice(0, -"_sector".length);
    const sector = (state.index?.sectors || []).find((item) => item.id.startsWith(`${prefix}_`));
    return `#/sector/${sector ? sector.id : value}`;
  }
  if (value.startsWith("B")) {
    const building = (state.index?.buildings || []).find((item) => item.id === value);
    if (building?.no_building_layer && building.sector_id) return `#/sector/${building.sector_id}`;
    return `#/building/${value}`;
  }
  return `#/room/${value}`;
}

function moodFor(place) {
  const id = place?.room?.building_id || place?.building?.id || place?.id || "";
  if (String(id).includes("cafe")) return "blossom";
  if (String(id).includes("wine")) return "herb";
  if (String(id).includes("kitchen")) return "sky";
  if (String(id).includes("resto")) return "leaf";
  if (String(id).includes("cooking") || place?.room?.kind === "street_segment") return "mist";
  if (place?.kind === "sector") return "square";
  return "leaf";
}

function exitKind(key) {
  return { prev: "back", back: "back", next: "forward", forward: "forward", left: "left", right: "right" }[key] || "";
}

function endingMarker(text) {
  const parts = String(text || "").trim().split(/\s*\/\s*/).map((part) => part.trim()).filter(Boolean);
  return parts.length > 0 && parts.every((part) => /^-(?:er|ir|re)$/i.test(part));
}

function verbSide(word, scene) {
  const hot = (scene.hotspots || []).find((item) => item.word_id === word?.id && !item.helper && item.side);
  const raw = String(hot?.side || word?.side || "").toLowerCase();
  if (raw === "left" || raw === "right") return raw;
  const lemma = word?.lemma || "";
  if (/(?:ir|re)$/i.test(lemma)) return "right";
  if (/er$/i.test(lemma)) return "left";
  return "";
}

function wrapLines(text, boxWidth, boxHeight, maxSize = 36, widthFactor = 0.56) {
  const words = String(text).split(/\s+/).filter(Boolean);
  const widthOf = (value, size) => Array.from(value).length * size * widthFactor;
  const layout = (size) => {
    if (!words.length) return [];
    if (words.some((word) => widthOf(word, size) > boxWidth + 0.5)) return null;
    const space = widthOf(" ", size);
    const widths = words.map((word) => widthOf(word, size));
    const n = words.length;
    const best = Array(n + 1).fill(Infinity);
    const next = Array(n).fill(n);
    best[n] = 0;
    for (let start = n - 1; start >= 0; start -= 1) {
      let width = 0;
      for (let end = start + 1; end <= n; end += 1) {
        width += widths[end - 1] + (end > start + 1 ? space : 0);
        if (width > boxWidth + 0.5) break;
        const score = (boxWidth - width) ** 2 + best[end];
        if (score < best[start]) {
          best[start] = score;
          next[start] = end;
        }
      }
    }
    if (!Number.isFinite(best[0])) return null;
    const lines = [];
    for (let index = 0; index < n;) {
      const end = next[index];
      lines.push(words.slice(index, end).join(" "));
      index = end;
    }
    if (lines.length * size * 1.15 > boxHeight + 1) return null;
    return lines;
  };
  let size = Math.min(maxSize, Math.max(8, Math.floor(boxHeight * 0.72)));
  while (size >= 8) {
    const lines = layout(size);
    if (lines) return { size, lines };
    size -= 1;
  }
  return { size: 8, lines: [String(text)] };
}

function textBlock(className, text, box, opts = {}) {
  const wrapped = wrapLines(text, box[2] - box[0], box[3] - box[1], opts.maxSize || 36);
  const cx = (box[0] + box[2]) / 2;
  const lineHeight = wrapped.size * 1.15;
  const top = (box[1] + box[3]) / 2 - (wrapped.lines.length * lineHeight) / 2 + wrapped.size * 0.72;
  return wrapped.lines.map((line, index) =>
    `<text class="${className}" x="${cx.toFixed(1)}" y="${(top + index * lineHeight).toFixed(1)}" text-anchor="middle" font-size="${wrapped.size.toFixed(1)}">${esc(line)}</text>`
  ).join("");
}

function fittedPlate(className, text, box, opts = {}) {
  const [x0, y0, x1, y1] = box;
  const width = Math.max(12, x1 - x0);
  const height = Math.max(12, y1 - y0);
  const inset = Math.min(2, width * 0.04, height * 0.08);
  const wrapped = wrapLines(
    text,
    Math.max(8, width - inset * 2),
    Math.max(8, height - inset * 2),
    opts.maxSize || Math.max(11, (height - inset * 2) * 0.82),
    opts.widthFactor || 0.62,
  );
  const cx = (x0 + x1) / 2;
  const lineHeight = wrapped.size * 1.05;
  const top = (y0 + y1) / 2 - (wrapped.lines.length * lineHeight) / 2 + wrapped.size * 0.78;
  const lines = wrapped.lines.map((line, index) =>
    `<text x="${cx.toFixed(1)}" y="${(top + index * lineHeight).toFixed(1)}" text-anchor="middle" font-size="${wrapped.size.toFixed(1)}">${esc(line)}</text>`
  ).join("");
  const rx = Math.min(5, height / 4);
  const word = opts.wordId ? ` data-word="${esc(opts.wordId)}"` : "";
  return `<g class="${className}" data-sign-box="${box.join(",")}"${word}>
    <rect class="plate" x="${(x0 + 0.5).toFixed(1)}" y="${(y0 + 0.5).toFixed(1)}" width="${(width - 1).toFixed(1)}" height="${(height - 1).toFixed(1)}" rx="${rx.toFixed(1)}"></rect>
    ${lines}
  </g>`;
}

function paintedSign(className, text, box, opts = {}) {
  const [x0, y0, x1, y1] = box;
  const width = Math.max(12, x1 - x0);
  const height = Math.max(12, y1 - y0);
  const inset = Math.min(3, width * 0.08, height * 0.14);
  const wrapped = wrapLines(
    text,
    Math.max(8, width - inset * 2),
    Math.max(8, height - inset * 2),
    opts.maxSize || Math.max(11, (height - inset * 2) * 0.72),
    opts.widthFactor || 0.56,
  );
  const cx = (x0 + x1) / 2;
  const lineHeight = wrapped.size * 1.08;
  const top = (y0 + y1) / 2 - (wrapped.lines.length * lineHeight) / 2 + wrapped.size * 0.78;
  const lines = wrapped.lines.map((line, index) =>
    `<text x="${cx.toFixed(1)}" y="${(top + index * lineHeight).toFixed(1)}" text-anchor="middle" font-size="${wrapped.size.toFixed(1)}">${esc(line)}</text>`
  ).join("");
  const id = opts.signId ? ` data-sign-id="${esc(opts.signId)}"` : "";
  return `<g class="painted-sign ${className}" data-sign-box="${box.join(",")}"${id}>${lines}</g>`;
}

function wordLabel(word, box, labelXy) {
  const [x0, y0, x1, y1] = box;
  let x;
  let y;
  if (labelXy && labelXy.length >= 2) {
    x = Number(labelXy[0]);
    y = Number(labelXy[1]);
  } else {
    x = (x0 + x1) / 2;
    y = Math.min(Math.max(y1 - 8, y0 + 14), y1 - 4);
  }
  return `<text class="lbl ${genderClass(word)}" x="${x}" y="${y}" text-anchor="middle" font-size="18">${esc(word.head)}</text>`;
}

function nameTag(text, box) {
  if (!text) return "";
  const size = 22;
  const width = Array.from(text).length * size * 0.58 + 28;
  const [x0, y0, x1, y1] = box;
  const cx = (x0 + x1) / 2;
  const y = y0 + Math.min(48, (y1 - y0) * 0.35);
  return `<g class="name-tag">
    <rect class="plate" x="${(cx - width / 2).toFixed(1)}" y="${(y - size).toFixed(1)}" width="${width.toFixed(1)}" height="${(size * 1.7).toFixed(1)}" rx="12"></rect>
    <text x="${cx.toFixed(1)}" y="${(y + 4).toFixed(1)}" text-anchor="middle" font-size="${size}">${esc(text)}</text>
  </g>`;
}

function wayCue(item, exitKey) {
  const kind = String(item?.kind || "");
  const key = exitKind(exitKey) || "";
  if (kind === "stairs_up" || kind === "stairs") return { icon: "stairs", dir: "up" };
  if (kind === "stairs_down") return { icon: "stairs", dir: "down" };
  if (key === "left" || key === "right" || key === "forward" || key === "back") {
    return { icon: "arrow", dir: { left: "left", right: "right", forward: "up", back: "down" }[key] };
  }
  if (kind === "street" || kind === "path") return { icon: "arrow", dir: "up" };
  if (kind === "zoom_back") return { icon: "arrow", dir: "down" };
  return { icon: "door", dir: "through" };
}

function foldName(value) {
  return String(value || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

function boxGap(signBox, linkBox) {
  if (!signBox || !linkBox) return Infinity;
  const cx = (Number(signBox[0]) + Number(signBox[2])) / 2;
  const cy = (Number(signBox[1]) + Number(signBox[3])) / 2;
  const dx = cx < linkBox[0] ? linkBox[0] - cx : cx > linkBox[2] ? cx - linkBox[2] : 0;
  const dy = cy < linkBox[1] ? linkBox[1] - cy : cy > linkBox[3] ? cy - linkBox[3] : 0;
  return Math.hypot(dx, dy);
}

function signAssignments(scene) {
  const areas = scene.text_areas || {};
  const portals = [];
  (scene.links || []).forEach((link, index) => {
    if (!link?.box || !link.target || isZoomTarget(link.target)) return;
    portals.push({ id: `link:${index}`, item: link, exitKey: "" });
  });
  Object.entries(scene.exits || {}).forEach(([key, exit]) => {
    const kind = exitKind(key);
    if (!kind || !exit?.box || !exit.target || isZoomTarget(exit.target)) return;
    portals.push({ id: `exit:${key}`, item: exit, exitKey: key });
  });
  const assigned = new Map();
  const usedSigns = new Set();
  const usedPortals = new Set();
  const claim = (portal, signId) => {
    if (!portal || usedSigns.has(signId) || usedPortals.has(portal.id)) return;
    usedSigns.add(signId);
    usedPortals.add(portal.id);
    assigned.set(portal.id, signId);
  };
  portals.forEach((portal) => {
    const signId = portal.item.signed_by;
    if (signId && areas[signId]) claim(portal, signId);
  });
  Object.entries(areas).forEach(([id, area]) => {
    if (area.role !== "direction" || !area.for_exit) return;
    const kind = exitKind(area.for_exit) || area.for_exit;
    claim(portals.find((item) => item.exitKey === area.for_exit || item.exitKey === kind), id);
  });
  Object.entries(areas).forEach(([id, area]) => {
    if (usedSigns.has(id)) return;
    if (area.role !== "direction" || area.for_exit) return;
    const trimmed = String(area.text || "").trim();
    if (trimmed.startsWith("-")) return;
    const text = foldName(trimmed);
    if (text.length < 3) return;
    const box = area.box || area.text_box;
    let best = null;
    let bestDist = 180;
    portals.forEach((portal) => {
      if (usedPortals.has(portal.id) || portal.item.soon) return;
      const name = foldName(`${portal.item.name || ""} ${portal.item.label || ""}`);
      if (!name.includes(text)) return;
      const dist = boxGap(box, portal.item.box);
      if (dist <= bestDist) {
        bestDist = dist;
        best = portal;
      }
    });
    claim(best, id);
  });
  Object.entries(areas).forEach(([id, area]) => {
    if (usedSigns.has(id)) return;
    if (area.role !== "building_name" && area.role !== "street_name" && id !== "building_name") return;
    const text = foldName(area.text || "");
    if (text.length < 3) return;
    const box = area.box || area.text_box;
    let best = null;
    let bestDist = 180;
    portals.forEach((portal) => {
      if (usedPortals.has(portal.id)) return;
      const name = foldName(portal.item.name || portal.item.label || "");
      if (!name.includes(text)) return;
      const dist = boxGap(box, portal.item.box);
      if (dist <= bestDist) {
        bestDist = dist;
        best = portal;
      }
    });
    claim(best, id);
  });
  return assigned;
}

function wayMarkup(item, exitKey, signId) {
  if (!item?.box || !item.target || isZoomTarget(item.target)) return "";
  const cue = wayCue(item, exitKey);
  const name = hoverLabel(item, exitKey ? `nav.${exitKind(exitKey) || "forward"}` : "open");
  const lights = signId ? ` data-lights-sign="${esc(signId)}"` : "";
  return ` data-way-box="${item.box.join(",")}" data-way-dir="${cue.dir}" data-way-icon="${cue.icon}" data-way-name="${esc(name)}"${lights}`;
}

function hitShape(item) {
  if (item.polygon && item.polygon.length >= 3) {
    const points = item.polygon.map((point) => point.join(",")).join(" ");
    return `<polygon class="hit" points="${points}"></polygon>`;
  }
  const [x0, y0, x1, y1] = item.box;
  return `<rect class="hit" x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}"></rect>`;
}

function sceneMarkup(scene, words, zooms) {
  const byId = Object.fromEntries((words || []).map((word) => [word.id, word]));
  const areas = scene.text_areas || {};
  const signs = signAssignments(scene);
  const signed = new Set(Object.keys(areas).filter((key) => key.endsWith("_sign")).map((key) => key.slice(0, -5)));
  state.nav = { forward: null, back: null, left: null, right: null };
  const parts = [];
  (scene.links || []).forEach((link, index) => {
    if (!link?.box || !link.target) return;
    if (link.soon) {
      const name = hoverLabel(link, "open");
      parts.push(`<g class="hot soon" data-soon-box="${link.box.join(",")}" role="img" aria-label="${esc(`${name}. ${t("seal.soon")}`)}">${hitShape(link)}</g>`);
      return;
    }
    const zoomBox = isZoomTarget(link.target) ? ` data-zoom-box="${link.box.join(",")}"` : "";
    const way = wayMarkup(link, "", signs.get(`link:${index}`) || "");
    const label = hoverLabel(link, "open");
    const tag = way ? "" : nameTag(label, link.box);
    parts.push(`<g class="hot link${way ? " way" : ""}${zoomBox ? " zoom" : ""}" data-target="${esc(link.target)}"${zoomBox}${way} tabindex="0" role="button" aria-label="${esc(label)}">${hitShape(link)}${tag}</g>`);
  });
  Object.entries(scene.exits || {}).forEach(([key, exit]) => {
    const kind = exitKind(key);
    if (!kind || !exit?.box || !exit.target) return;
    state.nav[kind] = hashFor(exit.target);
    const zoomBox = isZoomTarget(exit.target) ? ` data-zoom-box="${exit.box.join(",")}"` : "";
    const way = wayMarkup(exit, key, signs.get(`exit:${key}`) || "");
    const label = hoverLabel(exit, `nav.${kind}`);
    parts.push(`<g class="hot exit ${kind}${way ? " way" : ""}${zoomBox ? " zoom" : ""}" data-target="${esc(exit.target)}"${zoomBox}${way} tabindex="0" role="button" aria-label="${esc(label)}">${hitShape(exit)}</g>`);
  });
  (scene.hotspots || []).forEach((hot) => {
    if (hot.helper) return;
    const word = byId[hot.word_id];
    const box = hot.mnemonic_box ? [
      Math.min(hot.box[0], hot.mnemonic_box[0]),
      Math.min(hot.box[1], hot.mnemonic_box[1]),
      Math.max(hot.box[2], hot.mnemonic_box[2]),
      Math.max(hot.box[3], hot.mnemonic_box[3]),
    ] : hot.box;
    const [x0, y0, x1, y1] = box;
    const cx = (x0 + x1) / 2;
    const pad = `<rect class="hit pad" data-pad data-cx="${cx}" data-cy="${(y0 + y1) / 2}" data-w="${x1 - x0}" data-h="${y1 - y0}" x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}"></rect>`;
    let shape = pad;
    if (hot.polygon) shape += `<polygon class="hit" points="${hot.polygon.map((point) => point.join(",")).join(" ")}"></polygon>`;
    if (hot.zoom_id) {
      const named = (zooms || []).find((zoom) => zoom.id === hot.zoom_id);
      const label = state.lang === "fr"
        ? (hot.label_fr || named?.sign_fr || named?.sign || hot.label || t("lookCloser"))
        : (hot.label_en || hot.label || named?.sign || t("lookCloser"));
      const zoomBox = hot.box ? ` data-zoom-box="${hot.box.join(",")}"` : "";
      parts.push(`<g class="hot zoom" data-zoom="${esc(hot.zoom_id)}"${zoomBox} tabindex="0" role="button" aria-label="${esc(label)}">${shape}${nameTag(label, hot.box)}</g>`);
      return;
    }
    if (!word) return;
    const hasPlaque = Boolean(areas[`${word.id}_plaque`]);
    let extra = "";
    if (hot.door_plaque && word.prepositions?.length && !hasPlaque) {
      const [a, b, c, d] = hot.door_plaque;
      extra += textBlock("plaque", word.prepositions.join(" · "), [a, b, c, d]);
    }
    const label = signed.has(word.id) ? "" : wordLabel(word, box, hot.label_xy);
    parts.push(`<g class="hot word" data-word="${esc(word.id)}" data-item-box="${box.join(",")}" tabindex="0" role="button" aria-label="${esc(`${word.head}, ${word.gloss}`)}">${shape}${label}${extra}</g>`);
  });
  Object.entries(areas).forEach(([key, area]) => {
    const text = area.text || (key === "sign" ? scene.sign_text : "") || (key === "plaque" ? scene.plaque_text : "");
    if (!text) return;
    const box = area.text_box || area.box;
    const wordId = key.endsWith("_sign") ? key.slice(0, -5) : "";
    const word = byId[wordId];
    if (area.role === "direction") {
      if (endingMarker(text)) return;
      parts.push(paintedSign("direction-sign", text, box, { maxSize: 18, signId: key }));
      return;
    }
    if (area.role === "sector_name") {
      parts.push(paintedSign("sector-name", text, box, { maxSize: 28, signId: key }));
      return;
    }
    if (area.role === "building_name" || area.role === "street_name" || key === "building_name") {
      const klass = area.role === "street_name" ? "street-name" : "building-name";
      parts.push(paintedSign(klass, text, box, { maxSize: 32, signId: key }));
      return;
    }
    if (area.role === "room_name" || key === "sign") {
      parts.push(paintedSign("room-name", text, box, { maxSize: 40, signId: key }));
      return;
    }
    if (area.role === "verb_sign" || (word && word.pos === "verb")) {
      const side = verbSide(word, scene);
      parts.push(fittedPlate(`verb-sign ${side}`, text, box, { maxSize: 16, wordId }));
      return;
    }
    const klass = key.endsWith("_plaque") || key === "plaque" ? "plaque" : "sign";
    parts.push(textBlock(klass, text, box));
  });
  return `<svg viewBox="0 0 ${scene.width} ${scene.height}" preserveAspectRatio="xMidYMid meet">${parts.join("")}</svg>`;
}

function walkHtml(dialog) {
  const place = state.place;
  const scene = place.kind === "room" ? place.room.scene : place.kind === "building" ? place.building.scene : place.sector.scene;
  const words = place.room?.words || [];
  const zooms = place.room?.zooms || [];
  const alt = place.room?.sign || localizedName(place.building) || localizedName(place.sector) || "";
  const ratio = scene ? `${scene.width} / ${scene.height}` : "16 / 9";
  return `<div class="walk-root mood-${moodFor(place)} ${state.hits ? "show-hits" : ""}" style="--ratio:${ratio}">
    <div class="frame">
      ${scene?.image ? `<img class="bleed" src="${esc(url(scene.image))}" alt="" aria-hidden="true"><img class="painting" src="${esc(url(scene.image))}" alt="${esc(alt)}">${sceneMarkup(scene, words, zooms)}` : ""}
    </div>
    <div class="dialog-host">${dialog || ""}</div>
  </div>`;
}

function activeDialog() {
  const place = state.place;
  if (!place) return "";
  if (place.kind === "room") {
    const room = place.room;
    const word = (room.words || []).find((item) => item.id === place.wordId);
    if (word) return cardLayer(word);
    if (place.talk && room.conversation) return conversationHtml(room);
    if (place.extraDialog) return place.extraDialog;
    if (state.wordsOpen) return wordsDialog(room);
  }
  if (place.extraDialog) return place.extraDialog;
  return "";
}

function wordsDialog(room) {
  return `<div class="dialog-layer">
    <article class="dialog" role="dialog" aria-labelledby="words-title">
      <button class="x" type="button" data-close-dialog aria-label="${esc(t("close"))}">×</button>
      <h2 id="words-title">${esc(t("words.title"))}</h2>
      <ul class="wordlist">${(room.words || []).map((word) => `
        <li><button type="button" data-word="${esc(word.id)}"><span class="${genderClass(word)}">${esc(word.head)}</span><small>${esc(word.painted === false ? t("words.unpainted") : word.gloss)}</small></button></li>
      `).join("")}</ul>
    </article>
  </div>`;
}

function pageShell(body, current, back = "") {
  state.place = null;
  return shell(body, current, { backNav: back });
}

function conversationHtml(room) {
  const conv = room.conversation;
  if (!conv?.lines?.length) return "";
  const lines = conv.lines.map((line, index) => `
    <article class="line" data-i="${index}" id="line-${index}">
      <div class="who">${esc(line.speaker)}</div>
      <p class="fr">${esc(state.talkLang === "fr" ? line.fr : line.en)}</p>
      ${state.showEn ? `<p class="en">${esc(state.talkLang === "fr" ? line.en : line.fr)}</p>` : ""}
    </article>`).join("");
  const title = state.lang === "fr" ? (conv.title_fr || conv.title || t("talk.title")) : (conv.title || conv.title_fr || t("talk.title"));
  const premise = state.lang === "fr" ? (conv.premise_fr || conv.premise || "") : (conv.premise || conv.premise_fr || "");
  return `<div class="dialog-layer">
    <article class="dialog" role="dialog" aria-labelledby="talk-title">
      <button class="x" type="button" data-close-dialog aria-label="${esc(t("close"))}">×</button>
      <h2 id="talk-title">${esc(title)}</h2>
      ${premise ? `<p class="premise">${esc(premise)}</p>` : ""}
      <div class="row">
        <button class="btn primary" type="button" data-play>${esc(t("talk.play"))}</button>
        <button class="btn" type="button" data-stop>${esc(t("talk.stop"))}</button>
        <button class="btn" type="button" data-en>${esc(state.showEn ? t("talk.hide") : t("talk.show"))}</button>
      </div>
      <p class="note" data-speech-note>${esc(state.speechNote || speechHint(state.talkLang === "fr" ? "fr-FR" : "en-GB"))}</p>
      ${lines}
    </article>
  </div>`;
}

function hookBlurb(word) {
  const parts = [];
  if (word.hook?.sound_alike) parts.push(word.hook.sound_alike);
  if (word.hook?.scene) parts.push(word.hook.scene);
  return parts.filter(Boolean).join(" — ");
}

function speakButton(word) {
  return `<button class="speak" type="button" data-speak="${esc(word.head)}" data-lang="fr-FR" aria-label="${esc(t("card.listen"))}">${doodle("speaker")}</button>`;
}

function cardLayer(word) {
  const hook = hookBlurb(word);
  const verb = word.pos === "verb" ? verbBlock(word) : "";
  const kind = word.pos === "verb" ? "verb" : "noun";
  const french = word.example_fr ? `<p class="example" lang="fr">${esc(word.example_fr)}</p>` : "";
  const english = word.example_en ? `<p class="example en" lang="en">${esc(word.example_en)}</p>` : "";
  const example = french || english
    ? `<div class="example-block"><div class="example-row"><div class="examples">${french}${english}</div>${speakButton(word)}</div></div>`
    : `<div class="example-block lone-speak">${speakButton(word)}</div>`;
  const respell = [word.respelling, word.ipa].filter(Boolean).join(" · ");
  const cautions = [
    word.false_cognate_note ? `<p class="caution">${esc(word.false_cognate_note)}</p>` : "",
    word.usage_warning ? `<p class="caution">${esc(word.usage_warning)}</p>` : "",
  ].join("");
  return `<div class="dialog-layer">
    <div class="card-shell ${kind}">
      <button class="x" type="button" data-close-dialog aria-label="${esc(t("close"))}">×</button>
      <article class="dialog word-card" role="dialog" aria-labelledby="card-title">
        <h2 id="card-title" class="head">${esc(word.head)}${word.reflexive ? ` ${mirrorIcon()}` : ""}</h2>
        ${word.gloss ? `<p class="gloss"><span>${esc(word.gloss)}</span></p>` : ""}
        ${respell ? `<p class="respell">${esc(respell)}</p>` : ""}
        ${hook ? `<p class="hook"><span class="field">${esc(t("card.mnemonic"))}:</span> ${esc(hook)}</p>` : ""}
        ${verb}
        ${example}
        ${cautions}
        <p class="note" data-speech-note>${esc(speechHint("fr-FR"))}</p>
      </article>
    </div>
  </div>`;
}

function mirrorIcon() {
  return `<span class="mirror" title="${esc(t("card.reflexive"))}">${doodle("twins")}</span>`;
}

function formParts(text, name) {
  const value = String(text || "").trim();
  const who = String(name || "").trim();
  if (!value) return ["", ""];
  if (who === "je" && value.startsWith("j'")) return ["j'", value.slice(2).trim()];
  if (who && value.startsWith(who)) return [who, value.slice(who.length).trim()];
  if (who && !value.includes(" ")) return [who, value];
  return ["", value];
}

function conjLine(text, name) {
  const [who, form] = formParts(text, name);
  if (!who) return `<p>${esc(form)}</p>`;
  return `<p><span class="who">${esc(who)}</span> ${esc(form)}</p>`;
}

function conjugationTable(rows, names) {
  const cells = rows.map((row, index) => conjLine(row, names[index]));
  if (cells.length <= 3) {
    return `<div class="conj-grid single">${cells.join("")}</div>`;
  }
  const left = cells.slice(0, 3).join("");
  const right = cells.slice(3, 6).join("");
  return `<div class="conj-grid"><div>${left}</div><div>${right}</div></div>`;
}

function verbBlock(word) {
  const tables = word.conjugations || {};
  const tenseOrder = ["present", "passe", "imparfait", "futur", "conditionnel", "subjonctif", "imperatif"];
  const available = tenseOrder.filter((key) => tables[key]);
  const current = available.includes(state.tense) ? state.tense : (available[0] || "present");
  const names = {
    present: ["je", "tu", "il/elle", "nous", "vous", "ils/elles"],
    passe: ["je", "tu", "il/elle", "nous", "vous", "ils/elles"],
    imparfait: ["je", "tu", "il/elle", "nous", "vous", "ils/elles"],
    futur: ["je", "tu", "il/elle", "nous", "vous", "ils/elles"],
    conditionnel: ["je", "tu", "il/elle", "nous", "vous", "ils/elles"],
    imperatif: ["tu", "nous", "vous"],
    subjonctif: ["je", "tu", "il/elle", "nous", "vous", "ils/elles"],
  };
  const tabs = available.map((key) => `<button type="button" role="tab" data-tense="${key}" aria-selected="${key === current ? "true" : "false"}">${esc(t(`tense.${key}`))}</button>`).join("");
  const rows = tables[current];
  const table = rows ? conjugationTable(rows, names[current]) : `<p class="note">${esc(t("card.noTable"))}</p>`;
  const parts = [];
  if (word.auxiliary) parts.push(`${t("card.auxiliary")} ${word.auxiliary}`);
  if (tables.participe_passe) {
    const fem = tables.participe_passe_f ? `, ${tables.participe_passe_f}` : "";
    parts.push(`${t("card.pastParticiple")} ${tables.participe_passe}${fem}`);
  }
  if (tables.participe_present) parts.push(`${t("card.presentParticiple")} ${tables.participe_present}`);
  const passe = tables.passe?.[0]
    ? `<p class="passe-line">${esc(t("tense.passe"))}: ${esc(tables.passe[0])}</p>`
    : "";
  const prep = word.prepositions?.length
    ? `<p class="field">${esc(t("card.onTheDoor"))}</p><div class="door-plaque">${word.prepositions.map((item) => `<span>${esc(item)}</span>`).join("")}</div>`
    : "";
  return `
    <div class="verb-card">
      ${word.reflexive ? `<p class="meta">${mirrorIcon()} ${esc(t("card.reflexive"))}${word.pronominal_form ? ` · ${esc(word.pronominal_form)}` : ""}</p>` : ""}
      <div class="tenses" role="tablist">${tabs}</div>
      <div class="conj-frame">
        <h3 class="tense-title">${esc(t(`tense.${current}`))}</h3>
        ${table}
      </div>
      ${passe}
      ${parts.length ? `<p class="parts">${esc(parts.join(" · "))}</p>` : ""}
      ${prep}
    </div>`;
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
      <p class="lede">${esc(tf("quiz.intro", { title: pack.title }))}</p>
      ${scoreLine(`${pack.scope}:${pack.id}`)}
      <div class="choices">
        <button type="button" data-mode="fr-en">${esc(t("modes.fr-en"))}</button>
        <button type="button" data-mode="en-fr">${esc(t("modes.en-fr"))}</button>
        <button type="button" data-mode="gender" ${genders.size < 2 ? "disabled" : ""}>${esc(genders.size < 2 ? t("quiz.oneGender") : t("modes.gender"))}</button>
        <button type="button" data-mode="listen">${esc(t("modes.listen"))}</button>
      </div>`;
  } else if (quiz.done) {
    body = `
      <p class="score">${quiz.correct} / ${quiz.round.length}</p>
      <p>${esc(t("quiz.saved"))}</p>
      <button class="btn primary" type="button" data-again>${esc(t("quiz.again"))}</button>`;
  } else {
    const item = quiz.round[quiz.index];
    const prompt = quiz.mode === "en-fr"
      ? item.gloss
      : quiz.mode === "gender"
        ? item.lemma
        : quiz.mode === "listen"
          ? t("quiz.listenPrompt")
          : item.head;
    body = `
      <p class="meta">${quiz.index + 1} / ${quiz.round.length} · ${esc(modeLabel(quiz.mode))}</p>
      <h2>${esc(prompt)}</h2>
      ${quiz.mode === "listen" ? `<div class="row"><button class="btn" type="button" data-replay>${esc(t("quiz.replay"))}</button>${quiz.reveal ? `<span>${esc(item.head)} · ${esc(item.respelling || "")}</span>` : ""}</div>` : ""}
      ${quiz.mode === "gender" ? `<p class="meta">${esc(t("quiz.genderHint"))}</p>` : ""}
      <div class="choices">
        ${quiz.choices.map((choice, index) => `<button type="button" data-choice="${index}" class="${quiz.picked == null ? "" : choice.ok ? "good" : index === quiz.picked ? "bad" : ""}" ${quiz.picked == null ? "" : "disabled"}>${esc(choice.tkey ? t(choice.tkey) : choice.label)}</button>`).join("")}
      </div>
      ${quiz.picked != null ? `<button class="btn primary" type="button" data-next>${esc(quiz.index + 1 === quiz.round.length ? t("quiz.seeScore") : t("quiz.next"))}</button>` : ""}
      <p class="note">${esc(state.speechNote)}</p>`;
  }
  return `<div class="dialog-layer">
    <article class="dialog" role="dialog" aria-labelledby="quiz-title">
      <button class="x" type="button" data-close-dialog aria-label="${esc(t("close"))}">×</button>
      <h2 id="quiz-title">${esc(pack.title)}</h2>
      ${body}
    </article>
  </div>`;
}

function modeLabel(mode) {
  return t(`modes.${mode}`);
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
      { tkey: "gender.feminine", ok: answer === "feminine" },
      { tkey: "gender.masculine", ok: answer === "masculine" },
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
    <p class="kicker">${esc(t("prayers.kicker"))}</p>
    <h1>${esc(t("prayers.title"))}</h1>
    <p class="lede">${esc(t("prayers.intro"))}</p>
    <div class="grid">
      ${prayers.prayers.map((prayer) => `<a class="card-link" href="#/prayer/${prayer.id}"><h2>${esc(state.lang === "fr" ? prayer.title_fr : prayer.title_en)}</h2><p class="meta">${esc(state.lang === "fr" ? prayer.title_en : prayer.title_fr)}</p></a>`).join("")}
    </div>
  `, "/prayers");
}

function prayerView(prayer) {
  return shell(`
    ${crumbs([{ href: "#/prayers", label: t("prayers.crumb") }, { label: state.lang === "fr" ? prayer.title_fr : prayer.title_en }])}
    <p class="kicker">${esc(state.lang === "fr" ? prayer.title_en : prayer.title_fr)}</p>
    <h1>${esc(state.lang === "fr" ? prayer.title_fr : prayer.title_en)}</h1>
    <div class="row">
      <button class="btn primary" type="button" data-speak-prayer>${esc(t("prayers.listen"))}</button>
      <button class="btn" type="button" data-en>${esc(state.showEn ? t("prayers.hide") : t("prayers.show"))}</button>
    </div>
    <p class="note">${esc(speechHint("fr-FR"))}</p>
    <p class="prayer" id="prayer-fr">${esc(prayer.fr)}</p>
    ${state.showEn ? `<p class="prayer en">${esc(prayer.en)}</p>` : ""}
    <p class="source">${esc(prayer.source || "")}</p>
  `, `/prayer/${prayer.id}`);
}

function aboutView() {
  return shell(`
    <p class="kicker">${esc(t("about.kicker"))}</p>
    <h1>${esc(t("about.title"))}</h1>
    <div class="prose">
      <p class="lede">${esc(t("about.p1"))}</p>
      <h2>${esc(t("about.h2"))}</h2>
      <p>${esc(t("about.p2"))}</p>
      <p>${esc(t("about.p3"))}</p>
      <p>${esc(t("about.p4"))}</p>
    </div>
  `, "/about");
}

function creditsView(markdown) {
  return shell(`
    <p class="kicker">${esc(t("credits.kicker"))}</p>
    <h1>${esc(t("credits.title"))}</h1>
    <div class="credits">${renderMarkdown(markdown)}</div>
    <h2>${esc(t("credits.typeTitle"))}</h2>
    <p>${esc(t("credits.fonts"))}</p>
    <p class="source">${esc(t("credits.flelex"))}</p>
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
    <h1>${esc(title || t("soon.title"))}</h1>
    <p>${esc(t("sector.closed"))}</p>
    ${open ? `<a class="btn primary" href="#/sector/${open}">${esc(t("sector.walkOpen"))}</a>` : ""}
  `);
}

function guideDialog() {
  const guide = state.guide?.[state.lang] || state.guide?.en;
  if (!guide) return "";
  const sections = (guide.sections || []).map((section) => `
    <section class="guide-section">
      <h3>${doodle(section.icon)}<span>${esc(section.title)}</span></h3>
      <p>${esc(section.body)}</p>
    </section>`).join("");
  return `<div class="dialog-layer">
    <article class="dialog guide" role="dialog" aria-labelledby="guide-title">
      <button class="x" type="button" data-close-dialog aria-label="${esc(t("close"))}">×</button>
      <h2 id="guide-title">${doodle("book")}<span>${esc(guide.title)}</span></h2>
      ${sections}
    </article>
  </div>`;
}

function mountGuide() {
  let host = document.querySelector("#guide-host");
  if (!host) {
    host = document.createElement("div");
    host.id = "guide-host";
    (document.querySelector("#stage") || document.body).appendChild(host);
  }
  host.innerHTML = state.guideOpen ? guideDialog() : "";
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
        ? t("speech.readAloud")
        : t("speech.stopped");
      const note = document.querySelector("[data-speech-note]");
      if (note) note.textContent = state.speechNote;
      return;
    }
    state.speechNote = result.voice ? "" : speechHint(state.talkLang === "fr" ? "fr-FR" : "en-GB");
    await new Promise((resolve) => window.setTimeout(resolve, 280));
  }
}

function closeDialog() {
  state.wordsOpen = false;
  const parts = parseRoute();
  if (parts[0] === "quiz") {
    location.hash = parts[1] === "room" ? `#/room/${parts[2]}` : `#/sector/${parts[2]}`;
    return;
  }
  if (parts[0] === "room" && (parts[2] === "word" || parts[2] === "talk")) {
    location.hash = `#/room/${parts[1]}`;
    return;
  }
  render();
}

function setHits(on) {
  state.hits = on;
  localStorage.setItem(HITS_KEY, on ? "1" : "0");
  document.querySelector(".walk-root")?.classList.toggle("show-hits", on);
  document.querySelectorAll("[data-hits]").forEach((button) => {
    button.setAttribute("aria-pressed", on ? "true" : "false");
  });
}

async function render() {
  const app = document.querySelector("#app");
  const walk = document.querySelector("#walk");
  state.menu = false;
  state.place = null;
  playToken += 1;
  window.speechSynthesis?.cancel();
  const parts = parseRoute();
  let html = "";
  try {
    if (!state.i18n) state.i18n = await getJSON("data/i18n.json");
    if (!state.guide) state.guide = await getJSON("data/guide.json");
    applyChrome();
    if (!state.index) state.index = await getJSON("data/index.json");
    const [kind, a, b, c] = parts;
    if (!kind) html = mapView();
    else if (kind === "sector") html = sectorView(await getJSON(`data/sectors/${a}.json`));
    else if (kind === "building") {
      const buildingInfo = state.index.buildings.find((item) => item.id === a);
      if (buildingInfo?.no_building_layer && buildingInfo.sector_id) {
        location.replace(`#/sector/${buildingInfo.sector_id}`);
        return;
      }
      if (!buildingInfo) html = soonView(t("soon.unknown"));
      else {
        const sector = await getJSON(`data/sectors/${buildingInfo.sector_id}.json`);
        const building = sector.buildings.find((item) => item.id === a);
        html = building ? buildingView(sector, building) : soonView(localizedName(buildingInfo));
      }
    } else if (kind === "room") {
      try {
        const room = await getJSON(`data/rooms/${a}.json`);
        html = roomView(room, b === "word" ? c : null, b === "talk");
        state.currentRoom = room;
      } catch {
        html = soonView(t("room.soon"));
      }
    } else if (kind === "quiz") {
      const pack = await getJSON(`data/quiz/${a}/${b}.json`);
      state.quizPack = pack;
      const dialog = quizView(pack);
      if (a === "room") {
        const room = await getJSON(`data/rooms/${b}.json`);
        html = roomView(room, null, false, dialog);
        state.currentRoom = room;
      } else if (a === "sector") html = sectorView(await getJSON(`data/sectors/${b}.json`), dialog);
      else html = pageShell(dialog, `/quiz/${a}/${b}`);
    } else if (kind === "prayers") html = prayersView(await getJSON("data/prayers.json"));
    else if (kind === "prayer") {
      const prayers = await getJSON("data/prayers.json");
      const prayer = prayers.prayers.find((item) => item.id === a);
      html = prayer ? prayerView(prayer) : soonView("Prayer");
      state.currentPrayer = prayer;
    } else if (kind === "about") html = aboutView();
    else if (kind === "credits") html = creditsView(await (await fetch(url("data/credits.md"))).text());
    else html = soonView(t("soon.unknown"));
  } catch (error) {
    html = shell(`<h1>${esc(t("error.title"))}</h1><p>${esc(error.message || t("error.body"))}</p>`);
  }
  if (state.place && walk) {
    document.body.classList.add("walking");
    walk.hidden = false;
    const current = state.place.kind === "room"
      ? `/room/${state.place.id}`
      : state.place.kind === "building"
        ? `/building/${state.place.id}`
        : `/sector/${state.place.id}`;
    app.innerHTML = shell("", current, {
      scene: true,
      backNav: backNav(state.place),
      extraNav: sceneNav(state.place),
    });
    walk.innerHTML = walkHtml(activeDialog());
  } else {
    document.body.classList.remove("walking");
    if (walk) {
      walk.hidden = true;
      walk.innerHTML = "";
    }
    app.innerHTML = html;
  }
  applyChrome();
  mountGuide();
  fitHits();
  const quiz = state.quiz;
  if (parts[0] === "quiz" && quiz && quiz.mode === "listen" && quiz.picked == null && !quiz.done) {
    const item = quiz.round[quiz.index];
    speak(item.head, "fr-FR").then((result) => {
      if (!result.ok || !result.voice) {
        quiz.reveal = true;
        state.speechNote = speechHint("fr-FR") || t("speech.failed");
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
  if (event.target.closest("[data-hits]")) {
    setHits(!state.hits);
    return;
  }
  const langBtn = event.target.closest("[data-lang-set]");
  if (langBtn) {
    setLang(langBtn.dataset.langSet);
    return;
  }
  if (event.target.closest("[data-guide]")) {
    state.guideOpen = !state.guideOpen;
    mountGuide();
    return;
  }
  const tense = event.target.closest("[data-tense]");
  if (tense) {
    state.tense = tense.dataset.tense;
    render();
    return;
  }
  if (event.target.closest("[data-fs]")) {
    if (document.fullscreenElement) document.exitFullscreen?.();
    else document.documentElement.requestFullscreen?.();
    return;
  }
  if (event.target.closest("[data-words]")) {
    state.wordsOpen = true;
    render();
    return;
  }
  if (event.target.closest("[data-close-dialog]") || event.target.classList?.contains("dialog-layer")) {
    if (state.guideOpen && event.target.closest("#guide-host")) {
      state.guideOpen = false;
      mountGuide();
      return;
    }
    closeDialog();
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
  if (event.target.closest("[data-close-card]") || event.target.classList?.contains("card-layer")) {
    closeDialog();
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
  if (event.key === "h" || event.key === "H") {
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    const tag = event.target?.tagName;
    if (tag === "INPUT" || tag === "TEXTAREA") return;
    event.preventDefault();
    setHits(!state.hits);
    return;
  }
  if (event.key === "Escape") {
    const tag = event.target?.tagName;
    if (tag === "INPUT" || tag === "TEXTAREA") return;
    if (document.querySelector(".dialog-layer")) {
      event.preventDefault();
      if (state.guideOpen) {
        state.guideOpen = false;
        mountGuide();
        return;
      }
      closeDialog();
      return;
    }
    if (document.fullscreenElement) return;
    const room = state.place?.kind === "room" ? state.place.room : null;
    if (room?.kind === "zoom") {
      const target = backTarget(state.place);
      if (target?.href) {
        event.preventDefault();
        location.hash = target.href;
      }
    }
    return;
  }
  if (!document.querySelector(".dialog-layer") && state.nav) {
    const side = state.nav.left || state.nav.right;
    let hash = "";
    if (event.key === "ArrowRight") hash = side ? (state.nav.right || state.nav.forward) : (state.nav.forward || state.nav.right);
    if (event.key === "ArrowLeft") hash = side ? (state.nav.left || state.nav.back) : (state.nav.back || state.nav.left);
    if (event.key === "ArrowUp") hash = state.nav.forward || "";
    if (event.key === "ArrowDown") hash = state.nav.back || "";
    if (hash) {
      event.preventDefault();
      location.hash = hash;
    }
  }
  const hot = event.target.closest?.(".hot");
  if (hot && (event.key === "Enter" || event.key === " ")) {
    event.preventDefault();
    hot.click();
  }
}

document.addEventListener("click", onClick);
document.addEventListener("fullscreenchange", () => {
  fitHits();
  const fullscreen = Boolean(document.fullscreenElement);
  const label = fullscreen ? t("tools.leave") : t("tools.fullscreen");
  const icon = doodle(fullscreen ? "collapse" : "expand");
  document.querySelectorAll("[data-fs]").forEach((button) => {
    button.setAttribute("aria-label", label);
    const caption = button.querySelector(".tool-label");
    if (caption) caption.textContent = label;
    const mark = button.querySelector(".tool-icon");
    if (mark) mark.innerHTML = icon;
  });
});
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
