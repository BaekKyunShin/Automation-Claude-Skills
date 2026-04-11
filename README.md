# Automation-Claude-Skills

한국생산성본부(KPC) 업무·강의·멘토링에 사용할 Claude Code Agent Skills 모음.

---

## 이 레포가 해결하는 문제

한국생산성본부에서는 공문, 보고서, 회의록, 제안서, 강사 이력서 등 **한글(HWPX) 문서를 반복적으로 작성**합니다. 이 레포는 Claude Code의 스킬 시스템을 활용해 자연어 요청만으로 한글 문서를 자동 생성·편집할 수 있게 합니다.

**핵심 가치**: "공문 만들어줘" 한마디로 서식이 완비된 .hwpx 파일 생성. 기존 한글 양식에 내용만 자동 채우기도 가능.

---

## 기술 스택 및 의존성

| 구성 요소 | 역할 |
|---|---|
| **Claude Code** | AI 에이전트 런타임. `.claude/skills/` 내 SKILL.md를 자동 인식 |
| **python-hwpx** | HWPX(한컴오피스 XML) 문서 조작 Python 라이브러리. 내장 Skeleton 기반 문서 생성 |
| **lxml** | python-hwpx 내부 의존성 (XML 파싱) |
| **Python 3.8+** | 스크립트 실행 환경 |

---

## 동작 플로우

```
사용자 (자연어 요청)
    │
    ▼
Claude Code ── SKILL.md 읽음 (워크플로우 매뉴얼)
    │
    ├─ 모드 A: 내장 템플릿 사용
    │   HwpxDocument.open("templates/gonmun.hwpx")
    │   → 플레이스홀더 치환 → 저장
    │
    ├─ 모드 B: 사용자 양식 사용
    │   HwpxDocument.open("사용자_양식.hwpx")
    │   → 플레이스홀더 치환 → 저장
    │
    └─ 모드 C: 빈 문서에서 자유 생성
        HwpxDocument.new()
        → add_paragraph() / add_table() → 저장
    │
    ▼
출력: .hwpx 파일 (한컴오피스에서 열기 가능)
```

**스킬(SKILL.md)은 자동화 스크립트가 아닙니다.** Claude에게 주는 작업 매뉴얼이며, Claude가 이를 읽고 상황에 맞는 Python 코드를 작성·실행합니다.

---

## 파일 역할 맵

```
Automation-Claude-Skills/
│
├── README.md                              ← 이 파일 (레포 전체 안내)
├── .gitignore
│
└── .claude/skills/hwpx-docgen/            ← HWPX 문서 생성 스킬
    │
    ├── SKILL.md                           ← [AI용] Claude가 읽는 워크플로우 매뉴얼
    │                                         의사결정 트리, 5개 워크플로우, 규칙 정의
    │
    ├── templates/                         ← 내장 문서 템플릿 (.hwpx)
    │   ├── base.hwpx                         빈 문서
    │   ├── gonmun.hwpx                       공문 (발신·수신·제목·본문)
    │   ├── report.hwpx                       보고서 (장·절 구조)
    │   ├── minutes.hwpx                      회의록 (메타 표 + 안건·결정)
    │   └── proposal.hwpx                     제안서 (개요·예산·기대효과)
    │
    ├── scripts/                           ← Python 도구 스크립트
    │   ├── build_hwpx.py                     템플릿 + JSON → .hwpx 빌드
    │   ├── zip_replace_all.py                .hwpx 내 플레이스홀더 치환
    │   ├── validate_hwpx.py                  문서 구조 검증
    │   ├── extract_text.py                   텍스트 추출 (plain/markdown/json)
    │   ├── analyze_template.py               문서 구조 분석
    │   ├── generate_templates.py             템플릿 재생성 도구
    │   ├── table_gen.py                      독립 표 생성
    │   └── page_guard.py                     페이지 수 추정
    │
    ├── references/                        ← 참조 문서
    │   ├── owpml-format.md                   OWPML XML 규격 요약
    │   ├── table-xml-spec.md                 표 XML 구조 레퍼런스
    │   └── api.md                            스크립트 API 레퍼런스
    │
    └── examples/
        └── sample-queries.md              ← 테스트용 샘플 쿼리 5종
```

---

## 현재 설치된 스킬

| 스킬 | 트리거 키워드 | 용도 |
|---|---|---|
| `hwpx-docgen` | 한글 문서, HWPX, 생성, 편집, 분석, 표 | HWPX 한글 문서 생성·편집·분석·표 만들기 |
| `skill-finder` | 스킬 찾아줘, find skill, search skills | 9개 검증 소스에서 Claude Code 스킬 검색·비교·추천 |

---

## 제약 사항

| 항목 | 내용 |
|---|---|
| **지원 형식** | `.hwpx`만 지원. `.hwp`(구버전 바이너리)는 미지원 |
| **한글 변환** | `.hwp` → `.hwpx` 변환은 한컴오피스에서 "다른 이름으로 저장" 필요 |
| **실행 환경** | Claude Code가 설치된 환경에서만 동작 |
| **문서 조작** | python-hwpx API를 통해서만 조작. XML 직접 편집 금지 (OWPML 구조 깨짐 방지) |
| **양식 기반** | 사용자 양식 사용 시 `{{플레이스홀더}}`를 미리 넣으면 정확도 100%. 없어도 분석 후 채우기 가능 |

---

## 사용 방법

### 설치

```bash
git clone https://github.com/BaekKyunShin/Automation-Claude-Skills.git
cd Automation-Claude-Skills
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install python-hwpx lxml
claude
```

### 사용 예시

```
# 내장 템플릿으로 문서 생성
> 공문 만들어줘. 발신: 한국생산성본부, 수신: 삼육대학교, 제목: 협조 요청

# 내 양식에 내용 채우기
> 강사프로필양식.hwpx에 이름: 홍길동, 소속: ABC회사로 채워줘

# 문서 분석
> document.hwpx 분석해줘. 마크다운으로 텍스트도 추출해줘
```

---

## 확장 가이드

새 스킬을 추가하려면:

1. `.claude/skills/<스킬명>/SKILL.md` 생성
2. SKILL.md에 트리거 키워드, 워크플로우, 규칙 정의
3. 필요 시 `scripts/`, `templates/`, `references/` 하위 디렉터리 추가
4. Claude Code가 자동으로 인식 (재시작 필요)
