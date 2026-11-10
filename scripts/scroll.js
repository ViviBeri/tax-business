const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const revealTargets = [...document.querySelectorAll(".tile, .step, .proof-chip, [data-reveal]")];
if (reduced) {
  revealTargets.forEach(el => { el.style.opacity = "1"; el.style.transform = "none"; });
} else {
  const gsapModule = await import("https://cdn.jsdelivr.net/npm/gsap@3/+esm").catch(() => null);
  const stModule = await import("https://cdn.jsdelivr.net/npm/gsap@3/ScrollTrigger/+esm").catch(() => null);
  const gsap = gsapModule?.gsap || gsapModule?.default;
  const ScrollTrigger = stModule?.ScrollTrigger;
  if (gsap && ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);
    const mm = gsap.matchMedia();
    mm.add("(min-width: 0px)", () => {
      gsap.fromTo(".tile", {autoAlpha:0,y:12}, {autoAlpha:1,y:0,duration:.45,stagger:.06,ease:"power2.out",scrollTrigger:{trigger:"#services",start:"top 82%",once:true}});
      gsap.fromTo(".proof-chip", {autoAlpha:0,y:8,scale:.98}, {autoAlpha:1,y:0,scale:1,duration:.35,stagger:.07,ease:"back.out(1.3)",scrollTrigger:{trigger:".proof-strip",start:"top 85%",once:true}});
      document.querySelectorAll("[data-count]").forEach(node => {
        const target = Number(node.dataset.count);
        if (!Number.isFinite(target)) return;
        const proxy = {value:0};
        gsap.to(proxy,{value:target,duration:1.2,ease:"power1.out",scrollTrigger:{trigger:node,start:"top 90%",once:true},onUpdate:()=>{node.textContent=Math.round(proxy.value).toLocaleString();}});
      });
      const timeline = document.querySelector("[data-compliance-timeline]");
      if (timeline) {
        const steps = [...timeline.querySelectorAll("[data-timeline-step]")];
        mm.add("(min-width: 960px)", () => {
          ScrollTrigger.create({trigger:timeline,start:"top top+=90",end:()=>"+="+Math.max(steps.length*260,700),pin:true,scrub:true,
            onUpdate:self=>{const active=Math.min(steps.length-1,Math.floor(self.progress*steps.length));steps.forEach((step,i)=>step.classList.toggle("is-active",i===active));}});
        });
      }
    });
    window.addEventListener("pagehide",()=>{mm.revert();},{once:true});
  } else {
    revealTargets.forEach(el => { el.style.opacity="1"; el.style.transform="none"; });
  }
}
