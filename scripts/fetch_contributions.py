import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

USERNAME = "JoeyGirdhar"
OUT = os.path.join("data", "contributions.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "X-Requested-With": "XMLHttpRequest",
}


def fetch_html(username):
    url = "https://github.com/users/" + username + "/contributions"
    print("Fetching " + url)
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")

    tips = {}
    for tip in soup.find_all("tool-tip"):
        target = tip.get("for")
        if not target:
            continue
        m = re.search(r"(\d[\d,]*)\s+contribution", tip.get_text())
        tips[target] = int(m.group(1).replace(",", "")) if m else 0

    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        cells = soup.select("rect.ContributionCalendar-day")

    days = []
    for cell in cells:
        d = cell.get("data-date")
        if not d:
            continue
        level = int(cell.get("data-level") or 0)
        count = tips.get(cell.get("id"), 0)
        if count == 0 and level > 0:
            count = level
        days.append({"date": d, "count": count, "level": level})

    days.sort(key=lambda x: x["date"])
    return days


def stats(days):
    total = sum(d["count"] for d in days)

    longest = 0
    current = 0
    for d in days:
        if d["count"] > 0:
            current += 1
            if current > longest:
                longest = current
        else:
            current = 0

    streak = 0
    for d in reversed(days):
        if d["count"] > 0:
            streak += 1
        else:
            break

    best = {"date": "", "count": 0}
    for d in days:
        if d["count"] > best["count"]:
            best = d

    monthly = {}
    for d in days:
        key = d["date"][:7]
        monthly[key] = monthly.get(key, 0) + d["count"]

    return {
        "total": total,
        "current_streak": streak,
        "longest_streak": longest,
        "best_day": best,
        "monthly": monthly,
    }


def main():
    html = fetch_html(USERNAME)
    days = parse(html)

    if len(days) < 300:
        print("")
        print("ERROR: only captured " + str(len(days)) + " day cells - expected around 365.")
        print("Check that the username is spelled right and the profile is public.")
        print("Not overwriting data/contributions.json with bad data.")
        return 1

    payload = {"username": USERNAME, "days": days, "stats": stats(days)}

    os.makedirs("data", exist_ok=True)
    f = open(OUT, "w", encoding="utf-8", newline="\n")
    json.dump(payload, f, indent=2)
    f.write("\n")
    f.close()

    print("Captured " + str(len(days)) + " days, " + format(payload["stats"]["total"], ",") + " contributions.")
    print("Range: " + days[0]["date"] + " to " + days[-1]["date"])
    return 0


if __name__ == "__main__":
    sys.exit(main())