"""데이터 파일 모양과 예외를 짧게 본다 (표준 라이브러리만). 사용: python3 <requirements-interview 스킬 폴더>/scripts/profile_csv.py data/*
지원: .csv .tsv .json(객체 배열) .jsonl — 파일마다 행 수 · 열, 열별 빈 값 · 고유값, 표기 변형, 시간 형식 · 정렬, 완전 중복 행."""
import csv, json, re, sys
from collections import Counter
from pathlib import Path

TIME_LIKE = re.compile(r'\d{4}\D{1,3}\d{1,2}\D{1,3}\d{1,2}|\d{1,2}:\d{2}')
PARTS = re.compile(r'(\d{4})\D+(\d{1,2})\D+(\d{1,2})(?:\D*?(오전|오후|AM|PM|am|pm))?\D*?(?:(\d{1,2}):(\d{2})(?::(\d{2}))?)?')

def load(p):
    ext = p.suffix.lower()
    if ext in ('.csv', '.tsv'):
        with open(p, newline='', encoding='utf-8-sig') as f:
            rows = list(csv.reader(f, delimiter='\t' if ext == '.tsv' else ','))
        return (rows[0], rows[1:], 2) if rows else ([], [], 2)
    if ext in ('.json', '.jsonl'):
        text = p.read_text(encoding='utf-8-sig')
        objs = json.loads(text) if ext == '.json' else [json.loads(l) for l in text.splitlines() if l.strip()]
        if not isinstance(objs, list): return None
        head = list(dict.fromkeys(k for o in objs if isinstance(o, dict) for k in o))
        cell = lambda v: '' if v is None else v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
        return head, [[cell(o.get(k)) if isinstance(o, dict) else '' for k in head] for o in objs], 1
    return None

def when(v):
    """시간 값을 비교할 수 있는 튜플로 (모르면 None). '2026. 10. 26. 오후 8:08:16' 같은 한국어 형식도."""
    m = PARTS.search(v)
    if not m: return None
    y, mo, d, ap, h, mi, s = m.groups(); h = int(h or 0)
    if ap in ('오후', 'PM', 'pm') and h < 12: h += 12
    if ap in ('오전', 'AM', 'am') and h == 12: h = 0
    return (int(y), int(mo), int(d), h, int(mi or 0), int(s or 0))

q = lambda v: '"' + v + '"'

def column(name, vals, out, off):
    empty = sum(not v.strip() for v in vals); cnt = Counter(vals)
    shown = cnt.most_common() if len(cnt) <= 50 else cnt.most_common(5)
    out.append(f'  [{name}] 빈 값 {empty} · 고유 {len(cnt)} · ' + ('전부: ' if len(cnt) <= 50 else '상위: ') + ', '.join(f'{q(v)} {n}' for v, n in shown))
    groups = {}   # 앞뒤 공백 · 대소문자 · _/- 차이만 나는 표기
    for v in cnt:
        if v.strip(): groups.setdefault(re.sub(r'[\s_\-]+', '-', v.strip().lower()), []).append(v)
    var = [g for g in groups.values() if len(g) > 1]
    if var: out.append(f'    표기 변형 {len(var)}묶음: ' + ' | '.join(' · '.join(f'{q(v)} {cnt[v]}' for v in sorted(g, key=lambda v: -cnt[v])) for g in var[:8]))
    filled = [v for v in vals if v.strip()]
    if filled and sum(bool(TIME_LIKE.search(v)) for v in filled) >= 0.5 * len(filled):
        shape = lambda v: re.sub(r'\d+', 'N', v.strip())   # 자릿수는 무시하고 모양만 ('오후 8:08' = '오후 10:14')
        shapes = Counter(shape(v) for v in filled); ex = {}
        for v in filled: ex.setdefault(shape(v), v)
        out.append(f'    시간 형식 {len(shapes)}종: ' + ' | '.join(f'{s} ×{n} (예 {q(ex[s])})' for s, n in shapes.most_common(4)))
        ts = [(i, when(v)) for i, v in enumerate(vals) if v.strip()]
        bad = [i for i, t in ts if t is None]
        if bad: out.append(f'    시간으로 못 읽음 {len(bad)}개 (처음 {bad[0] + off}행 {q(vals[bad[0]])})')
        ts = [(i, t) for i, t in ts if t is not None]
        back = next(((a, b) for a, b in zip(ts, ts[1:]) if b[1] < a[1]), None)
        out.append('    시간순 정렬됨' if not back else f'    시간순 아님: 처음 역행 {back[1][0] + off}행 {q(vals[back[1][0]])} < {back[0][0] + off}행 {q(vals[back[0][0]])}')

def profile(p):
    try: got = load(p)
    except (ValueError, UnicodeDecodeError, csv.Error) as e: return [f'읽기 실패: {p.name} ({e})']
    if got is None: return [f'지원 안 함: {p.name}']
    head, rows, off = got
    out = [f'== {p.name}: {len(rows)}행 · 열 {len(head)}개 {head}']
    short = [i + off for i, r in enumerate(rows) if len(r) != len(head)]
    if short: out.append(f'  열 수가 다른 행 {len(short)}개 (처음 {short[0]}행)')
    for j, name in enumerate(head): column(name, [r[j] if j < len(r) else '' for r in rows], out, off)
    seen = Counter(tuple(r) for r in rows); dup = sum(n - 1 for n in seen.values() if n > 1)
    first = next((i + off for i, r in enumerate(rows) if seen[tuple(r)] > 1), None)
    out.append(f'  완전 중복 행 {dup}개' + (f' (처음 {first}행)' if dup else '') + '   ※ 행 번호: ' + ('머리줄을 1행으로 센 파일 줄' if off == 2 else 'n번째 객체(줄)'))
    return out

if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit('사용: python3 <requirements-interview 스킬 폴더>/scripts/profile_csv.py data/*')
    for a in sys.argv[1:]:
        p = Path(a)
        if p.is_file(): print('\n'.join(profile(p)), end='\n\n')
