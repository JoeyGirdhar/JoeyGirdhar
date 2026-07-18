import glob
import os

for path in sorted(glob.glob("*.svg")):
    raw = open(path, "rb").read()

    if not raw.strip():
        print("SKIPPED (empty): " + path)
        continue

    fixed = raw

    for bom in (b"\xef\xbb\xbf", b"\xff\xfe", b"\xfe\xff"):
        if fixed.startswith(bom):
            fixed = fixed[len(bom):]
            break

    fixed = fixed.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

    if fixed == raw:
        print("unchanged: " + path)
        continue

    out = open(path, "wb")
    out.write(fixed)
    out.close()
    print("fixed: " + path + "  (" + format(len(raw), ",") + " -> " + format(len(fixed), ",") + " bytes)")