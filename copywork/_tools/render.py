# -*- coding: utf-8 -*-
"""render.py <판.json> <08_make/<편>>
판 한 파일 + 편 폴더(대본.json · 재료.json · tts.mp3/tts_align.json) → final.mp4 · 자막표.json · timeline.json · run_log.json
값은 판에서만 읽는다(숫자 상수 금지 — 그리는 법만). 모르는 판 칸이 있으면 멈춘다."""
import sys, os, json, re, time, hashlib, subprocess, argparse, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import lib

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = json.load(open(os.path.join(HERE, "..", "_assets", "fonts.json"), encoding="utf-8-sig"))
KNOWN = {"name", "renderer", "version", "history", "_note", "bench", "voice", "cps_target", "cps_target_from", "tempo_fixed", "clip_speed", "still_max", "face_ban", "crop_min_h", "tempo_max", "tempo_max_from", "pause_max",
         "pause_max_from", "pause_trim_over", "pause_xfade", "pause_silence_db", "bgm", "orig_audio", "loudness", "length", "timing", "frame", "caption", "cuts", "sfx_files", "sfx_from", "placement", "rhythm",
         "title_form", "script", "source", "checks", "variables", "frozen_at"}

def J(p): return json.load(open(p, encoding="utf-8-sig"))
def font(name, px):
    key = os.path.splitext(name)[0]
    return ImageFont.truetype(FONTS[key], px)
def run(cmd, log, name):
    t = time.time(); r = subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL)
    log["steps"].append({"name": name, "sec": round(time.time() - t, 2)})
    if r.returncode != 0:
        raise SystemExit(f"멈춤: {name} 실패 — " + r.stderr.decode("utf-8", "replace")[-600:])
    return r
def hexrgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

# ---------- 글 그림 ----------
def text_png(text, fnt, fill, outline_px, outline_hex, shadow=None, box=None, pad=(0, 0), radius=0, erode=0):
    """글 한 줄을 RGBA 로. 돌려주는 값: (그림, 잉크 상자(그림 안), 잉크 위 끝 기준)."""
    l, t, r, b = fnt.getbbox(text)
    m = max(outline_px, (shadow or {}).get("blur", 0) * 2 + (shadow or {}).get("spread", 0)) + 6
    W = r - l + 2 * m + 2 * pad[0]; H = b - t + 2 * m + 2 * pad[1]
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ox, oy = m + pad[0] - l, m + pad[1] - t
    if box:
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([m, m, W - m, H - m], radius=radius, fill=hexrgb(box) + (255,))
    if shadow:
        sh = Image.new("L", (W, H), 0)
        ImageDraw.Draw(sh).text((ox, oy), text, font=fnt, fill=255, stroke_width=outline_px + shadow.get("spread", 0), stroke_fill=255)
        sh = sh.filter(ImageFilter.GaussianBlur(shadow["blur"] / 2))
        a = (np.array(sh).astype(np.float32) * shadow["alpha"]).astype(np.uint8)
        layer = Image.new("RGBA", (W, H), hexrgb(shadow["hex"]) + (0,)); layer.putalpha(Image.fromarray(a))
        im = Image.alpha_composite(im, layer)
    d = ImageDraw.Draw(im)
    if erode and outline_px:
        # 테를 글자 가장자리 안쪽까지 먹게(벤치 흰 획이 더 가늚): 테를 먼저 그리고, 흰 채움을 erode px 깎아 덮는다
        d.text((ox, oy), text, font=fnt, fill=hexrgb(outline_hex) + (255,), stroke_width=outline_px, stroke_fill=hexrgb(outline_hex) + (255,))
        fm = Image.new("L", (W, H), 0); ImageDraw.Draw(fm).text((ox, oy), text, font=fnt, fill=255)
        fm = fm.filter(ImageFilter.MinFilter(2 * erode + 1))
        lay = Image.new("RGBA", (W, H), hexrgb(fill) + (0,)); lay.putalpha(fm)
        im = Image.alpha_composite(im, lay)
    else:
        d.text((ox, oy), text, font=fnt, fill=hexrgb(fill) + (255,), stroke_width=outline_px, stroke_fill=hexrgb(outline_hex) + (255,) if outline_px else None)
    ink_top = oy + t  # 글자 잉크 위 끝(외곽 포함 전) ≈ oy + bbox top
    return im, ink_top

def glyph_check(texts, fnames):
    miss = []
    for fn in fnames:
        f = font(fn, 60)
        for t in texts:
            for ch in t:
                if ch == " ":
                    if f.getlength(" ") <= 0: miss.append((fn, "공백 폭 0"))
                    continue
                m = f.getmask(ch)
                if m.size[0] == 0 or m.getbbox() is None:
                    miss.append((fn, ch))
    return sorted(set(miss))

