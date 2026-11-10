import { gsap } from "https://cdn.jsdelivr.net/npm/gsap@3.12.5/+esm";
import { ScrollTrigger } from "https://cdn.jsdelivr.net/npm/gsap@3.12.5/ScrollTrigger/+esm";

function initWhySplit() {
  const section = document.querySelector("#why-kvb");
  const heading = section?.querySelector(".section-head");
  const cards = section?.querySelector(".glass-grid");
  if (!section || !heading || !cards) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (window.innerWidth <= 960) return;

  gsap.registerPlugin(ScrollTrigger);
  ScrollTrigger.matchMedia({
    "(min-width: 961px) and (prefers-reduced-motion: no-preference)": () => {
      const context = gsap.context(() => {
        gsap.fromTo(heading, { y: 0 }, {
          y: -72,
          ease: "none",
          scrollTrigger: {
            trigger: section,
            start: "top bottom",
            end: "bottom top",
            scrub: .8,
            invalidateOnRefresh: true
          }
        });
        gsap.fromTo(cards, { y: 0 }, {
          y: 72,
          ease: "none",
          scrollTrigger: {
            trigger: section,
            start: "top bottom",
            end: "bottom top",
            scrub: .8,
            invalidateOnRefresh: true
          }
        });
      }, section);
      return () => context.revert();
    },
    "(max-width: 960px), (prefers-reduced-motion: reduce)": () => {
      gsap.set([heading, cards], { clearProps: "transform" });
    }
  });
}

initWhySplit();
