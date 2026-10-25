#!/usr/bin/env python3
# Update the compact GitHub public-repository insights SVG (stdlib only).
import json, os, html, urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

USERNAME = "GrimVeqsum"
API = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "GrimVeqsum-profile-insights"}
if os.environ.get("GITHUB_TOKEN"):
    HEADERS["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]

def get(path):
    req = urllib.request.Request(API+path, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.load(response)

user = get("/users/" + USERNAME)
repos = []
page=1
while True:
    result = get(f"/users/{USERNAME}/repos?type=owner&per_page=100&page={page}")
    if not result:
        break
    repos.extend(r for r in result if not r.get("private") and not r.get("fork"))
    if len(result)<100:
        break
    page += 1

n = len(repos)
stars = sum(r.get("stargazers_count", 0) for r in repos)
counts = Counter(r["language"] for r in repos if r.get("language"))
top = counts.most_common(3)
now = datetime.now(timezone.utc).strftime("%d %b %Y")

def bar(x, y, label, val, shade):
    maxcount=max((k for _,k in top),default=1)
    length= int(370*val/maxcount)
    return f'''<text x="{x}" y="{y}" fill="#d3e2f2" font-size="24" font-family="DejaVu Sans,Arial,sans-serif">{html.escape(label)}</text><text x="{x+370}" y="{y}" text-anchor="end" fill="#9fb7d0" font-size="22" font-family="DejaVu Sans,Arial,sans-serif">{val} repos</text><rect x="{x}" y="{y+15}" width="370" height="9" rx="4" fill="#1d3047"/><rect x="{x}" y="{y+15}" width="{length}" height="9" rx="4" fill="{shade}"/>'''
colors=["#64b9ff", "#5dd6c9", "#e6aa7e"]
rows = ''.join(bar(945, 70+i*64, lang, val,colors[i]) for i,(lang,val) in enumerate(top))
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="260" viewBox="0 0 1400 260" role="img" aria-label="Public GitHub insights: {n} public repositories, {stars} stars; language bars count repositories by primary language">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#101e2e"/><stop offset="1" stop-color="#0b1421"/></linearGradient></defs>
<rect x="1" y="1" width="1398" height="258" rx="19" fill="url(#bg)" stroke="#2b3c52" stroke-width="2"/>
<text x="35" y="42" fill="#90abc5" font-size="20" font-family="DejaVu Sans,Arial,sans-serif" letter-spacing="2.5">PUBLIC REPOSITORIES</text><text x="40" y="140" fill="#f0f6ff" font-size="83" font-weight="700" font-family="DejaVu Sans,Arial,sans-serif">{n:02}</text>
<text x="40" y="199" fill="#a8c0d9" font-size="24" font-family="DejaVu Sans,Arial,sans-serif">non-fork projects</text>
<path d="M290 55 V214" stroke="#293e55" stroke-width="2"/>
<text x="330" y="42" fill="#90abc5" font-size="20" font-family="DejaVu Sans,Arial,sans-serif" letter-spacing="2.5">TOTAL STARS</text><text x="333" y="140" fill="#f0f6ff" font-size="83" font-weight="700" font-family="DejaVu Sans,Arial,sans-serif">{stars}</text>
<text x="333" y="199" fill="#a8c0d9" font-size="24" font-family="DejaVu Sans,Arial,sans-serif">across public repos</text>
<path d="M595 55 V214" stroke="#293e55" stroke-width="2"/>
<text x="635" y="42" fill="#90abc5" font-size="20" font-family="DejaVu Sans,Arial,sans-serif" letter-spacing="2.5">SELECTED WORK</text><text x="638" y="140" fill="#f0f6ff" font-size="83" font-weight="700" font-family="DejaVu Sans,Arial,sans-serif">04</text>
<text x="638" y="199" fill="#a8c0d9" font-size="24" font-family="DejaVu Sans,Arial,sans-serif">featured projects</text>
<path d="M905 55 V214" stroke="#293e55" stroke-width="2"/>
<text x="945" y="42" fill="#90abc5" font-size="20" font-family="DejaVu Sans,Arial,sans-serif" letter-spacing="2.5">TOP PRIMARY LANGUAGES</text>
{rows}
<text x="1360" y="244" fill="#647f98" text-anchor="end" font-size="15" font-family="DejaVu Sans,Arial,sans-serif">Updated {html.escape(now)} UTC</text>
</svg>'''
Path("assets/github-insights.svg").write_text(svg, encoding="utf-8")
print(f"Updated: public non-fork repos={n}, stars={stars}, languages={top}")
