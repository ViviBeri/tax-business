#!/usr/bin/env python3
"""Capture deployed-site desktop/mobile screenshots and check browser health."""
# Browser audit runs against the published GitHub Pages deployment.
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_URL = "https://viviberi.github.io/tax-business/"
OUTPUT = Path("browser-audit")
OUTPUT.mkdir(exist_ok=True)

failures = []

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    for name, width, height in [
        ("desktop", 1440, 1000),
        ("mobile", 390, 844),
    ]:
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=1,
            is_mobile=name == "mobile",
            has_touch=name == "mobile",
        )
        page.on("pageerror", lambda error, view=name: failures.append(f"{view}: page error: {error}"))
        page.on(
            "console",
            lambda message, view=name: failures.append(f"{view}: console error: {message.text}")
            if message.type == "error" else None,
        )
        response = page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)
        if response is None or response.status >= 400:
            failures.append(f"{name}: homepage returned {response.status if response else 'no response'}")
        page.wait_for_timeout(1500)
        # Full-page screenshots do not scroll through the document, so native
        # lazy-loaded images may remain unloaded. Eager-load and decode them first.
        image_report = page.evaluate("""async () => {
            const images = [...document.images];
            images.forEach(image => { image.loading = "eager"; });
            await Promise.all(images.map(image => image.decode().catch(() => null)));
            return images.map(image => ({
                src: image.currentSrc || image.src,
                alt: image.alt,
                loaded: image.complete && image.naturalWidth > 0,
                naturalWidth: image.naturalWidth
            }));
        }""")
        for image in image_report:
            print(f"{name} image: {image}")
            if not image["loaded"]:
                failures.append(f"{name}: image failed to load: {image['src']}")
        page.screenshot(path=str(OUTPUT / f"{name}.png"), full_page=True)
        metrics = page.evaluate("""() => ({
            title: document.title,
            width: document.documentElement.clientWidth,
            scrollWidth: document.documentElement.scrollWidth,
            height: document.documentElement.scrollHeight
        })""")
        print(f"{name}: {metrics}")
        if not metrics["title"].strip():
            failures.append(f"{name}: missing document title")
        if metrics["scrollWidth"] > metrics["width"] + 2:
            failures.append(f"{name}: horizontal overflow ({metrics['scrollWidth']} > {metrics['width']})")
        page.close()
    browser.close()

if failures:
    print("\n".join(f"FAIL: {failure}" for failure in failures))
    raise SystemExit(1)

print("Browser audit passed. Desktop and mobile screenshots saved.")
