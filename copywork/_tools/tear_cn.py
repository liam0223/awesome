# -*- coding: utf-8 -*-
"""뜯기(창 위 띠 + 흰 자막 띠 꼴): tear_cn.py <02_source/<id>.mp4> --out <03_tear/<id>>
클릭노트처럼 위 짙은 띠(로고·[광고]·제목 줄) + 그 아래 흰 자막 띠(검은 글) + 영상 창 꼴을 잰다.
부록 A-2 꼴 뜯기.json — 기계값만(글·역할 판독은 줄판독). 공용 함수는 lib(우리 편에도 같은 함수)."""
import sys, os, json, argparse, datetime
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import lib
from tear import f0_estimate


def runs(mask):
    out, s = [], None
    for i, v in enumerate(list(mask) + [False]):
        if v and s is None: s = i
        if not v and s is not None: out.append([s, i]); s = None
    return out


def layout(mp4, dur):
    """본편(표지 뒤) 2fps 프레임으로 고정 띠를 잰다."""
    fr = lib.frames(mp4, fps=2, t0=min(4.0, dur * 0.3), t1=dur - 0.3)
    st = np.stack([f for _, f in fr]).astype(np.float32)          # n,h,w,3
    g = st.mean(3)
    row_std = g.std(0).mean(1)
    med = np.median(st, 0)                                         # h,w,3
    rowmed = np.median(med, 1)                                     # h,3
    # 흰 자막 띠: 줄 가운데값이 거의 흰색(>=240 세 채널)이고 위쪽 900px 안
    # (줄 가운데값만 보면 파란 강조 낱말이 걸친 줄을 놓친다 → 흰 픽셀 비율 0.5 이상인 줄)
    white = ((med.min(2) >= 235).mean(1) >= 0.15)
    wr = [r for r in runs(white[:1100]) if r[1] - r[0] >= 60]
    band = max(wr, key=lambda r: r[1] - r[0]) if wr else None
    # 위 짙은 띠: 0 ~ 흰 띠 위 끝
    top = [0, band[0]] if band else None
    top_rgb = np.median(med[5:max(6, (band[0] if band else 300) - 5), :60].reshape(-1, 3), 0).astype(int).tolist() if band else None
    # 영상 창: 흰 띠 아래 끝 ~ 1920 (줄 표준편차가 큰 곳 시작)
    thr = max(4.0, float(np.percentile(row_std, 50)) * 0.25)
    y_win = band[1] if band else int(np.where(row_std > thr)[0].min())
    while y_win < 1919 and row_std[y_win] < thr:
        y_win += 1
    # 위 띠 안 글 줄(밝은 글): 줄마다 밝은 픽셀 수
    text_rows = []
    if top:
        tb = g.mean(0)[top[0]:top[1]]
        bright = (tb > 120).sum(1)
        for r in runs(bright > 6):
            if r[1] - r[0] >= 12:
                y0, y1 = r[0] + top[0], r[1] + top[0]
                cols = np.where((g.mean(0)[y0:y1] > 120).any(0))[0]
                crop = med[y0:y1, cols.min():cols.max() + 1].reshape(-1, 3)
                br = crop[crop.max(1) > 120]
                text_rows.append({"y": [int(y0), int(y1)], "x": [int(cols.min()), int(cols.max()) + 1],
                                  "fill_hex": lib.hexc(np.median(br, 0).astype(int)) if len(br) else None})
    return {"window": [0, int(y_win), 1080, int(1920 - y_win)], "caption_box": band, "top_band": top, "top_rgb": top_rgb,
            "top_hex": lib.hexc(top_rgb) if top_rgb else None, "top_text_rows": text_rows, "row_std_thr": round(thr, 2)}


