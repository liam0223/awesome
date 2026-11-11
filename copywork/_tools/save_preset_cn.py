# -*- coding: utf-8 -*-
"""save_preset_cn.py <ch_click_note> <presets/<슬러그>> <편 폴더 이름>
클릭노트판 저장(지침서 §11 · preset_spec.md 1-2 나무) — 작업 폴더 파일에서 프리셋 폴더를 만든다.
값은 작업 폴더 파일에서 읽고, 숫자마다 _from 을 붙인다(근거는 FROM 표 — 판_만든기록·스타일분석·뜯기에서 옮김)."""
import sys, os, json, re, glob, shutil, copy, subprocess, collections

CH, OUT, EPN = sys.argv[1], sys.argv[2], sys.argv[3]
EP = os.path.join(CH, "08_make", EPN)
J = lambda p: json.load(open(p, encoding="utf-8"))
def W(name, obj):
    p = os.path.join(OUT, name)
    if isinstance(obj, str): open(p, "w", encoding="utf-8").write(obj)
    else: json.dump(obj, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "lines")); os.makedirs(os.path.join(OUT, "sample"))
BENCH = ["Uu_SJaiAuwQ", "HmGDP6rrqo8", "BG8D7oeIhwY", "3iQHc3oTP2Q"]   # 갈래 A(조회 많은 4편) — 판이 따른 갈래
TODAY = "2026-11-08"

