"""
Blueprint-style title block banner -- replaces the generic waving-gradient
header. Modeled on a real engineering drawing's title block: grid paper
background, corner registration ticks, drawing-number style name, and a
field strip (ROLE / STATUS / LOC / REV) like DRAWN BY / DATE / SHEET.
"""

WIDTH = 1000
HEIGHT = 190

NAVY = "#0F2A47"
PANEL = "#16324F"
TRACE = "#E7EDF3"
AMBER = "#F2A93B"
SLATE = "#7086A0"


def grid_pattern():
    return f"""
    <pattern id="gridpx" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="{SLATE}" stroke-width="0.4" opacity="0.25"/>
    </pattern>
    """


def corner_ticks():
    ticks = []
    positions = [(14, 14), (WIDTH - 14, 14), (14, HEIGHT - 14), (WIDTH - 14, HEIGHT - 14)]
    for x, y in positions:
        ticks.append(
            f'<path d="M {x-9} {y} H {x+9} M {x} {y-9} V {y+9}" stroke="{AMBER}" stroke-width="1.6" />'
        )
    return "\n".join(ticks)


def build_svg():
    parts = [
        f'<svg viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="IBM Plex Mono, Consolas, monospace">'
    ]
    parts.append(f"<defs>{grid_pattern()}</defs>")
    parts.append(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{NAVY}" />')
    parts.append(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#gridpx)" />')

    # Outer drafting frame
    parts.append(
        f'<rect x="6" y="6" width="{WIDTH-12}" height="{HEIGHT-12}" fill="none" '
        f'stroke="{SLATE}" stroke-width="1.2" />'
    )
    parts.append(corner_ticks())

    # Drawing-number eyebrow
    parts.append(
        f'<text x="34" y="42" fill="{AMBER}" font-size="12" letter-spacing="2">'
        f"SYSTEM &#8594; AARYA_MHATRE.README &#160; REV.03</text>"
    )

    # Big name, display-ish via mono at large size + letter spacing to feel drafted
    parts.append(
        f'<text x="34" y="108" fill="{TRACE}" font-size="52" font-weight="700" letter-spacing="1">'
        f"AARYA MHATRE</text>"
    )
    parts.append(
        f'<text x="36" y="138" fill="{SLATE}" font-size="15">'
        f"Computer Engineer &#160;/&#160; Systems Builder &#160;/&#160; AI + Full-Stack</text>"
    )

    # Field strip along the bottom, like a real title block's data fields
    fields = [
        ("STATUS", "OPEN TO SWE / AI ROLES"),
        ("LOC", "MUMBAI, IN"),
        ("GRAD", "MAY 2027"),
    ]
    field_w = (WIDTH - 68) / len(fields)
    fy = HEIGHT - 34
    parts.append(f'<line x1="34" y1="{fy-18}" x2="{WIDTH-34}" y2="{fy-18}" stroke="{SLATE}" stroke-width="1" opacity="0.5"/>')
    for i, (label, value) in enumerate(fields):
        fx = 34 + i * field_w
        if i > 0:
            parts.append(f'<line x1="{fx}" y1="{fy-18}" x2="{fx}" y2="{fy+10}" stroke="{SLATE}" stroke-width="1" opacity="0.5"/>')
        parts.append(f'<text x="{fx+14}" y="{fy-4}" fill="{AMBER}" font-size="10" letter-spacing="1.5">{label}</text>')
        parts.append(f'<text x="{fx+14}" y="{fy+12}" fill="{TRACE}" font-size="12">{value}</text>')

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    with open("banner-titleblock.svg", "w", encoding="utf-8") as f:
        f.write(build_svg())
    print("wrote banner-titleblock.svg")
