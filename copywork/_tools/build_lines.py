# -*- coding: utf-8 -*-
"""줄판독 합치기: build_lines.py --ch <ch> --reader <_reader_*.json>...
일꾼(클로드 눈) 판독 + 뜯기 기계값 + 지휘 클로드 실측 공통값 → 05_lines/<id>.json (§6-3 칸 전부)."""
import sys, os, json, argparse
sys.path.insert(0, os.path.dirname(__file__))

# 지휘 클로드 실측(04_frames 확대·fontmatch·ink) — 편 공통
CAP = {"font": {"name": "BMJUA", "basis": "fontmatch 1위 0.784(2위 yg-jalnan 0.615) + 눈(둥근 굵은 고딕)"},
       "size_px": 61, "fill_hex": "#FFFFFF", "outline": {"px": 3, "hex": "#000000"}, "ring": None,
       "shadow": {"dx": 0, "dy": 0, "blur": 14, "hex": "#000000", "alpha": 0.75, "basis": "눈 — 가로 스캔 밝기 74→33 이 약 12px 에 걸쳐 내려감"},
       "glow": None, "box": None, "letter_gap_px": 2, "line_gap_px": None, "x": 540, "align": "center", "max_w": 1014}
TITLE = {"font": {"name": "GothicA1-Black", "basis": "fontmatch 0.91(2위 KCCGanpan 0.747)"}, "size_px": 125,
         "outline": {"px": 6, "hex": "#000000"}, "white": "#FFFFFF"}
