# -*- coding: utf-8 -*-
"""뜯기: tear.py <02_source/<id>.mp4> --out <03_tear/<id>>
부록 A-2 꼴 뜯기.json. 기계값만(확정 판독은 줄판독)."""
import sys, os, json, argparse, datetime, math
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import lib

def find_band(mp4, lo=330, hi=640):
    fr = lib.frames(mp4, fps=2, crop=(0, lo, 1080, hi - lo))
    prof = np.zeros(hi - lo)
    for t, f in fr[3:]:
        prof += lib.outlined_white_mask(f).sum(1)
    prof /= max(1, len(fr) - 3)
    thr = max(3.0, prof.max() * 0.15)
    on = np.where(prof > thr)[0]
    # 가장 센 덩어리
    best, s = None, None
    segs = []
    for y in range(len(prof) + 1):
        o = y < len(prof) and prof[y] > thr
        if o and s is None: s = y
        if not o and s is not None:
            segs.append((s, y, prof[s:y].sum())); s = None
    s0, s1, _ = max(segs, key=lambda x: x[2])
    return [int(s0 + lo), int(s1 + lo)], [round(float(v), 1) for v in prof]

def dark_box_track(mp4, y0=1560, y1=1820, x0=200, x1=880, fps=10):
    """아래쪽 검은 상자(제품구입 띠) 있는 시각."""
    fr = lib.frames(mp4, fps=fps, crop=(x0, y0, x1 - x0, y1 - y0))
    on = []
    for t, f in fr:
        g = f.mean(2)
        rows = (g < 30).mean(1)
        on.append((t, float((rows > 0.5).sum())))
    pres = [t for t, n in on if n >= 40]
    return {"t_in": round(pres[0], 2) if pres else None, "t_out": round(pres[-1] + 1 / fps, 2) if pres else None, "n_on": len(pres), "frames": len(on)}

