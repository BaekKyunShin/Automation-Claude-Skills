# Sample Queries for skill-finder

These three queries validate the skill's behavior across different scenarios. Use them as smoke tests after editing `SKILL.md` or `references/sources.md`.

---

## Query 1 — Install-ready, Korean

```
/skill-finder PDF 생성 스킬
```

**What to check:**

- Response is in **Korean** (matches query language).
- **Embedded group is populated first**, with `anthropics/skills` PDF skill in position 1.
- Install command is shown **verbatim**:
  ```
  /plugin marketplace add anthropics/skills
  /plugin install pdf@anthropics-skills
  ```
- Index group may include 1–2 additional references from awesome lists.
- Total entries ≤ 7.

**Pass criterion**: the user can copy-paste the install command and it works on the next Claude Code session.

---

## Query 2 — Broad exploration, English

```
/skill-finder Slack automation
```

**What to check:**

- Response is in **English** (matches query language).
- **Index group is populated first or equally**, with `ComposioHQ/awesome-claude-skills` as a top source (strongest for SaaS / API automation).
- Embedded group may still have entries from `sickn33` or `alirezarezvani` if they include Slack-related skills.
- Each Index entry includes a **direct link** to the external source (not just the awesome list URL).
- Each Embedded entry includes an install command.

**Pass criterion**: the user gets at least 2 actionable options across both groups.

---

## Query 3 — No strong match, Korean (regression test)

```
/skill-finder 한글 HWP 문서 생성
```

**What to check:**

- Response is in **Korean**.
- Embedded group is **empty or shows "없음"**.
- Output uses the fallback template:
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
3. If any check fails, inspect `SKILL.md` (workflow) or `references/sources.md` (routing) and fix.

## Adding new sample queries

When you discover a new edge case (e.g. a query that returns too many results, or fails silently), add it here with the same format: query → expected behavior → pass criterion.
