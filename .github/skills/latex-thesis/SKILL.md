---
name: latex-thesis
description: Write, edit, and build the LaTeX MSc thesis .tex files on Parkinson's Disease voice classification. Use when working with thesis chapters, analyzing experiment results for discussion, managing BibTeX bibliography, syncing figures, or building the thesis PDF. Keywords include LaTeX, thesis writing, bibliography management, figure syncing, research integrity, statistical reporting, interpretation guidelines, .tex files.
---

# LaTeX Thesis Writing

Write and maintain the MSc thesis (`.tex` files) on Parkinson's Disease voice classification using classical machine learning. This skill covers LaTeX editing, result analysis, bibliography management, figure syncing, and research integrity.

## Research Context

This thesis investigates binary classification of Parkinson's Disease (PD) vs Healthy Controls (HC) using voice data:

- **Dataset A (MDVR-KCL)**: Raw audio → feature extraction → ML (n=37 subjects for ReadText, n=36 for SpontaneousDialogue)
- **Dataset B (PD Speech Features)**: Pre-extracted features → ML (subject IDs unavailable)
- **Models**: Logistic Regression, SVM (RBF), Random Forest — no deep learning
- **Features**: 47 baseline (21 prosodic + 26 spectral), 78 extended
- **Evaluation**: Accuracy, Precision, Recall, F1, ROC-AUC — all reported as mean ± std

> **Source of truth:** LaTeX files in `thesis/` are authoritative. Markdown files in `_legacy_/v2/` are **DEPRECATED** (read-only archive).

## Build System

```bash
make thesis         # Build PDF (auto figure sync + latexmk)
make thesis-watch   # Continuous rebuild on changes
make thesis-clean   # Remove all build artifacts
make sync-figures   # Sync figures only (from outputs/plots/ → thesis/figures/)
```

Build process: `make thesis` runs `sync-figures` first, then `latexmk -pdf` with `-f` flag.

### Troubleshooting

| Symptom | Fix |
|---------|-----|
| "Bibliography entries: 0" | `make thesis-clean && make thesis` |
| "Citation undefined" | Check entry exists in `references/references.bib` |
| "File not found" | Run `make sync-figures` |

## File Locations

| Resource | Path |
|----------|------|
| Main thesis | `thesis/main.tex` |
| Chapters | `thesis/chapters/*.tex` |
| Appendices | `thesis/appendices/*.tex` |
| Bibliography | `thesis/references/references.bib` |
| Figures (source) | `outputs/plots/` |
| Figures (thesis) | `thesis/figures/` |
| Figure sync script | `scripts/sync_figures.py` |
| Baseline results | `outputs/results/baseline/summary.csv` |
| Weighted results | `outputs/results/weighted/summary.csv` |

### What to Edit

- Chapter files in `thesis/chapters/`
- Appendices in `thesis/appendices/`
- Bibliography at `thesis/references/references.bib`

### Do NOT Edit

- `thesis/main.tex` (unless adding packages)
- Files in `thesis/figures/` (managed by sync script)
- Build artifacts (`.aux`, `.bbl`, `.log`, `.fls`, `.fdb_latexmk`)

## Research Integrity

### Statistical Reporting

Always report **mean ± std** across cross-validation folds. Single-point estimates are forbidden in tables, figures, and text.

```latex
% CORRECT
The Random Forest classifier achieved an accuracy of $0.82 \pm 0.05$ and F1-score of $0.79 \pm 0.06$.

% INCORRECT — single point estimate
The Random Forest classifier achieved 82\% accuracy.
```

### Forbidden Language

| Forbidden | Use Instead |
|-----------|-------------|
| "X outperforms Y" | "X achieved higher scores than Y" |
| "This proves..." | "These results suggest..." |
| "Clearly superior" | "Showed improvement" |
| "This diagnoses..." | "This classifies..." |
| "Significant" (without statistical test) | "Notable" or "Observed" |

### Required Caveats

Include these when discussing results:

```latex
% Dataset A (small sample) — ALWAYS include
These results should be interpreted cautiously given the small sample size ($n=37$).

% Dataset B (unknown subjects) — ALWAYS include
Results may be optimistic due to unknown subject overlap across samples.

% Comparing conditions
Differences observed under identical classifier configurations.
```

### Interpretation Guidelines

| Scenario | Guidance |
|----------|----------|
| ROC-AUC < 0.5 | Document as model instability, not failure |
| Overlapping CIs | Use "suggests" / "trend toward" |
| Dataset B results | Caveat about potential subject leakage |
| Cross-dataset | Never attribute differences to a single factor |

## Analyzing Results for Thesis

Follow this process when translating experiment outputs into thesis discussion:

1. Read the summary CSV files:
   - `outputs/results/baseline/summary.csv` — main results
   - `outputs/results/weighted/summary.csv` — class-weighted results
2. Compare across dimensions:
   - Tasks: ReadText vs SpontaneousDialogue
   - Models: Logistic Regression vs SVM vs Random Forest
   - Feature sets: baseline (47) vs extended (78)
