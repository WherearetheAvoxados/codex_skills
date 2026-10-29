---
name: arch-diagram
description: 과제의 설계 구조도(무엇이 어떤 순서로 무엇을 하는지, 각 부분이 어디까지 됐는지)를 새로 그리거나 확정된 결정에 맞춰 갱신할 때 쓴다. 기본은 SVG 한 장 docs/architecture.svg: 왼쪽에 구조도, 오른쪽에 구현 단계 표(impl-steps가 채움). "구조도 그려줘", "구조도 갱신", "구조도에 반영"에 쓴다.
disable-model-invocation: true
---

# 구조도 그리기 · 갱신 (SVG 한 장)

코드 구조가 아니라 **설계 구조**를 한 장에: 입력 → 처리 → 출력, 그리고 진행 상태. 내가 눈으로 보며 작업하는 것이 목적이다.
한 파일 `docs/architecture.svg`에 **왼쪽 구조도(이 스킬)**, **오른쪽 구현 단계 표(impl-steps)**를 함께 그린다.

## 1. 찾기
- `docs/architecture.svg`가 있으면 그것을 고친다. README.md는 과제 원문이라 읽기만 하고 그리지 않는다.
- 글자만 읽기: `grep -o '<text[^>]*>[^<]*</text>' docs/architecture.svg | sed 's/<[^>]*>//g'`
- 없으면 아래 틀로 새로 만든다. 오른쪽 표 자리는 제목만 두고, $impl-steps로 채우자고 말한다.

## 2. 넣을 내용 정하기
- SPEC.md와 DECISIONS.md에서 **확정된 것만** 넣는다. 검토 중이면 "(검토 중)"으로 표시하거나 넣지 않는다.
- 상자 하나 = SPEC 요구 하나 이상과 이어지는 부분. 이어지지 않는 상자는 그리지 않는다.
- 상자 3~7개. 넘으면 묶는다. 시험 채점자가 10초 안에 읽을 수 있게.
- 상자 안: 제목 한 줄(10자 안팎) + 설명 1~2줄. 결정 시각이 의미 있으면 "(HH:MM 확정)"처럼 줄 안에.

## 3. 틀 (너비 1240: 왼쪽 x 20~700 구조도, x 740 세로 구분선, 오른쪽 x 760~1220 단계 표)
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="1240" height="H" viewBox="0 0 1240 H" font-family="sans-serif">
  <defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#5F5E5A"/></marker></defs>
  <rect width="1240" height="H" fill="#FFFFFF"/>
  <!-- structure -->
  <text x="20" y="32" font-size="16" font-weight="600" fill="#2C2C2A">(과제 이름) 구조 (MM-DD HH:MM 갱신)</text>
  <rect x="20" y="60" width="680" height="64" rx="8" fill="#EAF3DE" stroke="#3B6D11"/>
  <text x="36" y="84" font-size="13" font-weight="600" fill="#2C2C2A">입력: CSV 업로드</text>
  <text x="36" y="104" font-size="12" fill="#444441">지점 · 날짜 · 매출 세 칸, 빈 값은 0</text>
  <path d="M360 124 L360 156" stroke="#5F5E5A" fill="none" marker-end="url(#a)"/>
  <!-- 다음 상자: y = 앞 상자 아래 + 32 … -->
  <!-- legend -->
  <text x="20" y="LY" font-size="11" fill="#5F5E5A">초록 = 구현됨 · 주황 = 진행 중 · 회색 = 미착수</text>
  <!-- divider -->
  <path d="M740 20 L740 H-20" stroke="#D3D1C7"/>
  <!-- implementation steps (impl-steps가 채운다) -->
  <text x="760" y="32" font-size="14" font-weight="600" fill="#2C2C2A">구현 단계 (MM-DD HH:MM 기준)</text>
</svg>
```
| 상태 | fill | stroke |
|---|---|---|
| 구현됨 | #EAF3DE | #3B6D11 |
| 진행 중 | #FAEEDA | #BA7517 |
| 미착수 | #F1EFE8 | #888780 |
- 글자: 제목 16/600, 상자 제목 13/600, 본문 12 (#444441), 주석 11 (#5F5E5A). 화살표 marker는 `<defs>`의 하나를 재사용.
- 구역마다 `<!-- 이름 -->` 주석을 단다. 오른쪽 `<!-- implementation steps -->` 아래는 impl-steps 몫이라 건드리지 않는다.
- 높이 H = 왼쪽 맨 아래와 오른쪽 맨 아래 중 큰 쪽 + 40. `<svg height viewBox>`, 배경 rect, 구분선을 함께 맞춘다.

## 4. 고칠 때
- 상자 · 줄을 더하면 그 아래 왼쪽 요소의 y를 모두 같은 만큼 내리고, 상자 높이 · 화살표 path · H를 함께 늘린다. python으로 왼쪽 구역(x < 740)만 범위를 정해 바꾼다.
- 상태가 바뀌면 상자 색을 바꾸고, 제목의 "갱신" 시각을 지금으로.
- 구조가 바뀌어 오른쪽 표의 문구가 틀리게 되면 그 사실을 보고한다(표는 impl-steps가 고친다).

## 5. 확인 (내가 눈으로 볼 수 있게)
- XML: `python -c "import xml.dom.minidom,sys; xml.dom.minidom.parse(sys.argv[1])" docs/architecture.svg`
- 넘침 어림: 한글 1자 ≈ 글자 크기(12px), 영문 · 숫자 ≈ 0.6배. 상자 오른쪽 끝(x 700)을 넘지 않게 짧게 쓴다.
- 보고: 바뀐 상자 · 줄을 짧게, 그리고 "docs/architecture.svg를 열어 확인" 한 줄(웹 IDE 미리보기). 커밋은 요청받을 때만.
