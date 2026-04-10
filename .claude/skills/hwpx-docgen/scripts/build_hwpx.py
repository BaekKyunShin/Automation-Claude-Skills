#!/usr/bin/env python3
"""템플릿 + 콘텐츠 JSON으로 HWPX 문서를 조립."""
import argparse
import json
import os
import shutil
import sys

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

NS_HP = "urn:hancom:hwpml:2011"
NS_HS = "urn:hancom:hwpml:2011:section"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_template(template_dir: str, output_dir: str):
    """템플릿을 output_dir로 복사."""
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    shutil.copytree(template_dir, output_dir)


def build_section(content_json: dict, output_dir: str, p_id_start: int = 2):
    """content JSON을 파싱해서 section0.xml에 단락/표를 추가."""
    section_path = os.path.join(output_dir, "Contents", "section0.xml")
    tree = etree.parse(section_path)
    root = tree.getroot()

    # 기존 빈 단락 제거 (secPr 단락은 유지)
    paragraphs = list(root.iter(f"{{{NS_HP}}}p"))
    for p in paragraphs[1:]:  # 첫 번째(secPr) 유지
        parent = _find_parent(root, p)
        if parent is not None:
            parent.remove(p)

    p_id = p_id_start
    sec_elem = root if root.tag == f"{{{NS_HS}}}sec" else root.find(f".//{{{NS_HS}}}sec")
    if sec_elem is None:
        sec_elem = root

    for item in content_json.get("paragraphs", []):
        item_type = item.get("type", "text")

        if item_type == "heading":
            level = item.get("level", 1)
            char_pr = "1" if level == 1 else "2"
            para_pr = "1" if level == 1 else "2"
            p = _make_paragraph(p_id, para_pr, char_pr, item.get("text", ""))
            p_id += 1
            sec_elem.append(p)

        elif item_type == "text":
            p = _make_paragraph(p_id, "0", "0", item.get("text", ""))
            p_id += 1
            sec_elem.append(p)

        elif item_type == "table":
            # table_gen 모듈 사용
            sys.path.insert(0, SCRIPT_DIR)
            from table_gen import create_table
            rows = item.get("rows", 2)
            cols = item.get("cols", 2)
            data = item.get("data", None)
            merge = item.get("merge", None)
            tbl = create_table(rows, cols, data, merge, p_id_start=p_id)
            # 표를 감싸는 단락
            wrapper_p = etree.SubElement(sec_elem, f"{{{NS_HP}}}p", {
                "id": str(p_id), "paraPrIDRef": "0", "styleIDRef": "0"
            })
            p_id += rows * cols + 1
            wrapper_p.append(tbl)

    # 저장
    try:
        tree.write(section_path, encoding="UTF-8", xml_declaration=True, pretty_print=True)
    except TypeError:
        tree.write(section_path, encoding="UTF-8", xml_declaration=True)


def _make_paragraph(p_id, para_pr_id, char_pr_id, text):
    p = etree.Element(f"{{{NS_HP}}}p", {
        "id": str(p_id), "paraPrIDRef": str(para_pr_id), "styleIDRef": "0"
    })
    r = etree.SubElement(p, f"{{{NS_HP}}}r", {"charPrIDRef": str(char_pr_id)})
    t = etree.SubElement(r, f"{{{NS_HP}}}t")
    t.text = text
    return p


def _find_parent(root, target):
    for parent in root.iter():
        for child in parent:
            if child is target:
                return parent
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="템플릿 기반 HWPX 문서 조립")
    parser.add_argument("--template", required=True, help="템플릿 디렉터리 경로")
    parser.add_argument("--content", required=True, help="콘텐츠 JSON 파일")
    parser.add_argument("--output", required=True, help="출력 디렉터리")
    args = parser.parse_args()

    if not os.path.isdir(args.template):
        print(f"ERROR: 템플릿 없음: {args.template}", file=sys.stderr)
        sys.exit(2)

    with open(args.content, "r", encoding="utf-8") as f:
        content = json.load(f)

    load_template(args.template, args.output)
    build_section(content, args.output)

    print(f"OK: {args.output}")
    print("다음 단계: fix_namespaces.py → validate_hwpx.py → pack_hwpx.py")
