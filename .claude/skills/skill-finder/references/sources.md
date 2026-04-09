# Source Guide for skill-finder

**Last verified**: 2026-04-09
**Verification method**: GitHub API (stars, forks, pushed_at) + WebFetch (README, Claude Code support)

This file catalogs the 9 verified sources that `skill-finder` searches. All entries passed these criteria:

1. URL exists and is reachable (no 403 / 404 / dead domains)
2. 1,000+ stars **OR** official vendor (Anthropic / HuggingFace)
3. Pushed within the last 3 months
4. Explicit Claude Code support (SKILL.md format or `/plugin marketplace add`)

---

The 9 sources are split into two groups **by their storage structure**, which determines how to search them:

- **Group A (Embedded)** — repos that contain actual `SKILL.md` files. Search method: fetch the repo tree or skills directory, match skill names / descriptions against the query.
- **Group B (Index)** — awesome lists / catalogs that link to external skills. Search method: fetch the README, scan link text and surrounding descriptions for matches, then follow links to the actual source for verification.

The groups are **not** used to rank or group the output. `skill-finder` produces a single ranked list across all 9 sources.

---

## Group A — Embedded (actual SKILL.md files in repo, installable)

### A1. anthropics/skills

- **URL**: https://github.com/anthropics/skills
- **Stars**: 113,728
- **Last push**: 2026-04-08
- **Install**:
  ```
  /plugin marketplace add anthropics/skills
  /plugin install <skill-name>@anthropics-skills
  ```
- **Strengths**: Anthropic official. SKILL.md spec authority. Ships document skills (`docx`, `pdf`, `pptx`, `xlsx`) and general categories.
- **Structure**: `skills/<category>/<skill-name>/SKILL.md`
- **When to prefer**: when the user wants the official, spec-compliant, well-tested skill.

### A2. sickn33/antigravity-awesome-skills

- **URL**: https://github.com/sickn33/antigravity-awesome-skills
- **Stars**: 31,780
- **Last push**: 2026-04-09
- **Install**:
  ```
  npx antigravity-awesome-skills --claude
  ```
- **Strengths**: 1,392+ skills. Multi-agent support (Claude Code / Cursor / Codex / Gemini / Copilot / Windsurf). Largest breadth of any single installable source.
- **Structure**: `skills/<skill-name>/SKILL.md` + installer CLI
- **When to prefer**: when maximum breadth is needed or when A1 is thin on the domain.

### A3. alirezarezvani/claude-skills

- **URL**: https://github.com/alirezarezvani/claude-skills
- **Stars**: 10,162
- **Last push**: 2026-04-08
- **Install**:
  ```
  /plugin marketplace add alirezarezvani/claude-skills
  /plugin install <skill-name>@claude-code-skills
  ```
- **Strengths**: 156+ skills across 9 domains (engineering, devops, data, docs, etc.). stdlib-only Python design.
- **Structure**: embedded SKILL.md + plugin marketplace
- **When to prefer**: development-focused skills (testing, refactoring, CI/CD).

### A4. huggingface/skills

- **URL**: https://github.com/huggingface/skills
- **Stars**: 10,114
- **Last push**: 2026-04-09
- **Install**:
  ```
  /plugin marketplace add huggingface/skills
  /plugin install <skill-name>@huggingface/skills
  ```
- **Strengths**: HuggingFace official. 12 ML / data skills (hf-cli, huggingface-datasets, huggingface-gradio, huggingface-llm-trainer, transformers-js, etc.).
- **Caveat**: ML / data domain only. Not useful for office documents or SaaS automation.
- **When to prefer**: ML training, dataset curation, model deployment, inference.

---

## Group B — Index (awesome lists with external links, not embedded storage)

### B1. ComposioHQ/awesome-claude-skills

- **URL**: https://github.com/ComposioHQ/awesome-claude-skills
- **Stars**: 52,378
- **Last push**: 2026-02-19
- **Strengths**: Claude-specific ecosystem index. Strong on SaaS / API integrations — Slack, Notion, Jira, GitHub, Linear, CRM systems, workflow automation.
- **When to prefer**: connecting Claude Code to external SaaS or API services.

