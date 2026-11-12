# -*- coding: utf-8 -*-
"""뼈대: skeleton.py <03_tear/<id>/뜯기.json> --ch <ch 폴더>
05_lines/<id>.json 뼈대(t0·t1·cut_at·words·loud 만, 나머지 null + _todo)
04_frames/<id>/판독목록.json · sheet_2fps.jpg · lines_sheet.jpg(덩어리마다 자막 띠 + 장면 작은 그림)"""
import sys, os, json, argparse
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
import lib, sheet

TODO_FIELDS = ["speaker", "text", "layer", "read", "role", "enter", "enter_ms", "variant", "emph", "sticker", "sfx", "scene", "scene_desc",
               "fit", "motion", "transition", "y", "x", "align", "max_w", "fill_hex", "font", "size_px", "letter_gap_px", "line_gap_px",
               "outline", "ring", "shadow", "glow", "box", "confidence", "notes", "exit", "enter_curve", "type_cps", "cursor"]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("tear"); ap.add_argument("--ch", required=True)
    a = ap.parse_args()
    T = json.load(open(a.tear, encoding="utf-8"))
    vid = os.path.basename(os.path.dirname(a.tear))
    mp4 = os.path.join(a.ch, T["source"])
    fdir = os.path.join(a.ch, "04_frames", vid); os.makedirs(fdir, exist_ok=True)
    sheet.make_sheet(mp4, 0.5, os.path.join(fdir, "sheet_2fps.jpg"), cols=8, w=180)
    cuts = T["cuts"]["times"]; words = T["audio"]["transcript"]["words"]; r = T["audio"]["rms_025"]
    band = T["layout"].get("caption_band") or T["layout"]["caption_box"]
    lines, changes = [], []
    for it in T["captions"]["items"]:
        t0, t1 = it["t0"], it["t1"]
        L = {"t0": t0, "t1": t1, "cut_at": [c for c in cuts if t0 <= c < t1],
             "words": [w for w in words if w["t1"] > t0 and w["t0"] < t1],
             "loud": r[int(t0 / 0.25): int(t1 / 0.25) + 1]}
        for k in TODO_FIELDS:
            L[k] = None
        lines.append(L); changes.append(t0)
    doc = {"id": vid, "dur": T["probe"]["duration"], "fps": T["probe"]["fps"], "size": [1080, 1920], "form": None, "title_lines": None,
           "source_label": None, "layout": None, "lines": lines, "no_caption": None, "beats": None, "narr_share": None,
           "name_evidence": None, "frame0": None, "notes": None,
           "_todo": ["form", "title_lines", "source_label", "layout", "no_caption", "beats", "narr_share", "name_evidence", "frame0", "notes"]
                    + [f"lines[{i}].{k}" for i in range(len(lines)) for k in TODO_FIELDS]}
    os.makedirs(os.path.join(a.ch, "05_lines"), exist_ok=True)
    out = os.path.join(a.ch, "05_lines", vid + ".json")
    if os.path.exists(out):
        print("이미 있음(덮지 않음):", out)
    else:
        json.dump(doc, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"changes": changes, "cuts": cuts}, open(os.path.join(fdir, "판독목록.json"), "w", encoding="utf-8"), ensure_ascii=False)
    # lines_sheet: 덩어리마다 한 줄 = [번호·시각] [자막 띠 1080 → 720] [장면 작은 그림]
    rows = []
    f = sheet.font(22)
    for i, L in enumerate(lines):
        tm = min(L["t1"] - 0.05, L["t0"] + 0.25)
        img = lib.frame(mp4, tm)
        crop = Image.fromarray(img[band[0] - 20: band[1] + 20]).resize((720, int((band[1] - band[0] + 40) * 720 / 1080)))
        thumb = Image.fromarray(img).resize((60, 107))
        row = Image.new("RGB", (900, max(crop.height, 107)), "black")
        d = ImageDraw.Draw(row)
        d.text((4, 4), f"{i}", fill="yellow", font=f)
        d.text((4, 34), f"{L['t0']:.1f}", fill="white", font=f)
        d.text((4, 64), f"{L['t1']:.1f}", fill="white", font=f)
        row.paste(crop, (80, 0)); row.paste(thumb, (820, 0))
        rows.append(row)
    if rows:
        Hh = sum(r_.height for r_ in rows)
        sh = Image.new("RGB", (900, Hh), "gray"); y = 0
        for r_ in rows:
            sh.paste(r_, (0, y)); y += r_.height
        sh.save(os.path.join(fdir, "lines_sheet.jpg"), quality=90)
    print(vid, len(lines), "줄 뼈대 →", out)

if __name__ == "__main__":
    main()
