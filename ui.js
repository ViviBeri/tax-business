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


  function serviceBentoGrid() {
    var wrap = document.querySelector(".tiles-carousel");
    var track = document.getElementById("serviceTiles");
    if (!wrap || !track || track.dataset.bentoReady === "true") return;

    var cards = Array.prototype.slice.call(track.querySelectorAll(":scope > .tile"));
    if (!cards.length) return;

    track.dataset.bentoReady = "true";
    wrap.classList.remove("is-liquid-coverflow");
    wrap.classList.add("is-3d-bento");
    track.removeAttribute("tabindex");
    track.setAttribute("aria-label", "KVB services");
    var nav = wrap.querySelector(".liquid-pagination");
    if (nav) nav.remove();
    var filter = wrap.querySelector(".liquid-filter-defs");
    if (filter) filter.remove();
    var arrows = wrap.querySelectorAll(".tiles-arrow");
    arrows.forEach(function (arrow) { arrow.hidden = true; });

    var reduceMotion = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    cards.forEach(function (card, index) {
      card.classList.add("bento-card");
      card.style.removeProperty("pointer-events");
      card.removeAttribute("aria-current");
      card.removeAttribute("tabindex");
      card.style.setProperty("--bento-order", index);
      card.addEventListener("pointermove", function (event) {
        if (reduceMotion || event.pointerType === "touch") return;
        var rect = card.getBoundingClientRect();
        var x = (event.clientX - rect.left) / rect.width;
        var y = (event.clientY - rect.top) / rect.height;
        card.style.setProperty("--bento-tilt-x", ((.5-y)*8).toFixed(2)+"deg");
        card.style.setProperty("--bento-tilt-y", ((x-.5)*9).toFixed(2)+"deg");
        card.style.setProperty("--bento-glow-x", (x*100).toFixed(1)+"%");
        card.style.setProperty("--bento-glow-y", (y*100).toFixed(1)+"%");
      });
      card.addEventListener("pointerleave", function () {
        card.style.setProperty("--bento-tilt-x","0deg");
        card.style.setProperty("--bento-tilt-y","0deg");
        card.style.setProperty("--bento-glow-x","50%");
        card.style.setProperty("--bento-glow-y","50%");
      });
      card.addEventListener("focus", function () { card.classList.add("is-focused"); });
      card.addEventListener("blur", function () { card.classList.remove("is-focused"); });
    });
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
    serviceBentoGrid();
    venomButton();
  });
})();
