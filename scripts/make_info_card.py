"""
Hand-author a neofetch-style info card SVG: a title bar, then colored
key/value rows. Each line fades and slides in on a short stagger.

Set STATIC=1 to emit a frozen (no-animation) frame for local previews.
"""

import os

STATIC = os.environ.get("STATIC") == "1"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "info-card.svg")

WIDTH = 490
LINE_H = 26
TOP_PAD = 54

# label, value, accent color
ROWS = [
    ("Now", "SWE Intern @ InfinityPool Finnotech", "#39d353"),
    ("Recent", "SWE Intern @ Mahanagar Gas Ltd (MGL)", "#69f0a0"),
    ("Track", "B.Tech Computer Engineering, AI/ML Honours - FCRIT", "#26a641"),
    ("Stack", "Python / TS / React / .NET / SQL Server / PyTorch", "#006d32"),
    ("Built", "Shankh / MGL PNG+CNG Systems / Vehicle Analytics", "#0e4429"),
    ("Focus", "Open to SWE & AI Engineering roles - grad May 2027", "#39d353"),
]

TITLE_BAR_H = 34


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_svg():
    height = TOP_PAD + len(ROWS) * LINE_H + 18

    parts = [
        f'<svg viewBox="0 0 {WIDTH} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="Consolas, Menlo, Monaco, monospace">'
    ]

    if not STATIC:
        parts.append(
            """
            <style>
              .line {
                opacity: 0;
                transform: translateX(-6px);
                animation: fadeSlide 0.4s ease-out forwards;
              }
              @keyframes fadeSlide {
                to { opacity: 1; transform: translateX(0); }
              }
            </style>
            """
        )

    # Background panel
    parts.append(
        f'<rect x="0" y="0" width="{WIDTH}" height="{height}" rx="8" ry="8" fill="#0d1117" '
        f'stroke="#30363d" stroke-width="1" />'
    )

    # Title bar with traffic-light dots
    parts.append(f'<rect x="0" y="0" width="{WIDTH}" height="{TITLE_BAR_H}" rx="8" ry="8" fill="#161b22" />')
    parts.append(f'<rect x="0" y="{TITLE_BAR_H - 8}" width="{WIDTH}" height="8" fill="#161b22" />')
    for i, dot_color in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        cx = 20 + i * 18
        parts.append(f'<circle cx="{cx}" cy="{TITLE_BAR_H / 2}" r="5" fill="{dot_color}" />')
    parts.append(
        f'<text x="{WIDTH / 2}" y="{TITLE_BAR_H / 2 + 4}" text-anchor="middle" '
        f'fill="#8b949e" font-size="12">avi@github: ~/whoami</text>'
    )

    # neofetch-style prompt line
    prompt_y = TOP_PAD - 12
    parts.append(f'<text x="20" y="{prompt_y}" fill="#39d353" font-size="13">aarya@github &gt; neofetch</text>')

    delay_step = 0.09
    for i, (label, value, color) in enumerate(ROWS):
        y = TOP_PAD + 10 + i * LINE_H
        cls = "" if STATIC else "class=\"line\" "
        style = "" if STATIC else f'style="animation-delay:{i * delay_step:.2f}s"'
        parts.append(
            f'<text {cls}x="20" y="{y}" {style} font-size="13">'
            f'<tspan fill="{color}" font-weight="bold">{esc(label)}</tspan>'
            f'<tspan fill="#8b949e">  {esc(value)}</tspan>'
            f"</text>"
        )

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    svg = build_svg()
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
