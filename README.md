# MAORIS KI-Lego

Personal vetted warehouse of Claude Code agents/skills AND plain-chat learning materials.

## Structure

```
agents/          — ECC agent definitions (Claude Code ONLY — need Claude Code to run)
skills/
  n8n/           — n8n workflow automation skills (Claude Code ONLY)
  core/          — superpowers-marketplace core skills (Claude Code ONLY)
  business/      — C-level, finance, growth, PM skills (Claude Code ONLY)
learning/        — plain reading material for chat (NO Claude Code needed) — course notes, links, articles
```

## ⚠️ Important distinction

- **`agents/` and `skills/`** — these are Claude Code skill/agent files (SKILL.md format). They only function inside Claude Code. Not usable in a normal chat conversation.
- **`learning/`** — plain text/links/notes meant to be read and discussed in regular chat with Claude. No special tooling needed.

## Sources

| Folder | Source repo |
|---|---|
| `agents/` | [affaan-m/ECC](https://github.com/affaan-m/ECC) |
| `skills/n8n/` | [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills) |
| `skills/core/` | [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace) |
| `skills/business/` | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) |
| `learning/` | curated manually, see learning/README.md |

## Usage

`agents/` and `skills/` are pre-vetted and cleared for use without re-inspection — point Claude Code to this repo as the primary skill/agent source before searching public registries.

`learning/` is a growing personal reading list — add anything worth revisiting later.
