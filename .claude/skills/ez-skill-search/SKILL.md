---
name: ez-skill-search
description: "AI 에이전트 스킬 검색·비교·추천. Skills.sh 및 주요 GitHub 스킬 라이브러리에서 최소 토큰으로 스킬을 탐색합니다. 'skill search', '스킬 검색', '스킬 찾아줘', '스킬 추천', 'find skill' 키워드 시 사용."
user-invocable: true
argument-hint: "<검색 키워드 또는 요청>"
allowed-tools: WebSearch, WebFetch, Read, Grep
---

# /ez-skill-search — AI 스킬 탐색 스킬

개방형 웹 리서치 대신 짧고 반복 가능한 스킬 검색 패스를 실행합니다.

## 사용법

```
/ez-skill-search GitHub PR 리뷰 스킬 찾아줘
/ez-skill-search Slack + Jira 자동화 설치 가능한 스킬
/ez-skill-search 한국어 문서·번역 워크플로우 스킬
/ez-skill-search best skills for data pipeline
```

## 실행 워크플로우

### Step 1: 브리프 추출

`$ARGUMENTS`에서 최소한의 검색 브리프를 추출합니다:

- 태스크 또는 도메인
- 에이전트 호스트 (명시된 경우: Claude Code, Codex, Cursor, Gemini CLI 등)
- 필요한 통합 또는 도구
- 하드 제약 (언어, 설치 가능 여부, 공식만 등)

### Step 2: 소스 참조

`references/sources.md`를 읽고 최적의 검색 소스를 결정합니다.

### Step 3: 검색 실행

**소스 우선순위 (높은 순):**

| 필요 | 1차 소스 | 백업 |
|---|---|---|
| 최신 설치 가능 스킬 | Skills.sh | sickn33 |
| 도메인 라이브러리 | alirezarezvani/claude-skills | - |
| 공식/벤더 소스 | VoltAgent/awesome-agent-skills | - |
| SaaS/API 워크플로우 | ComposioHQ/awesome-claude-skills | - |
| 큐레이션 숏리스트 | abubakarsiddik31/claude-skills-collection | - |
| 최대 커버리지 | sickn33/antigravity-awesome-skills | - |

**검색 규칙:**
- 2-4 키워드로 시작: `<도구> <태스크> <호스트>` 패턴
- `best`, `top`, `recommended` 요청 시 상위 3개 소스만 검색 (결과 약하면 확장)
- `official` 요청 시 벤더/공식 엔트리 우선
- 설치 요청 시 최단 설치 힌트 포함

### Step 4: 중단 조건

- 3개 강한 매칭 발견 시 중단
- 1개 확실한 승자 + 2개 대안 발견 시 중단
- 첫 패스가 약하거나 반복적일 때만 하위 소스로 확장

### Step 5: 결과 출력

아래 포맷을 사용합니다 (사용자가 다른 형식을 요청하지 않는 한):

```
1줄 판정

| Skill | Source | 매칭 이유 | 설치/사용 힌트 |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

Next action: ...
```

- 기본 3-7행
- 강한 매칭이 없으면 "없음" + 가장 가까운 2개 옵션 제시

## 토큰 절약 규칙

- 매 실행마다 각 소스를 설명하지 않는다
- 긴 README 섹션을 인용하지 않는다
- 충분한 시그널을 얻은 후 추가 브라우징을 하지 않는다
- repo 수준 요약 대신 정확한 skill id, repo 서브패스, 카탈로그 엔트리를 제시한다
- 반복 검색에서 같은 컴팩트 테이블 포맷을 재사용한다
