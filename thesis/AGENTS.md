---
title: "LaTeX Thesis Editing Guide for AI Agents"
project: "Parkinson's Disease Voice Classification Thesis"
last_updated: "2026-01-14"
agent: thesis-specialist

critical_rules:
  - Figure synchronization is automated.
  - Do NOT manually copy figures into the thesis directory.

figure_sync:
  script: scripts/sync_figures.py
  source_dir: outputs/
  target_dir: thesis/figures/
  mapping_key: FIGURE_MAPPING

procedure_on_new_figures:
  - Update FIGURE_MAPPING in scripts/sync_figures.py
  - Run: make sync-figures

notes:
  - This file defines the authoritative thesis build workflow.
  - Any deviation from this process must update this frontmatter accordingly.

---

# LaTeX Thesis Editing Guide for AI Agents

> **Source of Truth:** LaTeX files in `thesis/` are authoritative.  
> Markdown files in `docs/v2/` are **DEPRECATED** (read-only archive).

---

## 1. Build System

### Build Commands

```bash
make thesis         # Build PDF (includes automatic figure sync)
make thesis-watch   # Continuous rebuild on file changes
make thesis-clean   # Remove build artifacts
```

**Build Process:**

1. `make thesis` automatically runs `make sync-figures` first
2. Figures are synced from `outputs/plots/` → `thesis/figures/`
3. LaTeX compilation happens via `latexmk -pdf`
4. Multiple passes ensure citations and references resolve

**Troubleshooting:**

- "Undefined references" → Normal on first build, run `make thesis` again
- "Citation undefined" → Check BibTeX entry exists in `references/references.bib`
- "File not found" → Run `make sync-figures` or check figure path
- Persistent errors → Try `make thesis-clean` then `make thesis`

---

## 2. Citations and Bibliography

### Citation Rules (CRITICAL)

✅ **Always cite external sources** using BibTeX:

```latex
\cite{little2009suitability}           % Single citation
\cite{tsanas2010accurate,breiman2001random}  % Multiple citations
```

✅ **Required BibTeX entry in `references/references.bib`:**

```bibtex
@article{little2009suitability,
  author = {Little, Max A and McSharry, Patrick E and Roberts, Stephen J},
  title = {Exploiting Nonlinear Recurrence and Fractal Scaling Properties for Voice Disorder Detection},
  journal = {BioMedical Engineering OnLine},
  year = {2009},
  volume = {6},
  number = {1},
  pages = {23},
  doi = {10.1186/1475-925X-6-23}
}
```

❌ **Forbidden:**

- Citing internal outputs (e.g., `outputs/`, `assets/`, `docs/v2/`)
- Using URLs directly in text instead of BibTeX entries
- Citing GitHub repos without proper `@software` entry
- Adding citations without corresponding BibTeX entry

### BibTeX Key Format

**Pattern:** `<firstauthor><year><keyword>`

Examples:

- `little2009suitability` — Paper on voice disorder detection
- `mdvr_kcl_2019` — MDVR-KCL dataset (Zenodo)
- `sklearn2011` — scikit-learn software

### Required Fields by Entry Type

**@article:** author, title, journal, year, volume, pages, doi  
**@inproceedings:** author, title, booktitle, year, pages  
**@book:** author, title, publisher, year, isbn  
**@software:** author, title, year, url  
**@misc:** author, title, year, howpublished, url/doi

---

## 3. Figure Workflow

### Automatic Figure Syncing

**Script:** `scripts/sync_figures.py`  
**Mapping:** Renames experimental plots for thesis use

Example mappings:

```text
outputs/plots/roc_curve_ReadText.pdf → thesis/figures/fig_roc_readtext.pdf
outputs/plots/heatmap_readtext.png → thesis/figures/fig_heatmap_readtext.png
```

**To add new figures:**

1. Generate plot in experiment code → saves to `outputs/plots/`
2. Update `FIGURE_MAPPING` dictionary in `scripts/sync_figures.py`
3. Run `make sync-figures` (or just `make thesis` — it auto-syncs)

### Using Figures in LaTeX

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{fig_roc_readtext.pdf}
    \caption{ROC curves for ReadText task across models}
    \label{fig:roc-readtext}
