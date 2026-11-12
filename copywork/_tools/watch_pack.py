# -*- coding: utf-8 -*-
"""watch_pack.py <벤치 mp4> <final.mp4> --out <09_verify>
compare_sheet.png(상대 시각 1/8~8/8 — 위 벤치·아래 우리) · watch_pack/(0·1·2초 나란히, 우리 끝 0.5초) · 자동 검사(검정·멈춤 구간)"""
import sys, os, argparse, json, subprocess
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
import lib, sheet

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("bench"); ap.add_argument("ours"); ap.add_argument("--out", required=True); a = ap.parse_args()
    os.makedirs(os.path.join(a.out, "watch_pack"), exist_ok=True)
    db, do = lib.duration(a.bench), lib.duration(a.ours)
    W = 240; Hh = 427; f = sheet.font(20)
    sh = Image.new("RGB", (W * 8, Hh * 2 + 30), "black"); d = ImageDraw.Draw(sh)
    for k in range(8):
        for row, (mp4, dur) in enumerate([(a.bench, db), (a.ours, do)]):
            t = min(dur - 0.2, dur * (k + 1) / 8)
            im = Image.fromarray(lib.frame(mp4, t)).resize((W, Hh))
            sh.paste(im, (k * W, 30 + row * Hh))
            d.text((k * W + 4, 30 + row * Hh + 4), f"{'벤치' if row == 0 else '우리'} {t:.1f}", fill="yellow", font=f)
    d.text((4, 4), "위 = 벤치 · 아래 = 우리 (각 영상 길이의 1/8~8/8)", fill="white", font=f)
    sh.save(os.path.join(a.out, "compare_sheet.png"))
    for t in (0.0, 1.0, 2.0):
        pair = Image.new("RGB", (W * 2, Hh))
        pair.paste(Image.fromarray(lib.frame(a.bench, t)).resize((W, Hh)), (0, 0)); pair.paste(Image.fromarray(lib.frame(a.ours, t)).resize((W, Hh)), (W, 0))
        pair.save(os.path.join(a.out, "watch_pack", f"pair_{t:.0f}s.png"))
    sheet.make_sheet(a.ours, 0.1, os.path.join(a.out, "watch_pack", "ours_end_0.5s.jpg"), cols=5, w=216, t0=max(0, do - 0.5), t1=do)
    # 자동 검사: 검정 구간 · 멈춘 구간(0.1초 칸 픽셀 차)
    fr = lib.frames(a.ours, fps=10, scale_w=108, gray=True)
    black = [round(t, 1) for t, im in fr if im.mean() < 12]
    frozen, run = [], 0
    for (t0, x0), (t1, x1) in zip(fr, fr[1:]):
        run = run + 1 if np.abs(x1.astype(int) - x0.astype(int)).mean() < 0.6 else 0
        if run == 10: frozen.append(round(t1 - 1.0, 1))
    res = {"black_frames": black, "frozen_1s_starts": frozen}
    json.dump(res, open(os.path.join(a.out, "watch_pack", "auto_checks.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(res)

if __name__ == "__main__":
    main()

