# -*- coding: utf-8 -*-
"""sheet.py <mp4> <간격초> [--out <jpg>] [--cols 6] [--w 270] [--t0 0] [--t1 끝]
시각 글자를 찍은 프레임 시트. strip.py / frame.py 도 같은 모듈에 있다(공용 함수)."""
import subprocess, sys, os, argparse, io, json
from PIL import Image, ImageDraw, ImageFont

def duration(mp4):
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                       capture_output=True, stdin=subprocess.DEVNULL).stdout.decode()
    return float(o.strip())

def frame_at(mp4, t, w=None):
    vf = ["-vf", f"scale={w}:-2"] if w else []
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", mp4, "-frames:v", "1", *vf, "-f", "image2pipe", "-vcodec", "png", "-"],
                       capture_output=True, stdin=subprocess.DEVNULL)
    if not r.stdout:
        return None
    return Image.open(io.BytesIO(r.stdout)).convert("RGB")

def frames_fps(mp4, t0, t1, step, w=None, crop=None):
    """t0~t1 을 step 간격으로 한 번에 뽑는다(빠름). crop=(y0,y1)."""
    fps = 1.0 / step
    vf = f"fps={fps}"
    if crop:
        vf += f",crop=iw:{crop[1]-crop[0]}:0:{crop[0]}"
    if w:
        vf += f",scale={w}:-2"
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1-t0:.3f}", "-i", mp4, "-vf", vf,
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True, stdin=subprocess.DEVNULL)
    data, out, i = r.stdout, [], 0
    sig = b"\x89PNG\r\n\x1a\n"
    parts = data.split(sig)[1:]
    for p in parts:
        try:
            out.append(Image.open(io.BytesIO(sig + p)).convert("RGB"))
        except Exception:
            pass
    return out

def font(sz=20):
    for f in ["C:/Windows/Fonts/malgunbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()

def make_sheet(mp4, step, out, cols=6, w=270, t0=0.0, t1=None):
    t1 = t1 if t1 is not None else duration(mp4)
    ims = frames_fps(mp4, t0, t1, step, w=w)
    if not ims:
        raise SystemExit("프레임 없음")
    fw, fh = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (cols * fw, rows * fh), "black")
    d = ImageDraw.Draw(sh); f = font(max(14, w // 12))
    for i, im in enumerate(ims):
        x, y = (i % cols) * fw, (i // cols) * fh
        sh.paste(im, (x, y))
        t = t0 + i * step
        d.rectangle([x, y, x + w // 3, y + w // 9], fill="black")
        d.text((x + 3, y + 1), f"{t:.1f}", fill="yellow", font=f)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    sh.save(out, quality=88)
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("mp4"); ap.add_argument("step", type=float)
    ap.add_argument("--out"); ap.add_argument("--cols", type=int, default=6); ap.add_argument("--w", type=int, default=270)
    ap.add_argument("--t0", type=float, default=0.0); ap.add_argument("--t1", type=float)
    a = ap.parse_args()
    out = a.out or os.path.join(os.path.dirname(a.mp4), f"sheet_{a.step:g}s.jpg")
    print(make_sheet(a.mp4, a.step, out, a.cols, a.w, a.t0, a.t1))