# ---------- 소리 ----------
def narration(ep, P, log):
    A = J(os.path.join(ep, "tts_align.json")); al = A["alignment"]
    cs, ce = al["character_start_times_seconds"], al["character_end_times_seconds"]
    sr = 44100
    c, o, e = lib.run(["ffmpeg", "-v", "error", "-i", os.path.join(ep, "tts.mp3"), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"])
    x = np.frombuffer(o, np.float32)
    pm, over, xf = P["pause_max"], P["pause_trim_over"], P["pause_xfade"]
    text = A["text"]
    # 소리는 한 덩어리로 두고, 긴 쉼(over 초 넘는 글자 사이 틈)의 가운데만 잘라 pm 초로 줄인다 — 자른 자리는 xf 초 겹쳐 섞는다(툭 끊김 방지)
    idx = [k for k in range(min(len(text), A["spans"][-1][1])) if not text[k].isspace() and k < len(cs)]   # 대본 글자만(tts 꼬리 '...' 뺌)
    first, last = cs[idx[0]], ce[idx[-1]]
    # 글자 시각(정렬)은 받침 끝소리보다 일찍 끝날 때가 있다 → 실제로 조용한 구간만 자른다(말끝 잘림 방지)
    win = int(0.01 * sr)
    env = np.sqrt(np.convolve(x.astype(np.float64) ** 2, np.ones(win) / win, mode="same"))
    thr = env.max() * 10 ** (P["pause_silence_db"] / 20)
    quiet = env < thr
    def quiet_run(a, b):
        i0, i1 = int(max(0, a) * sr), int(min(len(x) / sr, b) * sr)
        best, cur = (0, 0), None
        for i in range(i0, i1, win):
            if quiet[i]:
                cur = cur if cur is not None else i
                if i - cur > best[1] - best[0]: best = (cur, i)
            else:
                cur = None
        return best[0] / sr, best[1] / sr
    cuts_ = []
    for p_, q_ in zip(idx, idx[1:]):
        g0, g1 = ce[p_], cs[q_]
        if g1 - g0 > over:
            r0, r1 = quiet_run(g0 - 0.05, g1 + 0.05)
            if r1 - r0 > pm + 0.04:
                cuts_.append((r0 + pm / 2, r1 - pm / 2))
    if P.get("pause_scan_all"):
        # v3 는 쉼이 글자 시각 안(말끝 글자가 길게 잡힘)에 숨어 글자 사이 틈으로 안 잡힌다 → 처음~끝 사이 조용한 덩어리를 소리로 직접 찾는다
        i, cur = int(first * sr), None
        while i < int(last * sr):
            if quiet[i]:
                cur = cur if cur is not None else i
            else:
                if cur is not None and (i - cur) / sr > over and (i - cur) / sr > pm + 0.04:
                    r0, r1 = cur / sr, i / sr
                    if not any(a0 < r1 and r0 < a1 for a0, a1 in cuts_): cuts_.append((r0 + pm / 2, r1 - pm / 2))
                cur = None
            i += win
        cuts_.sort()
    keep, st = [], max(0.0, first - 0.03)
    for (r0, r1) in cuts_:
        keep.append((st, r0)); st = r1
    # 마지막 말소리가 실제로 끝난 뒤까지: 정렬 끝에서 앞으로 가며 0.1초 넘게 조용해지는 첫 자리 + 0.08초(꼬리 '...' 숨소리는 안 넣음)
    i, run_q, end_i = int(max(0, last - 0.1) * sr), 0, None
    while i < len(x):
        run_q = run_q + win if quiet[i] else 0
        if run_q >= int(0.1 * sr): end_i = i - run_q; break
        i += win
    end_t = max(last + 0.1, (end_i / sr + 0.08) if end_i is not None else len(x) / sr)
    keep.append((st, min(len(x) / sr, end_t)))
    log["narr_end_extra"] = round(end_t - last, 3)
    n_xf = int(xf * sr)
    y = x[int(keep[0][0] * sr): int(keep[0][1] * sr)].copy()
    starts_new = [0.0]
    for (u, v) in keep[1:]:
        seg = x[int(u * sr): int(v * sr)].copy()
        k = min(n_xf, len(y), len(seg))
        if k > 0:
            r = np.linspace(0, 1, k, dtype=np.float32)
            y[-k:] = y[-k:] * (1 - r) + seg[:k] * r
        starts_new.append(len(y) / sr - k / sr)
        y = np.concatenate([y, seg[k:]])
    nf = min(len(y), int(0.03 * sr)); y[-nf:] *= np.linspace(1, 0, nf, dtype=np.float32)   # 끝 딸깍 방지
    def remap(t):
        for j in range(len(keep) - 1, -1, -1):
            if t >= keep[j][0] - 1e-6:
                return starts_new[j] + min(t, keep[j][1]) - keep[j][0]
        return 0.0
    line_t = [[remap(cs[s]), remap(ce[e_ - 1])] for s, e_ in A["spans"]]
    log["pause_cuts"] = len(cuts_)
    raw = os.path.join(ep, "_narr_raw.wav")
    import wave
    with wave.open(raw, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    D = len(y) / sr
    D_ = J(os.path.join(ep, "대본.json"))
    chars = sum(len(L["display"].replace(" ", "")) for L in D_["lines"])
    T = chars / P["cps_target"]
    tempo = D / T
    log["tempo_wanted"] = round(tempo, 3)
    if P.get("tempo_fixed"):   # 회원 2026-11-07: 목소리는 항상 지난 편들 속도로(편마다 바꾸지 않음) — 길이는 대본 길이를 따른다
        tempo = P["tempo_fixed"]
    if tempo > P["tempo_max"] and P.get("tempo_cap"):   # 상한에서 멈추고 말속도 차이를 기록(검증 speech.cps ±10% 로 판정)
        log["not_done"].append(f"배속 {tempo:.2f} 이 상한 {P['tempo_max']} 넘음 — 상한으로 둠(말속도 벤치보다 느림)"); tempo = P["tempo_max"]
    if tempo > P["tempo_max"]:
        raise SystemExit(f"멈춤: 배속 {tempo:.2f} > 상한 {P['tempo_max']} — 쉼을 줄여도 길다. 대본을 줄인다")
    tempo = max(1.0, tempo)
    out = os.path.join(ep, "_narr.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"atempo={tempo:.4f}", "-ar", "48000", out], log, "나레 배속")
    line_t = [[a / tempo, b / tempo] for a, b in line_t]
    return out, line_t, round(tempo, 3), D / tempo

# ---------- 본체 ----------
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("pan"); ap.add_argument("ep"); a = ap.parse_args()
    P = J(a.pan); ep = a.ep
    unk = set(P) - KNOWN - {k for k in P if k.endswith("_from")}
    if unk:
        raise SystemExit(f"멈춤: 판에 모르는 칸 {sorted(unk)} — 조용히 버리지 않는다")
    D = J(os.path.join(ep, "대본.json")); M = J(os.path.join(ep, "재료.json"))
    log = {"steps": [], "paid": {"asr_min": 0, "tts_chars": 0, "tts_note": "tts.py 에서 따로 1회(캐시)"}, "not_done": []}
    fr, cap, tm = P["frame"], P["caption"]["layers"][0], P["timing"]
    # 렌더 전 관문
    texts = [L["display"] for L in D["lines"]] + D["title_card"]["lines"] + [D["cta"]["text"], fr["ad_mark"]["text"], fr["watermark"]["text"]]
    texts = [t for t in texts if t]
    miss = glyph_check(texts, [cap["font"], fr["title_card"]["font"], fr["cta"]["font"], fr["ad_mark"]["font"]])
    if miss:
        raise SystemExit(f"멈춤: 글꼴에 없는 글자 {miss[:10]}")
    for L in D["lines"]:
        if re.search(r"[/¦‖|]", L["read"]): raise SystemExit("멈춤: TTS 글 기호")
        if len(L["display"].replace(" ", "")) > P["caption"]["chunk_max_chars"]: raise SystemExit(f"멈춤: 조각 글자 넘침 {L['display']}")
    nar, line_t, tempo, ndur = narration(ep, P, log)
    off = tm["title_sec"]
    total = round(off + ndur + tm["tail"], 3)
    if not P["length"]["min"] <= total <= P["length"]["max"]:
        log["not_done"].append(f"길이 {total}초가 벤치 범위 밖")
    # 줄 시각: 목소리 시작 = 자막 시작, 다음 줄 시작까지(빈틈 = 판 gap)
    rows = []
    starts = [off + s for s, _ in line_t]
    for i, L in enumerate(D["lines"]):
        t0 = starts[i]; t1 = starts[i + 1] - P["timing"]["gap"] if i + 1 < len(starts) else total
        rows.append({"id": i, "kind": "해설", "t0": round(t0, 3), "t1": round(t1, 3), "text": L["display"], "enter": cap["enter"], "emph": [], "sticker": [], "sfx": None,
                     "voice": [round(off + line_t[i][0], 3), round(off + line_t[i][1], 3)]})
    # ---- 영상 토막 ----
    fps = 30
    tmp = os.path.join(ep, "_clips"); os.makedirs(tmp, exist_ok=True)
    plan = []
    plan.append((0.0, off, M["title"]))
    for i, segs in enumerate(M["lines"]):
        t0 = rows[i]["t0"]; t1 = rows[i]["t1"]
        if i == 0: t0 = off
        if segs == "cont":   # 앞 줄 장면을 이어 쓴다(한 컷이 두 줄에 걸침 — 벤치 긴 컷 p90)
            pt0, _, psegs = plan[-1]; plan[-1] = (pt0, t1, psegs); continue
        plan.append((t0, t1, segs))
    # 앞 줄 끝 = 다음 줄 시작으로 이어 붙인다(빈틈 없이 화면)
    cuts, clip_files = [], []
    shot_cache = {}
    def shots_of(src):
        if src not in shot_cache:
            ts_ = set(lib.cuts(os.path.join(ep, src))["times"])
            # ffmpeg scene 이 놓치는 장면 바뀜(비슷한 색 장면끼리) — 앞뒤 그림 차이가 둘레보다 크게 튀는 자리
            fr_ = lib.frames(os.path.join(ep, src), fps=30, gray=True, scale_w=180)
            dd = np.array([np.abs(fr_[i][1].astype(int) - fr_[i - 1][1].astype(int)).mean() for i in range(1, len(fr_))])
            for i, v in enumerate(dd):
                loc = np.median(np.concatenate([dd[max(0, i - 8):i], dd[i + 1:i + 9]])) if len(dd) > 1 else 0
                if v > max(P["source"]["shot_jump"]["min"], P["source"]["shot_jump"]["x_local"] * loc):
                    t_ = round(fr_[i + 1][0], 3)
                    if all(abs(t_ - x) > 0.2 for x in ts_): ts_.add(t_)
            shot_cache[src] = sorted(ts_)
        return shot_cache[src]
    import cv2
    BT = P["source"]["burned_text"]
    lab_cache = {}
    def blue_mask(im):
        r, g, bl = [im[..., k].astype(int) for k in range(3)]
        return ((bl > 170) & (r < 100) & (bl - r > 110) & (g > 90)).astype(np.uint8)
    def label_track(src):
        """원본에 박힌 파란 글 상자(원본 좌표) — 0.1초마다. 돌려줌: [(t, [상자…])] , 상자가 바뀌는 시각들"""
        if src not in lab_cache:
            fr_ = lib.frames(os.path.join(ep, src), fps=10)
            tr = []
            for t, im in fr_:
                m = blue_mask(im); bx = []
                if m.sum() > 300:
                    cnt, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
                    for k in range(1, cnt):
                        x, y, ww, hh, area = stats[k]
                        if area >= 200: bx.append([int(x), int(y), int(x + ww), int(y + hh)])
                tr.append((round(t, 3), bx))
            def uni(bx):
                return None if not bx else [min(b[0] for b in bx), min(b[1] for b in bx), max(b[2] for b in bx), max(b[3] for b in bx)]
            def same(u, v):
                if u is None or v is None: return u is None and v is None
                ix = max(0, min(u[2], v[2]) - max(u[0], v[0])) * max(0, min(u[3], v[3]) - max(u[1], v[1]))
                ar = lambda q: (q[2] - q[0]) * (q[3] - q[1])
                return ix / (ar(u) + ar(v) - ix + 1e-6) > 0.6
            # 바뀐 상태가 0.3초(3장) 이상 이어질 때만 바뀐 자리로 본다(깜빡임 무시)
            ch, cur = [], uni(tr[0][1]) if tr else None
            for i in range(1, len(tr)):
                u = uni(tr[i][1])
                if not same(u, cur) and all(same(uni(tr[j][1]), u) for j in range(i, min(len(tr), i + 3))):
                    ch.append(round((tr[i - 1][0] + tr[i][0]) / 2, 3)); cur = u
            lab_cache[src] = (tr, ch)
        return lab_cache[src]
    def bounds_of(src, labels=True):
        return sorted(set(shots_of(src)) | (set(label_track(src)[1]) if labels else set()))
    for (t0, t1, segs) in plan:
        dur = t1 - t0; k = len(segs); each = dur / k
        for s in segs:
            # 샷 경계·박힌 글 바뀌는 자리를 넘지 않게: [a,b] 안 경계로 나눈 조각 중 가장 긴 것, 모자라면 같은 토막 안에서 앞뒤로 늘린다
            allb = bounds_of(s["src"], labels=not s.get("crop")); sd = lib.duration(os.path.join(ep, s["src"]))
            bnd = [x for x in allb if s["a"] < x < s["b"]]
            pts = [s["a"]] + bnd + [s["b"]]
            best = max(zip(pts, pts[1:]), key=lambda p: p[1] - p[0])
            lo = max([x for x in allb if x <= best[0] + 1e-6] + [0.0]); hi = min([x for x in allb if x >= best[1] - 1e-6] + [sd])
            lo_ = lo + (0.05 if lo > 0 else 0); hi_ = hi - (0.05 if hi < sd else 0.08)
            a0 = max(best[0], lo_); b0 = min(best[1], hi_)
            if b0 - a0 < each:   # 같은 토막 안에서 뒤로, 그다음 앞으로 늘린다
                b0 = min(hi_, a0 + each)
                a0 = max(lo_, b0 - each)
            if bnd or (a0, b0) != (s["a"], s["b"]):
                log.setdefault("shot_fix", []).append({"src": s["src"], "was": [s["a"], s["b"]], "now": [round(a0, 3), round(b0, 3)], "boundaries": bnd})
            s = dict(s, a=round(a0, 3), b=round(b0, 3), lo=round(lo_, 3), hi=round(hi_, 3))
            avail = s["b"] - s["a"]
            speed = 1.0
            CS = P.get("clip_speed", {"min": 0.75, "max": 1.0})   # 회원 2026-11-07: 영상 속도 1~1.4 · 1 아래(느리게) 금지
            if each > avail:
                speed = avail / each
                if speed < CS["min"] - 1e-6:
                    raise SystemExit(f"멈춤: 재료 구간 짧음 {s['src']} {s['a']}~{s['b']} 필요 {each:.2f}초({CS['min']}배 아래로 느리게 할 수 없음 — 재료를 늘리거나 나눈다)")
            if speed > CS["max"] + 1e-6:
                raise SystemExit(f"멈춤: 영상 속도 {speed:.2f} > 상한 {CS['max']}")
            cuts.append({"t0": round(t0, 3), "t1": round(t0 + each, 3), "src": s["src"], "a": s["a"], "b": round(s["a"] + each * speed, 3), "speed": round(speed, 3),
                         "lo": s["lo"], "hi": s["hi"], "fit": s.get("fit"), "crop_fix": s.get("crop")})
            t0 += each
    # ---- 정지 사진 막기(회원 2026-11-07 '정지된 사진은 사용 금지') — 토막 안 움직임 중앙값이 판 still_max 미만이면 멈춤 ----
    if P.get("still_max"):
        import motion as _mo
        for c in cuts:
            fr_s, med = _mo.still_frac(os.path.join(ep, c["src"]), c["a"], c["b"], c.get("crop_fix"), P["still_max"])
            c["motion_med"] = round(med, 2)
            if med < P["still_max"]:
                raise SystemExit(f"멈춤: 정지 화면 {c['src']} {c['a']}~{c['b']} 움직임 {med:.2f} < {P['still_max']} — 움직이는 영상으로 바꾼다")
    # ---- 얼굴·과한 확대 막기(회원 2026-11-07 '사람 얼굴 금지 · 옆·뒷모습은 됨 · 화면 클로즈업으로 어색함') ----
    if P.get("face_ban"):
        import faces as _fa
        for c in cuts:
            hit = [h for h in _fa.faces(os.path.join(ep, c["src"]), c["a"], c["b"], c.get("crop_fix"), 2) if h["frontal"]]
            if hit:
                raise SystemExit(f"멈춤: 정면 얼굴 {c['src']} {c['a']}~{c['b']} ({hit[0]['t']}초) — 얼굴 없는 구간·창으로 바꾼다")
    if P.get("crop_min_h"):
        for c in cuts:
            cf = c.get("crop_fix")
            if cf and cf[3] < P["crop_min_h"]:
                raise SystemExit(f"멈춤: 확대가 큼 {c['src']} 창 높이 {cf[3]} < {P['crop_min_h']} — 넓은 창으로")
    # ---- 박힌 글 처리: 글 상자를 피해 화면을 잘라 확대(crop) → 안 되면 메우기(inpaint) ----
    TR = P["cuts"]["transition"]; xd = TR["ms"] / 1000.0 if "dissolve" in TR["kinds"] else 0.0
    def best_crop(boxes, W0, H0):
        """상자들과 겹치지 않는 9:16 창 중 가장 큰 것(같으면 가운데에 가까운 것). 없으면 None."""
        pad = BT["pad_px"]; B = [[x0 - pad, y0 - pad, x1 + pad, y1 + pad] for x0, y0, x1, y1 in boxes]
        hmin = int(H0 * BT["min_crop_h_frac"])
        for h in range(H0, hmin - 1, -8):
            w = int(round(h * 9 / 16));
            if w > W0: continue
            cand = []
            for y in range(0, H0 - h + 1, 4):
                for x in range(0, W0 - w + 1, 4):
                    if all(x + w <= b[0] or x >= b[2] or y + h <= b[1] or y >= b[3] for b in B):
                        cand.append((abs(x + w / 2 - W0 / 2) + abs(y + h / 2 - H0 / 2), x, y))
            if cand:
                _, x, y = min(cand); return [x, y, w, h]
        return None
    def clean_clip(c, pre, post, out):
        """원본 구간 → 1080×1920 30fps. 앞뒤로 pre/post 초를 더 만든다(장면 녹여 잇기용 — 같은 토막 밖은 첫/끝 그림 유지)."""
        src = os.path.join(ep, c["src"])
        n_out = int(round((c["t1"] - c["t0"] + pre + post) * fps))
        ts = [min(c["hi"], max(c["lo"], c["a"] + (k / fps - pre) * c["speed"])) for k in range(n_out)]
        s0, s1 = min(ts), max(ts)
        fr_ = lib.frames(src, fps=fps, t0=s0, t1=s1 + 0.1)
        H0, W0 = fr_[0][1].shape[:2]
        if c.get("crop_fix"):
            # 재료에 직접 정한 9:16 창(원본에 박힌 흰 글·카드 등 파란 상자 밖의 글을 피함 — 눈으로 정함)
            boxes = []; crop = c["crop_fix"]
        else:
            tr, _ = label_track(c["src"])
            boxes = [b for t, bx in tr if s0 - 0.05 <= t <= s1 + 0.05 for b in bx]
            crop = best_crop(boxes, W0, H0) if boxes else None
        if crop is None:
            # 상자가 없거나 상자를 피한 창이 없으면 화면 가득(9:16 가운데)
            w = min(W0, int(round(H0 * 9 / 16))); crop0 = [(W0 - w) // 2, 0, w, H0]
        c["crop"] = crop; c["inpaint"] = bool(boxes) and crop is None
        if c["inpaint"]:
            log["not_done"].append(f"박힌 글을 피해 자를 창이 없음 — 메우기 {c['t0']}~{c['t1']}초")
        x, y, w, h = crop if crop else crop0
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", str(fps), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for st in ts:
            fi = min(len(fr_) - 1.0, max(0.0, (st - s0) * fps))
            i0 = int(fi); i1 = min(len(fr_) - 1, i0 + 1); wt = fi - i0
            if c["speed"] < 1 and wt > 0.05 and i1 != i0:
                # 느리게 쓸 때 같은 그림이 두 번 나와 툭툭 끊기지 않게: 앞뒤 그림을 섞는다
                im = (fr_[i0][1].astype(np.float32) * (1 - wt) + fr_[i1][1].astype(np.float32) * wt).astype(np.uint8)
            else:
                im = fr_[int(round(fi))][1]
            if c["inpaint"]:
                m = blue_mask(im)
                cnt, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
                mask = np.zeros_like(m)
                for k in range(1, cnt):
                    bx_, by_, bw_, bh_, area = stats[k]
                    if area >= 200: cv2.rectangle(mask, (bx_ - 6, by_ - 6), (bx_ + bw_ + 6, by_ + bh_ + 6), 1, -1)
                im = cv2.inpaint(np.ascontiguousarray(im), mask * 255, 7, cv2.INPAINT_TELEA)
            im = np.ascontiguousarray(im[y:y + h, x:x + w])
            im = cv2.resize(im, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
            p.stdin.write(im.tobytes())
        p.stdin.close(); p.wait()
        return n_out
    for ci, c in enumerate(cuts):
        src = os.path.join(ep, c["src"])
        wh = [int(v) for v in lib.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", src])[1].decode().strip().split(",")[:2]]
        h0 = min(wh)   # 세로 영상도 짧은 변으로(회원 2026-11-07 '화질 720 이하 금지')
        if h0 < P["source"]["min_h"]: raise SystemExit(f"멈춤: 원본 화질 {h0}p < {P['source']['min_h']}p")
        out = os.path.join(tmp, f"c{ci:02d}.mp4")
        pre = xd / 2 if ci > 0 else 0.0; post = xd / 2 if ci < len(cuts) - 1 else 0.0
        tt = time.time()
        clean_clip(c, pre, post, out)
        log["steps"].append({"name": f"토막 {ci}", "sec": round(time.time() - tt, 2)})
        clip_files.append(out)
    base = os.path.join(ep, "_base.mp4")
    if xd > 0 and len(clip_files) > 1:
        # 장면 녹여 잇기(디졸브): 컷 시각 가운데로 xd 초 겹침
        args = ["ffmpeg", "-v", "error", "-y"]
        for f in clip_files: args += ["-i", f]
        fx, last = "", "0:v"
        for k in range(1, len(clip_files)):
            off_k = cuts[k]["t0"] - xd / 2
            fx += f"[{last}][{k}:v]xfade=transition={TR['xfade']}:duration={xd:.3f}:offset={off_k:.3f}[x{k}];"
            last = f"x{k}"
        run(args + ["-filter_complex", fx.rstrip(";"), "-map", f"[{last}]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(fps), base], log, "토막 잇기(녹여)")
    else:
        lst = os.path.join(tmp, "list.txt")
        open(lst, "w", encoding="utf-8").write("".join(f"file '{os.path.abspath(f)}'\n".replace("\\", "/") for f in clip_files))
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base], log, "토막 잇기")
    # ---- 덧그림(PNG) ----
    ov = os.path.join(ep, "_ov"); os.makedirs(ov, exist_ok=True)
    layers = []  # (png, x, y, t0, t1)
    tc = fr["title_card"]; ft = font(tc["font"], tc["px"])
    tl = D["title_card"]["lines"]; col = tc["color"]; cl = D["title_card"].get("colored_line", tc["colored_line"])
    ims = [text_png(t, ft, col if (j + 1) == cl else tc["white"], tc["outline_px"], "#000000")[0] for j, t in enumerate(tl)]
    hh = [ft.getbbox(t)[3] - ft.getbbox(t)[1] for t in tl]
    block = sum(hh) + tc["line_gap_px"]
    cy = (P["variables"].get("title_center_y") or tc["center_y"])
    ytop = cy - block / 2
    for j, im in enumerate(ims):
        p = os.path.join(ov, f"title{j}.png"); im.save(p)
        _, ink_top = text_png(tl[j], ft, "#FFFFFF", tc["outline_px"], "#000000")
        y = int(ytop + sum(hh[:j]) + j * tc["line_gap_px"] - ink_top)
        layers.append((p, int(540 - im.width / 2), y, 0.0, off))
    fc = font(cap["font"], cap["px"])
    for r in rows:
        im, ink_top = text_png(r["text"], fc, cap["fill"], cap["outline"]["px"], cap["outline"]["hex"], shadow=cap["shadow"], erode=cap.get("fill_erode_px", 0))
        ink_top += cap.get("fill_erode_px", 0)
        p = os.path.join(ov, f"cap{r['id']:02d}.png"); im.save(p)
        r["y_ink_top"] = cap["ink_top"]
        layers.append((p, int(cap["x"] - im.width / 2), int(cap["ink_top"] - ink_top), r["t0"], r["t1"]))
    am = fr["ad_mark"]; fa = font(am["font"], am["px"])
    im, ink_top = text_png(am["text"], fa, am["fill"], 0, "#000000")
    p = os.path.join(ov, "ad.png"); im.save(p)
    bxa = am["box"]
    layers.append((p, int((bxa[0] + bxa[2]) / 2 - im.width / 2), int(bxa[1] - ink_top), 0.0, total))
    ct = fr["cta"]; sty = ct["styles"][ct["style"]]; fcta = font(ct["font"], ct["px"])
    l_, t_, r_, b_ = fcta.getbbox(D["cta"]["text"])
    pad_y = (ct["box_h"] - (b_ - t_)) // 2
    im, _ = text_png(D["cta"]["text"], fcta, sty["fill"], 0, "#000000", box=sty["box"], pad=(ct["pad_x"], pad_y), radius=ct["radius"])
    p = os.path.join(ov, "cta.png"); im.save(p)
    cta_t0 = round(total * ct["start_frac"], 2)
    layers.append((p, int(540 - im.width / 2), int(ct["center_y"] - im.height / 2), cta_t0, total))
    rows.append({"id": len(rows), "kind": "제품구입띠", "t0": cta_t0, "t1": total, "text": D["cta"]["text"], "enter": "cut", "emph": [], "sticker": [], "sfx": None})
    rows.insert(0, {"id": -1, "kind": "제목", "t0": 0.0, "t1": off, "text": " / ".join(tl), "enter": "cut", "emph": [{"word": tl[cl - 1], "hex": col}], "sticker": [], "sfx": None})
    wm = fr["watermark"]
    if wm["text"]:
        # 워터마크: 글 한 줄, 흰색, 투명도 alpha — 제품구입 띠 바로 위(띠 위 끝 − gap_above 에 잉크 아래 끝)
        fw = font(wm["font"], wm["px"])
        im, ink_top = text_png(wm["text"], fw, wm.get("fill", "#FFFFFF"), wm.get("outline_px", 0), "#000000")
        a_ = np.array(im); a_[..., 3] = (a_[..., 3].astype(np.float32) * wm["alpha"]).astype(np.uint8); im = Image.fromarray(a_)
        p = os.path.join(ov, "wm.png"); im.save(p)
        l_w, t_w, r_w, b_w = fw.getbbox(wm["text"])
        cta_top = ct["center_y"] - ct["box_h"] / 2
        y_ink_bottom = cta_top - wm["gap_above_cta"]
        y = int(y_ink_bottom - (b_w - t_w) - ink_top)
        layers.append((p, int(540 - im.width / 2), y, 0.0, total))
    # ---- 소리 섞기 ----
    bg = J(os.path.join(HERE, "..", "_assets", "bgm_list.json")); bid = D.get("bgm", {}).get("id") or P["bgm"]["id"]
    if bid not in P["bgm"]["pool"]: raise SystemExit(f"멈춤: 배경음 {bid} 가 판 bgm.pool 에 없음")
    bgi = next(b for b in bg if b["id"] == bid); log["bgm"] = {"id": bid, "credit": bgi["credit"]}
    bgm = os.path.join(HERE, "..", bgi["file"].replace("_assets/", "_assets/"))
    bgm = os.path.normpath(os.path.join(HERE, "..", bgi["file"]))
    nl = lib.loud(nar)["I"]
    bl = lib.loud(bgm)["I"]
    gain_bgm = (nl - P["bgm"]["db_below_voice"]) - bl
    mix = os.path.join(ep, "_mix.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", nar, "-i", bgm, "-filter_complex",
         f"[0:a]adelay={int(off * 1000)}|{int(off * 1000)},apad=whole_dur={total}[n];"
         f"[1:a]atrim=0:{total},asetpts=PTS-STARTPTS,volume={gain_bgm:.2f}dB,afade=t=out:st={total - P['bgm']['fade_out']:.2f}:d={P['bgm']['fade_out']}[b];"
         f"[n][b]amix=inputs=2:normalize=0:duration=first[m]", "-map", "[m]", "-ac", "2", "-ar", "48000", mix], log, "소리 섞기")
    I0 = lib.loud(mix)["I"]
    g = P["loudness"]["lufs"] - I0
    mixn = os.path.join(ep, "_mixn.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", mix, "-af", f"volume={g:.2f}dB,alimiter=limit={10 ** (P['loudness']['tp'] / 20):.4f}:level=false", mixn], log, "음량 맞추기")
    # ---- 합치기 ----
    args = ["ffmpeg", "-v", "error", "-y", "-i", base]
    for (p_, x, y, t0, t1) in layers:
        args += ["-loop", "1", "-i", p_]
    args += ["-i", mixn]
    fcx, last = "", "0:v"
    for k, (p_, x, y, t0, t1) in enumerate(layers):
        fcx += f"[{last}][{k + 1}:v]overlay={x}:{y}:enable='between(t,{t0:.3f},{t1 - 0.001:.3f})':shortest=1[v{k}];"
        last = f"v{k}"
    fcx = fcx.rstrip(";")
    final = os.path.join(ep, "final.mp4")
    run(args + ["-filter_complex", fcx, "-map", f"[{last}]", "-map", f"{len(layers) + 1}:a", "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-pix_fmt", "yuv420p", "-r", str(fps), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final], log, "합치기")
    md5 = hashlib.md5(open(final, "rb").read()).hexdigest()
    json.dump({"rows": rows, "transitions": [{"t": c["t0"], "kind": ("dissolve" if xd > 0 else "cut"), "ms": int(xd * 1000)} for c in cuts[1:]]}, open(os.path.join(ep, "자막표.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"cuts": cuts, "total": total, "tempo": tempo}, open(os.path.join(ep, "timeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ldf = lib.loud(final)
    log.update({"pan": os.path.abspath(a.pan), "pan_version": P.get("version"), "total": total, "tempo": tempo, "bgm_gain_db": round(gain_bgm, 2), "lufs": ldf["I"], "tp": ldf["TP"], "md5": md5})
    log["not_done"] += ["소리를 귀로 들어 보지 않음(클로드는 들을 수 없음 — 회원 판정 때 들어 달라고 할 것)"]
    json.dump(log, open(os.path.join(ep, "run_log.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("완성", final, "길이", total, "배속", tempo, "LUFS", ldf["I"], "TP", ldf["TP"], "토막", len(cuts))

if __name__ == "__main__":
    main()
