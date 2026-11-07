## 부록 B. 프리셋 저장 규격 (첫 일로 `copywork/preset_spec.md` 로 저장 — 아래 전문)

## 프리셋 저장 규격 (회원용)

> 채널을 따라 만든 뒤 **판정 통과 → 이 규격대로 저장 → `check_preset.py` 통과** 까지가 저장이다.
> 이 문서가 저장 폴더·파일·칸의 **유일한 정의**다. 회원용 지침서 끝에 부록 B 로 붙어 오고, 클로드가 첫 일로 `copywork/preset_spec.md` 로 저장한다. 지침서 §11 저장 단계와 저장 명령은 이 문서를 가리키기만 한다.
> 예시는 전부 스냅봤니(@스냅봤니) 1차 프리셋의 **실제 산출 값**이다. 못 잰 값은 '안 잼 — 다음: 잴 방법' 으로 남아 있다(지어낸 값 없음). 예시 속 벤치 영상 id 는 읽기 쉽게 자리표(`video_A`~`video_D` 벤치 4편 · `video_E` 출처를 추적한 벤치 편 · `reel_F` 원 작가 릴스)로 바꿔 적었다 — 실제로 저장할 때는 진짜 영상 id 를 쓴다.

---

### 1. 폴더 규칙 — 처음부터 저장까지 (이름·위치 고정 · 이 절이 주인)

<!--FOLDER_START-->
**클로드에게: 새 파일을 만들 때마다 아래 표에 있는 자리·이름으로만 만든다. 표에 없는 자리에 만들어야 하면 먼저 이 표(작업 폴더의 `preset_spec.md` 1절)에 한 줄을 더하고 만든다.** 검사 = `python _tools/check_preset.py --work copywork`(작업 폴더 나무) · `python _tools/check_preset.py presets/<슬러그>`(저장 폴더).

#### 1-1. 폴더 나무 한 장 (copywork 전체)

```
copywork/                              ← 작업 폴더(영문). 한글·공백 경로면 드라이브 바로 아래에
  guide.md                             ← 붙여 넣은 지침서 본문(첫 일로 저장)
  preset_spec.md                       ← 이 규격(지침서 부록 B, 첫 일로 저장)
  회원지시.md                          ← 회원이 중간에 덧붙인 말(날짜 · 원문)
  .env                                 ← 키(받아쓰기·TTS) — 화면·다른 파일에 찍지 않는다
  장점기록표.json                      ← 채널마다 장점메모.md 를 모은 것(업그레이드 단계)
  _tools/                              ← 클로드가 짠 도구(check_preset.py · render.py · match.py …, 다음 채널에서도 다시 씀)
  _assets/                             ← 내 재료 창고: bgm/<id>.mp3 · bgm_list.json · sfx/<영문>.mp3 · fonts.json
  ch_<슬러그>/                         ← 채널마다 작업 폴더
    00_progress.md                     ← 단계표(진행 한 줄)
    01_select/   top.json · 선정표.md · 전체목록.json · 메타표.md · 길이분포.png
    02_source/   <영상id>.mp4 · <영상id>.info.json · <영상id>.ko.vtt · <영상id>.comments.json · <영상id>.mp4.asr.json · 받기검사.md
    03_tear/<영상id>/   뜯기.json · sheet_1s.jpg · 정밀.json
    04_frames/<영상id>/ sheet_2fps.jpg · strips_01s/<초>.jpg · 판독목록.json
    04_frames/fontset/  글꼴 모음 그림(분위기마다 새 글꼴이 보인 장면)
    05_lines/    <영상id>.json · 줄판독_브리프.md
    06_rules/    규칙빈도.json · 규칙빈도.md · 대본말꼴.md · 팔레트.json · 스타일분석_초안.md · 스타일분석.md · 반대검사.md
    07_pan/      판.json · 판_업그레이드.json · 판_만든기록.md · 업그레이드_기록.md · 하이브리드_설계.md · 기능_만들목록.md · frame_<영상id>.json · 발음사전.json
    08_make/ep<NN>_<영문낱말>_<MMDD_HHMM>/   대본.json · 결과물기록표.json · 재료.json · 출처.md · src.mp4 · src.asr.json · 자막표.json · timeline.json · final.mp4 · run_log.json
    09_verify/   재현일치도.md · 재현일치도.json · 픽셀차이표.md · compare_sheet.png · watch_pack/ · 시청판정.json
    10_apply/    장면표.md · 업로드글.txt · 채널분석보고서.md · 장점메모.md · 결과물기록표.json
  (음원 분리 결과 = 03_tear/<영상id>/<영상id>_vocals.wav · _bg.wav)
  presets/<슬러그>/                     ← 저장한 프리셋(1-2 나무) — 회원 눈 판정 '통과' 뒤 §11
```

#### 1-2. 저장 폴더 나무 (presets/<슬러그>/)

```
presets/<슬러그>/
  카드.json                   ← 프리셋 한 장 요약 · 완료 단계
  판설정.json                 ← 다음 편을 만들 때 render.py 가 읽는 값(07_pan/판.json 과 같은 값 + 숫자마다 _from)
  규칙.json                   ← 요소 15종 "언제 무엇을 붙이나"
  lines/<영상id>.json         ← 줄판독(따라 한 벤치 편마다 한 파일)
  스타일분석.md               ← 11축 머리
  팔레트.json                 ← 층별 색
  재현일치도.md               ← 벤치 vs 우리 칸 표
  기본값.json                 ← 목소리·빠르기·배경음·자막 쌓기
  출처.md                     ← 쓴 영상 주소·계정·확인 방법
  제작순서.md                 ← 다음 편 만드는 단계
  금지.md                     ← 이 채널에서 하면 안 되는 것
  실패기록.md                 ← 깎기 내역(결과물을 보고 고친 것)
  sample/                     ← final.mp4 · sheet_1s.jpg · thumb.jpg · compare_sheet.png
  assets/                     ← (선택) 로고 자리 내 브랜드 그림 등 렌더가 읽는 그림(brand_band.png)
```

#### 1-3. 슬러그 짓는 법
- 채널 @핸들에서 만든다. 영문 소문자 · 숫자 · 밑줄(`_`)만(검사 꼴 `^[a-z][a-z0-9_]{1,30}$`).
- 핸들이 영문이면 소문자로 그대로(대시·점은 밑줄로). 한글이면 소리 나는 대로 로마자로 붙여 쓰고, 영어에서 온 낱말은 영어 철자로 — 예 `@스냅봤니` → `snapbwatni`(스냅 = snap · 봤니 = bwatni).
- 같은 슬러그 폴더에 다른 채널 기록이 있으면 `_2`·`_3` 을 붙인다(예 `snapbwatni_2`).

#### 1-4. 파일 이름 규칙
| 무엇 | 꼴 | 예 |
|---|---|---|
| 벤치 영상 파일·폴더 | 유튜브 영상 id 11자 그대로(`[A-Za-z0-9_-]{11}`) + 확장자 | `02_source/<영상id>.mp4` · `03_tear/<영상id>/` |
| 편 폴더(제작) | `ep<두 자리 번호>_<영문 낱말>_<MMDD_HHMM>` — 다시 만들 때마다 새 시각 폴더(지난 폴더는 읽기만) | `ep01_namdaemun_1106_0748` |
| 판 | `07_pan/판.json` 하나(업그레이드는 `판_업그레이드.json`) · 판 안 `name` = `<채널 이름>판` | `스냅봤니판` |
| ffmpeg 가 읽는 그림·영상·소리 | 영문·숫자·밑줄만 | `sheet_1s.jpg` · `compare_sheet.png` · `final.mp4` |
| 사람이 읽는 json·md | 이 표의 한글 이름 그대로(바꾸지 않는다) | `스타일분석.md` · `판설정.json` |
| 띠 그림 | `<초 소수 한 자리>.jpg` | `strips_01s/4.8.jpg` |

#### 1-5. 단계마다 쓰는 자리
| 단계 | 폴더 | 만드는 파일 이름 꼴 | 예(스냅봤니) |
|---|---|---|---|
| 시작 | `copywork/` | guide.md · preset_spec.md · `_tools/check_preset.py` · 회원지시.md | — |
| 0 선정 | `ch_<슬러그>/01_select/` | top.json · 선정표.md · 전체목록.json · 메타표.md · 길이분포.png | `ch_snapbwatni/01_select/top.json` |
| 1 받기 | `02_source/` | `<영상id>.mp4 · .info.json · .ko.vtt · .comments.json` · 받기검사.md | `02_source/video_A.mp4` |
| 2 뜯기 | `03_tear/<영상id>/` | 뜯기.json · sheet_1s.jpg · 정밀.json | `03_tear/video_A/뜯기.json` |
| 3 프레임 | `04_frames/<영상id>/` | sheet_2fps.jpg · `strips_01s/<초>.jpg` · 판독목록.json | `04_frames/video_A/strips_01s/4.8.jpg` |
| 4·5 뼈대·줄판독 | `05_lines/` | `<영상id>.json` · 줄판독_브리프.md | `05_lines/video_A.json` |
| 6 규칙 | `06_rules/` | 규칙빈도.json · 규칙빈도.md · 대본말꼴.md · 팔레트.json · 스타일분석.md · 반대검사.md | `06_rules/스타일분석.md` |
| 7 판 | `07_pan/` | 판.json · 판_만든기록.md · 기능_만들목록.md · `frame_<영상id>.json` | `07_pan/판.json` |
| 8 제작 | `08_make/ep<NN>_<영문>_<MMDD_HHMM>/` | 대본.json · 재료.json · 출처.md · src.mp4 · 자막표.json · timeline.json · final.mp4 · run_log.json | `08_make/ep01_namdaemun_1106_0748/final.mp4` |
| 9 검증 | `09_verify/` | 재현일치도.md·.json · 픽셀차이표.md · compare_sheet.png · `watch_pack/` · 시청판정.json | `09_verify/compare_sheet.png` |
| 10 적용 | `10_apply/` | 장면표.md · 업로드글.txt · 채널분석보고서.md · 장점메모.md | `10_apply/장면표.md` |
| 저장 | `presets/<슬러그>/` | 1-2 나무 | `presets/snapbwatni/카드.json` |
<!--FOLDER_END-->

#### 1-6. 왜 이렇게 갈랐나
- **폴더 이름은 전부 영문**(presets · <슬러그> · lines · sample · assets). 렌더 도구가 ffmpeg 에 경로를 넘길 때 한글이 끼면 죽는다 — 실측(2026-11-06, ffmpeg 8.1.2): drawtext 에 한글 폴더·한글 파일 이름 글꼴을 주면 접근 위반(종료 코드 3221225477), 같은 파일을 영문 경로로 주면 0.
- **sample/·assets/ 안 파일 이름도 영문**(ffmpeg 가 읽는 그림·영상).
- **json·md 파일 이름은 위 한글 이름 그대로**(파이썬·클로드만 읽는다 — 지침서·명령과 같은 이름이라 어긋나지 않는다). 다른 이름으로 바꾸지 않는다.
- 파일 안에 적는 경로는 **프리셋 폴더 기준 상대경로**(예 `lines/`, `sample/final.mp4`). 드라이브 글자로 시작하는 경로·사용자 폴더 경로 같은 내 PC 경로는 검사가 거절한다.

---

### 2. 모든 파일에 공통인 적는 법

| 규칙 | 뜻 | 예 |
|---|---|---|
| 단위 | 크기·좌표 px · 색 #RRGGBB · 시간 초 · 음량 LUFS·dB · 말속도 자/초 | `"px": 62` · `"fill": "#FFFFFF"` |
| `_from` | 판설정·기본값의 숫자 칸 K 바로 옆에 `"K_from": "뒷받침"`. 뒷받침 = 몇 편 몇 초에서 잰 값 / 어떤 파일의 어느 칸 | `"px": 62, "px_from": "잉크 높이 56~60px(lines/ size_px 62)"` |
| 숫자 묶음 | 숫자만 든 목록·사전(`[0,521,1080,1399]` · `{"cut":1.0}`)은 값 하나로 보고 `_from` 하나 | `"window_from": "..."` |
| 도구 집계 | `made_by` 와 `source` 가 함께 있는 묶음(도구가 센 표)은 그 두 칸이 뒷받침 — 안 숫자마다 `_from` 안 단다 | `placement.counted` |
| 안 잼 | 못 잰 값도 남긴다: `"안 잼 — 다음: <잴 방법>"`. 같은 줄 안에 `다음:` 이 없으면 검사가 거절 | `"fade_out_from": "안 잼 — 다음: 마지막 2초 RMS 로 잰다"` |
| 신뢰도 | `픽셀`(프로그램 실측) · `눈`(클로드가 프레임을 보고) · `신호`(기계 판독·agy) · `미측정` 넷 중 하나 | |
| 표본부족 | 분모 n < 5 이면 등급 = 표본부족(규칙으로 쓰되 강하게 믿지 않는다). 줄판독이 5편 밑이면 카드 `sample_short: true` | |
| 등급 | n ≥ 5 이고 k/n ≥ 0.6 = 강 · ≥ 0.3 = 중 · 그 밑 = 약 · n < 5 = 표본부족 | 12/93 = 약 |
| 회원 말 | 작업 중 회원이 고치라고 한 말은 규칙.json 또는 금지.md 의 한 줄로 남긴다 | |
| 키·비밀 | 키 값은 어느 파일에도 적지 않는다 | |

---

### 3. 파일마다

#### 3-1. 카드.json

**목적**: 프리셋 한 장 요약 — 무엇을 따라 했고, 어디까지 왔고, 무엇이 남았나.

**칸**

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| slug | 영문 슬러그(폴더 이름과 같다) | 영문 소문자 | 필수 | snapbwatni |
| channel · channel_url | 따라 한 벤치 채널 이름·주소 | 글 | 필수 · 선택 | 스냅봤니 |
| brand | 로고 자리에 넣는 내 브랜드 | 글 | 필수 | 숏템스냅 |
| format · format_note | 형식 — 나레형 / 원음형 / 나레+원음 · 한 줄 설명 | 셋 중 하나 · 글 | 필수 · 선택 | 원음형 |
| sound_style · voice · bgm · caption_look | 소리 결 · 목소리 이름(없으면 '없음') · 배경 음악 id · 자막 꼴 한 줄 | 글 | 필수 | 원음 + BGM · 없음 |
| copied_n | 따라 만든 시험편 수 | 정수 ≥0 | 필수 | 1 |
| line_reads_n | 줄판독 편 수 = lines/ 파일 수 | 정수 | 필수 | 4 |
| sample_short · sample_short_why | 줄판독 5편 밑이면 true + 이유 | 참/거짓 · 글 | 필수(5편 밑이면 true) | true |
| axes | 11축(1자막·2제목틀·3전환·4장면대사·5스토리·6대본언어·7소리·8스티커짤·9썸네일·10소재·11채널)마다 {value, confidence} | 사전 11칸 · confidence 넷 중 하나 | 필수 | "3전환": {"value":"하드컷만 11/11","confidence":"픽셀"} |
| rules_file · rules_n · rules_unmeasured | 규칙 파일 · 줄 수 · 미측정 줄 수 | 글 · 정수 | 필수 · 선택 | 규칙.json · 18 · 1 |
| match | 재현일치도 기준 칸 수(rows)·○(ok, 해당 없음 포함)·×(bad)·안 잼(unmeasured)·판정 · 픽셀 표 안/전체 | 정수 — 재현일치도.md 표와 같아야 | 필수 | rows 19 · ok 15 · bad 1 · unmeasured 3 |
| eye | {member_pass: 회원 눈 판정 통과?, note} | 참/거짓 | 필수 | false |
| done | {level 0~3, level_name, missing[남은 일], next(다음 할 일)} | 4절 표대로 계산한 값 | 필수 | level 0 |
| saved_at | 저장 날짜 | YYYY-MM-DD | 필수 | 2026-11-06 |

**예시 전문(스냅봤니 실제)**

```json
{
 "slug": "snapbwatni",
 "channel": "스냅봤니",
 "channel_url": "https://www.youtube.com/@스냅봤니",
 "brand": "숏템스냅",
 "format": "원음형",
 "format_note": "남의 일상 클립 재편집 — 원본 소리 + 아래 해설 자막 + 위 말풍선(나레 없음)",
 "sound_style": "원음 + BGM",
 "voice": "없음",
 "bgm": "honwaka_puppu",
 "caption_look": "흰 BMJUA 검정 테 8px 해설 + 검정 상자 색 글 말풍선",
 "copied_n": 1,
 "line_reads_n": 4,
 "sample_short": true,
 "sample_short_why": "줄판독 4편 < 5 — 편 단위 규칙은 전부 표본부족(규칙.json)",
 "axes": {
  "1자막": {
   "value": "해설 BMJUA 62px 흰 글 검정 테 8px 컷인 + 말풍선 검정 상자 색 글 기울기 +4.7°",
   "confidence": "픽셀"
  },
  "2제목틀": {
   "value": "흰 바탕 #FDFDFD · 위 로고 띠 · 제목 2개 줄(검정 #010001 / 분홍 #FB39A7) Cafe24Ohsquare 92px · 창 y521~",
   "confidence": "픽셀"
  },
  "3전환": {
   "value": "하드컷만 11/11",
   "confidence": "픽셀"
  },
  "4장면대사": {
   "value": "fit 93개 줄 모두 8 — 줄마다 다시 매겨야 함",
   "confidence": "눈"
  },
  "5스토리": {
   "value": "상황 → '~라는데' → 행동 → 질문 → 반전(길이 0.30~0.70) → 공개 → 감상 '~네요'",
   "confidence": "눈"
  },
  "6대본언어": {
   "value": "3인칭 관찰 반말 · 끝만 '~네요' · 조각 11.5~14자 · ㅋㅋㅋ 줄 0.10~0.36",
   "confidence": "픽셀"
  },
  "7소리": {
   "value": "나레 없음 · BGM 크게 4/4 · 원본 현장음 · 효과음 미측정",
   "confidence": "신호"
  },
  "8스티커짤": {
   "value": "끝 흐린 분홍 하트 3/4 · 이모지·반짝이 12/93개 줄 · 짤 0",
   "confidence": "신호"
  },
  "9썸네일": {
   "value": "0초 = 원본 첫 장면 + 틀 제목 4/4",
   "confidence": "눈"
  },
  "10소재": {
   "value": "아이·가족·직장·시장 '일상 돌발 순간' 인스타 릴스 · 제품 없음",
   "confidence": "눈"
  },
  "11채널": {
   "value": "구독 76,400 · 165편 · 조회 중앙 473,000 · 구독 대비 중앙 6.19",
   "confidence": "픽셀"
  }
 },
 "rules_file": "규칙.json",
 "rules_n": 18,
 "rules_unmeasured": 1,
 "match": {
  "file": "재현일치도.md",
  "rows": 19,
  "ok": 15,
  "bad": 1,
  "unmeasured": 3,
  "verdict": "미달",
  "pixel_in": 18,
  "pixel_total": 27
 },
 "eye": {
  "member_pass": false,
  "note": "회원 눈 판정 전 — 클로드 1차 의견 미달(말풍선 7개뿐·끝 하트·스티커 0·토막 경계 소리 끊김)"
 },
 "done": {
  "level": 0,
  "level_name": "분석 덜 됨",
  "missing": [
   "줄판독 2편 더(지금 4편, 1단계는 6편 이상)",
   "재현일치도 미측정 3칸(fx.pos·transition.rate·thumb.frame0) 재기",
   "framecmp × — 자막 띠 y 11px·줄 폭 30% 차 고치기",
   "끝 하트·스티커 render.py 에 만들기",
   "회원 눈 판정"
  ],
  "next": "벤치 2편 더 받아 줄판독 → 규칙.json·스타일분석.md 다시 → check_preset.py 로 1단계 확인"
 },
 "saved_at": "2026-11-06"
}
```

**흔한 실수**
- match 숫자를 재현일치도.md 와 따로 세어 어긋남 — 검사가 두 숫자를 맞대어 본다.
- done.level 을 바라는 값으로 적음 — 검사가 파일 내용으로 계산한 단계와 다르면 거절.
- 5편 밑인데 sample_short 를 안 적음.
- axes 에 값만 적고 confidence 를 뺌.

