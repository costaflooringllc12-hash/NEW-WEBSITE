import { chromium } from "playwright";
import fs from "node:fs";
const [out, w, path, sel] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());
const page = await browser.newPage({ viewport: { width: +w, height: 900 } });
await page.goto("http://localhost:8765" + path, { waitUntil: "networkidle" });
await page.evaluate(() => document.querySelectorAll(".reveal").forEach(e => e.classList.add("is-in")));
const els = await page.$$(sel);
let i = 0;
for (const el of els) {
  await el.scrollIntoViewIfNeeded();
  await page.waitForTimeout(350);
  await el.screenshot({ path: `${out}/${path.replace(/[^a-z0-9]+/gi, "-")}${w}-${i++}.png` });
}
console.log(els.length, "shots");
await browser.close();
