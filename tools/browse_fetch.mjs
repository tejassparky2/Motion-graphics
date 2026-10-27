// Render a public web page in headless Chromium and print its visible text (for JS-heavy pages WebFetch can't read).
//   node tools/browse_fetch.mjs URL [--html] [--wait MS]
// Research use only: public pages, honest user agent. Do not use it on sites that block automated access or need a login.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const url = process.argv[2];
const html = process.argv.includes('--html');
const wi = process.argv.indexOf('--wait');
const wait = wi > 0 ? Number(process.argv[wi + 1]) : 1500;
if (!url) { console.error('usage: node tools/browse_fetch.mjs URL [--html] [--wait MS]'); process.exit(2); }
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', headless: true });
const page = await browser.newPage({ userAgent: 'yours3d-research/0.1 (headless Chromium; research)' });
try {
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(wait);
  console.log(html ? await page.content() : await page.evaluate(() => document.body.innerText));
} finally { await browser.close(); }