#### 3-2. 판설정.json

**목적**: 다음 편을 만들 때 render.py 가 **이 파일 하나만** 읽는다. 작업 폴더 `07_pan/판.json` 과 같은 값이고, 저장 때 숫자마다 `_from` 을 붙인다. 칸 이름은 판 칸 이름 그대로 쓴다.

**칸**

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| name | 판 이름 | 글 | 필수 | 스냅봤니판 |
| renderer | 그리는 길(1차 판은 bench) | 글 | 필수 | bench |
| bench | 뒷받침 파일: ko · channel · analysis · line_reads · palette · rules | 프리셋 폴더 상대경로 | 필수 | "line_reads": "lines/" |
| voice | {name, voice_id, none, why} — 나레 없으면 none: true |  | 필수 | none: true |
| cps_target | 목표 말속도(배속은 렌더가 계산) | 자/초 4~12 | 선택(나레형 필수) | 7.0 |
| bgm | {id, db_below_voice, duck_orig_db, fade_out} — id 는 내 곡 목록 이름 | dB · 초 | 필수 | db_below_voice 5.0 |
| loudness | {lufs, tp} | −14 · −1.5 고정 | 필수 | −14.0 |
| length | {min, max} | 초 | 필수 | 16.1 ~ 37.6 |
| timing | {gap(줄 사이), tail(끝 여운)} | 초 | 필수 | 0.0 |
| frame | 틀: kind · bg · window[x,y,w,h] · band(로고 자리 그림) · title[](줄마다 font·px·ink_top·color·max_w) · logo · watermark · credit · 채널 고유 층(예 bubble) | px · hex | 필수 | window [0,521,1080,1399] |
| caption | 자막: layers[](층마다 name·font·px·fill·outline{px,hex}·shadow·box·x·y_center·max_w·letter_gap_px·enter·exit) · pack_default(줄 칸별 등장) · typing_cps · chunk_max_chars | px · hex · 자 | 필수 | BMJUA 62 · 테 8 |
| cuts | {push_tts, push_orig, transition{kinds, ms}} | 비율 · ms | 필수 | kinds {cut:1.0} |
| sfx_files | 효과음 종류 → 파일 · gain_db | dB | 선택 | gain_db −8(안 잼) |
| placement | {rules(손으로 — 등장·전환·짤·효과음 규칙), counted(도구 집계 — made_by·source 필수)} |  | 필수 | rules.enter 전부 cut |
| rhythm | 판 리듬 4칸: cut_median{v,max} · hook_cuts_3s{min} · plain_share{v,tol,range} · photo_share_max{v} | 초 · 비율 | 필수 | cut_median 3.97 |
| title_form | 제목 꼴 한 줄 | 글 | 선택 | 2개 줄 — 검정 상황 / 분홍 반응 |
| script | {brief[대본 지시 줄], audit[검사 규칙]} | 글 | 필수 | brief 4개 줄 |
| source | {min_h} 원본 최소 높이 | px | 선택 | 720 |
| checks | 켜고 끄는 검사(참/거짓) + why | 참/거짓 | 선택 | even_height true |
| <숫자칸>_from | 그 숫자의 뒷받침(2절) | 글 · '안 잼 — 다음:' 허용 | 숫자마다 필수 | "px_from": "…" |

**예시 전문(스냅봤니 실제)**

```json
{
 "name": "스냅봤니판",
 "renderer": "bench",
 "_note": "스냅봤니 1차 판(2026-11-06) — 나레 없는 클립 재편집: 원본 한 장면을 2.6~4.6초 토막으로 건너뛰어 + 아래 흰 해설 자막 + 위 말풍선 + 원본 소리 + BGM",
 "bench": {
  "ko": "스냅봤니",
  "channel": "https://www.youtube.com/@스냅봤니",
  "analysis": "스타일분석.md",
  "line_reads": "lines/",
  "palette": "팔레트.json",
  "rules": "규칙.json",
  "sfx_events": null
 },
 "voice": {
  "name": null,
  "voice_id": null,
  "none": true,
  "why": "벤치 나레 0/4편(agy 귀 4/4 '나레 없음') — 목소리 합성 안 함"
 },
 "cps_target": 7.0,
 "cps_target_from": "나레 없음 — 해설 글 읽기 속도 편별 7.49·5.87·8.98·10.1자/초(lines/ 4편 해설 글자÷표시 초)의 아래쪽 중앙 · 계획 어림용",
 "bgm": {
  "id": "honwaka_puppu",
  "why_id": "벤치 곡은 남의 곡이라 안 씀 — 내 곡 목록에서 경쾌·코믹 결",
  "db_below_voice": 5.0,
  "db_below_voice_from": "원음보다 5dB 아래 — 1차 렌더 10dB 아래에서 agy 귀 '배경음 작음·토막 경계마다 현장음 툭 끊김' → 5dB 로 올림(실패기록.md 4)",
  "duck_orig_db": 0.0,
  "duck_orig_db_from": "벤치 4/4 BGM 이 원음 위에 크게 깔림(agy) — 원음 줄에서 따로 줄이지 않음",
  "fade_out": 0.5,
  "fade_out_from": "안 잼 — 다음: 벤치 4편 마지막 2초 0.25초 RMS dB 로 BGM 내려가는 길이를 잰다(지금 0.5 는 렌더 도구 기본값)"
 },
 "loudness": {
  "lufs": -14.0,
  "lufs_from": "−14 통일(지침서 §5 — 벤치 −7.7~−15.1 과 견주지 않는다)",
  "tp": -1.5,
  "tp_from": "−1.5 dBTP 통일(지침서 §5)"
 },
 "length": {
  "min": 16.1,
  "min_from": "벤치 4편 길이 16.1·16.4·34.0·37.6초 중 최소",
  "max": 37.6,
  "max_from": "같은 4편 중 최대"
 },
 "timing": {
  "gap": 0.0,
  "gap_from": "해설 줄 사이 빈틈 편별 중앙 0.0~0.5초(lines/ 4편 t0−앞줄 t1) — 줄 사이는 원본 토막이 바뀌는 자리",
  "tail": 0.0,
  "tail_from": "안 잼 — 다음: 벤치 4편 마지막 해설 줄 끝 → 영상 끝 초를 lines/ t1 과 dur 로 잰다"
 },
 "frame": {
  "kind": "window",
  "bg": [
   253,
   253,
   253
  ],
  "bg_from": "바탕 #FDFDFD — video_D 8초·video_A 5초 원 프레임 0~150행 픽셀 중앙(lines/ layout._basis)",
  "window": [
   0,
   521,
   1080,
   1399
  ],
  "window_from": "세로 원본 편 video_D 실측 y521~1919(lines/video_D.json layout.window) — 가로 원본 편은 y524~1533",
  "band": {
   "src": "assets/brand_band.png",
   "box": [
    0,
    0,
    1080,
    330
   ],
   "box_from": "벤치 로고 자리 y193~317 x108~408 을 덮는 위 띠(내 브랜드 그림으로 바꾸는 곳은 이 자리뿐)"
  },
  "title": [
   {
    "font": "Cafe24Ohsquare.ttf",
    "px": 92,
    "px_from": "같은 글을 잉크 높이 80px 로 그려 벤치 video_C 크롭과 대조: 획 14.0 vs 13.4 · 채움 0.479 vs 0.484(후보 글꼴 13개 중 가장 가까움)",
    "ink_top": 332,
    "ink_top_from": "1개 줄 잉크 y332~411(lines/ layout.title_rows.line1)",
    "color": "#010001",
    "max_w": 1000,
    "max_w_from": "1개 줄 잉크 x107~974(폭 867) + 여유 — 벤치 최대 폭"
   },
   {
    "font": "Cafe24Ohsquare.ttf",
    "px": 92,
    "px_from": "1개 줄과 같은 글꼴·크기(2개 줄 잉크 높이 77 vs 1개 줄 79)",
    "ink_top": 423,
    "ink_top_from": "2개 줄 잉크 y423~500(lines/ layout.title_rows.line2)",
    "color": "#FB39A7",
    "max_w": 1000,
    "max_w_from": "1개 줄과 같음"
   }
  ],
  "logo": null,
  "watermark": null,
  "credit": null,
  "bubble": {
   "font": "BMJUA.ttf",
   "px": 72,
   "px_from": "말풍선 글 폭이 BMJUA 72px 와 3/4 편 0.98~1.0(벤치 말풍선 31개 줄 가운데 시각 프레임)",
   "rot": 4.7,
   "rot_from": "글 기울기 중앙 +4.7도(29개, −3.9~13.4)",
   "box": {
    "rgb": "#000000",
    "alpha": 1.0,
    "alpha_from": "상자 안 색 중앙 #000000 — 밝은 배경 위 불투명",
    "radius": 14,
    "radius_from": "똑바른 검정 상자 7개 네 모서리 윤곽을 원에 맞춤 — 위 모서리 중앙 13.3·전체 중앙 14(실패기록.md 6)",
    "pad_x": 23,
    "pad_x_from": "잘 잡힌 상자 9개 가로 여백 중앙",
    "pad_y": 17,
    "pad_y_from": "같은 9개 세로 여백 중앙"
   },
   "ring": {
    "px": 6,
    "px_from": "흰 테 꼴 5/31 — 흰 테 약 6px(눈, 기울기가 섞여 픽셀로는 안 잼 — 다음: 기울기 0도 근처 흰 테 말풍선만 골라 가로줄 스캔)",
    "color": "#FFFFFF"
   },
   "colors": {
    "yellow": "#FCE61C",
    "green": "#3CF141",
    "pink": "#F741A4",
    "blue": "#4EA1FB",
    "sky": "#7EE9FA"
   },
   "colors_from": "렌더에 쓰는 정본 = 말풍선 31개 줄 가운데 시각 프레임에서 프로그램으로 잰 글색 픽셀 중앙. 팔레트.json 본문 층의 #FFE14A·#39E85A·#FF4FA3·#3E8BFF·#7FD8FF 는 줄판독 fill_hex(눈 판독)를 센 벤치 기록이라 값이 다르다 — 둘 다 남기고, 렌더는 이 칸 값을 쓴다",
   "color_count": {
    "yellow": 10,
    "green": 9,
    "pink": 8,
    "blue": 3,
    "sky": 1
   },
   "color_count_from": "말풍선 31개 줄 글색 실제 픽셀 중앙 개수(팔레트.json 눈값과 다름 — 그림 쪽 값을 쓴다)",
   "per_10s": 2.98,
   "per_10s_from": "말풍선 31개 줄 ÷ 104.1초 × 10(lines/ 4편 길이 합)",
   "show_sec": [
    0.7,
    2.6
   ],
   "show_sec_from": "말풍선 표시 초 범위(lines/ t1−t0)",
   "center_y": [
    642,
    826
   ],
   "center_y_from": "상자 가운데 y 범위 / 1920 — 인물 머리 옆(편마다 다름)"
  }
 },
 "caption": {
  "layers": [
   {
    "name": "해설",
    "font": "BMJUA.ttf",
    "px": 62,
    "px_from": "잉크 높이 56~60px(lines/ size_px 62, 글꼴 크기는 눈 ±3px)",
    "fill": "#FFFFFF",
    "outline": {
     "px": 8,
     "px_from": "검정 외곽선 획 8.0px(크롭 6개 같음, lines/ outline.px)",
     "hex": "#000000"
    },
    "shadow": null,
    "box": null,
    "x": 540,
    "x_from": "가운데 정렬 x540(lines/ x)",
    "y_center": 1288,
    "y_center_from": "세로 원본 편 잉크 1256~1319 가운데(video_D·video_B lines/ y)",
    "max_w": 1014,
    "max_w_from": "lines/ max_w 1014",
    "letter_gap_px": 0,
    "letter_gap_px_from": "lines/ letter_gap_px 0(눈)",
    "enter": "instant",
    "exit": "instant"
   }
  ],
  "pack_default": {
   "narr.first": "cut",
   "narr.rest": "cut",
   "orig.first": "cut",
   "orig.rest": "cut"
  },
  "typing_cps": null,
  "chunk_max_chars": 18,
  "chunk_max_chars_from": "해설 조각 자수 최대 18(편별 중앙 12·11.5·13·14 · p90 15~16, lines/ 4편 OCR)"
 },
 "cuts": {
  "push_tts": 0.0,
  "push_tts_from": "카메라 = 원본 그대로(편집 줌 없음, 1초 시트 눈)",
  "push_orig": 0.0,
  "push_orig_from": "같음",
  "transition": {
   "kinds": {
    "cut": 1.0
   },
   "kinds_from": "줄판독 컷 경계 11/11 하드컷(lines/ cut_at · 0.1초 띠)",
   "ms": 0,
   "ms_from": "전환 효과 0 → 길이 0"
  }
 },
 "sfx_files": {
  "gain_db": -8,
  "gain_db_from": "안 잼 — 다음: 효과음 규칙이 생기면 벤치 효과음 구간 LUFS − 원음 LUFS 로 잰다(지금 −8 은 렌더 도구 기본값, 효과음 0발이라 쓰이지 않음)"
 },
 "placement": {
  "rules": {
   "enter": {
    "narr.first": "cut",
    "narr.rest": "cut",
    "orig.first": "cut",
    "orig.rest": "cut",
    "why": "해설 등장 instant 93/93(규칙.json cap_enter 강)"
   },
   "transition": {
    "kinds": [],
    "why": "전환 효과 0"
   },
   "meme": {
    "rate": 0.0,
    "rate_from": "짤 0/4편(규칙.json meme)"
   },
   "sfx": {
    "kinds": {},
    "max": 0,
    "max_from": "효과음 뒷받침 미측정(규칙.json sfx) → 1차 판 0발"
   }
  },
  "counted": {
   "made_by": "rules.py count(lines/ 4편 집계)",
   "source": "lines/",
   "n_videos": 4,
   "slots": {
    "orig.first": {
     "n": 4,
     "enter": {
      "cut": 1.0
     },
     "emph": 0.0
    },
    "orig.rest": {
     "n": 89,
     "enter": {
      "cut": 1.0
     },
     "emph": 0.011
    }
   },
   "share": {
    "emph": 0.25,
    "typing": 0.0,
    "sfx": 0.0
   },
   "stickers": {
    "circle_arrow": 0.25,
    "heart": 0.75,
    "other": 0.75,
    "spark_lines": 0.5
   },
   "transition": {
    "cut": 1.0
   },
   "sfx_kinds": {
    "other": 1.0
   }
  }
 },
 "rhythm": {
  "cut_median": {
   "v": 3.97,
   "v_from": "벤치 4편 영상 창 컷 중앙(cuts.py) 4.53·3.70·2.67·4.23 → 중앙",
   "max": 4.53,
   "max_from": "가장 느린 편 video_A"
  },
  "hook_cuts_3s": {
   "min": 0,
   "min_from": "0.1~3초 진짜 컷 경계 편별 0(video_A 첫 컷 9.87)·1(video_B 0.83)·1(video_C 2.67)·0(video_D 11.2) → 최소"
  },
  "plain_share": {
   "v": 0.8,
   "v_from": "꾸밈 없는 줄 74/93(편별 12/15·26/30·13/14·23/34)",
   "tol": 0.13,
   "tol_from": "편별 값과 0.8 의 최대 거리 0.129",
   "range": [
    0.676,
    0.929
   ],
   "range_from": "편별 최소·최대"
  },
  "photo_share_max": {
   "v": 0.0,
   "v_from": "벤치 정지 사진 컷 0/4편"
  }
 },
 "title_form": "2개 줄 — 1개 줄 상황 8~11자(검정) / 2개 줄 결론·반응 11~15자 + ㅋㅋㅋ(분홍)",
 "script": {
  "brief": [
   "나레 없음 — 모든 줄 kind:'orig'{id, src, spans[[a,b]], caps_rel[[글, 시작, 끝]]} — 한 줄 = 원본 한 토막 2.6~4.6초(벤치 컷 중앙 3.97), 토막 사이는 1초 넘게 건너뛴다.",
   "해설 = 3인칭 관찰 반말, 끝 줄만 '~네요'. 첫 줄 = 장소·인물·상황을 열어 두고('~에서/~의/~고'), 둘째 줄 '~라는데/~다는데 ㅋㅋㅋ'(4/4편).",
   "한 줄 11~14자(최대 18) · 1.3~1.9초 · 반전은 길이 0.3~0.7 자리 · 끝 = 감상·응원 '~네요'(4/4). CTA 0.",
   "장면에 보이는 것·원본 말(받아쓰기·박힌 글로 확인)만 말한다 — 지어낸 사실·금액 금지."
  ],
  "audit": [
   {
    "id": "est_length",
    "kind": "est_length",
    "min": 16.1,
    "min_from": "length.min 과 같음",
    "max": 37.6,
    "max_from": "length.max 와 같음"
   }
  ]
 },
 "source": {
  "min_h": 720,
  "min_h_from": "원본 높이 720 아래면 창 1399 에 늘려져 흐리다(우리 다른 판과 같은 선)"
 },
 "checks": {
  "hook_ending": true,
  "join_forbid": true,
  "no_stretch": true,
  "even_height": true,
  "timing_words": false,
  "why": "창 높이 1399 홀수 → 짝수 높이 필요(even_height) · 나레 없음 → 받아쓰기 시각 맞춤 끔(timing_words)"
 }
}
```

**흔한 실수**
- 묶음마다 why 하나만 적음(우리 첫 판 꼴) — 어느 숫자 뒷받침가 빠졌는지 못 가린다. 숫자마다 `K_from`.
- bench 칸에 내 PC 절대경로 — 프리셋 폴더 상대경로로.
- 렌더 도구 기본값을 잰 값처럼 적음 — 기본값이면 '안 잼 — 다음:' 으로(예 bgm.fade_out).
- 같은 값을 두 칸에(예 voice 를 판설정과 기본값에 다르게) — 기본값.json 은 판설정을 가리킨다.
- frame.band.src 그림이 없음 — 내 브랜드 로고 그림이 없으면 브랜드 글을 벤치 로고 자리 크기(box)로 PIL 로 그려 assets/brand_band.png 로 둔다(만든 방법을 _from 에).
- 창이 하나뿐인데 가로 원본 소재를 씀 — 이 판 창은 세로 원본 편 실측이다. 가로 원본 소재면 창 비율이 달라 늘어난다(checks.no_stretch 가 멈춘다) → 세로 원본 소재를 고르거나 가로 원본 편 창(y524~1533)으로 판을 하나 더 만든다.

#### 3-3. 규칙.json

**목적**: 요소마다 "어떤 조건에서 무엇을 붙이나"를 벤치 빈도와 함께 적는다. 레코드 꼴은 15종 모두 같다. 한 요소에 여러 줄을 써도 된다. 없는 것도 규칙이다(예 짤 0 = '짤 없음' 한 줄).

**칸**

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| slug · n_videos · n_lines · grade_rule | 머리 칸 |  | 필수 | 4 · 93 |
| rules[].element | 요소 이름 — cap_look(자막 글꼴·px·색·외곽) · cap_enter(등장) · cap_emph(강조 낱말) · cap_exit(퇴장) · transition(컷 사이 효과) · cut_rhythm(컷 길이) · scene_fit(대사↔장면) · bgm · sfx(효과음) · meme(짤) · sticker · pointer(화살표·원) · thumb(0초 화면) · speech(말속도·쉼) · script(어미·박자·훅/끝) | 15종 이름 그대로 | 필수 · 15종 다 | cap_enter |
| cond | 조건(화자·자리·역할·층·첫 덩어리·낱말) | 글 | 필수 | 모든 층(화자=원음) |
| action | 동작(종류·값·시각) | 글 | 필수 | instant(컷인) · 0ms |
| unit | 분모 단위 | 줄 / 편 / 컷 경계 | 필수 | 줄 |
| k · n · rate | 벤치에서 n 번 중 k 번 · k/n | 정수 · 0~1 | 필수 | 93 · 93 · 1.0 |
| base | 우연 기대(전체 줄 평균) — 없으면 null | 0~1 | 필수(null 허용) | 0.13 |
| grade | 강 / 중 / 약 / 표본부족 — 2절 등급 계산과 같아야 | 넷 중 하나 | 필수 | 강 |
| evidence | 편 id·초 | 목록 | 필수(미측정이면 빈 목록 허용) | "video_A 4.8~5.2 …" |
| confidence | 픽셀 / 눈 / 신호 / 미측정 | 넷 중 하나 | 필수 | 픽셀 |
| engine_cell | 이 규칙을 담는 판설정 칸(없으면 '(없음 — 이유)') | 글 | 필수 | 판설정.json placement.rules.enter |
| engine_support | render.py 지원 ○ 그대로 / △ 근사 / × 없음(기능 만들 목록으로) | 셋 중 하나 | 필수 | ○ |
| measure_task | 미측정이면 다음 잴 방법(10자 이상) — 아니면 null 또는 의심 메모 | 글 · null | 필수(미측정이면 글) | null |

