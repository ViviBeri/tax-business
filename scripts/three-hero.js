async function initThreeHero() {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const desktop = window.matchMedia("(min-width: 961px)");
  const connection = navigator.connection;
  if (reduceMotion.matches || !desktop.matches || !("WebGLRenderingContext" in window)) return;
  if (connection?.saveData || /^(slow-2g|2g)$/.test(connection?.effectiveType || "")) return;

  const hero = document.querySelector(".hero");
  const illustration = hero?.querySelector(".hero-illustration");
  if (!hero || !illustration) return;
  const initial = hero.getBoundingClientRect();
  if (initial.bottom <= 0 || initial.top >= window.innerHeight) return;

  let THREE;
  try {
    THREE = await import("https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js");
  } catch {
    return;
  }
  if (!hero.isConnected || reduceMotion.matches) return;

  let renderer, geometry, material, mesh, observer, frame = 0, disposed = false;
  const canvas = document.createElement("canvas");
  canvas.className = "hero-glass-canvas";
  canvas.setAttribute("aria-hidden","true");
  canvas.style.cssText = "position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:0";
  try {
    renderer = new THREE.WebGLRenderer({canvas,alpha:true,antialias:true});
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1,1.5));
    renderer.setSize(hero.clientWidth,hero.clientHeight,false);
    renderer.setClearColor(0x000000,0);
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(32,hero.clientWidth/Math.max(1,hero.clientHeight),.1,100);
    camera.position.z = 7;
    geometry = new THREE.SphereGeometry(.82,40,28);
    material = new THREE.MeshPhysicalMaterial({color:0x075f46,metalness:.08,roughness:.2,transmission:.72,thickness:.7,transparent:true,opacity:.58,clearcoat:.8});
    mesh = new THREE.Mesh(geometry,material);
    mesh.position.set(1.75,.05,0);
    scene.add(mesh);
    scene.add(new THREE.HemisphereLight(0xffffff,0x527b70,1.8));
    const light = new THREE.DirectionalLight(0xffffff,1.8);
    light.position.set(-3,4,5);
    scene.add(light);

    let visible = true;
    const render = () => {
      if (disposed || !visible) { frame = 0; return; }
      renderer.render(scene,camera);
      frame = requestAnimationFrame(render);
    };
    const syncScroll = () => {
      if (disposed) return;
      const bounds = hero.getBoundingClientRect();
      const progress = Math.min(1,Math.max(0,(window.innerHeight-bounds.top)/(window.innerHeight+bounds.height)));
      mesh.rotation.y = progress * Math.PI * 1.5;
      mesh.rotation.x = progress * .55;
      if (visible && !frame) render();
    };
    const resize = () => {
      if (disposed) return;
      const width = hero.clientWidth, height = hero.clientHeight;
      if (!width || !height) return;
      camera.aspect = width/height;
      camera.updateProjectionMatrix();
      renderer.setSize(width,height,false);
    };
    if (getComputedStyle(hero).position === "static") hero.style.position = "relative";
    hero.append(canvas);
    observer = new IntersectionObserver(entries => {
      visible = entries.some(entry => entry.isIntersecting);
      if (visible) syncScroll();
      else if (frame) { cancelAnimationFrame(frame); frame = 0; }
    },{threshold:0});
    observer.observe(hero);
    window.addEventListener("scroll",syncScroll,{passive:true});
    window.addEventListener("resize",resize);
    reduceMotion.addEventListener("change",() => { if (reduceMotion.matches) cleanup(); },{once:true});

    function cleanup() {
      if (disposed) return;
      disposed = true;
      if (frame) cancelAnimationFrame(frame);
      window.removeEventListener("scroll",syncScroll);
      window.removeEventListener("resize",resize);
      observer?.disconnect();
      geometry?.dispose();
      material?.dispose();
      renderer?.dispose();
      renderer?.forceContextLoss?.();
      canvas.remove();
    }
    window.addEventListener("pagehide",cleanup,{once:true});
    syncScroll();
  } catch {
    if (frame) cancelAnimationFrame(frame);
    observer?.disconnect();
    geometry?.dispose();
    material?.dispose();
    renderer?.dispose();
    canvas.remove();
  }
}
const scheduleThreeHero = () => {
  const start = () => initThreeHero().catch(() => {});
  if ("requestIdleCallback" in window) window.requestIdleCallback(start, { timeout: 1800 });
  else window.setTimeout(start, 250);
};
scheduleThreeHero();
