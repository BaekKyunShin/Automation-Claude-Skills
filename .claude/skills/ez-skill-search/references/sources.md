# Source Guide

Use this file only after `ez-skill-search` triggers.

## Core Sources

- `Skills.sh`
  - URL: `https://skills.sh/`
  - Docs: `https://skills.sh/docs/faq`
  - Best for: newest installable skills and owner/skill identifiers
  - Use first when the user wants something installable now
- `alirezarezvani/claude-skills`
  - URL: `https://github.com/alirezarezvani/claude-skills`
  - Best for: large direct library with real skill folders and domain coverage
  - Use when the query is broad, role-based, or domain-heavy
- `VoltAgent/awesome-agent-skills`
  - URL: `https://github.com/VoltAgent/awesome-agent-skills`
  - Best for: aggregator-style discovery, official sources, and upstream project links
  - Use when the user wants trusted or official ecosystems
- `ComposioHQ/awesome-claude-skills`
  - URL: `https://github.com/ComposioHQ/awesome-claude-skills`
  - Best for: SaaS actions, API integrations, and workflow automation
  - Use when the query mentions tools like Slack, Notion, GitHub, Jira, or CRM systems
- `abubakarsiddik31/claude-skills-collection`
  - URL: `https://github.com/abubakarsiddik31/claude-skills-collection`
  - Best for: smaller curated lists and practical picks
  - Use when the user wants concise recommendations rather than maximum coverage
- `sickn33/antigravity-awesome-skills`
  - URL: `https://github.com/sickn33/antigravity-awesome-skills`
  - Hosted catalog: `https://sickn33.github.io/antigravity-awesome-skills/`
  - Best for: very large fallback catalog, bundles, workflows, and installer-friendly discovery
  - Use when earlier sources are thin or the user wants breadth

## Fast Routing

- Need a fresh installable skill: `Skills.sh` -> `sickn33`
- Need a domain library: `alirezarezvani`
- Need official or vendor-backed pointers: `VoltAgent`
- Need SaaS or API workflow skills: `ComposioHQ`
- Need a short curated set: `abubakarsiddik31`
- Need maximum coverage: `sickn33`

## Query Patterns

- Base pattern: `<tool> <task>`
- Add host only if needed: `<tool> <task> codex`
- Add integration pair for actions: `<app1> <app2> automation`
- Add domain qualifier for broad requests: `<domain> workflow`, `<domain> analysis`, `<domain> review`
- Keep first-pass queries short: 2-4 keywords

## Stop Conditions

- Stop after 3 strong matches.
- Stop after 1 strong winner plus 2 credible alternatives.
- Expand to lower-priority sources only when the first pass is weak or repetitive.

## Result Hygiene

- Prefer exact skill ids, repo subpaths, or catalog entries over repo-level summaries.
- Mark aggregator-only results as `aggregator only`.
- If install instructions are visible, include the shortest reliable command or path.
- If the source only proves existence but not fit, leave it out.
