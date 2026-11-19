# news-image-20261119 entry (Python 3.13, standard library only).
#
# The entry image is entry.png beside this file: a 1024x1024 editorial
# infographic drawn for Thursday 19 November 2026 (see make_image.py,
# the generator that drew it). The grader runs this program with no
# network, so it simply copies the committed image to /output/entry.png.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
# /output:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
dest = OUT / "entry.png"
shutil.copyfile(HERE / "entry.png", dest)
print(f"wrote {dest} ({dest.stat().st_size} bytes)")
