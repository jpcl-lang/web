"""The brand palette, in one place.

These are the same values the stylesheet carries and the assets repo documents,
kept here so generated images cannot drift from the site. Traditional names are
on every colour that has one.
"""

from __future__ import annotations

RGB = tuple[int, int, int]


def hex_to_rgb(value: str) -> RGB:
    value = value.lstrip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def blend(fg: RGB, bg: RGB, alpha: float) -> RGB:
    """Flatten `fg` at `alpha` over an opaque `bg`."""
    return tuple(round(b + (f - b) * alpha) for f, b in zip(fg, bg))


# Surfaces ------------------------------------------------------------------

BG = hex_to_rgb("#192236")        # 紺 kon, the page
PANEL = hex_to_rgb("#0F2540")     # 紺 kon, the icon ground: code and cards

# The five --------------------------------------------------------------------

KON = hex_to_rgb("#0F2540")
MOMO = hex_to_rgb("#F596AA")
SAKURA = hex_to_rgb("#FEDFE1")
KURENAI = hex_to_rgb("#CB1B45")
TORINOKO = hex_to_rgb("#DAC9A6")

# The three that cover what the five do not -----------------------------------

BYAKUGUN = hex_to_rgb("#83CCD2")  # 白群, numbers
FUJI = hex_to_rgb("#A99CD6")      # 藤, lightened: keywords
AINEZU = hex_to_rgb("#6E7B8B")    # 藍鼠, the blue-grey the neutrals come from

# Ink, on the dark surfaces ---------------------------------------------------

TEXT = hex_to_rgb("#E7EEF7")
MUTED = hex_to_rgb("#9DB0C6")
PUNCT = hex_to_rgb("#8FA3BC")
COMMENT = hex_to_rgb("#8496AD")
STEM = hex_to_rgb("#3A5577")      # the icon's own nesting stem

# A hairline, as RGBA: rgb(154 182 214 / 16%) in the stylesheet.
LINE = (0x9A, 0xB6, 0xD6, 0x2B)
