---
name: hwpx-docgen
description: "HWPX 한글 문서 생성·편집·분석·표 만들기. 템플릿 기반 문서 생성, 플레이스홀더 치환, 텍스트 추출, 구조 검증. Trigger: 한글 문서, HWPX, hwpx 생성, hwpx 편집, hwpx 분석, 표 만들기"
context: fork
agent: general-purpose
effort: high
allowed-tools: Bash Read Grep Write Edit
---

# hwpx-docgen

HWPX(한컴오피스 XML) 문서를 생성·편집·분석하는 스킬. 템플릿 기반 문서 생성, 표 만들기, 플레이스홀더 치환, 텍스트 추출, 구조 검증을 지원합니다.

## 쿼리

$ARGUMENTS

## 의사결정 트리

$ARGUMENTS를 분석해서 의도 분류:

| 키워드 | 워크플로우 |
|---|---|
| "생성", "만들어", "create", "new" | → Workflow 1 (문서 생성) |
| "편집", "수정", "바꿔", "치환", "edit" | → Workflow 2 (문서 편집) |
| "분석", "추출", "읽어", "analyze" | → Workflow 3 (문서 분석) |
| "표", "테이블", "table" | → Workflow 4 (표 생성) |
| "템플릿", "template", "목록", "list" | → Workflow 5 (템플릿 관리) |

---

## Workflow 1 — 문서 생성

### Step 1: 레퍼런스 로드

[references/owpml-format.md](references/owpml-format.md)를 읽습니다. XML 구조 규칙과 스타일 참조 시스템을 확인합니다.

### Step 2: 템플릿 선택

사용자 요청에서 문서 유형을 파악하고 해당 템플릿을 선택합니다.

| 유형 | 템플릿 | 플레이스홀더 |
|---|---|---|
| 공문 | `templates/gonmun/` | 발신기관, 수신, 제목, 본문, 날짜, 발신자 |
| 보고서 | `templates/report/` | 제목, 작성일, 작성자, 장N_제목, 장N_본문 |
| 회의록 | `templates/minutes/` | 회의명, 일시, 장소, 참석자, 안건, 논의사항, 결정사항, 후속조치 |
| 제안서 | `templates/proposal/` | 제목, 부제, 기관명, 날짜, 개요, 목적, 세부내용, 예산, 기대효과 |
| 기본 | `templates/base/` | (없음 — 빈 문서) |

### Step 3: 콘텐츠 JSON 구성

사용자 입력을 아래 형태의 JSON으로 변환합니다:

```json
{
  "paragraphs": [
    {"type": "heading", "level": 1, "text": "제목"},
    {"type": "text", "text": "본문 내용"},
    {"type": "table", "rows": 3, "cols": 4, "data": [["a","b","c","d"], ...]}
  ]
}
```

### Step 4: 빌드

```bash
python scripts/build_hwpx.py --template templates/<type>/ --content content.json --output work/
```

### Step 5: 후처리

```bash
python scripts/validate_hwpx.py output.hwpx
```

### Step 6: 결과 전달

생성된 `.hwpx` 파일 경로를 사용자에게 알려줍니다. 검증 결과도 함께 보고합니다.

---

## Workflow 2 — 문서 편집

### Step 1: 언패킹

```bash
python scripts/unpack_hwpx.py input.hwpx work/
```

### Step 2: 분석

```bash
python scripts/analyze_template.py work/
```

현재 구조(스타일, 단락, 표, 플레이스홀더)를 파악합니다.

### Step 3: 편집 유형 판단

- **플레이스홀더 치환** → 매핑 JSON 생성 후:
  ```bash
  python scripts/zip_replace_all.py work/ --mapping mapping.json --auto-fix-ns
  ```
- **구조 변경** → `work/Contents/section0.xml`을 Read → Edit으로 직접 수정
- **표 수정/추가** → Workflow 4로 위임

### Step 4: 검증 + 리패킹

```bash
python scripts/fix_namespaces.py work/
python scripts/validate_hwpx.py work/
python scripts/page_guard.py work/ --ref-pages <원본_페이지_수>
python scripts/pack_hwpx.py work/ output.hwpx
```

---

## Workflow 3 — 문서 분석

### Step 1: 언패킹