def caption_track(mp4, box, fps=10.0, dark=110, min_px=120):
    """흰 띠 안 검은 글 덩어리: 잉크 모양이 바뀌면 새 덩어리."""
    y0, y1 = box
    fr = lib.frames(mp4, fps=fps, crop=(0, y0, 1080, y1 - y0), gray=True)
    segs, cur = [], None
    prev = None
    for t, f in fr:
        m = f < dark
        n = int(m.sum())
        if n < min_px:
            if cur: segs.append(cur); cur = None
            prev = None; continue
        if prev is not None:
            inter = (m & prev).sum(); uni = (m | prev).sum()
            iou = inter / max(1, uni)
        else:
            iou = 0
        if cur is None or iou < 0.55:
            if cur: segs.append(cur)
            ys, xs = np.where(m)
            cur = {"t0": round(t, 2), "t1": round(t + 1 / fps, 2), "bbox": [int(xs.min()), int(ys.min() + y0), int(xs.max()) + 1, int(ys.max() + y0) + 1], "ink": n}
        else:
            cur["t1"] = round(t + 1 / fps, 2)
        prev = m
    if cur: segs.append(cur)
    # 아주 짧은 깜박임(0.15초 미만)은 앞 덩어리에 붙인다
    out = []
    for s in segs:
        if out and s["t1"] - s["t0"] < 0.15 and abs(s["t0"] - out[-1]["t1"]) < 0.11:
            out[-1]["t1"] = s["t1"]; continue
        out.append(s)
    return out


