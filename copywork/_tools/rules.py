# -*- coding: utf-8 -*-
"""rules.py <05_lines> --out <06_rules> --tear <03_tear>
규칙빈도.json/.md · 대본말꼴.md(script_lang) · 팔레트.json(palette) · 숫자표.json(스타일분석 재료)"""
import sys, os, json, glob, re, argparse, statistics as st
from collections import Counter

def grade(k, n):
    if n < 5: return "표본부족"
    r = k / n
    return "강" if r >= 0.6 else "중" if r >= 0.3 else "약"

def q(a):
    a = sorted(a)
    if not a: return None
    n = len(a)
    if n < 10:
        return {"n": n, "min": round(a[0], 3), "median": round(st.median(a), 3), "max": round(a[-1], 3)}
    import numpy as np
    return {"n": n, "p10": round(float(np.percentile(a, 10)), 3), "median": round(st.median(a), 3), "p90": round(float(np.percentile(a, 90)), 3)}

def ending(t):
    t = t.strip().rstrip(".!?~")
    for e in ["다더라고요", "더라고요", "습니다", "합니다", "입니다", "는데요", "었어요", "겠어요", "겠네요", "네요", "거 있죠", "죠", "니까", "는데", "고", "면", "서", "가", "이", "도", "에", "게", "을", "를", "는", "다"]:
        if t.endswith(e): return e
    return t[-1:] if t else ""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("lines"); ap.add_argument("--out", required=True); ap.add_argument("--tear", required=True)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    docs = [json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(os.path.join(a.lines, "*.json"))) if not os.path.basename(p).startswith("_")]
    ALL = [(d["id"], L) for d in docs for L in d["lines"]]
    NAR = [(i, L) for i, L in ALL if L["speaker"] == "나레"]
    n = len(NAR); E = len(docs)
    rules = []
    def add(cond, eff, k, nn, base=None):
        rules.append({"cond": cond, "effect": eff, "k": k, "n": nn, "rate": round(k / nn, 3) if nn else None, "base": base, "grade": grade(k, nn)})
    add("나레 줄", "등장 cut(첫 프레임부터 완성)", sum(L["enter"] == "cut" for _, L in NAR), n)
    add("나레 줄", "강조색 없음", sum(not L["emph"] for _, L in NAR), n)
    add("나레 줄", "스티커 없음", sum(not L["sticker"] for _, L in NAR), n)
    add("나레 줄", "한 줄(줄바꿈 없음)", n, n)
    add("나레 줄", "꾸밈 없음(plain — 등장 cut·강조 0·스티커 0, 효과음은 미측정이라 뺌)", sum(L["enter"] == "cut" and not L["emph"] and not L["sticker"] for _, L in NAR), n)
    add("편", "0초 제목 표지(두 줄·한 줄 색)", sum(any(L["layer"] == "제목" and L["t0"] == 0 for L in d["lines"]) for d in docs), E)
    add("편", "제목 색 줄 = 2째 줄", sum(any(L["layer"] == "제목" and "2째" in L["variant"] for L in d["lines"]) for d in docs), E)
    add("편", "제품구입 띠(길이 60~70% 지점부터 끝까지)", sum(any(L["layer"] == "제품구입띠" and 0.6 <= L["t0"] / d["dur"] <= 0.7 for L in d["lines"]) for d in docs), E)
    add("편", "제품구입 띠 = 검은 상자+초록 글", sum(any(L["layer"] == "제품구입띠" and "초록" in L["variant"] for L in d["lines"]) for d in docs), E)
    add("편", "[광고] 오른쪽 위 처음부터 끝", E, E)
    by_role = Counter(L["role"] for _, L in NAR)
    # 숫자
    chars = [len(L["text"].replace(" ", "")) for _, L in NAR]
    secs = [L["t1"] - L["t0"] for _, L in NAR]
    cps_ep = []
    for d in docs:
        nl = [L for L in d["lines"] if L["speaker"] == "나레"]
        cps_ep.append(sum(len(L["text"].replace(" ", "")) for L in nl) / sum(L["t1"] - L["t0"] for L in nl))
    tear = {d["id"]: json.load(open(os.path.join(a.tear, d["id"], "뜯기.json"), encoding="utf-8")) for d in docs}
    shot = [x for t in tear.values() for x in t["cuts"]["shot_list"]]
    first_nar = [min(L["t0"] for L in d["lines"] if L["speaker"] == "나레") for d in docs]
    title_dur = [next(L["t1"] - L["t0"] for L in d["lines"] if L["layer"] == "제목") for d in docs]
    cta_pos = [next(L["t0"] / d["dur"] for L in d["lines"] if L["layer"] == "제품구입띠") for d in docs]
    gaps = [b["t0"] - a_["t1"] for d in docs for a_, b in zip([L for L in d["lines"] if L["speaker"] == "나레"], [L for L in d["lines"] if L["speaker"] == "나레"][1:])]
    role_first = {}
    for r in ["다리", "공개", "증거", "반전", "고조", "끝"]:
        v = []
        for d in docs:
            xs = [L["t0"] / d["dur"] for L in d["lines"] if L["speaker"] == "나레" and L["role"] == r]
            if xs: v.append(min(xs))
        role_first[r] = q([x * 100 for x in v])
    nums = {"편 수": E, "나레 줄 수": n, "줄 글자(공백 뺌)": q(chars), "줄 표시 초": q(secs), "나레 자/초(편마다)": q(cps_ep),
            "줄 사이 빈틈 초": q(gaps), "컷 길이 초(전 편 샷)": q(shot), "편 컷 중앙": q([t["cuts"]["shot_len"]["median"] for t in tear.values()]),
            "컷/분": q([t["cuts"]["cut_per_min"] for t in tear.values()]), "길이 초": q([d["dur"] for d in docs]),
            "첫 나레 자막 시각": q(first_nar), "제목 표지 초": q(title_dur), "제품구입 띠 자리(%)": q([x * 100 for x in cta_pos]),
            "LUFS": q([t["audio"]["bench"]["I"] for t in tear.values()]), "TP": q([t["audio"]["bench"]["TP"] for t in tear.values()]),
            "나레 f0": q([t["audio"]["composition"]["f0_median_hz"] for t in tear.values()]),
            "fit 평균(나레)": round(st.mean(L["fit"] for _, L in NAR), 2), "fit 7 미만 비율": round(sum(L["fit"] < 7 for _, L in NAR) / n, 3),
            "역할 첫 자리(%)": role_first, "역할 줄 수": dict(by_role)}
    json.dump({"rules": rules, "episodes": [d["id"] for d in docs], "by_speaker": dict(Counter(L["speaker"] for _, L in ALL)),
               "by_role": dict(by_role), "by_layer": dict(Counter(L["layer"] for _, L in ALL)), "nums": nums},
              open(os.path.join(a.out, "규칙빈도.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    M = ["# 규칙빈도", "", f"표본 {E}편 · 나레 줄 {n}개 · 등급: n≥5 이고 비율 ≥0.6 강 / ≥0.3 중 / 그 밑 약 / n<5 표본부족 (편 단위 규칙은 n=4 → 전부 표본부족)", "",
         "| 조건 | 효과 | k/n | 비율 | 등급 |", "|---|---|---|---|---|"]
    M += [f"| {r['cond']} | {r['effect']} | {r['k']}/{r['n']} | {r['rate']} | {r['grade']} |" for r in rules]
    M += ["", "## 숫자", "```json", json.dumps(nums, ensure_ascii=False, indent=1), "```"]
    open(os.path.join(a.out, "규칙빈도.md"), "w", encoding="utf-8").write("\n".join(M) + "\n")
    # 대본말꼴
    sents, cur, pieces, cnt = [], [], [], 0
    for d in docs:
        cur = []; cnt = 0
        for L in [L for L in d["lines"] if L["speaker"] == "나레"]:
            cur.append(L["text"]); cnt += 1
            if re.search(r"(니다|요|죠)$", L["text"].strip()):
                sents.append((d["id"], " ".join(cur), L["role"])); pieces.append(cnt); cur = []; cnt = 0
        if cur: sents.append((d["id"], " ".join(cur), "끝(안 맺음)"))
    ends = Counter(ending(s) for _, s, _ in sents)
    chunk_ends = Counter(ending(L["text"]) for _, L in NAR)
    S = ["# 대본말꼴", "", f"문장 {len(sents)}개(나레 줄을 맺음 어미로 이어 붙임) · 편 {E}", "",
         "## 문장 끝맺음 분포", *[f"- {k}: {v}/{len(sents)}" for k, v in ends.most_common()], "",
         "## 줄(자막 조각) 끝 꼴", *[f"- {k}: {v}/{n}" for k, v in chunk_ends.most_common(12)], "",
         f"- 문장 글자 수(공백 뺌): {q([len(s.replace(' ', '')) for _, s, _ in sents])}",
         f"- 문장당 조각 수(나레 줄 수): {q(pieces)}",
         "- 격식체(~니다) 문장: " + str(sum(1 for _, s, _ in sents if re.search(r'니다$', s))) + f"/{len(sents)}",
         "- 해요체(요·죠·네요) 문장: " + str(sum(1 for _, s, _ in sents if re.search(r'(요|죠)$', s))) + f"/{len(sents)}",
         "- 전언(~다더라고요): " + str(sum(1 for _, s, _ in sents if '다더라고요' in s)) + " · 회상(~더라고요, 전언 아님): " + str(sum(1 for _, s, _ in sents if '더라고요' in s and '다더라고요' not in s)) + f"/{len(sents)}", "",
         "## 편마다 첫 문장 · 끝 문장"]
    for d in docs:
        ss = [s for i, s, _ in sents if i == d["id"]]
        S.append(f"- {d['id']}: 첫 「{ss[0]}」 · 끝 「{ss[-1]}」")
    S += ["", "## 문장 전체(벤치 실제 줄 — 대본 예시는 여기서만 가져온다)", *[f"- [{i}] {s}" for i, s, _ in sents]]
    open(os.path.join(a.out, "대본말꼴.md"), "w", encoding="utf-8").write("\n".join(S) + "\n")
    # 팔레트
    pal = {"본 자막": {"fill": "#FFFFFF", "outline": "#000000", "shadow": "#000000", "n_eps": E},
           "제목 흰 줄": {"fill": "#FFFFFF", "outline": "#000000", "n_eps": E},
           "제목 색 줄": [{"ep": d["id"], "hex": [c["hex"] for tl in d["title_lines"] for c in tl["colors"] if c["hex"] != "#FFFFFF"][0]} for d in docs],
           "제품구입 띠": [{"ep": d["id"], "box": L["box"]["hex"], "fill": L["fill_hex"]} for d in docs for L in d["lines"] if L["layer"] == "제품구입띠"],
           "[광고]": {"fill": "#FFFFFF"}, "워터마크": {"fill": "#FFFFFF", "alpha": 0.9}}
    json.dump(pal, open(os.path.join(a.out, "팔레트.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(nums, ensure_ascii=False)); print(ends.most_common(8))

if __name__ == "__main__":
    main()

