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
      ".hero-card, .clients-grid > *, .proof-grid > div, .section-head, .tile[data-service], .step, .locations a, .tool-grid > div, .faq-list details, .about-points > div, .newbiz, .contact-box"
    );
    if (!targets.length) return;
    targets.forEach(function (el, index) { el.classList.add("kvb-reveal"); el.style.setProperty("--kvb-reveal-delay", Math.min(index % 4, 3) * 65 + "ms"); });
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
    if (!wrap || !track || track.dataset.liquidReady === "true") return;

    var cards = Array.prototype.slice.call(track.querySelectorAll(":scope > .tile"));
    var prev = wrap.querySelector(".tiles-prev");
    var next = wrap.querySelector(".tiles-next");
    if (!cards.length) return;

    track.dataset.liquidReady = "true";
    wrap.classList.add("is-liquid-coverflow");
    track.setAttribute("tabindex", "0");
    track.setAttribute("aria-label", "KVB services. Use arrow keys, swipe or drag to browse.");

    var nav = document.createElement("div");
    nav.className = "liquid-pagination";
    nav.setAttribute("role", "group");
    nav.setAttribute("aria-label", "Choose a service");
    var dots = cards.map(function (card, index) {
      var dot = document.createElement("button");
      dot.type = "button";
      dot.className = "liquid-dot";
      dot.setAttribute("aria-label", "Show " + (card.dataset.service || "service " + (index + 1)));
      dot.addEventListener("click", function () { setActive(index); });
      nav.appendChild(dot);
      return dot;
    });
    wrap.insertBefore(nav, next || null);

    var filterSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    filterSvg.setAttribute("class", "liquid-filter-defs");
    filterSvg.setAttribute("aria-hidden", "true");
    filterSvg.innerHTML = '<defs><filter id="kvb-liquid-goo"><feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur"/><feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 18 -7" result="goo"/><feComposite in="SourceGraphic" in2="goo" operator="atop"/></filter></defs>';
    wrap.appendChild(filterSvg);

    var active = Math.min(Math.max(cards.findIndex(function (card) {
      return card.classList.contains("is-active");
    }), 0), cards.length - 1);
    var pointerStart = 0;
    var pointerDelta = 0;
    var dragging = false;
    var suppressClick = false;
    var wheelLocked = false;
    var reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function animateHeading(card) {
      var heading = card.querySelector("b");
      if (!heading || heading.dataset.letterMotion === "true") return;
      var label = heading.textContent.trim();
      heading.dataset.letterMotion = "true";
      heading.setAttribute("aria-label", label);
      heading.textContent = "";
      Array.from(label).forEach(function (letter, index) {
        var span = document.createElement("span");
        span.className = "liquid-letter";
        span.style.setProperty("--letter-index", index);
        span.textContent = letter === " " ? "\u00a0" : letter;
        heading.appendChild(span);
      });
    }

    function render() {
      var width = Math.min(track.clientWidth * 0.58, 250);
      var step = Math.max(width + 28, Math.min(track.clientWidth * 0.62, 290));
      cards.forEach(function (card, index) {
        var offset = index - active;
        if (offset > cards.length / 2) offset -= cards.length;
        if (offset < -cards.length / 2) offset += cards.length;
        var distance = Math.abs(offset);
        var x = offset * step;
        var scale = Math.max(0.72, 1 - distance * 0.105);
        var z = distance === 0 ? 70 : -distance * 95;
        var rotate = offset * -27;
        var opacity = distance > 2 ? 0 : Math.max(0.35, 1 - distance * 0.24);

        card.style.setProperty("--liquid-x", x + "px");
        card.style.setProperty("--liquid-z", z + "px");
        card.style.setProperty("--liquid-rotate", rotate + "deg");
        card.style.setProperty("--liquid-scale", scale);
        card.style.setProperty("--liquid-opacity", opacity);
        card.style.zIndex = String(20 - distance);
        card.classList.toggle("is-active", index === active);
        card.setAttribute("aria-current", index === active ? "true" : "false");
        card.tabIndex = index === active ? 0 : -1;
        card.style.pointerEvents = distance <= 1 ? "auto" : "none";
      });
      dots.forEach(function (dot, index) {
        var selected = index === active;
        dot.classList.toggle("is-active", selected);
        dot.setAttribute("aria-pressed", String(selected));
      });
      animateHeading(cards[active]);
      if (prev) prev.disabled = false;
      if (next) next.disabled = false;
    }

    function setActive(index) {
      active = (index + cards.length) % cards.length;
      render();
    }
    function move(direction) { setActive(active + direction); }

    if (prev) prev.addEventListener("click", function () { move(-1); });
    if (next) next.addEventListener("click", function () { move(1); });

    track.addEventListener("pointerdown", function (event) {
      if (event.target.closest("a") && event.target.closest("a") !== cards[active]) return;
      dragging = true;
      pointerStart = event.clientX;
      pointerDelta = 0;
      suppressClick = false;
      track.classList.add("is-dragging");
      if (track.setPointerCapture) track.setPointerCapture(event.pointerId);
    });
    track.addEventListener("pointermove", function (event) {
      if (!dragging) return;
      pointerDelta = event.clientX - pointerStart;
      if (Math.abs(pointerDelta) > 8) suppressClick = true;
    });
    function finishDrag() {
      if (!dragging) return;
      dragging = false;
      track.classList.remove("is-dragging");
      if (pointerDelta > 42) move(-1);
      else if (pointerDelta < -42) move(1);
      if (suppressClick) window.setTimeout(function () { suppressClick = false; }, 80);
      pointerDelta = 0;
    }
    track.addEventListener("pointerup", finishDrag);
    track.addEventListener("pointercancel", finishDrag);
    track.addEventListener("lostpointercapture", finishDrag);
    track.addEventListener("click", function (event) {
      if (suppressClick) {
        event.preventDefault();
        event.stopPropagation();
        return;
      }
      var card = event.target.closest(".tile");
      if (!card) return;
      var index = cards.indexOf(card);
      if (index >= 0 && index !== active) {
        event.preventDefault();
        setActive(index);
      }
    }, true);

    track.addEventListener("keydown", function (event) {
      if (event.key === "ArrowRight") { event.preventDefault(); move(1); }
      if (event.key === "ArrowLeft") { event.preventDefault(); move(-1); }
      if (event.key === "Home") { event.preventDefault(); setActive(0); }
      if (event.key === "End") { event.preventDefault(); setActive(cards.length - 1); }
    });
    track.addEventListener("wheel", function (event) {
      if (Math.abs(event.deltaX) < Math.abs(event.deltaY) || wheelLocked) return;
      wheelLocked = true;
      move(event.deltaX > 0 ? 1 : -1);
      window.setTimeout(function () { wheelLocked = false; }, 550);
    }, { passive: true });

    if (!reducedMotion) {
      cards.forEach(function (card) {
        card.addEventListener("pointermove", function (event) {
          if (card !== cards[active] || dragging) return;
          var rect = card.getBoundingClientRect();
          var px = (event.clientX - rect.left) / rect.width - 0.5;
          var py = (event.clientY - rect.top) / rect.height - 0.5;
          card.style.setProperty("--liquid-tilt-x", (py * -3) + "deg");
          card.style.setProperty("--liquid-tilt-y", (px * 4) + "deg");
        });
        card.addEventListener("pointerleave", function () {
          card.style.setProperty("--liquid-tilt-x", "0deg");
          card.style.setProperty("--liquid-tilt-y", "0deg");
        });
      });
    }
    window.addEventListener("resize", render, { passive: true });
    render();
  }


  function venomButton() {
    var button = document.querySelector(".venom-cta");
    if (!button || button.dataset.venomReady === "true") return;
    button.dataset.venomReady = "true";
    if (!window.matchMedia || window.matchMedia("(pointer: fine)").matches === false) return;

    var svgNS = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("class", "kvb-venom-layer");
    svg.setAttribute("aria-hidden", "true");
    svg.innerHTML = '<defs><filter id="kvb-venom-goo"><feGaussianBlur in="SourceGraphic" stdDeviation="6" result="blur"/><feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 20 -8" result="goo"/><feComposite in="SourceGraphic" in2="goo" operator="atop"/></filter></defs><g filter="url(#kvb-venom-goo)"><path class="kvb-venom-strand"/><circle class="kvb-venom-anchor" r="10"/><circle class="kvb-venom-tip" r="7"/></g>';
    document.body.appendChild(svg);

    var path = svg.querySelector(".kvb-venom-strand");
    var anchor = svg.querySelector(".kvb-venom-anchor");
    var tip = svg.querySelector(".kvb-venom-tip");
    var point = {x:-1000,y:-1000};
    var smooth = {x:-1000,y:-1000};
    var active = false;
    var raf = 0;
    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    var cursor = document.createElement("span");
    cursor.className = "kvb-venom-cursor";
    cursor.setAttribute("aria-hidden","true");
    cursor.innerHTML = '<svg viewBox="0 0 24 24" width="21" height="21"><path d="M5 3.5 19 13l-6.2 1.2-3.1 5.3L5 3.5Z" fill="#fff" stroke="#16834b" stroke-width="1.4" stroke-linejoin="round"/></svg>';
    document.body.appendChild(cursor);

    function center() {
      var r = button.getBoundingClientRect();
      return {x:r.left+r.width/2,y:r.top+r.height/2};
    }
    function draw() {
      raf = 0;
      var c = center();
      var dx = point.x-c.x, dy = point.y-c.y;
      var d = Math.hypot(dx,dy);
      var near = active && d < 175;
      var pull = near ? Math.pow(1-d/175,2) : 0;
      var max = 13;
      button.style.setProperty("--venom-x", (dx/Math.max(d,1)*max*pull).toFixed(2)+"px");
      button.style.setProperty("--venom-y", (dy/Math.max(d,1)*max*pull).toFixed(2)+"px");

      smooth.x = reduceMotion ? point.x : smooth.x+(point.x-smooth.x)*.38;
      smooth.y = reduceMotion ? point.y : smooth.y+(point.y-smooth.y)*.38;
      cursor.style.transform = "translate3d("+(smooth.x-9)+"px,"+(smooth.y-9)+"px,0)";
      cursor.classList.toggle("is-visible", near);
      cursor.classList.toggle("is-near", near);

      var connected = near && d > 30 && d < 145;
      path.style.opacity = connected ? String(Math.max(.08,1-d/155)) : "0";
      anchor.style.opacity = connected ? "1" : "0";
      tip.style.opacity = connected ? "1" : "0";
      if (connected) {
        var nx = -dy/d, ny = dx/d;
        var w = Math.max(1.2,8*(1-d/155));
        var a1={x:c.x+nx*w,y:c.y+ny*w}, a2={x:c.x-nx*w,y:c.y-ny*w};
        var b1={x:point.x+nx*4,y:point.y+ny*4}, b2={x:point.x-nx*4,y:point.y-ny*4};
        var bend=Math.min(34,d*.22);
        var cx=(c.x+point.x)/2+nx*bend, cy=(c.y+point.y)/2+ny*bend;
        var ex=(c.x+point.x)/2-nx*bend, ey=(c.y+point.y)/2-ny*bend;
        path.setAttribute("d","M"+a1.x+" "+a1.y+" Q"+cx+" "+cy+" "+b1.x+" "+b1.y+" Q"+ex+" "+ey+" "+a2.x+" "+a2.y+" Z");
        anchor.setAttribute("cx",c.x); anchor.setAttribute("cy",c.y);
        tip.setAttribute("cx",point.x); tip.setAttribute("cy",point.y);
      }
      if (active || near) raf=requestAnimationFrame(draw);
      else {
        button.style.setProperty("--venom-x","0px");
        button.style.setProperty("--venom-y","0px");
      }
    }
    function schedule(){ if(!raf) raf=requestAnimationFrame(draw); }
    window.addEventListener("pointermove",function(e){
      point.x=e.clientX; point.y=e.clientY;
      var r=button.getBoundingClientRect();
      var pad=190;
      active=point.x>=r.left-pad && point.x<=r.right+pad && point.y>=r.top-pad && point.y<=r.bottom+pad;
      schedule();
    },{passive:true});
    window.addEventListener("pointerout",function(e){
      if(!e.relatedTarget){active=false;point.x=-1000;point.y=-1000;schedule();}
    });
    button.addEventListener("pointerdown",function(){cursor.classList.add("is-pressed");});
    window.addEventListener("pointerup",function(){cursor.classList.remove("is-pressed");});
    button.addEventListener("pointerleave",function(){
      button.style.setProperty("--venom-x","0px");
      button.style.setProperty("--venom-y","0px");
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
    venomButton();
  });
})();
