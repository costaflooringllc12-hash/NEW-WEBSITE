// Screenshot QA: node tools/shots.mjs [outDir]
// Requires the local server: python -m http.server 8765 --directory public
import { chromium } from "playwright";
import fs from "node:fs";

const out = process.argv[2] || "tools/shots";
fs.mkdirSync(out, { recursive: true });
const base = "http://localhost:8765";
const pages = ["/", "/services/", "/services/hardwood-floor-refinishing/", "/about/", "/estimate/", "/service-areas/", "/thanks/", "/404.html"];
const widths = [390, 768, 1440];

const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());
const issues = [];
for (const w of widths) {
  const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  page.on("console", (m) => { if (m.type() === "error") issues.push(`[console ${w}] ${page.url()} ${m.text()}`); });
  page.on("requestfailed", (r) => issues.push(`[reqfail ${w}] ${r.url()}`));
  page.on("response", (r) => { if (r.status() >= 400 && r.url().startsWith(base)) issues.push(`[${r.status()} ${w}] ${r.url()}`); });
  for (const p of pages) {
    await page.goto(base + p, { waitUntil: "networkidle" });
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } window.scrollTo(0, 0); });
    await page.waitForTimeout(800);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
    if (overflow) issues.push(`[overflow ${w}] ${p}`);
    const name = (p === "/" ? "home" : p.replace(/[^a-z0-9]+/gi, "-").replace(/^-|-$/g, "")) + `-${w}.png`;
    await page.screenshot({ path: `${out}/${name}`, fullPage: true });
  }
  await ctx.close();
}
await browser.close();
fs.writeFileSync(`${out}/issues.txt`, issues.join("\n") || "none");
console.log(issues.length ? issues.join("\n") : "no issues");
