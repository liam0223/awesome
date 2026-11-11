# -*- coding: utf-8 -*-
"""motion.py <mp4> [--t0 0] [--t1 끝] [--crop x,y,w,h] [--step 0.5]
구간마다 움직임 값(앞뒤 그림 차이 평균 · 0~255) — 정지된 사진(움직임 ≈ 0)·사진 넘김을 걸러 내려고(회원 2026-11-07 '정지된 사진 사용 금지').
0.2 프레임 간격(5fps) 회색 축소 그림 차이. 값이 still_max 미만이면 정지로 본다."""
import sys, os, argparse, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(__file__))

def motion_series(mp4, t0=0.0, t1=None, crop=None, fps=5, w=160):
    vf = []
    if crop: vf.append("crop=%d:%d:%d:%d" % (crop[2], crop[3], crop[0], crop[1]))
    vf += [f"fps={fps}", f"scale={w}:-2", "format=gray"]
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}"] + (["-t", f"{t1 - t0:.3f}"] if t1 else []) + ["-i", mp4, "-vf", ",".join(vf), "-f", "rawvideo", "-"]
    r = subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL).stdout
    # 크기 알아내기
    pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", mp4], capture_output=True).stdout.decode().strip().split(",")
    W0, H0 = int(pr[0]), int(pr[1])
    cw, ch = (crop[2], crop[3]) if crop else (W0, H0)
    h = int(round(ch * w / cw / 2)) * 2
    n = len(r) // (w * h)
    if n < 2: return []
    a = np.frombuffer(r[: n * w * h], np.uint8).reshape(n, h, w).astype(np.int16)
    d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    return [(round(t0 + (i + 1) / fps, 2), float(v)) for i, v in enumerate(d)]

def still_frac(mp4, a, b, crop=None, still_max=0.6):
    s = motion_series(mp4, a, b, crop)
    if not s: return 1.0, 0.0
    v = np.array([x[1] for x in s])
    return float((v < still_max).mean()), float(np.median(v))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("mp4"); ap.add_argument("--t0", type=float, default=0); ap.add_argument("--t1", type=float)
    ap.add_argument("--crop"); ap.add_argument("--step", type=float, default=0.5); a = ap.parse_args()
    crop = [int(x) for x in a.crop.split(",")] if a.crop else None
    s = motion_series(a.mp4, a.t0, a.t1, crop)
    buck = {}
    for t, v in s: buck.setdefault(int(t / a.step), []).append(v)
    print(" ".join(f"{k * a.step:.1f}:{np.mean(v):.1f}" for k, v in sorted(buck.items())))
