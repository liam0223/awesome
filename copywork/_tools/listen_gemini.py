# -*- coding: utf-8 -*-
"""listen_gemini.py <08_make/<편>> [--model gemini-2.5-flash]
완성 영상(final.mp4)을 제미나이 파일 API 로 올려 '소리까지' 듣고 판정 글을 받는다(회원 허락 2026-11-08).
결과 = <편>/소리판정.json. 같은 영상(sha256)·같은 질문이면 저장본을 다시 쓴다(두 번 과금 금지). 키 값은 찍지 않는다."""
import sys, os, json, time, hashlib, argparse, urllib.request, urllib.error

KEY = os.path.expanduser("~/.shortem/keys/gemini")
API = "https://generativelanguage.googleapis.com"


def req(url, data=None, headers=None, method=None, timeout=300):
    r = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        return urllib.request.urlopen(r, timeout=timeout)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"제미나이 오류 {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("ep"); ap.add_argument("--model", default="gemini-2.5-flash"); a = ap.parse_args()
    mp4 = os.path.join(a.ep, "final.mp4"); out = os.path.join(a.ep, "소리판정.json")
    D = json.load(open(os.path.join(a.ep, "대본.json"), encoding="utf-8"))
    T = json.load(open(os.path.join(a.ep, "자막표.json"), encoding="utf-8"))
    script = "\n".join(f"{r['t0']:.1f}~{r['t1']:.1f}초 · {r['text']}" for r in T["rows"])
    sfx = "\n".join(f"{c['t']:.2f}초 {c['kind']}({c.get('why', '')})" for c in T.get("sfx") or [])
    prompt = f"""이 세로 쇼츠 영상을 소리까지 끝까지 듣고 보세요. 한국어로, 아래 JSON 하나만 답하세요.
대본(자막 시각 · 나레가 읽는 글):
{script}
효과음 넣은 시각:
{sfx}
배경음악은 일부러 넣지 않았습니다.

JSON 꼴:
{{"voice": {{"natural": "자연스러움 한 줄", "issues": [{{"t": 초, "what": "발음 틀림·끊김·어색한 억양·너무 빠름 등 들린 그대로"}}]}},
 "script_match": [{{"t": 초, "script": "대본 글", "heard": "실제로 들린 말"}}],
 "sfx": {{"overall": "효과음 크기·개수가 과한지 한 줄", "issues": [{{"t": 초, "what": "너무 큼·작음·장면과 안 맞음·나레를 가림"}}]}},
 "mix": "나레 크기·잡음·끊김·끝 처리 한 줄",
 "picture": [{{"t": 초, "what": "화면에서 눈에 걸리는 것(남의 글자·로고·얼굴·장면과 말이 안 맞음)"}}],
 "verdict": "올려도 됨 / 고칠 곳 있음",
 "fix_first": ["가장 먼저 고칠 것 최대 3개"]}}
들리지 않거나 확실하지 않으면 지어내지 말고 '확실하지 않음'이라고 쓰세요. script_match 에는 대본과 다르게 들린 줄만 넣으세요."""
    sha = hashlib.sha256(open(mp4, "rb").read()).hexdigest()
    qh = hashlib.sha256((prompt + a.model).encode()).hexdigest()[:16]
    if os.path.exists(out):
        old = json.load(open(out, encoding="utf-8"))
        if old.get("sha256") == sha and old.get("q") == qh:
            print("저장된 판정 다시 씀"); print(json.dumps(old["result"], ensure_ascii=False, indent=1)); return
    key = open(KEY, encoding="utf-8").read().strip()
    size = os.path.getsize(mp4)
    # 1) 파일 올리기(resumable)
    r = req(f"{API}/upload/v1beta/files?key={key}", data=json.dumps({"file": {"display_name": os.path.basename(os.path.normpath(a.ep))}}).encode(),
            headers={"X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start", "X-Goog-Upload-Header-Content-Length": str(size),
                     "X-Goog-Upload-Header-Content-Type": "video/mp4", "Content-Type": "application/json"}, method="POST")
    up = r.headers["X-Goog-Upload-URL"]
    r = req(up, data=open(mp4, "rb").read(), headers={"Content-Length": str(size), "X-Goog-Upload-Offset": "0", "X-Goog-Upload-Command": "upload, finalize"}, method="POST", timeout=600)
    f = json.load(r)["file"]
    # 2) 처리 끝까지 기다림
    for _ in range(60):
        if f.get("state") == "ACTIVE": break
        time.sleep(5)
        f = json.load(req(f"{API}/v1beta/{f['name']}?key={key}"))
    if f.get("state") != "ACTIVE": raise SystemExit(f"멈춤: 제미나이 파일 처리 안 끝남 {f.get('state')}")
    # 3) 듣고 판정
    body = {"contents": [{"parts": [{"file_data": {"mime_type": "video/mp4", "file_uri": f["uri"]}}, {"text": prompt}]}],
            "generationConfig": {"response_mime_type": "application/json", "temperature": 0.2}}
    r = json.load(req(f"{API}/v1beta/models/{a.model}:generateContent?key={key}", data=json.dumps(body).encode(),
                      headers={"Content-Type": "application/json"}, method="POST", timeout=600))
    txt = "".join(p.get("text", "") for p in r["candidates"][0]["content"]["parts"])
    try: res = json.loads(txt)
    except Exception: res = {"raw": txt}
    try: req(f"{API}/v1beta/{f['name']}?key={key}", method="DELETE")   # 올린 파일 지우기
    except SystemExit: pass
    json.dump({"sha256": sha, "q": qh, "model": a.model, "who": "제미나이(소리·화면) — 회원 허락 2026-11-08", "usage": r.get("usageMetadata"), "result": res},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