def f0_estimate(x, sr=16000):
    vals = []
    w = 1024
    for i in range(0, len(x) - w, w):
        seg = x[i:i + w]
        if np.sqrt(np.mean(seg ** 2)) < 0.02:
            continue
        seg = seg - seg.mean()
        ac = np.correlate(seg, seg, "full")[w - 1:]
        lo, hi = sr // 400, sr // 70
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] > 0.3 * ac[0]:
            vals.append(sr / k)
    return round(float(np.median(vals)), 1) if vals else None, len(vals)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("mp4"); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    mp4 = a.mp4; os.makedirs(a.out, exist_ok=True)
    vid = os.path.splitext(os.path.basename(mp4))[0]
    dur = lib.duration(mp4); fps = lib.fps_of(mp4)
    win = lib.window(mp4)
    band, prof = find_band(mp4)
    pad = 14
    cband = [max(0, band[0] - pad), min(1920, band[1] + pad)]
    caps = lib.caption_track(mp4, cband, fps=10)
    # 글자 크기·외곽(덩어리 가운데 프레임)
    glyph, items = [], []
    for i, c in enumerate(caps):
        tm = (c["t0"] + c["t1"]) / 2
        img = lib.frame(mp4, tm)
        ik = lib.ink(img, cband[0], cband[1])
        col = lib.color(img, c["bbox"][0], c["bbox"][1], c["bbox"][2], c["bbox"][3]) if ik else {}
        items.append({"i": i, "t0": c["t0"], "t1": c["t1"], "lines": 1, "widths": [ik["w"]] if ik else [], "top_y": ik["y0"] if ik else None,
                      "bbox": c["bbox"], "text": [], "truncated": False, "fill": col.get("fill_hex"), "outline": col.get("outline_hex")})
        if ik:
            glyph.append({"caption": i, "line_h": ik["h"], "stroke": ik["stroke_px"], "outline_px": ik["outline_px"], "x_center": ik["x_center"],
                          "letter_gap_px": ik["letter_gap_px"], "ink_ratio": ik["ink_ratio"], "shadow": "눈 판독(줄판독)"})
    # 등장 곡선: 덩어리 시작 전후 30fps 6프레임 잉크 넓이
    starts = []
    for c in caps:
        t0 = max(0.0, c["t0"] - 0.1)
        fr = lib.frames(mp4, fps=30, t0=t0, t1=t0 + 0.27, crop=(0, cband[0], 1080, cband[1] - cband[0]))
        curve = []
        for t, f in fr:
            m = lib.outlined_white_mask(f); bb = lib.ink_bbox(m)
            curve.append({"t": round(t, 3), "ink": int(m.sum()), "bbox": bb})
        inks = [p["ink"] for p in curve]
        mx = max(inks) if inks else 0
        firsts = [i for i, v in enumerate(inks) if v > 0.05 * mx]
        if firsts and mx:
            k = firsts[0]
            first_ratio = inks[k] / mx
            anim = "cut(첫 프레임부터 완성)" if first_ratio > 0.8 else "점점(pop/fade 후보 — 30fps 띠로 확인)"
        else:
            anim = "미측정 — 잉크 없음"
        starts.append({"caption": caps.index(c), "t0": c["t0"], "anim": anim, "curve": curve})
    cu = lib.cuts(mp4, win["window"])
    ld = lib.loud(mp4)
    tr = lib.asr(mp4)
    x = lib.pcm(mp4, 16000)
    f0, nf0 = f0_estimate(x)
    # 말 구간 / 말 없는 구간 음량(배경 바닥)
    words = tr["words"]
    speech = np.zeros(int(dur * 10) + 1, bool)
    for w in words:
        speech[int(w["t0"] * 10):int(w["t1"] * 10) + 1] = True
    r = ld["rms_025"]
    def at(t): return r[min(len(r) - 1, int(t / 0.25))]
    sp_db = [at(i / 10) for i in range(len(speech)) if speech[i]]
    ns_db = [at(i / 10) for i in range(len(speech)) if not speech[i] and i / 10 < dur - 0.3]
    bgm_floor = round(float(np.median(ns_db)), 1) if ns_db else None
    over = dark_box_track(mp4)
    # 0초 제목 카드: 0~2초 band 넓은 범위 큰 글씨
    tfr = lib.frames(mp4, fps=10, t0=0, t1=2.5)
    title = []
    for t, f in tfr:
        m = lib.outlined_white_mask(f[200:800])
        rows = m.sum(1) > 25
        best, s, bs = 0, None, None   # 가장 긴 연속 글줄 높이(큰 글일수록 김)
        for y in range(len(rows) + 1):
            o = y < len(rows) and rows[y]
            if o and s is None: s = y
            if not o and s is not None:
                if y - s > best: best, bs = y - s, (s, y)
                s = None
        bb = lib.ink_bbox(m[bs[0]:bs[1]]) if bs else None
        title.append({"t": round(t, 2), "ink": int(m.sum()), "h": best,
                      "bbox": [bb[0], bb[1] + 200 + bs[0], bb[2], bb[3] + 200 + bs[0]] if bb else None})
    big = [p for p in title if p["h"] > 90]  # 본 자막 글줄 높이 ≈ 50px, 표지 글 ≈ 110px 이상
    title_card = {"t_in": big[0]["t"] if big else None, "t_out": round(big[-1]["t"] + 0.1, 2) if big else None,
                  "bbox": big[len(big) // 2]["bbox"] if big else None, "kind": "0초 표지 글(card)" if big else "없음(scene)"}
    js = {
        "engine": "뜯기 1판 2026-11-07(lib.py)", "source": f"02_source/{vid}.mp4", "measured_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "probe": {"w": 1080, "h": 1920, "fps": round(fps, 3), "duration": round(dur, 3), "has_audio": True},
        "layout": {"window": win["window"], "bg_rgb": win["bg_rgb"], "ink_polarity": "bright", "caption_pos": "inside",
                   "caption_band": cband, "caption_ink_band": band, "above_bands": win["above_bands"],
                   "intro_outro": {"intro": "없음" if not win["above_bands"] else "확인 필요", "outro": "없음(끝 0.3초 같은 틀 — 1초 시트로 확인)"},
                   "row_profile_330_640": prof[::4]},
        "captions": {"n_spans": len(items), "items": items, "glyph": glyph,
                     "note": "글(text)은 기계 OCR 없음 — 클로드가 줄판독에서 프레임을 보고 채운다(§2-2-1 ⑤)"},
        "caption_motion": {"starts": starts, "ends": [{"caption": i, "t1": c["t1"]} for i, c in enumerate(caps)]},
        "fonts": {"failed": "글꼴 대조는 글이 확정된 뒤 fontmatch.py 로(줄판독 단계에서 채움)"},
        "audio": {"bench": {"I": ld["I"], "LRA": ld["LRA"], "TP": ld["TP"]},
                  "transcript": {"engine": tr["engine"], "segments": tr["segments"], "words": tr["words"]},
                  "composition": {"narration": "받아쓰기 낱말 있음" if words else "없음", "speech_sec": round(speech.sum() / 10, 1),
                                  "speech_share": round(float(speech.mean()), 3), "f0_median_hz": f0, "f0_frames": nf0,
                                  "bgm": f"말 없는 구간 0.25초 RMS 중앙 {bgm_floor} dB(무음 바닥 −60 dB 보다 위면 배경음 있음 후보)",
                                  "separation": "미측정 — 분리 도구 없음"},
                  "phrase_loud": {"나레(말 구간 RMS dB 중앙)": round(float(np.median(sp_db)), 1) if sp_db else "미측정 — 말 없음",
                                  "BGM만(말 없는 구간 RMS dB 중앙)": bgm_floor if bgm_floor is not None else "미측정 — 말 없는 구간 없음",
                                  "원음": "해당 없음(원음 구간 판독은 줄판독)", "unit": "dBFS RMS(LUFS 아님 — 0.4초 LUFS 는 momentary_04)"},
                  "momentary_04": ld["momentary_04"], "rms_025": ld["rms_025"]},
        "cuts": cu,
        "sfx_rules": {"ok": True, "spikes": ld["spikes"], "n": len(ld["spikes"]), "per_sec": round(len(ld["spikes"]) / dur, 3),
                      "basis": "섞인 소리 10ms RMS 솟음(분리 도구 없음 — 말소리 끝도 섞임, 후보일 뿐)"},
        "bgm_rules": {"ok": bgm_floor is not None, "floor_db": bgm_floor, "has": (bgm_floor is not None and bgm_floor > -50), "mood": "미측정 — agy 없음(줄판독에서 눈·신호로)"},
        "voice_rules": {"ok": f0 is not None, "speakers": "미측정 — 화자 나누기 없음(위스퍼)", "f0_median_hz": f0,
                        "gender_guess": ("여" if f0 and f0 > 165 else "남") if f0 else "미측정"},
        "materials": "줄판독에서(해외 제품 영상 재편집 후보)",
        "overlay_rules": {"appearances": [
            {"kind": "제목 표지 글", **title_card},
            {"kind": "아래 검은 상자(제품구입 띠)", "t0": over["t_in"], "t1": over["t_out"], "box": [200, 1560, 880, 1820], "n_on_frames": over["n_on"]},
            {"kind": "[광고] 표시", "t0": "미측정 — 줄판독에서 0.1초 띠", "box": "오른쪽 위(1초 시트 눈 — 줄판독에서 px)"},
            {"kind": "워터마크 글(채널 이름)", "t0": "미측정 — 줄판독에서", "box": "가운데 아래(1초 시트 눈)"}]},
    }
    def nn(o, path=""):
        bad = []
        if o is None:
            bad.append(path)
        elif isinstance(o, dict):
            for k, v in o.items():
                bad += nn(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                bad += nn(v, f"{path}[{i}]")
        return bad
    def fill(o):
        """못 잰 칸은 None 대신 이유 글(뜯기 빈칸 관문 — 못 잰 칸 = ok:false + 이유)."""
        if isinstance(o, dict):
            return {k: ("미측정 — 기계 검출 실패(줄판독에서 프레임 눈으로 확인)" if v is None else fill(v)) for k, v in o.items()}
        if isinstance(o, list):
            return [fill(v) for v in o]
        return o
    js = fill(js)
    bad = nn(js)
    js["_none"] = bad
    js["_note"] = "overlay_rules·title 은 기계 후보(흰 바탕 편은 잘못 잡힘) — 확정은 05_lines 줄판독"
    json.dump(js, open(os.path.join(a.out, "뜯기.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(vid, "덩어리", len(items), "컷", cu["shots"], "컷중앙", cu["shot_len"]["median"], "LUFS", ld["I"], "TP", ld["TP"], "낱말", len(words),
          "f0", f0, "band", band, "CTA", over["t_in"], "제목", title_card["t_in"], title_card["t_out"], "None", bad[:5])

if __name__ == "__main__":
    main()
