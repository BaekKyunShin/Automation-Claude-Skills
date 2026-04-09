# Sample Queries for skill-finder

These three queries validate the skill's behavior across different scenarios. Use them as smoke tests after editing `SKILL.md` or `references/sources.md`.

---

## Query 1 — Korean, high-confidence match expected

```
/skill-finder PDF 생성 스킬
```

**What to check:**

- Response is in **Korean** (matches query language).
- A single ranked **매치 결과** table, with `anthropics/skills` PDF skill in position 1.
- Its `Action` cell shows the install command verbatim:
  ```
  /plugin marketplace add anthropics/skills
  /plugin install pdf@anthropics-skills
  ```
- Other entries below it may come from any of the 9 sources — some with install commands, some with direct URLs — ranked by match strength.
- Total entries ≤ 7.

**Pass criterion**: the user can copy-paste the row-1 install command and it works on the next Claude Code session.

---

## Query 2 — English, broad exploration

```
/skill-finder Slack automation
```

**What to check:**

- Response is in **English** (matches query language).
- The single result table includes Slack-related entries drawn from across the 9 sources. `ComposioHQ/awesome-claude-skills` is typically a top source for SaaS automation, but the ranking is determined by match strength, not source type.
- The `Action` column is populated correctly for each row: install commands for rows backed by an embedded skill, direct URLs for rows drawn from awesome lists.
- **Never link to the awesome list URL itself** — always follow the link to the actual skill source.

**Pass criterion**: the user gets at least 2 actionable rows (install command or direct skill URL), regardless of which source they came from.

---

## Query 3 — No strong match, Korean (regression test)

```
/skill-finder 한글 HWP 문서 생성
```

**What to check:**

- Response is in **Korean**.
- The **매치 결과** table is replaced by the fallback template:
  ```
  ## 매치 없음 (No strong match)

  가장 가까운 2개 대안:
  - anthropics/skills의 docx 스킬 — <이유>
  - anthropics/skills의 pdf 스킬 — <이유>

  대안 경로:
  pyhwpx 또는 python-hwpx 라이브러리를 래핑한 새 스킬을 만드는 것이 빠릅니다.
  ```
- **No fabricated install commands** for skills that don't exist.

**Pass criterion**: the skill honestly reports failure and suggests the correct fallback path (build a new skill using pyhwpx-class libraries).

---

## How to run

In a Claude Code session with this project loaded:

1. Type one of the queries above.
2. Compare the output against the "What to check" bullets.
3. If any check fails, inspect `SKILL.md` (workflow) or `references/sources.md` (source metadata) and fix.

## Adding new sample queries

When you discover a new edge case (e.g. a query that returns too many results, or fails silently), add it here with the same format: query → expected behavior → pass criterion.
