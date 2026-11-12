#!/usr/bin/env python3
"""Audit English and Tamil homepages at desktop and mobile breakpoints.

Scroll through the complete page before taking full-page screenshots so
IntersectionObserver-driven reveal effects are exercised rather than captured
in their initial hidden state.
"""
import os
from pathlib import Path
from xml.etree import ElementTree

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

            # Exercise each reveal target in sequence. Waiting between scrolls
            # gives IntersectionObserver a frame to reveal intermediate cards,
            # including horizontally off-screen carousel slides on mobile.
            page.evaluate("""async () => {
                document.documentElement.style.scrollBehavior = "auto";
                const items = [...document.querySelectorAll(".kvb-reveal")];
                for (const item of items) {
                    if (!item.getClientRects().length) continue;
                    item.scrollIntoView({ block: "center", inline: "center", behavior: "instant" });
                    await new Promise(resolve => requestAnimationFrame(() =>
                        requestAnimationFrame(() => setTimeout(resolve, 35))
                    ));
                }
                window.scrollTo({ top: 0, behavior: "instant" });
                await new Promise(resolve => requestAnimationFrame(() =>
                    requestAnimationFrame(resolve)
                ));
            }""")
            page.wait_for_timeout(700)

            reveal_state = page.evaluate("""() => {
                const items = [...document.querySelectorAll(".kvb-reveal")];
                const inLayout = items.filter(item => item.getClientRects().length > 0);
                const serviceTiles = [...document.querySelectorAll("#services .tile")];
                return {
                    revealCount: items.length,
                    visibleRevealCount: inLayout.length,
                    hiddenVisibleRevealCount: inLayout.filter(item => !item.classList.contains("is-visible")).length,
                    serviceTileCount: serviceTiles.length,
                    unrevealedServiceTileCount: serviceTiles.filter(item =>
                        item.classList.contains("kvb-reveal") && !item.classList.contains("is-visible")
                    ).length
                };
            }""")
            print(f"{label}: scrolled reveal state {reveal_state}")
            if reveal_state["hiddenVisibleRevealCount"]:
                failures.append(
                    f"{label}: {reveal_state['hiddenVisibleRevealCount']} visible reveal elements remain hidden after scrolling"
                )
            if reveal_state["serviceTileCount"] < 8:
                failures.append(
                    f"{label}: expected 8 service tiles after scrolling, found {reveal_state['serviceTileCount']}"
                )
            if reveal_state["unrevealedServiceTileCount"]:
                failures.append(
                    f"{label}: {reveal_state['unrevealedServiceTileCount']} service tiles remain unrevealed"
                )

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

    # Smoke-test every sitemap URL at desktop and mobile widths. The detailed
    # reveal/image checks above remain focused on the two homepages.
    sitemap = ElementTree.parse("sitemap.xml").getroot()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [node.text for node in sitemap.findall("sm:url/sm:loc", namespace) if node.text]
    print(f"Running responsive smoke checks for {len(urls)} sitemap URLs")
    for index, url in enumerate(urls, start=1):
        for name, width, height in [("desktop", 1440, 900), ("mobile", 390, 844)]:
            label = f"sitemap-{index}-{name}"
            page = browser.new_page(
                viewport={"width": width, "height": height},
                device_scale_factor=1,
                is_mobile=name == "mobile",
                has_touch=name == "mobile",
            )
            page.on("pageerror", lambda error, view=label: failures.append(f"{view}: page error: {error}"))
            try:
                response = page.goto(url, wait_until="domcontentloaded", timeout=20000)
                if response is None or response.status >= 400:
                    failures.append(f"{label}: {url} returned {response.status if response else 'no response'}")
                else:
                    metrics = page.evaluate("""() => ({
                        title: document.title.trim(),
                        h1: document.querySelectorAll("h1").length,
                        width: document.documentElement.clientWidth,
                        scrollWidth: document.documentElement.scrollWidth
                    })""")
                    if not metrics["title"]:
                        failures.append(f"{label}: missing title at {url}")
                    if metrics["h1"] != 1:
                        failures.append(f"{label}: expected one h1, found {metrics['h1']} at {url}")
                    if metrics["scrollWidth"] > metrics["width"] + 2:
                        failures.append(
                            f"{label}: horizontal overflow ({metrics['scrollWidth']} > {metrics['width']}) at {url}"
                        )
            except Exception as error:
                failures.append(f"{label}: failed to load {url}: {error}")
            finally:
                page.close()
            print(f"{label}: checked {url}")
    browser.close()

if failures:
    print("\n".join(f"FAIL: {failure}" for failure in failures))
    raise SystemExit(1)

print(f"Browser audit passed for {len(urls)} sitemap URLs at desktop and mobile widths, plus detailed homepage checks.")