3. Report all metrics as mean ± std
4. Frame findings with hedging language ("suggests", "observed")
5. Include mandatory caveats for each dataset

## Citations

### Citation Commands

```latex
\cite{little2009suitability}           % [1]
\citep{author2023}                     % [1] (parenthetical)
\citet{author2023}                     % Author et al. [1] (textual)
\cite{auth1,auth2}                     % [1, 2]
```

### Critical Rule

The bibliography requires **at least one `\cite{}` command** in chapters. Using only `\nocite{*}` in `main.tex` is insufficient.

### BibTeX Entry Types

Allowed: `@article`, `@book`, `@inproceedings`, `@misc`

**Never use `@software`** — use `@misc` with `howpublished`:

```bibtex
@misc{parselmouth2018,
  title        = {Parselmouth: {Praat} in {Python}},
  author       = {Jadoul, Yannick and Thompson, Bill and de Boer, Bart},
  year         = {2018},
  howpublished = {Software},
  url          = {https://github.com/YannickJadoul/Parselmouth}
}
```

### Forbidden

- Citing internal artifacts (`outputs/`, `assets/`, `_legacy_/`)
- Using URLs directly in text instead of BibTeX
- Adding `\cite{}` without a matching BibTeX entry

### Adding a New Bibliography Entry

1. Edit `thesis/references/references.bib`
2. Use a correct entry type (`@article`, `@book`, `@inproceedings`, or `@misc`)
3. Include DOI when available
4. Cite in chapter: `\cite{key}` or `\citep{key}`
5. Verify: build succeeds and bibliography count > 0

## Figure Workflow

Figures are automatically synced from `outputs/plots/` to `thesis/figures/` via `scripts/sync_figures.py`. Never manually copy figures.

### Adding a New Figure

1. Generate the plot → saves to `outputs/plots/`
2. Update `FIGURE_MAPPING` in `scripts/sync_figures.py`:

   ```python
   FIGURE_MAPPING = {
       "source_name.png": "fig_destination.png",
   }
   ```

3. Run `make thesis` (auto-syncs) or `make sync-figures`
4. Reference in LaTeX:

   ```latex
   \begin{figure}[H]
       \centering
       \includegraphics[width=0.8\textwidth]{fig_destination.png}
       \caption{Descriptive caption explaining the figure content.}
       \label{fig:descriptive-name}
   \end{figure}
   ```

### Figure Rules

- Use `[H]` placement (float package loaded)
- No path prefix needed (graphics path configured in `main.tex`)
- Never reference figures that don't exist in `thesis/figures/`

## LaTeX Patterns

### Label Conventions

| Type | Prefix | Example |
|------|--------|---------|
| Chapter | `ch:` | `\label{ch:methodology}` |
| Section | `sec:` | `\label{sec:feature-extraction}` |
| Figure | `fig:` | `\label{fig:roc-readtext}` |
| Table | `tab:` | `\label{tab:dataset-summary}` |
| Equation | `eq:` | `\label{eq:jitter-local}` |

### Cross-References

Always use non-breaking space before `\ref`:

```latex
% CORRECT
Chapter~\ref{ch:methodology}
Section~\ref{sec:feature-extraction}
Figure~\ref{fig:roc-readtext}
Table~\ref{tab:dataset-summary}
Equation~\ref{eq:jitter-local}

% INCORRECT — regular space
Figure \ref{fig:name}
```

### Table (booktabs)

Caption goes **above** table. Never use `\hline`.

```latex
\begin{table}[H]
    \centering
    \caption{Dataset A sample distribution}
    \label{tab:dataset-distribution}
    \begin{tabular}{@{}lrr@{}}
        \toprule
        Task & HC & PD \\
        \midrule
        ReadText & 21 & 16 \\
        SpontaneousDialogue & 21 & 15 \\
        \bottomrule
    \end{tabular}
\end{table}
```

### Math

```latex
% Inline
The jitter value $J$ is calculated as...

% Display equation
\begin{equation}
    J_{\text{local}} = \frac{1}{N-1} \sum_{i=1}^{N-1} |T_i - T_{i+1}|
    \label{eq:jitter-local}
\end{equation}
```

### Code Listings

```latex
\begin{lstlisting}[language=Python, caption={Feature extraction example}]
features = extract_prosodic_features(audio_signal)
\end{lstlisting}
```

### Lists

```latex
\begin{itemize}
    \item First point
    \item Second point
\end{itemize}

\begin{enumerate}
    \item First step
    \item Second step
\end{enumerate}
```

## Pre-Build Checklist

Before completing any thesis editing task, verify:

- [ ] At least one `\cite{}` in chapters (not just `\nocite{*}`)
- [ ] All `\cite{}` commands have matching BibTeX entries
- [ ] No `@software` entries (use `@misc`)
- [ ] All referenced figures exist in `thesis/figures/`
- [ ] Labels are unique and follow prefix conventions
- [ ] Statistical results use mean ± std format
- [ ] No forbidden language in text
- [ ] Required caveats included for each dataset discussed
- [ ] Build succeeds: `make thesis`
- [ ] Bibliography entry count > 0