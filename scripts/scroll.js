import { gsap } from "https://cdn.jsdelivr.net/npm/gsap@3.12.5/+esm";
import { ScrollTrigger } from "https://cdn.jsdelivr.net/npm/gsap@3.12.5/ScrollTrigger/+esm";

if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  // Keep the server-rendered values and layout untouched.
} else {
  gsap.registerPlugin(ScrollTrigger);

  const counters = gsap.utils.toArray("#why-kvb .stat-counter[data-target]");
  const steps = gsap.utils.toArray("#compliance-timeline [data-timeline-step]");

  counters.forEach((counter) => {
    const target = Number(counter.dataset.target);
    if (!Number.isFinite(target) || target < 0) return;
    const state = { value: 0 };
    gsap.to(state, {
      value: target,
      duration: 1.15,
      ease: "power2.out",
      snap: { value: 1 },
      scrollTrigger: {
        trigger: counter.closest("#why-kvb"),
        start: "top 82%",
        once: true
      },
      onUpdate: () => { counter.textContent = String(Math.round(state.value)); }
    });
  });

  if (steps.length) {
    gsap.from(steps, {
      y: 22,
      autoAlpha: 0,
      duration: .6,
      stagger: .12,
      ease: "power2.out",
      scrollTrigger: {
        trigger: "#compliance-timeline .timeline-steps",
        start: "top 84%",
        once: true
      }
    });
  }
}
