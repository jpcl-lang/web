"""The square Open Graph card: assets/img/png/square.png, 1200x1200.

The second image on the page. Chat clients and anything showing a compact
preview crop a wide card badly, or fall back to the favicon; a square one keeps
the mark and the wordmark whole. Same palette, same mark, less in it — at the
size these are actually shown, the tagline is the last thing that still reads.

    uv run --project tools square
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from . import mark
from .palette import BG, BYAKUGUN, MOMO, MUTED, SAKURA, TEXT
from .render import Canvas, find_site_root, save

SIZE = 1200
MARK = 280


def render(root: Path) -> Image.Image:
    canvas = Canvas(SIZE, SIZE, BG, root)
    canvas.glow(0.20 * SIZE, 0.18 * SIZE, 0.70 * SIZE, MOMO, 0.14)
    canvas.glow(0.88 * SIZE, 0.90 * SIZE, 0.55 * SIZE, BYAKUGUN, 0.08)

    s, draw = canvas.s, canvas.draw
    middle = SIZE / 2

    # (text, font, colour, gap above it). The mark is the first row; everything
    # is measured and stacked below, then the whole block is centred, so
    # nudging a font size cannot quietly unbalance the card.
    rows = [
        (None, None, None, 0),
        ("JPML", canvas.sans("Bold", 152), TEXT, 54),
        ("TOML’s sections.", canvas.sans("SemiBold", 52), SAKURA, 40),
        ("JSON’s nesting.", canvas.sans("SemiBold", 52), SAKURA, 14),
        ("A configuration language", canvas.sans("Regular", 34), MUTED, 44),
        ("for files people edit by hand.", canvas.sans("Regular", 34), MUTED, 10),
        ("pip install jpml    npm install jpml-lang",
         canvas.sans("Medium", 30), MOMO, 52),
    ]

    # Measure first: each row's real ink height, in 1x design units.
    measured = []
    for text, font, colour, gap in rows:
        if text is None:
            measured.append((None, None, None, gap, MARK, 0))
            continue
        x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=font, anchor="la")
        measured.append((text, font, colour, gap, (y1 - y0) / canvas.s(1), y0))

    total = sum(gap + height for _, _, _, gap, height, _ in measured)
    cursor = (SIZE - total) / 2

    for text, font, colour, gap, height, top_bearing in measured:
        cursor += gap
        if text is None:
            mark.draw(draw, middle - MARK / 2, cursor, MARK, scale=s)
        else:
            # Anchor by the ink, not the ascender, so the stack has no drift.
            draw.text((s(middle), s(cursor) - top_bearing), text,
                      font=font, fill=colour, anchor="ma")
        cursor += height

    return canvas.finish()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-o", "--output", type=Path,
                        help="where to write the PNG (default: the site's square card)")
    args = parser.parse_args()

    root = find_site_root()
    save(render(root), args.output or root / "assets" / "img" / "png" / "square.png", root)


if __name__ == "__main__":
    main()
