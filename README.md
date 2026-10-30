# codex_skills

3시간 AI 활용 실무 과제(웹 IDE + Codex)용 지침과 스킬.
흐름: **질문으로 요구사항 끌어내기 → SPEC 승인 → 덜어낸 계획 → 작은 단위 구현 · 검증 → 기록 · SOLUTION.md**. 과제 원문 README.md는 읽기만 한다.

```
AGENTS.md                               항상 적용되는 규칙 (40줄 이내)
skills/requirements-interview/SKILL.md  담당자 질문 순서 → SPEC.md                         (자동 호출)
  └ scripts/profile_csv.py               데이터 점검: 빈 값 · 고유값 · 표기 변형 · 시간 형식 · 정렬 · 중복 (표준 라이브러리만)
skills/impl-steps/SKILL.md              SPEC에서 PLAN.md 단계 표 만들기 · 상태 갱신, 같은 표를 docs/architecture.svg 오른쪽에        (이하 수동 $이름 만)
skills/follow-plan/SKILL.md             PLAN 단계를 하나씩 끝까지 구현 · 검증 (땜질이면 멈추고 묻기)
skills/finalize/SKILL.md                제출 전 마무리: 상태 점검 · SPEC 기준 점검 · DECISIONS 정리 · SOLUTION.md
skills/arch-diagram/SKILL.md            설계 구조도 SVG (docs/architecture.svg 왼쪽)
skills/discuss/SKILL.md                 파일 안 바꾸고 방향만 논의 (선택지 · 추천)
skills/discuss-with-research/SKILL.md   문서 · 사례를 찾아보며 논의 (설치 · 내려받기 없음)
skills/explain-cause/SKILL.md           원인 · 결정을 쉬운 말과 실제 예로 다시 설명 (서술형 대비)
skills/context-recall/SKILL.md          압축 · 새 세션 뒤 SPEC · PLAN · DECISIONS · git으로 상태 정리
skills/ui-kit/                          화면 틀: base.css · report.html(보고서형) · tool.html(입력→결과형) · parts.html(견본) · reference.html(원본, 읽지 않음)
```

스킬은 Agent Skills 형식(`SKILL.md` + `name` · `description` 머리말)이라 Codex와 Claude Code 모두 읽는다. hooks · MCP · 플러그인 · 외부 인증 없음.

**자동 호출은 `requirements-interview` 하나뿐.** 나머지 9개는 `$이름`(Claude Code는 `/이름`)으로 직접 부를 때만 돈다.
- Codex: 각 스킬의 `agents/openai.yaml`에 `policy.allow_implicit_invocation: false`
- Claude Code: 각 SKILL.md 머리말에 `disable-model-invocation: true` (Codex는 모르는 칸을 무시한다)

## 설치 1: Codex에게 말로 (외울 것 없음)

과제 프로젝트에서 Codex에게:

```
$skill-installer WherearetheAvoxados/codex_skills의 skills 폴더 스킬을 모두 설치하고, 저장소의 AGENTS.md는 ~/.codex/AGENTS.md로 받아줘
```

- 스킬 10개가 `~/.codex/skills/<이름>/`에 설치된다. 데이터 점검 스크립트(requirements-interview 안 `scripts/profile_csv.py`)와 화면 틀(ui-kit 폴더)도 함께 받아진다.
- AGENTS.md는 `~/.codex/AGENTS.md`(모든 프로젝트에 적용)로 받는다. **과제 프로젝트에는 아무 파일도 생기지 않는다** — 과제 README.md를 덮을 일도, 제출물에 키트가 섞일 일도 없다.
- 확인: `ls ~/.codex/skills ~/.codex/AGENTS.md`, 그리고 Codex를 다시 켜서 `/skills`에 열 이름이 보이는지.
- 같은 이름의 스킬이 이미 있으면 설치기가 멈춘다. 지우고 다시.
- `/skills`에 안 보이면: 최신 Codex는 사용자 스킬을 `~/.agents/skills/`에서 찾는다. `mkdir -p ~/.agents/skills && cp -R ~/.codex/skills/{requirements-interview,impl-steps,follow-plan,finalize,arch-diagram,discuss,discuss-with-research,explain-cause,context-recall,ui-kit} ~/.agents/skills/` 뒤 Codex 재시작.

**Codex가 이 저장소를 설치할 때 지킬 것** (위 요청을 받은 Codex가 이 README를 읽을 때를 위해)
1. 스킬은 `$skill-installer`의 설치 스크립트로 `skills/<이름>` 경로만 설치한다 (`tools/` 같은 다른 폴더는 없다).
2. AGENTS.md는 `curl -fsSL https://raw.githubusercontent.com/WherearetheAvoxados/codex_skills/main/AGENTS.md -o ~/.codex/AGENTS.md` 로만 받는다.
3. 이 저장소를 과제 프로젝트 안에 clone하거나 압축을 풀지 않는다. 이 README.md를 프로젝트에 받지 않는다 (과제 원문 README.md를 덮어쓴다).

