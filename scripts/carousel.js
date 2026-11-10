const container=document.querySelector("[data-services-carousel]");
if(container){
 const track=container.querySelector("[data-carousel-track]");
 const slides=track?[...track.children]:[];
 const prev=container.querySelector("[data-carousel-prev]");
 const next=container.querySelector("[data-carousel-next]");
 const live=container.querySelector("[data-carousel-live]");
 const media=matchMedia("(min-width: 961px)");
 if(track&&slides.length){
  let pointer=null,startX=0,startScroll=0;
  const index=()=>Math.max(0,Math.min(slides.length-1,Math.round(track.scrollLeft/(slides[0].getBoundingClientRect().width+parseFloat(getComputedStyle(track).columnGap||0)))));
  const announce=()=>{if(live)live.textContent=`Service ${index()+1} of ${slides.length}`;};
  const go=delta=>{const i=Math.max(0,Math.min(slides.length-1,index()+delta));track.scrollTo({left:slides[i].offsetLeft-track.offsetLeft,behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"});announce();};
  const onDown=e=>{if(media.matches||e.pointerType==="touch")return;pointer=e.pointerId;startX=e.clientX;startScroll=track.scrollLeft;track.setPointerCapture(pointer);};
  const onMove=e=>{if(pointer!==e.pointerId)return;track.scrollLeft=startScroll-(e.clientX-startX);};
  const onUp=e=>{if(pointer!==e.pointerId)return;pointer=null;announce();};
  const onKey=e=>{if(media.matches)return;if(e.key==="ArrowRight"){e.preventDefault();go(1);}if(e.key==="ArrowLeft"){e.preventDefault();go(-1);}};
  const onScroll=()=>{if(!media.matches)requestAnimationFrame(announce);};
  const teardown=()=>{track.removeEventListener("pointerdown",onDown);track.removeEventListener("pointermove",onMove);track.removeEventListener("pointerup",onUp);track.removeEventListener("pointercancel",onUp);track.removeEventListener("keydown",onKey);track.removeEventListener("scroll",onScroll);};
  const setup=()=>{teardown();if(!media.matches){track.addEventListener("pointerdown",onDown);track.addEventListener("pointermove",onMove);track.addEventListener("pointerup",onUp);track.addEventListener("pointercancel",onUp);track.addEventListener("keydown",onKey);track.addEventListener("scroll",onScroll,{passive:true});}};
  prev?.addEventListener("click",()=>go(-1));next?.addEventListener("click",()=>go(1));
  track.tabIndex=track.tabIndex<0?0:track.tabIndex;track.setAttribute("aria-label","Services carousel");setup();media.addEventListener("change",setup);
  window.addEventListener("pagehide",()=>{teardown();media.removeEventListener("change",setup);},{once:true});
 }
}
