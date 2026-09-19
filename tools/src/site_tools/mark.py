"""The JPCL mark, redrawn from icon.svg's own 128-unit grid.

Compositing the 128px PNG would blur the moment anything wants it larger, so the
shapes are reproduced instead. The coordinates below are lifted straight from
`jpcl-lang/assets` — keep them in step if the icon is ever redrawn.
"""

from __future__ import annotations

from PIL import ImageDraw

from .palette import MOMO, PANEL, SAKURA, STEM, TORINOKO, blend


def draw(draw_ctx: ImageDraw.ImageDraw, x: float, y: float, size: float,
         scale=lambda v: round(v)) -> None:
    """Draw the mark with its top-left at (x, y), `size` units across.

    `scale` maps a design coordinate onto the target canvas, so the caller can
    supersample without the mark needing to know about it.
    """
    u = size / 128

    def box(x0, y0, x1, y1, radius, fill):
        draw_ctx.rounded_rectangle(
            (scale(x + x0 * u), scale(y + y0 * u),
             scale(x + x1 * u), scale(y + y1 * u)),
            radius=scale(radius * u), fill=fill,
        )

    def stroke(points, width, fill):
        draw_ctx.line([(scale(x + px * u), scale(y + py * u)) for px, py in points],
                      fill=fill, width=scale(width * u), joint="curve")

    box(0, 0, 128, 128, 28, PANEL)                    # ground
    box(26, 26, 102, 44, 5, MOMO)                     # [SECTION] header
    stroke([(36, 30), (32, 30), (32, 40), (36, 40)], 3, PANEL)   # [
    stroke([(92, 30), (96, 30), (96, 40), (92, 40)], 3, PANEL)   # ]
    box(26, 56, 56, 65, 4.5, TORINOKO)                # key
    box(60.5, 55, 65.5, 60, 2.5, TORINOKO)            # the colon's two dots
    box(60.5, 61, 65.5, 66, 2.5, TORINOKO)
    stroke([(32, 72), (32, 100)], 3, STEM)            # nesting stem
    box(42, 72, 92, 81, 4.5, SAKURA)                  # nested values
    box(42, 88, 76, 97, 4.5, blend(SAKURA, PANEL, 0.65))
