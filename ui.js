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
      ".tile[data-service], .step, .locations a, .tool-grid > div, .faq-list details, .about-points > div, .newbiz"
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


  function serviceCarousel() {
    var wrap = document.querySelector(".tiles-carousel");
    var track = document.getElementById("serviceTiles");
    if (!wrap || !track) return;
    var cards = Array.prototype.slice.call(track.querySelectorAll(".tile"));
    var prev = wrap.querySelector(".tiles-prev");
    var next = wrap.querySelector(".tiles-next");
    if (!cards.length) return;

    var rotation = 0;
    var radius = 260;
    var step = 360 / cards.length;
    var lastTime = 0;
    var dragging = false;
    var startX = 0;
    var startRotation = 0;
    var paused = false;
    var reduced = reduce;
    var frame = 0;

    wrap.classList.add("is-circular");
    track.setAttribute("aria-label", "Circular carousel of KVB services");
    track.style.transformStyle = "preserve-3d";

    function layout() {
      var available = Math.min(wrap.clientWidth, window.innerWidth || wrap.clientWidth);\n      var width = Math.min(window.innerWidth <= 640 ? 158 : 230, Math.max(window.innerWidth <= 640 ? 132 : 170, available * (window.innerWidth <= 640 ? 0.40 : 0.23)));
      radius = Math.round((width / 2) / Math.tan(Math.PI / cards.length));
      cards.forEach(function (card, index) {
        card.style.width = width + "px";
        card.style.height = window.innerWidth <= 640 ? "205px" : "200px";
        card.style.left = "50%";
        card.style.top = "50%";
        card.style.transform = "translate(-50%,-50%) rotateY(" + (index * step) + "deg) translateZ(" + radius + "px)";
        card.style.position = "absolute";
        card.style.backfaceVisibility = "hidden";
      });
      track.style.height = (window.innerWidth <= 640 ? "270px" : "280px");
      render();
    }

    function render() {
      track.style.transform = "rotateY(" + rotation + "deg)";
      cards.forEach(function (card, index) {
        var angle = ((index * step + rotation) % 360 + 360) % 360;
        var normalized = angle > 180 ? 360 - angle : angle;
        var depth = Math.cos(normalized * Math.PI / 180);
        card.style.opacity = String(Math.max(0.18, 0.34 + 0.66 * Math.max(0, depth)));
        card.style.zIndex = String(Math.round((depth + 1) * 100));
        card.style.filter = depth < -0.15 ? "brightness(.72)" : "none";
        card.setAttribute("aria-hidden", depth < -0.35 ? "true" : "false");
        card.tabIndex = depth < -0.35 ? -1 : 0;
      });
    }

    function move(direction) {
      rotation -= direction * step;
      render();
    }
    if (prev) prev.addEventListener("click", function () { move(-1); });
    if (next) next.addEventListener("click", function () { move(1); });

    wrap.addEventListener("pointerdown", function (event) {
      if (event.target.closest("button")) return;
      dragging = true;
      paused = true;
      startX = event.clientX;
      startRotation = rotation;
      wrap.classList.add("is-dragging");
      if (wrap.setPointerCapture) wrap.setPointerCapture(event.pointerId);
    });
    wrap.addEventListener("pointermove", function (event) {
      if (!dragging) return;
      rotation = startRotation + (event.clientX - startX) * 0.42;
      render();
    });
    function endDrag() {
      if (!dragging) return;
      dragging = false;
      wrap.classList.remove("is-dragging");
      window.setTimeout(function () { paused = false; }, 900);
    }
    wrap.addEventListener("pointerup", endDrag);
    wrap.addEventListener("pointercancel", endDrag);
    wrap.addEventListener("mouseenter", function () { paused = true; });
    wrap.addEventListener("mouseleave", function () { if (!dragging) paused = false; });
    window.addEventListener("resize", layout);

    function animate(time) {
      if (!lastTime) lastTime = time;
      var delta = Math.min(40, time - lastTime);
      lastTime = time;
      if (!reduced && !paused && !dragging) {
        rotation -= delta * 0.006;
        render();
      }
      frame = window.requestAnimationFrame(animate);
    }
    layout();
    if (!reduced) frame = window.requestAnimationFrame(animate);
    window.addEventListener("pagehide", function () { if (frame) window.cancelAnimationFrame(frame); });
  }

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    mountProgress();
    headerShadow();
    reveals();
    serviceCarousel();
  });
})();
