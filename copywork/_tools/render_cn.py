# -*- coding: utf-8 -*-
"""render_cn.py <판.json> <08_make/<편>>  — renderer 'cn_window'(위 띠 + 흰 자막 띠 + 영상 창 + 0초 표지 카드 + 노래방 강조)
판 한 파일 + 편 폴더(대본.json · 재료.json · tts.mp3/tts_align.json) → final.mp4 · 자막표.json · timeline.json · run_log.json
값은 판에서만 읽는다(그리는 법만 여기). 모르는 판 칸이면 멈춘다. 화면은 파이썬이 프레임마다 합성한다."""
import sys, os, json, re, time, hashlib, subprocess, argparse, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import lib
from render import narration, glyph_check, J, run
import enter_fx

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = json.load(open(os.path.join(HERE, "..", "_assets", "fonts.json"), encoding="utf-8-sig"))
KNOWN = {"name", "renderer", "version", "history", "_note", "bench", "voice", "cps_target", "tempo_max", "pause_max", "pause_trim_over", "pause_xfade",
         "pause_silence_db", "bgm", "loudness", "length", "timing", "frame", "caption", "cuts", "placement", "rhythm", "title_form", "script", "source",
         "checks", "variables", "frozen_at", "sfx", "intro_fx", "pause_scan_all", "vary", "big_fx", "word_fx", "enter_fx"}
FPS = 30


def font(name, px): return ImageFont.truetype(FONTS[os.path.splitext(name)[0]], int(px))
def rgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def fit_font(name, px, text, max_w):
    f = font(name, px)
    while f.getlength(text) > max_w and px > 10:
        px -= 2; f = font(name, px)
    return f


def draw_center(im, text, f, cy, fill, outline=0, ocol="#000000", x=540):
    d = ImageDraw.Draw(im)
    l, t, r, b = f.getbbox(text)
    d.text((x - (r + l) / 2, cy - (b + t) / 2), text, font=f, fill=rgb(fill) + (255,), stroke_width=outline, stroke_fill=rgb(ocol) + (255,) if outline else None)


