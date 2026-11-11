# -*- coding: utf-8 -*-
"""vary_cn.py <판.json> <08_make/<편>> [--seed N]
편마다 바뀌는 것(회원지시 2026-11-08)을 한 번 골라 대본.json 'vary' 에 적는다 — TTS 전에 돌린다.
- 효과음 팩: 판 sfx.packs 중 하나(편마다 랜덤)
- '이건 ( ) 바로' 끼움말: 판 vary.insert_pool 중 이 편 근거(대본 viral_tags)가 받쳐 주는 것만 → 랜덤
- '진짜 미친 포인트는' 큰글 장면: 화면 효과 1개 + 이목 끄는 효과음 1개 랜덤
씨앗 = 편 폴더 이름 해시(같은 편은 다시 돌려도 같은 답 · --seed 로 바꿈). 이미 vary 가 있으면 그대로 둔다(--again 으로 다시)."""
import sys, os, json, glob, random, hashlib, argparse

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("pan"); ap.add_argument("ep"); ap.add_argument("--seed", type=int); ap.add_argument("--again", action="store_true")
    a = ap.parse_args()
    P = json.load(open(a.pan, encoding="utf-8")); dp = os.path.join(a.ep, "대본.json"); D = json.load(open(dp, encoding="utf-8"))
    def pick_enter(seed):
        EF = P["enter_fx"]; out, prev = {}, None; rnd = random.Random(seed + 2)
        for L in D["lines"][1:]:
            pool = EF["big_pool"] if L.get("layer") == "큰글" else EF["punchy"] if L.get("role") in EF["punchy_roles"] else EF["pool"]
            cand = [p for p in pool if p != prev]; used = list(out.values())
            low = min(used.count(p) for p in cand); k = rnd.choice([p for p in cand if used.count(p) == low])   # 덜 쓴 것부터 — 팩이 고루 나오게
            out[L["id"]] = k; prev = k
        return out
    if D.get("vary") and not a.again:
        ch = False
        if "word_fx" not in D["vary"] and P.get("word_fx"):   # 나중에 생긴 랜덤 칸만 채운다(앞서 고른 것은 그대로)
            D["vary"]["word_fx"] = random.Random(D["vary"]["seed"] + 1).choice(P["word_fx"]["pool"]); ch = True
        if "enter" not in D["vary"] and P.get("enter_fx"):    # 회원지시 2026-11-08 자막 등장 효과 팩 — 줄마다, 같은 것 연달아 없음
            D["vary"]["enter"] = pick_enter(D["vary"]["seed"]); ch = True
        if ch:
            json.dump(D, open(dp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("이미 고름", json.dumps(D["vary"], ensure_ascii=False)); return
    seed = a.seed if a.seed is not None else int(hashlib.md5(os.path.basename(os.path.normpath(a.ep)).encode()).hexdigest()[:8], 16)
    rnd = random.Random(seed); V = P["vary"]
    packs = sorted(glob.glob(os.path.join(HERE, "..", P["sfx"]["packs"])))
    if not packs: raise SystemExit("멈춤: 효과음 팩 없음")
    pack = rnd.choice(packs)
    tags = set(D.get("viral_tags", []))
    ok = [x for x in V["insert_pool"] if set(x.get("need", [])) <= tags]
    if not ok: raise SystemExit(f"멈춤: 끼움말 후보 0(이 편 근거 {sorted(tags)})")
    ins = rnd.choice(ok)["text"]
    fx = rnd.choice(V["big_fx_pool"])
    bk = rnd.choice(V["big_sfx_kinds"]); bpack = rnd.choice(packs)
    lid = V["insert_line"]
    for L in D["lines"]:
        if L["id"] == lid:
            base = V["insert_base"]
            if not L["display"].startswith(base.split()[0]): raise SystemExit(f"멈춤: {lid} 이 '{base}' 꼴이 아님")
            L["display"] = L["read"] = base.replace("()", ins).replace("  ", " ")
            if len(L["display"].replace(" ", "")) > P["caption"]["chunk_max_chars"]: raise SystemExit(f"멈춤: 끼움말 넣고 글자 넘침 {L['display']}")
    D["vary"] = {"seed": seed, "sfx_pack": os.path.basename(pack), "insert": ins, "big_fx": fx,
                 "big_sfx": {"pack": os.path.basename(bpack), "kind": bk},
                 "word_fx": random.Random(seed + 1).choice(P["word_fx"]["pool"]) if P.get("word_fx") else None,
                 "enter": pick_enter(seed) if P.get("enter_fx") else None, "why": "회원지시 2026-11-08 — 편마다 랜덤"}
    json.dump(D, open(dp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("고름", json.dumps(D["vary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
