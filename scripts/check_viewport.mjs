/**
 * Every painted item, exit and zoom box must sit fully inside the viewport
 * and clear of the cream strip. Windowed and fullscreen, at each size below.
 *
 * Preview must already be serving the built site (npm run preview).
 */
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import puppeteer from "puppeteer-core";

const base = process.env.PREVIEW_URL || "http://127.0.0.1:4173/";
const sizes = [
  { name: "1280x800", width: 1280, height: 800 },
  { name: "1440x900", width: 1440, height: 900 },
  { name: "1920x1080", width: 1920, height: 1080 },
  { name: "2560x1080", width: 2560, height: 1080 },
  { name: "390x844", width: 390, height: 844 },
];

function chromePath() {
  const candidates = [
    process.env.CHROME_PATH,
    "/usr/local/bin/google-chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
  ];
  return candidates.find((path) => path && existsSync(path));
}

async function routes(page) {
  const index = await page.evaluate(async (root) => {
    const response = await fetch(`${root}data/index.json`);
    if (!response.ok) throw new Error(`index json ${response.status}`);
    return response.json();
  }, base);
  const list = [];
  const rooms = [];
  const seen = new Set();
  const addRoom = (id) => {
    if (!id || seen.has(id)) return;
    seen.add(id);
    rooms.push(id);
  };
  for (const sectorId of index.open_sectors || []) {
    const sector = await page.evaluate(async (root, id) => {
      const response = await fetch(`${root}data/sectors/${id}.json`);
      if (!response.ok) throw new Error(`sector json ${response.status}`);
      return response.json();
    }, base, sectorId);
    if (sector.scene?.image) list.push({ id: sector.id, hash: `#/sector/${sector.id}`, image: sector.scene.image });
    for (const building of sector.buildings || []) {
      if (building.scene?.image) list.push({ id: building.id, hash: `#/building/${building.id}`, image: building.scene.image });
      for (const floor of building.floors || []) {
        for (const room of floor.rooms || []) if (room.open !== false) addRoom(room.id);
      }
    }
    for (const alley of sector.alleys || []) addRoom(alley.id);
  }
  for (let index = 0; index < rooms.length; index += 1) {
    const id = rooms[index];
    const room = await page.evaluate(async (root, roomId) => {
      const response = await fetch(`${root}data/rooms/${roomId}.json`);
      if (!response.ok) return null;
      const text = await response.text();
      try {
        return JSON.parse(text);
      } catch {
        return null;
      }
    }, base, id);
    if (room?.scene?.image) list.push({ id, hash: `#/room/${id}`, image: room.scene.image });
    for (const zoom of room?.zooms || []) addRoom(zoom.id);
  }
  return list;
}

async function openScene(page, place) {
  await page.evaluate((next) => {
    location.hash = next;
  }, place.hash);
  await page.waitForFunction((needle) => {
    const img = document.querySelector("#walk img.painting");
    return img && (img.getAttribute("src") || "").includes(needle) && img.complete && img.naturalWidth > 0;
  }, { timeout: 8000 }, place.image);
  await page.evaluate(() => new Promise((resolve) => {
    requestAnimationFrame(() => requestAnimationFrame(resolve));
  }));
  return "paint";
}

