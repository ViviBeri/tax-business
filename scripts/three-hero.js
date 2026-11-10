async function initThreeHero() {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion || !("WebGLRenderingContext" in window)) return;

  const hero = document.querySelector(".hero");
  if (!hero || !hero.querySelector(".hero-illustration")) return;
  const rect = hero.getBoundingClientRect();
  if (rect.bottom <= 0 || rect.top >= window.innerHeight) return;

  let THREE;
  try {
    THREE = await import("https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js");
  } catch {
    return;
  }

  if (!hero.isConnected || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const canvas = document.createElement("canvas");
  canvas.className = "hero-glass-canvas";
  canvas.setAttribute("aria-hidden", "true");
  canvas.style.cssText = "position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:1";
  const illustration = hero.querySelector(".hero-illustration");
  if (getComputedStyle(hero).position === "static") hero.style.position = "relative";
  hero.append(canvas);

  let renderer;
  let geometry;
  let material;
  let mesh;
  let frame = 0;
  let disposed = false;
  let scrollHandler;

  try {
    renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
    renderer.setSize(hero.clientWidth, hero.clientHeight, false);
    renderer.setClearColor(0x000000, 0);
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(32, hero.clientWidth / hero.clientHeight, .1, 100);
    camera.position.z = 7;
    geometry = new THREE.SphereGeometry(.82, 48, 32);
    material = new THREE.MeshPhysicalMaterial({
      color: 0xa8e8d2,
      metalness: .12,
      roughness: .12,
      transmission: .88,
      thickness: .8,
      transparent: true,
      opacity: .72,
      clearcoat: 1,
      clearcoatRoughness: .08
    });
    mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(1.75, .05, 0);
    scene.add(mesh);
    scene.add(new THREE.HemisphereLight(0xffffff, 0x527b70, 2));
    const key = new THREE.DirectionalLight(0xffffff, 2.2);
    key.position.set(-3, 4, 5);
    scene.add(key);

    const render = () => {
      if (disposed) return;
      renderer.render(scene, camera);
      frame = requestAnimationFrame(render);
    };
    const resize = () => {
      if (disposed) return;
      const width = hero.clientWidth;
      const height = hero.clientHeight;
      if (!width || !height) return;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height, false);
    };
    scrollHandler = () => {
      const bounds = hero.getBoundingClientRect();
      const progress = Math.min(1, Math.max(0, (window.innerHeight - bounds.top) / (window.innerHeight + bounds.height)));
      mesh.rotation.y = progress * Math.PI * 1.5;
      mesh.rotation.x = progress * .65;
    };
    window.addEventListener("scroll", scrollHandler, { passive: true });
    window.addEventListener("resize", resize);
    scrollHandler();
    render();

    const observer = new IntersectionObserver((entries) => {
      if (!entries.some((entry) => entry.isIntersecting)) return;
      scrollHandler();
    }, { threshold: 0 });
    observer.observe(hero);

    window.addEventListener("pagehide", () => {
      if (disposed) return;
      disposed = true;
      cancelAnimationFrame(frame);
      window.removeEventListener("scroll", scrollHandler);
      window.removeEventListener("resize", resize);
      observer.disconnect();
      geometry?.dispose();
      material?.dispose();
      renderer?.dispose();
      canvas.remove();
    }, { once: true });
  } catch {
    if (frame) cancelAnimationFrame(frame);
    window.removeEventListener("scroll", scrollHandler);
    geometry?.dispose();
    material?.dispose();
    renderer?.dispose();
    canvas.remove();
  }
}

initThreeHero().catch(() => {});
