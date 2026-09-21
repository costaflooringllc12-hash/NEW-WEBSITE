import { chromium } from "playwright";
const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
await page.goto("http://localhost:8765/", { waitUntil: "networkidle" });
await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
await page.waitForTimeout(800);
await page.screenshot({ path: "tools/shots/bottom-m.png" });
console.log(await page.evaluate(() => ({ h: document.body.scrollHeight, last: document.body.lastElementChild.tagName, footerBottom: Math.round(document.querySelector("footer").getBoundingClientRect().bottom + window.scrollY) })));
await browser.close();
