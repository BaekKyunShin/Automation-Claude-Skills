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

### Step 1 — Load the source guide

Read [references/sources.md](references/sources.md). This file lists the 9 verified sources with install commands and search notes. **Do not hard-code source URLs in this file** — always consult `sources.md`, so updates stay in one place.

Note the two groups defined in `sources.md`:
- **Group A (Embedded)**: repos that contain actual `SKILL.md` files. Search method: fetch the repo tree or skills directory, look for skill names matching the query.
- **Group B (Index)**: awesome lists / catalogs of external links. Search method: fetch the README, scan link text and descriptions for matches.

The groups only describe **how to search each source**, not how to present results.

### Step 2 — Search all 9 sources exhaustively

Search every source. Use parallel tool calls wherever possible. Match the response language to the query language (Korean in, Korean out).

1. `anthropics/skills` (Group A) — fetch repo tree, look for matching skill names
2. `sickn33/antigravity-awesome-skills` (Group A) — largest catalog, search the skills index
3. `alirezarezvani/claude-skills` (Group A) — browse the 9 domain folders
4. `huggingface/skills` (Group A) — if query relates to ML / data / HF ecosystem
5. `ComposioHQ/awesome-claude-skills` (Group B) — best for SaaS / API integrations
6. `hesreallyhim/awesome-claude-code` (Group B) — broad Claude Code curation
7. `VoltAgent/awesome-agent-skills` (Group B) — 1,000+ multi-agent entries
8. `travisvn/awesome-claude-skills` (Group B) — Claude-only curated set
9. `BehiSecc/awesome-claude-skills` (Group B) — Claude-first with multi-tool refs

**If all 9 return weak signals**, fall back to the GitHub direct search patterns listed in `sources.md` (`path:SKILL.md "<keyword>"` etc.).

### Step 3 — Rank the matches

Produce a **single ranked list** across all 9 sources. Rank by match strength:

1. Exact keyword match in skill name
2. Exact keyword match in description
3. Related-term match
4. Weak signal (category only)

**Cap the output at 7 total entries.** If more exist, mention the residual count in the verdict line.

### Step 4 — Cross-verify the `Action` value

For each entry, populate the `Action` column with one of:
- A copy-paste-ready install command (e.g. `/plugin marketplace add anthropics/skills` then `/plugin install pdf@anthropics-skills`) — confirm the command matches the source repo's README.
- A direct URL to the skill — when the entry is an Index entry, link to the actual destination, not the awesome list.
- `(manual: git clone <url>)` — only when no install path is documented.

**Never fabricate install commands.** When uncertain, fall back to the `(manual: ...)` form.

### Step 5 — Output

Respond in the user's language. Use the format below verbatim.

## Output format

```
## 판정 (1-line verdict)
<One sentence summary. E.g. "Anthropic 공식 docx 스킬이 1순위, 그 외 2개 관련 스킬 발견.">

## 매치 결과

| # | Skill | 출처 | ⭐ | Action | 매치 이유 |
|---|---|---|---|---|---|
| 1 | <skill-id> | <owner/repo> | <stars> | `<install command>` or `<https://url>` | <why it matches> |

## Next action
<One sentence. E.g. "1번 스킬을 바로 설치해서 써보세요." or "강한 매치가 없으므로 직접 새 스킬을 만드는 것이 빠릅니다.">
```

**If no strong match anywhere**, replace the result table with:

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
- **Cap output at 7 total entries.**
- **Respect context: fork.** You are running in a forked subagent. Your final answer is the only thing the main conversation sees — make it self-contained.

## Additional resources

- [references/sources.md](references/sources.md) — The 9 verified sources with metadata and GitHub search patterns.
- [examples/sample-queries.md](examples/sample-queries.md) — Three sample queries and expected output shapes.
