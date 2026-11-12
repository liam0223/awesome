# -*- coding: utf-8 -*-
"""프리셋 저장 검사 — 프리셋 저장 규격서대로 저장됐나 본다(표준 라이브러리만).

    python check_preset.py presets/<슬러그>            # 표 출력, 오류가 하나라도 있으면 종료 코드 1
    python check_preset.py presets/<슬러그> --stage 1  # 완료 단계가 1 밑이어도 종료 코드 1
    python check_preset.py --work copywork             # 작업 폴더 나무·이름 꼴(규격서 1절 표)만 본다

오류(✗) = 규격 위반 → 고친 뒤 다시 돌린다. 경고(△) = 규격 위반은 아니지만 봐야 할 것.
완료 단계(0~3)는 파일 내용으로 계산하고, 카드.json done.level 과 다르면 오류."""
import json
import re
import sys
from pathlib import Path

FILES_JSON = ["카드.json", "판설정.json", "규칙.json", "팔레트.json", "기본값.json"]
FILES_MD = ["스타일분석.md", "재현일치도.md", "출처.md", "제작순서.md", "금지.md", "실패기록.md"]
SAMPLE = ["final.mp4", "sheet_1s.jpg", "thumb.jpg", "compare_sheet.png"]
ELEMENTS = ["cap_look", "cap_enter", "cap_emph", "cap_exit", "transition", "cut_rhythm", "scene_fit", "bgm", "sfx",
            "meme", "sticker", "pointer", "thumb", "speech", "script"]
CONF = ["픽셀", "눈", "신호", "미측정"]
GRADES = ["강", "중", "약", "표본부족"]
AXES = ["1자막", "2제목틀", "3전환", "4장면대사", "5스토리", "6대본언어", "7소리", "8스티커짤", "9썸네일", "10소재", "11채널"]
AXIS_HEADS = ["## 1 자막", "## 2 제목·틀", "## 3 장면 전환", "## 4 장면↔대사", "## 5 스토리", "## 6 대본 언어", "## 7 소리",
              "## 8 스티커·짤", "## 9 썸네일·첫 화면", "## 10 소재", "## 11 채널"]
CARD_KEYS = ["slug", "channel", "brand", "format", "sound_style", "voice", "bgm", "caption_look", "copied_n", "line_reads_n",
             "sample_short", "axes", "rules_file", "match", "eye", "done", "saved_at"]
PAN_KEYS = ["name", "renderer", "bench", "voice", "bgm", "loudness", "length", "timing", "frame", "caption", "cuts",
            "placement", "rhythm", "script"]
RULE_KEYS = ["element", "cond", "action", "unit", "k", "n", "rate", "grade", "evidence", "confidence", "engine_cell",
             "engine_support", "measure_task"]
LINE_DOC = ["id", "dur", "title_lines", "source_label", "lines", "beats", "narr_share", "notes", "frame0"]
LINE_KEYS = ["t0", "t1", "speaker", "text", "layer", "enter", "emph", "sticker", "sfx", "scene", "cut_at",
             "role", "y", "fill_hex", "fit", "transition", "motion", "confidence"]
ROLES = ["훅", "다리", "고조", "공개", "증거", "반전", "질문", "답", "이음", "본문", "끝"]
SPEAKER = re.compile(r"^(나레|원음|해설|제3자|불명)")
MATCH_ROWS = ["len.duration", "cut.median", "speech.cps.나레", "chunk.chars", "chunk.sec", "enter.mode.나레", "enter.mode.원음",
              "fx.rate.나레", "fx.rate.원음", "fx.pos", "plain.rate", "transition.rate", "sfx.rate", "sticker.rate",
              "meme.rate", "thumb.frame0", "mix.lufs", "framecmp"]
VERDICT = ["○", "×", "안 잼", "해당 없음"]
ABS_PATH = re.compile(r"(?<![\w/])([A-Za-z]:[\\/]|/Users/|/home/|\\\\)")
NEXT = re.compile(r"안 잼[^\n]{0,80}?다음:\s*\S.{4,}")


