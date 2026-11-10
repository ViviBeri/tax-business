# Redesign preview GIF — 8-second storyboard

**Canvas:** 960 × 600 px  
**Frame rate:** 12–15 fps  
**Target file size:** approximately 2–4 MB  
**Loop:** seamless cut from the final settled frame to the opening frame  
**Capture:** browser viewport at 100% zoom; hide browser chrome; use the English homepage; record the pointer and page only. Avoid recording personal notifications or browser profile details.

| Time | Visual sequence | Cursor position | Easing / transition |
|---|---|---|---|
| 0.0–1.0 s | Fade from the dark glass background into the KVB hero. Wordmark and subtitle resolve first; the accent orbs drift subtly. | Park at the lower-right edge, outside the hero copy. | 500 ms opacity fade; slow ease-in-out orb drift. |
| 1.0–2.4 s | Five service cards appear in order: GST, ITR, FSSAI, Udyam, PAN. | Move to the GST card and pause without clicking. | 180 ms stagger; opacity 0→1 and y 12→0; no overshoot. |
| 2.4–3.4 s | Scroll to the services section; show the five service descriptions and their document-first approach. | Move down the right margin, clear of text. | Smooth scroll over 700–800 ms; restrained reveal. |
| 3.4–4.5 s | Show the three trust/stat cards and the compliance timeline. | Pause near the active timeline step. | Count-up settles once; timeline progress eases linearly with scroll. |
| 4.5–5.6 s | Reveal proof chips for audit, performance, accessibility and local SEO. | Move to the proof strip and hold. | 220 ms stagger with a restrained spring-like settle; maximum 4 px travel. |
| 5.6–6.8 s | Scroll to the contact CTA; show WhatsApp and call actions. | Hover over the primary contact action, but do not click. | 650 ms scroll; 160 ms opacity/contrast transition. |
| 6.8–8.0 s | Settle on the footer, then return to the exact opening hero frame for a clean loop. | Return to the original lower-right resting position. | 700 ms crossfade or cut only when the hero frame matches; hold the final 300 ms. |

## Capture notes

- Use a fixed 960 × 600 viewport and keep the browser at 100% zoom.
- Record at 12–15 fps; export an optimized GIF near 2–4 MB.
- Disable OS notifications and close unrelated tabs before recording.
- Keep the cursor movement deliberate and slow. Do not click, open menus, or expose personal information.
- Capture the final production build after the redesign is approved; do not use a development preview or placeholder audit values.
- Verify the first and last frames visually before publishing the GIF.
