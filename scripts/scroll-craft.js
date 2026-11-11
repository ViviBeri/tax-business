/* Lightweight Scroll-Craft pass for KVB. */
(() => {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const selector = [
    ".section-head", ".services-grid .tile", "#how .step",
    "#why-kvb .glass-card", ".tool-grid > div", ".about-points > div",
    ".faq-list details", ".contact-box"
  ].join(",");
  const items = Array.from(document.querySelectorAll(selector));

  const progress = document.createElement("div");
  progress.className = "kvb-scroll-progress";
  progress.setAttribute("aria-hidden", "true");
  document.body.append(progress);

  let frame = 0;
  function updateProgress() {
    frame = 0;
    const root = document.documentElement;
    const range = root.scrollHeight - window.innerHeight;
    const value = range > 0 ? Math.min(1, Math.max(0, window.scrollY / range)) : 0;
    progress.style.transform = "scaleX(" + value + ")";
  }
  function requestProgress() {
    if (!frame) frame = window.requestAnimationFrame(updateProgress);
  }
  window.addEventListener("scroll", requestProgress, { passive: true });
  window.addEventListener("resize", requestProgress, { passive: true });
  updateProgress();

  if (reduceMotion.matches || !("IntersectionObserver" in window)) return;

  items.forEach((item, index) => {
    item.classList.add("kvb-reveal");
    if (item.matches(".services-grid .tile, #how .step, #why-kvb .glass-card")) {
      item.style.setProperty("--kvb-reveal-delay", Math.min(index % 4, 3) * 65 + "ms");
    }
  });

  const observer = new IntersectionObserver((entries, activeObserver) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-visible");
      activeObserver.unobserve(entry.target);
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -36px 0px" });

  items.forEach(item => observer.observe(item));
  reduceMotion.addEventListener("change", event => {
    if (!event.matches) return;
    observer.disconnect();
    items.forEach(item => item.classList.add("is-visible"));
  });
  window.addEventListener("pagehide", () => {
    observer.disconnect();
    window.removeEventListener("scroll", requestProgress);
    window.removeEventListener("resize", requestProgress);
    if (frame) window.cancelAnimationFrame(frame);
  }, { once: true });
})();
