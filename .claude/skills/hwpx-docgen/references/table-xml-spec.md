# HWPX 표 XML 규격

`table_gen.py` 스크립트와 에이전트가 표를 생성·편집할 때 참조하는 문서.

---

## 1. 기본 표 구조

```xml
<hp:tbl borderFillIDRef="1" cellSpacing="0" colCount="3" rowCount="2">
  <!-- 열 너비 정의 -->
  <hp:colSz val="19843"/>  <!-- 열 1 너비 (hwpunit) -->
  <hp:colSz val="19843"/>  <!-- 열 2 -->
  <hp:colSz val="19843"/>  <!-- 열 3 -->

  <!-- 행 1 -->
  <hp:tr>
    <hp:tc borderFillIDRef="2">
      <hp:cellAddr colAddr="0" rowAddr="0"/>
      <hp:cellSpan colSpan="1" rowSpan="1"/>
      <hp:cellSz width="19843" height="1800"/>
      <hp:cellMargin left="510" right="510" top="142" bottom="142"/>
      <hp:p id="10" paraPrIDRef="1" styleIDRef="0">
        <hp:r charPrIDRef="1">
          <hp:t>셀 내용</hp:t>
        </hp:r>
      </hp:p>
    </hp:tc>
    <!-- ... 나머지 셀 -->
  </hp:tr>
  <!-- ... 나머지 행 -->
</hp:tbl>
```

---

## 2. 속성 상세

### hp:tbl (표)

| 속성 | 설명 | 예시 |
|---|---|---|
| `borderFillIDRef` | header.xml의 borderFill ID 참조 | `"1"` |
| `cellSpacing` | 셀 간격 (hwpunit) | `"0"` |
| `colCount` | 열 수 | `"3"` |
| `rowCount` | 행 수 | `"2"` |

### hp:colSz (열 너비)

`hp:tbl` 바로 아래에 열 수만큼 반복. `val` = 열 너비 (hwpunit).

A4 본문 영역 너비 = `pageWidth - marginLeft - marginRight` = 59528 - 8504 - 8504 = **42520 hwpunit**.
3열 균등: 42520 / 3 = **14173 hwpunit** (반올림).

### hp:tc (셀)

| 자식 요소 | 설명 | 필수 |
|---|---|---|
| `hp:cellAddr` | 셀 위치 (colAddr, rowAddr) | O |
| `hp:cellSpan` | 병합 범위 (colSpan, rowSpan) | O |
| `hp:cellSz` | 셀 크기 (width, height) | O |
| `hp:cellMargin` | 셀 내부 여백 | 권장 |
| `hp:p` | 셀 내용 (1개 이상의 단락) | O |

---

## 3. 셀 병합

### 원리

`hp:cellSpan`의 `colSpan`/`rowSpan`으로 병합 범위를 지정. 병합된 영역에 포함되는 다른 셀은 **생략하지 않고** `colSpan="0"` 또는 `rowSpan="0"`으로 표시.

### 예시: 첫 행 3열 병합 (헤더)

```xml
<!-- 행 1: 3열 병합 헤더 -->
<hp:tr>
  <hp:tc borderFillIDRef="2">
    <hp:cellAddr colAddr="0" rowAddr="0"/>
    <hp:cellSpan colSpan="3" rowSpan="1"/>
    <hp:cellSz width="42520" height="2000"/>
    <hp:cellMargin left="510" right="510" top="142" bottom="142"/>
    <hp:p id="10" paraPrIDRef="2" styleIDRef="0">
      <hp:r charPrIDRef="2">
        <hp:t>병합된 헤더</hp:t>
      </hp:r>
    </hp:p>
  </hp:tc>
  <!-- 병합에 흡수된 셀 (빈 셀로 존재해야 함) -->
  <hp:tc borderFillIDRef="2">
    <hp:cellAddr colAddr="1" rowAddr="0"/>
    <hp:cellSpan colSpan="0" rowSpan="0"/>
    <hp:cellSz width="0" height="0"/>
    <hp:p id="11" paraPrIDRef="1" styleIDRef="0"/>
  </hp:tc>
  <hp:tc borderFillIDRef="2">
    <hp:cellAddr colAddr="2" rowAddr="0"/>
    <hp:cellSpan colSpan="0" rowSpan="0"/>
    <hp:cellSz width="0" height="0"/>
    <hp:p id="12" paraPrIDRef="1" styleIDRef="0"/>
  </hp:tc>
</hp:tr>
```

### 예시: 2행 × 1열 병합 (세로 병합)

```xml
<!-- 행 1, 열 0: rowSpan=2 -->
<hp:tc borderFillIDRef="2">
  <hp:cellAddr colAddr="0" rowAddr="0"/>
  <hp:cellSpan colSpan="1" rowSpan="2"/>
  <hp:cellSz width="14173" height="3600"/>
  ...
</hp:tc>

<!-- 행 2, 열 0: 흡수된 셀 -->
<hp:tc borderFillIDRef="2">
  <hp:cellAddr colAddr="0" rowAddr="1"/>
  <hp:cellSpan colSpan="0" rowSpan="0"/>
  <hp:cellSz width="0" height="0"/>
  <hp:p id="20" paraPrIDRef="1" styleIDRef="0"/>
</hp:tc>
```

---

## 4. borderFill 정의 (header.xml)

표와 셀에 적용할 테두리·배경 스타일.

```xml
<!-- header.xml 내 -->
<hh:borderFill id="2">
  <hh:border>
    <hh:left type="thin" width="1" color="#000000"/>
    <hh:right type="thin" width="1" color="#000000"/>
    <hh:top type="thin" width="1" color="#000000"/>
    <hh:bottom type="thin" width="1" color="#000000"/>
  </hh:border>
  <hh:fillColor val="#FFFFFF"/>
</hh:borderFill>

<!-- 헤더 행용 (배경색) -->
<hh:borderFill id="3">
  <hh:border>
    <hh:left type="thin" width="1" color="#000000"/>
    <hh:right type="thin" width="1" color="#000000"/>
    <hh:top type="thin" width="1" color="#000000"/>
    <hh:bottom type="thin" width="1" color="#000000"/>
  </hh:border>
  <hh:fillColor val="#E6E6E6"/>
</hh:borderFill>
```

---

## 5. 기본값 참고

| 항목 | 기본값 |
|---|---|
| 셀 높이 | 1800 hwpunit (~6.35mm) |
| 셀 여백 (좌/우) | 510 hwpunit (~1.8mm) |
| 셀 여백 (상/하) | 142 hwpunit (~0.5mm) |
| A4 본문 너비 | 42520 hwpunit |
| 기본 테두리 | thin, width=1, #000000 |
| 기본 배경 | #FFFFFF |