# ---------------- lines/ (줄판독 8편) — confidence 는 어휘 하나로, 자세한 것은 confidence_note
LINES = {}
for f in sorted(glob.glob(os.path.join(CH, "05_lines", "*.json"))):
    n = os.path.basename(f)
    if n.startswith("_"): continue
    d = J(f); LINES[d["id"]] = d
    o = copy.deepcopy(d)
    for l in o["lines"]:
        c = str(l.get("confidence") or "")
        first = next((w for w in ["픽셀", "눈", "신호", "미측정"] if c.startswith(w)), "눈")
        l["confidence_note"] = c; l["confidence"] = first
    json.dump(o, open(os.path.join(OUT, "lines", n), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ALL = [(v, l) for v, d in LINES.items() for l in d["lines"]]
BODY = [(v, l) for v, l in ALL if l["layer"] != "제목"]
def ev(pred, k=2):
    return [f"{v} {l['t0']}~{l['t1']} '{l['text']}'" for v, l in BODY if pred(l)][:k]

# ---------------- 판설정.json — 판.json + 빠진 _from
P = J(os.path.join(CH, "07_pan", "판.json"))
P["frozen_at"] = TODAY
P["history"] = [{"v": f"v{h['v']}", "date": h.get("date", TODAY), "why": h.get("why", "")} for h in P.get("history", [])]
P["version_from"] = "판 고친 번호 — history 마지막(v1 판 → 회원 눈 판정 4번 반영 v5)"
P["bench"] = {"ko": "클릭노트", "channel": "https://www.youtube.com/@click_note", "analysis": "스타일분석.md", "line_reads": "lines/",
              "palette": "팔레트.json", "rules": "규칙.json", "follow": BENCH, "follow_why": "편 갈래 A(흰 띠 검은 자막 + 노래방 파랑) — 조회 많은 4편"}
F = {
 "frame.top_band": {"y0": "위 띠 위 끝 = 화면 맨 위(A 4편)", "y1": "흰 띠 위 끝 y403(뜯기 caption_box)"},
 "frame.logo": {"y_ink": "벤치 로고 글 잉크 위 끝 y94(A 4편 logo_y 94~196)"},
 "frame.ad_mark": {"box": "벤치 [광고] 잉크 상자 Uu 5초 픽셀"},
 "frame.top_title": {"max_w": "민트 제목 최대 잉크 폭 약 940(A 4편) + 여유"},
 "frame.top_title.one": {"center_y": "1줄 잉크 y267~349 가운데"},
 "frame.top_title.two": {"center_y": "2줄 잉크 y239~300 · 309~371 가운데"},
 "frame.caption_box": {"y0": "흰 띠 위 끝(뜯기 caption_box 403)", "y1": "흰 띠 아래 끝 = 영상 창 위 끝 586"},
 "frame.intro": {"band_y1": "표지 위 띠 아래 끝 y162(Uu·BG8·3kb 1초)", "panel_y1": "회색 판 아래 끝 y492"},
 "frame.intro.box": {"y0": "흰 상자 y497(1초 프레임)", "y1": "흰 상자 y628", "glow": "상자 바깥 흐림 ~652 − 628 ≈ 22(눈)"},
 "frame.intro.line1": {"outline": "흰 글 검은 테 6px(크롭 눈)", "center_y": "흰 글 잉크 y230~320 가운데", "max_w": "표지 글 최대 폭 약 980 + 여유"},
 "frame.intro.line2": {"outline": "파랑 글 검은 테 6px(크롭 눈)", "center_y": "파랑 글 잉크 y364~477 가운데", "max_w": "line1 과 같음"},
 "frame.intro.box_text": {"max_w": "상자 안 폭 1064 − 여백"},
 "caption.layers[0]": {"x": "가운데 정렬(줄판독 x 540)", "max_w": "흰 띠 자막 최대 잉크 폭 약 960(줄판독 max_w) + 여유"},
 "caption.layers[1].shadow": {"blur": "큰글 검은 그림자 흐림 12~14(BG8 18.9초 눈)", "alpha": "그림자 짙기 0.6~0.7(눈)", "spread": "그림자 번짐 3px(눈 — 글 둘레 어두운 테)"},
 "caption.layers[1]": {"line_gap": "큰글 2줄 사이 잉크 틈 약 24px(BG8 18.9초)"},
 "cuts.transition": {"ms": "전환 효과 0 → 길이 0"},
 "rhythm.big_lines": {"min": "큰글 줄 편당 0~2(6/8편 ≥1) — 1차 판은 1줄 이상", "max": "편당 최대 2(줄판독 8편)"},
 "sfx": {"peak_dbfs": "효과음 꼭짓점 — 나레 −14 LUFS 밑에 깔리게(회원 '너무 과하지 않게' · v2 렌더 실측 TP −2.0)", "per_sec_max": "효과음 3초에 1발 꼴 이하(회원 '과하지 않게') — v4 편 8발/28.4초 = 0.28", "min_gap": "효과음 사이 0.8초 이상(겹쳐 들리지 않게 — v3 렌더 0.79초에서 멈춤)"},
 "sfx.intro[0]": {"at": "0초 표지와 같이(회원 '처음 화면에서 효과음')"},
 "sfx.intro[1]": {"off": "표지→본문 컷 0.12초 앞(휙이 컷에 닿게)"},
 "intro_fx": {"start_zoom": "0초 1.15배에서 당겨 들어옴(회원 '처음 화면 화면변화')", "start_zoom_sec": "0.4초(프레임 눈 — 표지 글이 읽히기 전 끝남)",
              "start_flash_sec": "흰 번쩍임 0.18초", "cut_zoom": "표지→본문 1.06배 짧은 당김", "cut_zoom_sec": "0.22초"},
 "big_fx": {"shake": "흔들림 0.5초 · 22px에서 줄어듦(회원 '화면이 흔들리거나')", "zoom_punch": "1.14배에서 0.3초 당김", "flash": "흰 번쩍 0.15초 · 짙기 0.8"},
 "word_fx": {"draw": "숏클 낱말 강조 팩 그리는 초(caption-motions.js WORDFX draw — 밑줄 0.22 · 형광펜 0.28 · 동그라미 0.35 · 글로우 0)"},
}
def put_from(o, path):
    for k, v in list(o.items()):
        if k.startswith("_") or k.endswith("_from"): continue
        p = f"{path}.{k}" if path else k
        if isinstance(v, (int, float)) and not isinstance(v, bool) or (isinstance(v, (list, dict)) and v and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in (v.values() if isinstance(v, dict) else v))):
            if not o.get(k + "_from"):
                txt = F.get(path, {}).get(k)
                if txt is None and k == "version": continue
                o[k + "_from"] = txt or f"안 잼 — 다음: {p} 를 벤치 프레임에서 다시 잰다(지금 값은 판 v1 값)"
        elif isinstance(v, dict): put_from(v, p)
        elif isinstance(v, list):
            for i, x in enumerate(v):
                if isinstance(x, dict): put_from(x, f"{p}[{i}]")
put_from(P, "")
W("판설정.json", P)

# ---------------- 규칙.json — 요소 15종
RF = J(os.path.join(CH, "06_rules", "규칙빈도.json")); nums = RF["nums"]
nb = len(BODY)
def R(element, cond, action, unit, k, n, evidence, conf, cell, sup, task=None, base=None):
    g = "표본부족" if not n or n < 5 else ("강" if k / n >= 0.6 else "중" if k / n >= 0.3 else "약")
    return {"element": element, "cond": cond, "action": action, "unit": unit, "k": k, "n": n, "rate": round(k / n, 3) if n else None, "base": base,
            "grade": g, "evidence": evidence, "confidence": conf, "engine_cell": cell, "engine_support": sup, "measure_task": task}
k_band = sum(1 for _, l in BODY if l["layer"] == "해설"); k_big = sum(1 for _, l in BODY if l["layer"] == "큰글")
k_emph = sum(1 for _, l in BODY if l["emph"]); k_cut = sum(1 for _, l in BODY if str(l["enter"]).startswith("cut"))
k_exit = sum(1 for _, l in BODY if str(l["exit"]).startswith("cut")); k_st = sum(1 for _, l in BODY if not l["sticker"])
k_tr = sum(1 for _, l in BODY if l["transition"] in ("cut", "none")); k_fit = sum(1 for _, l in BODY if (l.get("fit") or 0) >= 5)
k_ring = sum(1 for _, l in BODY if not l.get("ring"))
rules = [
 R("cap_look", "층=해설(흰 띠 y403~586)", "GmarketSansBold 79px · #111111 · 테·그림자 없음 · 가운데 · 한 줄", "줄", k_band, nb, ev(lambda l: l["layer"] == "해설"), "픽셀", "판설정.json caption.layers[0]", "○"),
 R("cap_look", "층=큰글(흰 띠 숨김 · 창 가운데 2줄)", "GmarketSansBold 122px 흰 글 + 파랑 낱말 + 검은 그림자", "줄", k_big, nb, ev(lambda l: l["layer"] == "큰글"), "픽셀", "판설정.json caption.layers[1]", "○"),
 R("cap_enter", "모든 본 자막 줄", "cut(첫 프레임부터 완성) · 0ms", "줄", k_cut, nb, ev(lambda l: True), "픽셀", "판설정.json caption.layers[].enter", "○"),
 R("cap_emph", "나레 줄", "읽는 낱말 파랑 #0811F4(노래방) + 숏클 낱말 강조 팩 1개(밑줄·형광펜·동그라미·글로우 편마다 랜덤 — 회원지시 2026-11-08)", "줄", k_emph, nb, ev(lambda l: bool(l["emph"])), "픽셀", "판설정.json caption.layers[0].karaoke · word_fx · 대본 vary.word_fx", "○"),
 R("cap_exit", "모든 본 자막 줄", "cut — 다음 줄로 바로", "줄", k_exit, nb, ev(lambda l: True), "픽셀", "판설정.json caption.layers[].exit", "○"),
 R("transition", "컷 경계", "하드컷만(전환 효과 0)", "줄", k_tr, nb, ev(lambda l: l["transition"] == "cut"), "픽셀", "판설정.json cuts.transition", "○"),
 R("cut_rhythm", "편", f"컷 중앙 1.0~1.43초(편 중앙 {nums['편 컷 중앙']['med']}) · 갈래 A 1.18", "편", 8, 8, [f"{v} 컷 중앙(03_tear 뜯기 cuts)" for v in BENCH[:2]], "픽셀", "판설정.json cuts.target_median · rhythm.cut_median", "○"),
 R("scene_fit", "본 자막 줄", "말하는 대상이 화면에 보인다(fit ≥ 5)", "줄", k_fit, nb, ev(lambda l: (l.get("fit") or 0) >= 7), "눈", "(없음 — 재료.json 줄마다 장면 고름 · 제작순서 4)", "△"),
 R("bgm", "편", "배경음 없음(1차) — 벤치 말 없는 구간 바닥 −120~−32.5dB 로 갈림", "편", 0, 0, [], "미측정", "판설정.json bgm", "○", "음원 분리 도구를 깔고 8편 나레 밖 구간을 분리해 음악 유무를 다시 잰다"),
 R("sfx", "편 — 회원지시(2026-11-08)", "0초 opener + 표지→본문 whoosh + 움직임 줄 4~6발 + 큰글 장면 이목 효과음 1발 · 팩 21개 중 편마다 랜덤 · 0.35발/초 이하", "편", 0, 0, [], "미측정", "판설정.json sfx · 대본 lines[].sfx · vary.sfx_pack", "○", "agy·음원 분리로 벤치 8편 효과음 발 수·종류를 잰다(지금 규칙은 회원 말)"),
 R("meme", "편", "벤치 반응 짤(남의 얼굴) 4/8편 → 우리는 안 씀(출처 규칙) — 그 자리는 큰글 장면", "편", 4, 8, ["Uu_SJaiAuwQ 19.0~19.8 반응 짤 + 큰글 '진짜 반전은'"], "눈", "(없음 — 출처 규칙으로 안 씀)", "×"),
 R("sticker", "본 자막 줄", "스티커 없음", "줄", k_st, nb, ev(lambda l: not l["sticker"]), "눈", "(없음 — 쓰지 않음)", "○"),
 R("pointer", "본 자막 줄", "화살표·동그라미 표시 없음(낱말 강조 팩 동그라미는 자막 안 꾸밈 — cap_emph)", "줄", k_ring, nb, ev(lambda l: not l.get("ring")), "눈", "(없음 — 쓰지 않음)", "○"),
 R("thumb", "편 0초", "표지 카드(회색 막 + 흰/파랑 큰 2줄 + 흰 상자 작은 제목) · 나레가 읽음 · 2.5~4.2초", "편", 8, 8, [f"{v} 0.0~{LINES[v]['lines'][0]['t1']} 표지" for v in BENCH[:2]], "픽셀", "판설정.json frame.intro", "○"),
 R("speech", "나레", f"남성 나레 1명 f0 {nums['나레 f0']['med']}Hz · {nums['자막 자/초(편마다)']['min']}~{nums['자막 자/초(편마다)']['max']}자/초 · 줄 사이 빈틈 0초 → 우리 = 일레븐랩스 성욱 v3(회원지시) · 배속 상한 1.27", "편", 8, 8, [f"{v} 받아쓰기(02_source/{v}.mp4.asr.json)" for v in BENCH[:2]], "신호", "판설정.json voice · cps_target · tempo_max · pause_*", "○"),
 R("script", "편", "'이건 ( ) 바로' + 제품 일반 이름 공개(끼움말 편마다 랜덤 — 바이럴 근거 있는 것만)", "편", 8, 8, ev(lambda l: l["text"].startswith("이건"), 3), "눈", "판설정.json vary.insert_pool · script.brief", "○"),
 R("script", "편", "'게다가/심지어/진짜 ~ 포인트는' 둘째 장점 이음 줄", "편", 8, 8, ev(lambda l: l["text"].startswith(("게다가", "심지어", "진짜"))), "눈", "판설정.json script.brief", "○"),
 R("script", "줄 끝", "자막 끝 '~요'·'~죠' 금지 — '~다고'·'~다는데'·'~라는데'·'~거'(회원지시 2026-11-08) · 벤치 끝 줄 전언 꼴 7/8", "편", 7, 8, ev(lambda l: l["role"] == "끝"), "눈", "판설정.json script.audit[0]", "○"),
 R("script", "끝 줄", "이걸 살 수밖에 없는 이유를 위트 있게 한 줄(지어낸 숫자·금액·효능 없이 — 회원지시)", "편", 0, 0, [], "미측정", "판설정.json script.brief", "○", "다음 편부터 끝 줄 꼴을 편마다 모아 벤치 끝 줄 8편과 견준다"),
]
W("규칙.json", {"slug": os.path.basename(OUT), "n_videos": len(LINES), "n_lines": nb, "grade_rule": "n ≥ 5 이고 rate ≥ 0.6 = 강 / ≥ 0.3 = 중 / 그 밑 = 약 / n < 5 = 표본부족", "rules": rules})

# ---------------- 스타일분석 · 팔레트 · 재현일치도
sa = open(os.path.join(CH, "06_rules", "스타일분석.md"), encoding="utf-8").read()
sa += "\n\n---\n회원 눈 판정으로 바뀐 것(2026-11-08 — 회원 말이 벤치 '똑같이'보다 앞선다): 목소리 성욱 v3 · 자막 끝 ~요·~죠 금지(~다고·~다는데·~거) · 로고 '클릭노트' · 0초 효과음+화면 효과 · 움직임 효과음(팩 랜덤) · '이건 ( ) 바로' 끼움말 랜덤 · 큰글 장면 효과 랜덤 · 숏클 낱말 강조 팩 랜덤 · 끝 줄 위트 · 소재 = 바이럴 + 쿠팡 제품.\n"
W("스타일분석.md", sa)
shutil.copy(os.path.join(CH, "06_rules", "팔레트.json"), os.path.join(OUT, "팔레트.json"))
mt = open(os.path.join(CH, "09_verify", "재현일치도.md"), encoding="utf-8").read()
W("재현일치도.md", mt)

# ---------------- 기본값.json
V = P["voice"]
W("기본값.json", {
 "voice": {"see": "판설정.json voice", "name": V["name"], "voice_id": V["voice_id"], "model": V["model"]},
 "speed": {"tempo_max": P["tempo_max"], "tempo_max_from": P.get("tempo_max_from", "지침서 §1-2 배속 상한"),
           "cps_target": P["cps_target"], "cps_target_from": "판설정.json cps_target_from 과 같음"},
 "bgm": {"id": None, "none": True, "why": "판설정.json bgm.why"},
 "caption": {"mode": "한 줄 컷 교체(쌓지 않음) + 노래방 파랑 + 숏클 낱말 강조 팩 편마다 랜덤", "see": "판설정.json caption · word_fx"},
})

# ---------------- 출처.md
es = open(os.path.join(EP, "출처.md"), encoding="utf-8").read()
src = "# 출처 — 클릭노트판\n\n벤치는 분석에만 쓰고 화면은 쓰지 않았다. 시험편 재료는 올린 사람 본인 촬영 영상만.\n\n" + es.split("\n", 1)[1]
W("출처.md", src)

# ---------------- 제작순서.md · 금지.md · 실패기록.md
W("제작순서.md", """# 제작순서 — 클릭노트판(다음 편)

## 1. 소재 고르기
- 할 일: 국내·해외에서 바이럴된 제품 중 쿠팡에서 파는 것을 고른다(회원지시). 조회수를 yt-dlp 로 재서 '바이럴 근거'에, 쿠팡 검색어·날짜·결과를 출처.md 에 적는다.
- 확인: 쿠팡 검색 결과 있음 · 바이럴 근거 조회수 있음 · 의약품·의료기기 아님 · 금지 낱말(상품명·브랜드·회사명) 목록 적음
## 2. 재료 받기
- 할 일: 그 제품을 올린 사람 본인이 찍은 사용 영상 2~3개(세로 우선, 720p 이상)를 08_make/ep<NN>_<영문>_<MMDD_HHMM>/src/ 에 받는다.
- 확인: 본인 촬영인가 · 연예인·남의 얼굴 없음 · 박힌 글·상표 구간 메모
## 3. 대본 쓰기
- 할 일: 대본.json — 표지 2줄 → 불편 2~3줄 → '이건 () 바로' → 제품 일반 이름 → 쓰는 법(쭉·착·쓱) → '게다가' → '진짜 미친 포인트는'(큰글) → 고조 → 위트 끝 줄. 조각 4~13자. viral_tags 를 근거대로 단다.
- 확인: 자막 끝 ~요·~죠 0 · 금지 낱말 0 · 성분·효능·금액·안전성 지어냄 0
## 4. 장면 맞추기
- 할 일: 재료.json — 줄마다 말하는 대상이 보이는 구간, 컷 1.0~1.4초, 같은 원본 이웃 컷은 다른 구도.
- 확인: 같은 원본 ±3초 겹침 0 · 박힌 글·상표 창 밖 · 앞 장면이 뒤 장면을 미리 보여 주지 않음
## 5. 랜덤 고르기
- 할 일: python _tools/vary_cn.py <판설정.json> <편> — 효과음 팩 · 끼움말 · 큰글 장면 효과·효과음 · 낱말 강조 팩.
- 만들어지는 파일: 대본.json 'vary'
- 확인: 끼움말이 바이럴 근거와 맞나
## 6. 목소리
- 할 일: python _tools/tts.py <편> --voice <판설정.json voice.voice_id> --model eleven_v3 --stability 0.5 --similarity 0.78 --style 0.3 (유료 1회 — 같은 글이면 다시 쓰기)
- 만들어지는 파일: tts.mp3 · tts_align.json
- 확인: 키 값을 찍지 않음
## 7. 렌더
- 할 일: python _tools/render_cn.py presets/click_note/판설정.json <편>
- 만들어지는 파일: final.mp4 · 자막표.json · timeline.json · run_log.json
- 확인: 길이 23.7~31.7초 · −14 LUFS · 배속 1.27 이하 · 효과음 간격 0.8초 이상
## 8. 검증
- 할 일: tear_cn.py → match_cn.py → watch_pack.py, 1초 시트를 처음부터 끝까지 본다.
- 만들어지는 파일: 09_verify/재현일치도.md · compare_sheet.png
- 확인: 기준 18칸 · 말과 화면 같은 대상 · 남의 글자·얼굴
""")
W("금지.md", """# 금지 — 클릭노트판

- 벤치 영상 화면·소리를 쓰지 않는다(분석만). 벤치 워터마크 '@클릭 노트'·징글을 넣지 않는다. 로고 '클릭노트'는 회원 채널이라고 회원이 확인한 것만 쓴다(2026-11-08).
- 상품명·브랜드·회사·제조사 이름을 대본·자막·제목·화면 글자·업로드글에 넣지 않는다(회원지시 규칙 2) — 화면에 비치는 상표도 창 밖으로 잘라 낸다.
- 쿠팡에서 검색되지 않는 제품, 바이럴 근거(조회수)가 없는 제품은 소재로 쓰지 않는다(회원지시 규칙 1).
- 자막 끝 '~요'·'~죠' 를 쓰지 않는다 — '~다고'·'~다는데'·'~라는데'·'~거'(회원지시 2026-11-08).
- 성분·효능·과학 근거·안전성·금액을 지어내지 않는다. '해외에서 대박 난' 같은 끼움말은 근거 조회수가 있을 때만.
- 연예인·남의 얼굴 반응 짤을 쓰지 않는다(출처 규칙) — 그 자리는 큰글 장면.
- 제품 판매 연결 편은 [광고] 표시를 빼지 않는다.
- 목소리 높이(피치)를 바꾸지 않는다 — 빠르기는 배속 1.27 까지만.
""")
fails = [
 ("배속 상한 넘음", "1차 렌더 배속 1.31·1.37 > 1.27", "목소리(요한 쿠·크리스 v3)가 벤치보다 느림", "목소리 후보 5명 같은 글로 재고 v2 speed 1.2 · 렌더 tempo_cap", "판설정 tempo_max · run_log not_done 에 남김"),
 ("목소리 높이 다름", "요한 쿠 f0 228Hz vs 벤치 145Hz", "후보를 재지 않고 골랐음", "f0 실측으로 크리스 → 회원 지시로 성욱(145.5Hz)", "voice.candidates 에 f0 · 자/초 적어 둠"),
 ("영상이 짧음", "22.0·23.4초 < 벤치 최소 23.7", "줄 수가 적었음", "L5b·L10b·L17b 줄 더함", "길이 검사 not_done"),
 ("컷 중앙 김", "컷 중앙 2.6·1.7초(벤치 1.18)", "같은 원본 이웃 컷이 한 컷으로 재짐", "원본을 번갈아 쓰고 Tnaz 재료 더함", "제작순서 4 '같은 원본 이웃 컷은 다른 구도'"),
 ("상표 보임", "마가린 통 상표·'Contain 12 Pcs' 화면 글", "구간 고를 때 못 봄", "구간 옮김·cx 로 잘라 냄", "제작순서 4 확인 칸"),
 ("음량 모자람", "LUFS −15.5", "1회 맞추기로 모자람", "2차 음량 맞추기", "render_cn 2차 맞추기"),
 ("v3 쉼이 안 잘림", "성욱 v3 말속도 −12%", "쉼이 글자 시각 안에 숨어 글자 사이 틈으로 안 잡힘", "pause_scan_all — 소리로 조용한 덩어리를 직접 찾아 줄임", "판설정 pause_scan_all true"),
 ("긴 컷이 재짐", "컷 p90 2.18~2.64초", "색이 비슷한 같은 원본 컷 4곳을 측정 함수가 못 잡음 · 당겨 잡기도 못 잡음", "L13·L16 재료를 다른 구도로 바꿈", "제작순서 4"),
 ("로고 줄 어긋남", "글자 띠 3개(벤치 2)", "로고 72px 잉크 50px — [광고]와 떨어짐", "90px 로 잉크 높이 67px 맞춤", "판설정 frame.logo.px_from"),
 ("수박 미리 보임", "'이건 그 유명한 바로' 장면에 뒤 수박 장면", "원본 앞쪽이 모음 영상(미리보기)", "16.2초 뚜껑 든 장면으로", "제작순서 4 '앞 장면이 뒤 장면을 미리 보여 주지 않음'"),
 ("말투 규칙 바뀜", "회원이 전언 금지 → ~요·~죠 금지로 두 번 바꿈", "벤치 끝맺음(전언)과 회원 처음 규칙이 달랐음", "검사 정규식 (요$|죠$|…) 로 바꿈", "회원지시.md · 판설정 script.audit"),
]
txt = "# 실패기록 — 클릭노트판(깎기 내역)\n"
for i, (t, a, b, c, d) in enumerate(fails, 1):
    txt += f"\n## {i}. {t}\n- 무엇이: {a}\n- 왜: {b}\n- 어떻게 고쳤나: {c}\n- 다시 안 나게: {d}\n"
W("실패기록.md", txt)

# ---------------- sample/
S = os.path.join(OUT, "sample")
shutil.copy(os.path.join(EP, "final.mp4"), os.path.join(S, "final.mp4"))
shutil.copy(os.path.join(CH, "09_verify", "compare_sheet.png"), os.path.join(S, "compare_sheet.png"))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.5", "-i", os.path.join(S, "final.mp4"), "-frames:v", "1", "-q:v", "3", os.path.join(S, "thumb.jpg")], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(S, "final.mp4"), "-vf", "fps=1,scale=216:384,tile=8x4", "-frames:v", "1", "-q:v", "4", os.path.join(S, "sheet_1s.jpg")], check=True)

# ---------------- 카드.json
mtab = {}
for line in mt.split("\n## 2.")[0].splitlines():
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    if line.startswith("|") and len(c) >= 7 and c[6] == "기준": mtab[c[0]] = c[5]
ok = sum(1 for v in mtab.values() if v in ("○", "해당 없음")); bad = sum(1 for v in mtab.values() if v == "×"); un = sum(1 for v in mtab.values() if v == "안 잼")
px = [l for l in mt.split("\n## 2.")[1].splitlines() if l.startswith("| ") and not l.startswith("| 묶음")] if "\n## 2." in mt else []
pin = sum(1 for l in px if l.rstrip().endswith(("| 안 |", "| 설계상 다름 |")))
card = {
 "slug": os.path.basename(OUT), "channel": "클릭노트", "channel_url": "https://www.youtube.com/@click_note", "brand": "클릭노트",
 "brand_note": "회원 채널(2026-11-08 회원 확인) — 벤치와 같은 이름",
 "format": "나레형", "format_note": "제품 시연 클립 재편집 + 남성 나레 + 위 띠 제목 + 흰 띠 노래방 자막 + 0초 표지 카드",
 "sound_style": "나레 + 효과음(배경음 없음)", "voice": "일레븐랩스 성욱(eleven_v3)", "bgm": "없음",
 "caption_look": "흰 띠 GmarketSansBold 79px 검은 글 · 읽는 낱말 파랑 #0811F4 + 숏클 낱말 강조 팩 랜덤 · 큰글 122px",
 "copied_n": 1, "line_reads_n": len(LINES), "sample_short": False, "sample_short_why": None,
 "axes": {
  "1자막": {"value": "흰 띠 y403~586 GmarketSansBold 79px #111111 한 줄 컷 교체 · 노래방 파랑 #0811F4 · 큰글 2줄 3.5%", "confidence": "픽셀"},
  "2제목틀": {"value": "위 짙은 초록 #072723 띠 0~403 · 로고 · [광고] · 민트 제목 #44DFB7 · 창 y586~1920", "confidence": "픽셀"},
  "3전환": {"value": f"하드컷만 {k_tr}/{nb}", "confidence": "픽셀"},
  "4장면대사": {"value": f"말하는 대상이 화면에 보임(fit≥5) {k_fit}/{nb}", "confidence": "눈"},
  "5스토리": {"value": "표지 → 불편 → '이건 바로' 공개(22~40%) → 쓰는 법 → '게다가' → '진짜 ~ 포인트는' → 고조 → 끝", "confidence": "눈"},
  "6대본언어": {"value": "반말 서술 · 조각 중앙 8자(최대 13) · 끝 전언 7/8 → 우리 ~다고·~다는데(~요·~죠 금지)", "confidence": "픽셀"},
  "7소리": {"value": "남성 나레 f0 145.5Hz · 7.58자/초 · 빈틈 0 · 배경음 갈림 · 효과음 미측정", "confidence": "신호"},
  "8스티커짤": {"value": "스티커 0 · 반응 짤 4/8편(우리는 안 씀)", "confidence": "눈"},
  "9썸네일": {"value": "0초 표지 카드 8/8 · 나레가 읽음 2.5~4.2초", "confidence": "픽셀"},
  "10소재": {"value": "생활 발명품·주방·문구 해외 시연 영상 재편집", "confidence": "눈"},
  "11채널": {"value": "회원 지정 8편(01_select/메타표.md)", "confidence": "픽셀"}},
 "rules_file": "규칙.json", "rules_n": len(rules), "rules_unmeasured": sum(1 for r in rules if r["confidence"] == "미측정"),
 "match": {"file": "재현일치도.md", "rows": len(mtab), "ok": ok, "bad": bad, "unmeasured": un, "verdict": "통과" if not bad and not un else "미달", "pixel_in": pin, "pixel_total": len(px)},
 "eye": {"member_pass": True, "note": "회원 눈 판정 5번(목소리·효과음·말투·로고·끼움말·큰글 효과·낱말 강조 팩) 뒤 '통과'(2026-11-08)"},
 "done": {"level": 3, "level_name": "1차 통과", "missing": ["벤치 효과음·배경음 측정(분리 도구 없음)", "제목·표지 글꼴 대체(BMDOHYEON — 미일치)"], "next": "제작순서.md 대로 다음 편 — 바이럴 + 쿠팡 소재"},
 "saved_at": TODAY,
}
W("카드.json", card)
print("저장", OUT, "규칙", len(rules), "줄판독", len(LINES), "match", card["match"])
