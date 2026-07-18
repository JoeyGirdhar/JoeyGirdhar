import cv2
import numpy as np

SOURCE = "source-prepped.png"
OUTPUT = "avi-ascii.svg"

RAMP = " .`:-=+*cs#%@"
FILL_COLOR = "#b3b3b3"
CURSOR_COLOR = "#39d353"

COLUMNS = 100
WHITE_CUTOFF = 215
ROW_WIPE = 0.35
ROW_STAGGER = 0.05


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
        lines.append("".join(chars).rstrip())
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def esc(s):
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    return s


def create_svg(ascii_lines, output_path=OUTPUT):
    if not ascii_lines:
        return

    font_size = 12
    line_height = 13
    char_width = 7.2

    cols = max(len(l) for l in ascii_lines)
    svg_w = int(cols * char_width) + 20
    svg_h = int(len(ascii_lines) * line_height) + 30

    p = []
    p.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + str(svg_w) + ' ' +
             str(svg_h) + '" width="' + str(svg_w) + '" height="' + str(svg_h) +
             '" xml:space="preserve" role="img" aria-label="ASCII portrait">')
    p.append('<rect width="100%" height="100%" fill="#0d1117" rx="6"/>')
    p.append('<style>.term-text { font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, monospace; font-weight: 600; white-space: pre; }</style>')

    p.append("<defs>")
    for i, line in enumerate(ascii_lines):
        y_pos = 25 + (i * line_height)
        begin = format(i * ROW_STAGGER, ".2f")
        run = int(len(line) * char_width) + 4
        p.append('<clipPath id="w' + str(i) + '"><rect x="10" y="' + str(y_pos - line_height) +
                 '" width="0" height="' + str(line_height + 2) + '">'
                 '<animate attributeName="width" from="0" to="' + str(run) + '" dur="' +
                 str(ROW_WIPE) + 's" begin="' + begin + 's" fill="freeze"/></rect></clipPath>')
    p.append("</defs>")

    for i, line in enumerate(ascii_lines):
        y_pos = 25 + (i * line_height)
        begin = i * ROW_STAGGER
        run = int(len(line) * char_width) + 4
        p.append('<text x="10" y="' + str(y_pos) + '" fill="' + FILL_COLOR + '" font-size="' +
                 str(font_size) + '" class="term-text" xml:space="preserve" clip-path="url(#w' +
                 str(i) + ')">' + esc(line) + '</text>')
        if line.strip():
            p.append('<rect x="10" y="' + str(y_pos - 10) + '" width="' + str(char_width) +
                     '" height="11" fill="' + CURSOR_COLOR + '" opacity="0">'
                     '<animate attributeName="x" from="10" to="' + str(10 + run) + '" dur="' +
                     str(ROW_WIPE) + 's" begin="' + format(begin, ".2f") + 's" fill="freeze"/>'
                     '<set attributeName="opacity" to="0.85" begin="' + format(begin, ".2f") + 's"/>'
                     '<set attributeName="opacity" to="0" begin="' + format(begin + ROW_WIPE, ".2f") + 's"/>'
                     '</rect>')

    p.append("</svg>")

    svg = "\n".join(p)
    f = open(output_path, "w", encoding="utf-8", newline="\n")
    f.write(svg)
    f.close()
    print("Wrote " + output_path + " (" + str(cols) + " cols x " + str(len(ascii_lines)) +
          " rows, " + format(len(svg.encode("utf-8")), ",") + " bytes)")


if __name__ == "__main__":
    lines = img_to_ascii(SOURCE)
    create_svg(lines)