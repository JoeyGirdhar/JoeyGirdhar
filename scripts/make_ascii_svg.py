import cv2
import numpy as np

RAMP = " .`:-=+*cs#%@" 
FILL_COLOR = "#b3b3b3"

def img_to_ascii(img_path, width=85):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    aspect = h / w
    height = int(width * aspect * 0.48)
    resized = cv2.resize(img, (width, height))
    
    lines = []
    for row in resized:
        line = "".join(RAMP[int(pixel / 255 * (len(RAMP) - 1))] for pixel in row)
        lines.append(line)
    return lines

def create_svg(ascii_lines, output_path="avi-ascii.svg"):
    font_size = 12
    line_height = 13
    char_width = 7.2
    
    svg_w = int(len(ascii_lines[0]) * char_width) + 20
    svg_h = int(len(ascii_lines) * line_height) + 30
    
    svg = f'<svg xmlns="http://w3.org" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">\n'
    svg += f'  <rect width="100%" height="100%" fill="#0d1117" rx="6"/>\n'
    svg += '  <style>\n'
    svg += '    .term-text { font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace; font-weight: 600; }\n'
    svg += '    @keyframes lineType { from { width: 0; } to { width: 100%; } }\n'
    svg += '  </style>\n'
    
    for i, line in enumerate(ascii_lines):
        escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        y_pos = 25 + (i * line_height)
        delay = i * 0.04
        
        svg += f'  <svg x="10" y="{y_pos}" width="100%" height="{line_height}">\n'
        svg += f'    <text x="0" y="10" fill="{FILL_COLOR}" font-size="{font_size}" class="term-text" style="animation: lineType 0.15s steps(30) forwards; animation-delay: {delay:.2f}s; overflow: hidden; white-space: nowrap; width: 0;">{escaped_line}</text>\n'
        svg += f'  </svg>\n'
        
    svg += '</svg>'
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Success! Automated drawing asset saved as: {output_path}")

if __name__ == "__main__":
    lines = img_to_ascii("source-prepped.png")
    create_svg(lines)
