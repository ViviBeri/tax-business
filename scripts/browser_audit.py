#!/usr/bin/env python3
"""Audit English and Tamil homepages at desktop and mobile breakpoints.

Scroll through the complete page before taking full-page screenshots so
IntersectionObserver-driven reveal effects are exercised rather than captured
in their initial hidden state.
"""
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("KVB_AUDIT_URL", "https://viviberi.github.io/tax-business/")
EXPECT_PREMIUM_STYLESHEET = "KVB_AUDIT_URL" in os.environ
OUTPUT = Path("browser-audit")
OUTPUT.mkdir(exist_ok=True)

failures = []

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    for locale, route in [("english", ""), ("tamil", "ta/")]:
        for name, width, height in [
            ("desktop", 1440, 1000),
            ("mobile", 390, 844),
        ]:
            label = f"{locale}-{name}"
            page = browser.new_page(
                viewport={"width": width, "height": height},
                device_scale_factor=1,
                is_mobile=name == "mobile",
                has_touch=name == "mobile",
            )
            page.on("pageerror", lambda error, view=label: failures.append(f"{view}: page error: {error}"))
            page.on(
                "console",
                lambda message, view=label: failures.append(f"{view}: console error: {message.text}")
                if message.type == "error" else None,
            )
            response = page.goto(
                f"{BASE_URL.rstrip('/')}/{route}",
                wait_until="domcontentloaded",
                timeout=60000,
            )
            if response is None or response.status >= 400:
                failures.append(f"{label}: homepage returned {response.status if response else 'no response'}")
                page.close()
                continue

            page.wait_for_timeout(500)
            metrics = page.evaluate("""() => ({
                title: document.title,
                width: document.documentElement.clientWidth,
                scrollWidth: document.documentElement.scrollWidth,
                height: document.documentElement.scrollHeight,
                hero: Boolean(document.querySelector('.hero h1')),
                services: document.querySelectorAll('#services .tile').length,
                premiumStylesheet: [...document.styleSheets].some(sheet =>
                    sheet.href && sheet.href.includes('kvb-premium-pass.css')
                )
            })""")
            print(f"{label}: initial metrics {metrics}")
            if not metrics["title"].strip():
                failures.append(f"{label}: missing document title")
            if metrics["scrollWidth"] > metrics["width"] + 2:
                failures.append(f"{label}: horizontal overflow ({metrics['scrollWidth']} > {metrics['width']})")
            if not metrics["hero"]:
                failures.append(f"{label}: hero heading is missing")
            if metrics["services"] < 8:
                failures.append(f"{label}: expected at least 8 service tiles, found {metrics['services']}")
            if EXPECT_PREMIUM_STYLESHEET and not metrics["premiumStylesheet"]:
                failures.append(f"{label}: premium stylesheet was not loaded")

            # Trigger viewport-based reveals throughout the page before the
            # full-page screenshot. A full_page screenshot alone does not
            # reliably fire IntersectionObserver callbacks for off-screen
            # sections.
            step = max(400, int(height * 0.72))
            for offset in range(0, metrics["height"], step):
                page.evaluate("(y) => window.scrollTo(0, y)", offset)
                page.wait_for_timeout(160)
            page.evaluate("() => window.scrollTo(0, 0)")
            page.wait_for_timeout(350)

            reveal_state = page.evaluate("""() => ({
                revealCount: document.querySelectorAll('.kvb-reveal').length,
                hiddenRevealCount: document.querySelectorAll('.kvb-reveal:not(.is-visible)').length,
                servicesVisible: [...document.querySelectorAll('#services .tile')].filter(
                    element => element.getBoundingClientRect().height > 0
                ).length
            })""")
            print(f"{label}: scrolled reveal state {reveal_state}")
            if reveal_state["hiddenRevealCount"]:
                failures.append(
                    f"{label}: {reveal_state['hiddenRevealCount']} reveal elements remain hidden after scrolling"
                )
            if reveal_state["servicesVisible"] < 8:
                failures.append(f"{label}: service tiles are not fully visible after scrolling")

            image_report = page.evaluate("""async () => {
                const images = [...document.images];
                images.forEach(image => { image.loading = "eager"; });
                await Promise.all(images.map(image => image.decode().catch(() => null)));
                return images.map(image => ({
                    src: image.currentSrc || image.src,
                    loaded: image.complete && image.naturalWidth > 0
                }));
            }""")
            for item in image_report:
                if not item["loaded"]:
                    failures.append(f"{label}: image failed to load: {item['src']}")

            page.screenshot(path=str(OUTPUT / f"{label}.png"), full_page=True)
            page.close()
    browser.close()

if failures:
    print("\n".join(f"FAIL: {failure}" for failure in failures))
    raise SystemExit(1)

print("Browser audit passed for English and Tamil homepages on desktop and mobile.")