function measure() {
  const eps = 2;
  const img = document.querySelector("#walk img.painting");
  const svg = document.querySelector("#walk svg");
  const strips = [...document.querySelectorAll(".top, footer.site")]
    .map((node) => node.getBoundingClientRect())
    .filter((rect) => rect.width > 0 && rect.height > 0 && rect.bottom > 0);
  const frame = img.getBoundingClientRect();
  const scale = Math.min(frame.width / img.naturalWidth, frame.height / img.naturalHeight);
  const width = img.naturalWidth * scale;
  const height = img.naturalHeight * scale;
  const content = {
    left: frame.left + (frame.width - width) / 2,
    top: frame.top + (frame.height - height) / 2,
    width,
    height,
  };
  content.right = content.left + content.width;
  content.bottom = content.top + content.height;
  const failures = [];
  const fit = getComputedStyle(img).objectFit;
  if (fit !== "contain") failures.push(`painting object-fit is ${fit}`);
  const aspect = content.width / content.height;
  const natural = img.naturalWidth / img.naturalHeight;
  if (Math.abs(aspect - natural) > 0.02) failures.push("painting aspect changed");
  if (content.left < -eps || content.top < -eps || content.right > innerWidth + eps || content.bottom > innerHeight + eps) {
    failures.push(`painting extends outside the viewport (${content.left.toFixed(1)},${content.top.toFixed(1)} ${content.right.toFixed(1)},${content.bottom.toFixed(1)})`);
  }
  for (const strip of strips) {
    const overlap = Math.min(content.right, strip.right) - Math.max(content.left, strip.left);
    const overlapY = Math.min(content.bottom, strip.bottom) - Math.max(content.top, strip.top);
    if (overlap > eps && overlapY > eps) failures.push("painting sits under a strip");
  }
  const ctm = svg.getScreenCTM();
  if (!ctm) {
    failures.push("svg has no screen transform");
    return failures;
  }
  const origin = svg.createSVGPoint();
  origin.x = 0;
  origin.y = 0;
  const far = svg.createSVGPoint();
  far.x = svg.viewBox.baseVal.width;
  far.y = svg.viewBox.baseVal.height;
  const o = origin.matrixTransform(ctm);
  const f = far.matrixTransform(ctm);
  if (Math.abs(o.x - content.left) > eps || Math.abs(o.y - content.top) > eps || Math.abs(f.x - content.right) > eps || Math.abs(f.y - content.bottom) > eps) {
    failures.push("hotspot transform does not match the painting");
  }
  const project = (box) => {
    const [x0, y0, x1, y1] = box.split(",").map(Number);
    const a = svg.createSVGPoint();
    a.x = x0;
    a.y = y0;
    const b = svg.createSVGPoint();
    b.x = x1;
    b.y = y1;
    const pa = a.matrixTransform(ctm);
    const pb = b.matrixTransform(ctm);
    return {
      left: Math.min(pa.x, pb.x),
      top: Math.min(pa.y, pb.y),
      right: Math.max(pa.x, pb.x),
      bottom: Math.max(pa.y, pb.y),
    };
  };
  const hitsStrip = (rect) => strips.some((strip) => {
    const overlap = Math.min(rect.right, strip.right) - Math.max(rect.left, strip.left);
    const overlapY = Math.min(rect.bottom, strip.bottom) - Math.max(rect.top, strip.top);
    return overlap > eps && overlapY > eps;
  });
  const offscreen = (rect) => rect.left < -eps || rect.top < -eps || rect.right > innerWidth + eps || rect.bottom > innerHeight + eps;
  const endingOnly = (value) => {
    const parts = String(value || "").trim().split(/\s*\/\s*/).map((part) => part.trim()).filter(Boolean);
    return parts.length > 0 && parts.every((part) => /^-(?:er|ir|re)$/i.test(part));
  };
  for (const sign of svg.querySelectorAll(".painted-sign, .way-pill, .soon-pill, .name-tag")) {
    const value = [...sign.querySelectorAll("text, span")].map((node) => node.textContent || "").join(" ").replace(/\s+/g, " ").trim()
      || (sign.textContent || "").replace(/\s+/g, " ").trim();
    if (endingOnly(value)) failures.push(`ending overlay still shown: ${value}`);
  }
  for (const node of document.querySelectorAll("#walk .way-pill, #walk .soon-pill")) {
    const value = (node.textContent || "").replace(/\s+/g, " ").trim();
    if (endingOnly(value)) failures.push(`ending label still shown: ${value}`);
  }
  for (const node of svg.querySelectorAll("[data-item-box], [data-way-box], [data-zoom-box], [data-soon-box]")) {
    const raw = node.dataset.itemBox || node.dataset.wayBox || node.dataset.zoomBox || node.dataset.soonBox;
    if (!raw) continue;
    const rect = project(raw);
    if (rect.right - rect.left < 1 || rect.bottom - rect.top < 1) continue;
    const name = node.getAttribute("aria-label") || node.dataset.word || node.dataset.target || raw;
    if (offscreen(rect)) failures.push(`${name} is outside the viewport`);
    else if (hitsStrip(rect)) failures.push(`${name} is under a strip`);
  }
  const hash = location.hash || "";
  const up = document.querySelector("[data-sector-up]");
  if (/^#\/(building|room)\//.test(hash)) {
    const href = up?.getAttribute("href") || "";
    if (!up) failures.push("missing sector button");
    else if (!/^#\/sector\/S\d{2}_/.test(href)) failures.push(`sector button target ${href}`);
  } else if (/^#\/sector\//.test(hash) && up) {
    failures.push("sector view shows a sector button");
  }
  const covers = (a, b) => {
    const overlapX = Math.min(a.right, b.right) - Math.max(a.left, b.left);
    const overlapY = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
    return overlapX > 8 && overlapY > 6;
  };
  for (const badge of document.querySelectorAll("#walk .way-badge")) {
    const badgeRect = badge.getBoundingClientRect();
    for (const text of svg.querySelectorAll(".painted-sign text, .verb-sign text, text.lbl")) {
      const rect = text.getBoundingClientRect();
      if (rect.width < 2 || rect.height < 2) continue;
      if (covers(badgeRect, rect)) failures.push(`arrow covers ${(text.textContent || "").trim()}`);
    }
  }
  return failures;
}

async function ensurePreview() {
  try {
    const response = await fetch(base, { signal: AbortSignal.timeout(1500) });
    if (response.ok) return null;
  } catch {
    /* start a preview for this run */
  }
  const root = fileURLToPath(new URL("..", import.meta.url));
  const child = spawn("npx", ["vite", "preview", "--host", "127.0.0.1", "--port", "4173", "--strictPort"], {
    cwd: root,
    stdio: "ignore",
  });
  for (let attempt = 0; attempt < 40; attempt += 1) {
    try {
      const response = await fetch(base);
      if (response.ok) return child;
    } catch {
      /* not up yet */
    }
    await new Promise((resolve) => setTimeout(resolve, 250));
  }
  child.kill();
  throw new Error("preview did not start");
}

async function main() {
  const executablePath = chromePath();
  if (!executablePath) {
    console.error("chrome not found");
    process.exit(1);
  }
  const preview = await ensurePreview();
  const browser = await puppeteer.launch({
    executablePath,
    headless: "new",
    args: ["--no-sandbox", "--disable-dev-shm-usage"],
    defaultViewport: sizes[0],
  });
  const page = await browser.newPage();
  await page.goto(base, { waitUntil: "domcontentloaded" });
  await page.evaluate(() => {
    localStorage.setItem("memory-village-lang", "en");
    localStorage.setItem("memory-village-hits", "0");
  });
  await page.goto(`${base}#/sector/S04_cafes`, { waitUntil: "networkidle0" });
  const places = await routes(page);
  const failures = [];
  let painted = 0;
  for (const size of sizes) {
    await page.setViewport(size);
    for (const mode of ["windowed", "fullscreen"]) {
      if (mode === "fullscreen") {
        const button = await page.$("[data-fs]");
        if (!button) {
          failures.push(`${size.name} fullscreen: no fullscreen control`);
          continue;
        }
        await button.click();
        try {
          await page.waitForFunction(() => document.fullscreenElement, { timeout: 3000 });
        } catch {
          failures.push(`${size.name} fullscreen: did not enter fullscreen`);
          continue;
        }
      } else if (await page.evaluate(() => document.fullscreenElement)) {
        await page.evaluate(() => document.exitFullscreen());
        await page.waitForFunction(() => !document.fullscreenElement);
      }
      for (const place of places) {
        await openScene(page, place);
        if (mode === "windowed") painted += 1;
        const found = await page.evaluate(measure);
        for (const message of found) failures.push(`${size.name} ${mode} ${place.id}: ${message}`);
      }
    }
  }
  await browser.close();
  preview?.kill();
  const views = painted / sizes.length;
  if (failures.length) {
    console.error(failures.slice(0, 40).join("\n"));
    console.error(`${failures.length} viewport failures`);
    process.exit(1);
  }
  console.log(`ok paintings fit: ${views} spaces, ${sizes.length} sizes, windowed and fullscreen, 0 failures`);
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
