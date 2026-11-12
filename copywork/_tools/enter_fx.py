# -*- coding: utf-8 -*-
"""enter_fx.py — 숏클 자막 등장 효과 팩(engine/shopping_shorts/static/caption-motions.js CAPTION_MOTIONS)을 그림으로.
회원지시 2026-11-08: '쇼템의 자막등장효과팩 장면마다 알아서, 같은 등장 연속없음'.
- load(js 경로): CAPTION_MOTIONS json 을 읽는다(숏클 파일 그대로 — 값을 손으로 옮기지 않는다)
- pick(pool, roles, seed, punchy): 줄마다 하나, 바로 앞 줄과 같은 것 금지
- apply(layer, box, key, u, em, origin_y): 글자 그림(layer, RGBA)을 u초 시점 등장 모양으로 바꿔 돌려준다(끝나면 그대로)
단위: 통째 / 'word' 어절 / 'char' 글자. 키프레임 칸: opacity · transform(translateX/Y·scale·scaleX) · translate · scale · filter blur · clipPath(아래 끝 자르기) · spreadK."""
import json, re, random
from PIL import Image, ImageFilter


def load(js_path):
    t = open(js_path, encoding="utf-8").read()
    k = "root.CAPTION_MOTIONS = /*JSON*/"; a = t.index(k) + len(k); b = t.index("/*JSON*/", a)
    return json.loads(t[a:b])


def pick(pool, roles, seed, punchy=(), punchy_roles=()):
    rnd = random.Random(seed); out = []
    for role in roles:
        cand = [p for p in (punchy if role in punchy_roles and punchy else pool) if not out or p != out[-1]]
        out.append(rnd.choice(cand))
    return out


# ---- 시간 곡선 ----
def _bez(x1, y1, x2, y2):
    def f(x):
        lo, hi = 0.0, 1.0
        for _ in range(40):
            t = (lo + hi) / 2; bx = 3 * (1 - t) ** 2 * t * x1 + 3 * (1 - t) * t * t * x2 + t ** 3
            if bx < x: lo = t
            else: hi = t
        t = (lo + hi) / 2
        return 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t * t * y2 + t ** 3
    return f


def easing(s):
    s = (s or "linear").strip()
    if s == "linear": return lambda x: x
    if s == "ease": return _bez(.25, .1, .25, 1)
    if s == "ease-in": return _bez(.42, 0, 1, 1)
    if s == "ease-out": return _bez(0, 0, .58, 1)
    if s == "ease-in-out": return _bez(.42, 0, .58, 1)
    m = re.match(r"cubic-bezier\(([^)]*)\)", s)
    if m: return _bez(*[float(v) for v in m.group(1).split(",")])
    m = re.match(r"steps\((\d+)\s*,?\s*(\w+)?\)", s)
    if m:
        n = int(m.group(1)); end = (m.group(2) or "end") != "start"
        return lambda x: min(1.0, (int(x * n) + (0 if end else 1)) / n) if x < 1 else 1.0
    return lambda x: x


# ---- 키프레임 → 칸 값 ----
def _len(v, em, ref):
    v = v.strip()
    if v.endswith("px"): return float(v[:-2])
    if v.endswith("em"): return float(v[:-2]) * em
    if v.endswith("%"): return float(v[:-1]) / 100 * ref
    return float(v or 0)


def _parse(fr, em, uw, uh):
    """키프레임 하나 → {opacity, dx, dy, sx, sy, blur, clip, spread}(빠진 칸은 없음)"""
    o = {}
    if "opacity" in fr: o["opacity"] = float(fr["opacity"])
    tf = fr.get("transform")
    if tf:
        for fn, arg in re.findall(r"(\w+)\(([^)]*)\)", tf):
            if fn == "translateX": o["dx"] = _len(arg, em, uw)
            elif fn == "translateY": o["dy"] = _len(arg, em, uh)
            elif fn == "scale": o["sx"] = o["sy"] = float(arg)
            elif fn == "scaleX": o["sx"] = float(arg)
            elif fn == "scaleY": o["sy"] = float(arg)
    if "translate" in fr:
        p = str(fr["translate"]).split(); p += ["0"] * (2 - len(p))
        o["dx"] = _len(p[0], em, uw); o["dy"] = _len(p[1], em, uh)
    if "scale" in fr:
        p = str(fr["scale"]).split()
        o["sx"] = float(p[0]); o["sy"] = float(p[1] if len(p) > 1 else p[0])
    if "filter" in fr:
        m = re.search(r"blur\(([^)]*)\)", fr["filter"]); o["blur"] = _len(m.group(1), em, uh) if m else 0.0
    if "clipPath" in fr:
        m = re.search(r"inset\(([^)]*)\)", fr["clipPath"])
        if m: o["clip"] = _len(m.group(1).split()[2], em, uh)   # 아래쪽 안쪽 깎음(px)
    if "spreadK" in fr: o["spread"] = float(fr["spreadK"])
    return o


DEF = {"opacity": 1.0, "dx": 0.0, "dy": 0.0, "sx": 1.0, "sy": 1.0, "blur": 0.0, "clip": None, "spread": 0.0}


def _offsets(frames):
    n = len(frames); off = [f.get("offset") for f in frames]
    if off[0] is None: off[0] = 0.0
    if off[-1] is None: off[-1] = 1.0
    i = 0
    while i < n:
        if off[i] is None:
            j = i
            while off[j] is None: j += 1
            a, b = off[i - 1], off[j]
            for k in range(i, j): off[k] = a + (b - a) * (k - i + 1) / (j - i + 1)
            i = j
        i += 1
    return off


