import { chromium } from "playwright";
const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
const paths = process.argv.slice(2);
for (const p of paths) {
  await page.goto("http://localhost:8765" + p, { waitUntil: "networkidle" });
  await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } });
  await page.waitForTimeout(800);
  const bad = await page.evaluate(() => [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.currentSrc || i.src));
  console.log(p, bad.length ? "BROKEN: " + bad.join(", ") : "all images ok");
}
await browser.close();
