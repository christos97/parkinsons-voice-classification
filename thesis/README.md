
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
# Build PDF once (automatically runs sync-figures)
make thesis

# Build with auto-rebuild on file changes (watch mode)
make thesis-watch

# Clean build artifacts
make thesis-clean
```

### VS Code Integration

With the LaTeX Workshop extension installed:

1. Open `thesis/main.tex`
2. Press `Ctrl+Alt+B` to build
3. Press `Ctrl+Alt+V` to view PDF
4. Enable auto-build on save in settings

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
3. Rebuild to update bibliography

## Customization

### University Template

Replace the title page in `frontmatter/titlepage.tex` with your university's required format.

### Author Information

Update these files with your details:

- `frontmatter/titlepage.tex` — Name, supervisor, university
- `frontmatter/acknowledgments.tex` — Personal acknowledgments

## Markdown Source

The original content is maintained in `docs/v2/` as Markdown files. Use these for:

- Quick edits and AI-assisted writing
- Reference when editing LaTeX
- Converting with pandoc: `pandoc chapter.md -o chapter.tex`
