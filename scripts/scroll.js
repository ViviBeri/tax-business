import { gsap } from "https://cdn.jsdelivr.net/npm/gsap@3.12.5/+esm";
import { ScrollTrigger } from "https://cdn.jsdelivr.net/npm/gsap@3.12.5/ScrollTrigger/+esm";

function initScrollMotion() {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  gsap.registerPlugin(ScrollTrigger);
  const counters = gsap.utils.toArray("#why-kvb .stat-counter[data-target]");
  const steps = gsap.utils.toArray("#compliance-timeline [data-timeline-step]");
  if (!counters.length && !steps.length) return;

  ScrollTrigger.matchMedia({
    "(min-width: 761px)": () => {
      counters.forEach((counter) => {
        const target = Number(counter.dataset.target);
        if (!Number.isFinite(target)) return;
        const state = { value: 0 };
        gsap.set(counter, { textContent: "0" });
        gsap.to(state, {
          value: target,
          duration: 1.25,
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
          y: 24,
          autoAlpha: 0,
          duration: .65,
          stagger: .14,
          ease: "power2.out",
          scrollTrigger: {
            trigger: "#compliance-timeline .timeline-steps",
            start: "top 82%",
            once: true
          }
        });
      }
    },
    "(max-width: 760px)": () => {
      counters.forEach((counter) => {
        const target = Number(counter.dataset.target);
        if (!Number.isFinite(target)) return;
        const state = { value: 0 };
        gsap.set(counter, { textContent: "0" });
        gsap.to(state, {
          value: target,
          duration: .9,
          ease: "power2.out",
          snap: { value: 1 },
          scrollTrigger: {
            trigger: counter.closest("#why-kvb"),
            start: "top 88%",
            once: true
          },
          onUpdate: () => { counter.textContent = String(Math.round(state.value)); }
        });
      });
      if (steps.length) {
        gsap.from(steps, {
          y: 14,
          autoAlpha: 0,
          duration: .5,
          stagger: .1,
          ease: "power2.out",
          scrollTrigger: {
            trigger: "#compliance-timeline .timeline-steps",
            start: "top 90%",
            once: true
          }
        });
      }
    }
  });
}

initScrollMotion();
