# -*- coding: utf-8 -*-
"""fontmatch.py <png> <x0> <y0> <x1> <y1> --text <글> [--mode white|green|dark] [--top 5]
같은 글을 같은 잉크 높이로 그려 잉크 모양 겹침(IoU) 비교. 글꼴 = _assets/fonts.json."""
import sys, os, json, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))

HERE = os.path.dirname(os.path.abspath(__file__))
FJ = os.path.join(HERE, "..", "_assets", "fonts.json")

def target_mask(img, mode):
    a = img.astype(int)
    mx, mn = a.max(2), a.min(2)
    if mode == "white":
        return (a.mean(2) > 225) & (mx - mn < 40)
    if mode == "green":
        return (a[:, :, 1] > 180) & (a[:, :, 0] < 120)
    if mode == "dark":
        return a.mean(2) < 60
    if mode == "colored":
        return (mx - mn > 90) & (mx > 150)
    raise ValueError(mode)

def crop_bb(m):
    ys, xs = np.where(m)
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def render(font_path, text, h_target):
    sz = 100
    for _ in range(3):
        f = ImageFont.truetype(font_path, sz)
        im = Image.new("L", (int(sz * len(text) * 1.3) + 40, int(sz * 1.8)), 0)
        ImageDraw.Draw(im).text((20, 10), text, fill=255, font=f)
        m = np.array(im) > 128
        if not m.any():
            return None
        c = crop_bb(m)
        sz = max(8, int(round(sz * h_target / c.shape[0])))
    return c

def iou(a, b):
    h = max(a.shape[0], b.shape[0]); w = max(a.shape[1], b.shape[1])
    A = np.zeros((h, w), bool); B = np.zeros((h, w), bool)
    A[:a.shape[0], :a.shape[1]] = a; B[:b.shape[0], :b.shape[1]] = b
    return (A & B).sum() / max(1, (A | B).sum())

def match(img, box, text, mode="white", top=5):
    x0, y0, x1, y1 = box
    m = crop_bb(target_mask(img[y0:y1, x0:x1], mode))
    fonts = json.load(open(FJ, encoding="utf-8"))
    res = []
    for name, path in fonts.items():
        try:
            r = render(path, text.replace(" ", ""), m.shape[0]) if False else render(path, text, m.shape[0])
        except Exception:
            continue
        if r is None:
            continue
        wr = r.shape[1] / m.shape[1]
        rs = np.array(Image.fromarray(r.astype(np.uint8) * 255).resize((m.shape[1], m.shape[0]))) > 128
        s = iou(m, rs) * max(0.0, 1 - abs(wr - 1))
        res.append({"font": name, "score": round(float(s), 3), "width_ratio": round(float(wr), 3)})
    res.sort(key=lambda d: -d["score"])
    return {"ink_h": int(m.shape[0]), "ink_w": int(m.shape[1]), "top5": res[:top]}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("png")
    for k in ["x0", "y0", "x1", "y1"]:
        ap.add_argument(k, type=int)
    ap.add_argument("--text", required=True); ap.add_argument("--mode", default="white"); ap.add_argument("--top", type=int, default=5)
    a = ap.parse_args()
    img = np.array(Image.open(a.png).convert("RGB"))
    print(json.dumps(match(img, (a.x0, a.y0, a.x1, a.y1), a.text, a.mode, a.top), ensure_ascii=False))
