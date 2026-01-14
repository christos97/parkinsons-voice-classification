---
title: "LaTeX Thesis Editing Guide for AI Agents"
project: "Parkinson's Disease Voice Classification Thesis"
last_updated: "2026-01-14"
agent: thesis-specialist

critical_rules:
  - "Figure synchronization is automated via make sync-figures"
  - "Do NOT manually copy figures into thesis/figures/"
  - "At least one cite{} command required for bibliography to build"
  - "Use @misc instead of @software for BibTeX entries"

figure_sync:
  script: "scripts/sync_figures.py"
  source_dir: "outputs/plots/"
  target_dir: "thesis/figures/"
  mapping_key: "FIGURE_MAPPING"

procedure_on_new_figures:
  - "Update FIGURE_MAPPING in scripts/sync_figures.py"
  - "Run: make sync-figures"

build_commands:
  build: "make thesis"
  watch: "make thesis-watch"
  clean: "make thesis-clean"

label_prefixes:
  chapter: "ch:"
  section: "sec:"
  figure: "fig:"
  table: "tab:"
  equation: "eq:"

bibtex_types_allowed: ["@article", "@book", "@inproceedings", "@misc"]
bibtex_types_forbidden: ["@software"]
---

# LaTeX Thesis Editing Guide for AI Agents

> **Source of Truth:** LaTeX files in `thesis/` are authoritative.  
> Markdown files in `_legacy_/v2/` are **DEPRECATED** (use only as a read-only archive).

---

## 1. Build System

```bash
make thesis         # Build PDF (auto figure sync + latexmk)
make thesis-watch   # Continuous rebuild on changes
make thesis-clean   # Remove all artifacts
```

**Build Process:**

1. `make thesis` runs `make sync-figures` first
2. `latexmk -pdf` handles all passes automatically
3. Uses `-f` flag to complete even with warnings

**Troubleshooting:**

- "Bibliography entries: 0" → `make thesis-clean && make thesis`
- "Citation undefined" → Check entry exists in `references/references.bib`
- "File not found" → Run `make sync-figures`

---

## 2. Citations (CRITICAL)

### Requirements

⚠️ The bibliography requires **at least one `\cite{}` command** in chapters.
Using only `\nocite{*}` in main.tex is insufficient.

### Citation Commands

```latex
\cite{little2009suitability}           % [1]
\citep{author2023}                     % [1] (parenthetical)
\citet{author2023}                     % Author et al. [1] (textual)
\cite{auth1,auth2}                     % [1, 2]
```

### BibTeX Entry Types

| Allowed | Forbidden |
|---------|-----------|
| `@article` | `@software` |
| `@book` | |
| `@inproceedings` | |
| `@misc` | |

**For software citations, use `@misc`:**

```bibtex
@misc{parselmouth2018,
  title = {Parselmouth: {Praat} in {Python}},
  author = {Jadoul, Yannick and Thompson, Bill and de Boer, Bart},
  year = {2018},
  howpublished = {Software},
  url = {https://github.com/YannickJadoul/Parselmouth}
}
```

### Forbidden

❌ Citing internal artifacts (`outputs/`, `assets/`, `_legacy_/`)  
❌ Using URLs directly in text instead of BibTeX  
❌ Adding citations without BibTeX entry

---

## 3. Figure Workflow

### Automatic Syncing

**Script:** `scripts/sync_figures.py`

Figures sync automatically when building:

```
outputs/plots/heatmap_readtext.png → thesis/figures/fig_heatmap_readtext.png
```

### Adding New Figures

1. Generate plot → saves to `outputs/plots/`
2. Update `FIGURE_MAPPING` in `scripts/sync_figures.py`
3. Run `make thesis` (auto-syncs)

### Using Figures

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{fig_heatmap_readtext.png}
    \caption{Feature correlation heatmap for ReadText task}
    \label{fig:heatmap-readtext}
\end{figure}
```

**Rules:**

- Use `[H]` placement (float package loaded)
- No path prefix needed (graphics path configured)
- Label format: `\label{fig:descriptive-name}`
- Reference: `Figure~\ref{fig:heatmap-readtext}` (non-breaking space)

❌ Never reference figures that don't exist in `thesis/figures/`

---

## 4. Document Structure

### Label Prefixes

| Type | Prefix | Example |
|------|--------|---------|
| Chapter | `ch:` | `\label{ch:methodology}` |
| Section | `sec:` | `\label{sec:feature-extraction}` |
| Figure | `fig:` | `\label{fig:roc-readtext}` |
| Table | `tab:` | `\label{tab:dataset-summary}` |
| Equation | `eq:` | `\label{eq:jitter-local}` |

### Cross-References

```latex
Chapter~\ref{ch:methodology}
Section~\ref{sec:feature-extraction}
Figure~\ref{fig:roc-readtext}
Table~\ref{tab:dataset-summary}
```

### Tables (booktabs)

```latex
\begin{table}[H]
    \centering
    \caption{Dataset A sample distribution}
    \label{tab:dataset-distribution}
    \begin{tabular}{lrr}
        \toprule
        Task & HC & PD \\
        \midrule
        ReadText & 21 & 16 \\
        SpontaneousDialogue & 21 & 15 \\
        \bottomrule
    \end{tabular}
\end{table}
```

Caption goes **above** table. Use `\toprule`, `\midrule`, `\bottomrule`.

---

## 5. Research Integrity Constraints

From root AGENTS.md — apply to all thesis content:

### Forbidden Language

❌ "X outperforms Y"  
❌ "This proves..."  
❌ "Clearly superior"  
❌ Any diagnostic/clinical claims

### Required Language

✅ "Results suggest..."  
✅ "Observed under identical classifiers..."  
✅ "Should be interpreted cautiously..."

### Mandatory Caveats

- Dataset B: "Subject identifiers unavailable; results may be optimistic"
- Small sample: "Limited sample size (n=37) requires cautious interpretation"

### Statistical Results

Always report **mean ± std**:

```latex
Random Forest achieved $0.857 \pm 0.171$ ROC-AUC (ReadText task).
```

❌ Single-point estimates forbidden

---

## 6. File Organization

### What to Edit

- Chapter files (`.tex` in `chapters/`)
- Appendices (`.tex` in `appendices/`)
- Bibliography (`references/references.bib`)

### Do NOT Edit

- `main.tex` (unless adding packages)
- Files in `figures/` (managed by sync script)
- Build artifacts (`.aux`, `.bbl`, `.log`)

---

## 7. Pre-Commit Checklist

Before completing any LaTeX editing:

- [ ] At least one `\cite{}` in chapters (not just `\nocite{*}`)
- [ ] All citations have BibTeX entries
- [ ] BibTeX uses allowed types (no `@software`)
- [ ] All figures exist in `thesis/figures/`
- [ ] Labels are unique and follow conventions
- [ ] Statistical results: mean ± std
- [ ] No forbidden language
- [ ] Build succeeds: `make thesis`
- [ ] Bibliography count > 0

---

## End of Instructions
