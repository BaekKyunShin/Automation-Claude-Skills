---
name: skill-finder
description: "Finds Claude Code Skills from 9 verified sources (Anthropic, HuggingFace, large catalogs). Trigger phrases: 스킬 찾아줘, find skill for X, search skills, any skill for Y, or before creating a new skill to avoid duplication."
context: fork
agent: general-purpose
effort: high
allowed-tools: WebSearch WebFetch Read Grep
---

# skill-finder

새 스킬을 만들기 전에 9개의 검증된 소스에서 이미 존재하는 Claude Code Skill을 검색합니다. 복사 즉시 실행 가능한 설치 명령과 함께 컴팩트한 랭킹 테이블을 반환합니다.

## 쿼리

$ARGUMENTS

## 워크플로우

### Step 1 — 소스 가이드 로드

[references/sources.md](references/sources.md)를 읽습니다. 이 파일에는 9개 검증 소스의 설치 명령과 검색 주의사항이 있습니다. **이 SKILL.md에 소스 URL을 하드코딩하지 말 것** — 항상 `sources.md`를 참조해서 업데이트가 한 곳에서 관리되도록 합니다.

`sources.md`에 정의된 두 그룹에 주의:

- **Group A (Embedded)**: 리포 안에 실제 `SKILL.md` 파일이 있는 저장소. 검색 방법: 리포 트리 또는 skills 디렉터리를 fetch해서 쿼리와 일치하는 스킬 이름을 찾기.
- **Group B (Index)**: 외부 링크만 모아놓은 awesome list / 카탈로그. 검색 방법: README를 fetch해서 링크 텍스트와 설명에서 매치 찾기.

이 그룹 구분은 **각 소스를 어떻게 검색할지**만 설명합니다. 결과를 어떻게 표시할지와는 무관합니다.

### Step 2 — 9개 소스 전부 검색 (exhaustive)

모든 소스를 검색합니다. 가능한 경우 병렬 tool 호출. 응답 언어는 쿼리 언어에 맞춥니다 (한국어 입력 → 한국어 응답).

1. `anthropics/skills` (Group A) — 리포 트리 fetch, 일치하는 스킬 이름 찾기
2. `sickn33/antigravity-awesome-skills` (Group A) — 최대 규모 카탈로그, skills 인덱스 검색
3. `alirezarezvani/claude-skills` (Group A) — 9개 도메인 폴더 탐색
4. `huggingface/skills` (Group A) — 쿼리가 ML / 데이터 / HF 생태계와 관련된 경우에만
5. `ComposioHQ/awesome-claude-skills` (Group B) — SaaS / API 연동에 강함
6. `hesreallyhim/awesome-claude-code` (Group B) — 광범위한 Claude Code 큐레이션
7. `VoltAgent/awesome-agent-skills` (Group B) — 1,000+ 멀티 에이전트 엔트리
8. `travisvn/awesome-claude-skills` (Group B) — Claude 전용 큐레이션
9. `BehiSecc/awesome-claude-skills` (Group B) — Claude 중심 + 멀티 툴 참조 포함

**9개 모두 약한 시그널만 반환하면**, `sources.md`의 GitHub 직접 검색 패턴으로 폴백 (`path:SKILL.md "<키워드>"` 등).

### Step 3 — 매치 랭킹

9개 소스 전체에서 **단일 랭킹 리스트**를 생성합니다. 매치 강도 순으로 랭킹:

1. 스킬 이름에 정확한 키워드 매치
2. 설명에 정확한 키워드 매치
3. 관련 용어 매치
4. 약한 시그널 (카테고리만 일치)

**출력은 총 7개 엔트리로 제한.** 더 있으면 판정 줄에 남은 개수를 언급합니다.

### Step 4 — `Action` 값 교차검증

각 엔트리의 `Action` 컬럼을 다음 중 하나로 채웁니다:

- 복사 즉시 실행 가능한 설치 명령 (예: `/plugin marketplace add anthropics/skills` 다음에 `/plugin install pdf@anthropics-skills`) — 해당 소스 리포 README와 일치하는지 확인.
- 스킬의 직접 URL — Index 엔트리인 경우 awesome list URL이 아닌 **실제 스킬 목적지**로 링크.
- `(manual: git clone <url>)` — 설치 경로가 문서화되지 않은 경우에만.

**설치 명령을 날조하지 말 것.** 확실하지 않으면 `(manual: ...)` 형태로 폴백.

### Step 5 — 출력

사용자 언어로 응답. 아래 포맷을 그대로 사용.

## 출력 포맷

```
## 판정 (한 줄)
<한 문장 요약. 예: "Anthropic 공식 docx 스킬이 1순위, 그 외 2개 관련 스킬 발견.">

## 매치 결과

| # | 스킬 | 출처 | ⭐ | Action | 매치 이유 |
|---|---|---|---|---|---|
| 1 | <skill-id> | <owner/repo> | <stars> | `<설치 명령>` 또는 `<https://url>` | <왜 매치되는지> |

## Next action
<한 문장. 예: "1번 스킬을 바로 설치해서 써보세요." 또는 "강한 매치가 없으므로 새 스킬을 직접 만드는 것이 빠릅니다.">
```

**어디에서도 강한 매치가 없으면**, 결과 테이블을 다음으로 대체:

```
## 매치 없음

가장 가까운 2개 대안:
- <링크 1> — <왜 유사한지>
- <링크 2> — <왜 유사한지>

대안 경로:
<한 문장. 예: "관련 Python 라이브러리를 직접 래핑한 새 스킬을 만드는 것이 빠릅니다.">
```

## 규칙

- **긴 README 인용 금지.** 리포 경로, 스킬 ID, 설치 명령만 반환.
- **설치 명령 교차검증.** 날조 금지. 확실하지 않으면 `(manual: git clone …)` 출력.
- **사용자 언어 매칭.** 한국어 쿼리 → 한국어 응답. 영어 쿼리 → 영어 응답.
- **정직한 보고.** 매치가 없으면 "매치 없음 / No strong match"이라고 하고 폴백 경로 제안.
- **출력은 총 7개 엔트리로 제한.**
- **`context: fork` 준수.** 이 스킬은 포크된 서브에이전트에서 실행됩니다. 최종 답변만 메인 대화로 전달되므로 자체 완결적으로 작성할 것.

## 추가 리소스

- [references/sources.md](references/sources.md) — 9개 검증 소스의 메타데이터와 GitHub 검색 패턴.
- [examples/sample-queries.md](examples/sample-queries.md) — 샘플 쿼리 3개와 기대 출력 형식.