**예시 전문(스냅봤니 실제)**

```json
{
 "slug": "snapbwatni",
 "n_videos": 4,
 "n_lines": 93,
 "grade_rule": "n ≥ 5 이고 rate ≥ 0.6 = 강 / ≥ 0.3 = 중 / 그 밑 = 약 / n < 5 = 표본부족",
 "rules": [
  {
   "element": "cap_look",
   "cond": "층=해설(아래)",
   "action": "BMJUA 62px(잉크 56~60) · 채움 #FFFFFF · 검정 외곽선 8px · 상자·그림자 없음 · 가운데 x540 · 최대 폭 1014",
   "unit": "줄",
   "k": 60,
   "n": 60,
   "rate": 1.0,
   "base": null,
   "grade": "강",
   "evidence": [
    "video_D 0.0 y1256~1315",
    "video_A 4.8 잉크 위 y1215"
   ],
   "confidence": "픽셀",
   "engine_cell": "판설정.json caption.layers[0]",
   "engine_support": "○",
   "measure_task": null
  },
  {
   "element": "cap_look",
   "cond": "층=말풍선(위)",
   "action": "검정 둥근 상자(반지름 14·여백 23/17) + 색 글 BMJUA 72px · 기울기 중앙 +4.7° · 인물 머리 옆",
   "unit": "줄",
   "k": 26,
   "n": 33,
   "rate": 0.788,
   "base": null,
   "grade": "강",
   "evidence": [
    "video_D 0.8 '안 먹어! 안 먹는다고오오!'(흰 테 꼴)",
    "video_B 0.1 '자 드가자~ㅋㅋㅋ'"
   ],
   "confidence": "신호",
   "engine_cell": "판설정.json frame.bubble",
   "engine_support": "△",
   "measure_task": null
  },
  {
   "element": "cap_enter",
   "cond": "모든 층(화자=원음)",
   "action": "instant(컷인) · 0ms · 떠 있는 동안 움직임 0",
   "unit": "줄",
   "k": 93,
   "n": 93,
   "rate": 1.0,
   "base": null,
   "grade": "강",
   "evidence": [
    "video_A 4.8~5.2 0.1초 띠 — 앞 줄 한 프레임에 사라지고 통째로 나타남"
   ],
   "confidence": "픽셀",
   "engine_cell": "판설정.json placement.rules.enter",
   "engine_support": "○",
   "measure_task": null
  },
  {
   "element": "cap_emph",
   "cond": "해설 줄",
   "action": "강조 낱말 넣지 않음(없음도 스타일)",
   "unit": "줄",
   "k": 1,
   "n": 93,
   "rate": 0.011,
   "base": 0.01,
   "grade": "약",
   "evidence": [
    "video_B '삘(Feel)' #FF3FA4 — 93개 줄 중 1개 줄뿐"
   ],
   "confidence": "픽셀",
   "engine_cell": "판설정.json placement.counted.share.emph",
   "engine_support": "○",
   "measure_task": null
  },
  {
   "element": "cap_exit",
   "cond": "모든 줄",
   "action": "instant — 다음 줄 앞 0.1~0.5초 빈 화면",
   "unit": "줄",
   "k": 93,
   "n": 93,
   "rate": 1.0,
   "base": null,
   "grade": "강",
   "evidence": [
    "video_A 4.8~5.0 0.1초 띠"
   ],
   "confidence": "픽셀",
   "engine_cell": "판설정.json caption.layers[0].exit",
   "engine_support": "○",
   "measure_task": null
  },
  {
   "element": "transition",
   "cond": "컷 경계",
   "action": "하드컷(효과 없음)",
   "unit": "컷 경계",
   "k": 11,
   "n": 11,
   "rate": 1.0,
   "base": null,
   "grade": "강",
   "evidence": [
    "lines/ 4편 cut_at 11곳 — 0.1초 띠에서 번쩍·줌블러·검은 프레임 0"
   ],
   "confidence": "픽셀",
   "engine_cell": "판설정.json cuts.transition",
   "engine_support": "○",
   "measure_task": null
  },
  {
   "element": "cut_rhythm",
   "cond": "편 전체",
   "action": "컷 중앙 3.97초(편별 4.53·3.70·2.67·4.23) · 첫 3초 안 진짜 컷 0~1",
   "unit": "편",
   "k": 4,
   "n": 4,
   "rate": 1.0,
   "base": null,
   "grade": "표본부족",
   "evidence": [
    "video_A 첫 컷 9.87",
    "video_B 첫 컷 0.83",
    "video_C 첫 컷 2.67",
    "video_D 첫 컷 11.2"
   ],
   "confidence": "픽셀",
   "engine_cell": "판설정.json rhythm.cut_median",
   "engine_support": "○",
   "measure_task": null
  },
  {
   "element": "scene_fit",
   "cond": "모든 해설 줄",
   "action": "해설이 말하는 동작이 그 컷에 보인다(fit 8/10)",
   "unit": "줄",
   "k": 93,
   "n": 93,
   "rate": 1.0,
   "base": null,
   "grade": "강",
   "evidence": [
    "lines/ 4편 fit 93개 줄 모두 8"
   ],
   "confidence": "눈",
   "engine_cell": "제작순서.md 4단계(재료 고르기)",
   "engine_support": "△",
   "measure_task": "93개 줄이 모두 8 = 줄마다 따로 매긴 값이 아닐 수 있다 — 다음: 편마다 1초 시트 10칸을 보고 줄마다 0~10 을 다시 매겨 분포(평균·7 미만 비율)를 낸다"
  },
  {
   "element": "bgm",
   "cond": "편 전체",
   "action": "BGM 크게 + 원본 현장음 위(벤치 곡은 쓰지 않고 내 목록의 경쾌·코믹 곡, 원음보다 5dB 아래)",
   "unit": "편",
   "k": 4,
   "n": 4,
   "rate": 1.0,
   "base": null,
   "grade": "표본부족",
   "evidence": [
    "video_A 피지카토·실로폰",
    "video_B 레트로 댄스",
    "video_C 'Circle of Life' 풍",
    "video_D 남성 보컬 록"
   ],
   "confidence": "신호",
   "engine_cell": "판설정.json bgm",
   "engine_support": "○",
   "measure_task": null
  },
  {
   "element": "sfx",
   "cond": "말풍선·스티커 등장",
   "action": "1차 판 0발(뒷받침가 갈려 규칙으로 못 박지 않음)",
   "unit": "줄",
   "k": 8,
   "n": 93,
   "rate": 0.086,
   "base": 0.09,
   "grade": "약",
   "evidence": [
    "video_D agy 두 번 답 0 ↔ 7",
    "video_A agy 11개 이름 / 지난 판독 10개"
   ],
   "confidence": "미측정",
   "engine_cell": "판설정.json placement.rules.sfx",
   "engine_support": "○",
   "measure_task": "뜯기 효과음 후보 시각 + 10ms RMS 파형 솟음을 같이 보고 '둘다'인 것만 센다(agy 이름은 보조) — 줄 k/n 을 다시 낸다"
  },
  {
   "element": "meme",
   "cond": "편 전체",
   "action": "짤 없음",
   "unit": "편",
   "k": 0,
   "n": 4,
   "rate": 0.0,
   "base": null,
   "grade": "표본부족",
   "evidence": [
    "lines/ 4편 scene 칸에 '짤' 0"
   ],
   "confidence": "눈",
   "engine_cell": "판설정.json placement.rules.meme",
   "engine_support": "○",
   "measure_task": null
  },
  {
   "element": "sticker",
   "cond": "끝(마지막 1~2초)",
   "action": "흐린 분홍 하트 1개가 얼굴을 가림",
   "unit": "편",
   "k": 3,
   "n": 4,
   "rate": 0.75,
   "base": null,
   "grade": "표본부족",
   "evidence": [
    "video_A 31.0~32.6",
    "video_C 13.2~15.5",
    "video_D 14.3~15.6"
   ],
   "confidence": "신호",
   "engine_cell": "(없음 — render.py 에 흐린 하트 1개 모양 없음)",
   "engine_support": "×",
   "measure_task": "하트 크기·흐림·색 — 다음: 세 구간 프레임에서 분홍 덩어리 넓이·흐림 반경·중앙 hex 를 잰다"
  },
  {
   "element": "sticker",
   "cond": "모든 줄",
   "action": "이모지·반짝이·눈알 스티커(편당 1~5)",
   "unit": "줄",
   "k": 12,
   "n": 93,
   "rate": 0.129,
   "base": 0.13,
   "grade": "약",
   "evidence": [
    "video_C 2.1~3.8 굴러가는 눈 이모지",
    "video_A 당황 이모지 줄 10개"
   ],
   "confidence": "신호",
   "engine_cell": "판설정.json placement.counted.stickers",
   "engine_support": "×",
   "measure_task": null
  },
  {
   "element": "pointer",
   "cond": "훅(0~1.6초)",
   "action": "빨간 원(아이 얼굴)",
   "unit": "편",
   "k": 1,
   "n": 4,
   "rate": 0.25,
   "base": null,
   "grade": "표본부족",
   "evidence": [
    "video_A 0.0~1.6"
   ],
   "confidence": "신호",
   "engine_cell": "(없음 — 1차 판에 안 넣음)",
   "engine_support": "×",
   "measure_task": null
  },
  {
   "element": "thumb",
   "cond": "0초",
   "action": "원본 첫 장면 + 틀 제목(표지 카드 없음)",
   "unit": "편",
   "k": 4,
   "n": 4,
   "rate": 1.0,
   "base": null,
   "grade": "표본부족",
   "evidence": [
    "lines/ 4편 frame0.what '원본 첫 장면(표지 카드 없음) + 틀 제목'"
   ],
   "confidence": "눈",
   "engine_cell": "판설정.json frame.title",
   "engine_support": "○",
   "measure_task": null
  },
  {
   "element": "speech",
   "cond": "편 전체",
   "action": "나레 없음 — 목소리 안 넣음 · 해설 줄 표시 1.3~1.9초",
   "unit": "편",
   "k": 4,
   "n": 4,
   "rate": 1.0,
   "base": null,
   "grade": "표본부족",
   "evidence": [
    "agy 귀 4/4 '나레 없음'",
    "받아쓰기 rejected 2편(말소리 없음)"
   ],
   "confidence": "신호",
   "engine_cell": "판설정.json voice.none · cps_target",
   "engine_support": "○",
   "measure_task": null
  },
  {
   "element": "script",
   "cond": "둘째 해설 줄",
   "action": "'~라는데/~다는데 ㅋㅋㅋ' 로 받는다",
   "unit": "편",
   "k": 4,
   "n": 4,
   "rate": 1.0,
   "base": null,
   "grade": "표본부족",
   "evidence": [
    "video_A '터졌다는데'",
    "video_B '받았다는데'",
    "video_C '수단이라는데'",
    "video_D '중이라는데'"
   ],
   "confidence": "눈",
   "engine_cell": "판설정.json script.brief[1]",
   "engine_support": "○",
   "measure_task": null
  },
  {
   "element": "script",
   "cond": "마지막 해설 줄",
   "action": "감상·응원 '~네요' · CTA 없음",
   "unit": "편",
   "k": 4,
   "n": 4,
   "rate": 1.0,
   "base": null,
   "grade": "표본부족",
   "evidence": [
    "'대견하네요'",
    "'미소 짓게 되네요 💖'",
    "'아빠들 화이팅!'",
    "'현실 남매네요 ㅋㅋㅋ'"
   ],
   "confidence": "눈",
   "engine_cell": "판설정.json script.brief[2]",
   "engine_support": "○",
   "measure_task": null
  }
 ]
}
```

**흔한 실수**
- 빈도 표(조건×효과 k/n)만 두고 레코드 꼴로 안 옮김 — 검사가 '요소 없음 15종'으로 거절(6-1).
- n < 5 인데 '강' — 등급은 k/n 으로 다시 계산해 대조한다.
- 미측정인데 이유만 적고 다음 잴 방법이 없음.
- 93개 줄이 모두 같은 값(예 fit 8)인 것을 잰 값으로 믿음 — 의심 메모를 measure_task 에(예시 scene_fit).
- 빈도 표 → 레코드 바꾸는 법: 06_rules/규칙빈도.json 의 effect 가 enter=… → cap_enter · enter_fx → cap_enter(등장 효과 붙음) · emph·emph_color → cap_emph · sticker → sticker(화살표·원이면 pointer) · sfx → sfx · variant → cap_look. k·n·rate·base·grade 는 그대로 옮기고 cond 도 그대로. 빈도 표에 없는 요소(cap_look·cap_exit·transition·cut_rhythm·scene_fit·bgm·meme·thumb·speech·script)는 스타일분석.md 그 축의 실측 줄에서 한 줄씩 만든다(unit 은 줄/편/컷 경계 중 실제 분모).

#### 3-4. lines/<편 id>.json (줄판독)

**목적**: 벤치 한 편의 화면 자막 덩어리마다 한 줄 — 무엇이 붙었나·없나. 칸 정의는 지침서 §6-3 과 같고, 여기서는 **저장 때 꼭 있어야 하는 칸**만 다시 적는다(검사 기준).

**칸**

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| id · dur · fps · size | 편 id · 길이(초) · fps · [w,h] | 초 · px | 필수(id·dur) | video_D · 16.367 |
| title_lines[] | 틀 제목 줄 {text, hex} | hex | 필수 | 2개 줄 |
| source_label | 출처 줄 글(없으면 "") | 글 | 필수 | "" |
| form | 형식 한 낱말 | 리액션·랭킹·사연·정보·리뷰… | 선택 | 리액션 |
| layout | window · caption_band · title_y · logo_y · logo_x · source_y · source_hex · bg_hex · watermark{what,alpha} | px · hex | 선택(있으면 판설정 뒷받침) | window [0,521,1080,1399] |
| lines[].t0 · t1 | 덩어리 시작·끝 | 초, t1 > t0 | 필수 | 0.0 · 1.1 |
| lines[].speaker | 나레 / 원음[:이름] / 해설 / 제3자 / 불명 — 설명은 notes 로 | 어휘 | 필수 | 원음 |
| lines[].text · layer | 화면 글 그대로 · 층 이름 | 글 | 필수 | 스냅봤니·해설 |
| lines[].role | 훅 다리 고조 공개 증거 반전 질문 답 이음 본문 끝 | 어휘 | 필수 | 훅 |
| lines[].enter · emph · sticker · sfx | 등장 · 강조 낱말[] · 스티커[] · 효과음{kind,t,basis} 또는 null — 꾸밈 없는 줄도 빠짐없이 | [] 은 null 금지 | 필수 | instant · [] · [] · null |
| lines[].scene · fit · cut_at | 장면 종류 · 대사↔장면 0~10 · 덩어리 안 컷 시각[] | 0~10 · 초 | 필수 | 과정 · 8 · [] |
| lines[].y · fill_hex | 잉크 [y0,y1] · 채움 색 | px · hex | 필수 | [1256,1315] · #FFFFFF |
| lines[].transition · motion · confidence | 전환 cut/zoomblur/flash/black/none · 움직임 still/zoom_in/zoom_out/pan/cam · 신뢰도 | null 금지 | 필수 | none · cam · 픽셀 |
| lines[] 나머지 | font{name,basis} · size_px · x · align · max_w · letter_gap_px · line_gap_px · outline · ring · shadow · glow · box · enter_ms · enter_curve · type_cps · cursor · exit · variant · scene_desc · words · loud · notes | 지침서 §6-3 | 선택(검사 안 함 — 있으면 판설정 뒷받침) |  |
| beats · narr_share · notes[] | 흐름 한 줄 · 나레 비율 · 확인 못 한 것 | 글 | 필수 |  |
| frame0 | {what, face_frac, text} — text = 0초에 얹은 표지 카드 글만 |  | 필수 | 원본 첫 장면 + 틀 제목 |

**예시 전문(스냅봤니 실제)**

