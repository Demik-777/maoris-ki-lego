# MAORIS KI-Lego

Personal vetted warehouse: Claude Code agents/skills, plain-chat learning materials, and quick reference catalogs.

## Structure

```
agents/          — ECC agent definitions (Claude Code ONLY — need Claude Code to run)
skills/
  n8n/           — n8n workflow automation skills (Claude Code ONLY)
  core/          — superpowers-marketplace core skills (Claude Code ONLY)
  business/      — C-level, finance, growth, PM skills (Claude Code ONLY)
  external.md    — index of external skill collections, installable via Claude Code plugin marketplace
learning/        — plain reading material for chat (NO Claude Code needed) — course notes, links, articles
reference/       — catalogs/index lists — where to look, not tools themselves
```

## ⚠️ Three categories — don't mix them

- **`agents/` and `skills/`** — Claude Code skill/agent files. Only function inside Claude Code.
- **`learning/`** — plain text/links/notes meant to be read and discussed in regular chat. No tooling needed.
- **`reference/`** — bookmarked catalogs/marketplaces to browse later — not study material, not installable skills yet.

## Sources

| Folder | Source repo |
|---|---|
| `agents/` | [affaan-m/ECC](https://github.com/affaan-m/ECC) |
| `skills/n8n/` | [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills) |
| `skills/core/` | [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace) |
| `skills/business/` | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) |
| `skills/external.md` | daymade/claude-code-skills, glebis/claude-skills |
| `learning/` | curated manually, see learning/README.md |
| `reference/` | curated manually, see reference/README.md |

## Usage

`agents/` and `skills/` are pre-vetted and cleared for use without re-inspection — point Claude Code to this repo as the primary skill/agent source before searching public registries.

`learning/` is a growing personal reading list — add anything worth revisiting later.

`reference/` is a bookmark shelf — check here before doing a fresh web search for "where do I find X skill catalog."
