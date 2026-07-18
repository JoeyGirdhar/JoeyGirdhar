import os

OUT = "info-card.svg"
WIDTH = 490
HEIGHT = 430

USER = "joey@github"

ROWS = [
    ("Now", "Founder & CEO @ RightClick | $30k+ Invoiced"),
    ("Prev", "Top 100 Stock Pitcher @ Global YIS | 289.6% ROI"),
    ("Also", "FBLA President | Top 20 Nationally"),
    ("Plus", "4x Hackathon Competitor | 2x Hackathon Winner"),
    ("Built", "15+ DeepL Pipelines | 100+ AI/ML Agentic Systems"),
    ("Edu", "Rouse High School '28 (CS / AI / ML)"),
]

STACK = [
    ("Frontend", "React, JavaScript, TypeScript, Figma"),
    ("Backend", "Node.js, Python, Swift, Firebase, SQL"),
    ("AI / ML", "LangChain, OpenAI, Agentic Workflows"),
    ("Cloud", "AWS, Google Cloud, Supabase, Vercel"),
]

HIGHLIGHTS = [
    "Hourly App Creator | Top 100 Diamond Challenge Winner",
    "2nd Place Internationally - YIS Quiz Bowl",
]

KEY_X = 20
VAL_X = 110
STATIC = os.environ.get("STATIC") == "1"


def esc(s):
    s = str(s)
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    return s


def main():
    p = []
    delay = [0.1]

    def d():
        v = delay[0]
        delay[0] = round(v + 0.08, 2)
        return "0" if STATIC else format(v, ".2f")

    p.append('<svg xmlns="http://www.w3.org/2000/svg" width="' + str(WIDTH) +
             '" height="' + str(HEIGHT) + '" viewBox="0 0 ' + str(WIDTH) + ' ' +
             str(HEIGHT) + '" role="img" aria-label="' + esc(USER) + ' info card">')

    p.append("<style>")
    p.append(
        ".text { font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, monospace; "
        "font-size: 13px; font-weight: 600; opacity: " + ("1" if STATIC else "0") + "; " +
        ("" if STATIC else "animation: fadeIn 0.4s ease forwards; ") + "} "
        ".title { fill: #58a6ff; font-weight: bold; } "
        ".key { fill: #ff7b72; font-weight: bold; } "
        ".val { fill: #c9d1d9; } "
        ".blue { fill: #58a6ff; } "
        ".dim { fill: #8b949e; } "
        ".dot { fill: #39d353; } "
        "@keyframes fadeIn { to { opacity: 1; } }"
    )
    p.append("</style>")

    p.append('<rect width="100%" height="100%" fill="#0d1117" rx="6"/>')
    p.append('<circle cx="20" cy="20" r="6" fill="#ff5f56"/>')
    p.append('<circle cx="40" cy="20" r="6" fill="#ffbd2e"/>')
    p.append('<circle cx="60" cy="20" r="6" fill="#27c93f"/>')
    p.append('<text x="245" y="24" fill="#8b949e" font-family="monospace" font-size="12" '
             'text-anchor="middle">' + esc(USER) + ': ~</text>')

    y = 65
    p.append('<text x="20" y="' + str(y) + '" class="text title" style="animation-delay: ' + d() + 's;">' +
             esc(USER) + ' ~ $ neofetch</text>')

    y = 90
    p.append('<text x="20" y="' + str(y) + '" class="text blue" style="animation-delay: ' + d() + 's;">' +
             esc(USER) + '</text>')
    y = 102
    p.append('<text x="20" y="' + str(y) + '" class="text val" style="animation-delay: ' + d() + 's;">' +
             ("-" * len(USER)) + '</text>')

    y = 128
    for key, val in ROWS:
        p.append('<text x="' + str(KEY_X) + '" y="' + str(y) + '" class="text" style="animation-delay: ' + d() + 's;">'
                 '<tspan class="key">' + esc(key) + '</tspan>'
                 '<tspan class="val" x="' + str(VAL_X) + '">' + esc(val) + '</tspan></text>')
        y += 20

    y += 10
    p.append('<text x="20" y="' + str(y) + '" class="text blue" style="animation-delay: ' + d() + 's;">- Stack</text>')
    y += 20
    for key, val in STACK:
        p.append('<text x="' + str(KEY_X) + '" y="' + str(y) + '" class="text" style="animation-delay: ' + d() + 's;">'
                 '<tspan class="key">' + esc(key) + '</tspan>'
                 '<tspan class="val" x="' + str(VAL_X) + '">' + esc(val) + '</tspan></text>')
        y += 20

    y += 10
    p.append('<text x="20" y="' + str(y) + '" class="text blue" style="animation-delay: ' + d() + 's;">- Highlights</text>')
    y += 20
    for h in HIGHLIGHTS:
        p.append('<text x="' + str(KEY_X) + '" y="' + str(y) + '" class="text" style="animation-delay: ' + d() + 's;">'
                 '<tspan class="dot">*</tspan> <tspan class="val">' + esc(h) + '</tspan></text>')
        y += 20

    p.append("</svg>")

    svg = "\n".join(p)
    f = open(OUT, "w", encoding="utf-8", newline="\n")
    f.write(svg)
    f.close()
    print("Wrote " + OUT + " (" + format(len(svg.encode("utf-8")), ",") + " bytes)")


if __name__ == "__main__":
    main()