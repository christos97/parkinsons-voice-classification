---
name: latex-thesis
description: Build LaTeX thesis, sync figures from outputs/plots/, analyze experiment results, manage BibTeX bibliography. Use when working with thesis chapters, interpreting ML results, adding citations, or updating figures.
---

# LaTeX Thesis Writing Skill

This skill helps write and maintain the MSc thesis on Parkinson's Disease voice classification.

## When to Use This Skill

- Editing thesis chapters in `thesis/chapters/*.tex`
- Syncing figures from experiment outputs to thesis
- Analyzing results in `outputs/results/` for thesis discussion
- Adding or updating bibliography entries
- Building the thesis PDF

## Quick Reference

| Command | Purpose |
|---------|---------|
| `make thesis` | Build PDF (auto-syncs figures) |
| `make thesis-watch` | Continuous rebuild on changes |
| `make thesis-clean` | Remove build artifacts |
| `make sync-figures` | Sync figures only |

## Workflow: Adding a New Figure

1. **Generate the plot** → saves to `outputs/plots/`
2. **Update figure mapping** in `scripts/sync_figures.py`:

   ```python
   FIGURE_MAPPING = {
       "source_name.png": "fig_destination.png",
       # Add your new mapping here
   }
   ```

3. **Run sync**: `make thesis` (auto-syncs) or `make sync-figures`
4. **Reference in LaTeX**:

   ```latex
   \begin{figure}[H]
       \centering
       \includegraphics[width=0.8\textwidth]{fig_destination.png}
       \caption{Your caption here}
       \label{fig:descriptive-name}
   \end{figure}
   ```

## Workflow: Analyzing Results for Thesis

1. **Read summary CSV**:
   - `outputs/results/baseline/summary.csv` — Main results
   - `outputs/results/weighted/summary.csv` — Class-weighted results

2. **Key metrics to report** (always mean ± std):
   - Accuracy, Precision, Recall, F1-Score, ROC-AUC

3. **Interpret with required caveats**:
   - Dataset A: Small sample (n=37 ReadText, n=36 Spontaneous)
   - Dataset B: Subject IDs unavailable (potential leakage)
   - Use "suggests", "observed", not "proves", "outperforms"

## Workflow: Adding Bibliography Entry

1. **Edit** `thesis/references/references.bib`
2. **Use correct entry type**:

   ```bibtex
   % Journal article
   @article{key2024,
     author  = {Last, First and Other, Author},
     title   = {Title Here},
     journal = {Journal Name},
     year    = {2024},
     volume  = {1},
     pages   = {1--10},
     doi     = {10.xxxx/xxxxx}
   }
   
   % Software/Dataset (use @misc, NOT @software)
   @misc{software2024,
     author       = {Developer Name},
     title        = {Software Name},
     year         = {2024},
     howpublished = {Software},
     url          = {https://example.com}
   }
   ```

3. **Cite in chapter**: `\cite{key2024}` or `\citep{key2024}`
4. **Verify**: At least one `\cite{}` required for bibliography to build

## LaTeX Patterns

### Table (booktabs style)

```latex
\begin{table}[H]
    \centering
    \caption{Caption above table}
    \label{tab:my-table}
    \begin{tabular}{@{}lcc@{}}
        \toprule
        Model & Accuracy & F1 \\
        \midrule
        Random Forest & 0.82 ± 0.05 & 0.79 ± 0.06 \\
        \bottomrule
    \end{tabular}
\end{table}
```

### Cross-references

```latex
Figure~\ref{fig:name}    % Non-breaking space before \ref
Table~\ref{tab:name}
Chapter~\ref{ch:name}
Section~\ref{sec:name}
```

## Label Conventions

| Type | Prefix | Example |
|------|--------|---------|
| Chapter | `ch:` | `\label{ch:methodology}` |
| Section | `sec:` | `\label{sec:feature-extraction}` |
| Figure | `fig:` | `\label{fig:roc-readtext}` |
| Table | `tab:` | `\label{tab:dataset-summary}` |
| Equation | `eq:` | `\label{eq:jitter-formula}` |

## Forbidden vs Required Language

❌ **Never write:**

- "X outperforms Y"
- "This proves..."
- "Clearly superior"
- "This diagnoses..."

✅ **Always write:**

- "Results suggest..."
- "Observed under identical conditions..."
- "Should be interpreted cautiously..."
- "The trend toward..."

## Pre-Build Checklist

- [ ] At least one `\cite{}` in chapters
- [ ] All citations have BibTeX entries
- [ ] No `@software` entries (use `@misc`)
- [ ] All referenced figures exist
- [ ] Labels follow conventions
- [ ] Statistical results: mean ± std
- [ ] No forbidden language
- [ ] Run `make thesis` successfully

## File Locations

| Resource | Path |
|----------|------|
| Main thesis | `thesis/main.tex` |
| Chapters | `thesis/chapters/*.tex` |
| Bibliography | `thesis/references/references.bib` |
| Figures (source) | `outputs/plots/` |
| Figures (thesis) | `thesis/figures/` |
| Results | `outputs/results/` |
| Figure sync script | `scripts/sync_figures.py` |
| Full constraints | `thesis/AGENTS.md` |
