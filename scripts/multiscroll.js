const media = window.matchMedia("(prefers-reduced-motion: reduce)");
const section = document.querySelector("[data-split-scroll]");
if (section && !media.matches && window.innerWidth >= 960) {
  const left = section.querySelector("[data-split-left]");
  const right = section.querySelector("[data-split-right]");
  if (left && right) {
    const boot = async () => {
      const mod = await import("https://cdn.jsdelivr.net/npm/gsap@3/+esm").catch(()=>null);
      const st = await import("https://cdn.jsdelivr.net/npm/gsap@3/ScrollTrigger/+esm").catch(()=>null);
      const gsap = mod?.gsap || mod?.default, ScrollTrigger = st?.ScrollTrigger;
      if (!gsap || !ScrollTrigger || media.matches || innerWidth < 960) return;
      gsap.registerPlugin(ScrollTrigger);
      const mm=gsap.matchMedia();
      mm.add("(min-width: 960px) and (prefers-reduced-motion: no-preference)",()=>{
        const distance=Math.max(left.scrollHeight,right.scrollHeight)-section.clientHeight;
        const a=gsap.to(left,{y:()=>-Math.max(0,distance),ease:"none",scrollTrigger:{trigger:section,start:"top top",end:()=>"+="+Math.max(500,distance),scrub:true}});
        const b=gsap.fromTo(right,{y:()=>-Math.max(0,distance)},{y:0,ease:"none",scrollTrigger:{trigger:section,start:"top top",end:()=>"+="+Math.max(500,distance),scrub:true}});
        return ()=>{a.scrollTrigger?.kill();b.scrollTrigger?.kill();a.kill();b.kill();};
      });
      window.addEventListener("pagehide",()=>mm.revert(),{once:true});
    };
    boot();
  }
}