```json
{
 "id": "video_C",
 "dur": 16.133,
 "fps": 30.0,
 "size": [
  1080,
  1920
 ],
 "title_lines": [
  {
   "text": "약속 못 지킨 아빠가",
   "hex": "#010001"
  },
  {
   "text": "딸을 위해 선택한 기막힌 방법 ㅋㅋㅋ",
   "hex": "#FB39A7"
  }
 ],
 "source_label": "",
 "form": "리액션",
 "_form_vocab": "형식(유형) 한 낱말 — 예 리액션·랭킹·사연·정보·리뷰(rules-05, 형식별 집계)",
 "layout": {
  "window": [
   0,
   524,
   1080,
   1009
  ],
  "caption_band": [
   1210,
   1274
  ],
  "title_y": [
   332,
   500
  ],
  "source_y": null,
  "logo_y": [
   193,
   317
  ],
  "watermark": {
   "what": null,
   "alpha": 0
  },
  "title_rows": {
   "line1": [
    332,
    411
   ],
   "line2": [
    423,
    500
   ]
  },
  "logo_x": [
   108,
   408
  ],
  "bg_hex": "#FDFDFD",
  "source_hex": null,
  "_basis": "video_A 5초·video_D 8초 원 프레임 픽셀(check/z5.png·f8.png) — 띠 193~317·332~411·423~500, 1개 줄 #010001 · 2개 줄 #FB39A7 · 바탕 #FDFDFD"
 },
 "beats": "훅(0 '약속 못 지킨 아빠의 최후의 수단') → 공개(2.0 박스 목장) → 본문(아빠 입놀림·딸 진지) → 반전(11.3 당근 부스러기) → 끝(12.6~ '엄마도 빵 터짐 🤣'·'아빠들 화이팅!')",
 "narr_share": "0/11 줄 — 나레 없음(agy 귀 video_A·video_B·video_D '나레 없음 · 자막은 소리로 안 읽음' · video_C 받아쓰기 빈 답)",
 "notes": [
  "두 자막 층: 아래 해설(흰 BMJUA·검정 테 8px, 창 아래쪽 y≈1215/1262) + 위 말풍선(인물 속마음·추임새, 검정 상자 색 글 또는 흰 테 파랑, 기울기)",
  "효과음: 미측정",
  "BGM: 미측정 — agy 귀 없음 · 받아쓰기 빈 답(-15.1 LUFS)",
  "끝 꼴: 해설 '~네요' 감상 + 하트(얼굴 가림)·이모지"
 ],
 "name_evidence": [],
 "_made_by": "클로드 눈 판독(11-06) + 뜯기 기계값",
 "frame0": {
  "what": "원본 첫 장면(표지 카드 없음) + 틀 제목",
  "face_frac": null,
  "text": "",
  "frame_text": "약속 못 지킨 아빠가 / 딸을 위해 선택한 기막힌 방법 ㅋㅋㅋ",
  "basis": "1초 시트 0초 칸(눈)"
 },
 "sound": {
  "bgm": "미측정 — agy 귀 없음 · 받아쓰기 빈 답(-15.1 LUFS)",
  "sfx": null,
  "narration": "없음"
 },
 "lines": [
  {"t0": 0.0, "t1": 1.0, "speaker": "원음", "text": "약속을 못 지킨 아빠의", "layer": "스냅봤니·해설", "role": "훅", "enter": "instant", "y": [1216, 1275], "fill_hex": "#FFFFFF", "emph": [], "sticker": [], "sfx": null, "scene": "과정", "fit": 8, "cut_at": [], "words": [], "loud": [-27.4, -27.5, -23.4, -26.7], "font": {"name": "BMJUA", "basis": "뜯기 fontmatch 합산 top1 BMJUA 0.48 · 크롭 c00 0.86 · c12 0.84(video_A) + 눈(둥근 굵은 고딕)"}, "size_px": 62, "_size_basis": "잉크 높이 56~60px(뜯기 glyph 줄높이) — 글꼴 크기는 눈 추정 ±3px", "x": 540, "align": "center", "max_w": 1014, "letter_gap_px": 0, "line_gap_px": null, "outline": {"px": 8, "hex": "#000000"}, "ring": null, "shadow": null, "glow": null, "box": null, "enter_ms": 0, "enter_curve": [[0.0, 100, 100, 0]], "type_cps": null, "cursor": false, "exit": "instant — 다음 줄 앞 0.1~0.5초 빈 화면(0.1초 띠 video_A 4.8~5.0)", "variant": "기본(흰 글·검정 테)", "scene_desc": "원본 한 장면 — 해설이 말하는 동작이 그 컷에 보임(1초 시트 눈)", "transition": "none", "motion": "cam", "confidence": "픽셀", "notes": "시각·글 = 뜯기 OCR(기계) · y·획·글꼴 = 뜯기 glyph/fontmatch(픽셀) · 역할·장면·fit = 눈 · 효과음 = agy 귀", "_src": "뜯기 OCR(기계값 — 눈으로 확인)"},
  {"t0": 1.0, "t1": 2.0, "speaker": "원음", "text": "최후의 수단이라는데", "layer": "스냅봤니·해설", "role": "다리", "enter": "instant", "y": [1215, 1274], "fill_hex": "#FFFFFF", "emph": [], "sticker": [], "sfx": null, "scene": "과정", "fit": 8, "cut_at": [], "words": [], "loud": [-7.2, -11.9, -17.7, -19.4], "font": {"name": "BMJUA", "basis": "뜯기 fontmatch 합산 top1 BMJUA 0.48 · 크롭 c00 0.86 · c12 0.84(video_A) + 눈(둥근 굵은 고딕)"}, "size_px": 62, "_size_basis": "잉크 높이 56~60px(뜯기 glyph 줄높이) — 글꼴 크기는 눈 추정 ±3px", "x": 540, "align": "center", "max_w": 1014, "letter_gap_px": 0, "line_gap_px": null, "outline": {"px": 8, "hex": "#000000"}, "ring": null, "shadow": null, "glow": null, "box": null, "enter_ms": 0, "enter_curve": [[0.0, 100, 100, 0]], "type_cps": null, "cursor": false, "exit": "instant — 다음 줄 앞 0.1~0.5초 빈 화면(0.1초 띠 video_A 4.8~5.0)", "variant": "기본(흰 글·검정 테)", "scene_desc": "원본 한 장면 — 해설이 말하는 동작이 그 컷에 보임(1초 시트 눈)", "transition": "none", "motion": "cam", "confidence": "픽셀", "notes": "시각·글 = 뜯기 OCR(기계) · y·획·글꼴 = 뜯기 glyph/fontmatch(픽셀) · 역할·장면·fit = 눈 · 효과음 = agy 귀", "_src": "뜯기 OCR(기계값 — 눈으로 확인)"},
  {"t0": 2.0, "t1": 3.5, "speaker": "원음", "text": "박스로 만든 가성비 100% 목장 개장", "layer": "스냅봤니·해설", "role": "공개", "enter": "instant", "y": [1218, 1277], "fill_hex": "#FFFFFF", "emph": [], "sticker": [{"what": "굴러가는 눈 이모지", "x": 205, "y": 883, "w": 216, "t_in": 2.1, "t_out": 3.8, "anim": "instant", "basis": "뜯기 overlay_rules(Claude 0.1초 경계) + 1초 시트 눈"}], "sfx": null, "scene": "과정", "fit": 8, "cut_at": [2.67], "words": [], "loud": [-26.7, -26.7, -28.9, -22.4, -27.7, -17.0], "font": {"name": "BMJUA", "basis": "뜯기 fontmatch 합산 top1 BMJUA 0.48 · 크롭 c00 0.86 · c12 0.84(video_A) + 눈(둥근 굵은 고딕)"}, "size_px": 62, "_size_basis": "잉크 높이 56~60px(뜯기 glyph 줄높이) — 글꼴 크기는 눈 추정 ±3px", "x": 540, "align": "center", "max_w": 1014, "letter_gap_px": 0, "line_gap_px": null, "outline": {"px": 8, "hex": "#000000"}, "ring": null, "shadow": null, "glow": null, "box": null, "enter_ms": 0, "enter_curve": [[0.0, 100, 100, 0]], "type_cps": null, "cursor": false, "exit": "instant — 다음 줄 앞 0.1~0.5초 빈 화면(0.1초 띠 video_A 4.8~5.0)", "variant": "기본(흰 글·검정 테)", "scene_desc": "원본 한 장면 — 해설이 말하는 동작이 그 컷에 보임(1초 시트 눈)", "transition": "cut", "motion": "cam", "confidence": "픽셀", "notes": "시각·글 = 뜯기 OCR(기계) · y·획·글꼴 = 뜯기 glyph/fontmatch(픽셀) · 역할·장면·fit = 눈 · 효과음 = agy 귀", "_src": "뜯기 OCR(기계값 — 눈으로 확인)"},
  {"t0": 2.6, "t1": 4.8, "speaker": "원음", "text": "너 왜케 잘먹어 ㅋㅋ", "layer": "스냅봤니·말풍선", "role": "질문", "enter": "instant", "enter_ms": 0, "variant": "말풍선(흰 테)", "emph": [], "sticker": [], "sfx": null, "cut_at": [], "scene": "과정", "scene_desc": "인물 속마음·추임새(아기말투·감탄)를 인물 옆에", "fit": 8, "y": [537, 768], "x": 550, "fill_hex": "#3E8BFF", "font": {"name": "굵은 둥근 고딕(BMJUA 계열 추정)", "basis": "눈(1초 시트)"}, "size_px": 54, "box": null, "outline": {"px": 6, "hex": "#FFFFFF"}, "ring": null, "shadow": null, "glow": null, "rotate_deg": -5, "align": "left", "max_w": null, "letter_gap_px": 0, "line_gap_px": null, "enter_curve": [[0.0, 100, 100, 0]], "type_cps": null, "cursor": false, "exit": "instant", "transition": "none", "motion": "cam", "confidence": "신호", "notes": "시각 = 뜯기 overlay_rules 0.1초 경계 + 0.5초 위쪽 띠 눈 보정 · 기울기 약 -5°(눈) · 자리 = 인물 머리 옆(편마다 다름)"},
  {"t0": 3.5, "t1": 5.6, "speaker": "원음", "text": "메소드 연기 중인", "layer": "스냅봤니·해설", "role": "본문", "enter": "instant", "y": [1217, 1276], "fill_hex": "#FFFFFF", "emph": [], "sticker": [], "sfx": null, "scene": "과정", "fit": 8, "cut_at": [], "words": [], "loud": [-22.4, -22.7, -22.0, -20.8, -21.8, -23.6, -20.1, -23.5], "font": {"name": "BMJUA", "basis": "뜯기 fontmatch 합산 top1 BMJUA 0.48 · 크롭 c00 0.86 · c12 0.84(video_A) + 눈(둥근 굵은 고딕)"}, "size_px": 62, "_size_basis": "잉크 높이 56~60px(뜯기 glyph 줄높이) — 글꼴 크기는 눈 추정 ±3px", "x": 540, "align": "center", "max_w": 1014, "letter_gap_px": 0, "line_gap_px": null, "outline": {"px": 8, "hex": "#000000"}, "ring": null, "shadow": null, "glow": null, "box": null, "enter_ms": 0, "enter_curve": [[0.0, 100, 100, 0]], "type_cps": null, "cursor": false, "exit": "instant — 다음 줄 앞 0.1~0.5초 빈 화면(0.1초 띠 video_A 4.8~5.0)", "variant": "기본(흰 글·검정 테)", "scene_desc": "원본 한 장면 — 해설이 말하는 동작이 그 컷에 보임(1초 시트 눈)", "transition": "none", "motion": "cam", "confidence": "픽셀", "notes": "시각·글 = 뜯기 OCR(기계) · y·획·글꼴 = 뜯기 glyph/fontmatch(픽셀) · 역할·장면·fit = 눈 · 효과음 = agy 귀", "_src": "뜯기 OCR(기계값 — 눈으로 확인)"},
  {"t0": 5.6, "t1": 7.2, "speaker": "원음", "text": "아빠의 다급한 입놀림ㅋㅋㅋ", "layer": "스냅봤니·해설", "role": "본문", "enter": "instant", "y": [1215, 1274], "fill_hex": "#FFFFFF", "emph": [], "sticker": [], "sfx": null, "scene": "과정", "fit": 8, "cut_at": [], "words": [], "loud": [-22.9, -20.0, -19.6, -28.1, -23.4, -27.0], "font": {"name": "BMJUA", "basis": "뜯기 fontmatch 합산 top1 BMJUA 0.48 · 크롭 c00 0.86 · c12 0.84(video_A) + 눈(둥근 굵은 고딕)"}, "size_px": 62, "_size_basis": "잉크 높이 56~60px(뜯기 glyph 줄높이) — 글꼴 크기는 눈 추정 ±3px", "x": 540, "align": "center", "max_w": 1014, "letter_gap_px": 0, "line_gap_px": null, "outline": {"px": 8, "hex": "#000000"}, "ring": null, "shadow": null, "glow": null, "box": null, "enter_ms": 0, "enter_curve": [[0.0, 100, 100, 0]], "type_cps": null, "cursor": false, "exit": "instant — 다음 줄 앞 0.1~0.5초 빈 화면(0.1초 띠 video_A 4.8~5.0)", "variant": "기본(흰 글·검정 테)", "scene_desc": "원본 한 장면 — 해설이 말하는 동작이 그 컷에 보임(1초 시트 눈)", "transition": "none", "motion": "cam", "confidence": "픽셀", "notes": "시각·글 = 뜯기 OCR(기계) · y·획·글꼴 = 뜯기 glyph/fontmatch(픽셀) · 역할·장면·fit = 눈 · 효과음 = agy 귀", "_src": "뜯기 OCR(기계값 — 눈으로 확인)"},
  {"t0": 5.8, "t1": 7.2, "speaker": "원음", "text": "아~해 ㅋㅋ", "layer": "스냅봤니·말풍선", "role": "본문", "enter": "instant", "enter_ms": 0, "variant": "말풍선(흰 테)", "emph": [], "sticker": [], "sfx": null, "cut_at": [], "scene": "과정", "scene_desc": "인물 속마음·추임새(아기말투·감탄)를 인물 옆에", "fit": 8, "y": [710, 864], "x": 518, "fill_hex": "#3E8BFF", "font": {"name": "굵은 둥근 고딕(BMJUA 계열 추정)", "basis": "눈(1초 시트)"}, "size_px": 54, "box": null, "outline": {"px": 6, "hex": "#FFFFFF"}, "ring": null, "shadow": null, "glow": null, "rotate_deg": -5, "align": "left", "max_w": null, "letter_gap_px": 0, "line_gap_px": null, "enter_curve": [[0.0, 100, 100, 0]], "type_cps": null, "cursor": false, "exit": "instant", "transition": "none", "motion": "cam", "confidence": "신호", "notes": "시각 = 뜯기 overlay_rules 0.1초 경계 + 0.5초 위쪽 띠 눈 보정 · 기울기 약 -5°(눈) · 자리 = 인물 머리 옆(편마다 다름)"},
  {"t0": 7.9, "t1": 9.1, "speaker": "원음", "text": "세상에서 제일 진지한 딸 ㅋㅋㅋ", "layer": "스냅봤니·해설", "role": "본문", "enter": "instant", "y": [1215, 1274], "fill_hex": "#FFFFFF", "emph": [], "sticker": [], "sfx": null, "scene": "과정", "fit": 8, "cut_at": [], "words": [], "loud": [-24.0, -17.4, -21.2, -15.7, -14.1], "font": {"name": "BMJUA", "basis": "뜯기 fontmatch 합산 top1 BMJUA 0.48 · 크롭 c00 0.86 · c12 0.84(video_A) + 눈(둥근 굵은 고딕)"}, "size_px": 62, "_size_basis": "잉크 높이 56~60px(뜯기 glyph 줄높이) — 글꼴 크기는 눈 추정 ±3px", "x": 540, "align": "center", "max_w": 1014, "letter_gap_px": 0, "line_gap_px": null, "outline": {"px": 8, "hex": "#000000"}, "ring": null, "shadow": null, "glow": null, "box": null, "enter_ms": 0, "enter_curve": [[0.0, 100, 100, 0]], "type_cps": null, "cursor": false, "exit": "instant — 다음 줄 앞 0.1~0.5초 빈 화면(0.1초 띠 video_A 4.8~5.0)", "variant": "기본(흰 글·검정 테)", "scene_desc": "원본 한 장면 — 해설이 말하는 동작이 그 컷에 보임(1초 시트 눈)", "transition": "none", "motion": "cam", "confidence": "픽셀", "notes": "시각·글 = 뜯기 OCR(기계) · y·획·글꼴 = 뜯기 glyph/fontmatch(픽셀) · 역할·장면·fit = 눈 · 효과음 = agy 귀", "_src": "뜯기 OCR(기계값 — 눈으로 확인)"},
  {"t0": 8.5, "t1": 10.0, "speaker": "원음", "text": "하하하ㅋㅋ하하하 ㅋ", "layer": "스냅봤니·말풍선", "role": "고조", "enter": "instant", "enter_ms": 0, "variant": "말풍선(흰 테)", "emph": [], "sticker": [], "sfx": null, "cut_at": [], "scene": "과정", "scene_desc": "인물 속마음·추임새(아기말투·감탄)를 인물 옆에", "fit": 8, "y": [556, 691], "x": 588, "fill_hex": "#FF4FA3", "font": {"name": "굵은 둥근 고딕(BMJUA 계열 추정)", "basis": "눈(1초 시트)"}, "size_px": 54, "box": null, "outline": {"px": 6, "hex": "#FFFFFF"}, "ring": null, "shadow": null, "glow": null, "rotate_deg": -5, "align": "left", "max_w": null, "letter_gap_px": 0, "line_gap_px": null, "enter_curve": [[0.0, 100, 100, 0]], "type_cps": null, "cursor": false, "exit": "instant", "transition": "none", "motion": "cam", "confidence": "신호", "notes": "시각 = 뜯기 overlay_rules 0.1초 경계 + 0.5초 위쪽 띠 눈 보정 · 기울기 약 -5°(눈) · 자리 = 인물 머리 옆(편마다 다름)"},
  {"t0": 9.1, "t1": 10.8, "speaker": "원음", "text": "슬슬 입안 용량 초과가 되자 ㅋㅋㅋ", "layer": "스냅봤니·해설", "role": "고조", "enter": "instant", "y": [1209, 1268], "fill_hex": "#FFFFFF", "emph": [], "sticker": [], "sfx": null, "scene": "과정", "fit": 8, "cut_at": [], "words": [], "loud": [-15.1, -14.4, -23.4, -14.8, -23.7, -28.3, -25.8], "font": {"name": "BMJUA", "basis": "뜯기 fontmatch 합산 top1 BMJUA 0.48 · 크롭 c00 0.86 · c12 0.84(video_A) + 눈(둥근 굵은 고딕)"}, "size_px": 62, "_size_basis": "잉크 높이 56~60px(뜯기 glyph 줄높이) — 글꼴 크기는 눈 추정 ±3px", "x": 540, "align": "center", "max_w": 1014, "letter_gap_px": 0, "line_gap_px": null, "outline": {"px": 8, "hex": "#000000"}, "ring": null, "shadow": null, "glow": null, "box": null, "enter_ms": 0, "enter_curve": [[0.0, 100, 100, 0]], "type_cps": null, "cursor": false, "exit": "instant — 다음 줄 앞 0.1~0.5초 빈 화면(0.1초 띠 video_A 4.8~5.0)", "variant": "기본(흰 글·검정 테)", "scene_desc": "원본 한 장면 — 해설이 말하는 동작이 그 컷에 보임(1초 시트 눈)", "transition": "none", "motion": "cam", "confidence": "픽셀", "notes": "시각·글 = 뜯기 OCR(기계) · y·획·글꼴 = 뜯기 glyph/fontmatch(픽셀) · 역할·장면·fit = 눈 · 효과음 = agy 귀", "_src": "뜯기 OCR(기계값 — 눈으로 확인)"},
  {"t0": 11.0, "t1": 12.0, "speaker": "원음", "text": "풉ㅋㅋㅋㅋ", "layer": "스냅봤니·말풍선", "role": "반전", "enter": "instant", "enter_ms": 0, "variant": "말풍선(검정 상자)", "emph": [], "sticker": [], "sfx": null, "cut_at": [], "scene": "과정", "scene_desc": "인물 속마음·추임새(아기말투·감탄)를 인물 옆에", "fit": 8, "y": [710, 844], "x": 378, "fill_hex": "#FFE14A", "font": {"name": "굵은 둥근 고딕(BMJUA 계열 추정)", "basis": "눈(1초 시트)"}, "size_px": 54, "box": {"hex": "#000000", "alpha": 0.9, "pad": {"l": 14, "t": 6, "b": 6}, "radius": 8}, "outline": {"px": 0, "hex": null}, "ring": null, "shadow": null, "glow": null, "rotate_deg": -5, "align": "left", "max_w": null, "letter_gap_px": 0, "line_gap_px": null, "enter_curve": [[0.0, 100, 100, 0]], "type_cps": null, "cursor": false, "exit": "instant", "transition": "none", "motion": "cam", "confidence": "신호", "notes": "시각 = 뜯기 overlay_rules 0.1초 경계 + 0.5초 위쪽 띠 눈 보정 · 기울기 약 -5°(눈) · 자리 = 인물 머리 옆(편마다 다름)"},
  {"t0": 11.3, "t1": 12.6, "speaker": "원음", "text": "침대에 당근 부스러기 떨어지자 ㅋㅋㅋ", "layer": "스냅봤니·해설", "role": "반전", "enter": "instant", "y": [1216, 1275], "fill_hex": "#FFFFFF", "emph": [], "sticker": [], "sfx": null, "scene": "과정", "fit": 8, "cut_at": [], "words": [], "loud": [-14.4, -14.8, -16.1, -13.4, -17.3], "font": {"name": "BMJUA", "basis": "뜯기 fontmatch 합산 top1 BMJUA 0.48 · 크롭 c00 0.86 · c12 0.84(video_A) + 눈(둥근 굵은 고딕)"}, "size_px": 62, "_size_basis": "잉크 높이 56~60px(뜯기 glyph 줄높이) — 글꼴 크기는 눈 추정 ±3px", "x": 540, "align": "center", "max_w": 1014, "letter_gap_px": 0, "line_gap_px": null, "outline": {"px": 8, "hex": "#000000"}, "ring": null, "shadow": null, "glow": null, "box": null, "enter_ms": 0, "enter_curve": [[0.0, 100, 100, 0]], "type_cps": null, "cursor": false, "exit": "instant — 다음 줄 앞 0.1~0.5초 빈 화면(0.1초 띠 video_A 4.8~5.0)", "variant": "기본(흰 글·검정 테)", "scene_desc": "원본 한 장면 — 해설이 말하는 동작이 그 컷에 보임(1초 시트 눈)", "transition": "none", "motion": "cam", "confidence": "픽셀", "notes": "시각·글 = 뜯기 OCR(기계) · y·획·글꼴 = 뜯기 glyph/fontmatch(픽셀) · 역할·장면·fit = 눈 · 효과음 = agy 귀", "_src": "뜯기 OCR(기계값 — 눈으로 확인)"},
  {"t0": 12.6, "t1": 13.6, "speaker": "원음", "text": "아빠의 눈물겨운 열연에", "layer": "스냅봤니·해설", "role": "본문", "enter": "instant", "y": [1217, 1276], "fill_hex": "#FFFFFF", "emph": [], "sticker": [{"what": "흐린 분홍 하트(얼굴 가림)", "x": 270, "y": 960, "w": 151, "t_in": 13.2, "t_out": 15.5, "anim": "pulse", "basis": "뜯기 overlay_rules(Claude 0.1초 경계) + 1초 시트 눈"}], "sfx": null, "scene": "과정", "fit": 8, "cut_at": [], "words": [], "loud": [-13.8, -13.0, -19.5, -18.7], "font": {"name": "BMJUA", "basis": "뜯기 fontmatch 합산 top1 BMJUA 0.48 · 크롭 c00 0.86 · c12 0.84(video_A) + 눈(둥근 굵은 고딕)"}, "size_px": 62, "_size_basis": "잉크 높이 56~60px(뜯기 glyph 줄높이) — 글꼴 크기는 눈 추정 ±3px", "x": 540, "align": "center", "max_w": 1014, "letter_gap_px": 0, "line_gap_px": null, "outline": {"px": 8, "hex": "#000000"}, "ring": null, "shadow": null, "glow": null, "box": null, "enter_ms": 0, "enter_curve": [[0.0, 100, 100, 0]], "type_cps": null, "cursor": false, "exit": "instant — 다음 줄 앞 0.1~0.5초 빈 화면(0.1초 띠 video_A 4.8~5.0)", "variant": "기본(흰 글·검정 테)", "scene_desc": "원본 한 장면 — 해설이 말하는 동작이 그 컷에 보임(1초 시트 눈)", "transition": "none", "motion": "cam", "confidence": "픽셀", "notes": "시각·글 = 뜯기 OCR(기계) · y·획·글꼴 = 뜯기 glyph/fontmatch(픽셀) · 역할·장면·fit = 눈 · 효과음 = agy 귀", "_src": "뜯기 OCR(기계값 — 눈으로 확인)"},
  {"t0": 13.6, "t1": 14.7, "speaker": "원음", "text": "촬영하던 엄마도 결국 빵 터짐 🤣", "layer": "스냅봤니·해설", "role": "끝", "enter": "instant", "y": [1205, 1264], "fill_hex": "#FFFFFF", "emph": [], "sticker": [{"what": "🤣 이모지(자막 끝)", "x": 842, "y": 1536, "w": 65, "t_in": 13.7, "t_out": 14.7, "anim": "instant", "basis": "뜯기 overlay_rules(Claude 0.1초 경계) + 1초 시트 눈"}], "sfx": null, "scene": "과정", "fit": 8, "cut_at": [], "words": [], "loud": [-19.7, -23.4, -24.5, -21.4], "font": {"name": "BMJUA", "basis": "뜯기 fontmatch 합산 top1 BMJUA 0.48 · 크롭 c00 0.86 · c12 0.84(video_A) + 눈(둥근 굵은 고딕)"}, "size_px": 62, "_size_basis": "잉크 높이 56~60px(뜯기 glyph 줄높이) — 글꼴 크기는 눈 추정 ±3px", "x": 540, "align": "center", "max_w": 1014, "letter_gap_px": 0, "line_gap_px": null, "outline": {"px": 8, "hex": "#000000"}, "ring": null, "shadow": null, "glow": null, "box": null, "enter_ms": 0, "enter_curve": [[0.0, 100, 100, 0]], "type_cps": null, "cursor": false, "exit": "instant — 다음 줄 앞 0.1~0.5초 빈 화면(0.1초 띠 video_A 4.8~5.0)", "variant": "기본(흰 글·검정 테)", "scene_desc": "원본 한 장면 — 해설이 말하는 동작이 그 컷에 보임(1초 시트 눈)", "transition": "none", "motion": "cam", "confidence": "픽셀", "notes": "시각·글 = 뜯기 OCR(기계) · y·획·글꼴 = 뜯기 glyph/fontmatch(픽셀) · 역할·장면·fit = 눈 · 효과음 = agy 귀", "_src": "뜯기 OCR(기계값 — 눈으로 확인)"},
  {"t0": 14.7, "t1": 16.13, "speaker": "원음", "text": "오늘도 고생 많으신 아빠들 화이팅!", "layer": "스냅봤니·해설", "role": "끝", "enter": "instant", "y": [1217, 1276], "fill_hex": "#FFFFFF", "emph": [], "sticker": [], "sfx": null, "scene": "과정", "fit": 8, "cut_at": [15.43], "words": [], "loud": [-22.9, -18.8, -19.1, -21.1, -19.9, -21.5], "font": {"name": "BMJUA", "basis": "뜯기 fontmatch 합산 top1 BMJUA 0.48 · 크롭 c00 0.86 · c12 0.84(video_A) + 눈(둥근 굵은 고딕)"}, "size_px": 62, "_size_basis": "잉크 높이 56~60px(뜯기 glyph 줄높이) — 글꼴 크기는 눈 추정 ±3px", "x": 540, "align": "center", "max_w": 1014, "letter_gap_px": 0, "line_gap_px": null, "outline": {"px": 8, "hex": "#000000"}, "ring": null, "shadow": null, "glow": null, "box": null, "enter_ms": 0, "enter_curve": [[0.0, 100, 100, 0]], "type_cps": null, "cursor": false, "exit": "instant — 다음 줄 앞 0.1~0.5초 빈 화면(0.1초 띠 video_A 4.8~5.0)", "variant": "기본(흰 글·검정 테)", "scene_desc": "원본 한 장면 — 해설이 말하는 동작이 그 컷에 보임(1초 시트 눈)", "transition": "cut", "motion": "cam", "confidence": "픽셀", "notes": "시각·글 = 뜯기 OCR(기계) · y·획·글꼴 = 뜯기 glyph/fontmatch(픽셀) · 역할·장면·fit = 눈 · 효과음 = agy 귀", "_src": "뜯기 OCR(기계값 — 눈으로 확인)"}
 ]
}
```

