import datetime as dt
import json
import os
import sys

DATA = os.path.join("data", "contributions.json")
OUT = "contrib-heatmap.svg"

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

CELL = 12
GAP = 3
PITCH = CELL + GAP
GUTTER = 30
TOP = 22
PAD = 14
WEEKS = 53
FOOTER = 44

WIDTH = PAD * 2 + GUTTER + WEEKS * PITCH
HEIGHT = PAD * 2 + TOP + 7 * PITCH + FOOTER

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def esc(s):
    s = str(s)
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    return s


def build_grid(days):
    by_date = {}
    for d in days:
        by_date[d["date"]] = d

    if not by_date:
        raise SystemExit("No days found in contributions.json")

    last_dt = dt.date.fromisoformat(max(by_date))
    end_of_week = last_dt + dt.timedelta(days=(6 - last_dt.weekday()) % 7)
    start = end_of_week - dt.timedelta(days=WEEKS * 7 - 1)
    start = start - dt.timedelta(days=(start.weekday() + 1) % 7)

    grid = []
    for w in range(WEEKS):
        col = []
        for wd in range(7):
            day = start + dt.timedelta(days=w * 7 + wd)
            col.append((day, by_date.get(day.isoformat())))
        grid.append(col)
    return grid


def render(payload):
    days = payload["days"]
    total = payload.get("stats", {}).get("total")
    if total is None:
        total = sum(d.get("count", 0) for d in days)

    grid = build_grid(days)
    parts = []

    parts.append(
        '<svg xmlns="http://www.w3.org/2000/svg" width="' + str(WIDTH) +
        '" height="' + str(HEIGHT) + '" viewBox="0 0 ' + str(WIDTH) + ' ' + str(HEIGHT) +
        '" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        'role="img" aria-label="GitHub contribution graph">'
    )

    parts.append("<style>")
    parts.append(
        ".box { opacity: 0; transform-box: fill-box; transform-origin: center; "
        "animation: pop .38s ease-out forwards; } "
        "@keyframes pop { from { opacity: 0; transform: translateY(-6px) scale(.55); } "
        "to { opacity: 1; transform: translateY(0) scale(1); } } "
        ".lbl { fill: #7d8590; font-size: 10px; } "
        ".foot { fill: #39d353; font-size: 12px; opacity: 0; "
        "animation: fade .6s ease-out 2.6s forwards; } "
        "@keyframes fade { to { opacity: .9; } }"
    )
    parts.append("</style>")

    parts.append('<rect width="' + str(WIDTH) + '" height="' + str(HEIGHT) + '" rx="8" fill="#0d1117"/>')

    seen = []
    for w in range(len(grid)):
        first = grid[w][0][0]
        if first.month not in seen and first.day <= 7:
            seen.append(first.month)
            x = PAD + GUTTER + w * PITCH
            parts.append('<text class="lbl" x="' + str(x) + '" y="' + str(PAD + 12) + '">' + MONTHS[first.month - 1] + '</text>')

    for wd, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = PAD + TOP + wd * PITCH + CELL - 2
        parts.append('<text class="lbl" x="' + str(PAD) + '" y="' + str(y) + '">' + name + '</text>')

    for w in range(len(grid)):
        for wd in range(7):
            day, rec = grid[w][wd]
            level = rec["level"] if rec else 0
            count = rec.get("count", 0) if rec else 0
            if level < 0:
                level = 0
            if level > len(PALETTE) - 1:
                level = len(PALETTE) - 1
            x = PAD + GUTTER + w * PITCH
            y = PAD + TOP + wd * PITCH
            delay = (w + wd) * 0.014
            parts.append(
                '<rect class="box" x="' + str(x) + '" y="' + str(y) + '" width="' + str(CELL) +
                '" height="' + str(CELL) + '" rx="2.5" fill="' + PALETTE[level] +
                '" style="animation-delay:' + format(delay, ".3f") + 's">' +
                '<title>' + esc(count) + ' on ' + esc(day.isoformat()) + '</title></rect>'
            )

    ly = PAD + TOP + 7 * PITCH + 18
    lx = WIDTH - PAD - (len(PALETTE) * PITCH) - 62
    parts.append('<text class="lbl" x="' + str(lx) + '" y="' + str(ly + CELL - 3) + '">Less</text>')
    for i in range(len(PALETTE)):
        parts.append(
            '<rect class="box" x="' + str(lx + 32 + i * PITCH) + '" y="' + str(ly) +
            '" width="' + str(CELL) + '" height="' + str(CELL) + '" rx="2.5" fill="' + PALETTE[i] +
            '" style="animation-delay:' + format(2.2 + i * 0.05, ".2f") + 's"/>'
        )
    parts.append('<text class="lbl" x="' + str(lx + 36 + len(PALETTE) * PITCH) + '" y="' + str(ly + CELL - 3) + '">More</text>')

    parts.append('<text class="foot" x="' + str(PAD + GUTTER) + '" y="' + str(ly + CELL - 3) + '">' +
                 format(total, ",") + ' contributions in the last year</text>')

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    if not os.path.exists(DATA):
        print(DATA + " not found - run fetch_contributions.py first")
        return 1

    f = open(DATA, encoding="utf-8")
    payload = json.load(f)
    f.close()

    if isinstance(payload, list):
        payload = {"days": payload}

    svg = render(payload)

    out = open(OUT, "w", encoding="utf-8", newline="\n")
    out.write(svg)
    out.close()

    print("Wrote " + OUT + " (" + format(len(svg.encode("utf-8")), ",") + " bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())