# -*- coding: utf-8 -*-
"""rules_cn.py <05_lines> --out <06_rules> --tear <03_tear>
규칙빈도.json/.md · 대본말꼴.md · 팔레트.json(규격서 3-6 꼴) — 클릭노트 꼴(나레 + 흰 띠 자막 + 표지 카드)."""
import os, sys, json, glob, re, argparse, statistics as st
from collections import Counter


def grade(k, n):
    if n < 5: return "표본부족"
    r = k / n
    return "강" if r >= 0.6 else "중" if r >= 0.3 else "약"


def q(a):
    a = sorted(x for x in a if isinstance(x, (int, float)))
    if not a: return None
    n = len(a)
    if n < 10:
        return {"n": n, "min": round(a[0], 3), "med": round(st.median(a), 3), "max": round(a[-1], 3)}
    p = lambda f: round(a[min(n - 1, int(f * (n - 1) + 0.5))], 3)
    return {"n": n, "p10": p(0.1), "med": round(st.median(a), 3), "p90": p(0.9), "min": round(a[0], 3), "max": round(a[-1], 3)}


END_KINDS = [("전언", r"(다는데|라는데|냐는데|다고|라고|대요|랍니다|다네|라네|다는 거|라는 거)\??$"),
             ("~는 거(설명 맺음)", r"는 거$"), ("감상", r"(네|네요|싶네)$"), ("잇는 꼴", r"(고|서|며|면|데|게|는|던|을|를|의|이|가|은|도|에|까지|처럼|대신|사이에서|때문에|때|인데|다가|다)$")]


