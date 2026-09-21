// node shot.mjs <outDir> <path...>  — full-page screenshots at 390 and 1440 + overflow/console check
import { chromium } from "playwright";
import fs from "node:fs";
const out = process.argv[2];
const pages = process.argv.slice(3);
fs.mkdirSync(out, { recursive: true });
const base = "http://localhost:8765";
const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());
const issues = [];
for (const w of [390, 1440]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  page.on("console", (m) => { if (m.type() === "error") issues.push(`[console ${w}] ${page.url()} ${m.text()}`); });
  page.on("response", (r) => { if (r.status() >= 400 && r.url().startsWith(base)) issues.push(`[${r.status()} ${w}] ${r.url()}`); });
  for (const p of pages) {
    await page.goto(base + p, { waitUntil: "networkidle" });
    await page.evaluate(() => document.querySelectorAll("img[loading=lazy]").forEach((i) => { i.loading = "eager"; }));
    await page.waitForLoadState("networkidle");
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } window.scrollTo(0, 0); });
    await page.evaluate(() => document.querySelectorAll(".reveal, .timeline").forEach((e) => e.classList.add("is-in")));
    await page.waitForTimeout(1200);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
    if (overflow) issues.push(`[overflow ${w}] ${p}`);
    const name = p.replace(/[^a-z0-9]+/gi, "-").replace(/^-|-$/g, "") + `-${w}.png`;
    await page.screenshot({ path: `${out}/${name}`, fullPage: true });
  }
  await ctx.close();
}
await browser.close();
console.log(issues.length ? issues.join("\n") : "no issues");
