#!/usr/bin/env python3
"""HWPX 호환 표 XML 생성. 행/열/병합/스타일을 지정해서 hp:tbl 요소를 생성."""
import argparse
import json
import sys

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

NS_HP = "urn:hancom:hwpml:2011"

# A4 본문 너비 (기본 여백 기준)
DEFAULT_BODY_WIDTH = 42520  # hwpunit
DEFAULT_CELL_HEIGHT = 1800
DEFAULT_CELL_MARGIN = {"left": 510, "right": 510, "top": 142, "bottom": 142}


def _el(tag, attrib=None, text=None):
    elem = etree.Element(f"{{{NS_HP}}}{tag}", attrib or {})
    if text is not None:
        elem.text = text
    return elem


def create_table(rows: int, cols: int, data: list = None,
                 merge: list = None, border_fill_id: int = 2,
                 header_border_fill_id: int = 3,
                 body_width: int = DEFAULT_BODY_WIDTH,
                 char_pr_id: int = 0, para_pr_id: int = 0,
                 header_char_pr_id: int = 3,
                 p_id_start: int = 100) -> etree.Element:
    col_width = body_width // cols

    tbl = _el("tbl", {
        "borderFillIDRef": str(border_fill_id),
        "cellSpacing": "0",
        "colCount": str(cols),
        "rowCount": str(rows),
    })

    # 열 너비
    for _ in range(cols):
        tbl.append(_el("colSz", {"val": str(col_width)}))

    # 병합 정보 맵 생성
    merge_map = {}  # (row, col) -> {"rowSpan": n, "colSpan": m}
    absorbed = set()  # 병합에 흡수된 셀
    if merge:
        for m in merge:
            r, c = m["row"], m["col"]
            rs, cs = m.get("rowSpan", 1), m.get("colSpan", 1)
            merge_map[(r, c)] = {"rowSpan": rs, "colSpan": cs}
            for dr in range(rs):
                for dc in range(cs):
                    if dr == 0 and dc == 0:
                        continue
                    absorbed.add((r + dr, c + dc))

    p_id = p_id_start

    for ri in range(rows):
        tr = _el("tr")
        for ci in range(cols):
            is_header_row = (ri == 0)
            bf_id = str(header_border_fill_id if is_header_row else border_fill_id)
            tc = _el("tc", {"borderFillIDRef": bf_id})

            tc.append(_el("cellAddr", {"colAddr": str(ci), "rowAddr": str(ri)}))

            if (ri, ci) in absorbed:
                # 병합에 흡수된 셀
                tc.append(_el("cellSpan", {"colSpan": "0", "rowSpan": "0"}))
                tc.append(_el("cellSz", {"width": "0", "height": "0"}))
                empty_p = _el("p", {"id": str(p_id), "paraPrIDRef": str(para_pr_id), "styleIDRef": "0"})
                p_id += 1
                tc.append(empty_p)
            else:
                ms = merge_map.get((ri, ci), {"rowSpan": 1, "colSpan": 1})
                tc.append(_el("cellSpan", {
                    "colSpan": str(ms["colSpan"]),
                    "rowSpan": str(ms["rowSpan"]),
                }))
                cell_w = col_width * ms["colSpan"]
                cell_h = DEFAULT_CELL_HEIGHT * ms["rowSpan"]
                tc.append(_el("cellSz", {"width": str(cell_w), "height": str(cell_h)}))
                tc.append(_el("cellMargin", {
                    "left": str(DEFAULT_CELL_MARGIN["left"]),
                    "right": str(DEFAULT_CELL_MARGIN["right"]),
                    "top": str(DEFAULT_CELL_MARGIN["top"]),
                    "bottom": str(DEFAULT_CELL_MARGIN["bottom"]),
                }))

                # 셀 내용
                cell_text = ""
                if data and ri < len(data) and ci < len(data[ri]):
                    cell_text = str(data[ri][ci])

                cpr = str(header_char_pr_id if is_header_row else char_pr_id)
                p = _el("p", {"id": str(p_id), "paraPrIDRef": str(para_pr_id), "styleIDRef": "0"})
                p_id += 1
                r = _el("r", {"charPrIDRef": cpr})
                t = _el("t")
                t.text = cell_text
                r.append(t)
                p.append(r)
                tc.append(p)

            tr.append(tc)
        tbl.append(tr)

    return tbl


def table_to_string(tbl: etree.Element) -> str:
    try:
        return etree.tostring(tbl, encoding="unicode", pretty_print=True)
    except TypeError:
        # xml.etree 폴백
        etree.indent(tbl)
        return etree.tostring(tbl, encoding="unicode")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HWPX 표 XML 생성")
    parser.add_argument("--rows", type=int, required=True, help="행 수")
    parser.add_argument("--cols", type=int, required=True, help="열 수")
    parser.add_argument("--data", help="JSON 2D 배열 (셀 내용)")
    parser.add_argument("--merge", help="JSON 병합 명세 [{row, col, rowSpan, colSpan}]")
    parser.add_argument("--border-fill-id", type=int, default=2)
    parser.add_argument("--output", help="출력 XML 파일 (생략 시 stdout)")
    args = parser.parse_args()

    data = json.loads(args.data) if args.data else None
    merge = json.loads(args.merge) if args.merge else None

    tbl = create_table(args.rows, args.cols, data, merge, args.border_fill_id)
    xml_str = table_to_string(tbl)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(xml_str)
        print(f"OK: {args.output}")
    else:
        print(xml_str)
