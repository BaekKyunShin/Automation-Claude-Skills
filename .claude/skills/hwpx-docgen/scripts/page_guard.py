#!/usr/bin/env python3
"""페이지 수 모니터링. 문서의 예상 페이지 수를 기준값과 비교."""
import argparse
import os
import sys

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

NS_HP = "urn:hancom:hwpml:2011"


def estimate_pages(section_path: str) -> int:
    """단락 수, 표, 줄 간격을 기반으로 페이지 수를 추정 (근사치)."""
    tree = etree.parse(section_path)

    # 페이지 크기 추출
    page_height = 84188  # A4 기본
    margin_top = 5668
    margin_bottom = 4252
    margin_header = 4252
    margin_footer = 4252

    for sec_pr in tree.iter(f"{{{NS_HP}}}secPr"):
        ph = sec_pr.find(f"{{{NS_HP}}}pageHeight")
        if ph is not None:
            page_height = int(ph.get("val", str(page_height)))
        mt = sec_pr.find(f"{{{NS_HP}}}marginTop")
        if mt is not None:
            margin_top = int(mt.get("val", str(margin_top)))
        mb = sec_pr.find(f"{{{NS_HP}}}marginBottom")
        if mb is not None:
            margin_bottom = int(mb.get("val", str(margin_bottom)))
        mh = sec_pr.find(f"{{{NS_HP}}}marginHeader")
        if mh is not None:
            margin_header = int(mh.get("val", str(margin_header)))
        mf = sec_pr.find(f"{{{NS_HP}}}marginFooter")
        if mf is not None:
            margin_footer = int(mf.get("val", str(margin_footer)))
        break

    usable_height = page_height - margin_top - margin_bottom - margin_header - margin_footer

    # 단락당 예상 높이 (줄간격 160%, 10pt 기준)
    line_height = 1000 * 1.6 * 0.283  # pt → hwpunit 근사
    para_count = len(list(tree.iter(f"{{{NS_HP}}}p")))
    table_count = len(list(tree.iter(f"{{{NS_HP}}}tbl")))

    # 표는 평균 5줄 높이로 가산
    total_content_height = (para_count * line_height) + (table_count * 5 * line_height)

    estimated = max(1, int(total_content_height / usable_height) + 1)
    return estimated


def guard(dir_path: str, ref_pages: int):
    section_path = os.path.join(dir_path, "Contents", "section0.xml")
    if not os.path.isfile(section_path):
        print("ERROR: section0.xml 없음", file=sys.stderr)
        return 2

    estimated = estimate_pages(section_path)
    diff = abs(estimated - ref_pages)

    if diff == 0:
        print(f"PASS: 예상 {estimated}페이지 = 기준 {ref_pages}페이지")
        return 0
    elif diff <= 1:
        print(f"WARN: 예상 {estimated}페이지 ≠ 기준 {ref_pages}페이지 (±1 이내, 허용)")
        print("  주의: 추정치는 근사값입니다. 실제 렌더링과 다를 수 있습니다.")
        return 0
    else:
        print(f"WARN: 예상 {estimated}페이지 ≠ 기준 {ref_pages}페이지 (차이: {diff})")
        print("  레이아웃이 크게 변경되었을 수 있습니다. secPr 설정을 확인하세요.")
        return 0  # 경고만, 차단 안 함


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HWPX 페이지 수 모니터링")
    parser.add_argument("dir_path", help="언팩된 HWPX 디렉터리")
    parser.add_argument("--ref-pages", type=int, required=True, help="기준 페이지 수")
    args = parser.parse_args()
    sys.exit(guard(args.dir_path, args.ref_pages))