TITLE_HEX = {"n9-b7kuLizk": "#11FED3", "8cRRYqXqgo4": "#C5F910", "KT8fKHlFyls": "#17F1B1", "i2wtSB7-FWk": "#F7CE16"}
TITLE_Y = {"n9-b7kuLizk": [285, 585], "8cRRYqXqgo4": [570, 840], "KT8fKHlFyls": [285, 570], "i2wtSB7-FWk": [810, 1155]}
CTA = {"n9-b7kuLizk": {"t0": 15.5, "text": "제품구입-프로필링크58번", "box": [232, 1468, 883, 1572], "box_hex": "#FFFFFF", "fill_hex": "#000000"},
       "8cRRYqXqgo4": {"t0": 16.4, "text": "식비 아끼는 꿀팁-프로필링크52번", "box": [143, 1532, 937, 1642], "box_hex": "#000000", "fill_hex": "#0BFD23"},
       "KT8fKHlFyls": {"t0": 14.7, "text": "제품구입-프로필링크51번", "box": [181, 1643, 940, 1765], "box_hex": "#000000", "fill_hex": "#0AFB0D"},
       "i2wtSB7-FWk": {"t0": 14.4, "text": "제품구입-프로필링크53번", "box": [214, 1535, 865, 1639], "box_hex": "#FFFFFF", "fill_hex": "#000000"}}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--ch", required=True); ap.add_argument("--reader", nargs="+", required=True)
    a = ap.parse_args()
    for rp in a.reader:
        for R in json.load(open(rp, encoding="utf-8")):
            vid = R["id"]
            T = json.load(open(os.path.join(a.ch, "03_tear", vid, "뜯기.json"), encoding="utf-8"))
            dur = T["probe"]["duration"]; cuts = T["cuts"]["times"]; words = T["audio"]["transcript"]["words"]; rms = T["audio"]["rms_025"]
            band = T["layout"]["caption_ink_band"]
            def mk(t0, t1):
                return {"cut_at": [c for c in cuts if t0 <= c < t1], "words": [w for w in words if w["t1"] > t0 and w["t0"] < t1],
                        "loud": rms[int(t0 / 0.25): int(t1 / 0.25) + 1]}
            lines = []
            tc = R["title_card"]; col = TITLE_HEX[vid]
            lines.append({"t0": tc["t0"], "t1": tc["t1"], "speaker": "해설", "text": " / ".join(tc["lines"]), "layer": "제목", "read": False,
                          "role": "훅", "enter": "cut", "enter_ms": 0, "enter_curve": [], "type_cps": None, "cursor": None, "exit": "cut — 첫 본 자막으로 바로 바뀜",
                          "variant": f"두 줄 — {tc['colored_line']}째 줄 색 글", "emph": [{"word": tc["lines"][tc["colored_line"] - 1], "hex": col}],
                          "sticker": [], "sfx": None, "scene": "손·제품 근접", "scene_desc": R["frame0"]["what"], "fit": 6, "motion": "cam",
                          "transition": "none", "y": TITLE_Y[vid], "x": 540, "align": "center", "max_w": 900, "fill_hex": TITLE["white"],
                          "font": TITLE["font"], "size_px": TITLE["size_px"], "letter_gap_px": 4, "line_gap_px": 10,
                          "outline": TITLE["outline"], "ring": None, "shadow": None, "glow": None, "box": None,
                          "confidence": "픽셀(색·글꼴) · 눈(자리 ±10px)", "notes": "나레가 읽지 않음(받아쓰기 첫 낱말이 첫 본 자막 글)", **mk(tc["t0"], tc["t1"])})
            for L in R["lines"]:
                cut_at = [c for c in cuts if L["t0"] <= c < L["t1"]]
                lines.append({"t0": L["t0"], "t1": L["t1"], "speaker": "나레", "text": L["text"], "layer": "해설", "read": True, "role": L["role"],
                              "enter": "cut", "enter_ms": 0, "enter_curve": [], "type_cps": None, "cursor": None, "exit": "cut — 다음 줄로 바로(빈틈 0~0.2초)",
                              "variant": "기본", "emph": [], "sticker": [], "sfx": None, "scene": L["scene"], "scene_desc": L["scene_desc"], "fit": L["fit"],
                              "motion": L["motion"], "transition": "cut" if cut_at else "none", "y": band,
                              **{k: v for k, v in CAP.items()}, "confidence": "픽셀(글꼴·크기·색·y) · 눈(글·장면·fit)", "notes": "",
                              **mk(L["t0"], L["t1"])})
            c = CTA[vid]
            lines.append({"t0": c["t0"], "t1": round(dur, 2), "speaker": "해설", "text": c["text"], "layer": "제품구입띠", "read": False, "role": "끝",
                          "enter": "cut", "enter_ms": 0, "enter_curve": [], "type_cps": None, "cursor": None, "exit": "영상 끝까지",
                          "variant": "검은 상자+초록 글" if c["box_hex"] == "#000000" else "흰 상자+검은 글", "emph": [], "sticker": [], "sfx": None,
                          "scene": "기타", "scene_desc": "아래쪽 둥근 상자 띠(본 자막과 겹쳐 나옴)", "fit": 5, "motion": "cam", "transition": "none",
                          "y": [c["box"][1], c["box"][3]], "x": 540, "align": "center", "max_w": c["box"][2] - c["box"][0], "fill_hex": c["fill_hex"],
                          "font": {"name": "GothicA1-Black", "basis": "fontmatch 0.905"}, "size_px": 59, "letter_gap_px": 2, "line_gap_px": None,
                          "outline": None, "ring": None, "shadow": None, "glow": None,
                          "box": {"hex": c["box_hex"], "alpha": 1.0, "pad": [30, 22], "radius": 24},
                          "confidence": "픽셀(시각·상자·색) · 눈(반지름)", "notes": f"영상 길이의 {round(c['t0'] / dur * 100)}% 지점에 나옴", **mk(c["t0"], dur)})
            nar = [l for l in lines if l["speaker"] == "나레"]
            nar_sec = sum(l["t1"] - l["t0"] for l in nar)
            doc = {"id": vid, "dur": dur, "fps": T["probe"]["fps"], "size": [1080, 1920], "form": "리뷰(썰형 제품·꿀팁 소개)",
                   "title_lines": [{"text": tc["lines"][0], "colors": [{"word": tc["lines"][0], "hex": col if tc["colored_line"] == 1 else "#FFFFFF"}]},
                                   {"text": tc["lines"][1], "colors": [{"word": tc["lines"][1], "hex": col if tc["colored_line"] == 2 else "#FFFFFF"}]}],
                   "source_label": "없음(화면에 출처 글 없음)",
                   "layout": {"window": T["layout"]["window"], "caption_band": band, "title_y": TITLE_Y[vid], "logo_y": [1570, 1610], "logo_x": [452, 625],
                              "source_y": None, "source_hex": None, "bg_hex": "없음(화면 가득 영상)",
                              "watermark": {"what": "채널 이름 글 '생생정보템'(Gaegu-Bold 닮음 0.61) — 제품구입 띠 바로 위 가운데", "alpha": 0.9},
                              "ad_mark": {"text": "[광고]", "box": [855, 111, 998, 152], "hex": "#FFFFFF", "font": "Gaegu-Bold(눈 — 대조 0.32 미일치)", "t": "0~끝"}},
                   "lines": lines, "no_caption": R["no_caption"], "beats": R["beats"],
                   "narr_share": f"나레 덩어리 {len(nar)}/{len(lines)} · 나레 자막 초 {round(nar_sec, 1)}/{round(dur, 1)} · 받아쓰기 말 구간 {T['audio']['composition']['speech_share']}",
                   "name_evidence": [], "frame0": R["frame0"], "notes": R["notes"] + ["원음(영상 속 사람 말) 확인 못 함 — 분리 도구·agy 없음, 받아쓰기는 나레만 잡힘"]}
            json.dump(doc, open(os.path.join(a.ch, "05_lines", vid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print(vid, len(lines), "줄")

if __name__ == "__main__":
    main()

