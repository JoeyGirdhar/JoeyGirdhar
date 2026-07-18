import json

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def draw_svg():
    print("Converting data coordinates into animated grid array...")
    try:
        with open("data/contributions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: contributions.json missing! Run fetch_contributions.py first.")
        return
        
    svg_header = """<svg xmlns="http://w3.org" viewBox="0 0 860 160" width="860" height="160">
  <rect width="100%" height="100%" fill="#0d1117" rx="6"/>
  <style>
    rect { opacity: 0; animation: slideDiagonal 0.4s ease forwards; }
    .meta-text { font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, monospace; font-size: 13px; font-weight: 600; fill: #58a6ff; }
    .legend-text { font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, monospace; font-size: 11px; fill: #8b949e; }
    @keyframes slideDiagonal {
      from { opacity: 0; transform: translate(-4px, -4px); }
      to { opacity: 1; transform: translate(0, 0); }
    }
  </style>

  <circle cx="20" cy="20" r="6" fill="#ff5f56"/>
  <circle cx="40" cy="20" r="6" fill="#ffbd2e"/>
  <circle cx="60" cy="20" r="6" fill="#27c93f"/>
  <text x="80" y="24" class="meta-text">joey@github ~ $ ./contributions.sh</text>
"""
    
    rects = ""
    for index, day in enumerate(data):
        col = index // 7
        row = index % 7
        x = col * 15 + 20
        y = row * 15 + 45
        color = PALETTE[day["level"]]
        delay = (col + row) * 0.012
        
        rects += f'  <rect x="{x}" y="{y}" width="11" height="11" rx="2" fill="{color}" style="animation-delay: {delay:.3f}s;" />\n'
        
    legend = """
  <text x="730" y="152" class="legend-text">Less</text>
  <rect x="765" y="143" width="11" height="11" rx="2" fill="#161b22"/>
  <rect x="780" y="143" width="11" height="11" rx="2" fill="#0e4429"/>
  <rect x="795" y="143" width="11" height="11" rx="2" fill="#006d32"/>
  <rect x="810" y="143" width="11" height="11" rx="2" fill="#26a641"/>
  <rect x="825" y="143" width="11" height="11" rx="2" fill="#39d353"/>
  <text x="842" y="152" class="legend-text">More</text>
</svg>"""
    
    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write(svg_header + rects + legend)
    print("Success! Automated canvas array rendering saved as: contrib-heatmap.svg")

if __name__ == "__main__":
    draw_svg()