def intro_track(mp4, top_rgb, dur, fps=10.0):
    """표지(인트로): 위 띠 색이 본편 띠 색과 다른 구간(밝은 막이 덮임)."""
    fr = lib.frames(mp4, fps=fps, t0=0, t1=min(dur, 8.0), crop=(0, 10, 200, 120))
    on = []
    for t, f in fr:
        c = np.median(f.reshape(-1, 3), 0)
        on.append((round(t, 2), float(np.abs(c - np.array(top_rgb)).max())))
    flag = [d > 25 for _, d in on]
    t_out = None
    for i, v in enumerate(flag):
        if not v:
            t_out = on[i][0]; break
    return {"t_in": 0.0 if flag and flag[0] else None, "t_out": t_out if flag and flag[0] else None,
            "kind": "0초 표지 카드(card)" if flag and flag[0] else "없음(scene)", "top_color_diff": [d for _, d in on[:int(fps * 5)]][::2]}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("mp4"); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    mp4 = a.mp4; os.makedirs(a.out, exist_ok=True)
    vid = os.path.splitext(os.path.basename(mp4))[0]
    dur = lib.duration(mp4); fps = lib.fps_of(mp4)
    lay = layout(mp4, dur)
    box = lay["caption_box"]
    caps = caption_track(mp4, box) if box else []
    intro = intro_track(mp4, lay["top_rgb"], dur) if lay["top_rgb"] else {"kind": "미측정 — 위 띠 못 찾음"}
    items, glyph = [], []
    for i, c in enumerate(caps):
        tm = (c["t0"] + c["t1"]) / 2
        img = lib.frame(mp4, tm)
        bx = c["bbox"]
        crop = img[bx[1]:bx[3], bx[0]:bx[2]].reshape(-1, 3)
        dk = crop[crop.max(1) < 110]
        items.append({"i": i, "t0": c["t0"], "t1": c["t1"], "bbox": bx, "w": bx[2] - bx[0], "h": bx[3] - bx[1],
                      "x_center": (bx[0] + bx[2]) / 2, "fill_hex": lib.hexc(np.median(dk, 0).astype(int)) if len(dk) else "미측정 — 잉크 없음",
                      "text": [], "in_intro": bool(intro.get("t_out") and c["t0"] < intro["t_out"])})
    cu = lib.cuts(mp4, lay["window"])
    ld = lib.loud(mp4)
    tr = lib.asr(mp4)
    x = lib.pcm(mp4, 16000)
    f0, nf0 = f0_estimate(x)
    words = tr["words"]
    speech = np.zeros(int(dur * 10) + 1, bool)
    for w in words:
        speech[int(w["t0"] * 10):int(w["t1"] * 10) + 1] = True
    r = ld["rms_025"]
    def at(t): return r[min(len(r) - 1, int(t / 0.25))]
    sp_db = [at(i / 10) for i in range(len(speech)) if speech[i]]
    ns_db = [at(i / 10) for i in range(len(speech)) if not speech[i] and i / 10 < dur - 0.3]
    floor = round(float(np.median(ns_db)), 1) if ns_db else "미측정 — 말 없는 구간 없음"
    js = {
        "engine": "뜯기 cn판 2026-11-08(tear_cn.py · lib.py)", "source": f"02_source/{vid}.mp4",
        "measured_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "probe": {"w": 1080, "h": 1920, "fps": round(fps, 3), "duration": round(dur, 3), "has_audio": True},
        "layout": {**lay, "ink_polarity": "dark", "caption_pos": "above",
                   "intro_outro": {"intro": intro, "outro": "1초 시트 눈으로(줄판독)"}},
        "captions": {"n_spans": len(items), "items": items,
                     "note": "글(text)은 기계 OCR 없음 — 클로드가 줄판독에서 띠 그림을 보고 채운다(§2-2-1 ⑤)"},
        "caption_motion": {"starts": [{"caption": i, "t0": c["t0"], "anim": "줄판독에서 30fps 띠로"} for i, c in enumerate(items)],
                           "ends": [{"caption": i, "t1": c["t1"]} for i, c in enumerate(items)]},
        "fonts": {"ok": False, "failed": "글꼴 대조는 글이 확정된 뒤 fontmatch.py 로(줄판독 단계)"},
        "audio": {"bench": {"I": ld["I"], "LRA": ld["LRA"], "TP": ld["TP"]},
                  "transcript": {"engine": tr["engine"], "segments": tr["segments"], "words": words},
                  "composition": {"narration": "받아쓰기 낱말 있음" if words else "없음", "speech_sec": round(speech.sum() / 10, 1),
                                  "speech_share": round(float(speech.mean()), 3), "f0_median_hz": f0, "f0_frames": nf0,
                                  "bgm": f"말 없는 구간 0.25초 RMS 중앙 {floor} dB", "separation": "미측정 — 분리 도구 없음"},
                  "phrase_loud": {"나레(말 구간 RMS dB 중앙)": round(float(np.median(sp_db)), 1) if sp_db else "미측정 — 말 없음",
                                  "BGM만(말 없는 구간 RMS dB 중앙)": floor, "원음": "줄판독에서", "unit": "dBFS RMS"},
                  "momentary_04": ld["momentary_04"], "rms_025": ld["rms_025"]},
        "cuts": cu,
        "sfx_rules": {"ok": True, "spikes": ld["spikes"], "n": len(ld["spikes"]), "per_sec": round(len(ld["spikes"]) / dur, 3),
                      "basis": "섞인 소리 10ms RMS 솟음(분리 도구 없음 — 말소리 끝도 섞임, 후보일 뿐)"},
        "bgm_rules": {"ok": not isinstance(floor, str), "floor_db": floor, "has": (not isinstance(floor, str) and floor > -50), "mood": "미측정 — agy 없음"},
        "voice_rules": {"ok": f0 is not None, "speakers": "미측정 — 화자 나누기 없음(위스퍼)", "f0_median_hz": f0,
                        "gender_guess": ("여" if f0 and f0 > 165 else "남") if f0 else "미측정"},
        "materials": "줄판독에서",
        "overlay_rules": {"appearances": [{"kind": "0초 표지 카드", **{k: intro.get(k) for k in ("t_in", "t_out", "kind")}}]},
    }
    def fill(o):
        if isinstance(o, dict): return {k: ("미측정 — 기계 검출 실패(줄판독에서 프레임 눈으로)" if v is None else fill(v)) for k, v in o.items()}
        if isinstance(o, list): return [fill(v) for v in o]
        return o
    js = fill(js)
    json.dump(js, open(os.path.join(a.out, "뜯기.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(vid, "창", lay["window"], "흰띠", box, "위띠", lay["top_hex"], "덩어리", len(items), "표지", intro.get("t_out"),
          "컷", cu["shots"], "컷중앙", cu["shot_len"]["median"], "LUFS", ld["I"], "TP", ld["TP"], "낱말", len(words), "f0", f0)


if __name__ == "__main__":
    main()
