# OWPML 포맷 레퍼런스

HWPX 문서를 생성·편집할 때 참조하는 OWPML XML 규격 요약.

---

## 1. ZIP 구조

HWPX = ZIP 컨테이너. 필수 엔트리:

```
mimetype                    # 첫 번째 엔트리, ZIP_STORED(비압축), 값: application/hwp+zip
META-INF/
  container.xml             # 콘텐츠 매니페스트
Contents/
  content.hpf               # 파일 목록 (header, section 참조)
  header.xml                # 스타일 정의 (charPr, paraPr, style, borderFill)
  section0.xml              # 본문 (단락, 표, 이미지)
version.xml                 # OWPML 버전 선언
```

**mimetype 규칙**: 반드시 ZIP의 첫 번째 엔트리, `ZIP_STORED` (압축 없음). 위반 시 한컴오피스에서 열리지 않음.

---

## 2. 네임스페이스

```xml
xmlns:hp="urn:hancom:hwpml:2011"         <!-- 단락, 텍스트, 표 -->
xmlns:hc="urn:hancom:hwpml:2011:common"  <!-- 공통 속성 -->
xmlns:ha="urn:hancom:hwpml:2011:app"     <!-- 애플리케이션 설정 -->
xmlns:hp10="urn:hancom:hwpml:2016"       <!-- 확장 요소 -->
xmlns:hh="urn:hancom:hwpml:2011:head"    <!-- header.xml 루트 -->
xmlns:hs="urn:hancom:hwpml:2011:section" <!-- section XML 루트 -->
```

**주의**: lxml로 XML 편집 후 네임스페이스 선언이 누락되거나 `ns0:`, `ns1:` 접두사로 바뀔 수 있음. 편집 후 반드시 `fix_namespaces.py` 실행.

---

## 3. 핵심 요소

### section0.xml 요소

| 요소 | 부모 | 설명 | 필수 속성 |
|---|---|---|---|
| `hs:sec` | 루트 | 섹션 루트 | — |
| `hp:p` | `hs:sec` | 단락 | `id`, `paraPrIDRef`, `styleIDRef` |
| `hp:r` | `hp:p` | 텍스트 런 | `charPrIDRef` |
| `hp:t` | `hp:r` | 텍스트 내용 | — (빈 줄은 `<hp:t/>` self-closing) |
| `hp:tbl` | `hp:p` | 표 | `borderFillIDRef`, `cellSpacing` |
| `hp:tr` | `hp:tbl` | 표 행 | — |
| `hp:tc` | `hp:tr` | 표 셀 | `borderFillIDRef` |
| `hp:cellAddr` | `hp:tc` | 셀 주소 | `colAddr`, `rowAddr` |
| `hp:cellSpan` | `hp:tc` | 셀 병합 | `colSpan`, `rowSpan` |
| `hp:cellSz` | `hp:tc` | 셀 크기 | `width`, `height` |
| `hp:secPr` | `hp:p` (첫 번째) | 섹션 속성 | `pageWidth`, `pageHeight` |
| `hp:colPr` | `hp:secPr` | 단 속성 | `type`, `colCount` |

### header.xml 요소

| 요소 | 설명 | 핵심 자식 |
|---|---|---|
| `hh:refList` | 참조 목록 루트 | `hh:charProperties`, `hh:paraProperties` 등 |
| `hh:charPr` | 문자 속성 정의 | `fontRef`, `fontSize`, `bold`, `italic` |
| `hh:paraPr` | 단락 속성 정의 | `align`, `lineSpacing`, `margin` |
| `hh:style` | 스타일 정의 | `name`, `charPrIDRef`, `paraPrIDRef` |
| `hh:borderFill` | 테두리·채움 정의 | `border` (left/right/top/bottom), `fillColor` |

---

## 4. 스타일 참조 시스템

```
header.xml에 정의    →  section0.xml에서 참조
─────────────────────────────────────────────
charPr  (id=1)       →  hp:r  charPrIDRef="1"
paraPr  (id=1)       →  hp:p  paraPrIDRef="1"
style   (id=1)       →  hp:p  styleIDRef="1"
borderFill (id=1)    →  hp:tbl / hp:tc  borderFillIDRef="1"
```

**규칙**: section0.xml에서 참조하는 모든 ID는 header.xml에 정의되어 있어야 함. 없는 ID 참조 시 문서가 열리지 않거나 스타일 깨짐.

---

## 5. secPr (섹션 속성) — 절대 규칙

`section0.xml`의 **첫 번째 `hp:p`**에 반드시 `hp:secPr` + `hp:colPr` 포함.

```xml
<hp:p id="0" paraPrIDRef="0" styleIDRef="0">
  <hp:secPr>
    <hp:pageWidth val="59528"/>   <!-- A4: 210mm = 59528 hwpunit -->
    <hp:pageHeight val="84188"/>  <!-- A4: 297mm = 84188 hwpunit -->
    <hp:marginTop val="5668"/>    <!-- 20mm -->
    <hp:marginBottom val="4252"/>  <!-- 15mm -->
    <hp:marginLeft val="8504"/>   <!-- 30mm -->
    <hp:marginRight val="8504"/>  <!-- 30mm -->
    <hp:marginHeader val="4252"/>
    <hp:marginFooter val="4252"/>
    <hp:marginGutter val="0"/>
    <hp:colPr type="none" colCount="1" sameSz="0" sameGap="0"/>
  </hp:secPr>
</hp:p>
```

**hwpunit 변환**: 1mm = 283.46 hwpunit (반올림). A4 = 59528 x 84188.

**금지 사항**:
- `secPr`이 포함된 첫 번째 `hp:p`를 삭제/이동 금지
- 명시적 요청 없이 `pageWidth`, `pageHeight`, `margin*` 값 변경 금지

---

## 6. 폰트 참조

```xml
<!-- header.xml 내 charPr 예시 -->
<hh:charPr id="1">
  <hh:fontRef hangul="함초롬바탕" latin="Times New Roman"/>
  <hh:fontSize val="1000"/>  <!-- 10pt = 1000 -->
  <hh:bold val="false"/>
</hh:charPr>
```

**폰트 크기**: pt × 100 = val. 예: 10pt = 1000, 12pt = 1200, 16pt = 1600.

**기본 폰트 추천**: `함초롬바탕` (본문), `함초롬돋움` (제목), `맑은 고딕` (폴백).
