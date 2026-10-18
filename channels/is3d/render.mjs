// Record an Interestingly Strange 3D scene (channels/is3d) frame by frame in headless Chromium (engine from channels/lowpoly).
//   [SCENE=scene_is3d.html] node channels/is3d/render.mjs OUT_DIR [fps=30] [scale=1] [t1,t2,...]
// Writes OUT_DIR/f00000.png ... (or only the listed times, for quick checks). Needs three + playwright-core
// installed in build/is3d (npm install three playwright-core).
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "../..");
const MODS = path.join(ROOT, "build/is3d/node_modules");
const {chromium} = await import(path.join(MODS, "playwright-core/index.mjs"));

const [out, fpsArg = "30", scaleArg = "1", times] = process.argv.slice(2);
const fps = Number(fpsArg), scale = Number(scaleArg);
fs.mkdirSync(out, {recursive: true});

const TYPES = {".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".json": "application/json"};
const SCENE = process.env.SCENE || "scene_is3d.html";
const server = http.createServer((req, res) => {
  const url = decodeURIComponent(req.url.split("?")[0]);
  const file = url.startsWith("/node_modules/") ? path.join(MODS, url.slice(14))
    : url === "/timing.json" ? path.join(ROOT, "build/is3d/timing.json") : path.join(HERE, url === "/" ? SCENE : url);
  if (!file.startsWith(MODS) && !file.startsWith(HERE) && !file.endsWith("timing.json")) { res.writeHead(403); return res.end(); }
  fs.readFile(file, (err, data) => {
    if (err) { res.writeHead(404); return res.end(); }
    res.writeHead(200, {"Content-Type": TYPES[path.extname(file)] || "application/octet-stream"});
    res.end(data);
  });
}).listen(0, "127.0.0.1");
await new Promise(r => server.on("listening", r));

const exe = ["/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell", "/opt/pw-browsers/chromium"].find(p => fs.existsSync(p) && fs.statSync(p).isFile());
const browser = await chromium.launch({executablePath: exe, args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]});
const page = await browser.newPage({viewport: {width: 720, height: 1280}, deviceScaleFactor: scale});
page.on("pageerror", e => console.error("page error:", e.message));
page.on("console", m => m.type() === "error" && console.error("console:", m.text()));
await page.goto(`http://127.0.0.1:${server.address().port}/${SCENE}`);
await page.waitForFunction(() => window.READY === true, null, {timeout: 60000});

const dur = await page.evaluate(() => window.DURATION);
const list = times ? times.split(",").map(Number) : Array.from({length: Math.round(dur * fps)}, (_, i) => i / fps);
const t0 = Date.now();
for (let i = 0; i < list.length; i++) {
  const data = await page.evaluate(t => { window.renderAt(t); return document.querySelector("canvas").toDataURL("image/png"); }, list[i]);
  const name = times ? `t${list[i].toFixed(2)}.png` : `f${String(i).padStart(5, "0")}.png`;
  fs.writeFileSync(path.join(out, name), Buffer.from(data.split(",")[1], "base64"));
  if (i % 30 === 0) process.stderr.write(`frame ${i}/${list.length} (${((Date.now() - t0) / 1000).toFixed(0)} s)\n`);
}
await browser.close();
server.close();
console.log(`wrote ${list.length} frames to ${out}`);
