"""Render every generated image in one go.

    uv run --project tools images
"""

from __future__ import annotations

from pathlib import Path

from . import banner, square
from .render import find_site_root, save

TARGETS = (
    (banner, "banner.png"),
    (square, "square.png"),
)


def main() -> None:
    root = find_site_root()
    for module, name in TARGETS:
        save(module.render(root), root / "assets" / "img" / "png" / name, root)


if __name__ == "__main__":
    main()
