# -*- coding: utf-8 -*-
"""받기: fetch.py <01_select/top.json> --out <ch>/02_source
1080p 세로 원본 + info.json + ko.vtt + comments.json → 받기검사.md(여덟 검사)"""
import json, subprocess, sys, os, argparse, glob

FORMATS = ['137+ba[ext=m4a]/bv*[height>=1080]+ba/b', 'bv*[height>=720]+ba/b', 'b']

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL)
    return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")

def probe(p):
    c, o, e = run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", p])
    return json.loads(o) if c == 0 else None

def checks(mp4, list_dur):
    res = {}
    res["1 크기"] = os.path.exists(mp4) and os.path.getsize(mp4) > 200_000
    pr = probe(mp4) if res["1 크기"] else None
    res["2 열림"] = pr is not None
    vs = [s for s in (pr or {}).get("streams", []) if s["codec_type"] == "video"]
    as_ = [s for s in (pr or {}).get("streams", []) if s["codec_type"] == "audio"]
    res["3 화면 트랙"] = bool(vs); res["4 소리 트랙"] = bool(as_)
    h = int(vs[0]["height"]) if vs else 0; w = int(vs[0]["width"]) if vs else 0
    res["5 세로 720 이상"] = h >= 720
    dur = float((pr or {}).get("format", {}).get("duration", 0))
    res["6 길이"] = isinstance(list_dur, (int, float)) and abs(dur - list_dur) <= 1.5
    if as_:
        c, o, e = run(["ffmpeg", "-hide_banner", "-i", mp4, "-af", "volumedetect", "-vn", "-f", "null", "-"])
        mv = [l for l in e.splitlines() if "mean_volume" in l]
        mean = float(mv[0].split(":")[1].replace("dB", "")) if mv else -99
        res["7 무음 아님"] = mean > -50
    else:
        res["7 무음 아님"] = False
    c, o, e = run(["ffmpeg", "-v", "error", "-i", mp4, "-f", "null", "-"])
    res["8 끝까지 디코딩"] = c == 0 and not e.strip()
    return res, {"w": w, "h": h, "dur": round(dur, 3)}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("top"); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    top = json.load(open(a.top, encoding="utf-8"))
    lst = {r["id"]: r for r in json.load(open(os.path.join(os.path.dirname(a.top), "전체목록.json"), encoding="utf-8"))}
    os.makedirs(a.out, exist_ok=True)
    lines = ["# 받기검사", "", "| 편 | 1 크기 | 2 열림 | 3 화면 | 4 소리 | 5 세로≥720 | 6 길이 | 7 무음아님 | 8 디코딩 | 해상도 | 길이(초) | 받은 꼴 | 통과 |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    ok_n = 0
    for vid in top["top_ids"]:
        url = f"https://www.youtube.com/shorts/{vid}"
        base = os.path.join(a.out, vid)
        mp4 = base + ".mp4"
        res = None
        for fi, fmt in enumerate(FORMATS[:3]):
            if not os.path.exists(mp4):
                run(["yt-dlp", "--no-warnings", "-f", fmt, "--merge-output-format", "mp4", "-o", base + ".%(ext)s",
                     "--write-info-json", "--write-auto-subs", "--write-subs", "--sub-langs", "ko", "--sub-format", "vtt", url])
            res, meta = checks(mp4, lst.get(vid, {}).get("duration"))
            if all(res.values()):
                break
            if os.path.exists(mp4):
                os.remove(mp4)
        # 댓글(따로, 실패해도 영상은 성공)
        c, o, e = run(["yt-dlp", "--no-warnings", "--skip-download", "--write-comments", "--extractor-args", "youtube:max_comments=200",
                       "-o", base + "_c.%(ext)s", "--write-info-json", url])
        ci = base + "_c.info.json"
        if os.path.exists(ci):
            d = json.load(open(ci, encoding="utf-8"))
            json.dump([{"text": x.get("text"), "likes": x.get("like_count"), "author_is_uploader": x.get("author_is_uploader")} for x in (d.get("comments") or [])],
                      open(base + ".comments.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            os.remove(ci)
        ok = all(res.values())
        ok_n += ok
        lines.append(f"| {vid} | " + " | ".join("○" if v else "✗" for v in res.values()) +
                     f" | {meta['w']}×{meta['h']} | {meta['dur']} | {FORMATS[fi]} | {'○' if ok else '✗'} |")
        print(vid, ok, meta, flush=True)
    vtts = {v: os.path.exists(os.path.join(a.out, v + ".ko.vtt")) for v in top["top_ids"]}
    lines += ["", f"받은 편 {ok_n}/{len(top['top_ids'])} · 자동자막(ko.vtt) 있음 {sum(vtts.values())}/{len(vtts)} · 전체 목록 {top['total']}편"]
    open(os.path.join(a.out, "받기검사.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")

if __name__ == "__main__":
    main()
