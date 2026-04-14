# skill-finder

> **AI 분석용 안내**: 이 문서는 AI가 이 스킬의 목적·구조·사용법을 빠르게 파악하기 위한 이정표입니다. 실행 매뉴얼은 [SKILL.md](SKILL.md)를 참조하세요.

---

## 한 줄 요약

새 스킬을 만들기 전에 **9개 검증된 소스**에서 이미 존재하는 Claude Code Skill을 검색해 컴팩트한 랭킹 테이블로 반환하는 **범용 검색 스킬**.

---

## 무엇을 할 수 있는가

| 시나리오 | 입력 예시 | 출력 |
|---|---|---|
| 기존 스킬 탐색 | "PDF 읽는 스킬 찾아줘" | 9개 소스에서 매치된 스킬 랭킹 (최대 7개) |
| 중복 방지 | "스킬 만들기 전에 비슷한 거 있나 확인해줘" | 유사 스킬 + 설치 명령 |
| 소스 비교 | "find skill for excel automation" | 매치 강도순 정렬 + ⭐ 별점 |

**범용성**: 특정 도메인에 종속되지 않고 어떤 주제든 검색 가능 (한글 지원).

---

## 핵심 설계 원칙

1. **9개 소스 전체 검색** (exhaustive) — Anthropic 공식부터 awesome list까지 망라
2. **단일 랭킹 리스트** — 9개 소스를 별도로 보여주지 않고 통합 7개 엔트리로 압축
3. **사용자 언어 매칭** — 한국어 쿼리 → 한국어 응답, 영어 쿼리 → 영어 응답
4. **설치 명령 교차검증** — 날조 금지. 확실하지 않으면 `(manual: git clone ...)` 폴백
5. **정직한 보고** — 매치 없으면 "매치 없음"이라고 명시 + 대안 경로 제안

---

## 검색 대상 9개 소스

**Group A (Embedded — 리포 내 SKILL.md 직접 검색)**:
1. `anthropics/skills` — Anthropic 공식
2. `sickn33/antigravity-awesome-skills` — 최대 규모 카탈로그
3. `alirezarezvani/claude-skills` — 9개 도메인 폴더
4. `huggingface/skills` — ML/데이터 특화

**Group B (Index — awesome list / 카탈로그)**:
5. `ComposioHQ/awesome-claude-skills` — SaaS/API 연동
6. `hesreallyhim/awesome-claude-code` — 광범위한 큐레이션
7. `VoltAgent/awesome-agent-skills` — 1,000+ 멀티 에이전트
8. `travisvn/awesome-claude-skills` — Claude 전용 큐레이션
9. `BehiSecc/awesome-claude-skills` — Claude 중심 + 멀티 툴

---

## 폴더 구조

```
skill-finder/
├── SKILL.md                          # [핵심] Claude가 읽는 워크플로우 매뉴얼
├── README.md                         # 이 파일 (AI/사람 분석용)
│
├── references/
│   └── sources.md                    # 9개 소스 메타데이터 + GitHub 검색 패턴
│
└── examples/
    └── sample-queries.md             # 샘플 쿼리 3개 + 기대 출력 형식
```

---

## 의존성

**없음.** 외부 라이브러리 불필요.

Claude Code 내장 도구만 사용:
- `WebSearch` — 일반 웹 검색
- `WebFetch` — GitHub 리포·README fetch
- `Read`, `Grep` — 로컬 sources.md 참조

---

## 동작 플로우

```
사용자 쿼리 ("스킬 찾아줘 ...")
    │
    ▼
[Step 1] references/sources.md 로드 (9개 소스 정의)
    │
    ▼
[Step 2] 9개 소스 병렬 검색
    ├─ Group A: 리포 트리 fetch → 스킬 이름·설명 매칭
    └─ Group B: README fetch → 링크 텍스트 스캔
    │
    ▼
[Step 3] 매치 강도 랭킹 (이름 일치 > 설명 일치 > 카테고리 일치)
    │
    ▼
[Step 4] Action 컬럼 채우기 (설치 명령 교차검증)
    │
    ▼
[Step 5] 출력 (최대 7개 엔트리)
    │
    ├─ 강한 매치 있음: 랭킹 테이블 + Next action
    └─ 매치 없음: 대안 2개 + 직접 만들기 권장
```

---

## 출력 포맷

```markdown
## 판정 (한 줄)
<요약>

## 매치 결과
| # | 스킬 | 출처 | ⭐ | Action | 매치 이유 |
|---|---|---|---|---|---|
| 1 | <skill-id> | <owner/repo> | <stars> | `<설치 명령>` | <왜 매치> |

## Next action
<권장 다음 단계>
```

---

## 트리거 키워드

다음 키워드가 사용자 요청에 포함되면 Claude가 이 스킬을 자동 호출합니다:

`스킬 찾아줘`, `find skill for X`, `search skills`, `any skill for Y`, **또는 새 스킬을 만들기 전 중복 방지 체크**

---

## 제약 사항

| 항목 | 내용 |
|---|---|
| **출력 제한** | 총 7개 엔트리 (그 이상은 판정 줄에 남은 개수 언급) |
| **인용 금지** | 긴 README 인용 불가. 리포 경로·스킬 ID·설치 명령만 반환 |
| **실행 컨텍스트** | `context: fork` — 포크된 서브에이전트에서 실행. 자체 완결적 작성 필요 |

---

## 더 알아보기

- 실행 매뉴얼: [SKILL.md](SKILL.md)
- 9개 소스 상세: [references/sources.md](references/sources.md)
- 샘플 쿼리: [examples/sample-queries.md](examples/sample-queries.md)
