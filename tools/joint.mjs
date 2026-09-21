import { chromium } from "playwright";
const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());
for (const w of [1440, 390]) {
  const page = await browser.newPage({ viewport: { width: w, height: 900 } });
  await page.goto("http://localhost:8765/", { waitUntil: "networkidle" });
  const y = await page.evaluate(() => document.querySelector(".hero__strip").getBoundingClientRect().top + window.scrollY - 260);
  await page.evaluate((y) => window.scrollTo(0, y), y);
  await page.waitForTimeout(700);
  await page.screenshot({ path: `tools/shots/joint-${w}.png`, clip: { x: 0, y: 0, width: w, height: 600 } });
  await page.close();
}
await browser.close();