def words_line(im, words, hi_idx, f, cy, fill, hi, x=540, shadow=None, wfx=None):
    """낱말 목록을 한 줄로 가운데 정렬, hi_idx 낱말만 hi 색. wfx=(꼴, 그려진 정도 0~1) — 숏클 낱말 강조 팩(caption-motions.js WORDFX · precision20-ui.css .wfx-*)을 그림으로."""
    sp = f.getlength(" ")
    ws = [f.getlength(w) for w in words]
    total = sum(ws) + sp * (len(words) - 1)
    x0 = x - total / 2
    l, t, r, b = f.getbbox("가")
    y = cy - (b + t) / 2
    if shadow:
        sh = Image.new("L", im.size, 0); d = ImageDraw.Draw(sh); xx = x0
        for w, wd in zip(words, ws):
            d.text((xx, y), w, font=f, fill=255, stroke_width=shadow.get("spread", 0), stroke_fill=255); xx += wd + sp
        sh = sh.filter(ImageFilter.GaussianBlur(shadow["blur"] / 2))
        a = (np.array(sh).astype(np.float32) * shadow["alpha"]).astype(np.uint8)
        lay = Image.new("RGBA", im.size, rgb(shadow["hex"]) + (0,)); lay.putalpha(Image.fromarray(a))
        im.alpha_composite(lay)
    if wfx and 0 <= hi_idx < len(words):
        kind, pg = wfx; em = f.size; hx = x0 + sum(ws[:hi_idx]) + sp * hi_idx; hw = ws[hi_idx]; top, bot = y + t, y + b
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay); c = rgb(hi)
        if kind == "underline":
            x1 = hx - .04 * em; dl.rounded_rectangle([x1, bot + .05 * em, x1 + max(1, (hw + .08 * em) * pg), bot + .18 * em], radius=.07 * em, fill=c + (255,))
        elif kind == "highlight":
            x1 = hx - .1 * em; dl.rounded_rectangle([x1, top + .42 * (bot - top), x1 + max(1, (hw + .2 * em) * pg), bot + .06 * em], radius=.1 * em, fill=c + (70,))
        elif kind == "circle":
            dl.arc([hx - .26 * em, top - .2 * em, hx + hw + .26 * em, bot + .2 * em], start=-190, end=-190 + 360 * pg, fill=c + (255,), width=max(2, int(.075 * em)))
        elif kind == "glow":
            # 2026-11-08 ep04 고침: 같은 파랑 번짐을 2배 짙게 깔아 흰 띠 위 강조 글자가 뭉개져 안 읽혔다(1초 시트·제미나이 '모자이크') → 옅은 파랑 번짐(흰색과 섞음)
            cg = tuple(int(v * .45 + 255 * .55) for v in c)
            dl.text((hx, y), words[hi_idx], font=f, fill=cg + (255,), stroke_width=int(.08 * em), stroke_fill=cg + (255,))
            lay = lay.filter(ImageFilter.GaussianBlur(.18 * em)); a = np.array(lay); a[..., 3] = (a[..., 3].astype(np.float32) * (.6 + .4 * pg)).astype(np.uint8); lay = Image.fromarray(a)
        im.alpha_composite(lay)
    d = ImageDraw.Draw(im); xx = x0
    for k, (w, wd) in enumerate(zip(words, ws)):
        d.text((xx, y), w, font=f, fill=rgb(hi if k == hi_idx else fill) + (255,)); xx += wd + sp


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("pan"); ap.add_argument("ep"); a = ap.parse_args()
    P = J(a.pan); ep = a.ep
    unk = set(P) - KNOWN - {k for k in P if k.endswith("_from")}
    if unk: raise SystemExit(f"멈춤: 판에 모르는 칸 {sorted(unk)} — 조용히 버리지 않는다")
    D = J(os.path.join(ep, "대본.json")); M = J(os.path.join(ep, "재료.json"))
    log = {"steps": [], "paid": {"tts_chars": 0, "tts_note": "tts.py 에서 따로 1회(캐시)"}, "not_done": []}
    fr = P["frame"]; cap, big = P["caption"]["layers"]
    # ---- 렌더 전 관문 ----
    body = D["lines"][1:]
    texts = [L["display"] for L in body] + D["title_card"]["lines"] + [D["title_card"]["box"], fr["ad_mark"]["text"]] + D["top_title"]
    miss = glyph_check([t for t in texts if t], [cap["font"], fr["intro"]["line1"]["font"], fr["ad_mark"]["font"]])
    if miss: raise SystemExit(f"멈춤: 글꼴에 없는 글자 {miss[:10]}")
    rx = re.compile(P["script"]["audit"][0]["regex"])
    forbid = D.get("forbidden_words", [])
    for L in D["lines"]:
        if re.search(r"[/¦‖|]", L["read"]): raise SystemExit("멈춤: TTS 글 기호")
        for t in (L["display"], L["read"]):
            if rx.search(t.strip()): raise SystemExit(f"멈춤: 전언 말투(회원지시 규칙 3) '{t}'")
            hit = [w for w in forbid if w and w in t]
            if hit: raise SystemExit(f"멈춤: 금지 낱말(제품명·회사명) {hit} '{t}'")
    for L in body:
        if len(L["display"].replace(" ", "")) > P["caption"]["chunk_max_chars"]: raise SystemExit(f"멈춤: 조각 글자 넘침 {L['display']}")
    # ---- 나레 ----
    P2 = dict(P); P2["tempo_fixed"] = None; P2["tempo_cap"] = True
    nar, line_t, tempo, ndur = narration(ep, P2, log)
    A = J(os.path.join(ep, "tts_align.json")); al = A["alignment"]; cs, ce = al["character_start_times_seconds"], al["character_end_times_seconds"]
    total = round(ndur + P["timing"]["tail"], 3)
    if not P["length"]["min"] <= total <= P["length"]["max"]:
        log["not_done"].append(f"길이 {total}초가 벤치 범위 {P['length']['min']}~{P['length']['max']} 밖")
    # 줄 시각 + 낱말 시각(줄 안 글자 정렬 비율로)
    rows = []
    starts = [s for s, _ in line_t]; starts[0] = 0.0
    for i, L in enumerate(D["lines"]):
        t0 = starts[i]; t1 = starts[i + 1] if i + 1 < len(starts) else total
        s, e = A["spans"][i]; seg = A["text"][s:e]
        ws, pos = [], 0
        for w in L["display"].split():
            k = seg.find(w.replace("?", "")[:1], pos) if w else -1
            ws.append(max(k, pos)); pos = max(k, pos) + len(w)
        span0, span1 = cs[s], ce[min(e, len(ce)) - 1]
        vt0, vt1 = line_t[i]
        wt = [round(vt0 + (cs[min(s + k, len(cs) - 1)] - span0) / max(1e-6, span1 - span0) * (vt1 - vt0), 3) for k in ws]
        wt[0] = t0
        rows.append({"id": L["id"], "kind": "제목" if i == 0 else L.get("layer", "해설"), "t0": round(t0, 3), "t1": round(t1, 3), "text": L["display"],
                     "enter": "cut", "emph": [{"word": w, "t": t, "hex": cap["hi"]} for w, t in zip(L["display"].split(), wt)] if i else [],
                     "sticker": [], "sfx": None, "voice": [round(vt0, 3), round(vt1, 3)]})
        cue = []
        for q in L.get("sfx", []):
            if q["at"] == "cut": tq = t0
            else:
                ws_ = L["display"].split(); hit = [k for k, w in enumerate(ws_) if w.startswith(q["at"])]
                if not hit: raise SystemExit(f"멈춤: 효과음 자리 낱말 '{q['at']}' 이 줄 {L['id']} 에 없음")
                tq = wt[hit[0]]
            cue.append({"kind": q["kind"], "t": round(tq + q.get("off", 0), 3), "why": q.get("why", "")})
        rows[-1]["sfx"] = cue or None
    # ---- 효과음 자리(판 sfx) — 표지 2개 + 줄마다 ----
    SX = P.get("sfx"); sfx_list = []
    if SX:
        for q in SX["intro"]:
            tq = (rows[1]["t0"] if q["at"] == "title_end" else q["at"]) + q.get("off", 0)
            sfx_list.append({"kind": q["kind"], "t": round(max(0.0, tq), 3), "why": "표지"})
        VY = D.get("vary") or {}
        if P.get("vary") and not VY: raise SystemExit("멈춤: 대본에 vary 없음 — vary_cn.py 먼저")
        for c in sfx_list: c["pack"] = VY.get("sfx_pack")
        for r in rows:
            sfx_list += [dict(c, line=r["id"], pack=VY.get("sfx_pack")) for c in (r["sfx"] or [])]
            if r["kind"] == "큰글" and VY.get("big_sfx"):
                sfx_list.append({"kind": VY["big_sfx"]["kind"], "pack": VY["big_sfx"]["pack"], "t": r["t0"], "why": "큰글 장면 이목", "line": r["id"], "peak": "big"})
        sfx_list.sort(key=lambda c: c["t"])
        # 회원지시 2026-11-08 '효과음 한 영상당 10개 이상' — 대본에 적은 것이 모자라면 등장 효과가 센 줄의 시작에 그 효과와 맞는 소리를 더한다
        need_n = SX.get("min_count", 0); EK = VY.get("enter") or {}; AM = SX.get("auto_by_enter") or {}
        if len(sfx_list) < need_n and AM:
            order_ = sorted([r for r in rows[1:] if EK.get(r["id"]) in AM], key=lambda r: SX.get("auto_order", []).index(EK[r["id"]]) if EK[r["id"]] in SX.get("auto_order", []) else 99)
            for r in order_:
                if len(sfx_list) >= need_n: break
                c = {"kind": AM[EK[r["id"]]], "t": round(r["t0"], 3), "why": f"등장 {EK[r['id']]} 맞춤(10개 이상)", "line": r["id"], "pack": VY.get("sfx_pack")}
                tmp = sorted(sfx_list + [c], key=lambda x: x["t"]); i = tmp.index(c)
                nb = [tmp[j] for j in (i - 1, i + 1) if 0 <= j < len(tmp)]
                if all(abs(x["t"] - c["t"]) >= SX["min_gap"] and (x["kind"] != c["kind"] or not x.get("line")) for x in nb):
                    sfx_list = tmp
            if len(sfx_list) < need_n: raise SystemExit(f"멈춤: 효과음 {len(sfx_list)}개 < {need_n}(회원지시) — 대본 sfx 를 더 단다")
        for c1, c2 in zip(sfx_list, sfx_list[1:]):
            if c2["t"] - c1["t"] < SX["min_gap"]: raise SystemExit(f"멈춤: 효과음 간격 {c2['t'] - c1['t']:.2f}초 < {SX['min_gap']} ({c1['kind']}·{c2['kind']})")
            if c1["kind"] == c2["kind"] and c1.get("line") and c2.get("line"): raise SystemExit(f"멈춤: 같은 효과음 연달아 {c1['kind']}")
        rate = len(sfx_list) / total
        if rate > SX["per_sec_max"]: raise SystemExit(f"멈춤: 효과음 {rate:.2f}발/초 > {SX['per_sec_max']} (과함)")
    # ---- 그림 미리 그리기 ----
    ov = os.path.join(ep, "_ov"); os.makedirs(ov, exist_ok=True)
    # 본 틀 위쪽(0~586)
    top = Image.new("RGBA", (1080, fr["caption_box"]["y1"]), rgb(fr["top_band"]["hex"]) + (255,))
    ImageDraw.Draw(top).rectangle([0, fr["caption_box"]["y0"], 1080, fr["caption_box"]["y1"]], fill=rgb(fr["caption_box"]["hex"]) + (255,))
    am = fr["ad_mark"]; fa = font(am["font"], am["px"]); bx = am["box"]
    def ad(im): draw_center(im, am["text"], fa, (bx[1] + bx[3]) / 2, am["fill"], x=(bx[0] + bx[2]) / 2)
    ad(top)
    lg = fr["logo"]
    if lg["text"]:
        draw_center(top, lg["text"], font(lg["font"], lg["px"]), lg["y_ink"] + lg["px"] * 0.4, lg["fill"])
    tt = fr["top_title"]; tl = D["top_title"]
    if len(tl) == 1:
        draw_center(top, tl[0], fit_font(tt["font"], tt["one"]["px"], tl[0], tt["max_w"]), tt["one"]["center_y"], tt["fill"])
    else:
        for k, s_ in enumerate(tl[:2]):
            draw_center(top, s_, fit_font(tt["font"], tt["two"]["px"], s_, tt["max_w"]), tt["two"]["center_y"][k], tt["fill"])
    # 표지 카드(0~652)
    it = fr["intro"]; bxi = it["box"]
    intro = Image.new("RGBA", (1080, bxi["y1"] + bxi["glow"] + 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(intro)
    d.rectangle([0, 0, 1080, it["band_y1"]], fill=rgb(it["band_hex"]) + (255,))
    d.rectangle([0, it["band_y1"], 1080, it["panel_y1"]], fill=rgb(it["panel_hex"]) + (255,))
    glow = Image.new("L", intro.size, 0); ImageDraw.Draw(glow).rectangle([8, bxi["y0"], 1072, bxi["y1"]], fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(bxi["glow"] / 2))
    gl = Image.new("RGBA", intro.size, (255, 255, 255, 0)); gl.putalpha(glow); intro.alpha_composite(gl)
    d = ImageDraw.Draw(intro); d.rectangle([8, bxi["y0"], 1072, bxi["y1"]], fill=rgb(bxi["hex"]) + (255,))
    l1, l2 = D["title_card"]["lines"]
    draw_center(intro, l1, fit_font(it["line1"]["font"], it["line1"]["px"], l1, it["line1"]["max_w"]), it["line1"]["center_y"], it["line1"]["fill"], it["line1"]["outline"])
    draw_center(intro, l2, fit_font(it["line2"]["font"], it["line2"]["px"], l2, it["line2"]["max_w"]), it["line2"]["center_y"], it["line2"]["fill"], it["line2"]["outline"])
    bt = it["box_text"]
    draw_center(intro, D["title_card"]["box"], fit_font(bt["font"], bt["px"], D["title_card"]["box"], bt["max_w"]), (bxi["y0"] + bxi["y1"]) / 2, bt["fill"])
    if it.get("logo") and lg["text"]:   # 회원 2026-11-08 '0~3초 사이 맨 위 가운데 클릭노트 채널 이름 항상' — 본문 로고와 같은 글꼴·크기·자리
        draw_center(intro, lg["text"], font(lg["font"], lg["px"]), lg["y_ink"] + lg["px"] * 0.4, lg["fill"])
    ad(intro)
    intro.save(os.path.join(ov, "intro.png")); top.save(os.path.join(ov, "top.png"))
    fc = font(cap["font"], cap["px"]); fb = font(big["font"], big["px"])
    cache = {}
    def overlay_for(r, t):
        ws = r["text"].split()
        hi = max([k for k, e in enumerate(r["emph"]) if e["t"] <= t] or [0]) if cap.get("karaoke") else -1
        wk = (D.get("vary") or {}).get("word_fx"); wf = None
        if wk and hi >= 0:
            dr = P["word_fx"]["draw"].get(wk, 0)
            pg = 1.0 if not dr else min(1.0, max(0.0, (t - r["emph"][hi]["t"]) / dr))
            wf = (wk, round(pg, 1))
        key = (r["id"], hi, wf)
        if key in cache: return cache[key]
        if r["kind"] == "큰글":
            im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
            half = (len(ws) + 1) // 2
            parts = [ws[:half], ws[half:]] if len(ws) > 2 else [ws]
            l, t_, rr, b = fb.getbbox("가"); lh = b - t_ + big["line_gap"]
            y0 = big["center_y"] - lh * (len(parts) - 1) / 2; k0 = 0
            for j, pw in enumerate(parts):
                words_line(im, pw, hi - k0, fb, y0 + j * lh, big["fill"], big["hi"], shadow=big["shadow"], wfx=wf); k0 += len(pw)
        else:
            tl = Image.new("RGBA", top.size, (0, 0, 0, 0))   # 글만 — 등장 효과는 이 그림을 움직인다
            words_line(tl, ws, hi, fit_font(cap["font"], cap["px"], r["text"], cap["max_w"]), cap["ink_center_y"], cap["fill"], cap["hi"], wfx=wf)
            im = top.copy(); im.alpha_composite(tl); TEXT[key] = tl
        cache[key] = im
        return im
    TEXT = {}
    # ---- 자막 등장 효과(숏클 팩 — 회원지시 2026-11-08 '장면마다 알아서, 같은 등장 연속 없음') ----
    EF = P.get("enter_fx"); ENTER = {}
    if EF:
        MOT = enter_fx.load(os.path.join(os.path.expanduser("~"), EF["motions_js"]))
        ek = (D.get("vary") or {}).get("enter") or {}
        if not ek: raise SystemExit("멈춤: 대본 vary.enter 없음 — vary_cn.py 먼저")
        for r in rows[1:]:
            k = ek.get(r["id"])
            if not k or k not in MOT: raise SystemExit(f"멈춤: 줄 {r['id']} 등장 효과 '{k}' 가 숏클 팩에 없음")
            ENTER[r["id"]] = MOT[k]; r["enter"] = k
        ids = [r["id"] for r in rows[1:]]
        for a_, b_ in zip(ids, ids[1:]):
            if ek[a_] == ek[b_]: raise SystemExit(f"멈춤: 같은 등장 연달아 {a_}·{b_} {ek[a_]}")
    def enter_dur(M, n):
        st = (M.get("stagger") or 0) / 1000.0; sp = M.get("spread")
        if n > 1 and sp is not None: st = min(st, sp / 1000.0 / (n - 1)) if st else sp / 1000.0 / (n - 1)
        return (n - 1) * st + M["ms"] / 1000.0 if M.get("unit") else M["ms"] / 1000.0
    def caption_frame(r, t):
        """등장 중이면 움직이는 글, 아니면 미리 그린 그림."""
        im = overlay_for(r, t); M = ENTER.get(r["id"]); u = t - r["t0"]
        if not M: return im
        if r["kind"] == "큰글":
            em = fb.size; band = (int(big["center_y"] - 2.2 * em), int(big["center_y"] + 2.2 * em)); us = [(0, 1080)]
            if u >= enter_dur(M, 1): return im
            out = Image.new("RGBA", im.size, (0, 0, 0, 0)); enter_fx.draw(out, im, band, us, M, u, em); return out
        f = fit_font(cap["font"], cap["px"], r["text"], cap["max_w"]); em = f.size
        ws_ = r["text"].split(); tot = sum(f.getlength(w) for w in ws_) + f.getlength(" ") * (len(ws_) - 1)
        us = enter_fx.units(r["text"], f, 540 - tot / 2, M.get("unit"))
        if u >= enter_dur(M, len(us)): return im
        key = next(k for k in cache if cache[k] is im)
        out = top.copy(); cb = fr["caption_box"]
        enter_fx.draw(out, TEXT[key], (int(cap["ink_center_y"] - 0.9 * em), int(cap["ink_center_y"] + 0.9 * em)), us, M, u, em, clip_box=(cb["y0"], cb["y1"]))
        return out
    # ---- 영상 토막 ----
    W_ = fr["window"]; big_top = fr["caption_box"]["y0"]
    plan = []
    for i, r in enumerate(rows):
        segs = M["lines"][r["id"]]
        k = len(segs); each = (r["t1"] - r["t0"]) / k; t0 = r["t0"]
        for s in segs:
            plan.append({"line": r["id"], "t0": round(t0, 3), "t1": round(t0 + each, 3), **s, "big": r["kind"] == "큰글"}); t0 += each
    prev_end = {}
    for c in plan:
        src = os.path.join(ep, "src", c["src"])
        w0, h0 = [int(v) for v in lib.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", src])[1].decode().strip().split(",")[:2]]
        if min(w0, h0) < P["source"]["min_h"]: raise SystemExit(f"멈춤: 원본 화질 {min(w0, h0)}p < {P['source']['min_h']}p ({c['src']})")
        need = c["t1"] - c["t0"]; avail = c["b"] - c["a"]
        c["speed"] = round(min(1.0, avail / need), 3)
        if c["speed"] < 0.8: raise SystemExit(f"멈춤: 재료 구간 짧음 {c['src']} {c['a']}~{c['b']} 필요 {need:.2f}초")
        c["b_used"] = round(c["a"] + need * c["speed"], 3)
        # 같은 원본 ±3초 겹침 검사(지침 §2-4)
        for (sv, aa, bb) in prev_end.values():
            pass
        oh = 1920 - (big_top if c["big"] else W_[1]); asp = 1080 / oh
        cx = c.get("cx", 0.5)
        cw = min(w0, int(h0 * asp)); ch_ = int(cw / asp)
        FIT = c["fit"] if isinstance(c.get("fit"), dict) else (P["cuts"].get("fit") or {})   # 컷마다 fit 칸(표지 제품 전체 컷 — 회원 2026-11-10)
        c["fit_cfg"] = FIT
        c["fit"] = bool(FIT) and w0 > h0 * 1.1 and c.get("fit", True) is not False   # 가로 원본은 넓게 보이기(회원 2026-11-08 '화면 너무 줄여 상황 인식 안 됨')
        if c["fit"]:
            A = c.get("fit_aspect", FIT["aspect"]); ch_ = int(h0 * c.get("keep_h", FIT["keep_h"])); cw = min(w0, int(ch_ * A)); ch_ = int(cw / A)
            x = int(min(max(0, cx * w0 - cw / 2), w0 - cw)); y = int((h0 - ch_) * c.get("fit_cy", FIT["cy"]))
            c["fg_h"] = int(round(1080 / A / 2) * 2)
        else:
            zm = c.get("zoom", 1.0)   # 같은 원본 이웃 컷을 당겨 잡아 컷이 보이게(재료.json 컷마다)
            if zm > 1: cw, ch_ = int(cw / zm), int(ch_ / zm)
            x = int(min(max(0, cx * w0 - cw / 2), w0 - cw)); y = int((h0 - ch_) * c.get("cy", 0.5))
        c["crop"] = [x, y, cw, ch_]; c["out_h"] = oh
    # 같은 원본 ±3초 중복 0(지침 §2-4) — 이웃 줄이 같은 샷을 이어 쓰는 것은 빼고, 떨어진 줄끼리만 본다 · 훅(표지) 장면 본문 재사용 금지(§7-28)
    for i, c1 in enumerate(plan):
        for c2 in plan[i + 1:]:
            if c1["src"] != c2["src"] or c1["line"] == c2["line"]: continue
            adj = abs([r["id"] for r in rows].index(c1["line"]) - [r["id"] for r in rows].index(c2["line"])) == 1
            if not adj and c1["a"] - 3 < c2["b_used"] and c2["a"] < c1["b_used"] + 3:
                raise SystemExit(f"멈춤: 같은 원본 ±3초 중복 {c1['src']} {c1['line']} {c1['a']}~{c1['b_used']} / {c2['line']} {c2['a']}~{c2['b_used']}")
    # ---- 프레임 합성 → 인코딩 ----
    raw_v = os.path.join(ep, "_video.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", raw_v], stdin=subprocess.PIPE)
    intro_np = intro; title_end = rows[1]["t0"]
    nframes = int(round(total * FPS)); fi = 0
    tt0 = time.time()
    for c in plan:
        f_end = min(nframes, int(round(c["t1"] * FPS))) if c is not plan[-1] else nframes
        n = f_end - fi
        if n <= 0: continue
        x, y, cw, ch_ = c["crop"]; FIT = c.get("fit_cfg") or {}
        args = ["ffmpeg", "-v", "error", "-ss", f"{c['a']:.3f}", "-t", f"{(c['b_used'] - c['a']) + 0.2:.3f}", "-i", os.path.join(ep, "src", c["src"]),
                "-vf", (f"crop={cw}:{ch_}:{x}:{y},split[f][g];[g]scale=-2:{c['out_h']},crop=1080:{c['out_h']},boxblur={FIT['bg_blur']}:2,eq=brightness={FIT['bg_dark']}[bg];"
                        f"[f]scale=1080:{c['fg_h']}:flags=lanczos[fg];[bg][fg]overlay=0:{int((c['out_h'] - c['fg_h']) * FIT['fg_y'])},setpts=PTS/{c['speed']},fps={FPS}") if c["fit"] else
                       f"crop={cw}:{ch_}:{x}:{y},scale=1080:{c['out_h']}:flags=lanczos,setpts=PTS/{c['speed']},fps={FPS}", "-an", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
        o = subprocess.run(args, capture_output=True, stdin=subprocess.DEVNULL).stdout
        fsz = 1080 * c["out_h"] * 3; got = len(o) // fsz
        if got == 0: raise SystemExit(f"멈춤: 토막 디코딩 실패 {c['src']} {c['a']}")
        arr = np.frombuffer(o[:got * fsz], np.uint8).reshape(got, c["out_h"], 1080, 3)
        for k in range(n):
            t = (fi + k) / FPS
            canvas = Image.new("RGBA", (1080, 1920), rgb(fr["top_band"]["hex"]) + (255,))
            r = next((rr for rr in rows if rr["t0"] <= t < rr["t1"]), rows[-1])
            fr_img = Image.fromarray(arr[min(k, got - 1)])
            bfx = (D.get("vary") or {}).get("big_fx") if r["kind"] == "큰글" and t >= title_end else None
            if bfx == "mono": fr_img = fr_img.convert("L").convert("RGB")
            canvas.paste(fr_img, (0, 1920 - c["out_h"]))
            if t < title_end:
                canvas.alpha_composite(intro_np)
            elif r["kind"] == "큰글":
                band = Image.new("RGBA", (1080, big_top), rgb(fr["top_band"]["hex"]) + (255,)); band.alpha_composite(top.crop((0, 0, 1080, big_top)))
                canvas.alpha_composite(band); canvas.alpha_composite(caption_frame(r, t))
            else:
                canvas.alpha_composite(caption_frame(r, t), (0, 0))
            if bfx in ("shake", "zoom_punch", "flash"):
                BF = P["big_fx"][bfx]; u = t - r["t0"]
                if u < BF["sec"]:
                    if bfx == "shake":
                        amp = BF["px"] * (1 - u / BF["sec"]); rr_ = random.Random(fi + k)
                        dx, dy = int(rr_.uniform(-amp, amp)), int(rr_.uniform(-amp, amp))
                        sh = Image.new("RGBA", (1080, 1920), rgb(fr["top_band"]["hex"]) + (255,)); sh.alpha_composite(canvas, (max(0, dx), max(0, dy)), (max(0, -dx), max(0, -dy))); canvas = sh
                    elif bfx == "zoom_punch":
                        z = BF["from"] - (BF["from"] - 1) * (u / BF["sec"]); w2, h2 = int(1080 / z), int(1920 / z)
                        canvas = canvas.crop(((1080 - w2) // 2, (1920 - h2) // 2, (1080 - w2) // 2 + w2, (1920 - h2) // 2 + h2)).resize((1080, 1920), Image.BILINEAR)
                    else:
                        canvas = Image.blend(canvas.convert("RGB"), Image.new("RGB", (1080, 1920), (255, 255, 255)), BF["alpha"] * (1 - u / BF["sec"])).convert("RGBA")
            IF = P.get("intro_fx")
            if IF:
                z, fl = 1.0, 0.0
                if t < IF["start_zoom_sec"]:
                    u = t / IF["start_zoom_sec"]; z = IF["start_zoom"] - (IF["start_zoom"] - 1) * (1 - (1 - u) ** 3)
                if t < IF["start_flash_sec"]: fl = 1 - t / IF["start_flash_sec"]
                if title_end <= t < title_end + IF["cut_zoom_sec"]:
                    u = (t - title_end) / IF["cut_zoom_sec"]; z = IF["cut_zoom"] - (IF["cut_zoom"] - 1) * (1 - (1 - u) ** 3)
                if z > 1.0005:
                    w2, h2 = int(1080 / z), int(1920 / z)
                    canvas = canvas.crop(((1080 - w2) // 2, (1920 - h2) // 2, (1080 - w2) // 2 + w2, (1920 - h2) // 2 + h2)).resize((1080, 1920), Image.BILINEAR)
                if fl > 0:
                    canvas = Image.blend(canvas.convert("RGB"), Image.new("RGB", (1080, 1920), (255, 255, 255)), fl * 0.85).convert("RGBA")
            enc.stdin.write(canvas.convert("RGB").tobytes())
        fi = f_end
        c["frames_short"] = max(0, n - got)
    enc.stdin.close(); enc.wait()
    log["steps"].append({"name": "프레임 합성", "sec": round(time.time() - tt0, 2)})
    # ---- 소리: 나레만(배경음 없음 — 판 bgm.none) → −14 LUFS ----
    I0 = lib.loud(nar)["I"]; g = P["loudness"]["lufs"] - I0
    mixn = os.path.join(ep, "_mixn.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", nar, "-af", f"apad=whole_dur={total},volume={g:.2f}dB,alimiter=limit={10 ** (P['loudness']['tp'] / 20):.4f}:level=false",
         "-ar", "48000", "-ac", "2", mixn], log, "음량 맞추기")
    if sfx_list:
        ins, fl = ["-i", mixn], []
        for k, c in enumerate(sfx_list):
            f = os.path.join(HERE, "..", "_assets", "sfx", c["pack"], c["kind"] + ".wav")
            mv = float(re.search(r"max_volume: (-?[\d.]+) dB", lib.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "volumedetect", "-f", "null", "-"])[2])[1])
            ins += ["-i", f]; ms = int(c["t"] * 1000)
            fl.append(f"[{k + 1}:a]aresample=48000,aformat=channel_layouts=stereo,volume={(D.get('sfx_peak_override') or {}).get(c.get('peak', c['kind']), SX['peak_dbfs'][c.get('peak', c['kind'])]) - mv:.2f}dB,adelay={ms}|{ms}[s{k}]")
        fl.append("[0:a]" + "".join(f"[s{k}]" for k in range(len(sfx_list))) + f"amix=inputs={len(sfx_list) + 1}:duration=first:normalize=0[m]")
        mixs = os.path.join(ep, "_mixs.wav")
        run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[m]", "-ar", "48000", "-ac", "2", mixs], log, f"효과음 {len(sfx_list)}발 섞기")
        mixn = mixs
    I1 = lib.loud(mixn)["I"]          # 2차: 섞은 결과를 다시 재서 남은 차이를 맞춘다(1차에서 −0.7~−1.5 LU 모자랐음)
    if True:   # 2026-11-08 ep04 고침: 차이 0.3 LU 안이면 이 단계를 건너뛰어 효과음 섞은 소리가 리미터 없이 나가 TP −0.4(효과음 최고점 0.0 dBFS) → 늘 리미터를 거친다
        mix2 = os.path.join(ep, "_mixn2.wav")
        run(["ffmpeg", "-v", "error", "-y", "-i", mixn, "-af", f"volume={P['loudness']['lufs'] - I1:.2f}dB,alimiter=limit={10 ** (P['loudness']['tp'] / 20):.4f}:level=false", mix2], log, "음량 맞추기 2차")
        mixn = mix2
    final = os.path.join(ep, "final.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", raw_v, "-i", mixn, "-t", f"{total:.3f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final], log, "합치기")
    md5 = hashlib.md5(open(final, "rb").read()).hexdigest()
    json.dump({"rows": rows, "sfx": sfx_list, "vary": D.get("vary"), "intro_fx": P.get("intro_fx"), "transitions": [{"t": c["t0"], "kind": "cut", "ms": 0} for c in plan[1:]]}, open(os.path.join(ep, "자막표.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"cuts": plan, "total": total, "tempo": tempo}, open(os.path.join(ep, "timeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ldf = lib.loud(final)
    log.update({"pan": os.path.relpath(a.pan, ep), "pan_version": P.get("version"), "total": total, "tempo": tempo, "lufs": ldf["I"], "tp": ldf["TP"], "md5": md5})
    log["not_done"].append("소리를 귀로 들어 보지 않음(클로드는 들을 수 없음 — 회원 판정 때 들어 달라고 할 것)")
    json.dump(log, open(os.path.join(ep, "run_log.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("완성", final, "길이", total, "배속", tempo, "LUFS", ldf["I"], "TP", ldf["TP"], "컷", len(plan))


if __name__ == "__main__":
    main()
