---
name: ui-kit
description: 과제에 화면(HTML)이 필요할 때 쓴다. 이 스킬 폴더의 순수 HTML/CSS 틀(report.html 보고서형 · tool.html 입력→결과형)을 프로젝트로 복사해 시작하고 base.css 부품만 쓴다. 새 디자인 시스템 · UI 프레임워크 · 웹폰트 · CDN 없이. "화면 만들어줘", "대시보드", "결과 페이지", "입력 폼"에 쓴다.
disable-model-invocation: true
---

# 화면 틀 (순수 HTML/CSS)

이 폴더: `base.css`(부품 · 어두운 기본 + `<html data-theme="light">`), `report.html`(보고서형), `tool.html`(입력 → 결과형), `parts.html`(부품 견본, 참고용), `reference.html`(디자인 원본 번들 — **읽지 않는다**, 사람이 눈으로 볼 견본).
위치는 보통 `~/.codex/skills/ui-kit/` 또는 `~/.agents/skills/ui-kit/`.

## 쓰는 법
1. SPEC의 화면이 표 · 요약 · 필터 위주면 `report.html`, 입력하고 결과(AI 답 · 계산 결과)를 보는 화면이면 `tool.html`을 고른다.
2. 고른 파일과 `base.css`를 프로젝트의 화면 폴더(예: `web/`, 과제가 정한 곳)로 복사한다. `<link rel="stylesheet" href="base.css">`는 그대로 둔다.
3. `<!-- 선택: SPEC에 없으면 지울 것 -->` 주석이 붙은 부품은 SPEC에 없으면 지운다. 자리 글자("…자리")는 실제 내용으로 바꾼다.
4. 부품이 더 필요하면 `parts.html`에서 그 부분의 HTML만 가져온다. base.css에 없는 클래스를 새로 만들지 않는다. 꼭 필요하면 프로젝트 쪽 CSS에 몇 줄만 더하고 DECISIONS.md에 한 줄.

## 지킬 것
- 스크립트 · 웹폰트 · CDN · 이미지 없이도 더블클릭 · localhost에서 그대로 보인다. 동작(데이터 채우기 · 요청)이 필요하면 과제 코드에서 붙이고, 틀 자체를 프레임워크로 바꾸지 않는다.
- 숫자 열은 `td.num`(오른쪽 정렬 · 고정 폭 숫자). 접고 펴기는 `<details class="disclosure">`, 대화상자는 `<dialog class="dialog">` + `showModal()`.
- 주요 버튼은 `.btn-primary`(단색 주황 + 검은 글자). 빨강→주황 그라데이션은 `.alert-strip` 윗선에만, 빨강은 위험 배지 · `.btn-danger` · 오류 상태에만.
- 상태 배지는 기호 · 영문 · 한글을 함께(`! CRIT 위험`). 주황은 상태로 쓰지 않는다.
- 제출할 때 SOLUTION.md에 "화면 기본 틀은 공개 키트(ui-kit)에서 가져옴" 한 줄($finalize가 넣는다).
