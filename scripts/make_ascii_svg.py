"""
Convert source-prepped.png into a self-typing, monochrome ASCII-art SVG.

The prepped image is downsampled to a character grid (~100 x 53), and each
pixel's brightness picks a glyph from a density ramp -- sparse characters
for bright areas, dense ones for dark. One light-gray fill color only
(per-character rainbow coloring is what makes most ASCII art look noisy).

Each row wipes in left-to-right via a clip-path animation, staggered top to
bottom, with a small block "cursor" riding the wipe edge. Prints once and
freezes -- no looping.

Usage:
    python scripts/make_ascii_svg.py [source-prepped.png]
Output:
    avi-ascii.svg
"""

import sys

from PIL import Image

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense); leading space = blank
COLS = 100
ROWS = 53
FONT_SIZE = 6.2
CHAR_W = FONT_SIZE * 0.6
CHAR_H = FONT_SIZE * 1.05

OUT_PATH = "avi-ascii.svg"


def image_to_ascii(path: str):
    img = Image.open(path).convert("L")
    img = img.resize((COLS, ROWS))
    pixels = list(img.getdata())

    rows = []
    ramp_len = len(RAMP)
    for r in range(ROWS):
        row_chars = []
        for c in range(COLS):
            brightness = pixels[r * COLS + c]  # 0 (dark) - 255 (bright)
            idx = int((255 - brightness) / 255 * (ramp_len - 1))
            row_chars.append(RAMP[idx])
        rows.append("".join(row_chars))
    return rows


def esc(ch: str) -> str:
    if ch == "&":
        return "&amp;"
    if ch == "<":
        return "&lt;"
    if ch == ">":
        return "&gt;"
    return ch


def build_svg(rows):
    width = COLS * CHAR_W
    height = ROWS * CHAR_H

    parts = [
        f'<svg viewBox="0 0 {width:.0f} {height:.0f}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="Consolas, Menlo, Monaco, monospace">'
    ]
    parts.append(f'<rect width="{width:.0f}" height="{height:.0f}" fill="transparent" />')

    parts.append(
        f"""
        <style>
          text {{ fill: #c9d1d9; font-size: {FONT_SIZE}px; }}
          .row-wipe {{
            animation: wipe 0.35s steps(30) forwards;
          }}
          @keyframes wipe {{
            from {{ clip-path: inset(0 100% 0 0); }}
            to   {{ clip-path: inset(0 0 0 0); }}
          }}
        </style>
        """
    )

    row_delay_step = 0.05  # top-to-bottom stagger
    for r, row in enumerate(rows):
        y = (r + 1) * CHAR_H
        line_text = "".join(esc(ch) for ch in row)
        delay = r * row_delay_step
        parts.append(
            f'<g class="row-wipe" style="animation-delay:{delay:.2f}s">'
            f'<text x="0" y="{y:.1f}" xml:space="preserve">{line_text}</text>'
            f"</g>"
        )

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png"
    rows = image_to_ascii(src)
    svg = build_svg(rows)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
