# ⚠️ DEPRECATED — Read-Only Archive

> **Date:** 2026-01-14

The markdown files in this directory (`docs/v2/`) are **deprecated** and retained as a read-only archive.

## Source of Truth

**The LaTeX thesis under [`thesis/`](../../thesis/) is the authoritative source for all thesis content.**

To compile the thesis:

```bash
make thesis        # Build PDF
make thesis-watch  # Watch mode with auto-rebuild
make thesis-clean  # Remove build artifacts
```

## Migration Status

All content from these markdown files has been migrated to LaTeX:

| Markdown File | LaTeX Equivalent |
|---------------|------------------|
| `CHAPTER_1_INTRODUCTION.md` | `thesis/chapters/01_introduction.tex` |
| `CHAPTER_2_LITERATURE_REVIEW.md` | `thesis/chapters/02_literature_review.tex` |
| `CHAPTER_3_DATA_DESCRIPTION.md` | `thesis/chapters/03_data_description.tex` |
| `CHAPTER_4_METHODOLOGY.md` | `thesis/chapters/04_methodology.tex` |
| `CHAPTER_5_EXPERIMENTAL_DESIGN.md` | `thesis/chapters/05_experimental_design.tex` |
| `CHAPTER_6_RESULTS.md` | `thesis/chapters/06_results.tex` |
| `CHAPTER_7_DISCUSSION.md` | `thesis/chapters/07_discussion.tex` |
| `CHAPTER_8_LIMITATIONS.md` | `thesis/chapters/08_limitations.tex` |
| `CHAPTER_9_CONCLUSION.md` | `thesis/chapters/09_conclusion.tex` |
| `APPENDIX_A_FEATURE_IMPORTANCE.md` | `thesis/appendices/appendix_a_features.tex` |
| `APPENDIX_B_DETAILED_RESULTS.md` | `thesis/appendices/appendix_b_results.tex` |

## Policy

- ❌ Do **not** edit markdown files for thesis content updates
- ❌ Do **not** cite these files as external references
- ✅ Edit only LaTeX files under `thesis/` for thesis changes
- ✅ These files may be retained for historical reference

## Retained Documentation

The following documentation files remain **active** (not deprecated):

- [`docs/DATASET_MDVR_KCL.md`](../DATASET_MDVR_KCL.md) — Dataset A data card
- [`docs/DATASET_PD_SPEECH_FEATURES.md`](../DATASET_PD_SPEECH_FEATURES.md) — Dataset B data card
- [`docs/WEB_APP_ARCHITECTURE.md`](../WEB_APP_ARCHITECTURE.md) — Demo app architecture
