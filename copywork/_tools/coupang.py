# -*- coding: utf-8 -*-
"""coupang.py <검색어> [--limit 10] [--out <json>]
쿠팡 파트너스 상품 검색 API — 쿠팡에 실제로 있는 상품만 고르기 위해(회원 규칙 2026-11-07).
키는 ~/.shortem/keys/ 에서 읽고(숏클 설정 화면에서 넣은 것) 절대 출력하지 않는다."""
import os, sys, json, hmac, hashlib, time, argparse, urllib.request, urllib.parse, glob

KEYDIR = os.path.expanduser("~/.shortem/keys")

def load_keys():
    """설정 화면이 저장한 쿠팡 키 파일을 찾는다(이름 꼴이 달라도 된다). 값은 돌려주기만 하고 찍지 않는다."""
    cand = {}
    for p in glob.glob(os.path.join(KEYDIR, "*")):
        n = os.path.basename(p).lower()
        if "coupang" not in n and "쿠팡" not in n: continue
        try: t = open(p, encoding="utf-8-sig").read().strip()
        except Exception: continue
        if t.startswith("{"):
            try:
                d = json.loads(t)
                for k, v in d.items():
                    kl = k.lower()
                    if "secret" in kl: cand["secret"] = str(v).strip()
                    elif "access" in kl: cand["access"] = str(v).strip()
                continue
            except Exception: pass
        if "secret" in n: cand["secret"] = t
        elif "access" in n: cand["access"] = t
        elif "\n" in t:
            a, b = [x.strip() for x in t.splitlines()[:2]]; cand.setdefault("access", a); cand.setdefault("secret", b)
    if "access" not in cand or "secret" not in cand:
        raise SystemExit("쿠팡 파트너스 키를 찾지 못함 — 숏클 설정 화면에서 넣어 주세요(파일: " + ", ".join(os.path.basename(p) for p in glob.glob(os.path.join(KEYDIR, "*"))) + ")")
    return cand["access"], cand["secret"]

def search(keyword, limit=10):
    ak, sk = load_keys()
    path = "/v2/providers/affiliate_open_api/apis/openapi/products/search"
    query = urllib.parse.urlencode({"keyword": keyword, "limit": limit})
    signed = time.strftime("%y%m%dT%H%M%SZ", time.gmtime())
    msg = signed + "GET" + path + query
    sig = hmac.new(sk.encode(), msg.encode(), hashlib.sha256).hexdigest()
    auth = f"CEA algorithm=HmacSHA256, access-key={ak}, signed-date={signed}, signature={sig}"
    req = urllib.request.Request("https://api-gateway.coupang.com" + path + "?" + query, headers={"Authorization": auth, "Content-Type": "application/json;charset=UTF-8"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=30))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"쿠팡 API 실패 {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")
    data = (r.get("data") or {}).get("productData") or []
    return [{"productId": p.get("productId"), "name": p.get("productName"), "price": p.get("productPrice"), "rocket": p.get("isRocket"),
             "free_ship": p.get("isFreeShipping"), "category": p.get("categoryName"), "url": p.get("productUrl"), "image": p.get("productImage")} for p in data]

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("keyword"); ap.add_argument("--limit", type=int, default=10); ap.add_argument("--out")
    a = ap.parse_args()
    res = search(a.keyword, a.limit)
    out = {"keyword": a.keyword, "searched_at": time.strftime("%Y-%m-%d %H:%M"), "n": len(res), "items": res}
    if a.out: json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for i, p in enumerate(res, 1):
        print(i, p["productId"], "로켓" if p["rocket"] else "-", p["price"], p["name"])
