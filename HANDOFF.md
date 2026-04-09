# HANDOFF — claude/kpc-hangul-docgen 브랜치 세션 인수인계

> 이 문서는 새 Claude Code 세션에서 작업을 이어받기 위한 인수인계서입니다.
> Step 4가 끝나 머지되면 삭제하세요.

---

## 한 줄 요약

**죠르디 방법론 Step 2~4를 이 브랜치에서 진행. Step 2(한글 문서 생성 스킬 조사)부터 시작.**

---

## 어디까지 왔나

### Step 1 — 완료 (main에 머지됨, PR #1)

- **`skill-finder` 스킬 제작 완료**: `.claude/skills/skill-finder/`
- 9개 검증된 소스에서 Claude Code Skill을 exhaustive 검색하는 reusable 메타 도구
- `context: fork` + `agent: general-purpose` + `effort: high`로 서브에이전트 격리 실행
- 출력: 단일 랭킹 테이블, Action 컬럼에 설치 명령 또는 직접 URL
- **죠르디 원본 `ez-skill-search`도 참조용으로 `.claude/skills/ez-skill-search/`에 있음** (직접 쓰지 말 것, skill-finder가 개선판)

### Step 2~4 — 이 브랜치에서 진행

2. skill-finder로 한글/HWP 문서 생성 스킬 조사
3. 발견한 스킬들의 장점을 합성한 `kpc-hangul-docgen` 신규 스킬 제작
4. KPC 직무교육센터 도메인 지식 주입 (실제 템플릿, 폰트, 양식 규칙)

---

## 사용자 배경 (중요)

- **소속**: 한국생산성본부(KPC) 직무교육센터 팀장
- **역할**: 강의·멘토링·업무자동화에 Claude Code 활용 중. 삼육대 캡스톤 멘토링, CEO 아카데미 강의 담당
- **최종 목표**: 한글 문서 자동 생성 스킬을 본인 업무·강의에 실전 적용
- **방법론 출처**: "상담하는 죠르디" 강사와의 카카오톡 대화. 3단계 합성 워크플로우를 배워서 본인 도메인에 적용 중

### 대화 스타일 선호 (꼭 지켜주세요)

- **한국어**로 응답
- **두괄식** (결론 먼저)
- **간결** (밀도 > 길이). 장문 답변 싫어함
- **실전 디테일 위주**. 추상적 조언·일반론 금지
- **이모지 쓰지 말 것** (요청 시에만)
- **공식 문서·검증된 근거 기반**으로 의사결정. 추측 금지

---

## 지금 당장 해야 할 일 (Step 2)

사용자가 "A로 고" 하면 다음을 실행:

```
/skill-finder 한글 HWP 문서 생성
```

또는 자연어로 동일 쿼리. 그리고 결과를 바탕으로 Step 3(합성 스킬 설계) 준비.

**skill-finder가 기대대로 동작할 주요 시나리오**:
- 한국어 응답
- 매치 결과 표에 anthropics/skills의 docx/pdf 등 근접 대안 포함
- 강한 매치가 없으면 "매치 없음" + pyhwpx/python-hwpx 기반 새 스킬 제작 권장

---

## 필독 파일 (이 순서로 읽으세요)

1. `README.md` — 레포 목적 + 죠르디 방법론 개요
2. `.claude/skills/skill-finder/SKILL.md` — Step 1 결과물, Step 2에서 실행할 스킬
3. `.claude/skills/skill-finder/references/sources.md` — 9개 검증 소스 (Group A/B, 제외 리스트, 한국 소스 현황)
4. `.claude/skills/skill-finder/examples/sample-queries.md` — 기대 동작 검증용 쿼리 3개

**참조만 하고 복사하지 말 것**:
- `.claude/skills/ez-skill-search/` — 죠르디 원본. 여러 버그·누락이 있어서 skill-finder가 개선판임. 새 스킬 만들 때 여기서 복사 금지.

---

## 이미 내려진 설계 결정 (번복 금지)

### skill-finder 관련
- `description` 250자 이내 (Claude Code 스펙)
- `allowed-tools`는 space-separated (comma 아님)
- `user-invocable: true` 명시 금지 (기본값)
- Tier·Stop condition 없이 exhaustive 검색
- 단일 랭킹 테이블 출력 (Embedded/Index 그룹 분리 안 함)
- Group A/B 라벨은 sources.md에서 **검색 방법 차이 설명용으로만** 유지 (출력 그룹핑 아님)
- `Action` 컬럼 하나가 설치 명령 또는 URL 담당 (배지 없음)

### 번역 원칙
- SKILL.md 본문, sources.md, sample-queries.md의 **prose는 한글**
- 기술 용어(`$ARGUMENTS`, `WebFetch`, `/plugin marketplace add ...`, 리포 이름, URL, 숫자, `Group A/B`, `Action` 등)는 **영어 유지**
- YAML frontmatter의 `description`은 한/영 혼합 (auto-invoke 트리거용)

### 9개 검증 소스 (번복 금지, 월 1회 재검증만)