### B2. hesreallyhim/awesome-claude-code

- **URL**: https://github.com/hesreallyhim/awesome-claude-code
- **Stars**: 37,648
- **Last push**: 2026-04-09
- **Strengths**: Comprehensive Claude Code curation. Covers Skills **and** Hooks, Slash commands, CLAUDE.md examples, and agent patterns.
- **When to prefer**: broad Claude Code discovery beyond just skills.

### B3. VoltAgent/awesome-agent-skills

- **URL**: https://github.com/VoltAgent/awesome-agent-skills
- **Stars**: 14,894
- **Last push**: 2026-04-04
- **Strengths**: 1,000+ entries. Multi-agent index (Claude / Cursor / Codex / Gemini / Copilot / Windsurf / OpenCode). Aggregates official vendor skills (Vercel, Stripe, Cloudflare, Figma, React).
- **Caveat**: aggregator only — points to external sources.
- **When to prefer**: broad multi-agent discovery or finding official vendor-authored skills.

### B4. travisvn/awesome-claude-skills

- **URL**: https://github.com/travisvn/awesome-claude-skills
- **Stars**: 10,866
- **Last push**: 2026-03-16
- **Strengths**: Claude-only curation. Indexes obra/superpowers and other well-known Claude skill sets.
- **When to prefer**: Claude-specific, smaller curated set.

### B5. BehiSecc/awesome-claude-skills

- **URL**: https://github.com/BehiSecc/awesome-claude-skills
- **Stars**: 8,297
- **Last push**: 2026-04-01
- **Strengths**: Claude-centric but with multi-tool references (Cursor / Copilot / Windsurf / Zed / Continue.dev). Uses `agentskill.sh` marketplace paths.
- **When to prefer**: Claude-first but open to multi-tool alternatives.

---

## GitHub search patterns (fallback)

When all 9 sources above return weak matches, use `WebSearch` with these query templates:

| Pattern | Use for |
|---|---|
| `path:SKILL.md "<domain keyword>"` | Direct SKILL.md file search across GitHub |
| `topic:claude-skills sort:updated` | Recently updated skills catalogued with the topic |
| `"SKILL.md" "allowed-tools" pushed:>2026-01-01` | Active skills touched in the last few months |
| `"<app name>" "SKILL.md"` | App-specific skills (e.g. Notion, Slack) |
| `site:github.com "/plugin marketplace add" "<keyword>"` | Installable plugin marketplaces |

---

## Explicitly excluded sources (do not use)

These were evaluated and rejected on 2026-04-09:

| Source | Reason |
|---|---|
| Skills.sh | Domain does not respond (curl exit 000 + WebFetch 403) |
| skillsmp.com | Domain does not respond |
| awesomeclaude.ai | Domain does not respond |
| microsoft/skills | Azure / Copilot-only, no Claude Code support |
| daymade/claude-code-skills | 804 stars, below 1k non-official threshold |
| mhattingpete/claude-skills-marketplace | 542 stars, below 1k threshold |
| abubakarsiddik31/claude-skills-collection | 594 stars, below 1k threshold |
| karanb192/awesome-claude-skills | 246 stars + 6-month+ stagnation |
| GitHub topic `claude-skills` | Meta page, not a curated source |

---

## Korean sources — status

As of 2026-04-09, **no Korean-community source meets the selection bar** (1k+ stars + recent activity + not merely a docs mirror). Candidates checked and rejected:

- `bear2u/my-skills` — 813 ⭐ but personal mix with 1-line Korean descriptions, 2-month+ stagnation
- `modu-ai/cc-plugins` — 58 ⭐, below threshold
- `seilk/claude-code-docs` — 366 ⭐, documentation mirror (not skills)
- `claudecode.co.kr` — domain unreachable from our environment

**Action**: when a qualifying Korean source appears, add it to Group A or B above with the same metadata format. Document the date and reason in the commit message.

---

## Maintenance schedule

- **Monthly**: re-verify star counts and `last push` dates. Move stagnated sources to the excluded list.
- **Ad-hoc**: when a source goes 404 or is archived, replace it immediately and bump `Last verified`.
- **Commit discipline**: every edit to this file must update the `Last verified` timestamp at the top.
