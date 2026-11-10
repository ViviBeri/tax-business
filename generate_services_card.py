"""Generate a glassmorphic services card for the KVB ENTERPRISES website.

Requires godprofile-mcp. Run from the repository root:
    python3 generate_services_card.py
"""

from pathlib import Path
import re

from godprofile_mcp.core.svg_rendering import generate_svg_card


def main() -> None:
    output = Path("assets/services-card.svg")
    output.parent.mkdir(parents=True, exist_ok=True)

    svg = generate_svg_card(
        theme="luxury-glass",
        title="KVB ENTERPRISES",
        description="Tax and Business Compliance",
        tags=["GST", "ITR", "FSSAI", "Udyam", "PAN"],
        identifier="KVB",
    )

    # This card is informational, not a live GitHub profile widget.
    # Remove the toolkit's optional stars/forks tracking placeholders.
    svg = re.sub(
        r'\s*<text[^>]*>.*?STARS_COUNT_KVB.*?</text>',
        "",
        svg,
        flags=re.DOTALL,
    )
    svg = re.sub(
        r'\s*<text[^>]*>.*?FORKS_COUNT_KVB.*?</text>',
        "",
        svg,
        flags=re.DOTALL,
    )

    output.write_text(svg, encoding="utf-8")
    print(f"Services card generated: {output}")


if __name__ == "__main__":
    main()
