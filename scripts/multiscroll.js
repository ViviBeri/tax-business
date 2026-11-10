import { gsap } from "https://cdn.jsdelivr.net/npm/gsap@3.12.5/+esm";
import { ScrollTrigger } from "https://cdn.jsdelivr.net/npm/gsap@3.12.5/ScrollTrigger/+esm";

const motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
const desktopQuery = window.matchMedia("(min-width: 961px)");

function initWhySplit() {
  const section = document.querySelector("#why-kvb");
  const heading = section?.querySelector(".section-head");
  const cards = section?.querySelector(".glass-grid");
  if (!section || !heading || !cards || motionQuery.matches || !desktopQuery.matches) return;

  gsap.registerPlugin(ScrollTrigger);
  const context = gsap.context(() => {
    gsap.fromTo(heading,{y:0},{y:-54,ease:"none",scrollTrigger:{
      trigger:section,start:"top bottom",end:"bottom top",scrub:.7,invalidateOnRefresh:true
    }});
    gsap.fromTo(cards,{y:0},{y:54,ease:"none",scrollTrigger:{
      trigger:section,start:"top bottom",end:"bottom top",scrub:.7,invalidateOnRefresh:true
    }});
  },section);

  const teardown = () => context.revert();
  desktopQuery.addEventListener("change",() => { if (!desktopQuery.matches) teardown(); },{once:true});
  motionQuery.addEventListener("change",() => { if (motionQuery.matches) teardown(); },{once:true});
}
initWhySplit();
