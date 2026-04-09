# skill-finder 소스 가이드

**최종 검증일**: 2026-04-09
**검증 방법**: GitHub API (stars, forks, pushed_at) + WebFetch (README, Claude Code 지원 여부)

이 파일은 `skill-finder`가 검색하는 9개 검증 소스를 정리한 것입니다. 모든 엔트리는 다음 기준을 통과했습니다:

1. URL이 존재하고 접근 가능 (403 / 404 / 죽은 도메인 제외)
2. 1,000+ stars **또는** 공식 벤더 (Anthropic / HuggingFace)
3. 최근 3개월 내 push 활동
4. Claude Code 지원 명시 (SKILL.md 포맷 또는 `/plugin marketplace add`)

---

9개 소스는 **저장 구조**에 따라 두 그룹으로 나뉩니다. 이 구분은 각 소스를 어떻게 검색할지를 결정합니다:

- **Group A (Embedded)** — 리포 안에 실제 `SKILL.md` 파일이 있는 저장소. 검색 방법: 리포 트리 또는 skills 디렉터리를 fetch해서 쿼리와 스킬 이름·설명을 매칭.
- **Group B (Index)** — 외부 스킬로 링크하는 awesome list / 카탈로그. 검색 방법: README를 fetch해서 링크 텍스트와 주변 설명을 스캔, 매치되면 실제 소스 링크로 이동해서 검증.

이 그룹 구분은 **출력 랭킹·그룹화에 사용되지 않습니다.** `skill-finder`는 9개 소스 전체에서 단일 랭킹 리스트를 생성합니다.

---

## Group A — Embedded (리포 내부에 실제 SKILL.md 파일 존재, 설치 가능)

### A1. anthropics/skills

- **URL**: https://github.com/anthropics/skills
- **Stars**: 113,728
- **Last push**: 2026-04-08
- **설치**:
  ```
  /plugin marketplace add anthropics/skills
  /plugin install <skill-name>@anthropics-skills
  ```
- **강점**: Anthropic 공식. SKILL.md 스펙의 기준점. 문서 스킬 (`docx`, `pdf`, `pptx`, `xlsx`)과 범용 카테고리 제공.
- **구조**: `skills/<category>/<skill-name>/SKILL.md`
- **사용 상황**: 공식·스펙 준수·잘 테스트된 스킬이 필요할 때.

### A2. sickn33/antigravity-awesome-skills

- **URL**: https://github.com/sickn33/antigravity-awesome-skills
- **Stars**: 31,780
- **Last push**: 2026-04-09
- **설치**:
  ```
  npx antigravity-awesome-skills --claude
  ```
- **강점**: 1,392+ 스킬. 멀티 에이전트 지원 (Claude Code / Cursor / Codex / Gemini / Copilot / Windsurf). 단일 설치 가능 소스 중 최대 규모.
- **구조**: `skills/<skill-name>/SKILL.md` + 인스톨러 CLI
- **사용 상황**: 최대 커버리지가 필요하거나 A1이 해당 도메인에 부실할 때.

### A3. alirezarezvani/claude-skills

- **URL**: https://github.com/alirezarezvani/claude-skills
- **Stars**: 10,162
- **Last push**: 2026-04-08
- **설치**:
  ```
  /plugin marketplace add alirezarezvani/claude-skills
  /plugin install <skill-name>@claude-code-skills
  ```
- **강점**: 156+ 스킬, 9개 도메인 (엔지니어링, devops, 데이터, 문서 등). stdlib 전용 Python 설계.
- **구조**: embedded SKILL.md + plugin marketplace
- **사용 상황**: 개발 중심 스킬 (테스트, 리팩토링, CI/CD).

### A4. huggingface/skills

- **URL**: https://github.com/huggingface/skills
- **Stars**: 10,114
- **Last push**: 2026-04-09
- **설치**:
  ```
  /plugin marketplace add huggingface/skills
  /plugin install <skill-name>@huggingface/skills
  ```
- **강점**: HuggingFace 공식. 12개 ML / 데이터 스킬 (hf-cli, huggingface-datasets, huggingface-gradio, huggingface-llm-trainer, transformers-js 등).
- **주의**: ML / 데이터 도메인 전용. 오피스 문서나 SaaS 자동화에는 부적합.
- **사용 상황**: ML 훈련, 데이터셋 큐레이션, 모델 배포, 추론 작업.

---

## Group B — Index (awesome list + 외부 링크, 자체 저장소 아님)

### B1. ComposioHQ/awesome-claude-skills

- **URL**: https://github.com/ComposioHQ/awesome-claude-skills
- **Stars**: 52,378
- **Last push**: 2026-02-19
- **강점**: Claude 전용 생태계 인덱스. SaaS / API 연동에 강함 — Slack, Notion, Jira, GitHub, Linear, CRM 시스템, 워크플로우 자동화.
- **사용 상황**: Claude Code를 외부 SaaS / API 서비스와 연결할 때.

