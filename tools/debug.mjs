import { chromium } from "playwright";
const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
page.on("console", (m) => console.log("[console]", m.type(), m.text()));
page.on("pageerror", (e) => console.log("[pageerror]", e.message));
await page.goto("http://localhost:8765/", { waitUntil: "networkidle" });
await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 80)); } });
await page.waitForTimeout(500);
console.log(await page.evaluate(() => ({
  reveals: document.querySelectorAll(".reveal").length,
  revealsIn: document.querySelectorAll(".reveal.is-in").length,
  timelineIn: !!document.querySelector(".timeline.is-in"),
  motion: matchMedia("(prefers-reduced-motion: reduce)").matches,
  solid: document.getElementById("header").className,
})));
await browser.close();
