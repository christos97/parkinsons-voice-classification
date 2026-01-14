
# Thesis LaTeX Project

This folder contains the LaTeX source files for the MSc thesis on **Voice-Based Classification of Parkinson's Disease Using Classical Machine Learning**.

## Structure

```text
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
├── figures/                    # Place figures here
└── .gitignore                  # LaTeX build artifacts
```

## Building the Thesis

### Prerequisites

Install a LaTeX distribution:

- **Linux:** `sudo apt install texlive-full latexmk`

### Build Commands

```bash
# Build PDF (automatic figure sync + latexmk compilation)
make thesis

# Build with auto-rebuild on file changes (watch mode)
make thesis-watch

# Clean all build artifacts (aux, bbl, log, pdf, etc.)
make thesis-clean
```

**Build Process:**

1. `make thesis` automatically runs `make sync-figures` first
2. `latexmk -pdf` handles all compilation passes:
   - Runs pdflatex → bibtex → pdflatex (as many times as needed)
   - Automatically resolves cross-references and citations
3. Uses `-f` flag to complete even with non-fatal warnings

**Why latexmk instead of manual pdflatex/bibtex?**

- Automatically determines correct number of passes
- Handles stale aux files gracefully
- More reliable than manual compilation sequences

### VS Code Integration

With the LaTeX Workshop extension installed:

1. Open `thesis/main.tex`
2. Press `Ctrl+Alt+B` to build
3. Press `Ctrl+Alt+V` to view PDF
4. Enable auto-build on save in settings

### Citation Styles (natbib)

This thesis uses `natbib` with numerical citations:

```latex
\cite{author2023}          % [1]
\citep{author2023}         % [1] (parenthetical)
\citet{author2023}         % Author et al. [1] (textual)
\citep{auth1,auth2}        % [1, 2]
\citep[see][]{author2023}  % [see 1]
```

## Figure Management

Figures are managed centrally and synced from the experiment outputs.

### Workflow

1. **Generate Plots**: Run experiments to create plots in the `outputs/` directory.

   ```bash
   make experiments   # or make pipeline
   ```

2. **Sync Figures**: Copy files to `thesis/figures/` using the mapping script.

   ```bash
   make sync-figures
   ```

   *(Note: This runs automatically when you execute `make thesis`)*

### Adding New Figures

To include a new figure in the thesis:

1. Open `scripts/sync_figures.py`.
2. Update the `FIGURE_MAPPING` dictionary to map the source file to its destination name:

   ```python
   # scripts/sync_figures.py
   FIGURE_MAPPING = {
       "source_filename_in_outputs.png": "fig_descriptive_name.png",
       ...
   }
   ```

3. Run `make sync-figures`.
4. Use the figure in LaTeX using the destination filename:

   ```latex
   \begin{figure}[H]
   \centering
   \includegraphics[width=0.8\textwidth]{fig_descriptive_name.png}
   \caption{Figure caption}
   \label{fig:label}
   \end{figure}
   ```

## Adding Citations

1. Add entries to `references/references.bib`
2. Cite in text: `\cite{little2009suitability}`
3. Rebuild: `make thesis`

### Bibliography Troubleshooting

If you see "Bibliography entries: 0" after building:

1. **Most common fix**: Stale aux files from previous build
   ```bash
   make thesis-clean && make thesis
   ```

2. **Check for citations**: Ensure at least one `\cite{}` command exists in chapter files
   - Using only `\nocite{*}` in `main.tex` is insufficient
   - BibTeX requires actual citations to process entries

3. **Verify entry types**: Use supported BibTeX types
   - ✅ `@article`, `@book`, `@inproceedings`, `@misc`
   - ❌ `@software` (not supported by plainnat.bst)
   - Fix: Change `@software` to `@misc` with `howpublished = {Software}`

4. **Check document structure**: Bibliography must come AFTER appendices in `main.tex`

5. **Manual debugging** (only if latexmk fails):
   ```bash
   cd thesis
   pdflatex -interaction=nonstopmode main.tex
   bibtex main  # Check for errors here
   pdflatex -interaction=nonstopmode main.tex
   pdflatex -interaction=nonstopmode main.tex
   ```

6. **Verify .bbl file**: After build, should contain bibliography entries
   ```bash
   grep -c 'bibitem\[' thesis/main.bbl  # Should be > 0
   ```

## Customization

### University Template

Replace the title page in `frontmatter/titlepage.tex` with your university's required format.

### Author Information

Update these files with your details:

- `frontmatter/titlepage.tex` — Name, supervisor, university
- `frontmatter/acknowledgments.tex` — Personal acknowledgments

## Source of Truth

> **LaTeX files in `thesis/` are the authoritative source for all thesis content.**

⚠️ **DEPRECATED:** Markdown files in `docs/v2/` are a read-only archive.
- Do NOT edit markdown files for thesis content
- All thesis changes must be made in LaTeX files under `thesis/`
- See `docs/v2/DEPRECATED.md` for details
