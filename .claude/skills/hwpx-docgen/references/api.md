# hwpx-docgen 스크립트 API 레퍼런스

모든 스크립트는 `scripts/` 디렉터리에 있으며 Python 3.6+로 실행합니다.

---

## 일반 규칙

- 종료 코드: `0` 성공, `1` 검증 실패, `2` 치명적 오류
- 체이닝 순서: `unpack → (편집) → fix_namespaces → validate → pack`
- 모든 경로는 상대/절대 모두 지원

---

## 스크립트 목록

### unpack_hwpx.py
```
python scripts/unpack_hwpx.py <input.hwpx> <output_dir>
```
HWPX ZIP을 디렉터리로 해제. 필수 파일 누락 시 WARN 출력.

### pack_hwpx.py
```
python scripts/pack_hwpx.py <input_dir> <output.hwpx>
```
디렉터리를 HWPX ZIP으로 패킹. mimetype을 첫 번째 엔트리로 ZIP_STORED.

### fix_namespaces.py
```
python scripts/fix_namespaces.py <work_dir>
```
모든 XML 파일의 `ns0:`/`ns1:` 접두사를 정규 OWPML 접두사로 복원.

### extract_text.py
```
python scripts/extract_text.py <work_dir> --format <plain|markdown|json>
```
HWPX에서 텍스트 추출. 표도 포맷에 맞게 변환.

### analyze_template.py
```
python scripts/analyze_template.py <template_dir>
```
페이지 크기, 단락/표 수, charPr/paraPr/스타일/borderFill 목록, 플레이스홀더 탐지.

### validate_hwpx.py
```
python scripts/validate_hwpx.py <dir_or_hwpx>
```
ZIP 구조, secPr 존재, charPrIDRef/paraPrIDRef 참조 무결성 검증. PASS/WARN/FAIL 보고.

### zip_replace_all.py
```
python scripts/zip_replace_all.py <work_dir> --mapping <json_file> [--auto-fix-ns]
```
모든 XML에서 `{{key}}`를 `value`로 전역 치환. `--auto-fix-ns` 시 자동 네임스페이스 정리.

**매핑 JSON 형식:**
```json
{"{{이름}}": "홍길동", "{{날짜}}": "2026-04-10"}
```

### table_gen.py
```
python scripts/table_gen.py --rows <n> --cols <m> --data '<json>' [--merge '<json>'] [--output <file>]
```
HWPX 호환 `hp:tbl` XML 생성. 병합, borderFill, 셀 여백 자동 처리.

**data**: `[["a","b"], ["c","d"]]`
**merge**: `[{"row":0, "col":0, "rowSpan":1, "colSpan":2}]`

### build_hwpx.py
```
python scripts/build_hwpx.py --template <dir> --content <json> --output <dir>
```
템플릿 복사 후 콘텐츠 JSON으로 section0.xml 생성. heading/text/table 타입 지원.

### page_guard.py
```
python scripts/page_guard.py <dir> --ref-pages <n>
```
예상 페이지 수를 기준값과 비교. 경고만 출력 (차단 안 함). 근사치 추정.