class Report:
    def __init__(self):
        self.rows = []   # (구역, 결과, 글)

    def ok(self, sec, msg):
        self.rows.append((sec, "○", msg))

    def err(self, sec, msg):
        self.rows.append((sec, "✗", msg))

    def warn(self, sec, msg):
        self.rows.append((sec, "△", msg))

    @property
    def errors(self):
        return [r for r in self.rows if r[1] == "✗"]


def load_json(p: Path, rep: Report, sec: str):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except Exception as e:            # 깨진 json 은 숨기지 않는다
        rep.err(sec, f"{p.name} json 이 깨짐: {e}")
        return None


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def is_num_table(v):
    """숫자만 든 목록·사전(예 [0,521,1080,1399] · {cut:1.0}) = 값 하나로 본다."""
    if isinstance(v, list) and v:
        return all(is_num(x) or (isinstance(x, list) and x and all(is_num(y) for y in x)) for x in v)
    if isinstance(v, dict) and v:
        return all(is_num(x) for x in v.values())
    return False


def missing_from(o, path=""):
    """숫자 칸 K 마다 옆에 K_from 이 있어야 한다. made_by+source 가 있는 묶음(도구 집계)은 건너뛴다."""
    out = []
    if isinstance(o, dict):
        if "made_by" in o and "source" in o:
            return out
        for k, v in o.items():
            if k.startswith("_") or k.endswith("_from"):
                continue
            p = f"{path}.{k}" if path else k
            if is_num(v) or is_num_table(v):
                f = o.get(f"{k}_from")
                if not (isinstance(f, str) and f.strip()):
                    out.append(p)
            else:
                out += missing_from(v, p)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out += missing_from(v, f"{path}[{i}]")
    return out


def strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


def grade_of(k, n):
    if not n or n < 5:
        return "표본부족"
    r = k / n
    return "강" if r >= 0.6 else "중" if r >= 0.3 else "약"


def md_table(text, first_col_names):
    rows = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] in first_col_names:
            rows[cells[0]] = cells
    return rows


