#!/usr/bin/env python3
"""HWPX에서 텍스트 추출 (plain / markdown / json). python-hwpx 기반."""
import argparse
import json
import sys

from hwpx import HwpxDocument, TextExtractor


def extract_plain(hwpx_path: str) -> str:
    """일반 텍스트로 추출."""
    doc = HwpxDocument.open(hwpx_path)
    return doc.export_text()


def extract_markdown(hwpx_path: str) -> str:
    """마크다운 포맷으로 추출."""
    doc = HwpxDocument.open(hwpx_path)
    return doc.export_markdown()


def extract_json(hwpx_path: str) -> dict:
    """구조화된 JSON으로 추출."""
    extractor = TextExtractor.open(hwpx_path)
    result = {"sections": []}

    for section in extractor.iter_sections():
        sec_data = {"paragraphs": []}
        for para in extractor.iter_paragraphs(section):
            text = extractor.paragraph_text(para)
            if text:
                sec_data["paragraphs"].append({"text": text})
        result["sections"].append(sec_data)

    extractor.close()
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HWPX 텍스트 추출 (python-hwpx)")
    parser.add_argument("hwpx_path", help=".hwpx 파일 경로")
    parser.add_argument("--format", choices=["plain", "markdown", "json"],
                        default="plain", help="출력 포맷 (기본: plain)")
    args = parser.parse_args()

    if args.format == "plain":
        print(extract_plain(args.hwpx_path))
    elif args.format == "markdown":
        print(extract_markdown(args.hwpx_path))
    elif args.format == "json":
        print(json.dumps(extract_json(args.hwpx_path), ensure_ascii=False, indent=2))
