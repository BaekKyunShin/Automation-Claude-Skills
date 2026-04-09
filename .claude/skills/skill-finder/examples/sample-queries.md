# skill-finder 샘플 쿼리

이 3개 쿼리는 다양한 시나리오에서 스킬의 동작을 검증합니다. `SKILL.md` 또는 `references/sources.md`를 수정한 후 smoke test로 사용하세요.

---

## Query 1 — 한국어, 높은 확신도의 매치 기대

```
/skill-finder PDF 생성 스킬
```

**확인할 것:**

- 응답이 **한국어**여야 함 (쿼리 언어 매칭).
- 단일 랭킹 **매치 결과** 테이블에서 `anthropics/skills`의 PDF 스킬이 1위.
- `Action` 셀에 설치 명령이 verbatim으로 표시:
  ```
  /plugin marketplace add anthropics/skills
  /plugin install pdf@anthropics-skills
  ```
- 그 아래 엔트리는 9개 소스 어디서든 올 수 있음 — 일부는 설치 명령, 일부는 직접 URL — 매치 강도 순으로 랭킹.
- 총 엔트리 ≤ 7개.

**통과 기준**: 사용자가 1행의 설치 명령을 복사·붙여넣기하면 다음 Claude Code 세션에서 동작해야 함.

---

## Query 2 — 영어, 광범위한 탐색

```
/skill-finder Slack automation
```

**확인할 것:**

- 응답이 **영어**여야 함 (쿼리 언어 매칭).
- 단일 결과 테이블에 9개 소스 전체에서 나온 Slack 관련 엔트리가 포함됨. SaaS 자동화 쿼리에서는 보통 `ComposioHQ/awesome-claude-skills`가 상위 소스이지만, 랭킹은 매치 강도로 결정되지 소스 종류로 결정되지 않음.
- 각 행의 `Action` 컬럼이 올바르게 채워짐: embedded 스킬이 있는 행은 설치 명령, awesome list에서 가져온 행은 직접 URL.
- **awesome list URL 자체를 절대 링크하지 말 것** — 항상 실제 스킬 소스로 링크를 따라가야 함.

**통과 기준**: 소스 종류와 상관없이 최소 2개의 실행 가능한 행(설치 명령 또는 직접 스킬 URL)을 사용자가 얻어야 함.

---

## Query 3 — 강한 매치 없음, 한국어 (회귀 테스트)

```
/skill-finder 한글 HWP 문서 생성
```

**확인할 것:**

- 응답이 **한국어**여야 함.
- **매치 결과** 테이블이 폴백 템플릿으로 대체됨:
  ```
  ## 매치 없음

  가장 가까운 2개 대안:
  - anthropics/skills의 docx 스킬 — <이유>
  - anthropics/skills의 pdf 스킬 — <이유>

  대안 경로:
  pyhwpx 또는 python-hwpx 라이브러리를 래핑한 새 스킬을 만드는 것이 빠릅니다.
  ```
- **존재하지 않는 스킬의 설치 명령을 날조하지 말 것**.

**통과 기준**: 스킬이 정직하게 실패를 보고하고 올바른 폴백 경로(pyhwpx 계열 라이브러리로 새 스킬 구축)를 제안해야 함.

---

## 실행 방법

이 프로젝트가 로드된 Claude Code 세션에서:

1. 위 쿼리 중 하나를 입력.
2. "확인할 것" 목록과 출력을 비교.
3. 실패한 체크가 있으면 `SKILL.md` (워크플로우) 또는 `references/sources.md` (소스 메타데이터)를 검사 후 수정.

## 새 샘플 쿼리 추가

새로운 엣지 케이스를 발견하면 (예: 너무 많은 결과를 반환하는 쿼리, 조용히 실패하는 쿼리) 같은 포맷으로 여기에 추가: 쿼리 → 예상 동작 → 통과 기준.