def check(root: Path, need_stage: int | None):
    rep = Report()
    if not root.is_dir():
        rep.err("폴더", f"{root} 가 없다")
        return rep, 0
    # 1. 폴더 이름 = 영문 · 슬러그 꼴 · lines 파일 이름 꼴(규격서 1-3·1-4)
    if not SLUG.fullmatch(root.name):
        rep.err("폴더", f"슬러그 '{root.name}' 가 꼴 밖 — 영문 소문자·숫자·밑줄(규격서 1-3)")
    for q in sorted((root / "lines").glob("*")) if (root / "lines").is_dir() else []:
        if not re.fullmatch(r"[A-Za-z0-9_-]{5,20}\.json", q.name):
            rep.err("폴더", f"lines/{q.name} — 이름 꼴은 <영상id>.json")
    extra = [q.name for q in root.iterdir() if q.name not in set(FILES_JSON + FILES_MD) | {"lines", "sample", "assets"}]
    if extra:
        rep.err("폴더", f"규격서 1-2 나무에 없는 자리: {extra[:6]} — 먼저 규격서 표에 한 줄 더하고 만든다")
    for p in [root, *[q for q in root.rglob("*") if q.is_dir()]]:
        if re.search(r"[^\x00-\x7f]", p.name):
            rep.err("폴더", f"폴더 이름에 한글: {p.relative_to(root.parent)} — 폴더는 영문(ffmpeg 가 한글 경로에서 죽는다)")
    # 2. 필수 파일
    for f in FILES_JSON + FILES_MD:
        p = root / f
        if not p.exists():
            rep.err("파일", f"{f} 없음")
        elif p.stat().st_size == 0:
            rep.err("파일", f"{f} 빈 파일")
    for f in SAMPLE:
        p = root / "sample" / f
        if not p.exists() or p.stat().st_size == 0:
            rep.err("파일", f"sample/{f} 없음")
    lines_dir = root / "lines"
    lr = sorted(lines_dir.glob("*.json")) if lines_dir.is_dir() else []
    if not lr:
        rep.err("파일", "lines/<편>.json 없음(줄판독)")
    if not rep.errors:
        rep.ok("파일", f"필수 파일 {len(FILES_JSON) + len(FILES_MD)}개 + sample/ {len(SAMPLE)}개 + lines/ {len(lr)}편")

    J = {f: load_json(root / f, rep, "json") for f in FILES_JSON}
    card, pan, rules, pal, dflt = (J[f] for f in FILES_JSON)

    # 3. 모든 글 — 로컬 절대경로 금지 · '안 잼'엔 '다음:'
    texts = {}
    for p in root.rglob("*"):
        if p.suffix in (".json", ".md") and p.is_file():
            texts[str(p.relative_to(root))] = p.read_text(encoding="utf-8", errors="replace")
    n_abs = n_next = 0
    for name, t in texts.items():
        for i, line in enumerate(t.splitlines(), 1):
            if ABS_PATH.search(line):
                n_abs += 1
                if n_abs <= 5:
                    rep.err("경로", f"{name}:{i} 로컬 절대경로 — 프리셋 폴더 기준 상대경로로")
            for m in re.finditer(r"안 잼", line):
                if re.match(r"\s*\|", line[m.end():m.end() + 3]) and re.search(r"\|\s*$", line[:m.start()]):
                    continue                     # 표의 판정 칸 '| 안 잼 |' 은 기호 — 같은 줄 앞 칸에 다음 잴 방법을 적는다
                if not NEXT.search(line[m.start():]):
                    n_next += 1
                    if n_next <= 5:
                        rep.err("안 잼", f"{name}:{i} '안 잼' 뒤에 '다음: <잴 방법>' 이 없다")
    if n_abs > 5:
        rep.err("경로", f"로컬 절대경로 {n_abs}곳(앞 5곳만 표시)")
    if n_next > 5:
        rep.err("안 잼", f"'다음:' 없는 안 잼 {n_next}곳(앞 5곳만 표시)")
    if not n_abs:
        rep.ok("경로", "로컬 절대경로 0")
    if not n_next:
        rep.ok("안 잼", "모든 '안 잼' 에 다음 잴 방법 있음")

    # 4. 줄판독
    lr_bad = 0
    for p in lr:
        d = load_json(p, rep, "줄판독")
        if d is None:
            lr_bad += 1
            continue
        e0 = len(rep.errors)
        for k in LINE_DOC:
            if k not in d:
                rep.err("줄판독", f"{p.name} 문서 칸 없음: {k}")
        if d.get("_todo"):
            rep.err("줄판독", f"{p.name} _todo 남음")
        for i, l in enumerate(d.get("lines") or []):
            miss = [k for k in LINE_KEYS if k not in l]
            if miss:
                rep.err("줄판독", f"{p.name} 줄{i} 칸 없음: {miss}")
                continue
            if l["transition"] is None or l["motion"] is None or l["confidence"] is None:
                rep.err("줄판독", f"{p.name} 줄{i} transition·motion·confidence 는 null 금지(없으면 'none')")
            if not SPEAKER.match(str(l["speaker"] or "")):
                rep.err("줄판독", f"{p.name} 줄{i} speaker 어휘 밖: {l['speaker']!r}")
            if l["role"] not in ROLES:
                rep.err("줄판독", f"{p.name} 줄{i} role 어휘 밖: {l['role']!r}")
            if l["confidence"] not in CONF:
                rep.err("줄판독", f"{p.name} 줄{i} confidence 어휘 밖: {l['confidence']!r}")
            if not isinstance(l["emph"], list) or not isinstance(l["sticker"], list):
                rep.err("줄판독", f"{p.name} 줄{i} emph·sticker 는 [] (없음도 분모)")
            if is_num(l["t0"]) and is_num(l["t1"]) and l["t1"] <= l["t0"]:
                rep.err("줄판독", f"{p.name} 줄{i} t1 ≤ t0")
            if len(rep.errors) - e0 > 8:
                rep.err("줄판독", f"{p.name} 오류가 많아 나머지 줄은 생략")
                break
        if len(rep.errors) > e0:
            lr_bad += 1
    if lr and not lr_bad:
        rep.ok("줄판독", f"{len(lr)}편 칸 전부 있음")

    # 5. 판설정 — 필수 칸 · 숫자마다 _from
    pan_ok = False
    if pan is not None:
        miss = [k for k in PAN_KEYS if k not in pan]
        if miss:
            rep.err("판설정", f"필수 칸 없음: {miss}")
        nf = missing_from(pan)
        if nf:
            rep.err("판설정", f"_from 없는 숫자 {len(nf)}개: {nf[:6]}{' …' if len(nf) > 6 else ''}")
        else:
            rep.ok("판설정", "숫자 칸 전부 _from 있음")
        pan_ok = not miss and not nf

    # 6. 규칙 — 15종 레코드
    rules_ok = False
    rl = (rules or {}).get("rules") if isinstance(rules, dict) else rules
    if rules is not None:
        if not isinstance(rl, list) or not rl:
            rep.err("규칙", "rules 목록이 없다(요소 15종 레코드 꼴)")
        else:
            e0 = len(rep.errors)
            have = {r.get("element") for r in rl if isinstance(r, dict)}
            lack = [e for e in ELEMENTS if e not in have]
            if lack:
                rep.err("규칙", f"요소 없음: {lack} — 15종마다 한 줄 이상(없으면 '없음'도 규칙)")
            for i, r in enumerate(rl):
                if not isinstance(r, dict):
                    rep.err("규칙", f"{i}번 레코드가 사전이 아니다")
                    continue
                m = [k for k in RULE_KEYS if k not in r]
                if m:
                    rep.err("규칙", f"{i}번({r.get('element')}) 칸 없음: {m}")
                    if len(rep.errors) - e0 >= 8:
                        rep.err("규칙", f"오류가 많아 나머지 {len(rl) - i - 1}줄은 생략 — 15종 레코드 꼴(규격서 3-3)로 다시 쓴다")
                        break
                    continue
                if r["element"] not in ELEMENTS:
                    rep.err("규칙", f"{i}번 element 어휘 밖: {r['element']!r}")
                if r["confidence"] not in CONF:
                    rep.err("규칙", f"{i}번({r['element']}) confidence 어휘 밖: {r['confidence']!r}")
                if r["grade"] not in GRADES:
                    rep.err("규칙", f"{i}번({r['element']}) grade 어휘 밖: {r['grade']!r}")
                elif is_num(r["k"]) and is_num(r["n"]) and grade_of(r["k"], r["n"]) != r["grade"]:
                    rep.err("규칙", f"{i}번({r['element']}) 등급 {r['grade']} ≠ k/n {r['k']}/{r['n']} 로 계산한 {grade_of(r['k'], r['n'])}")
                if r["confidence"] == "미측정" and not (isinstance(r["measure_task"], str) and len(r["measure_task"].strip()) >= 10):
                    rep.err("규칙", f"{i}번({r['element']}) 미측정인데 measure_task(다음 잴 방법)가 없다")
                if r["confidence"] != "미측정" and not r["evidence"]:
                    rep.err("규칙", f"{i}번({r['element']}) evidence(편 id·초) 비어 있음")
            rules_ok = len(rep.errors) == e0
            if rules_ok:
                rep.ok("규칙", f"{len(rl)}개 레코드 · 15종 다 있음 · 등급 = k/n 계산과 같음")

    # 7. 스타일분석 — 11축 머리, 축마다 실측·규칙·신뢰도
    sa_ok = False
    t = texts.get("스타일분석.md")
    if t is not None:
        e0 = len(rep.errors)
        pos = []
        for h in AXIS_HEADS:
            i = t.find(h + "\n")
            if i < 0:
                rep.err("스타일분석", f"머리 없음: '{h}'")
            pos.append(i)
        good = [(h, i) for h, i in zip(AXIS_HEADS, pos) if i >= 0]
        for j, (h, i) in enumerate(good):
            end = good[j + 1][1] if j + 1 < len(good) else len(t)
            body = t[i:end]
            for w in ("실측", "고른 규칙", "신뢰도"):
                if f"- {w}" not in body:
                    rep.err("스타일분석", f"'{h}' 에 '- {w}:' 줄 없음")
        sa_ok = len(rep.errors) == e0
        if sa_ok:
            rep.ok("스타일분석", "11축 머리 · 축마다 실측/고른 규칙/신뢰도")

    # 8. 팔레트
    pal_ok = False
    if pal is not None:
        e0 = len(rep.errors)
        roles_ = pal.get("roles") if isinstance(pal, dict) else None
        if not isinstance(roles_, dict) or "n_docs" not in pal:
            rep.err("팔레트", "n_docs·roles 칸 없음")
        else:
            for role, items in roles_.items():
                for c in items:
                    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", str(c.get("hex", ""))) or not is_num(c.get("n_docs")):
                        rep.err("팔레트", f"{role} 색 칸이 hex·n_docs 꼴이 아님: {c}")
                        break
        pal_ok = len(rep.errors) == e0
        if pal_ok:
            rep.ok("팔레트", f"층 {len(roles_)}개 · hex 꼴")

    # 9. 재현일치도 — 기준 칸 18 · 판정 기호 · 비교 시트
    match_counts = None
    t = texts.get("재현일치도.md")
    if t is not None:
        e0 = len(rep.errors)
        allrows = {}
        sec1 = t.split("\n## 2.")[0]            # 1절(줄 단위 표)만 — 2절 픽셀 표는 framecmp 의 뒷받침
        for line in sec1.splitlines():
            if line.startswith("|") and not line.startswith("|---"):
                c = [x.strip() for x in line.strip().strip("|").split("|")]
                if len(c) >= 7 and c[0] not in ("칸", "묶음") and c[6] in ("기준", "참고"):
                    allrows[c[0]] = c
        lack = [r for r in MATCH_ROWS if r not in allrows]
        if lack:
            rep.err("재현일치도", f"기준 칸 없음: {lack}")
        crit = [c for c in allrows.values() if c[6] == "기준"]
        for c in allrows.values():
            if c[5] not in VERDICT:
                rep.err("재현일치도", f"'{c[0]}' 판정 '{c[5]}' — ○ / × / 안 잼 / 해당 없음 중 하나")
        if "compare_sheet.png" not in t:
            rep.err("재현일치도", "비교 시트(sample/compare_sheet.png) 경로가 없다")
        ok = sum(1 for c in crit if c[5] in ("○", "해당 없음"))
        bad = sum(1 for c in crit if c[5] == "×")
        un = sum(1 for c in crit if c[5] == "안 잼")
        match_counts = {"rows": len(crit), "ok": ok, "bad": bad, "unmeasured": un}
        if len(rep.errors) == e0:
            rep.ok("재현일치도", f"기준 {len(crit)}칸: ○ {ok} · × {bad} · 안 잼 {un}")

    # 10. 기본값
    if dflt is not None:
        miss = [k for k in ("voice", "speed", "bgm", "caption") if k not in dflt]
        nf = missing_from(dflt)
        if miss:
            rep.err("기본값", f"칸 없음: {miss}")
        if nf:
            rep.err("기본값", f"_from 없는 숫자: {nf}")
        if not miss and not nf:
            rep.ok("기본값", "목소리·빠르기·배경음·자막 쌓기 + _from")

    # 11. md 꼴
    t = texts.get("출처.md")
    if t is not None:
        rows = [l for l in t.splitlines() if l.startswith("| ") and "http" in l]
        if not rows:
            rep.err("출처", "주소(http) 있는 표 줄이 없다")
        elif any(len([c for c in l.split("|")]) < 7 for l in rows):
            rep.err("출처", "표 칸이 5개(쓴 곳·주소·계정·본인/공식·확인 방법)가 아닌 줄이 있다")
        elif not any(("예" in l.split("|")[4]) for l in rows):
            rep.err("출처", "원 작가 본인·공식 '예' 인 소재가 하나도 없다")
        else:
            rep.ok("출처", f"{len(rows)}줄")
    t = texts.get("제작순서.md")
    if t is not None:
        steps = re.split(r"\n## \d+\.", "\n" + t)[1:]
        badst = [i + 1 for i, s in enumerate(steps) if "- 확인" not in s or "- 만들어지는 파일" not in s and "- 할 일" not in s]
        if len(steps) < 5:
            rep.err("제작순서", f"단계 {len(steps)}개 — '## N. 이름' 꼴로 5단계 이상")
        elif badst:
            rep.err("제작순서", f"단계 {badst} 에 '- 확인' 또는 '- 만들어지는 파일/할 일' 줄이 없다")
        elif "판설정.json" not in t:
            rep.err("제작순서", "판설정.json 을 쓰는 렌더 단계가 없다")
        else:
            rep.ok("제작순서", f"{len(steps)}단계")
    t = texts.get("실패기록.md")
    if t is not None:
        ents = re.split(r"\n## \d+\.", "\n" + t)[1:]
        badent = [i + 1 for i, s in enumerate(ents) if not all(w in s for w in ("- 무엇이", "- 왜", "- 어떻게 고쳤나", "- 다시 안 나게"))]
        if not ents:
            rep.err("실패기록", "'## N. 제목' 항목이 없다(틀린 것이 없었으면 '## 1. 없음' 과 네 줄)")
        elif badent:
            rep.err("실패기록", f"항목 {badent} 에 무엇이/왜/어떻게 고쳤나/다시 안 나게 중 빠진 줄")
        else:
            rep.ok("실패기록", f"{len(ents)}건")
    t = texts.get("금지.md")
    if t is not None:
        n = len([l for l in t.splitlines() if l.startswith("- ")])
        (rep.ok if n >= 4 else rep.err)("금지", f"금지 줄 {n}개" + ("" if n >= 4 else " — 4개 이상(이름·로고 / 출처 / 사실·금액 / 광고 표시)"))

    # 12. 카드 — 칸 · 표본부족 · 숫자 맞대기 · 완료 단계
    stage = 0
    if card is not None:
        miss = [k for k in CARD_KEYS if k not in card]
        if miss:
            rep.err("카드", f"칸 없음: {miss}")
        ax = card.get("axes") or {}
        la = [a for a in AXES if a not in ax or not isinstance(ax[a], dict) or ax[a].get("confidence") not in CONF or not ax[a].get("value")]
        if la:
            rep.err("카드", f"11축 칸 빠짐/신뢰도 어휘 밖: {la}")
        if card.get("line_reads_n") != len(lr):
            rep.err("카드", f"line_reads_n {card.get('line_reads_n')} ≠ lines/ 편 수 {len(lr)}")
        if len(lr) < 5 and card.get("sample_short") is not True:
            rep.err("카드", f"줄판독 {len(lr)}편 < 5 인데 sample_short 가 true 가 아니다(표본부족 표시)")
        if match_counts and isinstance(card.get("match"), dict):
            cm = card["match"]
            diff = {k: (cm.get(k), v) for k, v in match_counts.items() if cm.get(k) != v}
            if diff:
                rep.err("카드", f"match 숫자가 재현일치도.md 와 다름(카드, 표): {diff}")
        # 완료 단계 계산
        s1 = len(lr) >= 6 and not lr_bad and rules_ok and sa_ok and pal_ok
        s2 = s1 and pan_ok and all(r.get("confidence") != "미측정" or r.get("measure_task") for r in (rl or []))
        s3 = s2 and match_counts is not None and match_counts["bad"] == 0 and match_counts["unmeasured"] == 0 \
            and (card.get("eye") or {}).get("member_pass") is True
        stage = 3 if s3 else 2 if s2 else 1 if s1 else 0
        lv = (card.get("done") or {}).get("level")
        if lv != stage:
            rep.err("카드", f"done.level {lv} ≠ 계산한 완료 단계 {stage}")
        if stage < 3 and not (card.get("done") or {}).get("missing"):
            rep.err("카드", "3단계 밑인데 done.missing(남은 일)이 비어 있다")
        if not [r for r in rep.rows if r[0] == "카드" and r[1] == "✗"]:
            rep.ok("카드", f"칸 · 11축 · 숫자 맞대기 · done.level {lv} = 계산 {stage}")
    if len(lr) < 5:
        rep.warn("표본", f"줄판독 {len(lr)}편 < 5 — 편 단위 규칙은 전부 표본부족")
    names = {0: "0 분석 덜 됨", 1: "1 분석됨", 2: "2 판 있음", 3: "3 1차 통과"}
    rep.rows.append(("완료 단계", "→", names[stage]))
    if need_stage is not None and stage < need_stage:
        rep.err("완료 단계", f"요구 {need_stage} 단계 밑")
    return rep, stage


