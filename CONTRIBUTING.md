# Contributing to Automation-Claude-Skills

이 레포에 새 스킬을 추가하거나 기존 스킬을 개선하는 방법 안내.

---

## 새 스킬 추가하기

### 1. 디렉터리 구조 생성

```
.claude/skills/<스킬명>/
├── SKILL.md              # [필수] Claude가 읽는 워크플로우 매뉴얼
├── README.md             # [권장] AI/사람 분석용 이정표
├── scripts/              # [옵션] Python 도구 스크립트
├── templates/            # [옵션] 템플릿 리소스
├── references/           # [옵션] 참조 문서 (토큰 절약용 분리)
└── examples/             # [옵션] 샘플 쿼리
    └── sample-queries.md
```

### 2. SKILL.md 작성

최소 요건:

```yaml
---
name: 스킬명
description: "한 줄 설명 + Trigger 키워드 명시"
context: fork              # 서브에이전트에서 실행
agent: general-purpose
effort: high
allowed-tools: Bash Read Write Edit
---
```

권장 구조:
- **쿼리 섹션**: `$ARGUMENTS` 처리
- **의사결정 트리**: 키워드 → 워크플로우 매핑 테이블
- **워크플로우**: 번호 붙인 Step별 설명
- **규칙**: 금지 사항과 핵심 원칙

기존 스킬 (`hwpx-docgen`, `skill-finder`)을 참고하세요.

### 3. README.md 작성

AI가 스킬을 빠르게 파악할 수 있도록 작성:
- 한 줄 요약
- 무엇을 할 수 있는가 (입출력 예시)
- 핵심 설계 원칙
- 폴더 구조
- 의존성 / 동작 플로우 / 제약 사항
- 트리거 키워드

기존 README 파일을 템플릿으로 사용하세요.

### 4. 테스트

`examples/sample-queries.md`에 최소 3개 이상의 샘플 쿼리와 기대 출력을 명시합니다. Claude Code에서 실제로 실행해 smoke test를 통과시킵니다.

### 5. PR 제출

브랜치명: `feature/<스킬명>` 또는 `fix/<이슈>`
커밋 메시지: Conventional Commits 스타일 사용 (예: `feat(skill-name): 설명`)

---

## 기존 스킬 개선하기

### 버그 수정
1. 이슈 확인 후 재현
2. 수정 후 `sample-queries.md`로 smoke test
3. `fix:` 커밋 메시지로 PR

### 기능 추가
1. SKILL.md 워크플로우 업데이트
2. 필요 시 README.md 동기화
3. `feat:` 커밋 메시지로 PR

### 리팩토링
1. 외부 동작(입출력)이 변경되지 않는지 확인
2. 기존 sample-queries가 계속 통과하는지 검증
3. `refactor:` 커밋 메시지로 PR

---

## 커밋 메시지 스타일

Conventional Commits 권장:

```
feat(hwpx-docgen): 표 병합 지원 추가
fix(skill-finder): 소스 URL 깨진 링크 수정
docs: README에 설치 가이드 보강
refactor(hwpx-docgen): python-hwpx Skeleton 기반으로 재구축
chore: 불필요한 파일 정리
```

---

## 로컬 개발 환경

```bash
git clone https://github.com/BaekKyunShin/Automation-Claude-Skills.git
cd Automation-Claude-Skills
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install python-hwpx lxml
claude
```

---

## 문의

이슈/PR은 이 레포의 Issues 탭을 활용해주세요.
