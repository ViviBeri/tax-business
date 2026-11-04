#!/usr/bin/env python3
"""Dependency-free integrity checks for the KVB static website."""
from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://viviberi.github.io/tax-business/"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class JsonLdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_jsonld = False
        self.current: list[str] = []
        self.blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "script" and dict(attrs).get("type", "").lower() == "application/ld+json":
            self.in_jsonld = True
            self.current = []

    def handle_data(self, data: str) -> None:
        if self.in_jsonld:
            self.current.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self.in_jsonld:
            self.blocks.append("".join(self.current))
            self.in_jsonld = False


def fail(message: str) -> None:
    print(f"::error::{message}")
    raise SystemExit(1)


def main() -> None:
    xml_path = ROOT / "sitemap.xml"
    text_path = ROOT / "sitemap.txt"
    robots_path = ROOT / "robots.txt"
    for path in (xml_path, text_path, robots_path):
        if not path.is_file():
            fail(f"Required SEO file is missing: {path.relative_to(ROOT)}")

    try:
        root = ElementTree.parse(xml_path).getroot()
    except ElementTree.ParseError as exc:
        fail(f"sitemap.xml is not valid XML: {exc}")

    urls = [node.text.strip() for node in root.findall("sm:url/sm:loc", SITEMAP_NS) if node.text]
    if not urls:
        fail("sitemap.xml contains no URL locations")
    if len(urls) != len(set(urls)):
        fail("sitemap.xml contains duplicate URLs")

    for url in urls:
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            fail(f"Sitemap URL must use HTTPS: {url}")
        if not url.startswith(SITE):
            fail(f"Sitemap URL is outside the published site: {url}")
        relative = url[len(SITE):]
        target = ROOT / (relative if relative else "index.html")
        if url.endswith("/"):
            target = target / "index.html"
        if not target.is_file():
            fail(f"Sitemap URL has no matching file: {url} (expected {target.relative_to(ROOT)})")

    text_urls = [line.strip() for line in text_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if text_urls != urls:
        fail("sitemap.txt does not exactly match sitemap.xml in URL order and content")

    robots = robots_path.read_text(encoding="utf-8")
    if f"Sitemap: {SITE}sitemap.xml" not in robots:
        fail("robots.txt must point to the canonical sitemap.xml")

    service_pages = sorted((ROOT / "services").glob("*.html"))
    tamil_pages = sorted((ROOT / "ta" / "services").glob("*.html"))
    pages = service_pages + tamil_pages
    if len(service_pages) != 9 or len(tamil_pages) != 8:
        fail(f"Expected 9 English and 8 Tamil service pages; found {len(service_pages)} and {len(tamil_pages)}")

    for page in pages:
        parser = JsonLdParser()
        parser.feed(page.read_text(encoding="utf-8"))
        if len(parser.blocks) != 1:
            fail(f"{page.relative_to(ROOT)} must contain exactly one JSON-LD script; found {len(parser.blocks)}")
        try:
            data = json.loads(parser.blocks[0])
        except json.JSONDecodeError as exc:
            fail(f"{page.relative_to(ROOT)} has invalid JSON-LD: {exc}")
        graph = data.get("@graph", []) if isinstance(data, dict) else []
        types = {
            item.get("@type")
            for item in graph
            if isinstance(item, dict)
        }
        if not {"WebPage", "Service"}.issubset(types):
            fail(f"{page.relative_to(ROOT)} JSON-LD graph must include WebPage and Service")
        expected_language = "ta-IN" if page.parts[0] == "ta" else "en-IN"
        if not any(item.get("@type") == "WebPage" and item.get("inLanguage") == expected_language for item in graph if isinstance(item, dict)):
            fail(f"{page.relative_to(ROOT)} WebPage must declare inLanguage={expected_language}")
        canonical = SITE + page.relative_to(ROOT).as_posix()
        if not any(item.get("@type") == "WebPage" and item.get("url") == canonical for item in graph if isinstance(item, dict)):
            fail(f"{page.relative_to(ROOT)} WebPage JSON-LD URL must match {canonical}")

    print(f"PASS: {len(urls)} unique sitemap URLs resolve to repository files.")
    print("PASS: sitemap.txt matches sitemap.xml and robots.txt references the sitemap.")
    print(f"PASS: {len(pages)} service pages contain valid localized WebPage + Service JSON-LD.")


if __name__ == "__main__":
    main()
