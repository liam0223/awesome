# -*- coding: utf-8 -*-
"""줄판독 합치기(클릭노트 꼴): build_lines_cn.py --ch <ch> <04_frames/<id>/줄판독_입력.json>...
클로드 눈 판독(_reader) + 뜯기 기계값 + 지휘 실측(MEAS) → 05_lines/<id>.json (§6-3 칸 전부).
reader 줄 = [덩어리 번호 또는 "t0-t1", 글, 역할, 장면, 장면 설명, fit, 움직임, 그때 보인 파랑 낱말[]]."""
import sys, os, json, argparse

# 지휘 클로드 실측(fontmatch · 잉크 · 색 — 2026-11-08, 04_frames/fontset)
FAM = {  # 자막 글꼴 갈래(편마다)
    "A": {"font": {"name": "GmarketSansBold", "basis": "fontmatch 0.919(2위 yg-jalnan 0.78) · 3iQ 13.0초"}, "ink": [462, 530], "size_px": 79,
          "hi": "#0811F4", "hi_basis": "Uu 3.6초 · HmG 6.0초 파랑 픽셀 중앙"},
    "B": {"font": {"name": "미일치(둥근 굵은 고딕 — 눈)", "basis": "fontmatch 안 돌림 — 편 2개뿐 · 갈래 B"}, "ink": [467, 545], "size_px": 90,
          "hi": "#046BD0", "hi_basis": "iEN 12.5초 · 3kb 12.0초 파랑 픽셀 중앙"},
    "C": {"font": {"name": "미일치(TmonMonsori 0.535 · Cafe24Ohsquare 0.529)", "basis": "fontmatch O8 3.5초 — 0.5 근처라 미일치"}, "ink": [467, 546], "size_px": 90,
          "hi": None, "hi_basis": "강조 없음(0.3초 띠 O8 2.7~4.5)"},
}
VFAM = {"O8ZNrU_7WVQ": "C", "EwwIlvMZoN4": "C", "Uu_SJaiAuwQ": "A", "HmGDP6rrqo8": "A", "BG8D7oeIhwY": "A", "3iQHc3oTP2Q": "A",
        "iEN1WxOIWoU": "B", "3kb2fopXnIw": "B"}
FILL = {"O8ZNrU_7WVQ": "#2A2C31", "Uu_SJaiAuwQ": "#111111", "HmGDP6rrqo8": "#101212", "BG8D7oeIhwY": "#0F0F13", "3iQHc3oTP2Q": "#050509",
        "EwwIlvMZoN4": "#0A0A0A", "iEN1WxOIWoU": "#020203", "3kb2fopXnIw": "#0A0C0C"}
