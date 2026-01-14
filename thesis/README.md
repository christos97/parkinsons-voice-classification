# Thesis LaTeX Project

LaTeX source files for the MSc thesis on **Voice-Based Classification of Parkinson's Disease Using Classical Machine Learning**.

**Build tool:** latexmk  
**Source of truth:** This directory contains the authoritative thesis content.

## Quick Start

```bash
make thesis         # Build PDF (auto-syncs figures + latexmk)
make thesis-watch   # Continuous rebuild on changes
make thesis-clean   # Remove all build artifacts
```

## Structure

```
thesis/
├── main.tex                    # Root document
├── frontmatter/
│   ├── titlepage.tex           # Title page
│   ├── abstract.tex            # Abstract
│   └── acknowledgments.tex     # Acknowledgments
├── chapters/
│   ├── 01_introduction.tex
│   ├── 02_literature_review.tex
│   ├── 03_data_description.tex
│   ├── 04_methodology.tex
│   ├── 05_experimental_design.tex
│   ├── 06_results.tex
│   ├── 07_discussion.tex
│   ├── 08_limitations.tex
│   └── 09_conclusion.tex
├── appendices/
│   ├── appendix_a_features.tex
│   └── appendix_b_results.tex
├── references/
│   └── references.bib          # BibTeX bibliography
└── figures/                    # Auto-synced from outputs/plots/
```

## Build Process

1. `make thesis` runs `make sync-figures` automatically
2. `latexmk -pdf` handles all compilation passes
3. Uses `-f` flag to complete even with warnings

## Figure Management

Figures are synced automatically from experiment outputs:

```bash
make sync-figures   # Copy outputs/plots/ → thesis/figures/
```

To add new figures:

1. Generate plot (saves to `outputs/plots/`)
2. Update `FIGURE_MAPPING` in `scripts/sync_figures.py`
3. Run `make thesis` (auto-syncs)

## Citation Style

Uses `natbib` with numerical citations:

```latex
\cite{author2023}          % [1]
\citep{author2023}         % [1] (parenthetical)
\citet{author2023}         % Author et al. [1] (textual)
```

## Prerequisites

```bash
sudo apt install texlive-full latexmk   # Linux
```

## Troubleshooting

**"Bibliography entries: 0"**

```bash
make thesis-clean && make thesis
```

**Missing figures**

```bash
make sync-figures
```

## Source of Truth

> **LaTeX files in `thesis/` are authoritative for thesis content.**

Markdown files in `_legacy_/v2/` are deprecated (read-only archive).

---

See [thesis/AGENTS.md](AGENTS.md) for AI agent-specific editing rules.
