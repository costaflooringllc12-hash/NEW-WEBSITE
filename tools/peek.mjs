// node tools/peek.mjs <path> <selector> <width> <out.png>
import { chromium } from "playwright";
const [, , path, sel, w, out] = process.argv;
const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());
const page = await browser.newPage({ viewport: { width: +w, height: 900 } });
await page.goto("http://localhost:8765" + path, { waitUntil: "networkidle" });
const el = page.locator(sel).first();
await el.scrollIntoViewIfNeeded();
await page.waitForTimeout(1200);
await el.screenshot({ path: out });
await browser.close();
