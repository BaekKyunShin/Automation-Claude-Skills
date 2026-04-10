#!/usr/bin/env python3
"""템플릿 + 콘텐츠 JSON으로 HWPX 문서를 조립. python-hwpx 기반."""
import argparse
import json
import os
import shutil
import sys

from hwpx import HwpxDocument


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "templates")


def build_from_template(template_dir: str, content_json: dict, output_path: str):
    """템플릿을 기반으로 콘텐츠를 채운 HWPX 문서를 생성."""
    # 템플릿 .hwpx가 있으면 열기, 디렉터리면 먼저 패킹
    hwpx_path = _ensure_hwpx(template_dir)
    doc = HwpxDocument.open(hwpx_path)

    for item in content_json.get("paragraphs", []):
        item_type = item.get("type", "text")

        if item_type == "heading":
            level = item.get("level", 1)
            char_pr = 1 if level == 1 else 2
            para_pr = 1 if level == 1 else 2
            doc.add_paragraph(
                item.get("text", ""),
                char_pr_id_ref=char_pr,
                para_pr_id_ref=para_pr,
                style_id_ref=level,
            )

        elif item_type == "text":
            doc.add_paragraph(item.get("text", ""))

        elif item_type == "table":
            rows = item.get("rows", 2)
            cols = item.get("cols", 2)
            data = item.get("data", None)
            merge = item.get("merge", None)

            tbl = doc.add_table(rows, cols)

            # 셀 내용 채우기
            if data:
                for ri, row in enumerate(data):
                    for ci, cell_text in enumerate(row):
                        if ri < rows and ci < cols:
                            tbl.set_cell_text(ri, ci, str(cell_text))

            # 셀 병합
            if merge:
                for m in merge:
                    sr, sc = m["row"], m["col"]
                    er = sr + m.get("rowSpan", 1) - 1
                    ec = sc + m.get("colSpan", 1) - 1
                    if er > sr or ec > sc:
                        tbl.merge_cells(sr, sc, er, ec)

    doc.save_to_path(output_path)
    print(f"OK: {output_path}")


def build_new(content_json: dict, output_path: str):
    """빈 문서에서 콘텐츠를 채운 HWPX 문서를 생성."""
    doc = HwpxDocument.new()

    for item in content_json.get("paragraphs", []):
        item_type = item.get("type", "text")

        if item_type == "heading":
            level = item.get("level", 1)
            char_pr = 1 if level == 1 else 2
            para_pr = 1 if level == 1 else 2
            doc.add_paragraph(
                item.get("text", ""),
                char_pr_id_ref=char_pr,
                para_pr_id_ref=para_pr,
            )

        elif item_type == "text":
            doc.add_paragraph(item.get("text", ""))

        elif item_type == "table":
            rows = item.get("rows", 2)
            cols = item.get("cols", 2)
            data = item.get("data", None)
            merge = item.get("merge", None)

            tbl = doc.add_table(rows, cols)

            if data:
                for ri, row in enumerate(data):
                    for ci, cell_text in enumerate(row):
                        if ri < rows and ci < cols:
                            tbl.set_cell_text(ri, ci, str(cell_text))

            if merge:
                for m in merge:
                    sr, sc = m["row"], m["col"]
                    er = sr + m.get("rowSpan", 1) - 1
                    ec = sc + m.get("colSpan", 1) - 1
                    if er > sr or ec > sc:
                        tbl.merge_cells(sr, sc, er, ec)

    doc.save_to_path(output_path)
    print(f"OK: {output_path}")


def _ensure_hwpx(template_dir: str) -> str:
    """디렉터리 템플릿을 임시 .hwpx로 패킹."""
    if template_dir.endswith(".hwpx") and os.path.isfile(template_dir):
        return template_dir

    import tempfile
    import zipfile
    tmp = tempfile.NamedTemporaryFile(suffix=".hwpx", delete=False)
    tmp.close()

    mimetype_path = os.path.join(template_dir, "mimetype")
    with zipfile.ZipFile(tmp.name, "w", zipfile.ZIP_DEFLATED) as zf:
        if os.path.isfile(mimetype_path):
            zf.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)
        for root, dirs, files in os.walk(template_dir):
            for f in sorted(files):
                full = os.path.join(root, f)
                arcname = os.path.relpath(full, template_dir)
                if arcname == "mimetype":
                    continue
                zf.write(full, arcname)

    return tmp.name


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="템플릿 기반 HWPX 문서 조립 (python-hwpx)")
    parser.add_argument("--template", help="템플릿 디렉터리 또는 .hwpx 파일")
    parser.add_argument("--content", required=True, help="콘텐츠 JSON 파일")
    parser.add_argument("--output", required=True, help="출력 .hwpx 파일 경로")
    args = parser.parse_args()

    with open(args.content, "r", encoding="utf-8") as f:
        content = json.load(f)

    if args.template:
        if not os.path.exists(args.template):
            print(f"ERROR: 템플릿 없음: {args.template}", file=sys.stderr)
            sys.exit(2)
        build_from_template(args.template, content, args.output)
    else:
        build_new(content, args.output)

    print("다음 단계: validate_hwpx.py → (완료)")
