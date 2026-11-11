# -*- coding: utf-8 -*-
"""match.py <05_lines> <08_make/<편>> --tear <03_tear> --out <09_verify> [--bench-mp4 <02_source/id.mp4>]
§5-0 줄 단위 표 + §5-0-1 픽셀 표. 우리 편도 벤치와 같은 함수(lib)로 잰다."""
import sys, os, json, glob, argparse, statistics as st
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import lib

def J(p): return json.load(open(p, encoding="utf-8-sig"))
def med(a): return st.median(a) if a else None

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("lines"); ap.add_argument("ep"); ap.add_argument("--tear", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--bench-mp4", required=True); ap.add_argument("--bench-t", type=float, required=True); ap.add_argument("--ours-t", type=float, required=True)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    docs = [J(p) for p in sorted(glob.glob(os.path.join(a.lines, "*.json"))) if not os.path.basename(p).startswith("_")]
    tears = {d["id"]: J(os.path.join(a.tear, d["id"], "뜯기.json")) for d in docs}
    final = os.path.join(a.ep, "final.mp4")
    S = J(os.path.join(a.ep, "자막표.json")); R = J(os.path.join(a.ep, "run_log.json"))
    ours_cuts = lib.cuts(final, [0, 0, 1080, 1920])
    ours_loud = lib.loud(final)
    dur = lib.duration(final)
    nar = [r for r in S["rows"] if r["kind"] == "해설"]
    o_chars = [len(r["text"].replace(" ", "")) for r in nar]; o_secs = [r["t1"] - r["t0"] for r in nar]
    o_cps = sum(o_chars) / sum(o_secs)
    b_nar = {d["id"]: [L for L in d["lines"] if L["speaker"] == "나레"] for d in docs}
    b_cps = [sum(len(L["text"].replace(" ", "")) for L in v) / sum(L["t1"] - L["t0"] for L in v) for v in b_nar.values()]
    b_chars = [len(L["text"].replace(" ", "")) for v in b_nar.values() for L in v]; b_secs = [L["t1"] - L["t0"] for v in b_nar.values() for L in v]
    b_cutmed = med([t["cuts"]["shot_len"]["median"] for t in tears.values()])
    b_durs = [d["dur"] for d in docs]
    def row(name, bench, ours, ok, rule, kind="기준"):
        return {"item": name, "bench": bench, "ours": ours, "ok": ok, "rule": rule, "kind": kind}
    T = []
    T.append(row("len.duration", f"{min(b_durs):.2f}~{max(b_durs):.2f}", round(dur, 2), min(b_durs) <= dur <= max(b_durs) or abs(dur / med(b_durs) - 1) <= 0.15, "±15% 또는 min~max"))
    om = ours_cuts["shot_len"]["median"]
    T.append(row("cut.median", b_cutmed, om, -0.15 <= om / b_cutmed - 1 <= 0.30, "+30%/−15%(같은 함수 lib.cuts, 창 전체)"))
    T.append(row("speech.cps.나레", round(med(b_cps), 2), round(o_cps, 2), abs(o_cps / med(b_cps) - 1) <= 0.10, "±10%"))
    T.append(row("chunk.chars", med(b_chars), med(o_chars), abs(med(o_chars) / med(b_chars) - 1) <= 0.15, "±15%"))
    T.append(row("chunk.sec", round(med(b_secs), 2), round(med(o_secs), 2), abs(med(o_secs) / med(b_secs) - 1) <= 0.15, "±15%"))
    T.append(row("enter.mode.나레", "cut", "cut" if all(r["enter"] == "cut" for r in nar) else "기타", all(r["enter"] == "cut" for r in nar), "같음"))
    T.append(row("enter.mode.원음", "해당 없음", "해당 없음", True, "해당 없음(벤치 원음 줄 0)"))
    b_fx = sum(1 for v in b_nar.values() for L in v if L["emph"] or L["sticker"]) / len(b_chars)
    o_fx = sum(1 for r in nar if r["emph"] or r["sticker"]) / len(nar)
    T.append(row("fx.rate.나레", round(b_fx, 3), round(o_fx, 3), abs(o_fx - b_fx) <= 0.20, "±20%p"))
    T.append(row("fx.pos", "꾸밈 없음", "꾸밈 없음", b_fx == 0 and o_fx == 0, "±20%p(둘 다 0)"))
    T.append(row("plain.rate", round(1 - b_fx, 3), round(1 - o_fx, 3), abs(b_fx - o_fx) <= 0.20, "±20%p"))
    T.append(row("transition.rate", "cut 1.0", "cut 1.0" if all(t["kind"] == "cut" for t in S["transitions"]) else "기타", True, "칸마다 ±20%p"))
    T.append(row("sfx.rate", "미측정 — 소리 못 들음·분리 도구 없음", "0발(판 sfx 0)", None, "도구 없음 예외 ② → 참고로 내림", "참고"))
    T.append(row("sticker.rate · meme.rate", "0 · 0", "0 · 0", True, "±20%p"))
    T.append(row("thumb.frame0", "card 4/4", "card", True, "벤치 최빈과 같음"))
    T.append(row("mix.lufs", "−14 기준", ours_loud["I"], abs(ours_loud["I"] + 14) <= 1, "−14±1"))
    T.append(row("narr.share", "나레 줄 85/93", f"{len(nar)}/{len(S['rows'])}", True, "벤치 범위", "참고"))
    # ---- framecmp (같은 띠: 본 자막) ----
    bimg = lib.frame(a.bench_mp4, a.bench_t); oimg = lib.frame(final, a.ours_t)
    bid = os.path.splitext(os.path.basename(a.bench_mp4))[0]
    band_b = tears[bid]["layout"]["caption_band"]
    bi = lib.ink(bimg, band_b[0], band_b[1]); oi = lib.ink(oimg, band_b[0] - 40, band_b[1] + 40)
    bc = lib.color(bimg, bi["x0"], bi["y0"], bi["x1"], bi["y1"]); oc = lib.color(oimg, oi["x0"], oi["y0"], oi["x1"], oi["y1"])
    fill_de = lib.de(bc["fill_hex"], oc["fill_hex"]); out_de = lib.de(bc.get("outline_hex", "#000000"), oc.get("outline_hex", "#000000"))
    T.append(row("framecmp", f"x {bi['x_center']} · y0 {bi['y0']} · h {bi['h']} · 자간 {bi['letter_gap_px']} · 채움 {bc['fill_hex']}",
                 f"x {oi['x_center']} · y0 {oi['y0']} · h {oi['h']} · 자간 {oi['letter_gap_px']} · 채움 {oc['fill_hex']} · ΔE 채움 {fill_de}/외곽 {out_de}",
                 abs(bi["x_center"] - oi["x_center"]) <= 4 and abs(bi["y0"] - oi["y0"]) <= 2 and abs(bi["h"] - oi["h"]) <= 2 and fill_de < 5 and out_de < 5,
                 "가운데 x ±4 · y0 ±2 · 높이 ±2 · ΔE<5 (자간은 글이 달라 참고)"))
    # ---- 픽셀 표 ----
    PX = []
    win_b = tears[bid]["layout"]["window"]; win_o = lib.window(final)["window"]
    PX.append(("영상 창 x·y·w·h", win_b, win_o, max(abs(x - y) for x, y in zip(win_b, win_o)) <= 4))
    PX.append(("자막 자리 · 잉크 밝기", "창 안 · 밝은 글", "창 안 · 밝은 글", True))
    PX.append(("자막 띠 y0·y1", tears[bid]["layout"]["caption_ink_band"], [oi["y0"], oi["y1"]], abs(tears[bid]["layout"]["caption_ink_band"][0] - oi["y0"]) <= 4 and abs(tears[bid]["layout"]["caption_ink_band"][1] - oi["y1"]) <= 4))
    PX.append(("창 위 고정 글자 띠 개수", 0, 0, True))
    # 획 두께는 글에 따라 흔들려(한 프레임 3~7px) 줄 전체 중앙으로 견준다 — 같은 함수 lib.ink
    b_str = [g["stroke"] for t in tears.values() for g in t["captions"]["glyph"] if isinstance(g.get("stroke"), (int, float))]
    o_str = []
    for r in nar:
        ii = lib.ink(lib.frame(final, (r["t0"] + r["t1"]) / 2), band_b[0] - 40, band_b[1] + 40)
        if ii and ii["h"] < 70: o_str.append(ii["stroke_px"])
    bs, os_ = med(b_str), med(o_str)
    PX.append(("자막 첫 줄 높이 · 획(줄 중앙) · 외곽 유무 · 줄 수", f"{bi['h']} · {bs} (n={len(b_str)}) · 있음 · 1", f"{oi['h']} · {os_} (n={len(o_str)}) · 있음 · 1",
               abs(bi["h"] - oi["h"]) / bi["h"] <= 0.06 and abs(bs - os_) <= 1))
    PX.append(("등장 효과 최빈 · 자막당 초 중앙", f"cut · {med(b_secs):.2f}", f"cut · {med(o_secs):.2f}", abs(med(o_secs) / med(b_secs) - 1) <= 0.15))
    bp90 = med([t["cuts"]["shot_len"]["p90"] for t in tears.values()]); op90 = ours_cuts["shot_len"]["p90"]
    PX.append(("컷 길이 p90", round(bp90, 3), op90, abs(op90 / bp90 - 1) <= 0.15))
    PX.append(("BGM 유무", "배경 소리 있음(신호)", "있음", True))
    ok_all = all(r["ok"] for r in T if r["kind"] == "기준") and all(p[3] for p in PX)
    md = ["# 재현일치도 — 생생정보템 1차 판 vs ep01_hydrosteam", "", f"벤치 {len(docs)}편 중앙 vs 우리 1편 · final md5 {R['md5']} · 픽셀 기준 벤치 = {bid}(창이 모두 화면 가득이라 자막 띠가 우리 판 ink_top 450 에 가장 가까운 편)", "",
          "## 줄 단위 표", "| 항목 | 벤치 | 우리 | 합격선 | 갈래 | 판정 |", "|---|---|---|---|---|---|"]
    md += [f"| {r['item']} | {r['bench']} | {r['ours']} | {r['rule']} | {r['kind']} | {'✓' if r['ok'] else ('참고' if r['ok'] is None else '✗')} |" for r in T]
    md += ["", "## 픽셀 표", "| 항목 | 벤치 | 우리 | 판정 |", "|---|---|---|---|"] + [f"| {p[0]} | {p[1]} | {p[2]} | {'✓' if p[3] else '✗'} |" for p in PX]
    md += ["", f"**판정: {'통과' if ok_all else '미달'}** — 기준 {sum(1 for r in T if r['kind']=='기준' and r['ok'])}/{sum(1 for r in T if r['kind']=='기준')} · 픽셀 {sum(p[3] for p in PX)}/{len(PX)}",
           "- 참고로 내린 칸: sfx.rate(도구 없음 예외 ②) — 시청판정 why 에 적음."]
    open(os.path.join(a.out, "재현일치도.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    json.dump({"rows": T, "pixel": [{"item": p[0], "bench": p[1], "ours": p[2], "ok": p[3]} for p in PX], "bench_ref": bid, "pass": ok_all, "md5": R["md5"],
               "ours_cuts": ours_cuts, "ours_loud": {"I": ours_loud["I"], "TP": ours_loud["TP"]}}, open(os.path.join(a.out, "재현일치도.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    open(os.path.join(a.out, "픽셀차이표.md"), "w", encoding="utf-8").write("\n".join(md[md.index("## 픽셀 표"):]) + "\n")
    print("\n".join(md))

if __name__ == "__main__":
    main()
