---
title: "LaTeX Thesis Folder — Agent Instructions"
project: "Parkinson's Disease Voice Classification Thesis"
last_updated: "2026-02-22"
---

# Thesis Folder Instructions

> **Full thesis writing guidance is consolidated in [.github/skills/latex-thesis/SKILL.md](../.github/skills/latex-thesis/SKILL.md).**

This folder contains the authoritative LaTeX source for the MSc thesis. Markdown files in `_legacy_/v2/` are **DEPRECATED**.

## Quick Rules

- **Build:** `make thesis` (auto-syncs figures + latexmk)
- **Figures:** Never manually copy into `thesis/figures/` — use `scripts/sync_figures.py`
- **Citations:** At least one `\cite{}` required in chapters; use `@misc` not `@software`
- **Stats:** Always mean ± std; no single-point estimates
- **Language:** No "outperforms", "proves", "diagnoses" — use hedging language

For LaTeX patterns, label conventions, figure workflow, bibliography management, result analysis, and the full pre-build checklist, see the [latex-thesis skill](../.github/skills/latex-thesis/SKILL.md).
