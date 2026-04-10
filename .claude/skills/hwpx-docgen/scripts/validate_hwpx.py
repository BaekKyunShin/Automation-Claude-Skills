#!/usr/bin/env python3
"""HWPX 구조 검증. OWPML 규격 준수 여부를 PASS/WARN/FAIL로 보고."""
import argparse
import os
import sys

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

NS_HP = "urn:hancom:hwpml:2011"
NS_HS = "urn:hancom:hwpml:2011:section"
NS_HH = "urn:hancom:hwpml:2011:head"


def check_zip_structure(dir_path: str) -> list:
    issues = []
    required = {
        "mimetype": "FAIL",
        "META-INF/container.xml": "FAIL",
        "Contents/content.hpf": "FAIL",
        "Contents/header.xml": "FAIL",
        "Contents/section0.xml": "FAIL",
    }
    for f, severity in required.items():
        if not os.path.isfile(os.path.join(dir_path, f)):
            issues.append((severity, f"필수 파일 누락: {f}"))

    mt_path = os.path.join(dir_path, "mimetype")
    if os.path.isfile(mt_path):
        with open(mt_path, "r") as f:
            content = f.read().strip()
        if content != "application/hwp+zip":
            issues.append(("FAIL", f"mimetype 값 오류: '{content}' (기대: 'application/hwp+zip')"))

    return issues


def check_section_integrity(dir_path: str) -> list:
    issues = []
    section_path = os.path.join(dir_path, "Contents", "section0.xml")
    if not os.path.isfile(section_path):
        return [("FAIL", "section0.xml 없음")]

    tree = etree.parse(section_path)
    paragraphs = list(tree.iter(f"{{{NS_HP}}}p"))

    if not paragraphs:
        issues.append(("FAIL", "section0.xml에 hp:p 요소 없음"))
        return issues

    # 첫 번째 단락에 secPr 확인
    first_p = paragraphs[0]
    sec_pr = first_p.find(f"{{{NS_HP}}}secPr")
    if sec_pr is None:
        issues.append(("FAIL", "첫 번째 hp:p에 secPr 없음"))
    else:
        col_pr = sec_pr.find(f"{{{NS_HP}}}colPr")
        if col_pr is None:
            issues.append(("WARN", "secPr에 colPr 없음"))

    # charPrIDRef 확인
    for r in tree.iter(f"{{{NS_HP}}}r"):
        if r.get("charPrIDRef") is None:
            issues.append(("WARN", f"hp:r에 charPrIDRef 누락"))
            break  # 첫 번째만 보고

    # paraPrIDRef 확인
    for p in paragraphs:
        if p.get("paraPrIDRef") is None:
            issues.append(("WARN", f"hp:p에 paraPrIDRef 누락 (id={p.get('id', '?')})"))
            break

    return issues


def check_style_references(dir_path: str) -> list:
    issues = []
    header_path = os.path.join(dir_path, "Contents", "header.xml")
    section_path = os.path.join(dir_path, "Contents", "section0.xml")

    if not os.path.isfile(header_path) or not os.path.isfile(section_path):
        return issues

    header_tree = etree.parse(header_path)
    section_tree = etree.parse(section_path)

    # header에 정의된 ID 수집
    char_pr_ids = set()
    for cp in header_tree.iter(f"{{{NS_HH}}}charPr"):
        cid = cp.get("id")
        if cid:
            char_pr_ids.add(cid)

    para_pr_ids = set()
    for pp in header_tree.iter(f"{{{NS_HH}}}paraPr"):
        pid = pp.get("id")
        if pid:
            para_pr_ids.add(pid)

    # section에서 참조하는 ID 확인
    for r in section_tree.iter(f"{{{NS_HP}}}r"):
        ref = r.get("charPrIDRef")
        if ref and ref not in char_pr_ids:
            issues.append(("WARN", f"charPrIDRef={ref} → header.xml에 미정의"))

    for p in section_tree.iter(f"{{{NS_HP}}}p"):
        ref = p.get("paraPrIDRef")
        if ref and ref not in para_pr_ids:
            issues.append(("WARN", f"paraPrIDRef={ref} → header.xml에 미정의"))

    return issues


def validate(dir_path: str):
    all_issues = []
    all_issues.extend(check_zip_structure(dir_path))
    all_issues.extend(check_section_integrity(dir_path))
    all_issues.extend(check_style_references(dir_path))

    has_fail = any(s == "FAIL" for s, _ in all_issues)

    if not all_issues:
        print("PASS: 모든 검증 통과")
        return 0

    for severity, msg in all_issues:
        print(f"{severity}: {msg}")

    if has_fail:
        print(f"\n결과: FAIL ({len(all_issues)}개 이슈)")
        return 1
    else:
        print(f"\n결과: WARN ({len(all_issues)}개 경고, 치명적 오류 없음)")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HWPX 구조 검증")
    parser.add_argument("dir_path", help="언팩된 HWPX 디렉터리 또는 .hwpx 파일")
    args = parser.parse_args()

    path = args.dir_path
    # .hwpx 파일이면 임시 해제
    if os.path.isfile(path) and path.endswith(".hwpx"):
        import tempfile
        import zipfile
        tmp = tempfile.mkdtemp(prefix="hwpx_validate_")
        with zipfile.ZipFile(path, "r") as zf:
            zf.extractall(tmp)
        path = tmp

    sys.exit(validate(path))
