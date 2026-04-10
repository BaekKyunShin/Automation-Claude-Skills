#!/usr/bin/env python3
"""디렉터리를 HWPX ZIP으로 패킹. mimetype은 첫 번째 엔트리, 비압축."""
import argparse
import os
import zipfile
import sys


def pack(input_dir: str, output_path: str):
    if not os.path.isdir(input_dir):
        print(f"ERROR: 디렉터리 없음: {input_dir}", file=sys.stderr)
        sys.exit(2)

    mimetype_path = os.path.join(input_dir, "mimetype")
    if not os.path.isfile(mimetype_path):
        print("ERROR: mimetype 파일 없음", file=sys.stderr)
        sys.exit(2)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # mimetype은 첫 번째 엔트리, 비압축 (ZIP_STORED)
        zf.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)

        for root, dirs, files in os.walk(input_dir):
            for f in sorted(files):
                full_path = os.path.join(root, f)
                arcname = os.path.relpath(full_path, input_dir)
                if arcname == "mimetype":
                    continue  # 이미 추가됨
                zf.write(full_path, arcname)

    print(f"OK: {input_dir} → {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="디렉터리를 HWPX ZIP으로 패킹")
    parser.add_argument("input_dir", help="입력 디렉터리")
    parser.add_argument("output_path", help="출력 .hwpx 파일")
    args = parser.parse_args()
    pack(args.input_dir, args.output_path)