(이 예시는 실제 파일 그대로이고, 보기 쉽게 줄 하나를 한 줄로 붙였다. 다른 3편 `video_A`·`video_B`·`video_D` 도 같은 꼴.)

**흔한 실수**
- 나레 없는 채널의 해설 줄 speaker — 지침서 어휘로는 `해설`. 스냅봤니 실제 산출은 `원음` 으로 적혀 있다(우리 쪽 어휘에 해설이 없던 때). 새로 쓸 때는 `해설`.
- transition 을 null 로 둠 — 전환이 없으면 'none'.
- 폴더 이름을 `줄판독/` 으로 — 폴더는 영문 `lines/`.
- words 열이 줄 글과 다른 소리(BGM 가사)를 받아 적은 것을 그대로 둠 — video_D 첫 줄 words '빨간 중독성을' 이 그 꼴. 나레 없는 편의 words 는 참고만.

#### 3-5. 스타일분석.md

**목적**: 11축마다 **실측 → 고른 규칙 → 신뢰도** 세 줄. 머리 글자는 아래 그대로(검사가 글자로 찾는다).

**칸**

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| # 제목 + 머리 줄 | 표본(편 id·조회·길이) · 뒷받침 파일 · 신뢰도 표기 · 표본부족 여부 | 글 | 필수 |  |
| ## 1 자막 … ## 11 채널 | 머리 11개: `## 1 자막` `## 2 제목·틀` `## 3 장면 전환` `## 4 장면↔대사` `## 5 스토리` `## 6 대본 언어` `## 7 소리` `## 8 스티커·짤` `## 9 썸네일·첫 화면` `## 10 소재` `## 11 채널` | 글자 그대로 | 필수 11개 |  |
| - 실측: | 잰 값과 [픽셀]/[신호]/[눈] 꼬리표 | 숫자 + 단위 + n | 축마다 필수 |  |
| - 고른 규칙: | 판에 넣은 것(규칙.json 요소 이름) | 글 | 축마다 필수 |  |
| - 신뢰도: | 픽셀/눈/신호/미측정 — 못 잰 것은 '안 잼 — 다음:' | 글 | 축마다 필수 |  |

**예시 전문(스냅봤니 실제)**

```markdown
# 스냅봤니 스타일분석 — 1차 프리셋 뒷받침 (2026-11-06)

- 표본: 하루당 조회 상위 4편 — video_A(1,300만·34.0초) · video_B(890만·37.6초) · video_C(1,000만·16.1초) · video_D(600만·16.4초)
- 뒷받침: lines/<id>.json(검사 오류 0, 93개 줄 = 해설 60 + 말풍선·괄호 33) · 규칙.json · 팔레트.json
- 신뢰도: [픽셀] 프로그램 실측 · [신호] 기계 판독 · [눈] 클로드가 시트·띠를 보고 · [미측정] 못 잼
- 표본 4편 < 5 → 편 단위 규칙은 전부 표본부족

## 1 자막
- 실측: 해설 BMJUA(글꼴 대조 1위, 크롭 0.86/0.84) · 잉크 높이 56~60px · #FFFFFF 60/60개 줄 · 검정 외곽선 8.0px · 상자·그림자 없음 · 가운데 x540 · 잉크 위 y1215(가로 원본 편) / y1256~1263(세로 원본 편) · 최대 폭 1014 [픽셀]. 말풍선 = 검정 둥근 상자 + 색 글 26/33, 흰 테 + 색 글 7/33 · 기울기 중앙 +4.7° [신호]. 등장 instant 93/93 · 표시 초 중앙 1.3~1.9 · 떠 있는 동안 움직임 0 [픽셀]. 강조 낱말 1/93 [픽셀].
- 고른 규칙: 해설 = 컷인·꾸밈 없음(cap_enter 강) · 강조 넣지 않음(cap_emph 약 = 없음도 스타일) · 말풍선 층은 판설정 frame.bubble.
- 신뢰도: 해설 픽셀 · 말풍선 신호(팝·흔들림은 agy 이름뿐, 0.1초 띠로 확인한 것은 video_A 5.2 컷인 1건)

## 2 제목·틀
- 실측: 바탕 #FDFDFD · 왼쪽 위 로고 y193~317 x108~408 · 제목 1개 줄 #010001 잉크 y332~411 · 2개 줄 #FB39A7 y423~500 · 창 y517~524 에서 시작(가로 원본 높이 884~1009, 세로 원본 1399) [픽셀]. 제목 1개 줄 상황 8~11자 / 2개 줄 결론·반응 11~15자 + ㅋㅋㅋ.
- 고른 규칙: 틀은 판설정 frame 그대로, 로고 자리만 내 브랜드 그림.
- 신뢰도: 픽셀

## 3 장면 전환
- 실측: 컷 경계 11곳 전부 하드컷 [픽셀] · 컷 중앙 4.53·3.70·2.67·4.23초 → 3.97 · 첫 컷 0.83~11.2초 · 줌 p90 2.9~22.9 %/초(원본 카메라 흔들림·편집 줌 섞임).
- 고른 규칙: 하드컷만 · 원본 한 장면을 2.6~4.6초 토막으로 건너뛰기.
- 신뢰도: 픽셀(편 단위는 표본부족)

## 4 장면↔대사
- 실측: 해설이 말하는 동작이 그 컷에 보임 — fit 93개 줄 모두 8 [눈].
- 고른 규칙: 장면에 보이는 것·원본 말만 해설로.
- 신뢰도: 눈 — 93개 줄 같은 값이라 안 잼으로 본다 — 다음: 1초 시트 10칸을 보고 줄마다 다시 매겨 평균·7 미만 비율을 낸다

## 5 스토리
- 실측: 훅(상황) → 다리('~라는데') → 본문(행동을 2~3개 줄에 쪼개 이어 말하기) → 질문(video_A 13.8 · video_B 8.0) → 반전(video_A 18.5 · video_B 23.5 · video_C 11.3 · video_D 4.9) → 공개 → 끝(감상 '~네요'). 반전 자리 ÷ 길이 0.54·0.625·0.70·0.30 → 중앙 0.58 [눈]. CTA 0/4.
- 고른 규칙: 판설정 script.brief 1~3개 줄.
- 신뢰도: 눈 · 표본부족

## 6 대본 언어
- 실측: 해설 반말 서술 + 끝만 존댓말('~네요' 4/4) · 잇는 어미(~는데·~더니·~자·~고 등)로 끝나는 줄 37/60 [픽셀·정규식] · ㅋㅋㅋ 붙은 해설 줄 비율 편별 0.10·0.33·0.36·0.30 · 조각 자수 중앙 11.5~14 · p90 15~16 · 최대 18 [픽셀·OCR]. 말풍선 = 1인칭 속마음·추임새(아이는 아기말투 video_A 6/13).
- 고른 규칙: 첫 줄 장소·인물·상황을 열어 두고 둘째 줄 '~라는데 ㅋㅋㅋ' 로 받기(4/4) · 한 줄 11~14자.
- 신뢰도: 픽셀(어미·자수) · 눈(목소리 두 갈래)

## 7 소리
- 실측: 통합 LUFS/TP video_A −14.7/0.0 · video_B −7.7/+0.7 · video_C −15.1/−0.1 · video_D −12.3/−0.1 [픽셀]. 나레 0/4 · BGM 4/4(피지카토·실로폰 / 레트로 댄스 / 'Circle of Life' 풍 / 록) · 원본 현장음 3/4 [신호 agy]. 효과음 = agy 두 번 답이 서로 다름(video_D 0 ↔ 7).
- 고른 규칙: −14 LUFS · 나레 없음 · 내 곡 BGM 원음보다 5dB 아래 · 효과음 0발.
- 신뢰도: 음량 픽셀 · BGM 신호 · 효과음 안 잼 — 다음: 뜯기 효과음 후보 시각과 10ms RMS 파형 솟음이 같이 있는 것만 센다

## 8 스티커·짤
- 실측: 스티커 편당 1~5(빨간 원·흰 점선 원·눈알·당황 이모지 줄·반짝이·흐린 분홍 하트) · 스티커 붙은 줄 12/93 · 끝 흐린 하트 3/4 [신호] · 짤 0/4.
- 고른 규칙: 끝 하트는 넣어야 하지만 render.py 에 모양이 없다(규칙.json sticker × — 기능 만들 목록).
- 신뢰도: 신호 · 하트 크기·흐림은 안 잼 — 다음: 세 구간 프레임에서 분홍 덩어리 넓이·흐림 반경을 잰다

## 9 썸네일·첫 화면
- 실측: 0초 = 원본 첫 장면 + 틀 제목, 표지 카드 없음 4/4 [눈].
- 고른 규칙: 0초 = 원본 장면 그대로(카드 넣지 않음).
- 신뢰도: 눈 · 표본부족

## 10 소재
- 실측: 아이·가족·직장 회식·시장 상인 '일상 돌발 순간' + 반전/귀여움 · 제품 없음 · 원본 = 인스타 릴스(설명란 '원본 출처: @핸들' 40편 가운데 3편) [눈].
- 고른 규칙: 원 작가 본인 계정 릴스만 소재로(출처.md).
- 신뢰도: 눈

## 11 채널
- 실측: 구독 76,400 · 165편 · 조회 중앙 473,000 · 최대 22,000,000 · 구독 대비 중앙 6.19 [픽셀].
- 고른 규칙: 상위↔하위 편 차이는 안 잼 — 다음: 조회 상위 5편·하위 5편 줄판독을 같은 칸으로 견준다(업그레이드 단계)
- 신뢰도: 픽셀(조회 수) · 상위↔하위 차이는 미측정(위 고른 규칙 줄에 다음 잴 방법)
```

**흔한 실수**
- 절을 채널 흐름대로(훅·스토리·말꼴…) 자유롭게 나눔 — 우리 첫 산출이 그랬다(0~8절). 저장 때 11축 머리로 옮긴다.
- '안 잼' 만 적고 다음 잴 방법을 안 씀.
- 표본부족을 숨기고 '4/4 = 규칙'으로 단정.

#### 3-6. 팔레트.json

**목적**: 층별로 쓰인 색 목록 — 어느 색이 몇 편·몇 줄에 나왔나.

**칸**

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| n_docs | 센 편 수 | 정수 | 필수 | 4 |
| roles | 층 이름 → 색 목록(본문·강조·외곽선·글로우·제목·스티커·출처) | 사전 | 필수 |  |
| roles.<층>[].hex | 색 | #RRGGBB | 필수 | #FFE14A |
| roles.<층>[].n_lines · n_docs · docs · members | 줄 수 · 편 수 · 편 id · 한 색으로 묶인 비슷한 색 | 정수 · 목록 | 필수(hex·n_docs) · 나머지 선택 | 11 · 4 |

**예시 전문(스냅봤니 실제)**

```json
{
 "n_docs": 4,
 "roles": {
  "본문": [
   {
    "hex": "#FFFFFF",
    "n_lines": 60,
    "n_docs": 4,
    "docs": [
     "video_C",
     "video_B",
     "video_A",
     "video_D"
    ],
    "members": [
     "#FFFFFF"
    ]
   },
   {
    "hex": "#FFE14A",
    "n_lines": 11,
    "n_docs": 4,
    "docs": [
     "video_C",
     "video_B",
     "video_A",
     "video_D"
    ],
    "members": [
     "#FFE14A"
    ]
   },
   {
    "hex": "#39E85A",
    "n_lines": 10,
    "n_docs": 2,
    "docs": [
     "video_B",
     "video_A"
    ],
    "members": [
     "#39E85A"
    ]
   },
   {
    "hex": "#FF4FA3",
    "n_lines": 8,
    "n_docs": 4,
    "docs": [
     "video_C",
     "video_B",
     "video_A",
     "video_D"
    ],
    "members": [
     "#FF4FA3"
    ]
   },
   {
    "hex": "#3E8BFF",
    "n_lines": 3,
    "n_docs": 2,
    "docs": [
     "video_C",
     "video_A"
    ],
    "members": [
     "#3E8BFF"
    ]
   },
   {
    "hex": "#7FD8FF",
    "n_lines": 1,
    "n_docs": 1,
    "docs": [
     "video_D"
    ],
    "members": [
     "#7FD8FF"
    ]
   }
  ],
  "강조": [
   {
    "hex": "#FF3FA4",
    "n_lines": 1,
    "n_docs": 1,
    "docs": [
     "video_B"
    ],
    "members": [
     "#FF3FA4"
    ]
   }
  ],
  "외곽선": [
   {
    "hex": "#000000",
    "n_lines": 60,
    "n_docs": 4,
    "docs": [
     "video_C",
     "video_B",
     "video_A",
     "video_D"
    ],
    "members": [
     "#000000"
    ]
   },
   {
    "hex": "#FFFFFF",
    "n_lines": 7,
    "n_docs": 4,
    "docs": [
     "video_C",
     "video_B",
     "video_A",
     "video_D"
    ],
    "members": [
     "#FFFFFF"
    ]
   }
  ],
  "글로우": [],
  "제목": [],
  "스티커": [],
  "출처": []
 }
}
```

**흔한 실수**
- 눈으로 본 색과 픽셀 중앙 색이 다를 때 그림 쪽(판설정 frame.bubble.colors) 값과 섞음 — 팔레트는 줄판독 fill_hex 를 센 표, 판설정은 그림에서 잰 값. 어느 쪽인지 _from 에 적는다.
- 빈 층을 지움 — 빈 층은 [] 로 남긴다(없음도 정보).

#### 3-7. 재현일치도.md

**목적**: 벤치 n편 중앙과 우리 시험편 1편을 같은 재는 법으로 견준 표. 1절 = 줄 단위 표, 2절 = 픽셀 표(framecmp 뒷받침).

**칸**

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| 머리 줄 | 재는 법 · 비교 시트 경로(sample/compare_sheet.png) · 판정 기호 · 합계 | 글 | 필수 |  |
| ## 1. 줄 단위 표 | 열: 칸 · 뜻 · 벤치 · 우리 · 차 · 판정 · 갈래 · 합격선 | 8열 | 필수 |  |
| 기준 칸 18개 | len.duration · cut.median · speech.cps.나레 · chunk.chars · chunk.sec · enter.mode.나레 · enter.mode.원음 · fx.rate.나레 · fx.rate.원음 · fx.pos · plain.rate · transition.rate · sfx.rate · sticker.rate · meme.rate · thumb.frame0 · mix.lufs · framecmp | 칸 이름 그대로 | 필수 18개 줄 |  |
| 채널 고유 칸 | 벤치에만 있는 층을 재는 칸(예 bubble.rate) | 갈래 = 기준 | 그 층이 있으면 필수 | bubble.rate |
| 참고 칸 | narr.share · speech.cps.asr · speech.gap · first.land · end.form · time.share · sync.ms | 갈래 = 참고 | 선택 |  |
| 판정 | ○ / × / 안 잼 / 해당 없음 — 안 잼이면 같은 줄 앞 칸에 '안 잼 — 다음: 잴 방법' | 넷 중 하나 | 필수 | ○ |
| 합격선 | 지침서 §5 숫자 | 글 | 필수 | ±15% |
| ## 2. 픽셀 표 | 열: 묶음 · 칸 · 벤치 · 우리 · 차 · 합격선 · 안/밖 | 7열 | 필수(framecmp 뒷받침) |  |

