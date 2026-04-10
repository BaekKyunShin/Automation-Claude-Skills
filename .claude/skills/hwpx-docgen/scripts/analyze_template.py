#!/usr/bin/env python3
"""HWPX 템플릿 심층 분석. 스타일·단락·표·페이지 구조 보고."""
import argparse
import os
import sys

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

NS_HP = "urn:hancom:hwpml:2011"
NS_HH = "urn:hancom:hwpml:2011:head"


def analyze_header(header_path: str) -> dict:
    tree = etree.parse(header_path)
    result = {"charPr": [], "paraPr": [], "styles": [], "borderFills": []}

    for cp in tree.iter(f"{{{NS_HH}}}charPr"):
        info = {"id": cp.get("id")}
        font_ref = cp.find(f"{{{NS_HH}}}fontRef")
        if font_ref is not None:
            info["font_hangul"] = font_ref.get("hangul", "")
        font_size = cp.find(f"{{{NS_HH}}}fontSize")
        if font_size is not None:
            val = int(font_size.get("val", "1000"))
            info["size_pt"] = val / 100
        bold = cp.find(f"{{{NS_HH}}}bold")
        if bold is not None:
            info["bold"] = bold.get("val") == "true"
        result["charPr"].append(info)

    for pp in tree.iter(f"{{{NS_HH}}}paraPr"):
        info = {"id": pp.get("id")}
        align = pp.find(f"{{{NS_HH}}}align")
        if align is not None:
            info["align"] = align.get("val", "")
        result["paraPr"].append(info)

    for st in tree.iter(f"{{{NS_HH}}}style"):
        result["styles"].append({
            "id": st.get("id"),
            "name": st.get("name", ""),
            "charPrIDRef": st.get("charPrIDRef", ""),
            "paraPrIDRef": st.get("paraPrIDRef", ""),
        })

    for bf in tree.iter(f"{{{NS_HH}}}borderFill"):
        result["borderFills"].append({"id": bf.get("id")})

    return result


def analyze_section(section_path: str) -> dict:
    tree = etree.parse(section_path)
    result = {
        "paragraph_count": 0,
        "table_count": 0,
        "page_width": None,
        "page_height": None,
        "placeholders": [],
    }

    result["paragraph_count"] = len(list(tree.iter(f"{{{NS_HP}}}p")))
    result["table_count"] = len(list(tree.iter(f"{{{NS_HP}}}tbl")))

    # secPr에서 페이지 크기
    for sec_pr in tree.iter(f"{{{NS_HP}}}secPr"):
        pw = sec_pr.find(f"{{{NS_HP}}}pageWidth")
        ph = sec_pr.find(f"{{{NS_HP}}}pageHeight")
        if pw is not None:
            result["page_width"] = int(pw.get("val", "0"))
        if ph is not None:
            result["page_height"] = int(ph.get("val", "0"))
        break

    # 플레이스홀더 {{...}} 탐지
    import re
    for t in tree.iter(f"{{{NS_HP}}}t"):
        if t.text:
            found = re.findall(r"\{\{[^}]+\}\}", t.text)
            result["placeholders"].extend(found)

    return result


def report(header_info: dict, section_info: dict):
    print("=" * 50)
    print("HWPX 템플릿 분석 보고서")
    print("=" * 50)

    print(f"\n[페이지] ", end="")
    if section_info["page_width"]:
        w_mm = round(section_info["page_width"] / 283.46)
        h_mm = round(section_info["page_height"] / 283.46)
        print(f"{w_mm}mm x {h_mm}mm")
    else:
        print("정보 없음")

    print(f"\n[단락] {section_info['paragraph_count']}개")
    print(f"[표] {section_info['table_count']}개")

    print(f"\n[문자 속성] {len(header_info['charPr'])}개")
    for cp in header_info["charPr"]:
        parts = [f"id={cp['id']}"]
        if "font_hangul" in cp:
            parts.append(cp["font_hangul"])
        if "size_pt" in cp:
            parts.append(f"{cp['size_pt']}pt")
        if cp.get("bold"):
            parts.append("굵게")
        print(f"  - {', '.join(parts)}")

    print(f"\n[단락 속성] {len(header_info['paraPr'])}개")
    for pp in header_info["paraPr"]:
        print(f"  - id={pp['id']}, align={pp.get('align', '?')}")

    print(f"\n[스타일] {len(header_info['styles'])}개")
    for st in header_info["styles"]:
        print(f"  - id={st['id']}, name={st['name']}")

    print(f"\n[테두리/채움] {len(header_info['borderFills'])}개")

    if section_info["placeholders"]:
        print(f"\n[플레이스홀더] {len(section_info['placeholders'])}개")
        for ph in sorted(set(section_info["placeholders"])):
            print(f"  - {ph}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HWPX 템플릿 분석")
    parser.add_argument("template_dir", help="언팩된 HWPX 디렉터리")
    args = parser.parse_args()

    header_path = os.path.join(args.template_dir, "Contents", "header.xml")
    section_path = os.path.join(args.template_dir, "Contents", "section0.xml")

    if not os.path.isfile(header_path):
        print(f"ERROR: header.xml 없음: {header_path}", file=sys.stderr)
        sys.exit(2)
    if not os.path.isfile(section_path):
        print(f"ERROR: section0.xml 없음: {section_path}", file=sys.stderr)
        sys.exit(2)

    h = analyze_header(header_path)
    s = analyze_section(section_path)
    report(h, s)
