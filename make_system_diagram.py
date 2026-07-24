"""
The signature element: a real system-architecture / IC-style diagram.
Aarya is the central chip (AM-01); Work experiences and Projects are wired
to it and to each other, like components on a board, with pin-tick marks
on box edges and orthogonal traces. Traces draw themselves in once on
load, then boxes fade in on a stagger. No looping.
"""

WIDTH = 1000
HEIGHT = 620

NAVY = "#0F2A47"
PANEL = "#16324F"
PANEL_LIGHT = "#1D3D5F"
TRACE = "#E7EDF3"
AMBER = "#F2A93B"
SLATE = "#7086A0"
GREEN = "#5FB88A"


def pins(x, y, w, h, side_left=True, side_right=True, n=4):
    """Small tick marks along the left/right edges of a chip box."""
    out = []
    step = h / (n + 1)
    for i in range(1, n + 1):
        py = y + i * step
        if side_left:
            out.append(f'<line x1="{x-7}" y1="{py}" x2="{x}" y2="{py}" stroke="{SLATE}" stroke-width="1.4" />')
        if side_right:
            out.append(f'<line x1="{x+w}" y1="{py}" x2="{x+w+7}" y2="{py}" stroke="{SLATE}" stroke-width="1.4" />')
    return "\n".join(out)


def chip(x, y, w, h, label, sublabel, fill=PANEL, stroke=SLATE, label_color=None, delay=0.0, n_pins=3):
    label_color = label_color or TRACE
    parts = [f'<g class="chip" style="animation-delay:{delay:.2f}s">']
    parts.append(pins(x, y, w, h, n=n_pins))
    parts.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" ry="6" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.4" />'
    )
    parts.append(
        f'<text x="{x + w/2}" y="{y + h/2 - 2}" text-anchor="middle" fill="{label_color}" '
        f'font-size="14" font-weight="700" letter-spacing="0.5">{label}</text>'
    )
    parts.append(
        f'<text x="{x + w/2}" y="{y + h/2 + 16}" text-anchor="middle" fill="{SLATE}" '
        f'font-size="10">{sublabel}</text>'
    )
    parts.append("</g>")
    return "\n".join(parts)


def orthogonal_trace(x1, y1, x2, y2, delay=0.0, dashed=False, color=GREEN):
    midx = (x1 + x2) / 2
    path = f"M {x1} {y1} L {midx} {y1} L {midx} {y2} L {x2} {y2}"
    dash = 'stroke-dasharray="5 4"' if dashed else ""
    return (
        f'<path d="{path}" fill="none" stroke="{color}" stroke-width="1.8" {dash} '
        f'class="trace" style="animation-delay:{delay:.2f}s" pathLength="100" />'
    )


