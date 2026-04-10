#!/usr/bin/env python3
"""HWPX에서 텍스트 추출 (plain / markdown / json)."""
import argparse
import json
import os
import sys

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

NS = {
    "hs": "urn:hancom:hwpml:2011:section",
    "hp": "urn:hancom:hwpml:2011",
    "hc": "urn:hancom:hwpml:2011:common",
}


def parse_section(work_dir: str):
    section_path = os.path.join(work_dir, "Contents", "section0.xml")
    if not os.path.isfile(section_path):
        print(f"ERROR: section0.xml 없음: {section_path}", file=sys.stderr)
        sys.exit(2)
    return etree.parse(section_path)


def extract_plain(tree) -> str:
    lines = []
    for p in tree.iter("{urn:hancom:hwpml:2011}p"):
        texts = []
        for t in p.iter("{urn:hancom:hwpml:2011}t"):
            if t.text:
                texts.append(t.text)
        line = "".join(texts)
        if line:
            lines.append(line)
    return "\n".join(lines)


def extract_markdown(tree) -> str:
    lines = []
    for p in tree.iter("{urn:hancom:hwpml:2011}p"):
        # 표 감지
        tables = list(p.iter("{urn:hancom:hwpml:2011}tbl"))
        if tables:
            for tbl in tables:
                lines.append(_table_to_md(tbl))
            continue

        texts = []
        for t in p.iter("{urn:hancom:hwpml:2011}t"):
            if t.text:
                texts.append(t.text)
        line = "".join(texts)
        if line:
            lines.append(line)
    return "\n\n".join(lines)


def _table_to_md(tbl) -> str:
    rows = []
    for tr in tbl.iter("{urn:hancom:hwpml:2011}tr"):
        cells = []
        for tc in tr.iter("{urn:hancom:hwpml:2011}tc"):
            cell_text = []
            for t in tc.iter("{urn:hancom:hwpml:2011}t"):
                if t.text:
                    cell_text.append(t.text)
            cells.append(" ".join(cell_text))
        rows.append(cells)

    if not rows:
        return ""

    md_lines = []
    # 헤더
    md_lines.append("| " + " | ".join(rows[0]) + " |")
    md_lines.append("| " + " | ".join(["---"] * len(rows[0])) + " |")
    # 데이터
    for row in rows[1:]:
        # 열 수 맞추기
        while len(row) < len(rows[0]):
            row.append("")
        md_lines.append("| " + " | ".join(row) + " |")
    return "\n".join(md_lines)


def extract_json(tree) -> dict:
    result = {"paragraphs": []}
    for p in tree.iter("{urn:hancom:hwpml:2011}p"):
        para_pr = p.get("paraPrIDRef", "0")
        style_id = p.get("styleIDRef", "0")

        tables = list(p.iter("{urn:hancom:hwpml:2011}tbl"))
        if tables:
            for tbl in tables:
                result["paragraphs"].append({
                    "type": "table",
                    "paraPrIDRef": para_pr,
                    "rows": _table_to_list(tbl),
                })
            continue

        texts = []
        for t in p.iter("{urn:hancom:hwpml:2011}t"):
            if t.text:
                texts.append(t.text)
        text = "".join(texts)
        if text:
            result["paragraphs"].append({
                "type": "text",
                "paraPrIDRef": para_pr,
                "styleIDRef": style_id,
                "text": text,
            })
    return result


def _table_to_list(tbl) -> list:
    rows = []
    for tr in tbl.iter("{urn:hancom:hwpml:2011}tr"):
        cells = []
        for tc in tr.iter("{urn:hancom:hwpml:2011}tc"):
            cell_text = []
            for t in tc.iter("{urn:hancom:hwpml:2011}t"):
                if t.text:
                    cell_text.append(t.text)
            cells.append(" ".join(cell_text))
        rows.append(cells)
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HWPX 텍스트 추출")
    parser.add_argument("work_dir", help="언팩된 HWPX 디렉터리")
    parser.add_argument("--format", choices=["plain", "markdown", "json"],
                        default="plain", help="출력 포맷 (기본: plain)")
    args = parser.parse_args()

    tree = parse_section(args.work_dir)

    if args.format == "plain":
        print(extract_plain(tree))
    elif args.format == "markdown":
        print(extract_markdown(tree))
    elif args.format == "json":
        print(json.dumps(extract_json(tree), ensure_ascii=False, indent=2))
