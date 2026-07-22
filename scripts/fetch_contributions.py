"""
Fetch a GitHub user's public contribution calendar with no API token.

GitHub serves the same HTML fragment used on the profile page at:
    https://github.com/users/<username>/contributions

We parse the day cells with BeautifulSoup and write data/contributions.json
with the raw per-day data plus a few derived stats (streaks, best day,
monthly totals) that the info card / heatmap footer can use.
"""

import json
import os
import sys
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_USERNAME", "Aarya-Mhatre69")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")


def fetch_days():
    headers = {"User-Agent": "profile-readme-bot"}
    resp = requests.get(URL, headers=headers, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    days = []
    # GitHub renders each day as a <td> with class "ContributionCalendar-day"
    # and data-date / data-level attributes (levels 0-4).
    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        # Fallback: some markup versions use <rect> tiles instead of <td>.
        cells = soup.select("rect.ContributionCalendar-day")

    for cell in cells:
        date_str = cell.get("data-date")
        level = cell.get("data-level")
        if date_str is None or level is None:
            continue
        days.append({"date": date_str, "level": int(level)})

    days.sort(key=lambda d: d["date"])
    return days


def derive_stats(days):
    total = sum(1 for d in days if d["level"] > 0)

    # Current streak: consecutive contributing days ending today (or the
    # most recent day in the data).
    current_streak = 0
    for d in reversed(days):
        if d["level"] > 0:
            current_streak += 1
        else:
            break

    # Longest streak anywhere in the window.
    longest_streak = 0
    running = 0
    best_day = None
    best_level = -1
    monthly_totals = {}

    for d in days:
        if d["level"] > 0:
            running += 1
            longest_streak = max(longest_streak, running)
        else:
            running = 0

        if d["level"] > best_level:
            best_level = d["level"]
            best_day = d["date"]

        month_key = d["date"][:7]  # YYYY-MM
        monthly_totals[month_key] = monthly_totals.get(month_key, 0) + (1 if d["level"] > 0 else 0)

    return {
        "total_contributions": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "monthly_totals": monthly_totals,
    }


def main():
    try:
        days = fetch_days()
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to fetch contributions: {exc}", file=sys.stderr)
        sys.exit(1)

    if not days:
        print("No contribution cells parsed — GitHub markup may have changed.", file=sys.stderr)
        sys.exit(1)

    payload = {
        "username": USERNAME,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "days": days,
        "stats": derive_stats(days),
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(days)} days to {OUT_PATH}")


if __name__ == "__main__":
    main()
