(() => {
  "use strict";

  const wrapper = document.querySelector(".tiles-carousel");
  const track = document.querySelector("#serviceTiles");
  if (!wrapper || !track) return;

  const breakpoint = window.matchMedia("(max-width: 960px)");
  const lang = document.documentElement.lang.toLowerCase();
  const tamil = lang.startsWith("ta");
  const labels = tamil
    ? { region: "சேவை ஸ்லைடுகள்", previous: "முந்தைய சேவை", next: "அடுத்த சேவை", slide: (n, total) => `சேவை ${n} / ${total}` }
    : { region: "Service carousel", previous: "Previous service", next: "Next service", slide: (n, total) => `Slide ${n} of ${total}` };

  let active = false;
  let controls;
  let live;
  let previous;
  let next;
  let pointerId = null;
  let startX = 0;
  let startScroll = 0;
  let dragged = false;
  let suppressClick = false;
  let savedTabindex = null;

  const slides = () => Array.from(track.querySelectorAll(":scope > .tile"));
  const currentIndex = () => {
    const items = slides();
    if (!items.length) return 0;
    const x = track.scrollLeft;
    let best = 0;
    let distance = Infinity;
    items.forEach((item, index) => {
      const delta = Math.abs(item.offsetLeft - track.offsetLeft - x);
      if (delta < distance) { distance = delta; best = index; }
    });
    return best;
  };
  const announce = () => {
    if (!live) return;
    live.textContent = labels.slide(currentIndex() + 1, slides().length);
  };
  const goTo = (index) => {
    const items = slides();
    if (!items.length) return;
    const bounded = Math.max(0, Math.min(items.length - 1, index));
    track.scrollTo({ left: items[bounded].offsetLeft - track.offsetLeft, behavior: "smooth" });
    window.setTimeout(announce, 220);
  };
  const onScroll = () => {
    if (onScroll.frame) cancelAnimationFrame(onScroll.frame);
    onScroll.frame = requestAnimationFrame(announce);
  };
  const onPrevious = () => goTo(currentIndex() - 1);
  const onNext = () => goTo(currentIndex() + 1);
  const onKeyDown = (event) => {
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    if (event.key === "ArrowRight") { event.preventDefault(); goTo(currentIndex() + 1); }
    if (event.key === "ArrowLeft") { event.preventDefault(); goTo(currentIndex() - 1); }
  };
  const onPointerDown = (event) => {
    if (event.pointerType === "mouse" && event.button !== 0) return;
    pointerId = event.pointerId;
    startX = event.clientX;
    startScroll = track.scrollLeft;
    dragged = false;
    track.setPointerCapture?.(pointerId);
  };
  const onPointerMove = (event) => {
    if (pointerId === null || event.pointerId !== pointerId) return;
    const delta = event.clientX - startX;
    if (Math.abs(delta) > 5) dragged = true;
    if (dragged) {
      track.scrollLeft = startScroll - delta;
      event.preventDefault();
    }
  };
  const finishPointer = (event) => {
    if (pointerId === null || (event && event.pointerId !== pointerId)) return;
    if (dragged) {
      suppressClick = true;
      window.setTimeout(() => { suppressClick = false; }, 0);
    }
    pointerId = null;
  };
  const onClickCapture = (event) => {
    if (!suppressClick) return;
    event.preventDefault();
    event.stopPropagation();
  };

  function activate() {
    if (active || !slides().length) return;
    active = true;
    savedTabindex = track.getAttribute("tabindex");
    track.setAttribute("tabindex", "0");
    track.setAttribute("aria-label", labels.region);
    track.style.display = "flex";
    track.style.overflowX = "auto";
    track.style.scrollSnapType = "x mandatory";
    track.style.scrollBehavior = "smooth";
    track.style.gap = "1rem";
    slides().forEach((slide) => {
      slide.style.flex = "0 0 min(84%, 340px)";
      slide.style.scrollSnapAlign = "start";
    });

    controls = document.createElement("div");
    controls.className = "tiles-carousel-controls";
    previous = document.createElement("button");
    next = document.createElement("button");
    previous.type = next.type = "button";
    previous.className = "carousel-control carousel-control--previous";
    next.className = "carousel-control carousel-control--next";
    previous.setAttribute("aria-label", labels.previous);
    next.setAttribute("aria-label", labels.next);
    previous.textContent = tamil ? "முந்தைய" : "Previous";
    next.textContent = tamil ? "அடுத்து" : "Next";
    controls.append(previous, next);
    wrapper.append(controls);

    live = document.createElement("span");
    live.className = "carousel-live";
    live.setAttribute("aria-live", "polite");
    live.setAttribute("aria-atomic", "true");
    live.style.cssText = "position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0";
    wrapper.append(live);

    previous.addEventListener("click", onPrevious);
    next.addEventListener("click", onNext);
    track.addEventListener("keydown", onKeyDown);
    track.addEventListener("scroll", onScroll, { passive: true });
    track.addEventListener("pointerdown", onPointerDown);
    track.addEventListener("pointermove", onPointerMove, { passive: false });
    track.addEventListener("pointerup", finishPointer);
    track.addEventListener("pointercancel", finishPointer);
    track.addEventListener("lostpointercapture", finishPointer);
    track.addEventListener("click", onClickCapture, true);
    announce();
  }

  function deactivate() {
    if (!active) return;
    active = false;
    previous.removeEventListener("click", onPrevious);
    next.removeEventListener("click", onNext);
    track.removeEventListener("keydown", onKeyDown);
    track.removeEventListener("scroll", onScroll);
    track.removeEventListener("pointerdown", onPointerDown);
    track.removeEventListener("pointermove", onPointerMove);
    track.removeEventListener("pointerup", finishPointer);
    track.removeEventListener("pointercancel", finishPointer);
    track.removeEventListener("lostpointercapture", finishPointer);
    track.removeEventListener("click", onClickCapture, true);
    if (onScroll.frame) cancelAnimationFrame(onScroll.frame);
    if (controls) controls.remove();
    if (live) live.remove();
    track.style.display = "";
    track.style.overflowX = "";
    track.style.scrollSnapType = "";
    track.style.scrollBehavior = "";
    track.style.gap = "";
    slides().forEach((slide) => {
      slide.style.flex = "";
      slide.style.scrollSnapAlign = "";
    });
    if (savedTabindex === null) track.removeAttribute("tabindex");
    else track.setAttribute("tabindex", savedTabindex);
    track.removeAttribute("aria-label");
    track.scrollLeft = 0;
    pointerId = null;
  }

  const onBreakpoint = () => breakpoint.matches ? activate() : deactivate();
  onBreakpoint();
  breakpoint.addEventListener?.("change", onBreakpoint);
  window.addEventListener("pagehide", () => {
    breakpoint.removeEventListener?.("change", onBreakpoint);
    deactivate();
  }, { once: true });
})();