### B2. hesreallyhim/awesome-claude-code

- **URL**: https://github.com/hesreallyhim/awesome-claude-code
- **Stars**: 37,648
- **Last push**: 2026-04-09
- **강점**: 종합 Claude Code 큐레이션. Skills **뿐만 아니라** Hooks, Slash commands, CLAUDE.md 예제, 에이전트 패턴까지 커버.
- **사용 상황**: 스킬을 넘어선 광범위한 Claude Code 탐색.

### B3. VoltAgent/awesome-agent-skills

- **URL**: https://github.com/VoltAgent/awesome-agent-skills
- **Stars**: 14,894
- **Last push**: 2026-04-04
- **강점**: 1,000+ 엔트리. 멀티 에이전트 인덱스 (Claude / Cursor / Codex / Gemini / Copilot / Windsurf / OpenCode). 공식 벤더 스킬(Vercel, Stripe, Cloudflare, Figma, React) 집약.
- **주의**: aggregator only — 외부 소스로만 연결.
- **사용 상황**: 광범위한 멀티 에이전트 탐색 또는 공식 벤더 스킬 찾기.

### B4. travisvn/awesome-claude-skills

- **URL**: https://github.com/travisvn/awesome-claude-skills
- **Stars**: 10,866
- **Last push**: 2026-03-16
- **강점**: Claude 전용 큐레이션. obra/superpowers 등 잘 알려진 Claude 스킬 세트 인덱싱.
- **사용 상황**: Claude 전용, 작은 큐레이션 세트.

### B5. BehiSecc/awesome-claude-skills

- **URL**: https://github.com/BehiSecc/awesome-claude-skills
- **Stars**: 8,297
- **Last push**: 2026-04-01
- **강점**: Claude 중심이지만 멀티 툴 참조 포함 (Cursor / Copilot / Windsurf / Zed / Continue.dev). `agentskill.sh` 마켓플레이스 경로 사용.
- **사용 상황**: Claude 우선이지만 멀티 툴 대안도 열려 있을 때.

---

## GitHub 검색 패턴 (폴백)

위 9개 소스 전체에서 약한 매치만 나오면 `WebSearch`로 다음 쿼리 템플릿을 사용:

| 패턴 | 용도 |
|---|---|
| `path:SKILL.md "<도메인 키워드>"` | GitHub 전체에서 SKILL.md 파일 직접 검색 |
| `topic:claude-skills sort:updated` | topic으로 등록된 최근 업데이트 스킬 |
| `"SKILL.md" "allowed-tools" pushed:>2026-01-01` | 최근 몇 달간 활성화된 스킬 |
| `"<앱 이름>" "SKILL.md"` | 앱 특화 스킬 (예: Notion, Slack) |
| `site:github.com "/plugin marketplace add" "<키워드>"` | 설치 가능한 플러그인 마켓플레이스 |

---

## 명시적으로 제외된 소스 (사용 금지)

2026-04-09에 평가 후 제외:

| 소스 | 제외 사유 |
|---|---|
| Skills.sh | 도메인 미응답 (curl 000 + WebFetch 403) |
| skillsmp.com | 도메인 미응답 |
| awesomeclaude.ai | 도메인 미응답 |
| microsoft/skills | Azure / Copilot 전용, Claude Code 미지원 |
| daymade/claude-code-skills | 804 stars, 1k 미만 비공식 기준 미달 |
| mhattingpete/claude-skills-marketplace | 542 stars, 1k 미만 |
| abubakarsiddik31/claude-skills-collection | 594 stars, 1k 미만 |
| karanb192/awesome-claude-skills | 246 stars + 6개월+ 정체 |
| GitHub topic `claude-skills` | 메타 페이지, 큐레이션 소스 아님 |

---

## 한국 소스 현황

2026-04-09 기준, **한국 커뮤니티 소스 중 선정 기준**(1k+ stars + 최근 활동 + 단순 docs 미러 아님)**을 만족하는 곳이 없음**. 확인 후 탈락한 후보:

- `bear2u/my-skills` — 813 ⭐이지만 개인 스킬 믹스(한국어 1줄 설명), 2개월+ 정체
- `modu-ai/cc-plugins` — 58 ⭐, 기준 미달
- `seilk/claude-code-docs` — 366 ⭐, 문서 미러 (스킬 아님)
- `claudecode.co.kr` — 환경에서 도달 불가

**액션**: 기준을 만족하는 한국 소스가 나타나면 위 Group A 또는 B에 동일한 포맷으로 추가. 날짜와 이유는 커밋 메시지에 기록.

---

## 유지보수 스케줄

- **매월**: star 수와 `Last push` 날짜 재검증. 정체된 소스는 제외 리스트로 이동.
- **수시**: 소스가 404가 되거나 archived되면 즉시 교체하고 `최종 검증일` 업데이트.
- **커밋 규칙**: 이 파일을 수정할 때마다 상단의 `최종 검증일` 타임스탬프를 갱신해야 함.
