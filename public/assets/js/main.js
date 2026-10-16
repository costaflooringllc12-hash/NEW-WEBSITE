/* Costa Flooring — vanilla JS, no dependencies. */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Header: transparent over the hero, solid once scrolled ---------- */
  var header = document.getElementById("header");
  var darkTop = document.querySelector("main > .hero, main > .page-hero");
  if (header && !darkTop) {
    header.classList.add("is-solid"); // no dark hero to sit over: always solid
  } else if (header) {
    var raf = null;
    function updateHeader() { raf = null; header.classList.toggle("is-solid", window.scrollY > 60); }
    window.addEventListener("scroll", function () { if (!raf) raf = requestAnimationFrame(updateHeader); }, { passive: true });
    window.addEventListener("pageshow", updateHeader);
    updateHeader();
  }

  /* ---------- Mobile drawer ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var drawer = document.getElementById("drawer");
  function setDrawer(open) {
    if (!toggle || !drawer) return;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    drawer.classList.toggle("is-open", open);
    document.body.classList.toggle("nav-open", open);
  }
  if (toggle && drawer) {
    toggle.addEventListener("click", function () { setDrawer(toggle.getAttribute("aria-expanded") !== "true"); });
    drawer.addEventListener("click", function (e) { if (e.target.closest("a")) setDrawer(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && drawer.classList.contains("is-open")) { setDrawer(false); toggle.focus(); } });
    window.matchMedia("(min-width: 64em)").addEventListener("change", function (mq) { if (mq.matches) setDrawer(false); });
  }

  /* ---------- Reveal + timeline draw ---------- */
  document.querySelectorAll("[data-stagger]").forEach(function (list) {
    Array.prototype.forEach.call(list.children, function (child, i) { child.style.setProperty("--i", i); });
  });
  var reveals = document.querySelectorAll(".reveal, .timeline, .contact-bar");
  if (reveals.length && "IntersectionObserver" in window && !reduce) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); ro.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.05 });
    reveals.forEach(function (el) { ro.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- FAQ accordion ---------- */
  document.querySelectorAll(".faq__q").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".faq__item");
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!open));
      item.classList.toggle("is-open", !open);
    });
  });

  /* ---------- Before / after sliders ---------- */
  document.querySelectorAll(".ba").forEach(function (ba) {
    var range = ba.querySelector("input[type=range]");
    if (!range) return;
    function update() { ba.style.setProperty("--pos", range.value + "%"); }
    range.addEventListener("input", update);
    update();
  });

  /* ---------- Portfolio wall: pause off-screen; lightbox on click ---------- */
  var wall = document.querySelector("[data-wall]");
  var lb = document.getElementById("lightbox");
  if (wall && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) { wall.classList.toggle("is-paused", !entries[0].isIntersecting); }, { threshold: 0.05 }).observe(wall);
  }
  if (wall && lb) {
    var lbImg = lb.querySelector(".lb__img");
    var lastTrigger = null;
    function openLb(a) {
      var img = a.querySelector("img");
      lbImg.src = a.getAttribute("href");
      lbImg.alt = img ? img.alt : "";
      lb.hidden = false;
      requestAnimationFrame(function () { lb.classList.add("is-open"); });
      document.body.style.overflow = "hidden";
      lastTrigger = a;
      lb.querySelector("[data-lb-close]").focus();
    }
    function closeLb() {
      lb.classList.remove("is-open");
      document.body.style.overflow = "";
      setTimeout(function () { lb.hidden = true; lbImg.src = ""; }, 250);
      if (lastTrigger) lastTrigger.focus();
    }
    wall.addEventListener("click", function (e) {
      var a = e.target.closest("[data-lb]");
      if (!a) return;
      e.preventDefault();
      if (lb.hidden) openLb(a);
    });
    lb.addEventListener("click", function (e) { if (e.target === lb || e.target.closest("[data-lb-close]")) closeLb(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !lb.hidden) closeLb(); });
  }

  /* ---------- Stain lab: click a swatch, the floor takes the colour ---------- */
  var lab = document.querySelector("[data-stain-lab]");
  if (lab) {
    var floor = lab.querySelector(".stain-floor");
    var nameEl = lab.querySelector(".stain-floor__name");
    var swatches = lab.querySelectorAll(".swatch");
    swatches.forEach(function (b) {
      b.addEventListener("click", function () {
        swatches.forEach(function (o) { o.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true");
        floor.style.setProperty("--stain", b.getAttribute("data-color"));
        if (nameEl) nameEl.textContent = b.getAttribute("data-name");
      });
    });
  }

  /* ---------- Service-area map: Leaflet + OSM, loaded when the map scrolls near ---------- */
  var areaMap = document.getElementById("area-map");
  if (areaMap) {
    var LEAFLET = "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min";
    function initMap() {
      var pins = JSON.parse(areaMap.getAttribute("data-pins") || "[]");
      var map = L.map(areaMap, { scrollWheelZoom: false, zoomControl: true, zoomSnap: 0.25 }).setView([40.65, -74.25], 10);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 18, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' }).addTo(map);
      pins.forEach(function (p) {
        var home = !!p[3];
        var icon = L.divIcon({ className: "map-pin" + (home ? " map-pin--home" : ""), html: '<span class="map-pin__ring"></span><span class="map-pin__dot"></span>', iconSize: [28, 28], iconAnchor: [14, 14] });
        L.marker([p[1], p[2]], { icon: icon, title: p[0], keyboard: false }).addTo(map)
          .bindTooltip(p[0], { permanent: home, direction: "top", offset: [0, -12], className: "map-label" });
      });
      if (pins.length) map.fitBounds(pins.map(function (p) { return [p[1], p[2]]; }), { padding: [30, 30] });
    }
    function loadMap() {
      if (window.L) return initMap();
      var css = document.createElement("link"); css.rel = "stylesheet"; css.href = LEAFLET + ".css"; document.head.appendChild(css);
      var js = document.createElement("script"); js.src = LEAFLET + ".js"; js.async = true; js.onload = initMap; document.head.appendChild(js);
    }
    if ("IntersectionObserver" in window) {
      var mo = new IntersectionObserver(function (entries) { if (entries[0].isIntersecting) { mo.disconnect(); loadMap(); } }, { rootMargin: "300px 0px" });
      mo.observe(areaMap);
    } else { loadMap(); }
  }

  /* ---------- Lead form: inline validation, then native submit ---------- */
  var form = document.getElementById("form01");
  if (form) {
    var fields = form.querySelectorAll("[required]");
    function validate(input) {
      var wrap = input.closest(".field");
      var ok = input.checkValidity();
      if (input.type === "tel") ok = ok && /\d{7,}/.test(input.value.replace(/\D/g, ""));
      if (wrap) wrap.classList.toggle("is-invalid", !ok);
      input.setAttribute("aria-invalid", String(!ok));
      return ok;
    }
    fields.forEach(function (f) {
      f.addEventListener("blur", function () { validate(f); });
      f.addEventListener("input", function () { if (f.closest(".field.is-invalid")) validate(f); });
    });
    form.addEventListener("submit", function (e) {
      var firstBad = null;
      fields.forEach(function (f) { if (!validate(f) && !firstBad) firstBad = f; });
      if (firstBad) { e.preventDefault(); firstBad.focus(); return; }
      var hp = form.querySelector("input.hp");
      if (hp && hp.value) { e.preventDefault(); return; }
      var btn = form.querySelector('[type="submit"]');
      if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }
    });
  }

  /* ---------- Blog post: reading progress + active section in the table of contents ---------- */
  var article = document.getElementById("article");
  var bar = document.querySelector(".read-progress span");
  if (article && bar) {
    var pRaf = null;
    function progress() {
      pRaf = null;
      var r = article.getBoundingClientRect();
      var total = r.height - window.innerHeight;
      var done = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 1;
      bar.style.transform = "scaleX(" + done + ")";
    }
    window.addEventListener("scroll", function () { if (!pRaf) pRaf = requestAnimationFrame(progress); }, { passive: true });
    progress();
  }
  var tocLinks = document.querySelectorAll(".toc--side a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    tocLinks.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var heads = Object.keys(byId).map(function (id) { return document.getElementById(id); }).filter(Boolean);
    var to = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        tocLinks.forEach(function (a) { a.classList.remove("is-active"); a.removeAttribute("aria-current"); });
        var link = byId[en.target.id];
        if (link) { link.classList.add("is-active"); link.setAttribute("aria-current", "true"); }
      });
    }, { rootMargin: "-15% 0px -70% 0px" });
    heads.forEach(function (h) { to.observe(h); });
  }

  /* ---------- Blog hub: filter cards by topic (chips stay hidden without JS) ---------- */
  var chipGroup = document.querySelector("[data-filter-group]");
  var filterList = document.querySelector("[data-filter-list]");
  if (chipGroup && filterList) {
    var chips = chipGroup.querySelectorAll(".chip");
    var empty = document.querySelector(".filter-empty");
    function applyFilter(cat) {
      var shown = 0;
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c.getAttribute("data-filter") === cat)); });
      filterList.querySelectorAll(".post-card").forEach(function (card) {
        var on = cat === "all" || card.getAttribute("data-cat") === cat;
        card.hidden = !on;
        if (on) shown++;
      });
      if (empty) empty.hidden = shown > 0;
    }
    chipGroup.hidden = false;
    chips.forEach(function (c) { c.addEventListener("click", function () { applyFilter(c.getAttribute("data-filter")); }); });
    var hash = location.hash.slice(1);
    if (chipGroup.querySelector('[data-filter="' + hash + '"]')) applyFilter(hash);
  }

  /* ---------- Footer year ---------- */
  var y = document.getElementById("year");
  if (y) y.textContent = String(new Date().getFullYear());
})();
