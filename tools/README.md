# jpcl-site-tools

Generators for the images the site cannot express as CSS. Everything here reads
its colours from `site_tools.palette`, so the output cannot drift from the
stylesheet or from the [brand assets](https://github.com/jpcl-lang/assets).

```bash
uv run --project tools banner              # -> assets/img/png/banner.png
uv run --project tools banner -o out.png   # somewhere else, to compare
```

The script finds the site by walking up to the folder holding `index.html`, so
the working directory does not matter.

| Module | |
| --- | --- |
| `palette.py` | The brand colours, with their traditional names. |
| `mark.py` | The JPCL mark, redrawn from `icon.svg`'s 128-unit grid. |
| `banner.py` | The 1280×640 Open Graph card. |

The mark is redrawn rather than composited from `icon.png`, which is only 128px
and blurs the moment anything wants it larger. Its coordinates come straight
from `icon.svg` — if the icon is ever redrawn, `mark.py` has to follow.

`banner.py` needs IBM Plex Sans in `assets/fonts` (the site ships it) and a
system monospace face for the code sample: Cascadia Mono, Consolas, DejaVu Sans
Mono or Menlo, whichever it finds first.
