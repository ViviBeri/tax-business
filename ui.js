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
    if (!wrap || !track || track.dataset.loopReady === "true") return;
    var originals = Array.prototype.slice.call(track.querySelectorAll(".tile"));
    var prev = wrap.querySelector(".tiles-prev");
    var next = wrap.querySelector(".tiles-next");
    if (!originals.length) return;

    wrap.classList.remove("is-circular");
    wrap.classList.add("is-horizontal-loop");
    wrap.setAttribute("aria-label", "Manually swipe or scroll through services. The list repeats continuously.");
    track.setAttribute("aria-label", "KVB services, repeating horizontal carousel");
    track.dataset.loopReady = "true";

    function appendCloneSet() {
      originals.forEach(function (card) {
        var clone = card.cloneNode(true);
        clone.setAttribute("aria-hidden", "true");
        clone.setAttribute("tabindex", "-1");
        clone.querySelectorAll("a,button,[tabindex]").forEach(function (el) { el.setAttribute("tabindex", "-1"); });
        track.appendChild(clone);
      });
    }
    appendCloneSet();
    appendCloneSet();

    var groupWidth = 0;
    var wrapping = false;

    function measure() {
      var first = track.children[0];
      var firstClone = track.children[originals.length];
      if (!first || !firstClone) return;
      groupWidth = firstClone.offsetLeft - first.offsetLeft;
      if (groupWidth > 0 && track.scrollLeft < groupWidth) {
        track.scrollLeft += groupWidth;
      }
    }

    track.addEventListener("scroll", function () {
      if (wrapping || !groupWidth) return;
      var position = track.scrollLeft;
      /* Keep the user inside the middle copy. Wrap before either edge
         becomes visible, so touch momentum never reaches the track ends. */
      var lowerBoundary = groupWidth * 0.5;
      var upperBoundary = groupWidth * 1.5;
      if (position > upperBoundary) {
        wrapping = true;
        track.scrollLeft = position - groupWidth;
        requestAnimationFrame(function () { wrapping = false; });
      } else if (position < lowerBoundary) {
        wrapping = true;
        track.scrollLeft = position + groupWidth;
        requestAnimationFrame(function () { wrapping = false; });
      }
    }, { passive: true });

    function move(direction) {
      var card = track.querySelector(".tile");
      var gap = parseFloat(window.getComputedStyle(track).columnGap || window.getComputedStyle(track).gap) || 16;
      var distance = card ? card.getBoundingClientRect().width + gap : track.clientWidth * 0.8;
      track.scrollBy({ left: direction * distance, behavior: "smooth" });
    }
    if (prev) prev.addEventListener("click", function () { move(-1); });
    if (next) next.addEventListener("click", function () { move(1); });

    window.addEventListener("resize", measure);
    requestAnimationFrame(function () {
      measure();
      track.scrollLeft = groupWidth;
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
    serviceCarousel();
  });
})();
