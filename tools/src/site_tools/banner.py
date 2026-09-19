"""The wide Open Graph card: assets/img/png/banner.png, 1280x640.

The cards social sites show are the one part of the site that cannot be CSS, so
they are drawn from the same palette rather than kept as binaries nobody can
edit.

    uv run --project tools banner
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from . import mark
from .palette import (BG, BYAKUGUN, COMMENT, LINE, MOMO, MUTED, PANEL, PUNCT,
                      SAKURA, TEXT, TORINOKO)
from .render import Canvas, find_site_root, save

W, H = 1280, 640

SNIPPET = [
    [("# a value is allowed to be empty", COMMENT)],
    [("[", PUNCT), ("SERVER_ID", MOMO), ("]", PUNCT)],
    [("config", TORINOKO), (": {", PUNCT)],
    [("  disabled_channels", TORINOKO), (":,", PUNCT)],
    [("  disabled_users", TORINOKO), (": [", PUNCT), ("9892", BYAKUGUN),
     (", ", PUNCT), ("8209", BYAKUGUN), ("]", PUNCT)],
    [("}", PUNCT)],
]


def draw_code_card(canvas: Canvas, x: float, y: float, w: float, h: float):
    s, draw = canvas.s, canvas.draw
    draw.rounded_rectangle((s(x), s(y), s(x + w), s(y + h)),
                           radius=s(18), fill=PANEL, outline=LINE, width=s(1))

    head = 46
    draw.line((s(x), s(y + head), s(x + w), s(y + head)), fill=LINE, width=s(1))
    draw.text((s(x + 24), s(y + head / 2)), "servers.jp",
              font=canvas.mono(17), fill=COMMENT, anchor="lm")

    font = canvas.mono(23)
    for row, runs in enumerate(SNIPPET):
        canvas.spans(x + 24, y + head + 30 + row * 41, runs, font)


def render(root: Path) -> Image.Image:
    canvas = Canvas(W, H, BG, root)
    canvas.glow(0.18 * W, 0.16 * H, 0.62 * W, MOMO, 0.13)
    canvas.glow(0.90 * W, 0.08 * H, 0.45 * W, BYAKUGUN, 0.09)

    s, draw = canvas.s, canvas.draw

    mark.draw(draw, 80, 116, 104, scale=s)
    draw.text((s(212), s(168)), "JPCL", font=canvas.sans("Bold", 100),
              fill=TEXT, anchor="lm")

    draw.text((s(80), s(288)), "TOML’s sections.",
              font=canvas.sans("SemiBold", 40), fill=SAKURA, anchor="la")
    draw.text((s(80), s(340)), "JSON’s nesting.",
              font=canvas.sans("SemiBold", 40), fill=SAKURA, anchor="la")
    draw.text((s(80), s(410)), "A configuration language for the",
              font=canvas.sans("Regular", 26), fill=MUTED, anchor="la")
    draw.text((s(80), s(446)), "files people edit by hand.",
              font=canvas.sans("Regular", 26), fill=MUTED, anchor="la")

    draw.text((s(80), s(524)), "pip install jpcl",
              font=canvas.sans("Medium", 24), fill=MOMO, anchor="la")
    draw.text((s(310), s(524)), "npm install jpcl",
              font=canvas.sans("Medium", 24), fill=MOMO, anchor="la")

    # Sized to its six lines and centred against the left column, rather than
    # stretched to match it — the empty half of a card reads as a mistake.
    draw_code_card(canvas, 648, 149, 552, 342)

    return canvas.finish()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-o", "--output", type=Path,
                        help="where to write the PNG (default: the site's banner)")
    args = parser.parse_args()

    root = find_site_root()
    save(render(root), args.output or root / "assets" / "img" / "png" / "banner.png", root)


if __name__ == "__main__":
    main()
