# -*- coding: utf-8 -*-
"""tts.py <08_make/<편>> --voice <voice_id> --model <id> [--stability ..]
대본.json read 줄을 한 번에 일레븐랩스 with-timestamps 로 합성 → tts.mp3 + tts_align.json.
같은 글·같은 목소리·같은 설정이면 저장된 것을 다시 쓴다(두 번 과금 금지). 키 값은 찍지 않는다."""
import sys, os, json, re, hashlib, base64, argparse, urllib.request

KEY = os.path.expanduser("~/.shortem/keys/elevenlabs")

def join(lines):
    out, spans = "", []
    for L in lines:
        t = L["read"].strip()
        end = "." if re.search(r"(니다|요|죠|네요|다|는데|거)$", t) else ""
        s = len(out)
        out += t + end
        spans.append([s, s + len(t)])
        out += " "
    return out.strip(), spans

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("ep"); ap.add_argument("--voice", required=True); ap.add_argument("--model", default="eleven_multilingual_v2")
    ap.add_argument("--stability", type=float, default=0.3); ap.add_argument("--similarity", type=float, default=0.78); ap.add_argument("--style", type=float, default=0.3); ap.add_argument("--speed", type=float, default=None)
    a = ap.parse_args()
    D = json.load(open(os.path.join(a.ep, "대본.json"), encoding="utf-8"))
    for L in D["lines"]:
        if re.search(r"[/¦‖|]", L["read"]):
            raise SystemExit("멈춤: TTS 글에 기호(/ ¦ ‖ |) 있음")
    text, spans = join(D["lines"])
    if a.model == "eleven_v3":
        # v3 는 마지막 말끝을 다 내기 전에 파일을 끊을 때가 있다 → 끝에 쉼표 말줄임을 붙여 꼬리를 남긴다(자막·줄 시각에는 안 씀)
        text += " ..."
    vs = {"stability": a.stability, "similarity_boost": a.similarity, "style": a.style}
    if a.speed: vs["speed"] = a.speed   # 일레븐랩스 말 빠르기(0.7~1.2 · v2 에서만 먹음 — v3 는 무시, 실측 2026-11-08)
    h = hashlib.sha256(json.dumps([text, a.voice, a.model, vs], ensure_ascii=False).encode()).hexdigest()[:16]
    out_mp3, out_js = os.path.join(a.ep, "tts.mp3"), os.path.join(a.ep, "tts_align.json")
    if os.path.exists(out_js) and json.load(open(out_js, encoding="utf-8")).get("hash") == h and os.path.exists(out_mp3):
        print("저장된 합성 다시 씀", h); return
    key = open(KEY, encoding="utf-8").read().strip()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{a.voice}/with-timestamps?output_format=mp3_44100_128",
                                 data=json.dumps({"text": text, "model_id": a.model, "voice_settings": vs, "language_code": "ko"}).encode(),
                                 headers={"xi-api-key": key, "Content-Type": "application/json"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=180))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"합성 실패 {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")
    open(out_mp3, "wb").write(base64.b64decode(r["audio_base64"]))
    al = r.get("alignment") or r.get("normalized_alignment")
    json.dump({"hash": h, "text": text, "spans": spans, "voice": a.voice, "model": a.model, "voice_settings": vs, "chars": len(text),
               "alignment": al}, open(out_js, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("합성 완료", len(text), "자", "align", bool(al))

if __name__ == "__main__":
    main()
