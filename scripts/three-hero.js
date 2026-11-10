const hero=document.querySelector("[data-three-hero]");
const reduced=matchMedia("(prefers-reduced-motion: reduce)").matches;
if(hero&&!reduced&&"WebGLRenderingContext"in window){
 const canvas=document.createElement("canvas");
 const gl=canvas.getContext("webgl",{alpha:true,antialias:false});
 const visible=new IntersectionObserver(async entries=>{
  if(!entries.some(e=>e.isIntersecting))return;
  visible.disconnect();
  if(!gl)return;
  const [threeMod,gsapMod,stMod]=await Promise.all([
   import("https://cdn.jsdelivr.net/npm/three@0.160.0/+esm").catch(()=>null),
   import("https://cdn.jsdelivr.net/npm/gsap@3/+esm").catch(()=>null),
   import("https://cdn.jsdelivr.net/npm/gsap@3/ScrollTrigger/+esm").catch(()=>null)
  ]);
  if(!threeMod||!gsapMod||!stMod||matchMedia("(prefers-reduced-motion: reduce)").matches)return;
  const THREE=threeMod,gsap=gsapMod.gsap||gsapMod.default,ScrollTrigger=stMod.ScrollTrigger;
  gsap.registerPlugin(ScrollTrigger);
  const renderer=new THREE.WebGLRenderer({canvas,context:gl,alpha:true,antialias:false});
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.setSize(hero.clientWidth,hero.clientHeight);
  const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(35,hero.clientWidth/hero.clientHeight,.1,100);
  camera.position.z=5;
  const geometry=new THREE.IcosahedronGeometry(1.15,1);
  const material=new THREE.MeshPhysicalMaterial({color:0x22d3ee,metalness:.35,roughness:.18,transmission:.35,transparent:true,opacity:.8,clearcoat:1});
  const mesh=new THREE.Mesh(geometry,material);scene.add(mesh);
  hero.append(canvas);
  const draw=()=>renderer.render(scene,camera);let raf=0,active=true;
  const tick=()=>{if(!active||document.hidden)return;draw();raf=requestAnimationFrame(tick);};tick();
  const tween=gsap.to(mesh.rotation,{y:Math.PI*1.2,x:.35,ease:"none",scrollTrigger:{trigger:hero,start:"top top",end:"bottom top",scrub:true}});
  const resize=()=>{camera.aspect=hero.clientWidth/hero.clientHeight;camera.updateProjectionMatrix();renderer.setSize(hero.clientWidth,hero.clientHeight);draw();};
  const observer=new ResizeObserver(resize);observer.observe(hero);
  const visibility=()=>{if(document.hidden){cancelAnimationFrame(raf);}else if(active){cancelAnimationFrame(raf);tick();}};
  document.addEventListener("visibilitychange",visibility);
  const dispose=()=>{active=false;cancelAnimationFrame(raf);tween.scrollTrigger?.kill();tween.kill();observer.disconnect();document.removeEventListener("visibilitychange",visibility);geometry.dispose();material.dispose();renderer.dispose();renderer.forceContextLoss();canvas.remove();};
  window.addEventListener("pagehide",dispose,{once:true});
 },{rootMargin:"120px"});
 visible.observe(hero);
}
