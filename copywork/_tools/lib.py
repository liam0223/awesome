# -*- coding: utf-8 -*-
"""공용 재는 함수 한 벌 — 벤치와 우리 영상에 똑같이 쓴다(지침 §1-6).
window · cuts · loud · asr · caption_track · ink · color · de"""
import subprocess, json, os, re, io, math, hashlib, statistics
import numpy as np
from PIL import Image

W, H = 1080, 1920

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL)
    return r.returncode, r.stdout, r.stderr.decode("utf-8", "replace")

def duration(mp4):
    c, o, e = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4])
    return float(o.decode().strip())

def fps_of(mp4):
    c, o, e = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", mp4])
    n, d = o.decode().strip().split("/")
    return float(n) / float(d)

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def frames(mp4, fps=10.0, scale_w=None, t0=0.0, t1=None, gray=False, crop=None):
    """(t, ndarray) 목록. crop=(x,y,w,h) 원본 좌표."""
    vf = [f"fps={fps}"]
    if crop:
        vf.append(f"crop={crop[2]}:{crop[3]}:{crop[0]}:{crop[1]}")
    if scale_w:
        vf.append(f"scale={scale_w}:-2")
    pix = "gray" if gray else "rgb24"
    args = ["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}"]
    if t1 is not None:
        args += ["-t", f"{t1 - t0:.3f}"]
    args += ["-i", mp4, "-vf", ",".join(vf), "-f", "rawvideo", "-pix_fmt", pix, "-"]
    # 크기 알아내기
    c, o, e = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", mp4])
    w0, h0 = [int(x) for x in o.decode().strip().split(",")[:2]]
    if crop:
        w0, h0 = crop[2], crop[3]
    if scale_w:
        h0 = int(round(h0 * scale_w / w0 / 2)) * 2; w0 = scale_w
    ch = 1 if gray else 3
    c, o, e = run(args)
    n = len(o) // (w0 * h0 * ch)
    arr = np.frombuffer(o[: n * w0 * h0 * ch], np.uint8).reshape(n, h0, w0, ch) if ch == 3 else np.frombuffer(o[: n * w0 * h0], np.uint8).reshape(n, h0, w0)
    return [(t0 + i / fps, arr[i]) for i in range(n)]

def frame(mp4, t):
    c, o, e = run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", mp4, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"])
    return np.array(Image.open(io.BytesIO(o)).convert("RGB"))

# ---------- 영상 창 · 고정 띠 (§2-2-1 ⑥) ----------
def window(mp4):
    fr = frames(mp4, fps=2, gray=True)
    st = np.stack([f for _, f in fr]).astype(np.float32)
    row_std = st.std(axis=0).mean(axis=1)   # 줄마다 시간 표준편차
    col_std = st.std(axis=0).mean(axis=0)
    thr = max(4.0, float(np.percentile(row_std, 50)) * 0.25)
    rows = np.where(row_std > thr)[0]; cols = np.where(col_std > thr)[0]
    y0, y1 = int(rows.min()), int(rows.max()) + 1
    x0, x1 = int(cols.min()), int(cols.max()) + 1
    mean = st.mean(axis=0)
    # 창 밖 고정 줄(띠) — 위쪽
    above = []
    fixed = row_std < thr
    i = 0
    while i < y0:
        if fixed[i] and mean[i].mean() > 0:
            j = i
            while j < y0 and fixed[j]:
                j += 1
            above.append([i, j]); i = j
        else:
            i += 1
    rgb = frames(mp4, fps=1)
    bg = np.median(np.stack([f[:max(1, y0)].reshape(-1, 3) if y0 > 0 else f[:2].reshape(-1, 3) for _, f in rgb]), axis=(0, 1)).astype(int).tolist()
    return {"window": [x0, y0, x1 - x0, y1 - y0], "above_bands": above, "bg_rgb": bg, "row_std_thr": round(thr, 2)}

# ---------- 컷 (§2-2-1 ⑦) ----------
def cuts(mp4, win=None, thr=0.3):
    vf = []
    if win:
        x, y, w, h = win
        vf.append(f"crop={w // 2 * 2}:{h // 2 * 2}:{x}:{y}")
    vf.append(f"select='gt(scene,{thr})',showinfo")
    c, o, e = run(["ffmpeg", "-hide_banner", "-i", mp4, "-vf", ",".join(vf), "-an", "-f", "null", "-"])
    ts = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", e)]
    merged = []
    for t in ts:
        if not merged or t - merged[-1] > 0.2:
            merged.append(round(t, 3))
    dur = duration(mp4)
    b = [0.0] + merged + [dur]
    shots = [round(b[i + 1] - b[i], 3) for i in range(len(b) - 1)]
    def pct(a, p):
        return round(float(np.percentile(a, p)), 3)
    return {"times": merged, "shots": len(shots), "shot_len": {"median": pct(shots, 50), "p10": pct(shots, 10), "p90": pct(shots, 90), "min": min(shots), "max": max(shots)},
            "first_cut": merged[0] if merged else None, "cut_per_min": round(len(merged) / dur * 60, 2), "shot_list": shots, "thr": thr}