def ending(t):
    t = t.strip()
    for name, rx in END_KINDS:
        if re.search(rx, t): return name
    return "기타"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("lines"); ap.add_argument("--out", required=True); ap.add_argument("--tear", required=True)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    docs = [json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(os.path.join(a.lines, "*.json"))) if not os.path.basename(p).startswith("_")]
    tear = {d["id"]: json.load(open(os.path.join(a.tear, d["id"], "뜯기.json"), encoding="utf-8")) for d in docs}
    E = len(docs)
    BODY = [(d["id"], L) for d in docs for L in d["lines"] if L["layer"] in ("해설", "큰글")]
    n = len(BODY)
    rules = []
    def add(cond, eff, k, nn, base=None, unit="줄"):
        rules.append({"cond": cond, "effect": eff, "unit": unit, "k": k, "n": nn, "rate": round(k / nn, 3) if nn else None, "base": base, "grade": grade(k, nn)})
    add("본 자막 줄(표지 뒤)", "enter=cut(첫 프레임부터 완성)", sum(L["enter"] == "cut" for _, L in BODY), n)
    add("본 자막 줄", "emph=노래방 파랑(나레 낱말 따라 옮겨 감)", sum(bool(L["emph"]) for _, L in BODY), n)
    add("본 자막 줄", "layer=흰 띠 검은 글", sum(L["layer"] == "해설" for _, L in BODY), n)
    add("본 자막 줄", "layer=큰글(흰 띠 숨기고 창 가운데 큰 2줄)", sum(L["layer"] == "큰글" for _, L in BODY), n)
    add("본 자막 줄", "sticker 없음", sum(not L["sticker"] for _, L in BODY), n)
    add("본 자막 줄", "한 줄(줄바꿈 없음 — 흰 띠)", sum(L["layer"] == "해설" for _, L in BODY), n)
    add("편", "0초 표지 카드(밝은 막 + 흰/파랑 큰 2줄 + 흰 상자 작은 글) · 나레가 읽음", sum(any(L["layer"] == "제목" for L in d["lines"]) for d in docs), E, unit="편")
    add("편", "노래방 파랑 강조가 있는 편", sum(any(L["emph"] for L in d["lines"] if L["layer"] != "제목") for d in docs), E, unit="편")
    add("편", "큰글 줄(창 가운데) 1개 이상", sum(any(L["layer"] == "큰글" for L in d["lines"]) for d in docs), E, unit="편")
    add("편", "반응 짤(남의 얼굴 반응 장면) 1개 이상", sum(any("반응 짤" in L["scene_desc"] for L in d["lines"]) for d in docs), E, unit="편")
    add("편", "[광고] 위 띠 오른쪽 처음부터 끝", E, E, unit="편")
    add("편", "'이건 바로' 줄 다음 줄에 제품 이름 공개", sum(any(L["text"].startswith("이건 바로") for L in d["lines"]) for d in docs), E, unit="편")
    add("편", "끝 줄 = 전언 꼴(~다는데/~다고)", sum(ending([L for L in d["lines"] if L["layer"] != "제목"][-1]["text"]) == "전언" for d in docs), E, unit="편")
    add("편", "'게다가/심지어/더 ~ 건/진짜 ~ 포인트는' 둘째 장점 이음 줄", sum(any(re.match(r"(게다가|심지어|더 |진짜 |이게 미친|미친 포인트|대박인)", L["text"]) for L in d["lines"]) for d in docs), E, unit="편")
    # 숫자
    chars = [len(L["text"].replace(" ", "")) for _, L in BODY]
    secs = [L["t1"] - L["t0"] for _, L in BODY]
    cps_ep = []
    for d in docs:
        nl = [L for L in d["lines"] if L["layer"] in ("해설", "큰글")]
        cps_ep.append(sum(len(L["text"].replace(" ", "")) for L in nl) / sum(L["t1"] - L["t0"] for L in nl))
    gaps = [b["t0"] - x["t1"] for d in docs for x, b in zip(d["lines"][1:], d["lines"][2:])]
    shot = [x for t in tear.values() for x in t["cuts"]["shot_list"]]
    role_first = {}
    for r in ["다리", "공개", "반전", "고조", "끝"]:
        v = []
        for d in docs:
            xs = [L["t0"] / d["dur"] for L in d["lines"] if L["role"] == r]
            if xs: v.append(min(xs) * 100)
        role_first[r] = q(v)
    reveal = []
    for d in docs:
        xs = [L["t0"] for L in d["lines"] if L["role"] == "공개"]
        if xs: reveal.append(round(xs[0] / d["dur"] * 100, 1))
    asr_cps = []
    for t in tear.values():
        w = t["audio"]["transcript"]["words"]
        if w:
            tot = sum(len(re.sub(r"[^가-힣0-9A-Za-z]", "", x["text"])) for x in w); sp = t["audio"]["composition"]["speech_sec"]
            asr_cps.append(tot / sp if sp else None)
    nums = {"편 수": E, "본 자막 줄 수": n, "조각 글자(공백 뺌)": q(chars), "조각 표시 초": q(secs), "자막 자/초(편마다)": q(cps_ep),
            "받아쓰기 말 구간 자/초(편마다)": q(asr_cps), "줄 사이 빈틈 초": q(gaps), "컷 길이 초(전 편 샷)": q(shot),
            "편 컷 중앙": q([t["cuts"]["shot_len"]["median"] for t in tear.values()]), "컷/분": q([t["cuts"]["cut_per_min"] for t in tear.values()]),
            "길이 초": q([d["dur"] for d in docs]), "표지 초": q([[L["t1"] for L in d["lines"] if L["layer"] == "제목"][0] for d in docs]),
            "공개 자리(%)": q(reveal), "LUFS": q([t["audio"]["bench"]["I"] for t in tear.values()]), "TP": q([t["audio"]["bench"]["TP"] for t in tear.values()]),
            "나레 f0": q([t["audio"]["composition"]["f0_median_hz"] for t in tear.values()]),
            "말 없는 구간 RMS dB(BGM 바닥)": q([t["bgm_rules"]["floor_db"] for t in tear.values()]),
            "나레 말 구간 RMS dB": q([t["audio"]["phrase_loud"]["나레(말 구간 RMS dB 중앙)"] for t in tear.values()]),
            "fit 평균": round(st.mean(L["fit"] for _, L in BODY), 2), "fit 7 미만 비율": round(sum(L["fit"] < 7 for _, L in BODY) / n, 3),
            "역할 첫 자리(%)": role_first, "역할 줄 수": dict(Counter(L["role"] for _, L in BODY)),
            "큰글 줄 표시 초": q([L["t1"] - L["t0"] for _, L in BODY if L["layer"] == "큰글"])}
    json.dump({"rules": rules, "episodes": [d["id"] for d in docs], "by_layer": dict(Counter(L["layer"] for d in docs for L in d["lines"])), "nums": nums},
              open(os.path.join(a.out, "규칙빈도.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    M = ["# 규칙빈도 — 클릭노트", "", f"표본 {E}편 · 본 자막 줄 {n}개 · 등급: n≥5 이고 비율 ≥0.6 강 / ≥0.3 중 / 그 밑 약 / n<5 표본부족", "",
         "| 조건 | 효과 | 분모 | k/n | 비율 | 등급 |", "|---|---|---|---|---|---|"]
    M += [f"| {r['cond']} | {r['effect']} | {r['unit']} | {r['k']}/{r['n']} | {r['rate']} | {r['grade']} |" for r in rules]
    M += ["", "## 숫자", "```json", json.dumps(nums, ensure_ascii=False, indent=1), "```"]
    open(os.path.join(a.out, "규칙빈도.md"), "w", encoding="utf-8").write("\n".join(M) + "\n")
    # 대본말꼴 — 문장 = 맺는 꼴(전언·~는 거·감상)이 나올 때까지 이어 붙인 조각
    sents = []
    for d in docs:
        cur = []
        for L in [L for L in d["lines"] if L["layer"] in ("해설", "큰글")]:
            cur.append(L["text"])
            k = ending(L["text"])
            if k in ("전언", "~는 거(설명 맺음)", "감상"):
                sents.append((d["id"], " ".join(cur), k)); cur = []
        if cur: sents.append((d["id"], " ".join(cur), "안 맺음"))
    ends = Counter(k for _, _, k in sents)
    chunk_ends = Counter(ending(L["text"]) for _, L in BODY)
    S = ["# 대본말꼴 — 클릭노트", "", f"문장 {len(sents)}개(본 자막 조각을 맺는 꼴까지 이어 붙임) · 편 {E} · 조각 {n}", "",
         "## 문장 맺음 분포", *[f"- {k}: {v}/{len(sents)}" for k, v in ends.most_common()], "",
         "## 조각 끝 꼴", *[f"- {k}: {v}/{n}" for k, v in chunk_ends.most_common()], "",
         f"- 문장 글자(공백 뺌): {q([len(s.replace(' ', '')) for _, s, _ in sents])}",
         "- 격식체(~니다) 문장: " + str(sum(1 for _, s, _ in sents if re.search(r'니다$', s))) + f"/{len(sents)}",
         "- 해요체(~요) 문장: " + str(sum(1 for _, s, _ in sents if re.search(r'요$', s))) + f"/{len(sents)}",
         "- 반말 서술(~다는데·~다고·~는 거) = 이 채널 기본 말투",
         "- 회원지시 규칙 3: 전언(~다는데·~라는데·~다고·~대요·~랍니다·~라고 하네요)은 우리 대본에서 쓰지 않는다 — 같은 자리를 직접 말하는 꼴(~입니다·~해요·~죠·~는 거죠)로 바꾼다", "",
         "## 이음 낱말(조각 첫 낱말) 상위", *[f"- {k}: {v}" for k, v in Counter(L['text'].split()[0] for _, L in BODY).most_common(12)], "",
         "## 편마다 첫 문장 · 끝 문장"]
    for d in docs:
        ss = [s for i, s, _ in sents if i == d["id"]]
        S.append(f"- {d['id']}: 첫 「{ss[0]}」 · 끝 「{ss[-1]}」")
    S += ["", "## 문장 전체(벤치 실제 줄 — 대본 뼈대는 여기서만 가져온다)", *[f"- [{i}] ({k}) {s}" for i, s, k in sents]]
    open(os.path.join(a.out, "대본말꼴.md"), "w", encoding="utf-8").write("\n".join(S) + "\n")
    # 팔레트(규격서 3-6)
    def role(items):
        c = {}
        for hx, vid in items:
            if not hx: continue
            r = c.setdefault(hx, {"hex": hx, "n_lines": 0, "docs": set()}); r["n_lines"] += 1; r["docs"].add(vid)
        return [{"hex": r["hex"], "n_lines": r["n_lines"], "n_docs": len(r["docs"]), "docs": sorted(r["docs"])} for r in sorted(c.values(), key=lambda r: -r["n_lines"])]
    pal = {"n_docs": E, "roles": {
        "본문": role([(L["fill_hex"], i) for i, L in BODY if L["layer"] == "해설"]),
        "강조": role([(e["hex"], i) for i, L in BODY for e in L["emph"][:1]]),
        "외곽선": [], "글로우": [],
        "제목": role([(c["hex"], d["id"]) for d in docs for tl in d["title_lines"] for c in tl["colors"]]),
        "띠": role([(d["layout"]["bg_hex"], d["id"]) for d in docs]),
        "스티커": [], "출처": []}}
    json.dump(pal, open(os.path.join(a.out, "팔레트.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(nums, ensure_ascii=False)); print(ends.most_common())


if __name__ == "__main__":
    main()