```bash
python scripts/unpack_hwpx.py input.hwpx work/
```

### Step 2: 텍스트 추출

```bash
python scripts/extract_text.py work/ --format <plain|markdown|json>
```

### Step 3: 구조 분석

```bash
python scripts/analyze_template.py work/
```

### Step 4: 검증

```bash
python scripts/validate_hwpx.py work/
```

### Step 5: 결과 보고

추출된 텍스트 + 구조 분석 + 검증 결과를 사용자에게 반환합니다.

---

## Workflow 4 — 표 생성

### Step 1: 레퍼런스 로드

[references/table-xml-spec.md](references/table-xml-spec.md)를 읽습니다. 셀 병합, borderFill, 크기 계산 규칙을 확인합니다.

### Step 2: 표 명세 파악

사용자 요청에서 행/열 수, 셀 내용, 병합 정보를 추출합니다.

### Step 3: 표 XML 생성

```bash
python scripts/table_gen.py --rows <n> --cols <m> --data '<json_2d_array>' --merge '<json_merge_spec>' --output table.xml
```

**data 형식**: `[["헤더1", "헤더2"], ["데이터1", "데이터2"]]`
**merge 형식**: `[{"row": 0, "col": 0, "rowSpan": 1, "colSpan": 2}]`

### Step 4: 삽입 (기존 문서에 추가할 경우)

1. 문서 언패킹
2. `section0.xml`에서 삽입 위치(hp:p) 파악
3. 생성된 `hp:tbl` 요소를 해당 위치에 삽입
4. 네임스페이스 정리 + 검증 + 리패킹

### Step 5: 독립 문서 (새 문서로 만들 경우)

`base/` 템플릿으로 Workflow 1을 실행하되 `"type": "table"` 항목 포함.

---

## Workflow 5 — 템플릿 관리

### 목록

`templates/` 디렉터리를 스캔:

```bash
ls templates/
```

각 템플릿의 이름과 용도를 보고합니다:

| 이름 | 용도 |
|---|---|
| base | 최소 골격 (빈 문서) |
| gonmun | 공문 (발신·수신·제목·본문) |
| report | 보고서 (장·절 계층 구조) |
| minutes | 회의록 (메타 표 + 안건·논의·결정·후속) |
| proposal | 제안서 (개요·목적·세부내용·예산·기대효과) |

### 분석

```bash
python scripts/analyze_template.py templates/<name>/
```

### 추가 (사용자가 .hwpx 파일 제공 시)

```bash
python scripts/unpack_hwpx.py user_file.hwpx templates/<new_name>/
python scripts/analyze_template.py templates/<new_name>/
```

---

## 규칙

### XML 구조

- `section0.xml`의 첫 `hp:p`에 `secPr` + `colPr` **필수**. 삭제/이동 절대 금지.
- 모든 `hp:r`에 `charPrIDRef` 필수. 모든 `hp:p`에 `paraPrIDRef` 필수.
- 참조하는 ID는 `header.xml`에 정의되어 있어야 함.

### 네임스페이스

- python-hwpx가 네임스페이스를 내부 관리. 별도 정리 불필요.

### ZIP 구조

- `mimetype`은 ZIP 첫 번째 엔트리, `ZIP_STORED` (비압축).
- `pack_hwpx.py`가 이를 자동 처리.

### 검증

- 모든 생성/편집 작업 후 `validate_hwpx.py` 실행.
- `page_guard.py`는 참고용 경고만 출력 (차단하지 않음).

### 플레이스홀더

- `{{이중중괄호}}` 형식 사용.
- XML 태그 문자(`<`, `>`, `&`)를 플레이스홀더 키로 사용 금지.

### 의존성

- **필수**: Python 3.8+, `pip install python-hwpx lxml`
- python-hwpx가 문서 생성·편집·추출·검증을 담당. lxml은 python-hwpx 내부 의존성.

## 추가 리소스

- [references/owpml-format.md](references/owpml-format.md) — OWPML XML 요소 레퍼런스
- [references/table-xml-spec.md](references/table-xml-spec.md) — 표 XML 구조 상세
- [examples/sample-queries.md](examples/sample-queries.md) — 샘플 쿼리 + 기대 동작
- [research.md](research.md) — 기존 HWPX 스킬 조사 보고서
