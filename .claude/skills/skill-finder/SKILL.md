---
name: skill-finder
description: "Finds Claude Code Skills from 9 verified sources (Anthropic, HuggingFace, large catalogs). Trigger phrases: 스킬 찾아줘, find skill for X, search skills, any skill for Y, or before creating a new skill to avoid duplication."
context: fork
agent: general-purpose
effort: high
allowed-tools: WebSearch WebFetch Read Grep
---

# skill-finder

Search for existing Claude Code Skills across 9 verified sources before building a new one. Returns a compact, ranked table of matches with copy-paste-ready install commands.

## Query

$ARGUMENTS

## Workflow

### Step 1 — Parse the query

Extract from `$ARGUMENTS`:
- **Domain / task**: what the user wants a skill for (e.g. "PDF generation", "Slack automation", "Korean HWP documents")
- **Intent**: `install-ready` (wants to use immediately) vs `explore` (wants to browse options)
- **Language**: Korean or English — the response must match the user's language

### Step 2 — Load the source guide

Read [references/sources.md](references/sources.md). This file lists the 9 verified sources, their install commands, domain strengths, and routing hints. **Do not hard-code source URLs here** — always consult that file, so updates stay in one place.

### Step 3 — Search all 9 sources

Search exhaustively (no tiered stop conditions). Use parallel tool calls wherever possible.

**For Group A (Embedded — actual SKILL.md files in repo):**
1. `anthropics/skills` — fetch repo tree or README, look for matching skill names
2. `sickn33/antigravity-awesome-skills` — largest catalog, search the skills index
3. `alirezarezvani/claude-skills` — browse the 9 domain folders
4. `huggingface/skills` — only if query relates to ML / data / HF ecosystem

**For Group B (Index — awesome lists with external links):**
5. `ComposioHQ/awesome-claude-skills` — best for SaaS / API integrations
6. `hesreallyhim/awesome-claude-code` — broad Claude Code curation
7. `VoltAgent/awesome-agent-skills` — 1,000+ multi-agent entries
8. `travisvn/awesome-claude-skills` — Claude-only curated set
9. `BehiSecc/awesome-claude-skills` — Claude-first with multi-tool refs

**If all 9 are weak**, fall back to GitHub direct search using the patterns in `references/sources.md` (`path:SKILL.md "<keyword>"` etc.).

### Step 4 — Rank and group

- **Group A (Embedded)** is listed first. These skills can be installed immediately.
- **Group B (Index)** is listed second. These are pointers to external repos that still need verification.
- Within each group, rank by match strength:
  1. Exact keyword match in skill name
  2. Exact keyword match in description
  3. Related-term match
  4. Weak signal (category only)
- **Cap the output at 7 total entries** across both groups. If there are more, mention the count in the summary.

### Step 5 — Cross-verify install commands

Before outputting any install command, confirm it matches the source repo's README. **Never fabricate an install path.** If an install command is not clearly documented, output `(manual: git clone <url>)` instead.

### Step 6 — Output

Respond in the same language as the user's query. Use the format below verbatim.

## Output format

```
## 판정 (1-line verdict)
<One sentence summary. E.g. "Anthropic 공식 docx 스킬이 1순위, 그 외 2개 관련 스킬 발견.">

## 🟢 Embedded (바로 설치 가능 / Ready to install)

| # | Skill | Source | ⭐ | Install | Match reason |
|---|---|---|---|---|---|
| 1 | <skill-id> | <owner/repo> | <stars> | `<install command>` | <why it matches> |

## 🔵 Index (외부 링크 / Awesome list entries)

| # | Skill / Entry | Listed in | Link | Match reason |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Next action
<One sentence. E.g. "1번 스킬을 바로 설치해서 써보세요." or "강한 매치가 없으므로 직접 새 스킬을 만드는 것이 빠릅니다.">
```

**If no strong match in any group**, replace the tables with:

```
## 매치 없음 (No strong match)

가장 가까운 2개 대안 / Closest alternatives:
- <Link 1> — <why it's similar>
- <Link 2> — <why it's similar>

대안 경로 / Fallback path:
<One sentence suggesting whether to build a new skill directly, e.g. "관련 Python 라이브러리를 직접 래핑하는 새 스킬을 만드는 것이 빠를 수 있음.">
```

## Rules

- **No verbose README quoting.** Return only repo paths, skill IDs, and install commands.
- **Cross-verify install commands.** Never fabricate. If uncertain, output `(manual: git clone …)`.
- **Match user language.** Korean query → Korean response. English query → English response.
- **Honest reporting.** If no match, say "없음 / No strong match" and suggest a fallback.
- **Prefer Embedded over Index** when both have matches (user can install right away).
- **Cap output at 7 total entries** across both groups.
- **Respect context: fork.** You are running in a forked subagent. Your final answer is the only thing the main conversation sees — make it self-contained.

## Additional resources

- [references/sources.md](references/sources.md) — The 9 verified sources with metadata, routing hints, and GitHub search patterns.
- [examples/sample-queries.md](examples/sample-queries.md) — Three sample queries and expected output shapes.