# ---------- 소리 ----------
def pcm(mp4, sr=16000, ch=1):
    c, o, e = run(["ffmpeg", "-v", "error", "-i", mp4, "-ac", str(ch), "-ar", str(sr), "-f", "s16le", "-"])
    return np.frombuffer(o, np.int16).astype(np.float32) / 32768.0

def loud(mp4):
    c, o, e = run(["ffmpeg", "-hide_banner", "-nostats", "-i", mp4, "-af", "ebur128=peak=true", "-f", "null", "-"])
    tail = e[e.rfind("Summary:"):]
    I = float(re.search(r"I:\s+(-?[0-9.]+) LUFS", tail).group(1))
    LRA = float(re.search(r"LRA:\s+(-?[0-9.]+) LU", tail).group(1))
    tp = re.search(r"Peak:\s+(-?[0-9.inf]+) dBFS", tail)
    TP = float(tp.group(1)) if tp else None
    mom = [float(x) for x in re.findall(r"M:\s*(-?[0-9.]+)", e)]
    x = pcm(mp4, 16000)
    def rms_db(seg):
        r = math.sqrt(float(np.mean(seg ** 2)) + 1e-12); return round(20 * math.log10(r + 1e-9), 1)
    w = 4000
    rms025 = [rms_db(x[i:i + w]) for i in range(0, len(x) - w + 1, w)]
    # 10ms RMS 솟음(효과음 후보)
    w10 = 160
    r10 = np.array([rms_db(x[i:i + w10]) for i in range(0, len(x) - w10 + 1, w10)])
    spikes = []
    for i in range(5, len(r10)):
        base = float(np.median(r10[max(0, i - 30):i]))
        if r10[i] - base > 12 and r10[i] > -30 and (not spikes or i * 0.01 - spikes[-1]["t"] > 0.15):
            spikes.append({"t": round(i * 0.01, 2), "db": float(r10[i])})
    return {"I": I, "TP": TP, "LRA": LRA, "rms_025": rms025, "momentary_04": mom[::4][:400], "spikes": spikes}

_WM = None
def asr(mp4, cache_dir=None):
    """위스퍼(로컬) 받아쓰기 — 낱말 시각. 같은 파일(sha256)은 다시 안 돌린다. 엔진 표시: 위스퍼(낱말 시각 정밀도 낮음)."""
    out = mp4 + ".asr.json"
    sh = sha256(mp4)
    if os.path.exists(out):
        d = json.load(open(out, encoding="utf-8"))
        if d.get("sha256") == sh:
            return d
    global _WM
    from faster_whisper import WhisperModel
    if _WM is None:
        _WM = WhisperModel(r"C:\Users\kgari\AppData\Local\Shortem\models\whisper\small", device="cpu", compute_type="int8")
    audio = pcm(mp4, 16000)  # 내장 av 판이 맞지 않아 ffmpeg 로 직접 푼 소리를 넘긴다
    segs, info = _WM.transcribe(audio, language="ko", word_timestamps=True, vad_filter=False, beam_size=5)
    words, segments = [], []
    for s in segs:
        segments.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(), "speaker": "미측정 — 위스퍼는 화자 나누기 없음"})
        for wd in (s.words or []):
            words.append({"t0": round(wd.start, 2), "t1": round(wd.end, 2), "text": wd.word.strip()})
    d = {"engine": "위스퍼 small 로컬(낱말 시각 정밀도 낮음)", "sha256": sh, "words": words, "segments": segments}
    json.dump(d, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return d

# ---------- 자막(흰 글 + 검은 외곽) ----------
def outlined_white_mask(img, white=225, dark=60, r=4):
    """흰 글자 픽셀 중 가까이(r px)에 검은 외곽이 있는 것."""
    g = img.mean(axis=2) if img.ndim == 3 else img
    sat = (img.max(axis=2).astype(int) - img.min(axis=2).astype(int)) if img.ndim == 3 else np.zeros_like(g)
    wm = (g > white) & (sat < 40)
    dm = g < dark
    from scipy_free import dilate
    return wm & dilate(dm, r)

def ink_bbox(mask):
    ys, xs = np.where(mask)
    if len(ys) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]

