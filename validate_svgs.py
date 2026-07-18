import glob
import os
import sys
import xml.etree.ElementTree as ET


def check(path):
    problems = []
    raw = open(path, "rb").read()

    if not raw.strip():
        return ["FILE IS EMPTY"]

    if raw.startswith(b"\xef\xbb\xbf"):
        problems.append("starts with a UTF-8 BOM")
    elif raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        problems.append("starts with a UTF-16 BOM")

    if b"\x00" in raw[:200]:
        problems.append("has NUL bytes in the header (file is UTF-16, not UTF-8)")

    crlf = raw.count(b"\r\n")
    if crlf:
        problems.append("has CRLF line endings (" + str(crlf) + " of them)")

    head = raw.lstrip()[:5]
    if not (head.startswith(b"<svg") or head.startswith(b"<?xml")):
        problems.append("does not begin with <svg or <?xml (begins with " + repr(head) + ")")

    try:
        root = ET.parse(path).getroot()
        if not root.tag.endswith("svg"):
            problems.append("root element is <" + root.tag + ">, not <svg>")
        if "viewBox" not in root.attrib and "width" not in root.attrib:
            problems.append("has no viewBox and no width/height")
        drawable = 0
        for el in root.iter():
            if el.tag.split("}")[-1] in ("rect", "text", "path", "circle", "tspan"):
                drawable += 1
        if drawable < 5:
            problems.append("only " + str(drawable) + " drawable elements - looks like a stub")
    except ET.ParseError as e:
        problems.append("INVALID XML: " + str(e))

    return problems


def main():
    files = sorted(glob.glob("*.svg"))
    if not files:
        print("No .svg files found. Run this from the repo root.")
        return 1

    bad = 0
    for f in files:
        size = os.path.getsize(f)
        problems = check(f)
        if problems:
            bad += 1
            print("")
            print("[BROKEN] " + f + "  (" + format(size, ",") + " bytes)")
            for p in problems:
                print("         - " + p)
        else:
            print("[ ok   ] " + f + "  (" + format(size, ",") + " bytes)")

    print("")
    if bad:
        print(str(bad) + " file(s) will not render on GitHub.")
    else:
        print("All SVGs are structurally valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())