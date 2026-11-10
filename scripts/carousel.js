(() => {
  "use strict";

  const wrapper = document.querySelector(".tiles-carousel");
  const track = document.querySelector("#serviceTiles");
  if (!wrapper || !track) return;

  const breakpoint = window.matchMedia("(max-width: 960px)");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const tamil = document.documentElement.lang.toLowerCase().startsWith("ta");
  const words = tamil
    ? { region:"சேவை ஸ்லைடுகள்", previous:"முந்தைய சேவை", next:"அடுத்த சேவை", slide:(n,total)=>"சேவை "+n+" / "+total }
    : { region:"Service carousel", previous:"Previous service", next:"Next service", slide:(n,total)=>"Slide "+n+" of "+total };

  const slides = () => Array.from(track.querySelectorAll(":scope > .tile"));
  let active = false, controls, live, previous, next;
  let pointerId = null, startX = 0, startScroll = 0, dragged = false, suppressClick = false;
  let original = null, scrollFrame = 0, announceTimer = 0;

  function indexNow() {
    const items = slides();
    if (!items.length) return 0;
    const left = track.getBoundingClientRect().left;
    let best = 0, distance = Infinity;
    items.forEach((item, i) => {
      const d = Math.abs(item.getBoundingClientRect().left - left);
      if (d < distance) { distance = d; best = i; }
    });
    return best;
  }
  function announce() {
    if (live) live.textContent = words.slide(indexNow() + 1, slides().length);
    if (previous) previous.disabled = indexNow() === 0;
    if (next) next.disabled = indexNow() >= slides().length - 1;
  }
  function goTo(i) {
    const items = slides();
    if (!items.length) return;
    const target = Math.max(0, Math.min(items.length - 1, i));
    track.scrollTo({ left: items[target].offsetLeft - items[0].offsetLeft, behavior: reducedMotion.matches ? "auto" : "smooth" });
    window.clearTimeout(announceTimer);
    announceTimer = window.setTimeout(announce, reducedMotion.matches ? 0 : 260);
  }
  function onScroll() {
    if (scrollFrame) cancelAnimationFrame(scrollFrame);
    scrollFrame = requestAnimationFrame(announce);
  }
  function onKeyDown(event) {
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    if (event.key === "ArrowRight") { event.preventDefault(); goTo(indexNow() + 1); }
    if (event.key === "ArrowLeft") { event.preventDefault(); goTo(indexNow() - 1); }
  }
  function onPointerDown(event) {
    if (event.pointerType === "mouse" && event.button !== 0) return;
    pointerId = event.pointerId; startX = event.clientX; startScroll = track.scrollLeft; dragged = false;
  }
  function onPointerMove(event) {
    if (pointerId === null || event.pointerId !== pointerId) return;
    const delta = event.clientX - startX;
    if (Math.abs(delta) > 6) dragged = true;
    if (dragged) { track.scrollLeft = startScroll - delta; event.preventDefault(); }
  }
  function finishPointer(event) {
    if (pointerId === null || (event && event.pointerId !== pointerId)) return;
    if (dragged) {
      suppressClick = true;
      window.setTimeout(() => { suppressClick = false; }, 0);
    }
    pointerId = null;
  }
  function onClickCapture(event) {
    if (!suppressClick) return;
    event.preventDefault(); event.stopPropagation();
  }
  function activate() {
    if (active || !slides().length) return;
    active = true;
    original = {
      tabindex:track.getAttribute("tabindex"), label:track.getAttribute("aria-label"),
      display:track.style.display, overflow:track.style.overflowX, scrollSnapType:track.style.scrollSnapType,
      behavior:track.style.scrollBehavior, gap:track.style.gap, touch:track.style.touchAction,
      slide:slides().map(el => ({ flex:el.style.flex, snap:el.style.scrollSnapAlign }))
    };
    track.setAttribute("tabindex","0");
    track.setAttribute("aria-label",words.region);
    Object.assign(track.style,{display:"flex",overflowX:"auto",scrollSnapType:"x mandatory",scrollBehavior:reducedMotion.matches?"auto":"smooth",gap:"1rem",touchAction:"pan-y"});
    slides().forEach(el => Object.assign(el.style,{flex:"0 0 min(84%, 340px)",scrollSnapAlign:"start"}));

    controls = document.createElement("div");
    controls.className = "tiles-carousel-controls";
    previous = document.createElement("button");
    next = document.createElement("button");
    previous.type = next.type = "button";
    previous.className = "carousel-control carousel-control--previous";
    next.className = "carousel-control carousel-control--next";
    previous.textContent = tamil ? "முந்தைய" : "Previous";
    next.textContent = tamil ? "அடுத்து" : "Next";
    previous.setAttribute("aria-label",words.previous);
    next.setAttribute("aria-label",words.next);
    controls.append(previous,next);
    wrapper.append(controls);

    live = document.createElement("span");
    live.className = "carousel-live";
    live.setAttribute("aria-live","polite");
    live.setAttribute("aria-atomic","true");
    wrapper.append(live);

    previous.addEventListener("click",() => goTo(indexNow()-1));
    next.addEventListener("click",() => goTo(indexNow()+1));
    track.addEventListener("keydown",onKeyDown);
    track.addEventListener("scroll",onScroll,{passive:true});
    track.addEventListener("pointerdown",onPointerDown);
    track.addEventListener("pointermove",onPointerMove,{passive:false});
    track.addEventListener("pointerup",finishPointer);
    track.addEventListener("pointercancel",finishPointer);
    track.addEventListener("click",onClickCapture,true);
    announce();
  }
  function deactivate() {
    if (!active) return;
    active = false;
    track.removeEventListener("keydown",onKeyDown);
    track.removeEventListener("scroll",onScroll);
    track.removeEventListener("pointerdown",onPointerDown);
    track.removeEventListener("pointermove",onPointerMove);
    track.removeEventListener("pointerup",finishPointer);
    track.removeEventListener("pointercancel",finishPointer);
    track.removeEventListener("click",onClickCapture,true);
    if (scrollFrame) cancelAnimationFrame(scrollFrame);
    window.clearTimeout(announceTimer);
    controls?.remove(); live?.remove();
    Object.assign(track.style,{display:original.display,overflowX:original.overflow,scrollSnapType:original.scrollSnapType,scrollBehavior:original.behavior,gap:original.gap,touchAction:original.touch});
    slides().forEach((el,i) => Object.assign(el.style,{flex:original.slide[i]?.flex ?? "",scrollSnapAlign:original.slide[i]?.snap ?? ""}));
    if (original.tabindex === null) track.removeAttribute("tabindex"); else track.setAttribute("tabindex",original.tabindex);
    if (original.label === null) track.removeAttribute("aria-label"); else track.setAttribute("aria-label",original.label);
    track.scrollLeft = 0; pointerId = null; original = null;
  }
  function onBreakpoint() { if (breakpoint.matches) activate(); else deactivate(); }
  onBreakpoint();
  breakpoint.addEventListener("change",onBreakpoint);
  window.addEventListener("pagehide",() => { breakpoint.removeEventListener("change",onBreakpoint); deactivate(); },{once:true});
})();