**예시 전문(스냅봤니 실제)**

```markdown
# 재현일치도 — 스냅봤니판 1차 시험편(sample/final.mp4 24.6초) vs 벤치 4편 중앙 — **미달**

- 재는 법 = match.py(벤치 4편·시험편 1편에 똑같은 함수) · 비교 시트 = sample/compare_sheet.png
- 판정 기호: ○ 합격 · × 불합격 · 안 잼(— 다음: 잴 방법) · 해당 없음(벤치에 그 갈래가 아예 없고 우리도 없음 = ○로 셈)
- 합계(기준 + 채널 고유): 19칸 중 ○ 15 · × 1 · 미측정 3 → 미달

## 1. 줄 단위 표

| 칸 | 뜻 | 벤치 | 우리 | 차 | 판정 | 갈래 | 합격선 |
|---|---|---|---|---|---|---|---|
| len.duration | 영상 길이(초) | 25.18 | 24.6 | −2.3% | ○ | 기준 | ±15% 또는 벤치 최소~최대 안 |
| cut.median | 컷 길이 중앙(초, 영상 창만) | 3.97 | 3.8 | −4.2% | ○ | 기준 | +30% / −15% |
| speech.cps.나레 | 나레 글자/표시 초 | 없음 | 없음 | — | 해당 없음 | 기준 | ±10% |
| chunk.chars | 자막 조각 자수 중앙 | 10.5 | 10.0 | −4.8% | ○ | 기준 | ±15% |
| chunk.sec | 자막당 표시 초 중앙 | 1.43 | 1.3 | −8.77% | ○ | 기준 | ±15% |
| enter.mode.나레 | 나레 줄 등장 최빈 | 없음 | 없음 | — | 해당 없음 | 기준 | 같음 |
| enter.mode.원음 | 원음 줄 등장 최빈 | instant | instant | 같음 | ○ | 기준 | 같음 |
| fx.rate.나레 | 나레 줄 중 꾸밈 붙은 비율 | 없음 | 없음 | — | 해당 없음 | 기준 | ±20%p |
| fx.rate.원음 | 원음 줄 중 꾸밈 붙은 비율 | 0.167 | 0.0 | −16.7%p | ○ | 기준 | ±20%p |
| fx.pos | 꾸밈 붙은 줄 자리(훅/본문/끝) | 훅 0.17 · 본문 0.42 · 끝 0.29 | 안 잼 — 다음: 우리 자막표 줄마다 꾸밈 자리를 적고 다시 센다 | — | 안 잼 | 기준 | 칸마다 ±20%p |
| plain.rate | 꾸밈 없는 줄 비율 | 0.834 | 1.0 | +16.6%p | ○ | 기준 | ±20%p |
| transition.rate | 전환 종류 분포 | cut 1.0 | 안 잼 — 다음: 우리 final.mp4 영상 창 컷 경계를 0.1초 띠로 보고 종류를 센다 | — | 안 잼 | 기준 | 칸마다 ±20%p |
| sfx.rate | 효과음 발/초 | 0.0 | 0.0 | 0 | ○ | 기준 | ±30%, 벤치 0이면 우리도 0 |
| sticker.rate | 스티커 붙은 줄 비율 | 0.124 | 0.0 | −12.3%p | ○ | 기준 | ±20%p |
| meme.rate | 짤 화면 줄 비율 | 0.0 | 0.0 | 0 | ○ | 기준 | ±20%p |
| thumb.frame0 | 0초 첫 화면 종류(card/scene) | scene | 안 잼 — 다음: 우리 final.mp4 0초 프레임을 뽑아 card/scene 을 가른다 | — | 안 잼 | 기준 | 벤치 최빈과 같음 |
| mix.lufs | 통합 LUFS | −13.5 | −13.9 | — | ○ | 기준 | −14±1(벤치와 견주지 않음) |
| framecmp | 틀·자막 좌표·색(아래 2절 픽셀 표) | 27칸 | 안 18칸 | 밖 9칸 | × | 기준 | ±4px · ±2px · ΔE<5 |
| bubble.rate | 말풍선 줄 비율(채널 고유 칸) | 0.334 | 0.269 | −6.5%p | ○ | 기준 | ±20%p |
| narr.share | 나레 줄 비율 | 0.0 | 0.0 | 범위 안 | ○ | 참고 | 벤치 범위 |
| speech.cps.asr | 말 구간 음절/초 | 4.24 | 7.59 | +79% | × | 참고 | ±10% |
| speech.gap | 1.5초 넘는 말 빈틈 수 | 1 | 0 | −100% | × | 참고 | ±50% |
| first.land | 첫 문장 끝 시각(초) | 2.51 | 7.1 | +4.59초 | × | 참고 | ±1초 |
| end.form | 끝맺음 꼴 | 없음 | 감상 | 다름 | × | 참고 | 벤치 최빈 — 벤치 '없음'은 받아쓰기 기준(나레 없음), 해설 자막으로 보면 감상 4/4(스타일분석 5) |
| time.share | 0.1초 격자 시간 갈래 비율 | 안 잼 — 다음: 벤치·우리 둘 다 0.1초 격자로 나레/원음/무음을 가른다 | 안 잼 — 다음: 같음 | — | 안 잼 | 참고 | ±10%p |
| sync.ms | 자막 시작 − 목소리 시작 | 없음 | 없음 | — | 해당 없음 | 참고 | 중앙 ±100ms |

## 2. 픽셀 표(같은 프레임 띠 — framecmp 판정 뒷받침, 벤치 video_D vs 우리)

| 묶음 | 칸 | 벤치 | 우리 | 차 | 합격선 | 안/밖 |
|---|---|---|---|---|---|---|
| 틀 | 영상 창 [x,y,w,h] | [0, 521, 1080, 1399] | [0, 521, 1080, 1399] | 0 | 영상 창 x,y,w,h 차 ≤ 4px | 안 |
| 틀 | 배경 RGB | [253, 253, 253] | [251, 251, 251] | 2 | 배경 RGB 채널 최대차 ≤ 8 | 안 |
| 틀 | 자막 자리 | inside | inside | 같음 | 자막 자리(위/아래/안) 같음 | 안 |
| 틀 | 자막 잉크 극성 | bright | bright | 같음 | 자막 잉크 극성 같음 | 안 |
| 틀 | 자막 띠 [y0,y1) | [1263, 1319] | [1258, 1308] | 11 | 자막 띠 y0,y1 차 ≤ 4px (틀 좌표 기준 §6-1) | **밖** |
| 틀 | 창 위 고정 띠 [[y0,y1)…] | [[194, 318], [328, 407], [417, 496]] | [[24, 67], [195, 316], [332, 412], [423, 504]] | 다름 | 참고(설계에 기준 수치 없음) | 참고 |
| 틀 | 띠 색 | - | - | - | 참고(설계에 기준 수치 없음) | 참고(failed:원본: bench에 띠 색을 재는 자가 없음(layout은 창 밖 배경 RGB만 잰다) / 우리: bench에 띠 색을 재는 자가 없음(layout은 창 밖 배경 RGB만 잰다)) |
| 틀 | 창 위 고정 글자 띠 개수 | 3 | 4 | 다름 | 창 위 고정 글자 띠 개수 같음 | **밖** |
| 틀 | 제목 블록 아래 끝~창 위 끝(px) | 27 | 110 | 83 | 제목 블록 아래 끝~창 위 끝 간격 차 ≤ 8px | **밖** |
| 틀 | 창 위 띠1 [194,318) 글 높이(px) | 124 | 121 | -3.0 (2.4%) | 띠 글 높이 차 ≤ 6% | 안 |
| 틀 | 창 위 띠1 [194,318) 획 두께(px) | 5 | 6 | 1 | 띠 획 두께 차 ≤ 1px | 안 |
| 틀 | 창 위 띠1 [194,318) 잉크 비율 | 0.04529 | 0.0611 | 0.016 (34.9%) | 띠 잉크 비율 차 ≤ 20% | **밖** |
| 틀 | 창 위 띠2 [328,407) 글 높이(px) | 79 | 80 | 1.0 (1.3%) | 띠 글 높이 차 ≤ 6% | 안 |
| 틀 | 창 위 띠2 [328,407) 획 두께(px) | 12 | 13 | 1 | 띠 획 두께 차 ≤ 1px | 안 |
| 틀 | 창 위 띠2 [328,407) 잉크 비율 | 0.36006 | 0.36669 | 0.007 (1.8%) | 띠 잉크 비율 차 ≤ 20% | 안 |
| 틀 | 창 위 띠3 [417,496) 글 높이(px) | 76 | - | - | 띠 글 높이 차 ≤ 6% | failed:우리: glyph_style 이 이 띠에서 글자를 못 찾음 |
| 틀 | 창 위 띠3 [417,496) 획 두께(px) | 1 | - | - | 띠 획 두께 차 ≤ 1px | failed:우리: glyph_style 이 이 띠에서 글자를 못 찾음 |
| 틀 | 창 위 띠3 [417,496) 잉크 비율 | 0.03198 | 0 | -0.032 (100.0%) | 띠 잉크 비율 차 ≤ 20% | **밖** |
| 자막 | 첫 줄 y 중앙(px) | 1261 | 1254 | -7.0px (0.4% of H1920) | 첫 줄 y 중앙 차 ≤ 화면 높이의 6% | 안 |
| 자막 | 줄 수 중앙 | 1 | 1 | 같음 | 줄 수(중앙) 같음 | 안 |
| 자막 | 줄 폭 중앙(px) | 810 | 567 | -243.0 (30.0%) | 줄 폭 중앙 차 ≤ 6% | **밖** |
| 자막 | 첫 줄 높이 중앙(px) | 56.5 | 55 | -1.5 (2.7%) | 첫 줄 높이 중앙 차 ≤ 6% | 안 |
| 자막 | 획 두께 중앙(px) | 7 | 7 | 0 | 획 두께 중앙 차 ≤ 1px | 안 |
| 자막 | 외곽선 있음(다수) | 있음 | 있음 | 같음 | 외곽선 유무(다수) 같음 — bench는 굵기 px를 안 재고 유무만 잰다 | 안 |
| 자막 | 그림자 있음(다수) | 없음 | 없음 | 같음 | 참고(설계에 기준 수치 없음) | 참고 |
| 자막 | 등장효과(최빈) | 없음 | 없음 | 같음 | 등장효과 종류(최빈) 같음 | 안 |
| 자막 | 자막당 초 중앙 | 1.25 | 1.3 | 0.05 (4.0%) | 자막당 초 중앙 차 ≤ 15% | 안 |
| 자막 | 자막 개수 | 12 | 19 | 7 | 참고(설계에 기준 수치 없음) | 참고 |
| 컷 | 컷 길이 중앙(초) | 4.234 | 3.8 | -0.434 (10.3%) | 참고(컷 중앙 판정 = 1절 cut.median 한 줄) | 안 |
| 컷 | 컷 길이 p90(초) | 9.807 | 8.12 | -1.687 (17.2%) | 컷 길이 p90 차 ≤ 15% | **밖** |
| 컷 | 첫 컷 시각(초) | 11.2 | 10.467 | -0.733 | 참고(설계에 기준 수치 없음) | 참고 |
| 컷 | 자막=컷 일치율(%) | 50 | 100 | 50 | 참고(설계에 기준 수치 없음) | 참고 |
| 컷 | 샷 수 | 3 | 5 | 2 | 참고(설계에 기준 수치 없음) | 참고 |
| 소리 | True Peak(dBTP) | -0.1 | -1.5 | -1.4 | 참고(설계에 기준 수치 없음) | 참고 |
| 길이 | 길이(초, 프레임÷fps) | 16.367 | 24.6 | 8.233 (50.3%) | 참고(길이 판정 = 1절 len.duration 한 줄) | **밖** |
```

**흔한 실수**
- 못 잰 칸을 ○ 로 셈 — 안 잼은 합격이 아니다(해당 없음만 ○로 센다).
- 도구가 준 None 을 그대로 둠 — 안 잼 + 다음 잴 방법으로.
- 카드.json match 숫자와 따로 셈 — 검사가 맞대 본다.
- 벤치에만 있는 층(말풍선)을 재는 칸이 없어 우리 쪽이 0으로 세짐 — 채널 고유 칸을 먼저 만든다(실패기록 7).

#### 3-8. 기본값.json

**목적**: 회원이 아무것도 안 바꿨을 때 쓰는 값 = 그 프리셋 원본 영상의 값. 회원이 바꾼 칸만 회원 값.

**칸**

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| voice | {provider, none} — 목소리 합성 서비스 · 나레 없음 |  | 필수 | none: true |
| speed | {tempo(배속), cps_target} | 배 · 자/초 | 필수 | cps_target 7.0 |
| bgm | {id, db_below_voice} | 곡 id · dB | 필수 | honwaka_puppu · 5.0 |
| caption | {mode, stack_lines} — 바꿔 끼움(replace)·쌓기 줄 수 | replace/stack · 정수 | 필수 | replace · 1 |
| <숫자칸>_from · none_from | 뒷받침 — 판설정 칸을 가리키면 된다 | 글 | 숫자마다 필수 |  |

**예시 전문(스냅봤니 실제)**

```json
{
 "_rule": "기본값 = 이 프리셋 원본 영상. 회원이 바꾼 칸만 회원 값",
 "voice": {
  "provider": null,
  "none": true,
  "none_from": "벤치 나레 0/4편(규칙.json speech)"
 },
 "speed": {
  "tempo": null,
  "tempo_from": "나레 없음 — 배속 없음",
  "cps_target": 7.0,
  "cps_target_from": "판설정.json cps_target 과 같음(해설 읽기 어림)"
 },
 "bgm": {
  "id": "honwaka_puppu",
  "id_from": "판설정.json bgm.id",
  "db_below_voice": 5.0,
  "db_below_voice_from": "판설정.json bgm.db_below_voice"
 },
 "caption": {
  "mode": "replace",
  "stack_lines": 1,
  "stack_lines_from": "해설 줄 수 중앙 1(픽셀 차이표 '줄 수 중앙' 벤치 1) — 쌓지 않고 바꿔 끼움"
 }
}
```

**흔한 실수**
- 판설정과 다른 값을 적음 — 같은 값을 두 곳에 다르게 두면 어긋난다. _from 에 판설정 칸을 가리킨다.
- 벤치 곡(남의 곡)을 bgm.id 로 — 내 곡 목록 이름만.

#### 3-9. 출처.md

**목적**: 쓴 영상마다 어디서 왔고, 원 작가 본인·공식 계정인지, 어떻게 확인했나.

**칸**

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| 표 열 5개 | 쓴 곳 · 주소 · 올린 계정 · 원 작가 본인·공식인가(예/아니오 + 쓰임) · 확인한 방법 | 주소는 http | 필수 |  |
| 벤치 편 줄 | 분석에만 쓴 편 — 본인 아님이면 '분석에만 씀, 화면은 안 씀' |  | 필수 |  |
| 소재 줄 | 시험편·다음 편 소재 — '예'(본인·공식)인 줄이 하나 이상 |  | 필수 |  |
| 주의 줄 | 판정이 틀렸던 것·미확정 | 글 | 있으면 필수 |  |

**예시 전문(스냅봤니 실제)**

```markdown
# 출처 — 스냅봤니판에 쓴 영상

| 쓴 곳 | 주소 | 올린 계정 | 원 작가 본인·공식인가 | 확인한 방법 |
|---|---|---|---|---|
| 벤치 분석 1 | https://www.youtube.com/shorts/video_A | @스냅봤니 | 아니오(재편집 채널) — 분석에만 씀, 화면은 안 씀 | 설명란에 원 작가 핸들 없음 |
| 벤치 분석 2 | https://www.youtube.com/shorts/video_B | @스냅봤니 | 아니오 — 분석에만 | 설명란 |
| 벤치 분석 3 | https://www.youtube.com/shorts/video_C | @스냅봤니 | 아니오 — 분석에만 | 설명란 |
| 벤치 분석 4 | https://www.youtube.com/shorts/video_D | @스냅봤니 | 아니오 — 분석에만 | 설명란 |
| 시험편 소재(남대문 스카프) | https://www.instagram.com/reel/reel_F/ | @glitter_esther | 예 — 원 작가 본인 계정 | 벤치 편 video_E 설명란 '원본 출처: @glitter_esther' → 그 계정 영상 목록 10편을 같은 영상 판정 · 원본 1초 시트와 벤치 1초 시트를 눈 대조 |

- 주의(실패기록.md 1): 시험편 소재는 원 작가 본인 계정이 맞지만 벤치 편의 원본이 아니라 **같은 가게의 다른 편(2탄)** 이었다. 여러 시각 프레임을 맞대어 보지 않고 한 장 판정을 믿었다.
- 설명란 출처 줄: '원본 출처: @glitter_esther (인스타그램)'
```

**흔한 실수**
- 썸네일 한 장만 보고 같은 편이라 판정 — 여러 시각 프레임 3곳 이상을 맞댄다(실패기록 1).
- 재편집 채널 영상을 소재로 — 원 작가 본인 계정을 찾고, 못 찾으면 그 편은 만들지 않는다.

#### 3-10. 제작순서.md

**목적**: 새 대화에서 **이 파일만 읽고** 다음 편을 처음부터 끝까지 만들 수 있게. 단계마다 도구·명령·만들어지는 파일·확인할 것.

**칸**

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| 머리 줄 | 명령을 어디서 치나(작업 폴더)·도구 폴더·판 파일 | 글 | 필수 |  |
| ## N. 단계 이름 | 5단계 이상 — 소재 · 받기(받아쓰기 포함) · 대본 · 재료 · 렌더 · 검증 · 회원 눈 판정 | ## 1. 꼴 | 필수 |  |
| - 도구 / - 명령 | 쓰는 도구·그대로 칠 명령 | 글 | 있으면 | python _tools/render.py presets/snapbwatni/판설정.json … |
| - 할 일 | 무엇을 하나(판설정 칸을 가리킨다) | 글 | 만들어지는 파일과 둘 중 하나 이상 |  |
| - 만들어지는 파일 | 그 단계가 남기는 파일 | 상대경로 |  | final.mp4 · 자막표.json |
| - 확인 | 다음 단계로 가기 전 볼 것 | 글 | 단계마다 필수 | −14 LUFS · 길이 16.1~37.6초 |

**예시 전문(스냅봤니 실제)**