**Group A — Embedded**:
1. anthropics/skills (113.7k ⭐)
2. sickn33/antigravity-awesome-skills (31.8k ⭐, 1,392+ 스킬)
3. alirezarezvani/claude-skills (10.2k ⭐, 156+ 스킬)
4. huggingface/skills (10.1k ⭐, ML 특화)

**Group B — Index**:
5. ComposioHQ/awesome-claude-skills (52.4k ⭐)
6. hesreallyhim/awesome-claude-code (37.6k ⭐)
7. VoltAgent/awesome-agent-skills (14.9k ⭐)
8. travisvn/awesome-claude-skills (10.9k ⭐)
9. BehiSecc/awesome-claude-skills (8.3k ⭐)

---

## 알려진 함정 / 주의사항

### 기술적
- **GitHub push 권한**: BaekKyunShin 계정에 Claude GitHub App이 설치되어 있어야 push 가능 (`https://github.com/apps/claude/installations/new`로 설치). 현재는 설치 완료 상태.
- **MCP 도구 연결/끊김**: GitHub MCP 도구(`mcp__github__*`)가 세션 중 자주 disconnect됨. 필요 시 ToolSearch로 `select:<tool_name>` 형식으로 재로딩.
- **API 과부하**: Agent/WebFetch 호출 중 529 overloaded 에러가 종종 발생. 재시도 필요.
- **로컬 git proxy는 read/write 모두 가능**하지만, GitHub App 설치 전에는 write가 403으로 막힘.

### 설계적
- **한국 커뮤니티 소스 0개**: bear2u/my-skills, modu-ai/cc-plugins, seilk/claude-code-docs 등 모두 기준(1k+ ⭐ + 최근 3개월 활동) 미달. sources.md에 기록됨. Step 3에서 한국 도메인 컨텍스트는 **직접 구축**해야 함.
- **ez-skill-search는 복사 금지**: description 250자 초과 가능성, allowed-tools 콤마 구분(스펙 위반), 한국 소스·anthropics/skills 누락. 참조만 가능.

---

## Step 2 이후 예상 흐름

### Step 2: 조사
- `/skill-finder 한글 HWP 문서 생성` 실행
- 추가로 Python 라이브러리(`pyhwpx`, `python-hwpx`, `hwp5`) 생태계 조사 필요할 가능성 높음 (한글 전용 스킬이 거의 없을 것으로 예상됨)
- 결과를 `.claude/skills/kpc-hangul-docgen/research.md` 같은 임시 파일에 기록해서 Step 3 자료로 활용

### Step 3: 합성 스킬 제작
- 경로: `.claude/skills/kpc-hangul-docgen/`
- 구조: `SKILL.md` + `references/` + `scripts/` + `templates/` + `examples/`
- skill-finder와 동일한 스펙 원칙 준수 (description 250자, allowed-tools space-separated 등)
- 한글 prose, 기술 용어 영어 원칙 동일

### Step 4: 도메인 주입
- KPC 실제 사용 문서 양식 (강의계획서, 수료증, 출장보고서, 품의서, 교육 안내서) 반영
- 폰트(함초롬바탕, HY헤드라인M 등), 여백, 로고 위치 등 브랜딩 규칙
- 사용자가 실제 템플릿 파일(.hwpx)을 공유해줄 가능성 있음 → `templates/raw/`에 받아서 `Contents/section0.xml` 파싱

---

## 커밋·브랜치 규칙

- **브랜치**: `claude/kpc-hangul-docgen` (이미 main에서 분기, push 완료)
- **main에 직접 push 금지**. 모든 작업은 이 브랜치에서.
- **PR 머지**: 사용자가 "PR 만들어줘" / "머지해줘"라고 명시적으로 말할 때만. 임의로 생성·머지 금지.
- **커밋 메시지 스타일** (예시):
  ```
  feat(kpc-hangul-docgen): add initial skill scaffold
  
  <본문 설명>
  
  https://claude.ai/code/session_<id>
  ```
- **squash merge** 선호 (Step 1 PR에서 사용한 방식)

---

## 새 세션 시작 프롬프트 (복붙용)

새 Claude Code 세션을 열고 아래 프롬프트를 그대로 붙여넣으세요:

```
이 레포의 claude/kpc-hangul-docgen 브랜치에서 이어서 작업할 거야.

먼저 HANDOFF.md를 읽고, 현재 상태와 다음 할 일을 파악해줘.
그다음 필독 파일 목록(README.md, .claude/skills/skill-finder/SKILL.md,
references/sources.md, examples/sample-queries.md)을 읽고, 준비되면
Step 2(한글 HWP 문서 생성 스킬 조사)로 넘어갈 수 있는지 확인해줘.

단, 절대 ez-skill-search 폴더는 참조만 하고 복사하지 말 것.
```

---

**작성일**: 2026-04-09
**작성 세션**: Step 1 완료 시점 (PR #1 머지 직후)
**다음 단계**: Step 2 — `/skill-finder 한글 HWP 문서 생성`
