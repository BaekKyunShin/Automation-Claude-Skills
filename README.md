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

| 스킬 | 용도 |
|---|---|
| `ez-skill-search` | 다른 Claude Code 스킬을 웹에서 탐색·비교·추천 |
| `hwpx-docgen` | HWPX 한글 문서 생성·편집·분석·표 만들기 |

## 사용 방법

```bash
git clone https://github.com/BaekKyunShin/Automation-Claude-Skills.git
cd Automation-Claude-Skills
python -m venv .venv
source .venv/bin/activate
pip install python-hwpx lxml
claude
```

Claude Code 세션에서 자연어로 요청:
```
> 공문 만들어줘. 발신: 한국생산성본부, 수신: 삼육대학교, 제목: 협조 요청
> 내양식.hwpx에 이름을 홍길동으로 채워줘
```
