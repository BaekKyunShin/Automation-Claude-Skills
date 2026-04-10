# hwpx-docgen 스크립트 API 레퍼런스

모든 스크립트는 `scripts/` 디렉터리에 있으며 **python-hwpx 2.9+** 기반입니다.

**사전 설치**: `pip install python-hwpx lxml`

---

## 일반 규칙

- 종료 코드: `0` 성공, `1` 검증 실패, `2` 치명적 오류
- 모든 스크립트는 `.hwpx` 파일을 직접 입출력 (언팩 불필요)
- 네임스페이스는 python-hwpx가 내부 관리 → `fix_namespaces.py` 불필요

---

## 스크립트 목록 (9개)

### build_hwpx.py
```
python scripts/build_hwpx.py --template <dir_or_hwpx> --content <json> --output <output.hwpx>
python scripts/build_hwpx.py --content <json> --output <output.hwpx>  # 템플릿 없이 신규
```
`HwpxDocument.open()` 또는 `.new()`로 문서 생성. 콘텐츠 JSON의 heading/text/table을 `add_paragraph()`/`add_table()`로 추가.

### table_gen.py
```
python scripts/table_gen.py --rows <n> --cols <m> --data '<json>' [--merge '<json>'] [--output <file.hwpx>]
```
`doc.add_table()` → `tbl.set_cell_text()` → `tbl.merge_cells()`로 표 생성. 출력 생략 시 마크다운 미리보기.

### extract_text.py
```
python scripts/extract_text.py <file.hwpx> --format <plain|markdown|json>
```
`doc.export_text()`, `doc.export_markdown()`, `TextExtractor`로 추출.

### validate_hwpx.py
```
python scripts/validate_hwpx.py <file.hwpx_or_dir>
```
`doc.validate()` 내장 검증 + 디렉터리 모드 시 ZIP 구조 체크. PASS/WARN/FAIL 보고.

### analyze_template.py
```
python scripts/analyze_template.py <file.hwpx>
```
`doc.char_properties`, `doc.paragraph_properties`, `doc.styles`, `doc.border_fills`로 메타데이터 분석. 플레이스홀더 `{{...}}` 자동 탐지.

### zip_replace_all.py
```
python scripts/zip_replace_all.py <work_dir> --mapping <json_file> [--auto-fix-ns]
```
모든 XML에서 `{{key}}`를 `value`로 전역 치환. 문자열 레벨 (XML 파싱 없음).

### unpack_hwpx.py
```
python scripts/unpack_hwpx.py <input.hwpx> <output_dir>
```
HWPX ZIP을 디렉터리로 해제. 필수 파일 누락 시 WARN.

### pack_hwpx.py
```
python scripts/pack_hwpx.py <input_dir> <output.hwpx>
```
디렉터리를 HWPX ZIP으로 패킹. mimetype 첫 번째 엔트리 + ZIP_STORED.

### page_guard.py
```
python scripts/page_guard.py <file.hwpx> --ref-pages <n>
```
`doc.paragraphs` 수 기반 페이지 추정. 경고만 출력 (차단 안 함).

---

## 삭제된 스크립트

| 스크립트 | 삭제 이유 |
|---|---|
| `fix_namespaces.py` | python-hwpx가 네임스페이스를 내부 관리 → 불필요 |
