# codex_skills

3시간 AI 활용 실무 과제(웹 IDE + Codex)용 지침과 스킬.
흐름: **질문으로 요구사항 끌어내기 → SPEC 승인 → 덜어낸 계획 → 작은 단위 구현 · 검증 → 기록 · README**.

```
AGENTS.md                               항상 적용되는 규칙 (30줄 이내)
skills/requirements-interview/SKILL.md  담당자 질문 순서 → SPEC.md                         (자동 호출)
skills/impl-steps/SKILL.md              SPEC에서 PLAN.md 단계 표 만들기 · 상태 갱신        (이하 수동 $이름 만)
skills/follow-plan/SKILL.md             PLAN 단계를 하나씩 끝까지 구현 · 검증 (땜질이면 멈추고 묻기)
skills/finalize/SKILL.md                제출 전 마무리: 상태 점검 · SPEC 기준 점검 · DECISIONS 정리 · README
skills/arch-diagram/SKILL.md            설계 구조도 (README mermaid, 필요하면 SVG)
skills/discuss/SKILL.md                 파일 안 바꾸고 방향만 논의 (선택지 · 추천)
skills/discuss-with-research/SKILL.md   문서 · 사례를 찾아보며 논의 (설치 · 내려받기 없음)
skills/explain-cause/SKILL.md           원인 · 결정을 쉬운 말과 실제 예로 다시 설명 (서술형 대비)
skills/context-recall/SKILL.md          압축 · 새 세션 뒤 SPEC · PLAN · DECISIONS · git으로 상태 정리
```

스킬은 Agent Skills 형식(`SKILL.md` + `name` · `description` 머리말)이라 Codex와 Claude Code 모두 읽는다. hooks · MCP · 플러그인 · 외부 인증 없음.

**자동 호출은 `requirements-interview` 하나뿐.** 나머지 8개는 `$이름`(Claude Code는 `/이름`)으로 직접 부를 때만 돈다.
- Codex: 각 스킬의 `agents/openai.yaml`에 `policy.allow_implicit_invocation: false`
- Claude Code: 각 SKILL.md 머리말에 `disable-model-invocation: true` (Codex는 모르는 칸을 무시한다)

## 설치 1: Codex 안에서 `$skill-installer`

Codex 세션에서:

```
$skill-installer install every skill under skills/ from https://github.com/WherearetheAvoxados/codex_skills
```

- 설치 위치는 `~/.codex/skills/<이름>/`. 다음 턴부터 쓸 수 있다. 같은 이름이 이미 있으면 설치가 멈추니 지우고 다시.
- 설치기 스크립트를 직접 부를 때:
  ```bash
  S="requirements-interview impl-steps follow-plan finalize arch-diagram discuss discuss-with-research explain-cause context-recall"
  python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo WherearetheAvoxados/codex_skills --path $(for s in $S; do printf 'skills/%s ' $s; done)
  ```
- `/skills`에 안 보이면: 최신 Codex는 사용자 스킬을 `~/.agents/skills/`에서 찾는다. `mkdir -p ~/.agents/skills && for s in $S; do cp -R ~/.codex/skills/$s ~/.agents/skills/; done` 뒤 Codex 재시작.

AGENTS.md는 설치기가 다루지 않으니 따로 둔다 (둘 중 하나):

```bash
curl -fsSL https://raw.githubusercontent.com/WherearetheAvoxados/codex_skills/main/AGENTS.md -o AGENTS.md            # 과제 프로젝트 루트
curl -fsSL https://raw.githubusercontent.com/WherearetheAvoxados/codex_skills/main/AGENTS.md -o ~/.codex/AGENTS.md   # 모든 프로젝트
```

## 설치 2: 설치가 막혔을 때 (파일로 직접)

```bash
git clone https://github.com/WherearetheAvoxados/codex_skills /tmp/kit      # 또는 ZIP 받아 풀기
cp /tmp/kit/AGENTS.md ./AGENTS.md                                   # 과제 프로젝트 루트 (이미 있으면 내용을 뒤에 붙인다)
mkdir -p .agents/skills && cp -R /tmp/kit/skills/* .agents/skills/  # Codex가 저장소 안 스킬로 자동 인식
```

- `.agents/skills`도 안 먹히면 경로로 직접 부른다: `skills/follow-plan/SKILL.md를 읽고 그 순서대로 해줘`.
- 네트워크가 막혔으면 AGENTS.md와 꼭 필요한 스킬(requirements-interview · impl-steps · follow-plan)만 웹 IDE에 새 파일로 붙여 넣는다.
- 과제 제출물에 이 키트 파일이 섞이지 않게 `/tmp/kit`처럼 프로젝트 밖에 받는다.

## 읽히는지 확인

1. 지침: 프로젝트 루트에서
   `codex --ask-for-approval never "지금 불러온 지침 파일 경로와 규칙을 5줄로 요약해줘. 파일은 바꾸지 마."`
   → AGENTS.md 경로와 "SPEC 승인 전 구현 안 함", "DECISIONS.md 한 줄 기록"이 나오면 됨.
2. 스킬: Codex에서 `/skills` 실행, 또는 `$`를 치면 아홉 이름이 목록에 보여야 함.

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
| 2:30–3:00 | 상태 점검, 성공 기준 점검, DECISIONS 정리, README | `$finalize` |

필요할 때만: 방향이 갈리면 `$discuss` (문서를 찾아봐야 하면 `$discuss-with-research`), 원인이나 결정을 이해 못 했으면 `$explain-cause`, 압축 · 새 세션 뒤엔 `$context-recall`.

사후 서술형 대비: DECISIONS.md의 "이유 / 버린 대안"이 곧 답안 재료다. 끝나기 전에 한 번 소리 내어 읽어 본다.
