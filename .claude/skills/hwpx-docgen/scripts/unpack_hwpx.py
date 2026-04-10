#!/usr/bin/env python3
"""HWPX ZIP을 디렉터리로 해제."""
import argparse
import os
import zipfile
import sys


def unpack(hwpx_path: str, output_dir: str) -> str:
    if not os.path.isfile(hwpx_path):
        print(f"ERROR: 파일 없음: {hwpx_path}", file=sys.stderr)
        sys.exit(2)
    if not zipfile.is_zipfile(hwpx_path):
        print(f"ERROR: 유효한 ZIP 아님: {hwpx_path}", file=sys.stderr)
        sys.exit(2)

    os.makedirs(output_dir, exist_ok=True)
    with zipfile.ZipFile(hwpx_path, "r") as zf:
        zf.extractall(output_dir)

    warnings = verify_structure(output_dir)
    if warnings:
        for w in warnings:
            print(f"WARN: {w}", file=sys.stderr)

    print(f"OK: {hwpx_path} → {output_dir}")
    return output_dir


def verify_structure(output_dir: str) -> list:
    warnings = []
    required = [
        "mimetype",
        "META-INF/container.xml",
        "Contents/content.hpf",
        "Contents/header.xml",
        "Contents/section0.xml",
    ]
    for f in required:
        if not os.path.isfile(os.path.join(output_dir, f)):
            warnings.append(f"필수 파일 누락: {f}")
    return warnings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HWPX 파일을 디렉터리로 해제")
    parser.add_argument("hwpx_path", help="입력 .hwpx 파일")
    parser.add_argument("output_dir", help="출력 디렉터리")
    args = parser.parse_args()
    unpack(args.hwpx_path, args.output_dir)