def caption_track(mp4, band, fps=10.0, min_px=150):
    """band=(y0,y1) 안 흰 외곽 글자를 0.1초마다 → 덩어리(바뀔 때마다 새 행)."""
    fr = frames(mp4, fps=fps, crop=(0, band[0], W, band[1] - band[0]))
    masks = [(t, outlined_white_mask(f)) for t, f in fr]
    segs, cur = [], None
    prev = None
    for t, m in masks:
        on = m.sum() >= min_px
        if on and prev is not None and cur is not None:
            inter = (m & prev).sum(); uni = (m | prev).sum()
            same = uni > 0 and inter / uni > 0.55
        else:
            same = False
        if on and cur is not None and same:
            cur["t1"] = round(t + 1 / fps, 2); cur["n"] += 1
        else:
            if cur is not None:
                segs.append(cur)
            cur = None
            if on:
                bb = ink_bbox(m)
                cur = {"t0": round(t, 2), "t1": round(t + 1 / fps, 2), "n": 1,
                       "bbox": [bb[0], bb[1] + band[0], bb[2], bb[3] + band[0]]}
        prev = m if on else None
    if cur is not None:
        segs.append(cur)
    return segs

# ---------- 잉크 재기 (§1-6 ink.py) ----------
def ink(img, y0, y1, x0=0, x1=None):
    crop = img[y0:y1, x0:x1]
    m = outlined_white_mask(crop)
    bb = ink_bbox(m)
    if not bb:
        return None
    sub = m[bb[1]:bb[3], bb[0]:bb[2]]
    # 획 두께 = 가로줄 연속 흰 길이 중앙
    runs = []
    for row in sub[:: max(1, sub.shape[0] // 20)]:
        r = 0
        for v in row:
            if v:
                r += 1
            elif r:
                runs.append(r); r = 0
    # 외곽선 두께 = 흰 글 바깥 검은 띠 폭(가로 스캔)
    g = crop.mean(axis=2)
    outl = []
    for yy in range(bb[1], bb[3], max(1, (bb[3] - bb[1]) // 10)):
        row = g[yy]; mrow = m[yy]
        xs = np.where(mrow)[0]
        if len(xs):
            xl = xs.min(); s = 0
            while s < 3 and xl - s - 1 >= 0 and row[xl - s - 1] >= 90:  # 경계 번짐(안티에일리어스) 2~3px 건너뜀
                s += 1
            k = 0
            while xl - s - k - 1 >= 0 and row[xl - s - k - 1] < 60:
                k += 1
            if k:
                outl.append(k)
    cols = sub.any(axis=0)
    gaps, r = [], 0
    for v in cols:
        if not v:
            r += 1
        elif r:
            gaps.append(r); r = 0
    return {"x_center": round((bb[0] + bb[2]) / 2 + x0, 1), "x0": bb[0] + x0, "x1": bb[2] + x0, "y0": bb[1] + y0, "y1": bb[3] + y0,
            "h": bb[3] - bb[1], "w": bb[2] - bb[0], "stroke_px": float(np.median(runs)) if runs else None,
            "outline_px": float(np.median(outl)) if outl else None,
            "letter_gap_px": float(np.median(gaps)) if gaps else None, "ink_ratio": round(float(sub.mean()), 3)}

# ---------- 색 ----------
def hexc(rgb):
    return "#%02X%02X%02X" % tuple(int(v) for v in rgb)

def color(img, x0, y0, x1, y1):
    c = img[y0:y1, x0:x1].reshape(-1, 3).astype(int)
    mx, mn = c.max(1), c.min(1); sat = mx - mn
    bright_low = c[(mx > 200) & (sat < 40)]
    colorful = c[(sat > 80) & (mx > 120)]
    dark = c[mx < 50]
    out = {}
    if len(colorful) > 30:
        out["fill_hex"] = hexc(np.median(colorful, 0))
    elif len(bright_low):
        out["fill_hex"] = hexc(np.median(bright_low, 0))
    if len(dark):
        out["outline_hex"] = hexc(np.median(dark, 0))
    return out

def de(h1, h2):
    def lab(h):
        r, g, b = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        f = lambda c: ((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92
        r, g, b = f(r), f(g), f(b)
        X = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
        Y = 0.2126 * r + 0.7152 * g + 0.0722 * b
        Z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
        ff = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
        return 116 * ff(Y) - 16, 500 * (ff(X) - ff(Y)), 200 * (ff(Y) - ff(Z))
    a, b = lab(h1), lab(h2)
    return round(math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b))), 2)
