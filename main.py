#!/usr/bin/env python3
"""Entrypoint for the news-image-20261119 entry.

Copies the pre-rendered entry.png into the output directory (default "out",
or $MAKEFUN_OUTPUT_DIR when set). The image itself is produced by
make_image.py; this entrypoint only delivers it, so the run is fast and
byte-identical every time.
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    out_dir.mkdir(parents=True, exist_ok=True)
    src = HERE / "entry.png"
    if not src.exists():
        print("entry.png missing; run make_image.py first", file=sys.stderr)
        return 1
    dest = out_dir / "entry.png"
    shutil.copyfile(src, dest)
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