# ---------------------------------------------------------------- 작업 폴더 나무(--work) — 규격서 1-1·1-4·1-5 표와 같은 꼴
SLUG = re.compile(r"[a-z][a-z0-9_]{1,30}")
WORK_TOP = {"guide.md", "preset_spec.md", "회원지시.md", ".env", "장점기록표.json", "_tools", "_assets", "presets"}
STEP_DIRS = ["01_select", "02_source", "03_tear", "04_frames", "05_lines", "06_rules", "07_pan", "08_make", "09_verify", "10_apply"]
VID = r"[A-Za-z0-9_-]{11}"
SRC_FILE = re.compile(VID + r"\.(mp4|info\.json|ko\.vtt|comments\.json|mp4\.asr\.json)")
EP_DIR = re.compile(r"ep\d{2}_[a-z0-9]+(?:_[a-z0-9]+)*_\d{4}_\d{4}")


def check_work(root: Path) -> Report:
    rep = Report()
    if not root.is_dir():
        rep.err("작업 폴더", f"{root} 가 없다")
        return rep
    for f in ("guide.md", "preset_spec.md", "_tools/check_preset.py"):
        if not (root / f).exists():
            rep.err("시작", f"{f} 없음 — 첫 일로 저장(지침서 §1-1 1)")
    for p in [root, *[q for q in root.rglob("*") if q.is_dir()]]:
        if re.search(r"[^\x00-\x7f]", p.name):
            rep.err("폴더 이름", f"한글 폴더: {p.relative_to(root.parent)} — 폴더는 영문(규격서 1-6)")
    chs = [q for q in root.iterdir() if q.is_dir() and q.name.startswith("ch_")]
    odd = [q.name for q in root.iterdir() if q.name not in WORK_TOP and not q.name.startswith("ch_")]
    if odd:
        rep.err("나무", f"규격서 1-1 나무에 없는 자리: {odd[:6]}")
    if not chs:
        rep.err("나무", "ch_<슬러그>/ 가 없다")
    for ch in chs:
        slug = ch.name[3:]
        if not SLUG.fullmatch(slug):
            rep.err("슬러그", f"{ch.name} — 영문 소문자·숫자·밑줄(규격서 1-3)")
        if not (ch / "00_progress.md").exists():
            rep.err("나무", f"{ch.name}/00_progress.md 없음")
        bad = [q.name for q in ch.iterdir() if q.name not in STEP_DIRS + ["00_progress.md"]]
        if bad:
            rep.err("나무", f"{ch.name}/ 안 규격서 1-1 에 없는 자리: {bad[:6]}")
        src = ch / "02_source"
        if src.is_dir():
            b2 = [q.name for q in src.iterdir() if q.name != "받기검사.md" and not SRC_FILE.fullmatch(q.name)]
            if b2:
                rep.err("이름 꼴", f"{ch.name}/02_source 이름 꼴 밖: {b2[:4]} — <영상id>.mp4 꼴(규격서 1-4)")
        for sub in ("03_tear", "04_frames"):
            d = ch / sub
            if d.is_dir():
                b3 = [q.name for q in d.iterdir() if q.is_dir() and not re.fullmatch(VID, q.name) and not (sub == "04_frames" and q.name == "fontset")]
                if b3:
                    rep.err("이름 꼴", f"{ch.name}/{sub} 폴더 이름 꼴 밖: {b3[:4]} — <영상id>/")
        d = ch / "05_lines"
        if d.is_dir():
            b4 = [q.name for q in d.glob("*.json") if not re.fullmatch(VID + r"\.json", q.name)]
            if b4:
                rep.err("이름 꼴", f"{ch.name}/05_lines 이름 꼴 밖: {b4[:4]}")
        d = ch / "07_pan"
        if d.is_dir() and not (d / "판.json").exists():
            rep.err("나무", f"{ch.name}/07_pan/판.json 없음")
        d = ch / "08_make"
        if d.is_dir():
            b5 = [q.name for q in d.iterdir() if q.is_dir() and not EP_DIR.fullmatch(q.name)]
            if b5:
                rep.err("이름 꼴", f"{ch.name}/08_make 편 폴더 꼴 밖: {b5[:4]} — ep<NN>_<영문>_<MMDD_HHMM>(규격서 1-4)")
        for sub in STEP_DIRS:
            if (ch / sub).is_dir():
                for q in (ch / sub).rglob("*"):
                    if q.is_file() and q.suffix.lower() in (".mp4", ".jpg", ".png", ".wav", ".mp3") and re.search(r"[^\x00-\x7f]", q.name):
                        rep.err("이름 꼴", f"ffmpeg 가 읽는 파일 이름에 한글: {q.relative_to(root)}")
                        break
    pres = root / "presets"
    if pres.is_dir():
        for q in pres.iterdir():
            if not SLUG.fullmatch(q.name):
                rep.err("슬러그", f"presets/{q.name} — 슬러그 꼴 밖")
    if not rep.errors:
        rep.ok("작업 폴더", f"규격서 1-1 나무 · 1-3 슬러그 · 1-4 이름 꼴 맞음(ch_ {len(chs)}개)")
    return rep


