# -*- coding: utf-8 -*-
"""faces.py <mp4> [--t0] [--t1] [--crop x,y,w,h] [--fps 2]
사람 얼굴(정면) 찾기 — 회원 2026-11-07 '사람 얼굴 금지. 옆·뒷모습은 됨'.
YuNet(숏클 설치 모델 face_detection_yunet_2023mar.onnx)으로 얼굴을 찾고, 두 눈·코 자리로 정면/옆을 가른다.
정면 = 두 눈이 다 보이고 코가 두 눈 사이 가운데쯤(눈 사이 거리의 25~75%) · 눈 사이가 얼굴 폭의 25% 넘음."""
import os, sys, glob, argparse, subprocess, numpy as np, cv2

def _model():
    c = glob.glob(os.path.join(os.environ.get("LOCALAPPDATA", ""), "Shortem", "**", "face_detection_yunet*.onnx"), recursive=True)
    if not c: raise SystemExit("멈춤: 얼굴 찾기 모델 없음(face_detection_yunet)")
    return c[0]

_det = {}
def detector(w, h):
    k = (w, h)
    if k not in _det:
        _det[k] = cv2.FaceDetectorYN.create(_model(), "", (w, h), 0.7, 0.3, 5000)
    return _det[k]

def frames(mp4, t0, t1, crop=None, fps=2, W=640):
    vf = []
    if crop: vf.append("crop=%d:%d:%d:%d" % (crop[2], crop[3], crop[0], crop[1]))
    vf += [f"fps={fps}", f"scale={W}:-2"]
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{max(0.05, t1 - t0):.3f}", "-i", mp4, "-vf", ",".join(vf), "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    raw = subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL).stdout
    pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", mp4], capture_output=True).stdout.decode().strip().split(",")
    cw, ch = (crop[2], crop[3]) if crop else (int(pr[0]), int(pr[1]))
    H = int(round(ch * W / cw / 2)) * 2
    n = len(raw) // (W * H * 3)
    return [(t0 + i / fps, np.frombuffer(raw[i * W * H * 3:(i + 1) * W * H * 3], np.uint8).reshape(H, W, 3)) for i in range(n)], W, H

def faces(mp4, t0, t1, crop=None, fps=2):
    fr, W, H = frames(mp4, t0, t1, crop, fps)
    out = []
    for t, im in fr:
        _, f = detector(W, H).detect(im)
        if f is None: continue
        for r in f:
            x, y, w, h = r[:4]; rex, rey, lex, ley, nx, ny = r[4:10]; sc = r[14]
            eye = abs(lex - rex)
            mid = (nx - min(rex, lex)) / (eye + 1e-6)
            frontal = eye > 0.25 * w and 0.25 <= mid <= 0.75
            out.append({"t": round(t, 2), "score": round(float(sc), 2), "frontal": bool(frontal), "box": [int(x), int(y), int(w), int(h)], "frame_h": H})
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("mp4"); ap.add_argument("--t0", type=float, default=0); ap.add_argument("--t1", type=float)
    ap.add_argument("--crop"); ap.add_argument("--fps", type=float, default=2); a = ap.parse_args()
    t1 = a.t1 or float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.mp4], capture_output=True).stdout.decode())
    crop = [int(x) for x in a.crop.split(",")] if a.crop else None
    hits = faces(a.mp4, a.t0, t1, crop, a.fps)
    sec = {}
    for h in hits:
        if h["frontal"]: sec[int(h["t"])] = 1
    print("정면 얼굴 초:", sorted(sec))
