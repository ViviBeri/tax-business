(function () {
  "use strict";
  const CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  const FLIP_MS = 120, STAGGER_MS = 60, FLIPS_PER_CHAR = 8;
  const glyph = c => c === " " ? "\u00a0" : c;
  const randomChar = () => CHARSET[Math.floor(Math.random() * CHARSET.length)];

  function charNode(value) {
    const node = document.createElement("span");
    node.className = "split-flap-text__char";
    node.textContent = glyph(value);
    return node;
  }

  function buildTile(host, current, next, flipping) {
    const tile = document.createElement("span");
    tile.className = "split-flap-text__tile" + (flipping ? " is-flipping" : "");
    tile.setAttribute("aria-hidden", "true");

    const top = document.createElement("span");
    top.className = "split-flap-text__half split-flap-text__half--top";
    top.appendChild(charNode(flipping ? next : current));
    tile.appendChild(top);

    const bottom = document.createElement("span");
    bottom.className = "split-flap-text__half split-flap-text__half--bottom";
    bottom.appendChild(charNode(current));
    tile.appendChild(bottom);

    if (flipping) {
      const shadeTop = document.createElement("span");
      shadeTop.className = "split-flap-text__shade split-flap-text__shade--top";
      tile.appendChild(shadeTop);
      const shadeBottom = document.createElement("span");
      shadeBottom.className = "split-flap-text__shade split-flap-text__shade--bottom";
      tile.appendChild(shadeBottom);
      const front = document.createElement("span");
      front.className = "split-flap-text__flap split-flap-text__flap--front";
      front.appendChild(charNode(current));
      tile.appendChild(front);
      const back = document.createElement("span");
      back.className = "split-flap-text__flap split-flap-text__flap--back";
      back.appendChild(charNode(next));
      tile.appendChild(back);
    }
    host.appendChild(tile);
    return tile;
  }

  function updateTile(tile, current, next, flipping) {
    const replacement = buildTile(document.createDocumentFragment(), current, next, flipping);
    tile.replaceWith(replacement);
    return replacement;
  }

  function mount(line) {
    const phrase = line.getAttribute("data-split-flap-words") || line.textContent.trim();
    const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const host = document.createElement("span");
    host.className = "split-flap-text";
    host.setAttribute("aria-hidden", "true");
    line.setAttribute("aria-label", phrase);
    line.replaceChildren(host);

    const sr = document.createElement("span");
    sr.className = "split-flap-text__sr";
    sr.textContent = phrase;
    line.appendChild(sr);

    const chars = Array.from(phrase);
    const width = Math.max(12, chars.length);
    while (chars.length < width) chars.push(" ");
    const tiles = chars.map(char => buildTile(host, reduced ? char : " ", reduced ? char : " ", false));
    if (reduced) return;

    chars.forEach((target, index) => {
      if (target === " ") return;
      const sequence = Array.from({ length: FLIPS_PER_CHAR }, randomChar).concat(target);
      sequence.forEach((next, step) => {
        window.setTimeout(() => {
          const current = step === 0 ? " " : sequence[step - 1];
          tiles[index] = updateTile(tiles[index], current, next, true);
          window.setTimeout(() => {
            tiles[index] = updateTile(tiles[index], next, next, false);
          }, FLIP_MS);
        }, index * STAGGER_MS + step * FLIP_MS);
      });
    });
  }

  document.querySelectorAll("[data-split-flap-words]").forEach(mount);
})();