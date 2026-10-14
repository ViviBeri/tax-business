(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function mountProgress() {
    if (document.getElementById("kvb-progress")) return;
    var bar = document.createElement("div");
    bar.id = "kvb-progress";
    bar.setAttribute("aria-hidden", "true");
    document.body.appendChild(bar);
    var raf = 0;
    function update() {
      raf = 0;
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      var p = max > 0 ? (h.scrollTop || document.body.scrollTop) / max : 0;
      bar.style.width = (p * 100).toFixed(2) + "%";
    }
    window.addEventListener("scroll", function () {
      if (!raf) raf = requestAnimationFrame(update);
    }, { passive: true });
    update();
  }

  function headerShadow() {
    var top = document.querySelector(".topbar");
    if (!top) return;
    function tick() {
      if (window.scrollY > 8) top.classList.add("is-scrolled");
      else top.classList.remove("is-scrolled");
    }
    window.addEventListener("scroll", tick, { passive: true });
    tick();
  }

  function reveals() {
    if (reduce || !("IntersectionObserver" in window)) return;
    var targets = document.querySelectorAll(
      ".service-card, .step, .locations a, .tool-grid > div, .faq-list details, .about-points > div, .newbiz"
    );
    if (!targets.length) return;
    targets.forEach(function (el) { el.classList.add("kvb-reveal"); });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("is-in");
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    targets.forEach(function (el) { io.observe(el); });
  }

  function enhanceMenu() {
    var btn = document.getElementById("menuBtn");
    var nav = document.getElementById("mainNav");
    if (!btn || !nav) return;
    var mo = new MutationObserver(function () {
      nav.classList.toggle("is-open", btn.getAttribute("aria-expanded") === "true");
    });
    mo.observe(btn, { attributes: true, attributeFilter: ["aria-expanded"] });
  }

  function dismissMenu() {
    var btn = document.getElementById("menuBtn");
    var nav = document.getElementById("mainNav");
    if (!btn || !nav) return;
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") btn.click();
    });
    document.addEventListener("click", function (e) {
      if (btn.getAttribute("aria-expanded") !== "true") return;
      if (nav.contains(e.target) || btn.contains(e.target)) return;
      btn.click();
    });
  }

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    mountProgress();
    headerShadow();
    reveals();
    enhanceMenu();
    dismissMenu();
  });
})();
