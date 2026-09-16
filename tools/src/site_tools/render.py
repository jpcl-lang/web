"""Canvas plumbing shared by the image generators.

Everything is drawn at `SS` times the final size and downsampled at the end,
which is cheaper than chasing antialiasing by hand. `Canvas.s()` maps a 1x
design coordinate onto that larger surface, so the drawing code stays written in
the dimensions it is designed in.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SS = 2  # supersampling factor

MONO_CANDIDATES = (
    "C:/Windows/Fonts/CascadiaMono.ttf",
    "C:/Windows/Fonts/consola.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/System/Library/Fonts/Menlo.ttc",
)


def find_site_root() -> Path:
    """Walk up until the folder holding index.html, so cwd does not matter."""
    for folder in Path(__file__).resolve().parents:
        if (folder / "index.html").exists():
            return folder
    raise SystemExit("could not find the site root (no index.html above this file)")


class Canvas:
    """A supersampled RGBA surface with the site's fonts attached."""

    def __init__(self, width: int, height: int, background, root: Path | None = None):
        self.width = width
        self.height = height
        self.root = root or find_site_root()
        self.image = Image.new("RGBA", (self.s(width), self.s(height)),
                               tuple(background) + (255,))
        self._draw: ImageDraw.ImageDraw | None = None

    def s(self, value: float) -> int:
        return round(value * SS)

    @property
    def draw(self) -> ImageDraw.ImageDraw:
        if self._draw is None:
            self._draw = ImageDraw.Draw(self.image)
        return self._draw

    def sans(self, weight: str, size: float) -> ImageFont.FreeTypeFont:
        path = self.root / "assets" / "fonts" / f"IBMPlexSans-{weight}.ttf"
        if not path.exists():
            raise SystemExit(f"missing font: {path}")
        return ImageFont.truetype(str(path), self.s(size))

    def mono(self, size: float) -> ImageFont.FreeTypeFont:
        for candidate in MONO_CANDIDATES:
            if Path(candidate).exists():
                return ImageFont.truetype(candidate, self.s(size))
        raise SystemExit("no monospace font found; add one to MONO_CANDIDATES")

    def glow(self, cx: float, cy: float, radius: float, colour,
             strength: float, res: int = 96) -> None:
        """Lay down a soft radial wash, echoing the two the hero paints in CSS.

        Glows must go on before anything else is drawn: compositing replaces the
        surface, so any drawing context taken earlier would be left behind.
        """
        mask = Image.new("L", (res, res), 0)
        pixels = mask.load()
        for y in range(res):
            for x in range(res):
                fx = (x + 0.5) / res * self.width
                fy = (y + 0.5) / res * self.height
                fade = max(0.0, 1.0 - math.hypot(fx - cx, fy - cy) / radius)
                pixels[x, y] = round(255 * fade ** 2 * strength)

        size = (self.s(self.width), self.s(self.height))
        layer = Image.new("RGBA", size, tuple(colour) + (0,))
        layer.putalpha(mask.resize(size, Image.BICUBIC))

        self.image = Image.alpha_composite(self.image, layer)
        self._draw = None

    def spans(self, x: float, y: float, runs, font, anchor: str = "la") -> None:
        """Draw coloured runs of text on one line, laid end to end."""
        pen = self.s(x)
        for text, colour in runs:
            self.draw.text((pen, self.s(y)), text, font=font, fill=colour, anchor=anchor)
            pen += round(self.draw.textlength(text, font=font))

    def finish(self) -> Image.Image:
        return self.image.convert("RGB").resize((self.width, self.height), Image.LANCZOS)


def save(image: Image.Image, out: Path, root: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out, optimize=True)
    shown = out.relative_to(root) if out.is_relative_to(root) else out
    print(f"wrote {shown}  {image.width}x{image.height}  "
          f"{out.stat().st_size / 1024:.0f} KB")
