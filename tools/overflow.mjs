import { chromium } from "playwright";
const [, , path = "/", w = "390"] = process.argv;
const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());
const page = await browser.newPage({ viewport: { width: +w, height: 800 } });
await page.goto("http://localhost:8765" + path, { waitUntil: "networkidle" });
await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } });
await page.waitForTimeout(1500);
console.log(await page.evaluate(() => {
  const vw = document.documentElement.clientWidth, out = [];
  document.querySelectorAll("body *").forEach((el) => {
    const r = el.getBoundingClientRect();
    if (r.right > vw + 1 && r.right < vw + 40 && r.width > 0 && getComputedStyle(el).position !== "fixed") out.push(`${el.tagName.toLowerCase()}.${[...el.classList].join(".")} right=${Math.round(r.right)} w=${Math.round(r.width)}`);
  });
  return { vw, sw: document.documentElement.scrollWidth, els: out.slice(0, 15) };
}));
await browser.close();

