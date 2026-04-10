# hwpx-docgen 샘플 쿼리

SKILL.md 또는 scripts를 수정한 후 smoke test로 사용하세요.

---

## Query 1 — 공문 생성

```
/hwpx-docgen 공문 만들어줘. 발신기관: 한국생산성본부, 수신: 삼육대학교 총장, 제목: 캡스톤 디자인 멘토링 협조 요청
```

**확인할 것:**
- `gonmun/` 템플릿 사용
- `{{발신기관}}`, `{{수신}}`, `{{제목}}` 플레이스홀더 치환
- 출력 `.hwpx` 파일이 `validate_hwpx.py` PASS
- 한컴오피스에서 열었을 때 공문 서식 유지

---

## Query 2 — 표 생성

```
/hwpx-docgen 3행 4열 표 만들어줘. 첫 행은 헤더. 열: 이름, 부서, 직급, 연락처. 데이터: 홍길동/교육팀/팀장/010-1234, 김영희/기획팀/과장/010-5678
```

**확인할 것:**
- `table_gen.py`로 3x4 표 생성
- 첫 행에 `borderFillIDRef="3"` (회색 배경 헤더)
- 데이터 행에 `borderFillIDRef="2"` (흰 배경)
- `charPrIDRef="3"` (헤더 굵게) 적용
- 셀 내용 정확히 매핑

---

## Query 3 — 기존 문서 편집 (플레이스홀더 치환)

```
/hwpx-docgen report.hwpx에서 {{작성자}}를 "신백균"으로, {{작성일}}을 "2026-04-10"으로 바꿔줘
```

**확인할 것:**
- `unpack_hwpx.py` → `zip_replace_all.py` → `validate_hwpx.py` → `pack_hwpx.py` 순서 실행
- 모든 XML 파일에서 치환 적용 (ZIP-level 전역)
- 네임스페이스 깨지지 않음

---

## Query 4 — 문서 분석 + 텍스트 추출

```
/hwpx-docgen document.hwpx 분석해줘. 마크다운으로 텍스트도 추출해줘.
```

**확인할 것:**
- `analyze_template.py` 실행: 페이지 크기, 단락 수, 표 수, 스타일 목록 보고
- `extract_text.py --format markdown` 실행: 표를 마크다운 표로 변환
- `validate_hwpx.py` 실행: 구조 검증 결과 포함

---

## Query 5 — 템플릿 목록

```
/hwpx-docgen 사용 가능한 템플릿 목록 보여줘
```

**확인할 것:**
- 5개 템플릿 (base, gonmun, report, minutes, proposal) 목록 반환
- 각 템플릿의 용도와 플레이스홀더 목록 포함

---

## 실행 방법

1. 이 프로젝트가 로드된 Claude Code 세션에서 위 쿼리 입력
2. "확인할 것" 목록과 실제 출력을 비교
3. 실패 시 `SKILL.md` (워크플로우) 또는 해당 `scripts/` 검사 후 수정
