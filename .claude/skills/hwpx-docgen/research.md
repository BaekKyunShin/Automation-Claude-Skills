# hwpx-docgen 조사 보고서

**조사일**: 2026-04-10
**검색 방법**: skill-finder 3개 쿼리 (HWP 한글 문서 생성 / HWPX 한컴오피스 / hangul document generation) + GitHub 직접 검색 + LobeHub·mcpmarket 보완 검색
**검색 범위**: 9개 검증 소스 (sources.md) + GitHub 전체 + LobeHub Skills Marketplace + mcpmarket

---

## 1. 검색 결과 요약

### 9개 검증 소스 내부

| 소스 | 매치 |
|---|---|
| anthropics/skills | 없음 (docx/pdf/pptx/xlsx만 존재) |
| sickn33/antigravity-awesome-skills (1,397개) | 없음 |
| alirezarezvani/claude-skills (233개) | 없음 |
| huggingface/skills (12개) | 없음 (ML 특화) |
| ComposioHQ/awesome-claude-skills | 없음 |
| hesreallyhim/awesome-claude-code | 없음 |
| VoltAgent/awesome-agent-skills | 없음 |
| travisvn/awesome-claude-skills | 없음 |
| BehiSecc/awesome-claude-skills | **1건** (polaris-datainsight-doc-extract) |

**결론**: 9개 검증 소스 중 HWPX 전용 스킬은 사실상 0개. HWP/HWPX는 한국 고유 포맷이라 글로벌 카탈로그에 거의 등재되지 않음.

### GitHub 직접 검색 + LobeHub + mcpmarket

GitHub, LobeHub Skills Marketplace, mcpmarket에서 **총 7개 HWPX 관련 스킬/도구** 발견.

---

## 2. 발견된 HWPX 스킬 전체 목록

