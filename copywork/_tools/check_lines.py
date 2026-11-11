# -*- coding: utf-8 -*-
"""check_lines.py <05_lines> [--strict] — §6-3 칸 검사. 오류 있으면 종료 코드 1."""
import sys, os, json, glob, re

DOC = ["id", "dur", "fps", "size", "form", "title_lines", "source_label", "layout", "lines", "no_caption", "beats", "narr_share", "name_evidence", "frame0", "notes"]
LINE = ["t0", "t1", "speaker", "text", "layer", "read", "role", "enter", "enter_ms", "variant", "emph", "sticker", "sfx", "cut_at", "scene", "scene_desc",
        "fit", "motion", "transition", "y", "x", "align", "max_w", "fill_hex", "font", "size_px", "outline", "box", "words", "loud", "confidence", "notes"]
SPK = re.compile(r"^(나레|원음:.+|원음|해설|제3자|불명)$")
ROLE = {"훅", "다리", "고조", "공개", "증거", "반전", "질문", "답", "이음", "본문", "끝"}
ENTER = {"pop", "cut", "fade", "typing", "append", "instant"}
SCENE = {"얼굴", "손·제품 근접", "과정", "화보", "기타"}
MOTION = {"still", "zoom_in", "zoom_out", "pan", "cam"}
TRANS = {"cut", "zoomblur", "flash", "black", "none"}
CONF = re.compile(r"(픽셀|눈|신호|미측정)")

def check(p, strict):
    E = []
    d = json.load(open(p, encoding="utf-8"))
    if "_todo" in d and d["_todo"]:
        E.append("_todo 남음")
    for k in DOC:
        if k not in d or (strict and d[k] is None and k not in ("source_y",)):
            E.append(f"문서 칸 {k} 없음/null")
    prev = None
    for i, L in enumerate(d.get("lines", [])):
        for k in LINE:
            if k not in L:
                E.append(f"lines[{i}].{k} 없음")
        if strict:
            for k in ("speaker", "text", "layer", "role", "enter", "scene", "fit", "motion", "transition", "confidence"):
                if L.get(k) in (None, ""):
                    E.append(f"lines[{i}].{k} 빔")
        if L.get("speaker") and not SPK.match(str(L["speaker"])):
            E.append(f"lines[{i}].speaker 어휘 밖: {L['speaker']}")
        if L.get("role") and L["role"] not in ROLE: E.append(f"lines[{i}].role 어휘 밖")
        if L.get("enter") and L["enter"].split()[0] not in ENTER and not L["enter"].startswith("기타"): E.append(f"lines[{i}].enter 어휘 밖")
        if L.get("scene") and L["scene"] not in SCENE: E.append(f"lines[{i}].scene 어휘 밖")
        if L.get("motion") and L["motion"] not in MOTION: E.append(f"lines[{i}].motion 어휘 밖")
        if L.get("transition") and L["transition"] not in TRANS: E.append(f"lines[{i}].transition 어휘 밖")
        if not isinstance(L.get("fit"), (int, float)) or not 0 <= L["fit"] <= 10: E.append(f"lines[{i}].fit 0~10 아님")
        if L.get("confidence") and not CONF.search(L["confidence"]): E.append(f"lines[{i}].confidence 어휘 밖")
        if not isinstance(L.get("emph"), list) or not isinstance(L.get("sticker"), list): E.append(f"lines[{i}] emph/sticker 목록 아님")
        if L.get("t1", 0) <= L.get("t0", 0): E.append(f"lines[{i}] t1<=t0")
        if L.get("read") is True and re.match(r"^\(.*\)$", L.get("text", "")): E.append(f"lines[{i}] 괄호 지문인데 read:true")
        if L.get("layer") == "해설" and L.get("speaker") == "나레" and prev and prev.get("layer") == "해설" and L["t0"] < prev["t1"] - 0.05:
            E.append(f"lines[{i}] 앞 줄과 겹침")
        if L.get("layer") == "해설":
            prev = L
    return E

if __name__ == "__main__":
    root = sys.argv[1]; strict = "--strict" in sys.argv
    bad = 0
    for p in sorted(glob.glob(os.path.join(root, "*.json"))):
        if os.path.basename(p).startswith("_"):
            continue
        E = check(p, strict)
        bad += len(E)
        print(os.path.basename(p), "오류", len(E), *E[:12], sep="\n  " if E else " ")
    sys.exit(1 if bad else 0)