```markdown
# 제작순서 — 스냅봤니판으로 다음 편 만들기 (새 대화에서 이 파일만 읽고 따라 한다)

> 모든 명령은 작업 폴더 copywork/ 에서 친다. 도구 = _tools/ · 판 = presets/snapbwatni/판설정.json · 편 폴더 = ch_snapbwatni/08_make/<편>(꼴 ep<NN>_<영문>_<MMDD_HHMM>, 예 ep02_market_1107_1030 — 규격서 1-4).

## 1. 소재 찾기
- 도구: 브라우저 + yt-dlp
- 할 일: 벤치 채널 최근 편 설명란의 원 출처 @핸들(지침서 §2-4-1)을 모은 뒤 그 계정 목록에서 '일상 돌발 순간'(아이·가족·직장·시장) 영상을 고른다. 원 작가 본인 계정 영상만. 이미 쓴 영상(출처.md)은 빼고, 핸들이 없으면 다음 40편 설명란.
- 만들어지는 파일: ch_snapbwatni/08_make/<편>/출처.md
- 확인: 출처.md 에 주소·계정·본인 계정인 뒷받침 한 줄 · 벤치 편과 같은 영상이라면 여러 시각 프레임 3곳 이상 맞대기

## 2. 원본 받기·받아쓰기
- 명령: `yt-dlp -o "ch_snapbwatni/08_make/<편>/src.mp4" <주소>` → `python _tools/asr.py ch_snapbwatni/08_make/<편>/src.mp4`
- 만들어지는 파일: src.mp4 · src.asr.json(낱말 시각)
- 확인: 높이 720 이상(판설정 source.min_h) · 받아쓰기가 비면 박힌 글(OCR)로 말 내용을 확인

## 3. 대본
- 할 일: 판설정 script.brief 4개 줄대로 — 나레 없음, 줄마다 원본 토막 2.6~4.6초 + 해설 11~14자. 둘째 줄 '~라는데 ㅋㅋㅋ', 끝 줄 '~네요'. 제목 2개 줄(검정 상황 / 분홍 반응 + ㅋㅋㅋ). 말풍선 = 10초당 약 3개, 인물 1인칭 속마음.
- 만들어지는 파일: 대본.json
- 확인: 받아쓰기·박힌 글에 없는 사실·금액 0(금지.md) · 금액이 들리는 토막은 뺀다

## 4. 재료 고르기(줄↔토막)
- 도구: `python _tools/sheet.py ch_snapbwatni/08_make/<편>/src.mp4 1` (1초 시트)
- 할 일: 줄마다 해설이 말하는 동작이 보이는 토막을 고르고 fit 0~10 을 매긴다. 말풍선 자리 = 인물 머리 옆, 얼굴을 가리지 않게.
- 만들어지는 파일: 재료.json
- 확인: 토막 사이 1초 넘게 건너뜀 · fit 7 미만 줄은 다른 토막

## 5. 렌더
- 명령: `python _tools/render.py presets/snapbwatni/판설정.json ch_snapbwatni/08_make/<편>`
- 만들어지는 파일: final.mp4 · 자막표.json · run_log.json
- 확인: −14 LUFS · 길이 16.1~37.6초 · 오른쪽 위 '광고' 표시(제품 연결이 있을 때) · 판설정 밖 값을 코드에 적지 않음

## 6. 검증
- 명령: `python _tools/match.py presets/snapbwatni/lines ch_snapbwatni/08_make/<편>` → `python _tools/watch_pack.py ch_snapbwatni/02_source/video_D.mp4 ch_snapbwatni/08_make/<편>/final.mp4 --out ch_snapbwatni/09_verify/`
- 만들어지는 파일: 재현일치도.md · 비교시트.png
- 확인: 기준 칸 전부 ○(미측정 0) — 아니면 판설정 칸을 고치고 5단계부터

## 7. 회원 눈 판정
- 할 일: final.mp4 와 비교시트.png 를 회원에게 보이고 '통과 / 여기가 다르다'를 받는다
- 확인: 다르다는 말은 규칙.json 또는 금지.md 한 줄로 남기고 5단계부터
```

**흔한 실수**
- '렌더한다' 한 줄로 끝냄 — 명령·파일·확인이 없으면 새 대화가 막힌다.
- 판설정 밖 값을 제작순서에 숫자로 또 적음 — 숫자는 판설정 한 곳, 여기선 칸을 가리킨다(같은 판단 두 곳 금지).

#### 3-11. 금지.md

**목적**: 이 채널에서 하면 안 되는 것 — 한 줄에 하나(`- ` 로 시작, 4개 줄 이상).

**칸**

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| 채널 이름·로고·징글·제목 문구 | 벤치 것 그대로 쓰기 금지 — 로고 자리는 내 브랜드 |  | 필수 |  |
| 출처 | 원 작가 본인·공식 계정이 아닌 영상 |  | 필수 |  |
| 사실·성분·효능·금액 | 확인 못 한 것 |  | 필수 |  |
| 광고 표시 | 협찬·판매 연결이 있으면 오른쪽 위 '광고' |  | 필수 |  |
| 채널 고유 | 이 채널에서 생긴 금지(회원 지적 포함) |  | 있으면 | 말풍선으로 얼굴 가리지 않기 |

**예시 전문(스냅봤니 실제)**

```markdown
# 금지 — 스냅봤니판

- 벤치 채널 이름·로고(개구리 그림 + 'Snap_This!/스냅봤니')·벤치 제목 문구를 그대로 쓰지 않는다 — 로고 자리는 assets/brand_band.png(내 브랜드)
- 벤치가 쓴 BGM 곡(남의 곡)을 쓰지 않는다 — 내 곡 목록에서 고른다
- 원 작가 본인·공식 계정이 아닌 영상(재편집 채널·벤치 편 화면)을 소재로 쓰지 않는다. 못 찾으면 그 편은 만들지 않는다
- 받아쓰기·박힌 글로 확인 못 한 사실·이름·금액을 해설에 쓰지 않는다 — 원음에 금액이 들리면 그 토막을 뺀다(실패기록.md 5)
- 협찬·판매 연결이 있는 편인데 오른쪽 위 '광고' 표시를 빠뜨리지 않는다
- 말풍선으로 인물 얼굴을 가리지 않는다(끝 하트만 벤치 꼴대로 얼굴 가림)
```

**흔한 실수**
- 일반 금지만 베껴 적고 이 채널 것(벤치 곡·로고 그림 이름)을 안 적음.

#### 3-12. 실패기록.md (깎기 내역)

**목적**: 결과물을 보고 고친 것(깎기)마다 네 줄. 다음 채널에서 같은 실수를 미리 막는 재료다. 틀린 것이 없었으면 `## 1. 없음` + 네 줄에 '없음'.

**칸**

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| ## N. 제목 | 한 건 한 절 | ## 1. 꼴 | 필수 |  |
| - 무엇이 | 무엇이 틀렸나(숫자·편 id·초) | 글 | 필수 |  |
| - 왜 | 왜 틀렸나(재지 않은 것·잘못 잰 것) | 글 | 필수 |  |
| - 어떻게 고쳤나 | 고친 칸·값 | 글 | 필수 |  |
| - 다시 안 나게 | 다음부터 지킬 규칙 한 줄 | 글 | 필수 |  |

**예시 전문(스냅봤니 실제)**

```markdown
# 실패기록(깎기 내역) — 스냅봤니판 1차: 결과물을 보고 고친 것

## 1. 소재 출처를 잘못 맞춤
- 무엇이: 벤치 편 원본이라고 고른 릴스가 같은 가게의 다른 편(2탄)이었다
- 왜: 출처 추적이 프레임 한 장을 여러 씨앗 프레임에 붙여 '같음'으로 판정했다(48쌍 중 1쌍 오판)
- 어떻게 고쳤나: 시험편은 원 작가 본인 계정 영상이라 그대로 두되 '벤치 원본 아님'을 출처.md 에 적었다
- 다시 안 나게: 같은 영상 판정은 여러 시각 프레임 3곳 이상을 맞대어 정한다. 확정 못 하면 '미확정'

## 2. 제목 글꼴이 획 두께에서 걸림
- 무엇이: 제목을 SBAggroB 로 그렸더니 획 15 vs 벤치 13, 폭 +23%
- 왜: 글꼴 대조 점수 1위만 믿고 같은 글을 같은 높이로 그려 견주지 않았다
- 어떻게 고쳤나: 후보 13개를 같은 글·잉크 높이 80px 로 그려 획·채움을 견줌 → Cafe24Ohsquare(획 14.0 vs 13.4)
- 다시 안 나게: 글꼴은 같은 글을 같은 잉크 높이로 그려 획·채움 두 값으로 고른다

## 3. 해설 자막이 16% 컸다
- 무엇이: 첫 렌더 자막 잉크 67px vs 벤치 56~60px
- 왜: 자막 꼴을 고를 때 잉크 높이를 재지 않았다
- 어떻게 고쳤나: 잉크 55px 꼴로 바꿈
- 다시 안 나게: 자막 꼴은 잉크 높이 ±6% 안인지 픽셀로 잰 뒤 고른다

## 4. 배경음이 작아 토막 경계마다 현장음이 끊겨 들림
- 무엇이: BGM 을 원음보다 10dB 아래로 두자 agy 귀 '배경음 작음·경계마다 툭 끊김'
- 왜: 벤치는 BGM 이 크게 깔려 경계를 덮는데(4/4), 그 크기를 재지 않고 나레형 기본값을 썼다
- 어떻게 고쳤나: 5dB 아래로 올림(판설정 bgm.db_below_voice)
- 다시 안 나게: BGM 크기는 벤치 BGM 구간과 원음 구간 음량 차로 정한다. 경계 페이드는 아직 렌더 도구 몫(남은 일)

## 5. 원음에 금액이 들어감
- 무엇이: 토막 O3·O6 원음에 '아홉 개 만 오천 원'·'여섯 개 만 원'
- 왜: 받아쓰기와 귀 판독이 갈린 구간을 그대로 썼다
- 어떻게 고쳤나: 두 토막 끝을 당겨 금액 말을 뺐다
- 다시 안 나게: 받아쓰기와 귀 판독이 갈린 구간은 쓰지 않는다(금지.md)

## 6. 말풍선 모서리 반지름을 잘못 잼
- 무엇이: 첫 기록 반지름 13
- 왜: 여백이 −125 = 글보다 작은 조각을 상자로 잡은 측정 실패였다. 넓이로 거꾸로 잰 값(32~54)도 글 구멍이 빠져 부풀었다
- 어떻게 고쳤나: 똑바른 상자 7개 네 모서리 윤곽을 원에 맞춤 → 14
- 다시 안 나게: 잰 값이 말이 되는지(여백 > 0, 상자 > 글) 먼저 거른다

## 7. 우리 말풍선이 0으로 세짐
- 무엇이: 말풍선 7개를 넣었는데 재현일치도가 0으로 셌다
- 왜: 재는 칸이 말풍선 층을 몰랐다
- 어떻게 고쳤나: bubble.rate 칸(채널 고유 칸)을 더함 → 0.269 vs 벤치 0.334
- 다시 안 나게: 벤치에만 있는 층이 있으면 재현일치도에 그 층 칸을 먼저 만든다
```

**흔한 실수**
- '고쳤다'만 적고 왜를 안 적음 — 다음 채널에서 같은 꼴을 못 막는다.
- 회원이 짚은 것을 빼먹음 — 회원 말은 전부 한 건씩.

#### 3-13. sample/ · assets/

**목적**: 완성 영상 견본과 그 그림들, 렌더가 읽는 그림(영문 이름).

**칸**

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| sample/final.mp4 | 따라 만든 시험편 완성본 | 1080×1920 | 필수 | 24.6초 |
| sample/sheet_1s.jpg | final.mp4 1초 간격 프레임 시트 | jpg | 필수 | 8×4 칸 |
| sample/thumb.jpg | 0초 프레임(썸네일 규칙 확인용) | jpg | 필수 |  |
| sample/compare_sheet.png | 벤치·우리 같은 상대 시각 비교 시트(재현일치도가 가리킨다) | png | 필수 |  |
| assets/ | 로고 자리 그림 등 — 판설정이 상대경로로 가리킨다 | 영문 이름 | 선택 | assets/brand_band.png |

**예시 전문(스냅봤니 실제)**

만드는 명령(예시 폴더에서 쓴 그대로):
```
ffmpeg -v error -y -ss 0 -i sample/final.mp4 -frames:v 1 -q:v 3 sample/thumb.jpg
ffmpeg -v error -y -i sample/final.mp4 -vf "fps=1,scale=216:-2,tile=8x4" -frames:v 1 -q:v 4 sample/sheet_1s.jpg
```

**흔한 실수**
- sample 안 파일 이름을 한글로 — ffmpeg 가 죽는다(1절).
- 견본 영상을 넣지 않고 경로만 적음.

---

### 4. 완료 단계 (카드.json `done.level` — 검사 도구가 계산해서 대조한다)

| 단계 | 이름 | 조건(전부) |
|---|---|---|
| 0 | 분석 덜 됨 | 아래 1단계 조건 중 하나라도 못 채움 |
| 1 | 분석됨 | 줄판독 6편 이상 · 줄판독 칸 오류 0 · 규칙.json 15종 · 스타일분석.md 11축 · 팔레트.json 꼴 |
| 2 | 판 있음 | 1단계 + 판설정.json 필수 칸 · 숫자 전부 `_from` · 규칙 미측정 줄 전부 measure_task |
| 3 | 1차 통과 | 2단계 + 재현일치도 기준 칸 × 0 · 안 잼 0 + 카드 `eye.member_pass: true`(회원 눈 판정 통과) |

- 3단계 밑이면 `done.missing`(남은 일)과 `done.next`(다음 할 일 한 줄)를 꼭 적는다.
- 저장은 단계와 상관없이 한다(0단계 프리셋도 저장 꼴이 맞으면 검사 통과). 단계는 "어디까지 왔나"를 숫자로 보이는 것이다.

---

### 5. 저장 검사 도구 `check_preset.py` (전문 — `copywork/_tools/check_preset.py` 로 그대로 저장)

- 표준 라이브러리만 쓴다(설치할 것 없음). 실행: `python _tools/check_preset.py presets/<슬러그>`
- 보는 것: 영문 폴더 이름 · 필수 파일 · json 유효 · 줄판독 칸·어휘 · 판설정 필수 칸·숫자마다 `_from` · 규칙 15종·등급 = k/n 계산·미측정엔 다음 잴 방법 · 스타일분석 11축 머리 · 팔레트 hex · 재현일치도 기준 칸 18개·판정 기호·비교 시트 · 기본값 `_from` · 출처·제작순서·실패기록·금지 꼴 · 내 PC 절대경로 0 · 모든 '안 잼' 에 '다음:' · 5편 밑 표본부족 표시 · 카드 숫자 = 재현일치도 표 숫자 · 완료 단계 계산 = 카드 `done.level`
- 결과: 표 출력. ✗ 가 하나라도 있으면 종료 코드 1. `--stage N` 을 주면 완료 단계가 N 밑일 때도 1.

```python
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
```

---

### 6. 스냅봤니 예시 폴더에 실제로 돌린 결과 (2026-11-06)

#### 6-1. 고치기 전 — 실제 산출을 규격 없이 모은 폴더(판설정 = why 꼴·절대경로, 규칙 = 빈도 표, 줄판독 폴더 한글, 7개 파일 없음)

```
프리셋 저장 검사: before\presets\snapbwatni
| 구역      | 결과 | 내용
|---------|------|------
| 폴더      |  ✗   | 규격서 1-2 나무에 없는 자리: ['줄판독'] — 먼저 규격서 표에 한 줄 더하고 만든다
| 폴더      |  ✗   | 폴더 이름에 한글: snapbwatni\줄판독 — 폴더는 영문(ffmpeg 가 한글 경로에서 죽는다)
| 파일      |  ✗   | 카드.json 없음
| 파일      |  ✗   | 기본값.json 없음
| 파일      |  ✗   | 출처.md 없음
| 파일      |  ✗   | 제작순서.md 없음
| 파일      |  ✗   | 금지.md 없음
| 파일      |  ✗   | 실패기록.md 없음
| 파일      |  ✗   | sample/final.mp4 없음
| 파일      |  ✗   | sample/sheet_1s.jpg 없음
| 파일      |  ✗   | sample/thumb.jpg 없음
| 파일      |  ✗   | sample/compare_sheet.png 없음
| 파일      |  ✗   | lines/<편>.json 없음(줄판독)
| 경로      |  ✗   | 스타일분석.md:4 로컬 절대경로 — 프리셋 폴더 기준 상대경로로
| 경로      |  ✗   | 스타일분석.md:9 로컬 절대경로 — 프리셋 폴더 기준 상대경로로
| 경로      |  ✗   | 스타일분석.md:29 로컬 절대경로 — 프리셋 폴더 기준 상대경로로
| 경로      |  ✗   | 재현일치도.md:34 로컬 절대경로 — 프리셋 폴더 기준 상대경로로
| 경로      |  ✗   | 판설정.json:6 로컬 절대경로 — 프리셋 폴더 기준 상대경로로
| 경로      |  ✗   | 로컬 절대경로 20곳(앞 5곳만 표시)
| 안 잼     |  ○   | 모든 '안 잼' 에 다음 잴 방법 있음
| 판설정     |  ✗   | _from 없는 숫자 54개: ['cps_target', 'bgm.db_below_voice', 'bgm.duck_orig_db', 'bgm.fade_out', 'loudness.lufs', 'loudness.tp'] …
| 규칙      |  ✗   | 요소 없음: ['cap_look', 'cap_enter', 'cap_emph', 'cap_exit', 'transition', 'cut_rhythm', 'scene_fit', 'bgm', 'sfx', 'meme', 'sticker', 'pointer', 'thumb', 'speech', 'script'] — 15종마다 한 줄 이상(없으면 '없음'도 규칙)
| 규칙      |  ✗   | 0번(None) 칸 없음: ['element', 'action', 'unit', 'evidence', 'confidence', 'engine_cell', 'engine_support', 'measure_task']
| 규칙      |  ✗   | 1번(None) 칸 없음: ['element', 'action', 'unit', 'evidence', 'confidence', 'engine_cell', 'engine_support', 'measure_task']
| 규칙      |  ✗   | 2번(None) 칸 없음: ['element', 'action', 'unit', 'evidence', 'confidence', 'engine_cell', 'engine_support', 'measure_task']
| 규칙      |  ✗   | 3번(None) 칸 없음: ['element', 'action', 'unit', 'evidence', 'confidence', 'engine_cell', 'engine_support', 'measure_task']
| 규칙      |  ✗   | 4번(None) 칸 없음: ['element', 'action', 'unit', 'evidence', 'confidence', 'engine_cell', 'engine_support', 'measure_task']
| 규칙      |  ✗   | 5번(None) 칸 없음: ['element', 'action', 'unit', 'evidence', 'confidence', 'engine_cell', 'engine_support', 'measure_task']
| 규칙      |  ✗   | 6번(None) 칸 없음: ['element', 'action', 'unit', 'evidence', 'confidence', 'engine_cell', 'engine_support', 'measure_task']
| 규칙      |  ✗   | 오류가 많아 나머지 98개 줄은 생략 — 15종 레코드 꼴(규격서 3-3)로 다시 쓴다
| 스타일분석   |  ✗   | 머리 없음: '## 1 자막'
| 스타일분석   |  ✗   | 머리 없음: '## 2 제목·틀'
| 스타일분석   |  ✗   | 머리 없음: '## 3 장면 전환'
| 스타일분석   |  ✗   | 머리 없음: '## 4 장면↔대사'
| 스타일분석   |  ✗   | 머리 없음: '## 5 스토리'
| 스타일분석   |  ✗   | 머리 없음: '## 6 대본 언어'
| 스타일분석   |  ✗   | 머리 없음: '## 7 소리'
| 스타일분석   |  ✗   | 머리 없음: '## 8 스티커·짤'
| 스타일분석   |  ✗   | 머리 없음: '## 9 썸네일·첫 화면'
| 스타일분석   |  ✗   | 머리 없음: '## 10 소재'
| 스타일분석   |  ✗   | 머리 없음: '## 11 채널'
| 팔레트     |  ○   | 층 7개 · hex 꼴
| 재현일치도   |  ✗   | 기준 칸 없음: ['len.duration', 'cut.median', 'speech.cps.나레', 'chunk.chars', 'chunk.sec', 'enter.mode.나레', 'enter.mode.원음', 'fx.rate.나레', 'fx.rate.원음', 'fx.pos', 'plain.rate', 'transition.rate', 'sfx.rate', 'sticker.rate', 'meme.rate', 'thumb.frame0', 'mix.lufs', 'framecmp']
| 재현일치도   |  ✗   | 비교 시트(sample/compare_sheet.png) 경로가 없다
| 표본      |  △   | 줄판독 0편 < 5 — 편 단위 규칙은 전부 표본부족
| 완료 단계   |  →   | 0 분석 덜 됨

오류 42 · 경고 1 · 완료 단계 0
판정: 실패 — ✗ 줄을 고친 뒤 다시 돌린다
```
종료 코드 1.

#### 6-2. 규격대로 저장한 폴더(이 문서 3절 예시가 그 파일들이다)

