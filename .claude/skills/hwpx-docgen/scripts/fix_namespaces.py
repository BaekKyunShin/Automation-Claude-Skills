#!/usr/bin/env python3
"""XML 네임스페이스 자동 정리. lxml 편집 후 깨진 접두사를 복원."""
import argparse
import os
import re
import sys

# OWPML 정규 네임스페이스 매핑
OWPML_NAMESPACES = {
    "hp": "urn:hancom:hwpml:2011",
    "hc": "urn:hancom:hwpml:2011:common",
    "ha": "urn:hancom:hwpml:2011:app",
    "hh": "urn:hancom:hwpml:2011:head",
    "hs": "urn:hancom:hwpml:2011:section",
    "hp10": "urn:hancom:hwpml:2016",
}

# URI → 정규 접두사 역매핑
URI_TO_PREFIX = {v: k for k, v in OWPML_NAMESPACES.items()}


def fix_file(xml_path: str) -> bool:
    with open(xml_path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # ns0:, ns1: 등 자동생성 접두사를 정규 접두사로 교체
    for uri, prefix in URI_TO_PREFIX.items():
        # xmlns:nsN="uri" 패턴 찾기
        pattern = rf'xmlns:(ns\d+)="{re.escape(uri)}"'
        match = re.search(pattern, content)
        if match:
            auto_prefix = match.group(1)
            # 네임스페이스 선언 교체
            content = content.replace(
                f'xmlns:{auto_prefix}="{uri}"',
                f'xmlns:{prefix}="{uri}"',
            )
            # 요소/속성 접두사 교체
            content = content.replace(f"<{auto_prefix}:", f"<{prefix}:")
            content = content.replace(f"</{auto_prefix}:", f"</{prefix}:")
            content = content.replace(f" {auto_prefix}:", f" {prefix}:")

    if content != original:
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def fix_all(work_dir: str) -> list:
    changed = []
    for root, dirs, files in os.walk(work_dir):
        for f in files:
            if f.endswith(".xml"):
                path = os.path.join(root, f)
                if fix_file(path):
                    changed.append(os.path.relpath(path, work_dir))
    return changed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OWPML 네임스페이스 자동 정리")
    parser.add_argument("work_dir", help="작업 디렉터리")
    parser.add_argument("--auto-fix-ns", action="store_true", default=True,
                        help="자동 정리 (기본 활성)")
    args = parser.parse_args()

    changed = fix_all(args.work_dir)
    if changed:
        print(f"OK: {len(changed)}개 파일 수정됨:")
        for f in changed:
            print(f"  - {f}")
    else:
        print("OK: 수정 불필요")
