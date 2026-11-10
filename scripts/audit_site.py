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


class SitePageParser(HTMLParser):
    """Collect local references and essential SEO metadata from one HTML page."""
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []
        self.ids: set[str] = set()
        self.lang = ""
        self.title = ""
        self.description = ""
        self.viewport = False
        self.canonical = ""
        self.h1_count = 0
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        tag = tag.lower()
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "html":
            self.lang = values.get("lang", "") or ""
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta":
            name = (values.get("name") or "").lower()
            if name == "description":
                self.description = values.get("content", "") or ""
            if name == "viewport":
                self.viewport = bool(values.get("content"))
        if tag == "link" and "canonical" in (values.get("rel") or "").lower().split():
            self.canonical = values.get("href", "") or ""
        for attribute in ("href", "src", "poster"):
            value = values.get(attribute)
            if value:
                self.references.append(value.strip())

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False


def audit_internal_references(html_files: list[Path]) -> int:
    errors: list[str] = []
    page_parsers: dict[Path, SitePageParser] = {}
    for page in html_files:
        parser = SitePageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        page_parsers[page] = parser

    for page, parser in page_parsers.items():
        for reference in parser.references:
            parsed = urlparse(reference)
            if parsed.scheme or parsed.netloc:
                continue
            if not parsed.path:
                if parsed.fragment and parsed.fragment not in parser.ids:
                    errors.append(
                        f"{page.relative_to(ROOT)}: "
                        f"missing same-page fragment #{parsed.fragment}"
                    )
                continue
            decoded = __import__("urllib.parse", fromlist=["unquote"]).unquote(parsed.path)
            if decoded.startswith("/tax-business/"):
                decoded = decoded[len("/tax-business/"):]
            elif decoded.startswith("/"):
                decoded = decoded.lstrip("/")
            else:
                decoded = (page.parent / decoded).as_posix()
            target = (ROOT / decoded).resolve()
            if ROOT.resolve() not in target.parents and target != ROOT.resolve():
                errors.append(f"{page.relative_to(ROOT)}: reference escapes repository: {reference}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append(f"{page.relative_to(ROOT)}: missing local target {reference}")
                continue
            if parsed.fragment and target.suffix.lower() == ".html":
                target_page = target.relative_to(ROOT)
                target_parser = page_parsers.get(target)
                if target_parser is None:
                    target_parser = SitePageParser()
                    target_parser.feed(target.read_text(encoding="utf-8"))
                    page_parsers[target] = target_parser
                if parsed.fragment not in target_parser.ids:
                    errors.append(f"{page.relative_to(ROOT)}: missing fragment #{parsed.fragment} in {target_page}")

    if errors:
        for error in errors[:100]:
            print(f"::error::{error}")
        if len(errors) > 100:
            print(f"::error::... and {len(errors) - 100} additional broken references")
        fail(f"Found {len(errors)} broken internal references.")
    print(f"PASS: local references resolve across {len(html_files)} HTML pages.")
    return len(html_files)


def audit_page_metadata(html_files: list[Path]) -> None:
    errors: list[str] = []
    for page in html_files:
        parser = SitePageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        label = page.relative_to(ROOT)
        if not parser.lang.strip():
            errors.append(f"{label}: missing html lang attribute")
        if not parser.title.strip():
            errors.append(f"{label}: missing non-empty title")
        if not parser.description.strip():
            errors.append(f"{label}: missing meta description")
        if not parser.viewport:
            errors.append(f"{label}: missing viewport meta")
        if parser.h1_count != 1:
            errors.append(f"{label}: expected exactly one h1, found {parser.h1_count}")
        if not parser.canonical.strip():
            errors.append(f"{label}: missing canonical link")
    if errors:
        for error in errors[:100]:
            print(f"::error::{error}")
        if len(errors) > 100:
            print(f"::error::... and {len(errors) - 100} additional metadata issues")
        fail(f"Found {len(errors)} page metadata issues.")
    print(f"PASS: essential SEO metadata is complete on all {len(html_files)} HTML pages.")



def _relative_luminance(hex_color: str) -> float:
    value = hex_color.removeprefix("#")
    if len(value) == 3:
        value = "".join(char * 2 for char in value)
    if len(value) != 6:
        raise ValueError(f"Expected a six-digit hex color: {hex_color}")
    channels = [int(value[index:index + 2], 16) / 255 for index in (0, 2, 4)]
    linear = [
        channel / 12.92 if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast_ratio(foreground: str, background: str) -> float:
    lighter, darker = sorted(
        (_relative_luminance(foreground), _relative_luminance(background)),
        reverse=True,
    )
    return (lighter + 0.05) / (darker + 0.05)


def audit_accessibility_colors() -> None:
    css = (ROOT / "site-quality-fix.css").read_text(encoding="utf-8")
    required_rules = (
        ".hero-title-main .split-flap-text__char",
        ".hero-title-accent .split-flap-text__char",
        ".hero-copy > .trust",
        ".hero-card .trust-item > span",
        ".location-card--featured .location-card__copy strong",
    )
    missing = [selector for selector in required_rules if selector not in css]
    if missing:
        fail("Missing final contrast override(s): " + ", ".join(missing))

    # Check the foreground/background pairs enforced by the final CSS layer.
    pairs = (
        ("Hero main heading", "#172b4d", "#f5fbf7"),
        ("Hero accent heading", "#086b46", "#f5fbf7"),
        ("Hero trust text", "#334155", "#ffffff"),
        ("Hero-card trust text", "#334155", "#f8fbf9"),
        ("Primary button text", "#ffffff", "#086b46"),
        ("Service-card supporting text", "#526275", "#ffffff"),
        ("Featured location heading", "#ffffff", "#203e63"),
        ("Featured location supporting text", "#e2e8f0", "#203e63"),
        ("Dark-section text", "#f4f7fb", "#101f38"),
    )
    failures: list[str] = []
    for label, foreground, background in pairs:
        ratio = _contrast_ratio(foreground, background)
        print(f"Contrast: {label}: {ratio:.2f}:1")
        if ratio < 4.5:
            failures.append(f"{label}: {ratio:.2f}:1 (requires 4.5:1)")
    if failures:
        for failure in failures:
            print(f"::error::{failure}")
        fail(f"Found {len(failures)} WCAG AA contrast failure(s).")
    print("PASS: all configured normal-text color pairs meet WCAG AA (4.5:1).")

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
        target = ROOT / relative / "index.html" if url.endswith("/") else ROOT / (relative or "index.html")
        if not target.is_file():
            fail(f"Sitemap URL has no matching file: {url} (expected {target.relative_to(ROOT)})")

    text_urls = [line.strip() for line in text_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(text_urls) != len(urls) or set(text_urls) != set(urls):
        fail("sitemap.txt must contain exactly the same URLs as sitemap.xml (order may differ)")

    robots = robots_path.read_text(encoding="utf-8")
    if f"Sitemap: {SITE}sitemap.xml" not in robots:
        fail("robots.txt must point to the canonical sitemap.xml")

    service_pages = sorted(page for page in (ROOT / "services").glob("*.html") if page.name not in {"gst-filing.html", "gst-registration.html"})
    tamil_pages = sorted((ROOT / "ta" / "services").glob("*.html"))
    pages = service_pages + tamil_pages
    if len(service_pages) != 8 or len(tamil_pages) != 8:
        fail(f"Expected 8 localized English and 8 Tamil service pages; found {len(service_pages)} and {len(tamil_pages)}")

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
        expected_language = "ta-IN" if page.relative_to(ROOT).parts[0] == "ta" else "en-IN"
        if not any(item.get("@type") == "WebPage" and item.get("inLanguage") == expected_language for item in graph if isinstance(item, dict)):
            fail(f"{page.relative_to(ROOT)} WebPage must declare inLanguage={expected_language}")
        canonical = SITE + page.relative_to(ROOT).as_posix()
        if not any(item.get("@type") == "WebPage" and item.get("url") == canonical for item in graph if isinstance(item, dict)):
            fail(f"{page.relative_to(ROOT)} WebPage JSON-LD URL must match {canonical}")

    print(f"PASS: {len(urls)} unique sitemap URLs resolve to repository files.")
    print("PASS: sitemap.txt matches sitemap.xml and robots.txt references the sitemap.")
    print(f"PASS: {len(pages)} service pages contain valid localized WebPage + Service JSON-LD.")

    html_files = sorted(path for path in ROOT.rglob("*.html") if "_builder" not in path.parts)
    audit_internal_references(html_files)
    audit_page_metadata(html_files)
    audit_accessibility_colors()


if __name__ == "__main__":
    main()