| # | 이름 | 출처 | ⭐ | 유형 | 핵심 접근 방식 |
|---|---|---|---|---|---|
| 1 | [Canine89/hwpxskill](https://github.com/Canine89/hwpxskill) | GitHub | 171 | SKILL.md | XML 직접 조작 (lxml), python-hwpx 미사용 |
| 2 | [airmang/hwpx-skill](https://github.com/airmang/hwpx-skill) | GitHub | 5 | SKILL.md | python-hwpx 래핑, ZIP-level 전역 치환 |
| 3 | [nathankim0/easy-hwp](https://github.com/nathankim0/easy-hwp) | GitHub | 4 | SKILL.md | 슬래시 커맨드 3개, 서식 분석→MD 매핑→HWPX 생성 |
| 4 | polaris-datainsight-doc-extract | BehiSecc 목록 | 2 | SKILL.md | Polaris AI API로 HWP/HWPX 데이터 추출 (생성 아님) |
| 5 | seocholaw-hwpx-legal-skill | LobeHub | ? | SKILL.md | 법률 도메인 특화, HWP→HWPX 변환, build_hwpx.py |
| 6 | iamseungpil-claude-for-dslab-hwpx | LobeHub | ? | SKILL.md | 데이터사이언스 도메인 HWPX |
| 7 | HWP & HWPX Document Editor (hwpilot) | mcpmarket | ? | SKILL.md | 계층적 참조 시스템 (섹션/단락/표/이미지 타겟팅) |

**참고 (스킬 아님)**:
- [jkf87/hwp-mcp](https://github.com/jkf87/hwp-mcp) — HWP MCP 서버
- [airmang/hwpx-mcp-server](https://github.com/airmang/hwpx-mcp-server) — HWPX MCP 서버
- [edwardkim/rhwp](https://github.com/edwardkim/rhwp) — Rust+WASM 기반 HWP 뷰어/에디터

---

## 3. 상위 3개 스킬 비교 분석

분석 대상: #1 hwpxskill, #2 hwpx-skill, #3 easy-hwp (SKILL.md 기반 + 충분한 정보 확보)

### 3-1. 기본 정보

| 항목 | hwpxskill (Canine89) | hwpx-skill (airmang) | easy-hwp (nathankim0) |
|---|---|---|---|
| ⭐ | 171 | 5 | 4 |
| 포크 | 58 | 2 | ? |
| 커밋 | 6 | 5 | ? |
| Python 버전 | 3.6+ | 3.x (python-hwpx 의존) | ? |
| 핵심 의존성 | **lxml** (stdlib 외 1개) | **python-hwpx + lxml** | ? |
| 멀티에이전트 | Claude Code / Cursor / Codex CLI | Claude Code / Cursor / Codex CLI | Claude Code 전용 |
| 설치 방식 | git clone → skills/ 복사 | git clone → skills/ 복사 + pip install | `/plugin marketplace add` |

### 3-2. 구현 방식 비교

| 항목 | hwpxskill | hwpx-skill | easy-hwp |
|---|---|---|---|
| **파일 조작** | OWPML XML 직접 조작 | python-hwpx API 래핑 | 불명 (슬래시 커맨드 뒤에 숨겨진 구현) |
| **ZIP 처리** | 직접 unzip/rezip | ZIP-level 전역 치환 (zip_replace_all.py) | 불명 |
| **네임스페이스** | 수동 관리 (OWPML 규칙 문서화) | **자동 정리** (fix_namespaces.py --auto-fix-ns) | 불명 |
| **HWP 바이너리** | 미지원 (HWPX 전용) | 미지원 (HWPX 전용) | 미지원 (HWPX 전용) |
| **pyhwpx 의존** | **없음** (lxml만) | **있음** (python-hwpx 필수) | 불명 |

### 3-3. 기능 매트릭스

| 기능 | hwpxskill | hwpx-skill | easy-hwp |
|---|---|---|---|
| HWPX 생성 (신규) | O (템플릿 기반) | O (프로그래밍적) | O (MD→HWPX) |
| HWPX 편집 (기존) | O (XML 직접) | O (API 기반) | O (서식 채우기) |
| 텍스트 추출 | O (plain/markdown) | O (JSON 출력 CLI) | O (분석 명령) |
| 변수/플레이스홀더 치환 | O | O (ZIP-level 전역) | O (표 빈칸 자동) |
| 구조 검증 | O | - | - |
| 페이지 수 모니터링 | O (기준 문서 대비) | - | - |
| 표 구조 보존 | O (셀 병합 포함) | O | O (표 빈칸 인식) |
| charPr/paraPr 포맷팅 | O (문자·단락 수준) | O (문단/표) | - |
| 이미지 삽입 | - | - | - |
| 슬래시 커맨드 | - | - | O (/hwp-analyze, /hwp-fill, /hwp-template) |
| 자연어 요청 | - | O (SKILL.md 트리거) | O ("IRB 서식에 내용 채워줘") |
| CLI 스크립트 | - | O (3개: text_extract, zip_replace_all, fix_namespaces) | - |
| 내장 템플릿 | O (5개) | - | - |
| 템플릿 관리 명령 | - | - | O (/hwp-template list) |
| HWP→HWPX 변환 | - | - | - |

### 3-4. 템플릿 상세 (hwpxskill)

| 템플릿 | 용도 | 특징 |
|---|---|---|
| base | 최소 문서 | 기본 골격 |
| gonmun (공문) | 공식 문서·공문 | 발신·수신·제목·본문 구조 |
| report (보고서) | 계층형 보고서 | 장·절·항 구조 |
| minutes (회의록) | 회의 기록 | 참석자·안건·결정사항 |
| proposal (제안서) | 제안·기획 | 스타일 헤더 |

### 3-5. 파일 구조 비교

```
# hwpxskill (Canine89)
SKILL.md
scripts/
  build_hwpx.py        # 템플릿 기반 HWPX 조립
  unpack_hwpx.py       # HWPX → 폴더 해제
  pack_hwpx.py         # 폴더 → HWPX 패킹
  analyze_template.py  # 템플릿 심층 분석
  validate_hwpx.py     # HWPX 구조 검증
  extract_text.py      # 텍스트 추출
templates/
  base/                # 최소 템플릿
  gonmun/              # 공문 템플릿
  report/              # 보고서 템플릿
  minutes/             # 회의록 템플릿
  proposal/            # 제안서 템플릿

# hwpx-skill (airmang)
SKILL.md
README.md
references/
scripts/
  text_extract.py      # 텍스트 추출 (JSON)
  zip_replace_all.py   # ZIP-level 전역 치환
  fix_namespaces.py    # 네임스페이스 자동 정리
examples/

# easy-hwp (nathankim0)
SKILL.md
(상세 구조 미확인)
```

---

## 4. 장점 수확 리스트

Step 2 합성 스킬 제작 시 채택할 장점들.

### hwpxskill에서 수확 (출처: Canine89/hwpxskill)

| # | 장점 | 채택 이유 |
|---|---|---|
| 1 | **5개 내장 템플릿** (base/gonmun/report/minutes/proposal) | 한국 실무 문서 유형을 바로 쓸 수 있음. 우리 스킬도 비슷한 템플릿 세트 필요 |
| 2 | **XML 직접 조작** (python-hwpx 미사용) | pyhwpx 배제 방침과 일치. lxml + stdlib만으로 안정적 |
| 3 | **unpack/pack 분리 스크립트** | HWPX 디버깅·분석에 필수. 문제 발생 시 중간 XML 확인 가능 |
| 4 | **페이지 수 모니터링** (기준 문서 대비) | 문서 생성 후 페이지가 늘거나 줄면 경고 → 레이아웃 깨짐 조기 탐지 |
| 5 | **구조 검증 스크립트** (validate_hwpx.py) | 생성된 HWPX가 OWPML 규격에 맞는지 자동 확인 |
| 6 | **charPr/paraPr 수준 포맷팅 문서화** | SKILL.md에 XML 구조 규칙을 상세히 적어서 에이전트가 참조 |
| 7 | **템플릿 심층 분석 스크립트** (analyze_template.py) | 새 템플릿 추가 시 구조 파악 자동화 |

### hwpx-skill에서 수확 (출처: airmang/hwpx-skill)

| # | 장점 | 채택 이유 |
|---|---|---|
| 1 | **ZIP-level 전역 치환** (zip_replace_all.py) | HWPX 내 모든 XML 파일에서 플레이스홀더를 한 번에 치환 → 누락 방지 |
| 2 | **네임스페이스 자동 정리** (fix_namespaces.py) | XML 편집 후 네임스페이스가 꼬이는 문제를 자동 해결 → 안정성 |
| 3 | **--auto-fix-ns 플래그** | 치환 후 자동으로 네임스페이스 정리 → 2단계 작업을 1단계로 |
| 4 | **CLI 스크립트 설계** (독립 실행 가능) | 에이전트 없이도 터미널에서 직접 사용 가능 → 디버깅·배치 처리 |
| 5 | **python-hwpx 원작자 관리** | API 정합성 보장. (단, 우리 스킬은 pyhwpx 미사용이므로 구현 방식이 아닌 "기능 아이디어"만 채택) |

### easy-hwp에서 수확 (출처: nathankim0/easy-hwp)

| # | 장점 | 채택 이유 |
|---|---|---|
| 1 | **슬래시 커맨드 UX** (/hwp-analyze, /hwp-fill, /hwp-template) | 사용자가 기억하기 쉬운 진입점. 자연어보다 명시적 |
| 2 | **서식 분석 → MD 매핑 → HWPX 생성** 워크플로우 | Markdown으로 콘텐츠 준비 → HWPX 서식에 자동 매핑. 콘텐츠/양식 분리 |
| 3 | **표 빈칸 자동 인식** | 서식 문서에서 채워야 할 칸을 자동 탐지 → 사용자가 일일이 지정 불필요 |
| 4 | **자연어 요청 지원** ("IRB 서식에 연구 내용 채워줘") | SKILL.md description에 도메인 키워드를 넣어 자동 트리거 |
| 5 | **plugin marketplace 설치** | `/plugin marketplace add` 한 줄로 설치 → 진입 장벽 최저 |
| 6 | **템플릿 관리 커맨드** (/hwp-template list) | 사용 가능한 템플릿 목록 조회 → 사용자 편의 |

### 추가 발견에서 수확

| # | 출처 | 장점 | 채택 이유 |
|---|---|---|---|
| 1 | seocholaw-hwpx-legal-skill | **HWP→HWPX 변환** 스크립트 | 레거시 .hwp 파일을 HWPX로 변환 후 처리 가능 → 호환성 확대 |
| 2 | seocholaw-hwpx-legal-skill | **도메인 특화 템플릿** (법률) | 도메인별 템플릿 분리 패턴. KPC 교육 도메인에도 적용 가능 |
| 3 | hwpilot (mcpmarket) | **계층적 참조 시스템** (섹션/단락/표/이미지 타겟팅) | 대형 문서에서 특정 위치를 정밀하게 지정 → 편집 정확도 향상 |

---

## 5. 합성 스킬 설계 핵심 인사이트

### 채택 방향

| 영역 | 채택 출처 | 구체적 내용 |
|---|---|---|
| **구현 방식** | hwpxskill | XML 직접 조작 (lxml). python-hwpx 미사용 |
| **템플릿 세트** | hwpxskill | 5개 기본 템플릿 구조 참고. KPC 도메인 확장 |
| **ZIP 치환** | hwpx-skill | ZIP-level 전역 치환 아이디어. 단, 구현은 lxml로 자체 작성 |
| **네임스페이스 관리** | hwpx-skill | 편집 후 자동 정리 로직 필수 |
| **사용자 경험** | easy-hwp | 슬래시 커맨드 + 자연어 트리거 병행 |
| **콘텐츠/양식 분리** | easy-hwp | MD → HWPX 매핑 패턴 |
| **품질 검증** | hwpxskill | 구조 검증 + 페이지 수 모니터링 |
| **도메인 확장성** | seocholaw | 도메인별 템플릿 분리 패턴 |
| **정밀 편집** | hwpilot | 계층적 참조 시스템 아이디어 |

### 미지원 기능 (현재 어떤 스킬에도 없음)

- 이미지 삽입 자동화
- 머리글/바닥글 동적 생성
- 다중 섹션 문서 (예: 목차 + 본문 + 부록) 자동 조립
- 폰트 임베딩/확인
- 한글 맞춤법 검사 연동
- 배치 생성 (여러 문서 한번에)

→ 이 중 일부는 우리 스킬에서 새로 구현할 기회.

---

## 6. 출처

### 스킬

- [Canine89/hwpxskill](https://github.com/Canine89/hwpxskill) — ⭐171, HWPX XML 직접 조작
- [airmang/hwpx-skill](https://github.com/airmang/hwpx-skill) — ⭐5, python-hwpx 기반
- [nathankim0/easy-hwp](https://github.com/nathankim0/easy-hwp) — ⭐4, Claude Code 슬래시 커맨드
- [polaris-datainsight-doc-extract](https://github.com/jacob-g-park/polaris-datainsight-doc-extract) — ⭐2, 데이터 추출
- [seocholaw-hwpx-legal-skill](https://lobehub.com/ko/skills/seocholaw-hwpx-legal-skill) — LobeHub, 법률 도메인
- [iamseungpil-claude-for-dslab-hwpx](https://lobehub.com/ko/skills/iamseungpil-claude-for-dslab-hwpx) — LobeHub, DS 도메인
- [HWP & HWPX Document Editor (hwpilot)](https://mcpmarket.com/tools/skills/hwp-hwpx-document-editor) — mcpmarket

### 관련 도구 (스킬 아님)

- [airmang/hwpx-mcp-server](https://github.com/airmang/hwpx-mcp-server) — HWPX MCP 서버
- [jkf87/hwp-mcp](https://github.com/jkf87/hwp-mcp) — HWP MCP 서버
- [airmang/python-hwpx](https://github.com/airmang/python-hwpx) — HWPX Python 라이브러리
- [edwardkim/rhwp](https://github.com/edwardkim/rhwp) — Rust+WASM HWP 뷰어/에디터

### 검색 소스

- BehiSecc/awesome-claude-skills — 9개 검증 소스 중 유일한 매치
- LobeHub Skills Marketplace (lobehub.com/skills)
- mcpmarket.com
