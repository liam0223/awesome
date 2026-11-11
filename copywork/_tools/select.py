# -*- coding: utf-8 -*-
"""선정: select.py <채널 주소> --out <ch>/01_select [--ids id1,id2,..] [--n 6]
채널 쇼츠 전체 목록(전체목록.json) + top.json + 선정표.md + 메타표.md + 길이분포.png
--ids 를 주면 그 편만 고른다(편 수를 늘리지 않는다 — 지침 §2-0)."""
import json, subprocess, sys, os, statistics, re, datetime, argparse

def ytdlp_json(args):
    r = subprocess.run(["yt-dlp", "--no-warnings", *args], capture_output=True, stdin=subprocess.DEVNULL)
    if r.returncode != 0:
        raise SystemExit("yt-dlp 실패: " + r.stderr.decode("utf-8", "replace")[-400:])
    return json.loads(r.stdout.decode("utf-8"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("channel"); ap.add_argument("--out", required=True)
    ap.add_argument("--ids", default=""); ap.add_argument("--n", type=int, default=6)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    url = a.channel.rstrip("/")
    if not url.endswith("/shorts"):
        url += "/shorts"
    pl = ytdlp_json(["--flat-playlist", "-J", url])
    entries = pl.get("entries") or []
    now = datetime.date.today()
    rows = []
    for e in entries:
        rows.append({"id": e.get("id"), "title": e.get("title"), "views": e.get("view_count"),
                     "comments": e.get("comment_count"), "likes": e.get("like_count"),
                     "upload_date": e.get("upload_date"), "duration": e.get("duration"),
                     "desc_head": (e.get("description") or "")[:120] or None})
    ids = [i for i in a.ids.split(",") if i]
    # 고른 편 + 목록에서 빈 칸(올린 날·길이·좋아요·댓글)은 상세 정보로 채운다
    detail_ids = set(ids) | {r["id"] for r in sorted(rows, key=lambda r: -(r["views"] or 0))[:max(18, a.n * 3)]}
    info = {}
    for vid in detail_ids:
        try:
            d = ytdlp_json(["--skip-download", "-J", f"https://www.youtube.com/shorts/{vid}"])
            info[vid] = d
        except SystemExit as ex:
            info[vid] = {"_err": str(ex)}
    for r in rows:
        d = info.get(r["id"])
        if d and "_err" not in d:
            for k, src in (("views", "view_count"), ("comments", "comment_count"), ("likes", "like_count"),
                           ("upload_date", "upload_date"), ("duration", "duration")):
                if r[k] is None:
                    r[k] = d.get(src)
            if r["desc_head"] is None:
                r["desc_head"] = (d.get("description") or "")[:120]
    for vid in ids:  # 목록에 없는 준 편
        if vid not in {r["id"] for r in rows} and vid in info and "_err" not in info[vid]:
            d = info[vid]
            rows.append({"id": vid, "title": d.get("title"), "views": d.get("view_count"), "comments": d.get("comment_count"),
                         "likes": d.get("like_count"), "upload_date": d.get("upload_date"), "duration": d.get("duration"),
                         "desc_head": (d.get("description") or "")[:120]})
    for r in rows:
        for k in ("views", "comments", "likes", "upload_date", "duration"):
            if r[k] is None:
                r[k] = "미측정"
        if r["upload_date"] != "미측정" and isinstance(r["views"], int):
            ud = datetime.datetime.strptime(r["upload_date"], "%Y%m%d").date()
            r["views_per_day"] = round(r["views"] / max(1, (now - ud).days), 1)
        else:
            r["views_per_day"] = "미측정"
    json.dump(rows, open(os.path.join(a.out, "전체목록.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    views = [r["views"] for r in rows if isinstance(r["views"], int)]
    any_info = next((d for d in info.values() if "_err" not in d), {})
    subs = any_info.get("channel_follower_count")
    if ids:
        top_ids, how = ids, "회원이 준 편만(§2-0)"
    else:
        cand = [r for r in rows[:30] if isinstance(r["views_per_day"], float)]
        top_ids = [r["id"] for r in sorted(cand, key=lambda r: -r["views_per_day"])[:a.n]]
        how = "최근 30편 안 하루당 조회 상위"
    med = statistics.median(views) if views else None
    top = {"channel": any_info.get("channel"), "handle": any_info.get("uploader_id"), "subs": subs,
           "total": len(rows), "views_median": med, "views_max": max(views) if views else None,
           "views_median_per_sub": round(med / subs, 2) if med and subs else "미측정",
           "measured_at": now.isoformat(), "how": how, "top_ids": top_ids}
    json.dump(top, open(os.path.join(a.out, "top.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    byid = {r["id"]: r for r in rows}
    L = [f"# 선정표 — {top['channel']} ({top['handle']})", "",
         f"구독 {subs} · 쇼츠 {len(rows)}편 · 조회 중앙 {med} · 최대 {top['views_max']} · 구독 대비 조회 중앙 {top['views_median_per_sub']} · 잰 날 {now}",
         f"고르는 법: {how}", "", "| 주소 | 제목 | 조회 | 올린 날 | 길이 | 하루당 조회 |", "|---|---|---|---|---|---|"]
    for i in top_ids:
        r = byid.get(i, {})
        L.append(f"| https://www.youtube.com/shorts/{i} | {r.get('title')} | {r.get('views')} | {r.get('upload_date')} | {r.get('duration')} | {r.get('views_per_day')} |")
    open(os.path.join(a.out, "선정표.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

    # 메타표: 제목 길이·끝꼴·이모지·물음표 / 올리는 간격
    def emoji(t): return bool(re.search(r"[\U0001F300-\U0001FAFF☀-➿]", t or ""))
    titles = [r["title"] or "" for r in rows]
    tl = [len(t) for t in titles]
    dates = sorted(r["upload_date"] for r in rows if r["upload_date"] != "미측정")
    gaps = [(datetime.datetime.strptime(b, "%Y%m%d") - datetime.datetime.strptime(a_, "%Y%m%d")).days for a_, b in zip(dates, dates[1:])]
    M = ["# 메타표", "", f"n = {len(rows)}편(전체 목록)", "",
         f"- 제목 글자 수: 중앙 {statistics.median(tl) if tl else '미측정'} · 최소~최대 {min(tl) if tl else '-'}~{max(tl) if tl else '-'}",
         f"- 이모지 들어간 제목: {sum(emoji(t) for t in titles)}/{len(titles)}",
         f"- 물음표로 끝나는 제목: {sum(t.strip().endswith('?') for t in titles)}/{len(titles)}",
         f"- 올리는 간격(일): 중앙 {statistics.median(gaps) if gaps else '미측정'} (n={len(gaps)})",
         f"- 최근 30일 업로드: {sum(1 for d in dates if (now - datetime.datetime.strptime(d, '%Y%m%d').date()).days <= 30)}편",
         "- 상관은 '같이 움직인다'까지만 적는다(원인 아님). 표본이 작으면 적지 않는다."]
    open(os.path.join(a.out, "메타표.md"), "w", encoding="utf-8").write("\n".join(M) + "\n")

    # 길이분포.png (5초 칸)
    from PIL import Image, ImageDraw
    durs = [r["duration"] for r in rows if isinstance(r["duration"], (int, float))]
    bins = {}
    for d in durs:
        bins[int(d // 5) * 5] = bins.get(int(d // 5) * 5, 0) + 1
    W, H = 800, 400
    im = Image.new("RGB", (W, H), "white"); dr = ImageDraw.Draw(im)
    if bins:
        ks = list(range(0, max(bins) + 5, 5)); mx = max(bins.values()); bw = (W - 40) / len(ks)
        for j, k in enumerate(ks):
            h = (bins.get(k, 0) / mx) * (H - 60)
            dr.rectangle([20 + j * bw, H - 30 - h, 20 + (j + 1) * bw - 2, H - 30], fill=(70, 110, 200))
            dr.text((20 + j * bw, H - 25), str(k), fill="black")
    im.save(os.path.join(a.out, "length_hist.png"))
    print(json.dumps(top, ensure_ascii=False))

if __name__ == "__main__":
    main()