def state(M, p, em, uw, uh):
    """효과 M 의 진행 p(0~1, 효과 곡선 적용 전) 시점 값."""
    p = easing(M.get("easing"))(min(1.0, max(0.0, p)))
    frames = M["frames"]; off = _offsets(frames)
    parsed = [_parse(f, em, uw, uh) for f in frames]
    out = dict(DEF)
    for key in DEF:
        pts = [(off[i], parsed[i][key], frames[i].get("easing")) for i in range(len(frames)) if key in parsed[i]]
        if not pts: continue
        if pts[0][0] > 0: pts.insert(0, (0.0, DEF[key], None))
        if pts[-1][0] < 1: pts.append((1.0, DEF[key], None))
        if key == "clip":
            out[key] = next((v for o_, v, _ in reversed(pts) if o_ <= p), pts[0][1]); continue
        for (o1, v1, e1), (o2, v2, _) in zip(pts, pts[1:]):
            if o1 <= p <= o2:
                q = 0 if o2 == o1 else (p - o1) / (o2 - o1); q = easing(e1)(q) if e1 else q
                out[key] = v1 + (v2 - v1) * q; break
        else:
            out[key] = pts[-1][1]
    return out


def units(text, f, x0, kind):
    """글 → 단위 x 범위 [(xa, xb)] — 'char' 글자(공백 뺌) · 'word' 어절 · 없음 통째."""
    if not kind: return [(x0, x0 + f.getlength(text))]
    out = []
    if kind == "word":
        pos = 0
        for w in text.split(" "):
            xa = x0 + f.getlength(text[:pos]); out.append((xa, xa + f.getlength(w))); pos += len(w) + 1
        return out
    for i, ch in enumerate(text):
        if ch == " ": continue
        out.append((x0 + f.getlength(text[:i]), x0 + f.getlength(text[:i + 1])))
    return out


def draw(canvas, layer, band, us, M, u, em, clip_box=None):
    """canvas(RGBA) 위에 layer(글만 그린 RGBA 전체 크기)를 u초 시점 등장 모양으로 얹는다.
    band=(y0, y1) 글 띠 · us=단위 x 범위 · clip_box=(y0, y1) 이 밖으로는 안 그림(흰 자막 띠)."""
    n = len(us); ms = M["ms"] / 1000.0
    st = (M.get("stagger") or 0) / 1000.0; sp = M.get("spread")
    if n > 1 and sp is not None: st = min(st, sp / 1000.0 / (n - 1)) if st else sp / 1000.0 / (n - 1)
    y0, y1 = band; uh = y1 - y0
    mid = (n - 1) / 2
    org = M.get("origin"); oy = 0.5
    if isinstance(org, str):
        p = org.split(); oy = float(p[1].rstrip("%")) / 100 if len(p) > 1 else 0.5
    if not M.get("unit") and n == 1 and u >= ms:
        canvas.alpha_composite(layer); return
    whole = not M.get("unit")
    for i, (xa, xb) in enumerate(us):
        p = (u - i * st) / ms if ms > 0 else 1.0
        xa_, xb_ = int(xa - 0.35 * em), int(xb + 0.35 * em)
        if whole: xa_, xb_ = 0, layer.width
        piece = layer.crop((xa_, y0, xb_, y1))
        if p >= 1:
            canvas.alpha_composite(piece, (xa_, y0)); continue
        if p <= 0 and M["frames"][0].get("opacity", 1) == 0: continue
        s = state(M, max(0.0, p), em, xb - xa, uh)
        if s["opacity"] <= 0.01: continue
        pw, ph = piece.size
        sx, sy = max(0.01, s["sx"]), max(0.01, s["sy"])
        if abs(sx - 1) > 1e-3 or abs(sy - 1) > 1e-3:
            nw, nh = max(1, int(pw * sx)), max(1, int(ph * sy))
            pc = piece.resize((nw, nh), Image.BILINEAR)
            cx = pw / 2; cy = ph * oy
            ox, oy_ = int(cx - cx * sx), int(cy - cy * sy)
        else:
            pc, ox, oy_ = piece, 0, 0
        if s["blur"] > 0.5: pc = pc.filter(ImageFilter.GaussianBlur(s["blur"] / 2))
        if s["opacity"] < 0.999:
            a = pc.getchannel("A").point(lambda v, k=s["opacity"]: int(v * k)); pc = pc.copy(); pc.putalpha(a)
        dx = s["dx"] + (i - mid) * (M.get("spreadX") or 0) * em * s["spread"]
        X, Y = int(xa_ + ox + dx), int(y0 + oy_ + s["dy"])
        if s["clip"] is not None or clip_box:
            lo = y1 if s["clip"] is not None else 10 ** 6
            if clip_box: lo = min(lo, clip_box[1]); hi = clip_box[0]
            else: hi = -10 ** 6
            top_cut = max(0, hi - Y); bot = min(pc.height, lo - Y)
            if bot <= top_cut: continue
            pc = pc.crop((0, top_cut, pc.width, bot)); Y += top_cut
        if X >= canvas.width or Y >= canvas.height: continue
        if X < 0: pc = pc.crop((-X, 0, pc.width, pc.height)); X = 0
        if Y < 0: pc = pc.crop((0, -Y, pc.width, pc.height)); Y = 0
        if pc.width > 0 and pc.height > 0: canvas.alpha_composite(pc, (X, Y))
