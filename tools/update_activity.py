#!/usr/bin/env python3

import calendar
import html
import json
import os
import urllib.error
import urllib.parse
import urllib.request

from datetime import datetime, timezone
from pathlib import Path

USER = "GrimVeqsum"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "GrimVeqsum-profile-activity",
    "X-GitHub-Api-Version": "2022-11-28",
}

token = os.environ.get("GITHUB_TOKEN")

if token:
    HEADERS["Authorization"] = f"Bearer {token}"


def month_offset(today, delta):
    index = today.year * 12 + today.month - 1 + delta
    year, month = divmod(index, 12)
    return year, month + 1



def count_contributions_by_month(months, today):
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required")

    first_year, first_month = months[0]

    start_date = datetime(
        first_year, first_month, 1, tzinfo=timezone.utc
    ).isoformat()

    end_date = datetime.now(timezone.utc).isoformat()

    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """

    payload = json.dumps({
        "query": query,
        "variables": {
            "login": USER,
            "from": start_date,
            "to": end_date,
        },
    }).encode("utf-8")

    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={**HEADERS, "Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"GitHub API error {error.code}: {details[:400]}"
        ) from error

    if result.get("errors"):
        raise RuntimeError(str(result["errors"]))

    calendar_data = (
        result["data"]["user"]
        ["contributionsCollection"]
        ["contributionCalendar"]
    )

    counts = dict.fromkeys(months, 0)

    for week in calendar_data["weeks"]:
        for day in week["contributionDays"]:
            date = datetime.strptime(day["date"], "%Y-%m-%d").date()
            key = (date.year, date.month)

            if key in counts and date <= today:
                counts[key] += day["contributionCount"]

    return [counts[month] for month in months]


def generate_svg(months, counts, today):
    total = sum(counts)
    maximum = max(1, max(counts))

    start = f"{months[0][0]}-{months[0][1]:02d}"
    end = f"{months[-1][0]}-{months[-1][1]:02d}"

    svg = ["""<svg xmlns="http://www.w3.org/2000/svg"
width="1400" height="410" viewBox="0 0 1400 410">

<defs>
  <linearGradient id="background" x1="0" y1="0" x2="1" y2="1">
    <stop stop-color="#101e2e"/>
    <stop offset="1" stop-color="#0b1421"/>
  </linearGradient>

  <linearGradient id="bar" x1="0" y1="1" x2="0" y2="0">
    <stop stop-color="#347aa9"/>
    <stop offset="1" stop-color="#69c6ee"/>
  </linearGradient>
</defs>

<rect x="1" y="1" width="1398" height="408" rx="19"
fill="url(#background)" stroke="#2b3c52" stroke-width="2"/>

<text x="45" y="61" fill="#eff6ff"
font-family="Arial" font-size="30" font-weight="700">
GitHub contribution activity
</text>
"""]

    svg.append(
        f'<text x="45" y="93" fill="#8fa9c3" '
        f'font-family="Arial" font-size="20">'
        f'{start} – {end} · monthly totals</text>'
    )

    svg.append(
        f'<text x="1350" y="61" text-anchor="end" '
        f'fill="#a4dafa" font-family="Arial" '
        f'font-size="29" font-weight="700">'
        f'{total} contributions</text>'
    )

    svg.append(
        '<text x="1350" y="92" text-anchor="end" '
        'fill="#8fa9c3" font-family="Arial" font-size="19">'
        'Last 12 calendar months</text>'
    )

    left = 78
    right = 1352
    top = 130
    bottom = 317

    for i in range(5):
        y = bottom - (bottom - top) * i / 4

        svg.append(
            f'<line x1="{left}" y1="{y:.1f}" '
            f'x2="{right}" y2="{y:.1f}" '
            f'stroke="#263a50" stroke-width="1"/>'
        )

    step = (right - left) / 12

    for index, ((year, month), count) in enumerate(zip(months, counts)):
        x = left + step * (index + 0.5)
        height = (bottom - top) * count / maximum

        if count > 0:
            y = bottom - height

            svg.append(
                f'<rect x="{x-26:.1f}" y="{y:.1f}" '
                f'width="52" height="{height:.1f}" '
                f'rx="6" fill="url(#bar)"/>'
            )

            svg.append(
                f'<text x="{x:.1f}" y="{max(117, y-11):.1f}" '
                f'text-anchor="middle" fill="#d9edfc" '
                f'font-family="Arial" font-size="19">'
                f'{count}</text>'
            )

        label = html.escape(calendar.month_abbr[month])

        svg.append(
            f'<text x="{x:.1f}" y="352" '
            f'text-anchor="middle" fill="#bdcde0" '
            f'font-family="Arial" font-size="21">'
            f'{label}</text>'
        )

        svg.append(
            f'<text x="{x:.1f}" y="374" '
            f'text-anchor="middle" fill="#66839f" '
            f'font-family="Arial" font-size="15">'
            f'{str(year)[2:]}</text>'
        )

    updated = today.strftime("%d %b %Y")

    svg.append(
        f'<text x="1350" y="397" text-anchor="end" '
        f'fill="#7491ad" font-family="Arial" font-size="16">'
        f'Updated {updated} UTC · Current month is partial'
        f'</text>'
    )

    svg.append("</svg>")

    return "\n".join(svg) + "\n"


def main():
    today = datetime.now(timezone.utc).date()

    months = [
        month_offset(today, delta)
        for delta in range(-11, 1)
    ]

    counts = count_contributions_by_month(months, today)

    result = generate_svg(months, counts, today)

    output = Path("assets/monthly-contributions.svg")
    output.write_text(result, encoding="utf-8")

    print("GitHub contributions by month:")

    for (year, month), count in zip(months, counts):
        print(f"{year}-{month:02d}: {count}")

    print(f"\nTotal: {sum(counts)}")
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