def main():
    try:                                   # 콘솔이 cp949 여도 한글·기호가 깨지지 않게(회원 PC 시험에서 깨짐 확인)
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    need = None
    if "--stage" in args:
        i = args.index("--stage")
        need = int(args[i + 1])
        del args[i:i + 2]
    if args[0] == "--work":
        root = Path(args[1])
        rep = check_work(root)
        stage = None
    else:
        root = Path(args[0])
        rep, stage = check(root, need)
    w = max(len(r[0]) for r in rep.rows) + 2
    print(("작업 폴더 검사: " if stage is None else "프리셋 저장 검사: ") + str(root))
    print(f"| {'구역'.ljust(w)} | 결과 | 내용")
    print(f"|{'-' * (w + 2)}|------|------")
    for sec, res, msg in rep.rows:
        print(f"| {sec.ljust(w)} |  {res}   | {msg}")
    ne = len(rep.errors)
    nw = sum(1 for r in rep.rows if r[1] == "△")
    print(f"\n오류 {ne} · 경고 {nw}" + ("" if stage is None else f" · 완료 단계 {stage}"))
    print("판정: " + ("통과" if ne == 0 else "실패 — ✗ 줄을 고친 뒤 다시 돌린다"))
    sys.exit(1 if ne else 0)


if __name__ == "__main__":
    main()
