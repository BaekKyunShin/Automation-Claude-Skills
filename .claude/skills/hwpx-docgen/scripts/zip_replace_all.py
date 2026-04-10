#!/usr/bin/env python3
"""ZIP-level 전역 플레이스홀더 치환. 모든 XML 파일에서 {{key}}를 값으로 교체."""
import argparse
import json
import os
import sys


def replace_all(work_dir: str, mapping: dict, auto_fix_ns: bool = True):
    changed_files = []

    for root, dirs, files in os.walk(work_dir):
        for f in files:
            if not f.endswith(".xml"):
                continue
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()

            original = content
            for key, val in mapping.items():
                content = content.replace(key, val)

            if content != original:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(content)
                changed_files.append(os.path.relpath(path, work_dir))

    if changed_files:
        print(f"치환 완료: {len(changed_files)}개 파일")
        for f in changed_files:
            print(f"  - {f}")
    else:
        print("치환 대상 없음")

    if auto_fix_ns and changed_files:
        print("\n네임스페이스 자동 정리 실행...")
        # fix_namespaces 직접 호출
        script_dir = os.path.dirname(os.path.abspath(__file__))
        fix_ns_path = os.path.join(script_dir, "fix_namespaces.py")
        if os.path.isfile(fix_ns_path):
            os.system(f'python3 "{fix_ns_path}" "{work_dir}"')

    return changed_files


def load_mapping(json_path: str) -> dict:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HWPX 전역 플레이스홀더 치환")
    parser.add_argument("work_dir", help="언팩된 HWPX 디렉터리")
    parser.add_argument("--mapping", required=True, help="JSON 매핑 파일 (예: {\"{{이름}}\": \"홍길동\"})")
    parser.add_argument("--auto-fix-ns", action="store_true", default=True,
                        help="치환 후 네임스페이스 자동 정리 (기본 활성)")
    args = parser.parse_args()

    mapping = load_mapping(args.mapping)
    replace_all(args.work_dir, mapping, args.auto_fix_ns)
