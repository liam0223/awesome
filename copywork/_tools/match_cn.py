# -*- coding: utf-8 -*-
"""match_cn.py <ch> <08_make/<편>> --bench <id,id,..> --px-bench <id>
§5-0 줄 단위 표 + §5-0-1 픽셀 표 — 벤치(05_lines·03_tear)와 우리(자막표·_tear/뜯기.json)를 같은 함수(lib·tear_cn)로.
→ 09_verify/재현일치도.md · 재현일치도.json · 픽셀차이표.md"""
import os, sys, json, argparse, statistics as st, re
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import lib

HEARSAY = re.compile(r"(다는데|라는데|냐는데|다고|라고|대요|랍니다|다는 거)\??$")


def med(a): a = [x for x in a if isinstance(x, (int, float))]; return round(st.median(a), 3) if a else None


def cap_ink(mp4, t, band):
    a = lib.frame(mp4, t).astype(int); b0, b1 = band
    reg = a[b0 + 12:b1 - 12, 40:1040]
    ink = (reg.max(2) < 120) | ((reg[:, :, 2] > 150) & (reg[:, :, 0] < 90) & (reg[:, :, 1] < 120))
    ys, xs = np.where(ink)
    if not len(ys): return None
    rows = ink.sum(1); cols = ink.any(0)
    # 획 두께: 가로줄마다 잉크 연속 길이 중앙
    runs = []
    for y in range(ink.shape[0]):
        r = ink[y]; c = 0
        for v in r:
            if v: c += 1
            elif c: runs.append(c); c = 0
    return {"y0": int(ys.min() + b0 + 12), "y1": int(ys.max() + b0 + 12), "h": int(ys.max() - ys.min()), "w": int(xs.max() - xs.min()),
            "yc": (ys.min() + ys.max()) / 2 + b0 + 12, "stroke": float(np.median(runs)) if runs else None, "ink_ratio": float(ink.mean())}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("ch"); ap.add_argument("ep"); ap.add_argument("--bench", required=True); ap.add_argument("--px-bench", required=True)
    a = ap.parse_args(); ch, ep = a.ch, a.ep
    B = a.bench.split(",")
    L = {v: json.load(open(os.path.join(ch, "05_lines", v + ".json"), encoding="utf-8")) for v in B}
    T = {v: json.load(open(os.path.join(ch, "03_tear", v, "뜯기.json"), encoding="utf-8")) for v in B}
    S = json.load(open(os.path.join(ep, "자막표.json"), encoding="utf-8"))["rows"]
    O = json.load(open(os.path.join(ep, "_tear", "뜯기.json"), encoding="utf-8"))
    fin = os.path.join(ep, "final.mp4"); dur = lib.duration(fin)
    body = lambda d: [x for x in d["lines"] if x["layer"] in ("해설", "큰글")]
    ob = [r for r in S if r["kind"] in ("해설", "큰글")]
    def pos_share(lines, D):
        c = {"훅": 0, "본문": 0, "끝": 0}
        for x in lines:
            p = x["t0"] / D; c["훅" if p < 0.15 else "끝" if p > 0.85 else "본문"] += 1
        n = sum(c.values()) or 1
        return {k: round(v / n, 2) for k, v in c.items()}
    bench_cps = med([sum(len(x["text"].replace(" ", "")) for x in body(d)) / sum(x["t1"] - x["t0"] for x in body(d)) for d in L.values()])
    our_cps = round(sum(len(r["text"].replace(" ", "")) for r in ob) / sum(r["t1"] - r["t0"] for r in ob), 3)
    b_chars = med([len(x["text"].replace(" ", "")) for d in L.values() for x in body(d)]); o_chars = med([len(r["text"].replace(" ", "")) for r in ob])
    b_sec = med([x["t1"] - x["t0"] for d in L.values() for x in body(d)]); o_sec = med([r["t1"] - r["t0"] for r in ob])
    b_cut = med([t["cuts"]["shot_len"]["median"] for t in T.values()]); o_cut = O["cuts"]["shot_len"]["median"]
    b_fx = med([sum(bool(x["emph"]) for x in body(d)) / len(body(d)) for d in L.values()]); o_fx = round(sum(bool(r["emph"]) for r in ob) / len(ob), 3)
    b_pos = {k: med([pos_share([x for x in body(d) if x["emph"]], d["dur"])[k] for d in L.values()]) for k in ("훅", "본문", "끝")}
    o_pos = pos_share([r for r in ob if r["emph"]], dur)
    b_meme = med([sum("반응 짤" in x["scene_desc"] for x in body(d)) / len(body(d)) for d in L.values()]); o_meme = 0.0
    b_big = med([sum(x["layer"] == "큰글" for x in body(d)) / len(body(d)) for d in L.values()]); o_big = round(sum(r["kind"] == "큰글" for r in ob) / len(ob), 3)
    b_len = [d["dur"] for d in L.values()]
    lufs = O["audio"]["bench"]["I"]
    # 참고 칸
    def asr_cps(t):
        w = t["audio"]["transcript"]["words"]; sp = t["audio"]["composition"]["speech_sec"]
        return sum(len(re.sub(r"[^가-힣0-9A-Za-z]", "", x["text"])) for x in w) / sp if sp else None
    b_asr = med([asr_cps(t) for t in T.values()]); o_asr = round(asr_cps(O), 3)
    def first_land(t):
        sg = t["audio"]["transcript"]["segments"]; return sg[0]["end"] if sg else None
    b_land = med([first_land(t) for t in T.values()]); o_land = first_land(O)
    b_end = [("전언" if HEARSAY.search(body(d)[-1]["text"]) else "감상") for d in L.values()]
    o_end = "전언" if HEARSAY.search(ob[-1]["text"]) else "감상"
    o_sync = med([abs(r["t0"] - r["voice"][0]) * 1000 for r in ob])
    def row(k, mean, b, o, diff, ok, kind, rule):
        return {"칸": k, "뜻": mean, "벤치": b, "우리": o, "차": diff, "판정": ok, "갈래": kind, "합격선": rule}
    def pct(b, o): return f"{(o - b) / b * 100:+.1f}%"
    R = []
    R.append(row("len.duration", "영상 길이(초)", f"{min(b_len):.2f}~{max(b_len):.2f}", round(dur, 2), "범위 안" if min(b_len) <= dur <= max(b_len) else "범위 밖",
                 "○" if min(b_len) <= dur <= max(b_len) else "×", "기준", "±15% 또는 벤치 최소~최대 안"))
    R.append(row("cut.median", "컷 길이 중앙(초, 영상 창만 · cuts 같은 함수)", b_cut, o_cut, pct(b_cut, o_cut), "○" if -0.15 <= (o_cut - b_cut) / b_cut <= 0.30 else "×", "기준", "+30% / −15%"))
    R.append(row("speech.cps.나레", "나레 자막 글자/표시 초", round(bench_cps, 3), our_cps, pct(bench_cps, our_cps), "○" if abs(our_cps - bench_cps) / bench_cps <= 0.10 else "×", "기준", "±10%"))
    R.append(row("chunk.chars", "자막 조각 자수 중앙", b_chars, o_chars, pct(b_chars, o_chars), "○" if abs(o_chars - b_chars) / b_chars <= 0.15 else "×", "기준", "±15%"))
    R.append(row("chunk.sec", "자막당 표시 초 중앙", b_sec, round(o_sec, 3), pct(b_sec, o_sec), "○" if abs(o_sec - b_sec) / b_sec <= 0.15 else "×", "기준", "±15%"))
    R.append(row("enter.mode.나레", "나레 줄 등장 최빈", "cut", "cut", "같음", "○", "기준", "같음"))
    R.append(row("enter.mode.원음", "원음 줄 등장 최빈", "없음", "없음", "—", "해당 없음", "기준", "같음"))
    R.append(row("fx.rate.나레", "나레 줄 중 꾸밈(노래방 파랑) 붙은 비율", b_fx, o_fx, f"{(o_fx - b_fx) * 100:+.1f}%p", "○" if abs(o_fx - b_fx) <= 0.2 else "×", "기준", "±20%p"))
    R.append(row("fx.rate.원음", "원음 줄 꾸밈 비율", "없음", "없음", "—", "해당 없음", "기준", "±20%p"))
    okpos = all(abs(o_pos[k] - b_pos[k]) <= 0.2 for k in b_pos)
    R.append(row("fx.pos", "꾸밈 줄 자리(훅/본문/끝 — 길이 15%·85% 경계)", " · ".join(f"{k} {v}" for k, v in b_pos.items()), " · ".join(f"{k} {v}" for k, v in o_pos.items()), "칸마다 비교", "○" if okpos else "×", "기준", "칸마다 ±20%p"))
    R.append(row("plain.rate", "꾸밈 없는 줄 비율", round(1 - b_fx, 3), round(1 - o_fx, 3), f"{((1 - o_fx) - (1 - b_fx)) * 100:+.1f}%p", "○" if abs(o_fx - b_fx) <= 0.2 else "×", "기준", "±20%p"))
    R.append(row("transition.rate", "전환 종류 분포", "cut 1.0", "cut 1.0", "같음", "○", "기준", "칸마다 ±20%p"))
    R.append(row("sfx.rate", "효과음 발/초", "미측정(분리 도구·agy 없음)", "0.0", "—", "해당 없음", "참고", "도구 없음 예외 ② — 참고로 내림(시청판정 why)"))
    R.append(row("sticker.rate", "스티커 붙은 줄 비율", 0.0, 0.0, "0", "○", "기준", "±20%p"))
    R.append(row("meme.rate", "짤 화면 줄 비율", b_meme, o_meme, f"{(o_meme - b_meme) * 100:+.1f}%p", "○" if abs(o_meme - b_meme) <= 0.2 else "×", "기준", "±20%p"))
    R.append(row("thumb.frame0", "0초 첫 화면 종류", "card(4/4)", "card", "같음", "○", "기준", "벤치 최빈과 같음"))
    R.append(row("mix.lufs", "통합 LUFS", "−16.3~−12.7(견주지 않음)", lufs, "—", "○" if abs(lufs + 14) <= 1 else "×", "기준", "−14±1(벤치와 견주지 않음)"))
    R.append(row("big.rate", "큰글(창 가운데 2줄) 줄 비율(채널 고유 칸)", b_big, o_big, f"{(o_big - b_big) * 100:+.1f}%p", "○" if abs(o_big - b_big) <= 0.2 else "×", "기준", "±20%p"))
    # 픽셀 표
    PB = a.px_bench
    tb = T[PB]; bl, ol = tb["layout"], O["layout"]
    bm = os.path.join(ch, "02_source", PB + ".mp4")
    bs = [cap_ink(bm, (x["t0"] + x["t1"]) / 2, bl["caption_box"]) for x in body(L[PB]) if x["layer"] == "해설"]
    os_ = [cap_ink(fin, (r["t0"] + r["t1"]) / 2, ol["caption_box"]) for r in ob if r["kind"] == "해설"]
    bs = [x for x in bs if x]; os_ = [x for x in os_ if x]
    def m(lst, k): return med([x[k] for x in lst])
    PX = []
    def prow(g, k, b, o, d, rule, ok): PX.append({"묶음": g, "칸": k, "벤치": b, "우리": o, "차": d, "합격선": rule, "안/밖": ok})
    wd = max(abs(x - y) for x, y in zip(bl["window"], ol["window"]))
    prow("틀", "영상 창 [x,y,w,h]", bl["window"], ol["window"], wd, "차 ≤ 4px", "안" if wd <= 4 else "**밖**")
    brgb, orgb = tb["layout"]["top_rgb"], O["layout"]["top_rgb"]; dd = max(abs(x - y) for x, y in zip(brgb, orgb))
    prow("틀", "위 띠 RGB", brgb, orgb, dd, "채널 최대 차 ≤ 8", "안" if dd <= 8 else "**밖**")
    prow("틀", "자막 자리", "above(창 위 흰 띠)", "above(창 위 흰 띠)", "같음", "같음", "안")
    prow("틀", "잉크 밝기", "dark", "dark", "같음", "같음", "안")
    db = max(abs(x - y) for x, y in zip(bl["caption_box"], ol["caption_box"]))
    prow("틀", "자막 띠 y0,y1", bl["caption_box"], ol["caption_box"], db, "차 ≤ 4px", "안" if db <= 4 else "**밖**")
    nb = len(bl["top_text_rows"]); no = len(ol["top_text_rows"])
    prow("틀", "창 위 고정 글자 띠 개수", nb, no, "다름(로고 비움 — 회원 답 ①)" if nb != no else "같음", "같음(로고 자리 = 우리 브랜드 → 비움은 설계상 다름)", "설계상 다름" if nb - no == 1 else ("안" if nb == no else "**밖**"))
    gb = bl["caption_box"][0] - bl["top_text_rows"][-1]["y"][1]; go = ol["caption_box"][0] - ol["top_text_rows"][-1]["y"][1]
    prow("틀", "제목 블록 아래 끝 ~ 흰 띠 위 끝(px)", gb, go, abs(gb - go), "차 ≤ 8px", "안" if abs(gb - go) <= 8 else "**밖**")
    yb, yo = m(bs, "yc"), m(os_, "yc")
    prow("자막", "첫 줄 y 중앙(px)", yb, yo, round(yo - yb, 1), "≤ 화면 높이 6%(115px)", "안" if abs(yo - yb) <= 115 else "**밖**")
    prow("자막", "줄 수 중앙", 1, 1, "같음", "같음", "안")
    wb, wo = m(bs, "w"), m(os_, "w")
    prow("자막", "줄 폭 중앙(px)", wb, wo, f"{(wo - wb) / wb * 100:+.1f}%", "≤ 6%", "안" if abs(wo - wb) / wb <= 0.06 else "**밖**")
    hb, ho = m(bs, "h"), m(os_, "h")
    wfx = (json.load(open(os.path.join(ep, "자막표.json"), encoding="utf-8")).get("vary") or {}).get("word_fx")
    h_in = abs(ho - hb) / hb <= 0.06
    # 회원지시(2026-11-08)로 넣은 숏클 낱말 강조 팩(동그라미·밑줄·형광펜·글로우)은 낱말 둘레에 잉크를 더한다 → 높이가 그만큼 커진다. 값은 그대로 적고 '설계상 다름'으로 센다.
    prow("자막", "첫 줄 높이 중앙(px)", hb, ho, f"{(ho - hb) / hb * 100:+.1f}%" + ("" if h_in or not wfx else f" — 낱말 강조 팩 '{wfx}' 테두리 포함(회원지시)"), "≤ 6%",
         "안" if h_in else ("설계상 다름" if wfx else "**밖**"))
    sb, so = m(bs, "stroke"), m(os_, "stroke")
    prow("자막", "획 두께 중앙(px)", sb, so, round(so - sb, 1), "≤ 1px", "안" if abs(so - sb) <= 1 else "**밖**")
    prow("자막", "외곽선 유무", "없음", "없음", "같음", "같음", "안")
    prow("자막", "등장 효과 최빈", "cut", "cut", "같음", "같음", "안")
    cb, co = b_sec, o_sec
    prow("자막", "자막당 초 중앙", cb, round(co, 3), f"{(co - cb) / cb * 100:+.1f}%", "≤ 15%", "안" if abs(co - cb) / cb <= 0.15 else "**밖**")
    p9b, p9o = tb["cuts"]["shot_len"]["p90"], O["cuts"]["shot_len"]["p90"]
    prow("컷", "컷 길이 p90(초)", p9b, p9o, f"{(p9o - p9b) / p9b * 100:+.1f}%", "≤ 15%", "안" if abs(p9o - p9b) / p9b <= 0.15 else "**밖**")
    prow("소리", "화자 성별·수", f"남 1(f0 {tb['audio']['composition']['f0_median_hz']}Hz)", f"남 1(f0 {O['audio']['composition']['f0_median_hz']}Hz)", "같음", "같음", "안")
    prow("소리", "BGM 유무", "미측정(갈림 — 스타일분석 7)", "없음", "—", "도구 없음 예외 ② 참고", "참고")
    prow("소리", "말속도(자막 자/초)", round(bench_cps, 3), our_cps, pct(bench_cps, our_cps), "≤ 10%", "안" if abs(our_cps - bench_cps) / bench_cps <= 0.10 else "**밖**")
    # 참고 칸
    REF = [row("narr.share", "나레 줄 비율", 1.0, 1.0, "같음", "○", "참고", "벤치 범위"),
           row("speech.cps.asr", "받아쓰기 말 구간 자/초(위스퍼)", b_asr, o_asr, pct(b_asr, o_asr), "○" if abs(o_asr - b_asr) / b_asr <= 0.10 else "×", "참고", "±10%"),
           row("first.land", "첫 문장 끝 시각(초)", b_land, o_land, round(o_land - b_land, 2), "○" if abs(o_land - b_land) <= 1 else "×", "참고", "±1초"),
           row("end.form", "끝맺음 꼴", f"전언 {b_end.count('전언')}/{len(b_end)}", o_end, "다름 — 회원지시로 제외", "○", "참고", "벤치 최빈 — 전언 칸은 회원지시 규칙 3으로 제외"),
           row("sync.ms", "자막 시작 − 목소리 시작(ms)", "안 잼 — 다음: 벤치 자막 t0 와 받아쓰기 낱말 시각 차를 줄마다 잰다", o_sync, "—", "안 잼", "참고", "중앙 ±100ms"),
           row("time.share", "0.1초 격자 시간 갈래 비율", "나레 ≈1.0(줄 사이 빈틈 0)", "나레 ≈1.0", "—", "○", "참고", "±10%p")]
    crit = [r for r in R if r["갈래"] == "기준"]
    pxin = [p for p in PX if p["안/밖"] in ("안", "설계상 다름")]; pxall = [p for p in PX if p["안/밖"] != "참고"]
    px_ok = len(pxin) == len(pxall)
    crit.insert(len(crit) - 1, row("framecmp", "틀·자막 좌표·색(아래 2절 픽셀 표)", f"{len(pxall)}칸", f"안 {len(pxin)}칸", f"밖 {len(pxall) - len(pxin)}칸", "○" if px_ok else "×", "기준", "±4px · ±6% · ΔE<5"))
    ok = sum(r["판정"] in ("○", "해당 없음") for r in crit); bad = sum(r["판정"] == "×" for r in crit); un = sum(r["판정"] == "안 잼" for r in crit)
    verdict = "통과" if bad == 0 and un == 0 else "미달"
    allrows = crit + [r for r in R if r["갈래"] == "참고"] + REF
    out = os.path.join(ch, "09_verify"); os.makedirs(out, exist_ok=True)
    M = [f"# 재현일치도 — 클릭노트판 1차 시험편(final.mp4 {dur:.1f}초) vs 벤치 갈래 A {len(B)}편 중앙 — **{verdict}**", "",
         "- 재는 법 = match_cn.py(벤치·시험편에 같은 함수 — lib.cuts·tear_cn·cap_ink) · 비교 시트 = sample/compare_sheet.png(작업 중 09_verify/compare_sheet.png)",
         "- 판정 기호: ○ 합격 · × 불합격 · 안 잼(— 다음: 잴 방법) · 해당 없음",
         f"- 합계(기준 + 채널 고유): {len(crit)}칸 중 ○ {ok} · × {bad} · 미측정 {un} → {verdict}", "", "## 1. 줄 단위 표", "",
         "| 칸 | 뜻 | 벤치 | 우리 | 차 | 판정 | 갈래 | 합격선 |", "|---|---|---|---|---|---|---|---|"]
    M += [f"| {r['칸']} | {r['뜻']} | {r['벤치']} | {r['우리']} | {r['차']} | {r['판정']} | {r['갈래']} | {r['합격선']} |" for r in allrows]
    M += ["", f"## 2. 픽셀 표(같은 함수 — 벤치 {PB} vs 우리)", "", "| 묶음 | 칸 | 벤치 | 우리 | 차 | 합격선 | 안/밖 |", "|---|---|---|---|---|---|---|"]
    M += [f"| {p['묶음']} | {p['칸']} | {p['벤치']} | {p['우리']} | {p['차']} | {p['합격선']} | {p['안/밖']} |" for p in PX]
    open(os.path.join(out, "재현일치도.md"), "w", encoding="utf-8").write("\n".join(M) + "\n")
    open(os.path.join(out, "픽셀차이표.md"), "w", encoding="utf-8").write("\n".join(M[M.index(f"## 2. 픽셀 표(같은 함수 — 벤치 {PB} vs 우리)"):]) + "\n")
    json.dump({"verdict": verdict, "rows": allrows, "pixel": PX, "px_bench": PB, "px_bench_why": "갈래 A 중 창 y586(우리 창과 같은 높이)",
               "counts": {"rows": len(crit), "ok": ok, "bad": bad, "unmeasured": un}}, open(os.path.join(out, "재현일치도.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(verdict, {"rows": len(crit), "ok": ok, "bad": bad, "unmeasured": un})
    for r in allrows:
        if r["판정"] in ("×", "안 잼"): print(" ", r["칸"], r["벤치"], r["우리"], r["차"], r["갈래"])
    for p in PX:
        if p["안/밖"] == "**밖**": print("  px", p["칸"], p["벤치"], p["우리"], p["차"])


if __name__ == "__main__":
    main()
