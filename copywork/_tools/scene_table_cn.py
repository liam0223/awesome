# -*- coding: utf-8 -*-
"""scene_table_cn.py <08_make/<편>> <10_apply/장면표.md> — timeline·자막표에서 장면표(효과음·랜덤 고름 포함)를 만든다."""
import sys, json
E, out = sys.argv[1], sys.argv[2]
T = json.load(open(E + '/timeline.json', encoding='utf-8')); S = json.load(open(E + '/자막표.json', encoding='utf-8'))
txt = {r['id']: r['text'] for r in S['rows']}; V = S.get('vary') or {}
sf = {}
for c in S['sfx']: sf.setdefault('T' if c['why'] == '표지' else c['line'], []).append(f"{c['kind']}({c.get('pack','')}) {c['t']}초")
o = ["# 장면표 — 클릭노트판 시험편", "", f"- 이 편 랜덤 고름: 효과음 팩 {V.get('sfx_pack')} · 끼움말 '{V.get('insert')}' · 큰글 장면 효과 {V.get('big_fx')} + {V.get('big_sfx')}", "",
     "| # | 시각(초) | 줄 | 자막 | 클립(원본·구간) | 화면 상황 | 효과음 |", "|---|---|---|---|---|---|---|"]
seen = set()
for i, c in enumerate(T['cuts'], 1):
    s = ', '.join(sf.get(c['line'], [])) if c['line'] not in seen else ''; seen.add(c['line'])
    o.append(f"| {i} | {c['t0']:.2f}~{c['t1']:.2f} | {c['line']} | {txt[c['line']]} | {c['src'][:-4]} {c['a']}~{c['b_used']} | {c.get('see','')} | {s} |")
o += ["", "- 0초 화면 효과: 흰 번쩍임 + 당겨 들어옴 · 표지→본문 짧은 당김 (판 intro_fx)"]
open(out, 'w', encoding='utf-8').write('\n'.join(o) + '\n')
