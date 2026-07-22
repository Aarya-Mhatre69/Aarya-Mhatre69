"""
Render data/contributions.json as a 53-week x 7-day GitHub-style heatmap SVG.

Boxes reveal with a diagonal, line-after-line slide-down (CSS keyframes that
play once on load, then freeze -- no infinite looping "glow"). Output:
contrib-heatmap.svg at the repo root.
"""

import json
import os
from datetime import datetime

PALETTE = [
    "#161b22",  # 0 - none
    "#0e4429",  # 1
    "#006d32",  # 2
    "#26a641",  # 3
    "#39d353",  # 4
    "#69f0a0",  # 5 - neon top end
]

BOX = 11
GAP = 3
CELL = BOX + GAP
LEFT_PAD = 28
TOP_PAD = 36
FOOTER_H = 34

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "contrib-heatmap.svg")


def week_columns(days):
    """Bucket days into GitHub-style Sunday-start week columns."""
    parsed = []
    for d in days:
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        parsed.append((dt, d["level"]))
    parsed.sort(key=lambda x: x[0])

    weeks = []
    current_week = [None] * 7
    for dt, level in parsed:
        dow = (dt.weekday() + 1) % 7  # Mon=0 -> shift so Sun=0
        if dow == 0 and any(c is not None for c in current_week):
            weeks.append(current_week)
            current_week = [None] * 7
        current_week[dow] = (dt, level)
    if any(c is not None for c in current_week):
        weeks.append(current_week)
    return weeks[-53:]


def month_labels(weeks):
    labels = []
    seen_month = None
    for i, week in enumerate(weeks):
        for cell in week:
            if cell is None:
                continue
            dt, _ = cell
            m = dt.strftime("%b")
            if m != seen_month:
                labels.append((i, m))
                seen_month = m
            break
    return labels


def build_svg(payload):
    days = payload["days"]
    stats = payload["stats"]
    weeks = week_columns(days)
    n_weeks = len(weeks)

    width = LEFT_PAD + n_weeks * CELL + 140  # room for legend on the right
    height = TOP_PAD + 7 * CELL + FOOTER_H

    parts = []
    parts.append(
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">'
    )
    parts.append(
        """
        <style>
          .cell {
            opacity: 0;
            transform: translate(0, -6px);
            animation: dropIn 0.5s ease-out forwards;
          }
          @keyframes dropIn {
            to { opacity: 1; transform: translate(0, 0); }
          }
          .month-label { fill: #8b949e; font-size: 10px; }
          .legend-label { fill: #8b949e; font-size: 9px; }
          .footer { fill: #c9d1d9; font-size: 12px; }
        </style>
        """
    )

    # Month labels
    for week_idx, label in month_labels(weeks):
        x = LEFT_PAD + week_idx * CELL
        parts.append(f'<text class="month-label" x="{x}" y="{TOP_PAD - 12}">{label}</text>')

    # Day boxes, staggered diagonally: delay grows with (week_idx + day_idx)
    delay_step = 0.012
    for week_idx, week in enumerate(weeks):
        for day_idx in range(7):
            cell = week[day_idx]
            level = cell[1] if cell else 0
            x = LEFT_PAD + week_idx * CELL
            y = TOP_PAD + day_idx * CELL
            delay = (week_idx + day_idx) * delay_step
            color = PALETTE[min(level, 5)]
            parts.append(
                f'<rect class="cell" x="{x}" y="{y}" width="{BOX}" height="{BOX}" rx="2" ry="2" '
                f'fill="{color}" style="animation-delay:{delay:.3f}s" />'
            )

    # Legend: Less -> More
    legend_x = LEFT_PAD + n_weeks * CELL + 14
    legend_y = TOP_PAD
    parts.append(f'<text class="legend-label" x="{legend_x}" y="{legend_y + BOX - 1}">Less</text>')
    swatch_x = legend_x + 34
    for i, color in enumerate(PALETTE):
        sx = swatch_x + i * (BOX + 2)
        parts.append(f'<rect x="{sx}" y="{legend_y}" width="{BOX}" height="{BOX}" rx="2" ry="2" fill="{color}" />')
    parts.append(
        f'<text class="legend-label" x="{swatch_x + len(PALETTE) * (BOX + 2) + 4}" '
        f'y="{legend_y + BOX - 1}">More</text>'
    )

    # Footer stats
    footer_y = TOP_PAD + 7 * CELL + 22
    total = stats["total_contributions"]
    streak = stats["longest_streak"]
    footer_text = f"{total} contributions in the last year  \u00b7  longest streak {streak} days"
    parts.append(f'<text class="footer" x="{LEFT_PAD}" y="{footer_y}">{footer_text}</text>')

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        payload = json.load(f)

    svg = build_svg(payload)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
