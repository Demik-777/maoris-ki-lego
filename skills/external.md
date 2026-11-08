# External Claude Code skill sources (not yet copied into this repo)

Reference entries for skill collections worth installing directly via Claude Code plugin marketplace, rather than duplicated file-by-file here.

## daymade/claude-code-skills
Professional Claude Code skills marketplace, production-ready.
- Install: `claude plugin marketplace add daymade/claude-code-skills`
- Notable: `photo-to-scanned-pdf` — turns phone photos of receipts/contracts/forms into a clean A4 PDF (useful for NS admin/audit scans)
- Notable: `github-review-pr` — reviews/re-reviews PRs against the live base
- Notable: financial data suite — investment-research and financial data workflows
- Source: https://github.com/daymade/claude-code-skills

## glebis/claude-skills
Actively maintained collection, frequent additions.
- Install: `claude plugin marketplace add glebis/claude-skills`
- Categories: meetings & transcripts, research & knowledge, writing/design/publishing, images/audio/media, personal analytics, Claude Code ops
- Recent (2026-07): font-features, typography (RU/EN/DE/FR smart quotes/dashes)
- Source: https://github.com/glebis/claude-skills

## evolsb/claude-legal-skill
Contract review skill with CUAD risk detection, market benchmarks, lawyer-ready redlines (tracked-changes .docx, redline PDFs, negotiation memos).
- Install: `git clone https://github.com/evolsb/claude-legal-skill ~/.claude/skills/contract-review`
- Benchmark: F1 ~0.62 on clause extraction (ContractEval) — first-pass review, not a replacement for attorney review on material deals
- Default focus: US law — provisions vary by jurisdiction, verify for DE/EU contracts
- Source: https://github.com/evolsb/claude-legal-skill

## ✅ skills/business/ refreshed (08.08.2026)
Re-synced from alirezarezvani/claude-skills: business-growth (44), c-level (287, incl. founder-mode personas + general-counsel-advisor), finance (27), pm/project-management (74) — 432 files total, up from the original ~386. Source repo continues to grow beyond these 4 categories (engineering, marketing, product, compliance, research-ops) — those are out of scope for `skills/business/`, not pulled in.

## External project frameworks and applications

These are separate forked projects, not directly installable Claude Code skills. Evaluate them alongside local materials when choosing an approach for project development.

| Project | Our fork | Routing and requirements |
|---|---|---|
| LLM Council by Andrej Karpathy (консилиум) | https://github.com/Demik-777/llm-council | [Project tools](../reference/project-tools.md#llm-council--консилиум-карпати) |
| AutoGen | https://github.com/Demik-777/autogen | [Project tools](../reference/project-tools.md#autogen--архитектура-нескольких-агентов) |

See [chat bootstrap](../reference/chat-bootstrap.md) for persistent assistant instructions. Source availability does not imply a running service or connected API.
