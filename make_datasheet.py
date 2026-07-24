"""
A component-datasheet panel in the same blueprint language as the system
diagram -- reads like a real IC datasheet's spec table instead of a
neofetch/terminal card. Rows fade in on a short stagger, then hold.
"""

import os

STATIC = os.environ.get("STATIC") == "1"

NAVY = "#0F2A47"
PANEL = "#16324F"
TRACE = "#E7EDF3"
AMBER = "#F2A93B"
SLATE = "#7086A0"
GREEN = "#5FB88A"

WIDTH = 520
ROW_H = 30
TOP_PAD = 78

ROWS = [
    ("PACKAGE", "B.Tech, Computer Engineering (AI/ML Hons.) \u2014 FCRIT"),
    ("GPA", "9.14 / 10.0"),
    ("CORE LANG", "Python, TypeScript, C, SQL"),
    ("OP. MODE", "Backend \u00b7 AI/RAG \u00b7 GIS dashboards \u00b7 Full-stack"),
    ("CURRENT ROLE", "SWE Intern @ InfinityPool Finnotech"),
    ("STATUS", "OPEN TO SWE / AI ENGINEERING ROLES"),
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg():
    height = TOP_PAD + len(ROWS) * ROW_H + 24

    parts = [
        f'<svg viewBox="0 0 {WIDTH} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="IBM Plex Mono, Consolas, monospace">'
    ]

    if not STATIC:
        parts.append(
            """
            <style>
              .row { opacity: 0; animation: fadeIn 0.4s ease-out forwards; }
              @keyframes fadeIn { to { opacity: 1; } }
            </style>
            """
        )

    parts.append(f'<rect width="{WIDTH}" height="{height}" rx="8" ry="8" fill="{NAVY}" stroke="{SLATE}" stroke-width="1.2" />')

    # header strip
    parts.append(f'<rect x="0" y="0" width="{WIDTH}" height="48" rx="8" ry="8" fill="{PANEL}" />')
    parts.append(f'<rect x="0" y="40" width="{WIDTH}" height="8" fill="{PANEL}" />')
    parts.append(f'<text x="20" y="30" fill="{AMBER}" font-size="13" letter-spacing="2">AM-01 &#8212; DATASHEET</text>')
    parts.append(f'<circle cx="{WIDTH-24}" cy="24" r="5" fill="{GREEN}" />')

    header_y = 66
    parts.append(f'<text x="20" y="{header_y}" fill="{SLATE}" font-size="10" letter-spacing="1.5">FIELD</text>')
    parts.append(f'<text x="160" y="{header_y}" fill="{SLATE}" font-size="10" letter-spacing="1.5">VALUE</text>')
    parts.append(f'<line x1="20" y1="{header_y+8}" x2="{WIDTH-20}" y2="{header_y+8}" stroke="{SLATE}" stroke-width="0.8" opacity="0.5"/>')

    delay_step = 0.09
    for i, (label, value) in enumerate(ROWS):
        y = TOP_PAD + i * ROW_H
        cls = "" if STATIC else 'class="row" '
        style = "" if STATIC else f'style="animation-delay:{i*delay_step:.2f}s"'
        parts.append(f'<g {cls}{style}>')
        parts.append(f'<text x="20" y="{y}" fill="{AMBER}" font-size="11" font-weight="700">{esc(label)}</text>')
        parts.append(f'<text x="160" y="{y}" fill="{TRACE}" font-size="11">{esc(value)}</text>')
        if i < len(ROWS) - 1:
            parts.append(f'<line x1="20" y1="{y+10}" x2="{WIDTH-20}" y2="{y+10}" stroke="{SLATE}" stroke-width="0.5" opacity="0.25"/>')
        parts.append("</g>")

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    with open("datasheet.svg", "w", encoding="utf-8") as f:
        f.write(build_svg())
    print("wrote datasheet.svg")
