(function () {
  "use strict";

  const DEFAULTS = {
    flipDuration: 0.12,
    stagger: 0.06,
    cycleDelay: 2400,
    charset: "alphanumeric",
    flipsPerChar: 8,
    tileColor: "#111827",
    textColor: "#f8fafc",
    tileRadius: 8,
    gap: 6,
    fontSize: 52,
    loop: true,
    padTo: 12,
    align: "left",
    intro: true,
    glare: 0,
    depth: 0.5,
    order: "left",
    tileStyle: "board"
  };

  const CHARSETS = {
    alpha: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    alphanumeric: "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    numeric: "0123456789"
  };

  const clamp = value => Math.min(1, Math.max(0, Number(value) || 0));
  const round = value => Number(value.toFixed(3));
  const cssUnit = value => typeof value === "number" ? value + "px" : value;
  const sampleChar = charset => charset.charAt(Math.floor(Math.random() * charset.length)) || " ";
  const glyph = char => char === " " ? "\u00a0" : char;

  function normalizePhrase(phrase, width, align) {
    const safe = String(phrase == null ? "" : phrase).slice(0, width);
    if (align === "right") return safe.padStart(width, " ");
    if (align === "center") {
      return safe.padStart(safe.length + Math.floor((width - safe.length) / 2), " ").padEnd(width, " ");
    }
    return safe.padEnd(width, " ");
  }

  function cascadeStep(index, width, order, randomOrder) {
    if (order === "right") return width - 1 - index;
    if (order === "center") return Math.floor(Math.abs(index - (width - 1) / 2));
    if (order === "random" && randomOrder) return randomOrder[index];
    return index;
  }

  function shuffleIndices(count) {
    const list = Array.from({ length: count }, (_, index) => index);
    for (let i = count - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [list[i], list[j]] = [list[j], list[i]];
    }
    return list;
  }

  function createChar(value) {
    const span = document.createElement("span");
    span.className = "split-flap-text__char";
    span.textContent = glyph(value);
    return span;
  }

  function createTile(tile, settings) {
    const node = document.createElement("span");
    node.className = "split-flap-text__tile" + (tile.flipping ? " is-flipping" : "");
    node.setAttribute("aria-hidden", "true");

    const top = document.createElement("span");
    top.className = "split-flap-text__half split-flap-text__half--top";
    top.appendChild(createChar(tile.flipping ? tile.next : tile.current));
    node.appendChild(top);

    const bottom = document.createElement("span");
    bottom.className = "split-flap-text__half split-flap-text__half--bottom";
    bottom.appendChild(createChar(tile.current));
    node.appendChild(bottom);

    if (tile.flipping) {
      if (settings.shaded) {
        const shadeTop = document.createElement("span");
        shadeTop.className = "split-flap-text__shade split-flap-text__shade--top";
        node.appendChild(shadeTop);
        const shadeBottom = document.createElement("span");
        shadeBottom.className = "split-flap-text__shade split-flap-text__shade--bottom";
        node.appendChild(shadeBottom);
      }

      const front = document.createElement("span");
      front.className = "split-flap-text__flap split-flap-text__flap--front";
      front.appendChild(createChar(tile.current));
      node.appendChild(front);

      const back = document.createElement("span");
      back.className = "split-flap-text__flap split-flap-text__flap--back";
      back.appendChild(createChar(tile.next));
      node.appendChild(back);
    }
    return node;
  }

  function readPhrases(line) {
    const encoded = line.getAttribute("data-split-flap-words");
    if (encoded) {
      try {
        const parsed = JSON.parse(encoded);
        if (Array.isArray(parsed) && parsed.length) return parsed.map(value => String(value == null ? "" : value));
      } catch (_) {
        return [encoded];
      }
    }
    return [line.textContent.trim()];
  }

  function mount(line) {
    const data = line.dataset;
    const options = Object.assign({}, DEFAULTS, {
      flipDuration: Number(data.flipDuration || DEFAULTS.flipDuration),
      stagger: Number(data.stagger || DEFAULTS.stagger),
      cycleDelay: Number(data.cycleDelay || DEFAULTS.cycleDelay),
      charset: data.charset || DEFAULTS.charset,
      flipsPerChar: Number(data.flipsPerChar == null ? DEFAULTS.flipsPerChar : data.flipsPerChar),
      tileColor: data.tileColor || DEFAULTS.tileColor,
      textColor: data.textColor || DEFAULTS.textColor,
      tileRadius: data.tileRadius == null ? DEFAULTS.tileRadius : data.tileRadius,
      gap: data.gap == null ? DEFAULTS.gap : data.gap,
      fontSize: data.fontSize == null ? DEFAULTS.fontSize : data.fontSize,
      loop: data.loop !== "false",
      padTo: Number(data.padTo || DEFAULTS.padTo),
      align: data.align || DEFAULTS.align,
      intro: data.intro !== "false",
      glare: Number(data.glare || DEFAULTS.glare),
      depth: Number(data.depth == null ? DEFAULTS.depth : data.depth),
      order: data.order || DEFAULTS.order,
      tileStyle: data.tileStyle || DEFAULTS.tileStyle
    });

    const sourcePhrases = readPhrases(line);
    const longest = sourcePhrases.reduce((max, phrase) => Math.max(max, phrase.length), 1);
    const width = Math.max(1, Math.ceil(options.padTo || 0), longest);
    const phrases = sourcePhrases.map(phrase => normalizePhrase(phrase, width, options.align));
    const charset = CHARSETS[options.charset] || options.charset || CHARSETS.alphanumeric;
    const flipMs = Math.max(40, options.flipDuration * 1000);
    const staggerMs = Math.max(0, options.stagger * 1000);
    const holdMs = Math.max(400, options.cycleDelay);
    const flips = Math.max(0, Math.floor(options.flipsPerChar));
    const reducedQuery = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");
    let prefersReduced = Boolean(reducedQuery && reducedQuery.matches);
    let frame = 0;
    let timer = 0;
    let cancelled = false;
    let activeIndex = 0;
    let shown = null;
    let from = null;
    let tiles = [];

    const root = document.createElement("span");
    root.className = [
      "split-flap-text",
      options.tileStyle === "minimal" ? "split-flap-text--minimal" : "",
      options.tileStyle !== "minimal" && clamp(options.glare) > 0 ? "split-flap-text--glare" : ""
    ].filter(Boolean).join(" ");
    root.setAttribute("aria-hidden", "true");

    const level = clamp(options.depth);
    const flat = Math.min(1, level * 2);
    const deep = Math.max(0, level - 0.5) * 2;
    const sheen = options.tileStyle === "minimal" ? 0 : clamp(options.glare);
    const style = {
      "--split-flap-tile-color": options.tileColor,
      "--split-flap-text-color": options.textColor,
      "--split-flap-radius": cssUnit(options.tileRadius),
      "--split-flap-gap": cssUnit(options.gap),
      "--split-flap-font-size": cssUnit(options.fontSize),
      "--split-flap-flip-duration": Math.max(0.04, options.flipDuration) + "s",
      "--split-flap-front-from": round(1 + 0.08 * flat),
      "--split-flap-front-to": round(1 - 0.48 * flat - 0.3 * deep),
      "--split-flap-back-from": round(1 - 0.42 * flat - 0.3 * deep),
      "--split-flap-hinge": "calc(1px + " + round(deep * 0.05) + "em)",
      "--split-flap-hinge-shade": round(0.25 + 0.39 * flat + 0.21 * deep),
      "--split-flap-drop": round(0.28 * flat + 0.2 * deep),
      "--split-flap-lift": round(0.4 + 0.6 * flat + 0.7 * deep),
      "--split-flap-cast": round(deep * 0.62),
      "--split-flap-edge": round(deep * 0.035) + "em",
      "--split-flap-split": (0.015 + level * 0.06).toFixed(3) + "em",
      "--split-flap-glare": round(sheen * 0.55)
    };
    Object.keys(style).forEach(key => root.style.setProperty(key, style[key]));

    const label = document.createElement("span");
    label.className = "split-flap-text__sr";
    label.textContent = String(sourcePhrases[0] || "").trim();
    line.setAttribute("aria-label", label.textContent);
    line.replaceChildren(root, label);

    function renderInitial(phrase) {
      tiles = phrase.split("").map(char => ({
        current: options.intro && !prefersReduced ? " " : char,
        next: char,
        flipping: false,
        tick: 0
      }));
      root.replaceChildren();
      tiles.forEach(tile => root.appendChild(createTile(tile, { shaded: ! (options.tileStyle === "minimal") && deep > 0 })));
    }

    function updateTiles(updates) {
      updates.forEach(update => {
        const previous = tiles[update.index];
        if (!previous) return;
        const next = {
          current: update.current,
          next: update.next,
          flipping: !update.done,
          tick: previous.tick + 1
        };
        tiles[update.index] = next;
        const oldNode = root.children[update.index];
        const newNode = createTile(next, { shaded: options.tileStyle !== "minimal" && deep > 0 });
        if (oldNode) oldNode.replaceWith(newNode);
        else root.appendChild(newNode);
      });
    }

    function stopFrame() {
      if (frame) cancelAnimationFrame(frame);
      frame = 0;
    }

    function animateTo(target) {
      const currentShown = shown == null ? target : shown;
      const startText = normalizePhrase(currentShown, target.length, options.align);
      const randomOrder = options.order === "random" ? shuffleIndices(target.length) : null;
      stopFrame();
      shown = target;
      from = null;
      const plans = [];

      if (!prefersReduced) {
        for (let index = 0; index < target.length; index += 1) {
          if (startText[index] === target[index]) continue;
          const sequence = [];
          for (let i = 0; i < flips; i += 1) sequence.push(sampleChar(charset));
          sequence.push(target[index]);
          plans.push({
            index,
            from: startText[index],
            target: target[index],
            sequence,
            start: cascadeStep(index, target.length, options.order, randomOrder) * staggerMs,
            step: -1,
            done: false
          });
        }
      }

      if (!plans.length) {
        renderInitial(target);
        return 0;
      }

      from = startText;
      renderInitial(startText);
      const totalDuration = plans.reduce((max, plan) => Math.max(max, plan.start + plan.sequence.length * flipMs), 0);
      const startedAt = performance.now();

      const tick = now => {
        if (cancelled) return;
        const elapsed = now - startedAt;
        const updates = [];
        let running = false;

        plans.forEach(plan => {
          const localElapsed = elapsed - plan.start;
          if (localElapsed < 0) {
            running = true;
            return;
          }
          const step = Math.floor(localElapsed / flipMs);
          if (step < plan.sequence.length) {
            running = true;
            if (step !== plan.step) {
              plan.step = step;
              updates.push({
                index: plan.index,
                current: step === 0 ? plan.from : plan.sequence[step - 1],
                next: plan.sequence[step],
                done: false
              });
            }
          } else if (!plan.done) {
            plan.done = true;
            updates.push({ index: plan.index, current: plan.target, next: plan.target, done: true });
          }
        });

        if (updates.length) updateTiles(updates);
        if (running) {
          frame = requestAnimationFrame(tick);
        } else {
          frame = 0;
          from = null;
        }
      };

      frame = requestAnimationFrame(tick);
      return totalDuration;
    }

    function show(index) {
      activeIndex = index;
      label.textContent = String(sourcePhrases[index] || "").trim();
      line.setAttribute("aria-label", label.textContent);
      return animateTo(phrases[index]);
    }

    function scheduleNext(delay) {
      timer = window.setTimeout(() => {
        if (cancelled) return;
        if (document.hidden) {
          scheduleNext(holdMs);
          return;
        }
        const nextIndex = activeIndex + 1;
        if (nextIndex >= phrases.length && !options.loop) return;
        const duration = show(nextIndex % phrases.length);
        scheduleNext(holdMs + duration);
      }, delay);
    }

    if (prefersReduced) {
      shown = phrases[0];
      renderInitial(phrases[0]);
    } else {
      shown = options.intro ? " ".repeat(width) : phrases[0];
      renderInitial(shown);
      const startDuration = animateTo(phrases[0]);
      if (phrases.length > 1) scheduleNext(holdMs + startDuration);
    }

    function onMotionChange(event) {
      prefersReduced = event.matches;
      cancelled = true;
      window.clearTimeout(timer);
      stopFrame();
      if (prefersReduced) {
        cancelled = false;
        shown = phrases[activeIndex];
        renderInitial(shown);
      }
    }
    if (reducedQuery && reducedQuery.addEventListener) reducedQuery.addEventListener("change", onMotionChange);

    line._splitFlapCleanup = () => {
      cancelled = true;
      window.clearTimeout(timer);
      stopFrame();
      if (reducedQuery && reducedQuery.removeEventListener) reducedQuery.removeEventListener("change", onMotionChange);
    };
  }

  document.querySelectorAll("[data-split-flap-words]").forEach(mount);
})();