def build_svg():
    parts = [
        f'<svg viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="IBM Plex Mono, Consolas, monospace">'
    ]
    parts.append(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{NAVY}" />')

    # faint grid
    parts.append(
        f"""<defs><pattern id="g2" width="28" height="28" patternUnits="userSpaceOnUse">
        <path d="M 28 0 L 0 0 0 28" fill="none" stroke="{SLATE}" stroke-width="0.3" opacity="0.18"/>
        </pattern></defs>"""
    )
    parts.append(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#g2)" />')

    parts.append(
        """
        <style>
          .trace {
            stroke-dasharray: 100;
            stroke-dashoffset: 100;
            animation: draw 0.7s ease-out forwards;
          }
          @keyframes draw { to { stroke-dashoffset: 0; } }
          .chip {
            opacity: 0;
            animation: fadeUp 0.45s ease-out forwards;
          }
          @keyframes fadeUp {
            from { opacity: 0; transform: translateY(6px); }
            to   { opacity: 1; transform: translateY(0); }
          }
        </style>
        """
    )

    # eyebrow
    parts.append(
        f'<text x="30" y="34" fill="{AMBER}" font-size="12" letter-spacing="2">'
        f"FIG.1 &#8212; SYSTEM ARCHITECTURE</text>"
    )

    # --- Node coordinates ---
    cpu = dict(x=40, y=250, w=170, h=110)
    work = {
        "INFINITYPOOL": dict(x=380, y=70, w=180, h=76),
        "MGL": dict(x=380, y=270, w=180, h=76),
        "IISER MOHALI": dict(x=380, y=470, w=180, h=76),
    }
    proj = {
        "SHANKH": dict(x=730, y=40, w=220, h=70),
        "PNG-EXPANSION": dict(x=730, y=150, w=220, h=70),
        "CNG-ELIGIBILITY": dict(x=730, y=260, w=220, h=70),
        "VEHICLE-ANALYTICS": dict(x=730, y=460, w=220, h=70),
    }

    # --- Traces first (so chips draw on top) ---
    def center_right(n):
        return n["x"] + n["w"], n["y"] + n["h"] / 2

    def center_left(n):
        return n["x"], n["y"] + n["h"] / 2

    cx, cy = center_right(cpu)
    t = 0.0
    for name, n in work.items():
        wx, wy = center_left(n)
        parts.append(orthogonal_trace(cx, cy, wx, wy, delay=t))
        t += 0.08

    parts.append(orthogonal_trace(*center_right(work["INFINITYPOOL"]), *center_left(proj["SHANKH"]), delay=t)); t += 0.08
    parts.append(orthogonal_trace(*center_right(work["MGL"]), *center_left(proj["PNG-EXPANSION"]), delay=t)); t += 0.08
    parts.append(orthogonal_trace(*center_right(work["MGL"]), *center_left(proj["CNG-ELIGIBILITY"]), delay=t)); t += 0.08
    # independent/personal project: dashed trace direct from CPU
    parts.append(orthogonal_trace(*center_right(cpu), *center_left(proj["VEHICLE-ANALYTICS"]), delay=t, dashed=True, color=AMBER)); t += 0.08

    # --- Chips ---
    chip_delay = t + 0.05
    parts.append(chip(cpu["x"], cpu["y"], cpu["w"], cpu["h"], "AM-01", "CORE // AARYA MHATRE",
                       fill=PANEL_LIGHT, stroke=AMBER, label_color=AMBER, delay=chip_delay, n_pins=4))
    chip_delay += 0.08

    sub = {
        "INFINITYPOOL": "SWE INTERN // JUN'25\u2013PRESENT",
        "MGL": "SWE INTERN // JUN\u2013JUL'26",
        "IISER MOHALI": "ML INTERN // 15D",
    }
    for name, n in work.items():
        parts.append(chip(n["x"], n["y"], n["w"], n["h"], name, sub[name], delay=chip_delay, n_pins=3))
        chip_delay += 0.08

    psub = {
        "SHANKH": "WEBAR + RAG + WHISPER",
        "PNG-EXPANSION": "GIS + LEAFLET + GEMINI",
        "CNG-ELIGIBILITY": "ASP.NET + SQL SERVER",
        "VEHICLE-ANALYTICS": "YOLOV5 + OPENCV // 92%+",
    }
    for name, n in proj.items():
        parts.append(chip(n["x"], n["y"], n["w"], n["h"], name, psub[name], delay=chip_delay, n_pins=3))
        chip_delay += 0.08

    # legend, bottom-left
    ly = HEIGHT - 30
    parts.append(f'<circle cx="34" cy="{ly}" r="4" fill="{GREEN}" />')
    parts.append(f'<text x="46" y="{ly+4}" fill="{SLATE}" font-size="11">EMPLOYMENT-DERIVED</text>')
    parts.append(f'<circle cx="220" cy="{ly}" r="4" fill="{AMBER}" />')
    parts.append(f'<text x="232" y="{ly+4}" fill="{SLATE}" font-size="11">INDEPENDENT / PERSONAL</text>')

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    with open("system-diagram.svg", "w", encoding="utf-8") as f:
        f.write(build_svg())
    print("wrote system-diagram.svg")