BIG = {"font": {"name": "미일치(굵은 고딕 — 눈)", "basis": "흰 글 + 파랑 낱말 2줄, 검은 그림자"}, "y": [1150, 1380], "fill_hex": "#FFFFFF"}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--ch", required=True); ap.add_argument("readers", nargs="+")
    a = ap.parse_args()
    for rp in a.readers:
        R = json.load(open(rp, encoding="utf-8"))
        vid = R["id"]
        T = json.load(open(os.path.join(a.ch, "03_tear", vid, "뜯기.json"), encoding="utf-8"))
        items = T["captions"]["items"]
        dur = T["probe"]["duration"]; cuts = T["cuts"]["times"]; words = T["audio"]["transcript"]["words"]; rms = T["audio"]["rms_025"]
        lay = T["layout"]; intro_out = lay["intro_outro"]["intro"]["t_out"]
        fam = FAM[VFAM[vid]]

        def mk(t0, t1):
            return {"cut_at": [c for c in cuts if t0 <= c < t1], "words": [w for w in words if w["t1"] > t0 and w["t0"] < t1],
                    "loud": rms[int(t0 / 0.25): int(t1 / 0.25) + 1]}
        tc = R["title_card"]
        lines = [{"t0": 0.0, "t1": intro_out, "speaker": "나레", "text": " / ".join(tc["lines"]), "layer": "제목", "read": True, "role": "훅",
                  "enter": "cut", "enter_ms": 0, "enter_curve": [], "type_cps": None, "cursor": None, "exit": "cut — 표지 막이 걷히며 본 틀로",
                  "variant": "표지 카드 — 흰 1줄 + 파랑 2줄(검은 테) + 아래 흰 상자 작은 글 '" + tc["box"] + "'",
                  "emph": [{"word": tc["lines"][1], "hex": "#0B8FF0"}], "sticker": [], "sfx": None,
                  "scene": "손·제품 근접", "scene_desc": R["frame0"]["what"], "fit": 6, "motion": "cam", "transition": "none",
                  "y": [220, 640], "x": 540, "align": "center", "max_w": 1000, "fill_hex": "#FFFFFF",
                  "font": {"name": "미일치(BMDOHYEON 눈 대체)", "basis": "fontmatch 0.46 — 미일치"}, "size_px": 110,
                  "letter_gap_px": 0, "line_gap_px": None, "outline": {"px": 6, "hex": "#000000"}, "ring": None, "shadow": None,
                  "glow": None, "box": {"hex": "#FFFFFF", "alpha": 0.95, "pad": [20, 12], "radius": 6},
                  "confidence": "눈(글·자리) · 신호(시각 — 위 띠 색 바뀜)", "notes": "나레가 표지 제목을 읽음(받아쓰기 첫 구간)", **mk(0.0, intro_out)}]
        for L in R["lines"]:
            key, text, role, scene, desc, fit, motion, *rest = L
            hi = rest[0] if rest else []
            if isinstance(key, str):
                t0, t1 = [float(x) for x in key.split("-")]
            else:
                t0, t1 = items[key]["t0"], items[key]["t1"]
            big = "흰 띠 없이" in desc
            hx = fam["hi"]
            ln = {"t0": t0, "t1": t1, "speaker": "나레", "text": text, "layer": "큰글" if big else "해설", "read": True, "role": role,
                  "enter": "cut", "enter_ms": 0, "enter_curve": [], "type_cps": None, "cursor": None, "exit": "cut — 다음 줄로 바로",
                  "variant": ("창 안 큰 2줄 글(흰 띠 숨김)" if big else "흰 띠 검은 글") + (" · 나레 낱말 따라 파랑 강조(노래방)" if hx else " · 강조 없음"),
                  "emph": [{"word": w, "hex": hx} for w in hi] if hx else [], "sticker": [], "sfx": None,
                  "scene": scene, "scene_desc": desc, "fit": fit, "motion": motion, "transition": "cut" if [c for c in cuts if t0 <= c < t1] else "none",
                  "y": BIG["y"] if big else fam["ink"], "x": 540, "align": "center", "max_w": 960,
                  "fill_hex": BIG["fill_hex"] if big else FILL[vid], "font": BIG["font"] if big else fam["font"],
                  "size_px": 100 if big else fam["size_px"], "letter_gap_px": 0, "line_gap_px": None,
                  "outline": {"px": 0, "hex": None} if not big else {"px": 4, "hex": "#000000"}, "ring": None,
                  "shadow": None if not big else {"blur": 12, "hex": "#000000", "alpha": 0.6}, "glow": None,
                  "box": None if big else {"hex": "#FFFFFF", "alpha": 1.0, "pad": "흰 띠 전체(y403~590)", "radius": 0},
                  "confidence": "픽셀(시각·띠·색·글꼴 A) · 눈(글·장면·fit·역할)", "notes": hi and ("그 순간 파랑: " + ", ".join(hi)) or "", **mk(t0, t1)}
            lines.append(ln)
        lines.sort(key=lambda x: x["t0"])
        nar = [l for l in lines if l["speaker"] == "나레"]
        caps_t = sorted((l["t0"], l["t1"]) for l in lines)
        noc, prev = [], 0.0
        for t0, t1 in caps_t:
            if t0 - prev >= 0.3: noc.append([round(prev, 2), round(t0, 2)])
            prev = max(prev, t1)
        if dur - prev >= 0.3: noc.append([round(prev, 2), round(dur, 2)])
        doc = {"id": vid, "dur": dur, "fps": T["probe"]["fps"], "size": [1080, 1920], "form": "정보(발명품 소개)",
               "title_lines": [{"text": R["top_title"], "colors": [{"word": R["top_title"], "hex": lay["top_text_rows"][-1]["fill_hex"]}]}],
               "source_label": "",
               "layout": {"window": lay["window"], "caption_band": lay["caption_box"], "title_y": [r["y"] for r in lay["top_text_rows"][1:]],
                          "logo_y": lay["top_text_rows"][0]["y"], "logo_x": lay["top_text_rows"][0]["x"], "source_y": None, "source_hex": None,
                          "bg_hex": lay["top_hex"], "watermark": {"what": "'@클릭 노트' 흐린 흰 글 — 영상 창 가운데 아래(눈)", "alpha": 0.5},
                          "ad_mark": {"text": "[광고]", "where": "위 띠 오른쪽(로고 줄 끝 x≈960~1040)", "t": "0~끝"}},
               "lines": lines, "no_caption": noc, "beats": R["beats"],
               "narr_share": f"나레 줄 {len(nar)}/{len(lines)} · 받아쓰기 말 구간 {T['audio']['composition']['speech_share']}",
               "name_evidence": [], "frame0": R["frame0"],
               "notes": R["notes"] + ["받아쓰기 = 위스퍼(낱말 시각 정밀도 낮음)", "효과음·BGM 이름 = 미측정 — agy·분리 도구 없음"]}
        json.dump(doc, open(os.path.join(a.ch, "05_lines", vid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(vid, len(lines), "줄")


if __name__ == "__main__":
    main()
