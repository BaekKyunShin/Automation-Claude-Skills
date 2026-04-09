# Automation-Claude-Skills

한국생산성본부(KPC) 업무·강의·멘토링에 사용할 Claude Code Agent Skills 모음.

## 목적

- 한글(HWP/HWPX), Word, Excel, PPT 등 실무 문서 자동 생성
- 강의·멘토링용 비계(scaffolding) 스킬
- 바이브코딩 워크플로우 자동화

## 구조

```
.claude/skills/       # Claude Code가 자동 로드하는 스킬 디렉터리
  <skill-name>/
    SKILL.md          # 스킬 정의 + 자동 호출 트리거
    references/       # 참조 리소스 (토큰 절약용 분리)
    scripts/          # 실행 스크립트 (옵션)
    templates/        # 템플릿 리소스 (옵션)
    examples/         # 사용 예시 (옵션)
```

## 현재 설치된 스킬

| 스킬 | 출처 | 용도 |
|---|---|---|
| `ez-skill-search` | 죠르디 공유 (초안) | 다른 Claude Code 스킬을 웹에서 탐색·비교·추천 |

## 개발 브랜치

- `claude/review-agent-skills-s7Zui` — 스킬 리뷰 및 신규 스킬 개발

## 워크플로우 (죠르디 방법론)

1. **Step 1**: 스킬 검색 스킬(`ez-skill-search`)로 원하는 기능의 기존 스킬들을 수집
2. **Step 2**: 수집된 스킬들의 장점을 합성한 신규 스킬 초안 생성
3. **Step 3**: 내 도메인(KPC) 지식으로 업데이트. 필요 시 YouTube URL 등 외부 자료를 추가 학습
