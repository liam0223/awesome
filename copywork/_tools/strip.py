# -*- coding: utf-8 -*-
"""strip.py <mp4> <t0> <t1> <간격> <y0> <y1> <out.jpg> [--w 360]
세로 띠 y0~y1 만 잘라 간격마다 세로로 쌓은 jpg(시각 글자 찍음)."""
import sys, os, argparse
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
import lib, sheet

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for k in ["mp4", "t0", "t1", "step", "y0", "y1", "out"]:
        ap.add_argument(k)
    ap.add_argument("--w", type=int, default=540)
    a = ap.parse_args()
    t0, t1, st, y0, y1 = float(a.t0), float(a.t1), float(a.step), int(a.y0), int(a.y1)
    fr = lib.frames(a.mp4, fps=1 / st, t0=t0, t1=t1, crop=(0, y0, 1080, y1 - y0), scale_w=a.w)
    h = fr[0][1].shape[0]
    sh = Image.new("RGB", (a.w + 70, h * len(fr)), "black"); d = ImageDraw.Draw(sh); f = sheet.font(18)
    for i, (t, img) in enumerate(fr):
        sh.paste(Image.fromarray(img), (70, i * h)); d.text((2, i * h + 2), f"{t:.3f}", fill="yellow", font=f)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    sh.save(a.out, quality=90); print(a.out, len(fr))