## 설치 2: 설치기가 막혔을 때 (파일로 직접)

```bash
git clone https://github.com/WherearetheAvoxados/codex_skills /tmp/kit   # 반드시 프로젝트 밖 (안에 받으면 과제 README.md를 덮어씀)
cp /tmp/kit/AGENTS.md ~/.codex/AGENTS.md                                  # 모든 프로젝트에 적용
mkdir -p ~/.agents/skills && cp -R /tmp/kit/skills/* ~/.agents/skills/    # 사용자 스킬 (스크립트 포함)
```

- `~/.codex`에 쓸 수 없는 환경이면: `cat /tmp/kit/AGENTS.md >> AGENTS.md`(프로젝트 루트, 덮어쓰지 않고 뒤에 붙임)와 `mkdir -p .agents/skills && cp -R /tmp/kit/skills/* .agents/skills/`. 이때는 키트 파일이 프로젝트에 생기니 제출 전 지우거나 SOLUTION.md에 "점검 도구 · 스킬은 키트에서 가져옴" 한 줄($finalize가 넣는다).
- 스킬이 안 읽히면 경로로 직접 부른다: `/tmp/kit/skills/follow-plan/SKILL.md를 읽고 그 순서대로 해줘`.
- 네트워크가 막혔으면 AGENTS.md와 꼭 필요한 스킬(requirements-interview · impl-steps · follow-plan)만 웹 IDE에 새 파일로 붙여 넣는다.

## 화면 틀 쓰는 법 (ui-kit)

1. 보고서형(표 · 요약 · 필터)은 `report.html`, 입력 → 결과형은 `tool.html`을 `base.css`와 함께 프로젝트 화면 폴더로 복사한다 (`$ui-kit`, 원본은 `~/.codex/skills/ui-kit/`).
2. `<link rel="stylesheet" href="base.css">`는 그대로 두고 base.css 부품만 쓴다. 새 디자인 시스템 · 프레임워크 · 웹폰트 · CDN 없이.
3. `<!-- 선택: SPEC에 없으면 지울 것 -->`이 붙은 부품은 SPEC에 없으면 지운다. 제출 때 SOLUTION.md에 "화면 기본 틀은 공개 키트에서 가져옴" 한 줄.

## 읽히는지 확인

1. 지침: 프로젝트 루트에서
   `codex --ask-for-approval never "지금 불러온 지침 파일 경로와 규칙을 5줄로 요약해줘. 파일은 바꾸지 마."`
   → AGENTS.md 경로와 "SPEC 승인 전 구현 안 함", "DECISIONS.md 한 줄 기록"이 나오면 됨.
2. 스킬: Codex에서 `/skills` 실행, 또는 `$`를 치면 열 이름이 목록에 보여야 함.

## 시험 프롬프트

```
README에 "판매 데이터로 대시보드 만들어줘"라고만 적혀 있어. 다 만들어줘.
```
기대: 코드를 쓰지 않고, 담당자에게 물을 질문 3개 이내(지금 업무 방식부터)를 제안. 파일 변경 없음.

```
$impl-steps SPEC.md 기준으로 PLAN.md 단계 표만 만들어줘.
```
기대: 단계마다 검증 명령과 기대 결과가 붙은 표, SPEC에 없는 것은 "제안만". 구현은 시작하지 않음.

수동 전용 확인: `이거 구현하지 말고 방향만 얘기해 보자`처럼 `$` 없이 말했을 때 discuss가 저절로 불리지 않아야 한다 (AGENTS.md 규칙으로만 답함).

## 쓰는 순서 (시험 당일)

| 시간 | 할 일 | 스킬 |
|---|---|---|
| 0:00–0:30 | README 읽기, 담당자 질문, SPEC.md 확정 | `$requirements-interview` |
| 0:30–0:45 | 단계 표 · 구조도, 승인 | `$impl-steps`, `$arch-diagram` |
| 0:45–2:30 | 단계마다 구현 → 실행 → 보고, 표 갱신 | `$follow-plan`, `$impl-steps` |
| 2:30–3:00 | 상태 점검, 성공 기준 점검, DECISIONS 정리, SOLUTION.md | `$finalize` |

필요할 때만: 방향이 갈리면 `$discuss` (문서를 찾아봐야 하면 `$discuss-with-research`), 원인이나 결정을 이해 못 했으면 `$explain-cause`, 압축 · 새 세션 뒤엔 `$context-recall`.

토큰 아끼기 (내 쪽): README나 긴 로그를 프롬프트에 통째로 붙여 넣지 말고 `README.md 읽고`처럼 경로만 준다. 한 프롬프트에 한 가지 일만.

사후 서술형 대비: DECISIONS.md의 "이유 / 버린 대안 / 출처"가 곧 답안 재료다. 출처가 "AI 제안 수정 · 내 결정"인 줄이 내 판단의 근거이니, AI 제안을 고치거나 거절할 때마다 바로 한 줄 남긴다. 끝나기 전에 한 번 소리 내어 읽어 본다.
