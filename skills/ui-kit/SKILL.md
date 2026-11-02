---
name: ui-kit
description: 과제에 화면(HTML)이 필요할 때 쓴다. 이 스킬 폴더의 순수 HTML/CSS 틀(app-shell · login · list-detail · form-page · report · tool)을 프로젝트로 복사해 자리만 채우고 base.css 부품만 쓴다. 새 디자인 시스템 · UI 프레임워크 · 웹폰트 · CDN 없이. "화면 만들어줘", "사이트", "로그인", "대시보드", "결과 페이지", "입력 폼"에 쓴다.
disable-model-invocation: true
---

# 화면 틀 (순수 HTML/CSS)

이 폴더: `base.css`(부품 · 레이아웃 · 어두운 기본 + `<html data-theme="light">`), 틀 6개, `parts.html`(부품 견본, 참고용), `reference.html`(디자인 원본 번들 — **읽지 않는다**, 사람이 눈으로 볼 견본).
위치는 보통 `~/.codex/skills/ui-kit/` 또는 `~/.agents/skills/ui-kit/`.

| 틀 | 배치 | 쓰는 화면 |
|---|---|---|
| `app-shell.html` | 왼쪽 메뉴 + 상단 바(역할 · 사용자) + 본문 | 여러 페이지 사이트의 공통 뼈대, 맞는 틀이 없는 화면 |
| `login.html` | 가운데 카드 | 로그인 · 역할 선택 |
| `list-detail.html` | app-shell + 왼쪽 목록 · 오른쪽 상세 | 목록에서 골라 보고 처리 |
| `form-page.html` | app-shell + 2열 폼 | 등록 · 수정 |
| `report.html` | app-shell + 요약 숫자 · 필터 · 표 | 대시보드 · 보고서 |
| `tool.html` | app-shell + 입력 · 결과 | 입력해서 결과(AI 답 · 계산) 보기 |

## 쓰는 법
1. **화면 → 틀 매핑부터.** SPEC의 화면 목록을 만들고 화면마다 틀 하나를 고른다. 이 표를 PLAN.md에 먼저 적는다.
   ```markdown
   | 화면 | 틀 | 넣을 내용 |
   |---|---|---|
   | 로그인 | login.html | 역할 A/B 선택 |
   | 요청 목록 | list-detail.html | 행: 번호 · 상태 · 날짜 / 상세: 승인 · 반려 |
   ```
2. 고른 틀과 `base.css`를 프로젝트의 화면 폴더(예: `web/`, 과제가 정한 곳)로 복사한다. 화면이 여럿이면 틀을 화면마다 복사하고 `.app-menu`의 링크와 `aria-current="page"`만 맞춘다. `<link rel="stylesheet" href="base.css">`는 그대로 둔다.
3. **틀의 레이아웃 뼈대(.app · 격자 · 자리 구조)는 바꾸지 않고 `<!-- 자리: … -->`에 내용만 채운다.** 부품을 `.page`에 세로로 쌓지 않는다. 자리 글자("…자리")는 실제 내용으로 바꾼다.
4. `<!-- 선택: SPEC에 없으면 지울 것 -->` 부품은 SPEC에 없으면 지운다. `<!-- 상태: … -->`는 그 상태일 때만 보이게 과제 코드에서 켠다.
5. 맞는 틀이 없으면 app-shell의 본문 자리에 base.css 레이아웃 부품을 조합한다: `.grid-2` · `.grid-3` · `.grid-auto`(카드 격자) · `.main-aside`(본문 + 오른쪽 320px) · `.list-detail` · `.form-grid`(`.span-2`) · `.row`(`.between`). 부품 HTML은 `parts.html`에서 가져온다.
6. 그래도 부족하면 프로젝트 CSS에 몇 줄 더하고 DECISIONS.md에 한 줄(무엇을 · 왜 base.css로 안 되는지).
7. 화면 단위를 마칠 때 1280px 폭으로 열어 고른 틀과 같은 배치인지 확인한다(메뉴 왼쪽 · 격자 열 수 · 목록/상세 나란히).

## 지킬 것
- **기본 스택은 정적 HTML + vanilla JS.** 화면 동작은 `web/app.js` 한 파일, 서버가 필요하면 Python 표준 라이브러리(`http.server`)로 한다. Next.js · React는 과제가 지정했거나, 화면이 6~7개를 넘어 뼈대 공유가 필요하거나, 역할별 접근 제한이 채점 대상일 때만 쓰고 DECISIONS.md에 한 줄. 그때도 base.css를 그대로 import하고 틀의 뼈대를 JSX로 옮긴다.
- 애니메이션 · 실시간 현황도 라이브러리 없이: 깜빡임은 CSS `@keyframes`(위험 상태에만, `prefers-reduced-motion`이면 끔), 이동은 `transform` + `transition`, 갱신은 `setInterval` + `fetch` 또는 `EventSource`(SSE), 지도 대신 SVG 도식(외부 타일은 막힘).
- 스크립트 · 웹폰트 · CDN · 이미지 없이도 더블클릭 · localhost에서 그대로 보인다. 동작(데이터 채우기 · 요청 · 역할 전환 · 행 선택)이 필요하면 과제 코드에서 붙이고, 틀 자체를 프레임워크로 바꾸지 않는다.
- 인증 방식(화면 전환만 / 데모 계정 / 실제 인증)은 담당자에게 확인한 뒤 정한다. 배포하지 않는다(결과물 외부 전송 금지).
- 900px 아래에선 메뉴가 위로, 여러 열이 1열로 바뀐다(base.css가 한다). 화면마다 따로 반응형을 만들지 않는다.
- 숫자 열은 `td.num`(오른쪽 정렬 · 고정 폭 숫자). 접고 펴기는 `<details class="disclosure">`, 대화상자는 `<dialog class="dialog">` + `showModal()`. 칸 오류는 `.field.is-error` + `.field-error`.
- 주요 버튼은 `.btn-primary`(단색 주황 + 검은 글자). 빨강→주황 그라데이션은 `.alert-strip` 윗선에만, 빨강은 위험 배지 · `.btn-danger` · 오류 상태에만.
- 상태 배지는 기호 · 영문 · 한글을 함께(`! CRIT 위험`). 주황은 상태로 쓰지 않는다(현재 메뉴 · 선택 행 강조에만).
- 제출할 때 SOLUTION.md에 "화면 기본 틀은 공개 키트(ui-kit)에서 가져옴" 한 줄($finalize가 넣는다).