\end{figure}
```

**Rules:**

- Use `[H]` placement (requires `float` package — already loaded)
- No path prefix needed (graphics path configured in `main.tex`)
- Label format: `\label{fig:descriptive-name}`
- Reference as: `Figure~\ref{fig:roc-readtext}` (non-breaking space `~`)
- Caption style: Brief descriptive sentence

❌ **Never reference figures that don't exist in `thesis/figures/`**

---

## 4. LaTeX Editing Conventions

### Chapter Structure

```latex
\chapter{Methodology}
\label{ch:methodology}

\section{Feature Extraction}
\label{sec:feature-extraction}

\subsection{Prosodic Features}
% content
```

**Label prefixes:**

- `ch:` — Chapters
- `sec:` — Sections
- `fig:` — Figures
- `tab:` — Tables
- `eq:` — Equations

**Cross-references:**

```latex
Chapter~\ref{ch:methodology}
Section~\ref{sec:feature-extraction}
Figure~\ref{fig:roc-readtext}
Table~\ref{tab:dataset-summary}
```

### Tables

Use `booktabs` package (already loaded):

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

**Rules:**

- Caption goes **above** table
- Use `\toprule`, `\midrule`, `\bottomrule` (no `\hline`)
- Align numbers right: `r` (or `S` from `siunitx` for decimals)
- `[H]` placement for fixed positioning

### Statistical Results

**Always report mean ± std:**

```latex
Random Forest achieved $0.857 \pm 0.171$ ROC-AUC (ReadText task).
```

❌ Single-point estimates forbidden without variance

### Math and Variables

```latex
% Variables
The fundamental frequency \( f_0 \) was extracted from each recording.

% Equations
\begin{equation}
    \text{Jitter}_{\text{local}} = \frac{1}{N-1} \sum_{i=1}^{N-1} \frac{|T_i - T_{i+1}|}{T_i}
    \label{eq:jitter-local}
\end{equation}
```

---

## 5. Research Integrity Constraints

### From Root AGENTS.md

These rules apply to **all thesis content**:

❌ **Forbidden Language:**

- "X outperforms Y" → Use "X showed higher performance than Y"
- "This proves..." → Use "Results suggest..."
- "Clearly superior" → Use "Observed trend toward..."
- Any diagnostic/clinical claims → **This is research only**

✅ **Mandatory Caveats:**

- Dataset B: "Subject identifiers unavailable; results may be optimistic due to potential within-subject sample correlation"
- Small sample: "Limited sample size (n=37 for Dataset A) requires cautious interpretation"
- Cross-dataset comparisons: "Performance differences attributed to multiple factors including sample size, feature dimensionality, and cross-validation strategy"

✅ **Model Constraints:**

- Only classical ML: Logistic Regression, SVM (RBF), Random Forest
- No deep learning, no production deployment claims

---

## 6. File Organization

```text
thesis/
├── main.tex                  # Main document (do not edit structure)
├── chapters/                 # Edit chapter content here
│   ├── 01_introduction.tex
│   ├── 02_literature_review.tex
│   ├── ...
│   └── 09_conclusion.tex
├── appendices/
│   ├── appendix_a_features.tex
│   └── appendix_b_results.tex
├── frontmatter/
│   ├── abstract.tex
│   ├── acknowledgments.tex
│   └── titlepage.tex
├── references/
│   └── references.bib       # All citations must be here
└── figures/                 # Auto-synced (do not edit manually)
```

**What to edit:**

- Chapter files (`.tex` in `chapters/`)
- Appendices (`.tex` in `appendices/`)
- Bibliography (`references/references.bib`)

**Do not edit:**

- `main.tex` (unless adding packages/configuration)
- Files in `figures/` (managed by sync script)
- Build artifacts (`.aux`, `.bbl`, `.log`, etc.)

---

## 7. Quick Checklist for Agents

Before completing any LaTeX editing task:

- [ ] All external claims have `\cite{}` commands
- [ ] All citations have BibTeX entries in `references/references.bib`
- [ ] All figures referenced exist in `thesis/figures/`
- [ ] All labels are unique and follow naming convention
- [ ] Statistical results reported as mean ± std
- [ ] No forbidden language (see Section 5)
- [ ] Cross-references use `~` (non-breaking space)
- [ ] Tables use `booktabs` formatting
- [ ] Build succeeds: `make thesis` completes without errors

---

## End of Instructions
