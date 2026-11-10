"""Generate the KVB ENTERPRISES SVG hero banner.

Requires slabkit. Run from the repository root:
    python3 generate_hero.py
"""

from pathlib import Path

from slabkit import Theme, banner, write


def main() -> None:
    output = Path("assets/hero-banner.svg")
    output.parent.mkdir(parents=True, exist_ok=True)

    theme = Theme(158)
    write(
        str(output),
        banner(
            theme,
            "KVB ENTERPRISES",
            "Tax & Business Compliance, Simplified",
            meta="GST · ITR · FSSAI · Udyam · PAN",
            note="Puducherry, India",
        ),
    )
    print(f"Hero banner generated: {output}")


if __name__ == "__main__":
    main()
