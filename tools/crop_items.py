"""Crops the test items out of a PDF of the test, on your own computer.

It finds every framed figure on the chosen pages, groups them into rows, and
saves each row of 5 figures (target + 4 options) as one item:

    stimuli/item01_target.png, item01_A.png, item01_B.png, item01_C.png, item01_D.png, ...

Those are the file names config.js already expects. Items are numbered in reading
order (top to bottom, page by page). Nothing is uploaded anywhere and the
stimuli folder is ignored by git.

Needs macOS (it uses the built-in PDF engine through Swift, which comes with
Xcode's command line tools) and numpy.

Examples (run from the repo folder):
    python3 tools/crop_items.py ~/Downloads/MRT_test.pdf --pages 3-6
    python3 tools/crop_items.py test.pdf --pages 3-6 --dry-run      # just report what it finds
    python3 tools/crop_items.py test.pdf --pages 2 --prefix P --start 1 --out stimuli/practice

Afterwards: fill in each item's answer in config.js and open index.html?check=1.
"""
import argparse
import glob
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LETTERS = "ABCD"


# ── PDF → pixels ──────────────────────────────────────────────────────
def render(pdf, outdir, dpi):
    build = HERE / ".build"
    exe = build / "render_pdf"
    src = HERE / "render_pdf.swift"
    if not exe.exists() or exe.stat().st_mtime < src.stat().st_mtime:
        build.mkdir(exist_ok=True)
        print("Compiling the PDF renderer (first run only)…")
        subprocess.run(["swiftc", "-O", str(src), "-o", str(exe)], check=True)
    subprocess.run([str(exe), str(pdf), str(outdir), str(dpi)], check=True, stdout=subprocess.DEVNULL)
    pages = {}
    for p in glob.glob(f"{outdir}/*.raw"):
        n, w, h, b = map(int, re.search(r"page(\d+)_(\d+)x(\d+)_(\d+)\.raw", p).groups())
        pages[n] = np.fromfile(p, np.uint8).reshape(h, b)[:, :w]
    return pages


# ── Finding the framed figures ────────────────────────────────────────
def dark_runs(row, minlen, thresh):
    d = np.diff(np.concatenate([[0], (row < thresh).astype(np.int8), [0]]))
    st, en = np.flatnonzero(d == 1), np.flatnonzero(d == -1)
    keep = (en - st) >= minlen
    return zip(st[keep], en[keep])


def find_boxes(a, thresh=200, min_frac=0.06):
    """Rectangles drawn as thin dark frames. Returns (x0, y0, x1, y1) in pixels."""
    h, w = a.shape
    minlen = int(w * min_frac)
    lines = []                       # horizontal frame edges
    for y in range(h):
        for s, e in dark_runs(a[y], minlen, thresh):
            for L in lines:
                if abs(L[1] - s) < 6 and abs(L[2] - e) < 6 and y - L[3] <= 2:
                    L[3] = y
                    break
            else:
                lines.append([y, s, e, y])   # y0, x-start, x-end, y1
    boxes, used = [], set()
    for i, (ty0, ts, te, ty1) in enumerate(lines):
        if i in used:
            continue
        for j in range(i + 1, len(lines)):
            if j in used:
                continue
            by0, bs, be, by1 = lines[j]
            bw, bh = te - ts, by1 - ty0
            if abs(ts - bs) < 8 and abs(te - be) < 8 and 0.5 * bw < bh < 2.0 * bw:
                left = (a[ty0:by1, ts:ts + 6] < thresh).any(axis=1).mean()
                right = (a[ty0:by1, te - 6:te] < thresh).any(axis=1).mean()
                if left > 0.9 and right > 0.9:
                    boxes.append((int(ts), int(ty0), int(te), int(by1)))
                    used |= {i, j}
                    break
    return boxes


def rows_of(boxes):
    """Groups boxes whose tops line up into rows, left to right, top to bottom."""
    rows = []
    for b in sorted(boxes, key=lambda b: b[1]):
        if rows and abs(rows[-1][0][1] - b[1]) < 25:
            rows[-1].append(b)
        else:
            rows.append([b])
    return [sorted(r) for r in rows]


# ── Writing PNGs (no extra libraries needed) ──────────────────────────
def write_png(path, g):
    h, w = g.shape
    raw = b"".join(b"\x00" + g[y].tobytes() for y in range(h))
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    Path(path).write_bytes(b"\x89PNG\r\n\x1a\n"
                           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0))
                           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def parse_pages(spec, n):
    if not spec:
        return list(range(1, n + 1))
    out = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out += range(int(a), int(b or a) + 1)
    return [p for p in out if 1 <= p <= n]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", help="the test PDF")
    ap.add_argument("--pages", help="pages holding the test items, e.g. 3-6 (default: all pages)")
    ap.add_argument("--out", default=str(ROOT / "stimuli"), help="folder to save into (default: stimuli/)")
    ap.add_argument("--prefix", default="item", help='file name prefix (default "item")')
    ap.add_argument("--start", type=int, default=1, help="number of the first item (default 1)")
    ap.add_argument("--per-row", type=int, default=5, help="figures per item row: target + options (default 5)")
    ap.add_argument("--dpi", type=int, default=300, help="render resolution (default 300)")
    ap.add_argument("--dry-run", action="store_true", help="report what would be saved without saving")
    args = ap.parse_args()

    tmp = tempfile.mkdtemp(prefix="mrt_crop_")
    try:
        pages = render(Path(args.pdf).expanduser(), tmp, args.dpi)
        chosen = parse_pages(args.pages, len(pages))
        out = Path(args.out)
        if not args.dry_run:
            out.mkdir(parents=True, exist_ok=True)
        num, problems = args.start, []
        for pg in chosen:
            a = pages[pg]
            rows = rows_of(find_boxes(a))
            good = [r for r in rows if len(r) == args.per_row]
            print(f"Page {pg}: {len(good)} item row(s)", end="")
            odd = [len(r) for r in rows if len(r) != args.per_row]
            if odd:
                print(f"  (skipped rows with {', '.join(map(str, odd))} figure(s))", end="")
                problems.append(f"page {pg}: skipped rows with {odd} figures instead of {args.per_row}")
            print(f"  -> items {num}–{num + len(good) - 1}" if good else "")
            for r in good:
                names = ["target"] + list(LETTERS[:args.per_row - 1])
                for (x0, y0, x1, y1), nm in zip(r, names):
                    if not args.dry_run:
                        write_png(out / f"{args.prefix}{num:02d}_{nm}.png", np.ascontiguousarray(a[y0:y1 + 1, x0:x1 + 1]))
                num += 1
        total = num - args.start
        print(f"\n{'Would save' if args.dry_run else 'Saved'} {total} item(s) "
              f"({total * args.per_row} pictures){'' if args.dry_run else ' to ' + str(out)}.")
        if problems:
            print("Check these:\n  " + "\n  ".join(problems))
        if total and not args.dry_run:
            print("Next: fill in each item's answer in config.js, then open index.html?check=1 to compare.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
