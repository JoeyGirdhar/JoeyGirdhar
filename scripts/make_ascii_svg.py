import cv2
import numpy as np

SOURCE = "source-prepped.png"
OUTPUT = "avi-ascii.svg"

USER = "joey@github"
NAME = "Joey Girdhar"

RAMP = " .`:-=+*cs#%@"
FILL_COLOR = "#c9d1d9"
CURSOR_COLOR = "#c9d1d9"

COLUMNS = 100
WHITE_CUTOFF = 235

CANVAS_W = 740
CANVAS_H = 860
PAD = 18
TITLE_H = 34
FOOTER_H = 46

ROW_WIPE = 0.12
ROW_STAGGER = 0.10


def img_to_ascii(img_path, width=COLUMNS):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: " + img_path + " missing!")
        return []
    h, w = img.shape
    aspect = h / w
    height = int(width * aspect * 0.48)
    resized = cv2.resize(img, (width, height))

    last = len(RAMP) - 1
    lines = []
    for row in resized:
        chars = []
        for pixel in row:
            if pixel >= WHITE_CUTOFF:
                chars.append(" ")
            else:
                chars.append(RAMP[int((255 - pixel) / 255 * last)])
        lines.append("".join(chars))

    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return [l.ljust(width) for l in lines]


def esc(s):
    for a, b in (("&", "&amp;"), ("<", "&lt;"), (">", "&gt;"), ('"', "&quot;")):
        s = s.replace(a, b)
    return s


def create_svg(ascii_lines, output_path=OUTPUT):
    if not ascii_lines:
        return

    rows = len(ascii_lines)
    cols = len(ascii_lines[0])

    art_w = CANVAS_W - PAD * 2
    art_top = TITLE_H + PAD
    art_h = CANVAS_H - art_top - FOOTER_H - PAD

    font_size = (art_w / cols) / 0.55
    line_h = font_size * 1.15
    if rows * line_h > art_h:
        shrink = art_h / (rows * line_h)
        font_size *= shrink
        line_h *= shrink
    art_top += (art_h - rows * line_h) / 2

    p = []
    p.append('<svg xmlns="http://www.w3.org/2000/svg" width="' + str(CANVAS_W) + '" height="' +
             str(CANVAS_H) + '" viewBox="0 0 ' + str(CANVAS_W) + ' ' + str(CANVAS_H) +
             '" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
             'xml:space="preserve" role="img" aria-label="ASCII portrait">')

    p.append('<rect width="' + str(CANVAS_W) + '" height="' + str(CANVAS_H) + '" rx="10" fill="#0d1117"/>')
    p.append('<rect x="0.5" y="0.5" width="' + str(CANVAS_W - 1) + '" height="' + str(CANVAS_H - 1) +
             '" rx="10" fill="none" stroke="#30363d"/>')
    p.append('<line x1="0" y1="' + str(TITLE_H) + '" x2="' + str(CANVAS_W) + '" y2="' +
             str(TITLE_H) + '" stroke="#30363d"/>')
    p.append('<circle cx="22" cy="17" r="5.5" fill="#ff5f56"/>')
    p.append('<circle cx="40" cy="17" r="5.5" fill="#ffbd2e"/>')
    p.append('<circle cx="58" cy="17" r="5.5" fill="#27c93f"/>')
    p.append('<text x="' + str(CANVAS_W // 2) + '" y="21" fill="#e6edf3" font-size="12" '
             'text-anchor="middle">' + esc(USER) + ': ~$ ./portrait.sh</text>')

    for i, line in enumerate(ascii_lines):
        y_top = art_top + i * line_h
        baseline = y_top + font_size * 0.85
        begin = i * ROW_STAGGER
        p.append('<clipPath id="r' + str(i) + '"><rect x="' + str(PAD) + '" y="' +
                 format(y_top, ".1f") + '" width="0" height="' + format(line_h + 1, ".1f") + '">'
                 '<animate attributeName="width" from="0" to="' + str(art_w) + '" begin="' +
                 format(begin, ".2f") + 's" dur="' + str(ROW_WIPE) + 's" fill="freeze"/></rect></clipPath>')
        p.append('<g clip-path="url(#r' + str(i) + ')"><text xml:space="preserve" x="' + str(PAD) +
                 '" y="' + format(baseline, ".1f") + '" fill="' + FILL_COLOR + '" font-size="' +
                 format(font_size, ".2f") + '" textLength="' + str(art_w) +
                 '" lengthAdjust="spacing">' + esc(line) + '</text></g>')
        if line.strip():
            p.append('<rect y="' + format(y_top, ".1f") + '" width="7" height="' +
                     format(line_h, ".1f") + '" fill="' + CURSOR_COLOR + '" opacity="0">'
                     '<animate attributeName="x" from="' + str(PAD) + '" to="' + str(PAD + art_w) +
                     '" begin="' + format(begin, ".2f") + 's" dur="' + str(ROW_WIPE) + 's" fill="freeze"/>'
                     '<set attributeName="opacity" to="0.85" begin="' + format(begin, ".2f") + 's"/>'
                     '<set attributeName="opacity" to="0" begin="' + format(begin + ROW_WIPE, ".2f") + 's"/>'
                     '</rect>')

    fy = CANVAS_H - FOOTER_H
    p.append('<line x1="0" y1="' + str(fy) + '" x2="' + str(CANVAS_W) + '" y2="' + str(fy) +
             '" stroke="#30363d"/>')
    p.append('<text x="' + str(PAD) + '" y="' + str(fy + 28) + '" fill="#7d8590" font-size="13">' +
             esc(USER) + ':~$ whoami <tspan fill="#e6edf3">' + esc(NAME) + '</tspan></text>')
    p.append('<rect x="' + str(PAD + 8 * 13) + '" y="' + str(fy + 16) + '" width="8" height="14" '
             'fill="#e6edf3"><animate attributeName="opacity" values="1;1;0;0" '
             'keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/></rect>')

    p.append("</svg>")

    svg = "\n".join(p)
    f = open(output_path, "w", encoding="utf-8", newline="\n")
    f.write(svg)
    f.close()
    print("Wrote " + output_path + " (" + str(cols) + "x" + str(rows) + " grid, font " +
          format(font_size, ".2f") + ", " + format(len(svg.encode("utf-8")), ",") + " bytes)")


if __name__ == "__main__":
    lines = img_to_ascii(SOURCE)
    create_svg(lines)