```
프리셋 저장 검사: after\presets\snapbwatni
| 구역      | 결과 | 내용
|---------|------|------
| 파일      |  ○   | 필수 파일 11개 + sample/ 4개 + lines/ 4편
| 경로      |  ○   | 로컬 절대경로 0
| 안 잼     |  ○   | 모든 '안 잼' 에 다음 잴 방법 있음
| 줄판독     |  ○   | 4편 칸 전부 있음
| 판설정     |  ○   | 숫자 칸 전부 _from 있음
| 규칙      |  ○   | 18개 레코드 · 15종 다 있음 · 등급 = k/n 계산과 같음
| 스타일분석   |  ○   | 11축 머리 · 축마다 실측/고른 규칙/신뢰도
| 팔레트     |  ○   | 층 7개 · hex 꼴
| 재현일치도   |  ○   | 기준 19칸: ○ 15 · × 1 · 안 잼 3
| 기본값     |  ○   | 목소리·빠르기·배경음·자막 쌓기 + _from
| 출처      |  ○   | 5개 줄
| 제작순서    |  ○   | 7단계
| 실패기록    |  ○   | 7건
| 금지      |  ○   | 금지 줄 6개
| 카드      |  ○   | 칸 · 11축 · 숫자 맞대기 · done.level 0 = 계산 0
| 표본      |  △   | 줄판독 4편 < 5 — 편 단위 규칙은 전부 표본부족
| 완료 단계   |  →   | 0 분석 덜 됨

오류 0 · 경고 1 · 완료 단계 0
판정: 통과
```
종료 코드 0. 저장 꼴은 통과, 완료 단계는 0(줄판독 4편 < 6) — 카드에 남은 일이 적혀 있다.

#### 6-3. 같은 폴더에 `--stage 1`

```
프리셋 저장 검사: after\presets\snapbwatni
| 구역      | 결과 | 내용
|---------|------|------
| 파일      |  ○   | 필수 파일 11개 + sample/ 4개 + lines/ 4편
| 경로      |  ○   | 로컬 절대경로 0
| 안 잼     |  ○   | 모든 '안 잼' 에 다음 잴 방법 있음
| 줄판독     |  ○   | 4편 칸 전부 있음
| 판설정     |  ○   | 숫자 칸 전부 _from 있음
| 규칙      |  ○   | 18개 레코드 · 15종 다 있음 · 등급 = k/n 계산과 같음
| 스타일분석   |  ○   | 11축 머리 · 축마다 실측/고른 규칙/신뢰도
| 팔레트     |  ○   | 층 7개 · hex 꼴
| 재현일치도   |  ○   | 기준 19칸: ○ 15 · × 1 · 안 잼 3
| 기본값     |  ○   | 목소리·빠르기·배경음·자막 쌓기 + _from
| 출처      |  ○   | 5개 줄
| 제작순서    |  ○   | 7단계
| 실패기록    |  ○   | 7건
| 금지      |  ○   | 금지 줄 6개
| 카드      |  ○   | 칸 · 11축 · 숫자 맞대기 · done.level 0 = 계산 0
| 표본      |  △   | 줄판독 4편 < 5 — 편 단위 규칙은 전부 표본부족
| 완료 단계   |  →   | 0 분석 덜 됨
| 완료 단계   |  ✗   | 요구 1 단계 밑

오류 1 · 경고 1 · 완료 단계 0
판정: 실패 — ✗ 줄을 고친 뒤 다시 돌린다
```
종료 코드 1(아직 1단계 밑).

#### 6-4. 작업 폴더 나무 검사 `--work` — 옛 꼴(CLAUDE.md · 한글 단계 폴더 · 한글 편 폴더 · 한글 저장 폴더) vs 1절 나무대로 (둘 다 스냅봤니 실제 파일)

고치기 전:
```
작업 폴더 검사: copywork
| 구역      | 결과 | 내용
|---------|------|------
| 시작      |  ✗   | guide.md 없음 — 첫 일로 저장(지침서 §1-1 1)
| 시작      |  ✗   | preset_spec.md 없음 — 첫 일로 저장(지침서 §1-1 1)
| 시작      |  ✗   | _tools/check_preset.py 없음 — 첫 일로 저장(지침서 §1-1 1)
| 폴더 이름   |  ✗   | 한글 폴더: copywork\프리셋 — 폴더는 영문(규격서 1-6)
| 폴더 이름   |  ✗   | 한글 폴더: copywork\ch_snapbwatni\01_선정 — 폴더는 영문(규격서 1-6)
| 폴더 이름   |  ✗   | 한글 폴더: copywork\ch_snapbwatni\02_원본 — 폴더는 영문(규격서 1-6)
| 폴더 이름   |  ✗   | 한글 폴더: copywork\ch_snapbwatni\03_뜯기 — 폴더는 영문(규격서 1-6)
| 폴더 이름   |  ✗   | 한글 폴더: copywork\ch_snapbwatni\05_줄판독 — 폴더는 영문(규격서 1-6)
| 폴더 이름   |  ✗   | 한글 폴더: copywork\ch_snapbwatni\06_규칙 — 폴더는 영문(규격서 1-6)
| 폴더 이름   |  ✗   | 한글 폴더: copywork\ch_snapbwatni\07_판 — 폴더는 영문(규격서 1-6)
| 폴더 이름   |  ✗   | 한글 폴더: copywork\ch_snapbwatni\08_제작 — 폴더는 영문(규격서 1-6)
| 폴더 이름   |  ✗   | 한글 폴더: copywork\ch_snapbwatni\09_검증 — 폴더는 영문(규격서 1-6)
| 폴더 이름   |  ✗   | 한글 폴더: copywork\ch_snapbwatni\10_적용 — 폴더는 영문(규격서 1-6)
| 폴더 이름   |  ✗   | 한글 폴더: copywork\프리셋\스냅봤니 — 폴더는 영문(규격서 1-6)
| 폴더 이름   |  ✗   | 한글 폴더: copywork\프리셋\스냅봤니\줄판독 — 폴더는 영문(규격서 1-6)
| 폴더 이름   |  ✗   | 한글 폴더: copywork\ch_snapbwatni\08_제작\남대문스카프 — 폴더는 영문(규격서 1-6)
| 나무      |  ✗   | 규격서 1-1 나무에 없는 자리: ['CLAUDE.md', '프리셋']
| 나무      |  ✗   | ch_snapbwatni/00_progress.md 없음
| 나무      |  ✗   | ch_snapbwatni/ 안 규격서 1-1 에 없는 자리: ['00_진행표.md', '01_선정', '02_원본', '03_뜯기', '05_줄판독', '06_규칙']

오류 19 · 경고 0
판정: 실패 — ✗ 줄을 고친 뒤 다시 돌린다
```
종료 코드 1.

1절 나무대로:
```
작업 폴더 검사: copywork
| 구역      | 결과 | 내용
|---------|------|------
| 작업 폴더   |  ○   | 규격서 1-1 나무 · 1-3 슬러그 · 1-4 이름 꼴 맞음(ch_ 1개)

오류 0 · 경고 0
판정: 통과
```
종료 코드 0.

- 이 문서를 만들며 검사가 실제로 잡은 것: 제작순서.md 에 '다음:' 없는 '안 잼'(판정 기호가 아닌 글) 1곳 → '미측정 0' 으로 고친 뒤 통과.

---

### 부록 A. 작업 폴더 파일 꼴 — `07_pan/판.json` · `03_tear/<id>/뜯기.json` · `08_make/<편>/대본.json` · `재료.json`

#### A-1. `07_pan/판.json`

판.json 과 판설정.json 은 **같은 칸·같은 값**이다(3-2 칸 표가 판.json 칸 표다). 다른 점은 하나 — 작업 중에는 `_from` 대신 묶음마다 `why` 한 줄도 허용하고, 저장 때 숫자마다 `_from` 으로 옮긴다. render.py 는 판.json(작업 중)·판설정.json(저장 뒤) 어느 것을 줘도 같은 칸을 읽는다.

#### A-2. `03_tear/<id>/뜯기.json` — 벤치 한 편을 기계로 잰 값(사람 판독 전)

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| engine · source · measured_at | 뜯기 도구 판 · 원본 경로(작업 폴더 상대) · 잰 때 | 글 | 필수 | 02_source/video_D.mp4 |
| probe | {w, h, fps, duration, has_audio} | px · fps · 초 | 필수 | 1080×1920 · 30 · 16.367 |
| layout | {window[x,y,w,h], bg_rgb, ink_polarity bright/dark, caption_pos inside/above/below, caption_band[y0,y1], above_bands[[y0,y1]…]} — window.py | px · RGB | 필수 | window [0,521,1080,1399] |
| captions | {n_spans, items[{i,t0,t1,lines,widths,top_y,text[],truncated}], glyph[{line_h,stroke,outline,outline_px,shadow}]} — ink.py + 글 후보(기계 OCR 은 후보일 뿐, 확정 글은 클로드가 프레임을 보고 — 지침서 §2-2-1 ⑤) | 초 · px | 필수 | n_spans 16 |
| caption_motion | {starts[{caption,t0,anim,curve[{t,bbox,ink}]}], ends[]} — 등장·퇴장 곡선 | 초 · px | 필수 | anim 없음 |
| fonts | {per_crop[{caption,text,top5[{font,score}]}], title, brand} — 글꼴 후보 | 점수 0~1 | 필수(실패면 failed 칸) |  |
| audio | {bench{I(LUFS),LRA,TP}, transcript{segments[{start,end,text,speaker}]}, composition} — loud.py · asr.py | LUFS · dBTP · 초 | 필수 | I −12.3 · TP −0.1 |
| cuts | {times[], shots, shot_len{median,p10,p90}, first_cut, cut_per_min} — cuts.py(영상 창만) | 초 | 필수 | median 4.23 |
| sfx_rules · bgm_rules · voice_rules | 효과음 발/초·개수 · BGM 있음·분위기 · 화자 수(agy 있으면 이름 보조) |  | 필수(못 재면 ok:false + 이유) | sfx 0 · bgm 있음 |
| materials | 컷마다 재료 갈래(원본 재편집·자체 촬영·그림…) |  | 선택 | 남의영상재편집 |
| overlay_rules | 꾸밈 후보 {appearances[{t0,t1,kind,box}]} — 스티커·짤이 나오는 구간(기계 후보, 확정은 줄판독) | 초 · px | 필수(지침서 §2-2 ①) | (스냅봤니 뜯기에는 이 칸 이름이 없다 — 꾸밈 후보는 caption_motion·layout 쪽에 섞여 있었다) |
| layout.intro_outro | 시작·끝 0.3초 안에 붙은 다른 틀(인트로·아웃트로) | 초 | 필수 | 있음/없음 |
| audio.phrase_loud | 구절 종류(나레·원음·BGM만)별 0.4초 음량 중앙 | LUFS | 필수(지침서 §2-2 ①) |  |

**예시(스냅봤니 video_D 실제 뜯기.json 발췌 — 전체 88KB 중 칸마다 앞부분)**

```json
{
 "engine": "뜯기 1판 2026-10-15",
 "source": "02_source/video_D.mp4",
 "measured_at": "2026-11-06 06:31",
 "probe": {
  "w": 1080,
  "h": 1920,
  "fps": 30.0,
  "duration": 16.367,
  "has_audio": true
 },
 "layout": {
  "window": [
   0,
   521,
   1080,
   1399
  ],
  "bg_rgb": [
   253,
   253,
   253
  ],
  "ink_polarity": "bright",
  "caption_pos": "inside",
  "caption_band": [
   1059,
   1319
  ],
  "above_bands": [
   [
    194,
    318
   ],
   [
    328,
    407
   ],
   [
    417,
    496
   ]
  ]
 },
 "captions": {
  "n_spans": 16,
  "items": [
   {
    "i": 0,
    "t0": 0.0,
    "t1": 1.1,
    "lines": 1,
    "widths": [
     856
    ],
    "top_y": 1263,
    "leading": null,
    "mark": true,
    "text": [
     "막내가 감기약 죽어도 안 먹겠다고"
    ],
    "truncated": true
   },
   {
    "i": 1,
    "t0": 1.6,
    "t1": 2.6,
    "lines": 1,
    "widths": [
     689
    ],
    "top_y": 1263,
    "leading": null,
    "mark": true,
    "text": [
     "온몸으로 버티는 중이라는데"
    ],
    "truncated": true
   }
  ],
  "glyph": [
   {
    "line_h": 56,
    "stroke": 8.0,
    "outline": true,
    "outline_px": 12,
    "shadow": null,
    "i": 0,
    "anim": "없음"
   }
  ]
 },
 "caption_motion": {
  "starts": [
   {
    "caption": 1,
    "t0": 1.6,
    "anim": "없음",
    "num": {
     "ms": 0,
     "kind": "instant",
     "steps": [
      {
       "t": 0.0,
       "w_pct": 100,
       "ink_pct": 97,
       "y": 1025
      },
      {
       "t": 0.1,
       "w_pct": 100,
       "ink_pct": 97,
       "y": 1026
      },
      {
       "t": 0.2,
       "w_pct": 104,
       "ink_pct": 98,
       "y": 1021
      },
      {
       "t": 0.3,
       "w_pct": 100,
       "ink_pct": 100,
       "y": 1027
      }
     ],
     "ref": "끝 프레임"
    }
   }
  ]
 },
 "audio": {
  "bench": {
   "I": -12.3,
   "LRA": 3.2,
   "TP": -0.1
  },
  "transcript": {
   "segments": [
    {
     "start": 0.14,
     "end": 2.51,
     "text": "빨간 중독성을 자랑하는 장난감",
     "speaker": "S?",
     "lang": "ko",
     "kind": "unknown"
    },
    {
     "start": 2.87,
     "end": 4.94,
     "text": "지금 이 느낌적인",
     "speaker": "S?",
     "lang": "ko",
     "kind": "unknown"
    }
   ]
  }
 },
 "cuts": {
  "times": [
   11.2,
   12.133
  ],
  "shots": 3,
  "shot_len": {
   "median": 4.23,
   "p10": 1.59,
   "p90": 9.81
  },
  "first_cut": 11.2,
  "cut_per_min": 7.3
 },
 "sfx_rules": {
  "per_sec": 0.0,
  "count": 0
 },
 "bgm_rules": {
  "present": true,
  "mood": [
   "경쾌",
   "신나는",
   "코믹"
  ],
  "start_s": 0.0
 }
}
```

**흔한 실수**
- 칸이 None 인 채 다음 단계로 — 그 편을 다시 뜯는다.
- 실패를 빈 값으로 넘김 — `ok: false` 와 `failed: 이유` 를 남긴다(이 예시의 fonts 칸이 그 꼴: '모든 후보 점수 0').
- 소리가 없는 편의 받아쓰기 글(BGM 가사)을 말로 믿음 — 예시 segments 가 그 꼴.

#### A-3. `08_make/<편>/대본.json` — render.py 가 읽는 대본(원음+자막 판 꼴)

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| slug · brand · pan | 편 이름 · 내 브랜드 · 쓰는 판 이름 | 글 | 필수 | snapbwatni_ep01_namdaemun · 숏템스냅 · 스냅봤니판 |
| title_lines | 틀 제목 줄 — 줄마다 [[글, 색 hex?]…](색 없으면 판 frame.title 색) | 목록 | 필수 | [["남대문 스카프 사장님의"]] · [["쇼핑 특강 레전드 ㅋㅋㅋ", "#FB39A7"]] |
| source_label | 출처 줄 글(없으면 "") | 글 | 필수 | "" |
| facts | 사실 뒷받침 — 줄에서 말하는 사실마다 받아쓰기 시각·박힌 글 | 사전 f1… → 글 | 필수(사실을 말하면) | f1: 7.55~11.90 받아쓰기 |
| lines[].id · kind · role | 줄 id · 갈래 orig(원음 토막)/tts(나레)/sub(자막만) · 역할(§6 어휘) |  | 필수 | O1 · orig · 훅 |
| lines[].src · spans | 원본 파일(편 폴더 상대) · 쓰는 구간 [[시작,끝]…] | 초 | orig 필수 | origin.mp4 · [[7.4, 11.3]] |
| lines[].said | 그 구간에서 실제로 들리는 말(받아쓰기로 확인) | 글 | orig 필수 |  |
| lines[].caps_rel | 해설 자막 [[글, 줄 시작부터 시작 초, 끝 초]…] | 초 | 필수 | ["남대문 스카프 가게에 갔다가", 0.0, 1.3] |
| lines[].bubbles | 말풍선 [[글, 시작, 끝, {x, y, color, rot}]…] — 판 frame.bubble 이 있을 때 | 초 · px · 도 | 선택 | x 650 · y 700 · green · 4.7 |
| lines[].text · read | (tts 줄) 화면 글 · TTS 가 읽는 글 | 글 | tts 필수 |  |

**예시(스냅봤니 시험편 실제 대본.json 발췌 — 앞 1개 줄)**

```json
{
 "slug": "snapbwatni_ep01_namdaemun",
 "brand": "숏템스냅",
 "pan": "스냅봤니판",
 "title_lines": [
  [
   [
    "남대문 스카프 사장님의"
   ]
  ],
  [
   [
    "쇼핑 특강 레전드 ㅋㅋㅋ",
    "#FB39A7"
   ]
  ]
 ],
 "source_label": "",
 "facts": {
  "f1": "원본 받아쓰기(스피치매틱스 material/origin.asr.json) 7.55~11.90 '어머님들 좀 나눠 줄 생각들 하시구요 좀 밑에다가 손을 자꾸 … 엄마' · 박힌 글 '좀 밑에다가 손을 자꾸 집어 넣어야 돼, 엄마'"
 },
 "lines": [
  {
   "id": "O1",
   "kind": "orig",
   "role": "훅",
   "src": "origin.mp4",
   "spans": [
    [
     7.4,
     11.3
    ]
   ],
   "said": "어머님들 좀 나눠줄 생각들 하시고요 / 좀 밑에다가 손을 자꾸 집어 넣어야 돼, 엄마",
   "caps_rel": [
    [
     "남대문 스카프 가게에 갔다가",
     0.0,
     1.3
    ],
    [
     "사장님 훈수에 빵 터짐ㅋㅋㅋ",
     1.3,
     2.6
    ],
    [
     "손은 밑으로 쑥 넣으라고",
     2.6,
     3.9
    ]
   ],
   "bubbles": [
    [
     "뭐 고르지~?",
     0.2,
     1.8,
     {
      "x": 650,
      "y": 700,
      "color": "green",
      "rot": 4.7
     }
    ]
   ]
  }
 ]
}
```

#### A-4. `08_make/<편>/재료.json` — 줄마다 어느 원본 장면을 어떻게 자르나

| 칸 | 뜻 | 단위·값 범위 | 필수 | 예(스냅봤니) |
|---|---|---|---|---|
| src_urls | 원본 이름 → 받은 주소(출처.md 와 같아야) | 주소 | 필수 | origin → instagram reel |
| cuts.<줄 id>[] | 줄 안 컷마다 {at(줄 시작부터 초), crop[x,y,w,h](원본 px), see(그 컷에 보이는 것 — 클로드가 프레임을 보고)} | 초 · px | 필수 | {at 0.0, crop [0,521,1080,1399]} |
| (선택) fit | 줄 글 ↔ 그 컷 0~10 | 0~10 | 선택 |  |

**예시(실제 재료.json 발췌 — 앞 2개 줄)**

```json
{
 "src_urls": {
  "origin": "https://www.instagram.com/reel/reel_F/"
 },
 "cuts": {
  "O1": [
   {
    "at": 0.0,
    "crop": [
     0,
     521,
     1080,
     1399
    ],
    "see": "버킷햇 손님 뒤로 사장님이 손님들에게 말함"
   }
  ],
  "O2": [
   {
    "at": 0.0,
    "crop": [
     0,
     521,
     1080,
     1399
    ],
    "see": "사장님 정면, 스카프 더미 앞"
   }
  ]
 }
}
```

**흔한 실수**
- spans 에 금액·남의 이름이 들리는 구간을 그대로 둠 — said 와 받아쓰기를 대조해 자른다(실패기록 5).
- crop 높이를 원본보다 크게 잡아 늘림 — 판 checks.no_stretch.
- see 칸을 비워 둠 — 장면표·fit 의 뒷받침가 없어진다.
