import { chromium } from "playwright";
const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());
for (const [path, w] of [["/", 1440], ["/", 390], ["/services/floor-repair/", 1440], ["/estimate/", 390]]) {
  const page = await browser.newPage({ viewport: { width: w, height: 900 } });
  await page.goto("http://localhost:8765" + path, { waitUntil: "networkidle" });
  const rows = await page.evaluate(() => [...document.querySelectorAll("main > section, footer, .page-hero, .hero")].map((el) => {
    const cs = getComputedStyle(el);
    return `${el.id || el.className.split(" ")[0]}: top ${cs.paddingTop} / bottom ${cs.paddingBottom}`;
  }));
  console.log(`\n== ${path} @${w}`); console.log(rows.join("\n"));
  await page.close();
}
await browser.close();
