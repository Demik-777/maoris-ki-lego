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

## ⚠️ Needs refresh
`skills/business/` in this repo was copied from alirezarezvani/claude-skills at ~253 files / early version. Source has since grown to 345 skills / 5200+ stars (added: founder-mode C-level personas, AEO marketing skills, enterprise research ops). Re-sync not done yet — flag for a dedicated pass, not a quick copy job.
