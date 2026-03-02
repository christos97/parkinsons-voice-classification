#!/usr/bin/env python3
"""Generate MSc Thesis Defense PowerPoint Presentation.

Creates a 26-slide + 5 backup slide presentation for the thesis defense
on "Voice-Based Classification of Parkinson's Disease Using Classical ML".

Usage:
    poetry run python scripts/generate_defense_presentation.py
"""

from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
FIGURES = ROOT / "thesis" / "figures"
OUTPUT_DIR = ROOT / "outputs"
PPTX_OUT = OUTPUT_DIR / "thesis_defense_presentation.pptx"
THESIS_PREAMBLE = ROOT / "thesis" / "Preamble.tex"

# Slide dimensions (16:9 widescreen)
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# ---------------------------------------------------------------------------
# Color Palette (NTUA-inspired academic blue/gray)
# ---------------------------------------------------------------------------
CLR_DARK_BLUE = RGBColor(0x00, 0x2B, 0x5C)  # Dark navy
CLR_BLUE = RGBColor(0x00, 0x56, 0xA0)  # Primary blue
CLR_LIGHT_BLUE = RGBColor(0xD6, 0xE8, 0xF7)  # Light blue background
CLR_ACCENT = RGBColor(0xE8, 0x6C, 0x00)  # Orange accent
CLR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CLR_BLACK = RGBColor(0x1A, 0x1A, 0x1A)
CLR_GRAY = RGBColor(0x66, 0x66, 0x66)
CLR_LIGHT_GRAY = RGBColor(0xF2, 0xF2, 0xF2)
CLR_GREEN = RGBColor(0x2E, 0x7D, 0x32)
CLR_RED = RGBColor(0xC6, 0x28, 0x28)
CLR_MEDIUM_GRAY = RGBColor(0x99, 0x99, 0x99)
CLR_BG = RGBColor(0xF8, 0xFB, 0xFF)
CLR_TITLE_LINE = RGBColor(0x3B, 0x82, 0xF6)


def extract_latex_macro(preamble_path: Path, macro_name: str, fallback: str) -> str:
    """Extract a simple \\newcommand{\\macro}{value} from LaTeX preamble."""
    try:
        content = preamble_path.read_text(encoding="utf-8")
    except OSError:
        return fallback

    macro_prefix = f"\\newcommand{{\\{macro_name}}}{{"
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith(macro_prefix) and stripped.endswith("}"):
            value = stripped[len(macro_prefix):-1].strip()
            return value or fallback

    pattern = re.compile(rf"\\newcommand\{{\\{re.escape(macro_name)}\}}\{{(.+?)\}}")
    match = pattern.search(content)
    if match:
        return match.group(1).strip() or fallback
    return fallback

def add_slide_footer(slide, footer_text: str = "Διπλωματική Εργασία - Μάρτιος 2026"):
    """Add subtle footer line and right-aligned footer text."""
    footer_line = slide.shapes.add_shape(
        1, Inches(0.5), Inches(7.06), Inches(12.3), Inches(0.01)
    )
    footer_line.fill.solid()
    footer_line.fill.fore_color.rgb = CLR_ACCENT
    footer_line.line.fill.background()

    add_textbox(
        slide,
        Inches(0.5),
        Inches(7.10),
        Inches(12.3),
        Inches(0.24),
        footer_text,
        Pt(9),
        CLR_ACCENT,
        alignment=PP_ALIGN.RIGHT,
    )


def add_table_legend(slide, table_caption: str = "", table_ref: str = "", source: str = ""):
    """Add a compact table legend bar."""
    parts = [part for part in [table_caption, table_ref, source] if part]
    legend_text = " | ".join(parts)
    if not legend_text:
        return

    legend_box = slide.shapes.add_shape(
        1, Inches(0.5), Inches(6.68), Inches(12.3), Inches(0.26)
    )
    legend_box.fill.solid()
    legend_box.fill.fore_color.rgb = CLR_LIGHT_GRAY
    legend_box.line.fill.background()

    tf = legend_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
    tf.margin_top = Inches(0.02)
    p = tf.paragraphs[0]
    p.text = legend_text
    p.font.size = Pt(10)
    p.font.color.rgb = CLR_GRAY
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.LEFT


def add_figure_legend(
    slide,
    left,
    top,
    width,
    caption: str = "",
    ref: str = "",
    source: str = "",
):
    """Add a compact centered legend beneath a figure."""
    if not caption and not ref and not source:
        return

    parts = []
    if caption:
        parts.append(caption)
    if ref:
        parts.append(f"Ref: {ref}")
    if source:
        parts.append(source)
    text = " | ".join(parts)

    legend_box = slide.shapes.add_shape(1, left, top, width, Inches(0.32))
    legend_box.fill.solid()
    legend_box.fill.fore_color.rgb = CLR_LIGHT_GRAY
    legend_box.line.fill.background()

    tf = legend_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.08)
    tf.margin_right = Inches(0.08)
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(8.5)
    p.font.color.rgb = CLR_GRAY
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.CENTER


def infer_figure_ref_and_caption(figure_name: str) -> tuple[str, str]:
    """Infer thesis figure reference key and caption from figure filename."""
    mapping = {
        "Speech_Language_Assessment_Parkinson_Disease_Diagram.png": (
            "fig:speech-language-assessment-pd",
            "Figure 1.1: Clinical speech-language assessment in PD",
        ),
        "speech_signal_hc_vs_pd.png": (
            "fig:speech-signal-hc-vs-pd",
            "Figure 2.1: Speech signal comparison (HC vs PD)",
        ),
        "fig_pipeline_overview_thesis.png": (
            "fig:pipeline-overview-thesis",
            "Figure 1.2: Experimental pipeline overview",
        ),
        "fig_roc_readtext.pdf": (
            "fig:roc-readtext-main",
            "Figure 6.1: ROC curves for ReadText task",
        ),
        "fig_roc_readtext.png": (
            "fig:roc-readtext-main",
            "Figure 6.1: ROC curves for ReadText task",
        ),
        "fig_roc_spontaneous.pdf": (
            "fig:roc-spontaneous-main",
            "Figure 6.2: ROC curves for SpontaneousDialogue task",
        ),
        "fig_roc_spontaneous.png": (
            "fig:roc-spontaneous-main",
            "Figure 6.2: ROC curves for SpontaneousDialogue task",
        ),
        "fig_roc_dataset_b.pdf": (
            "fig:roc-datasetb-main",
            "Figure 6.3: ROC curves for Dataset B",
        ),
        "fig_roc_dataset_b.png": (
            "fig:roc-datasetb-main",
            "Figure 6.3: ROC curves for Dataset B",
        ),
        "fig_confusion_readtext.pdf": (
            "fig:confusion-readtext",
            "Figure 6.4: Confusion matrix — ReadText",
        ),
        "fig_confusion_readtext.png": (
            "fig:confusion-readtext",
            "Figure 6.4: Confusion matrix — ReadText",
        ),
        "fig_confusion_spontaneous.pdf": (
            "fig:confusion-spontaneous",
            "Figure 6.5: Confusion matrix — SpontaneousDialogue",
        ),
        "fig_confusion_spontaneous.png": (
            "fig:confusion-spontaneous",
            "Figure 6.5: Confusion matrix — SpontaneousDialogue",
        ),
        "fig_confusion_dataset_b.pdf": (
            "fig:confusion-datasetb",
            "Figure 6.6: Confusion matrix — Dataset B",
        ),
        "fig_confusion_dataset_b.png": (
            "fig:confusion-datasetb",
            "Figure 6.6: Confusion matrix — Dataset B",
        ),
        "fig_imp_readtext_cats.png": (
            "fig:imp-categories-main",
            "Figure 7.1: Category importance — ReadText",
        ),
        "fig_imp_spontaneous_cats.png": (
            "fig:imp-categories-main",
            "Figure 7.2: Category importance — SpontaneousDialogue",
        ),
        "fig_heatmap_readtext_permutation.png": (
            "fig:heatmap-readtext-permutation-main",
            "Figure 7.3: Permutation importance heatmap — ReadText",
        ),
        "fig_heatmap_spontaneous_permutation.png": (
            "fig:heatmap-spontaneous-permutation-main",
            "Figure 7.4: Permutation importance heatmap — SpontaneousDialogue",
        ),
        "webapp-architecture.png": (
            "fig:demo-architecture-simple",
            "Figure 1.3: Demo application architecture",
        ),
        "fig_demo_upload_audio.png": (
            "fig:demo-screens-main",
            "Figure 1.4a: Demo upload screen",
        ),
        "fig_demo_analysis_result.png": (
            "fig:demo-screens-main",
            "Figure 1.4b: Demo analysis result",
        ),
    }
    if figure_name in mapping:
        return mapping[figure_name]
    return "[placeholder-ref]", f"Figure: {figure_name}"




def infer_figure_source(figure_name: str) -> str:
    """Infer source note for adapted figures that require direct paper credit."""
    source_map = {
        "Speech_Language_Assessment_Parkinson_Disease_Diagram.png": "Source: Adapted from Cao et al. (2025)",
        "speech_signal_hc_vs_pd.png": "Source: Adapted from Little et al. (2009)",
    }
    return source_map.get(figure_name, "")


def infer_table_ref_and_caption(title: str) -> tuple[str, str]:
    """Infer thesis table reference key and caption from slide title."""
    mapping = {
        "Dataset A — MDVR-KCL (Raw Audio)": (
            "tab:dataset-a-summary",
            "Table 3.1: Dataset A summary",
        ),
        "Dataset B & Cross-Dataset Comparison": (
            "tab:cross-dataset-comparison",
            "Table 3.3: Cross-dataset comparison",
        ),
        "Feature Extraction — Baseline (47) vs Extended (78)": (
            "tab:feature-counts",
            "Table 4.4: Feature counts by configuration",
        ),
        "Models & Parameters (Fixed A Priori)": (
            "tab:model-specs",
            "Table 4.5: Model specifications",
        ),
        "Experimental Design — 2×2×5 Factorial (300 Runs)": (
            "tab:conditions",
            "Table 5.1: Experimental conditions C1–C4",
        ),
        "Headline Results — Best ROC-AUC per Dataset": (
            "tab:best-results-summary",
            "Table 6.1: Best ROC-AUC summary",
        ),
        "RQ2 — Feature Extension Effect (Δ ROC-AUC: C3 − C1)": (
            "tab:ablation-main",
            "Table 6.3: Feature ablation effect",
        ),
        "RQ3 — Class Weighting Effect (Random Forest, Dataset A)": (
            "tab:weighting-main",
            "Table 6.4: Class weighting effect",
        ),
        "RQ4 — Cross-Dataset Comparison & Variance": (
            "tab:variance-summary",
            "Table 6.5: Variance comparison",
        ),
        "Limitations — Honest Self-Assessment": (
            "tab:validity-threats-summary",
            "Table 8.2: Validity threats and mitigation",
        ),
        "Full Results — C4: Extended + Weighted (Dataset A)": (
            "tab:results-c4-dataset-a",
            "Table 6.7: Full C4 results — Dataset A",
        ),
        "Full Results — C4: Extended + Weighted (Dataset B)": (
            "tab:results-c4-dataset-b",
            "Table 6.8: Full C4 results — Dataset B",
        ),
        "Full ROC-AUC — Dataset A ReadText (All Conditions)": (
            "[appendix-b-placeholder]",
            "Appendix Table: ReadText ROC-AUC all conditions",
        ),
        "Research Gap & Thesis Positioning": (
            "[custom-placeholder]",
            "Table: Literature gap vs thesis positioning",
        ),
    }
    if title in mapping:
        return mapping[title]
    return "[placeholder-ref]", f"Table: {title}"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def pdf_to_png(pdf_path: Path) -> Path:
    """Convert a PDF figure to PNG using pdftoppm (300 DPI)."""
    png_path = pdf_path.with_suffix(".png")
    if png_path.exists():
        return png_path
    # pdftoppm outputs name-1.png for single page
    tmp_prefix = str(pdf_path.with_suffix(""))
    subprocess.run(
        ["pdftoppm", "-png", "-r", "300", "-singlefile", str(pdf_path), tmp_prefix],
        check=True,
        capture_output=True,
    )
    expected = Path(f"{tmp_prefix}.png")
    if expected.exists():
        return expected
    raise FileNotFoundError(f"Failed to convert {pdf_path} to PNG")


def ensure_figure(name: str) -> Path | None:
    """Resolve a figure file, converting PDF→PNG if needed."""
    fig_path = FIGURES / name
    if fig_path.exists():
        if fig_path.suffix == ".pdf":
            return pdf_to_png(fig_path)
        return fig_path
    # Try PNG variant of PDF name
    png_variant = fig_path.with_suffix(".png")
    if png_variant.exists():
        return png_variant
    return None


def set_slide_bg(slide, color: RGBColor = CLR_BG):
    """Set solid background color on a slide."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(
    slide,
    left,
    top,
    width,
    height,
    text="",
    font_size=Pt(18),
    font_color=CLR_BLACK,
    bold=False,
    alignment=PP_ALIGN.LEFT,
    font_name="Calibri",
):
    """Add a text box and return the textframe for further editing."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = font_size
    p.font.color.rgb = font_color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return tf


def add_paragraph(tf, text, font_size=Pt(16), font_color=CLR_BLACK, bold=False,
                  alignment=PP_ALIGN.LEFT, space_before=Pt(4), space_after=Pt(2),
                  font_name="Calibri", level=0):
    """Append a paragraph to an existing text frame."""
    p = tf.add_paragraph()
    p.text = text
    p.font.size = font_size
    p.font.color.rgb = font_color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    p.space_before = space_before
    p.space_after = space_after
    p.level = level
    return p


def add_bullet_slide(
    slide,
    title: str,
    bullets: list[str],
    sub_bullets: dict[int, list[str]] | None = None,
    figure_name: str | None = None,
    figure_width: float = 4.5,
    figure_right: bool = True,
    note: str = "",
):
    """Create a standard content slide with title, bullets, optional figure."""
    set_slide_bg(slide)

    # Title bar (dark blue strip at top)
    title_shape = slide.shapes.add_shape(
        1, Inches(0), Inches(0), SLIDE_WIDTH, Inches(1.1)  # rectangle
    )
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = CLR_DARK_BLUE
    title_shape.line.fill.background()

    accent_line = slide.shapes.add_shape(
        1, Inches(0), Inches(1.08), SLIDE_WIDTH, Inches(0.02)
    )
    accent_line.fill.solid()
    accent_line.fill.fore_color.rgb = CLR_TITLE_LINE
    accent_line.line.fill.background()

    tf_title = title_shape.text_frame
    tf_title.word_wrap = True
    p = tf_title.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.color.rgb = CLR_WHITE
    p.font.bold = True
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.LEFT
    # Add left padding via indent
    tf_title.margin_left = Inches(0.5)
    tf_title.margin_top = Inches(0.15)

    # Determine content area
    has_figure = figure_name and ensure_figure(figure_name)
    if has_figure and figure_right:
        content_width = Inches(13.333 - figure_width - 0.8)
        content_left = Inches(0.5)
    elif has_figure and not figure_right:
        content_width = Inches(13.333 - figure_width - 0.8)
        content_left = Inches(figure_width + 0.5)
    else:
        content_width = Inches(12.3)
        content_left = Inches(0.5)

    # Bullets
    bullet_top = Inches(1.4)
    bullet_height = Inches(5.6)
    tf_bullets = add_textbox(
        slide, content_left, bullet_top, content_width, bullet_height,
        text="", font_size=Pt(18), font_color=CLR_BLACK
    )
    tf_bullets.paragraphs[0].text = ""  # clear default

    first = True
    for i, bullet in enumerate(bullets):
        if first:
            p = tf_bullets.paragraphs[0]
            first = False
        else:
            p = tf_bullets.add_paragraph()
        p.text = bullet
        p.font.size = Pt(18)
        p.font.color.rgb = CLR_BLACK
        p.font.name = "Calibri"
        p.space_before = Pt(6)
        p.space_after = Pt(3)
        p.level = 0

        # Sub-bullets
        if sub_bullets and i in sub_bullets:
            for sb in sub_bullets[i]:
                sp = tf_bullets.add_paragraph()
                sp.text = sb
                sp.font.size = Pt(15)
                sp.font.color.rgb = CLR_GRAY
                sp.font.name = "Calibri"
                sp.space_before = Pt(2)
                sp.space_after = Pt(1)
                sp.level = 1

    # Figure
    if has_figure:
        fig_path = ensure_figure(figure_name)
        fig_w = Inches(figure_width)
        if figure_right:
            fig_left = SLIDE_WIDTH - fig_w - Inches(0.3)
        else:
            fig_left = Inches(0.3)
        fig_top = Inches(1.4)
        fig_h = Inches(5.0)
        try:
            pic = slide.shapes.add_picture(str(fig_path), fig_left, fig_top, width=fig_w)
            # Scale height proportionally
            ratio = pic.height / pic.width
            pic.width = fig_w
            pic.height = int(fig_w * ratio)
            # Cap height
            if pic.height > fig_h:
                pic.height = fig_h
                pic.width = int(fig_h / ratio)

            fig_ref, fig_caption = infer_figure_ref_and_caption(figure_name)
            legend_top = min(
                pic.top + pic.height + Inches(0.06),
                SLIDE_HEIGHT - Inches(0.45),
            )
            add_figure_legend(
                slide,
                pic.left,
                legend_top,
                pic.width,
                caption=fig_caption,
                ref=fig_ref,
                source=infer_figure_source(figure_name),
            )
        except Exception:
            pass  # Skip if image fails

    # Speaker notes
    if note:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = note

    add_slide_footer(slide)

    return tf_bullets


def add_table_slide(
    slide,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[float] | None = None,
    note: str = "",
    highlight_cells: list[tuple[int, int]] | None = None,
    table_caption: str = "",
    table_ref: str = "",
    source: str = "",
):
    """Create a slide with a title and table."""
    set_slide_bg(slide)

    # Title bar
    title_shape = slide.shapes.add_shape(
        1, Inches(0), Inches(0), SLIDE_WIDTH, Inches(1.1)
    )
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = CLR_DARK_BLUE
    title_shape.line.fill.background()

    accent_line = slide.shapes.add_shape(
        1, Inches(0), Inches(1.08), SLIDE_WIDTH, Inches(0.02)
    )
    accent_line.fill.solid()
    accent_line.fill.fore_color.rgb = CLR_TITLE_LINE
    accent_line.line.fill.background()

    tf_title = title_shape.text_frame
    tf_title.word_wrap = True
    p = tf_title.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.color.rgb = CLR_WHITE
    p.font.bold = True
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.LEFT
    tf_title.margin_left = Inches(0.5)
    tf_title.margin_top = Inches(0.15)

    # Table
    n_rows = len(rows) + 1  # +1 for header
    n_cols = len(headers)
    table_left = Inches(0.5)
    table_top = Inches(1.5)
    table_width = Inches(12.3)
    table_height = Inches(0.43) * n_rows

    if col_widths:
        total = sum(col_widths)
        actual_widths = [Inches(w / total * 12.3) for w in col_widths]
    else:
        actual_widths = [Inches(12.3 / n_cols)] * n_cols

    table_shape = slide.shapes.add_table(n_rows, n_cols, table_left, table_top, table_width, table_height)
    table = table_shape.table

    # Set column widths
    for i, w in enumerate(actual_widths):
        table.columns[i].width = w

    # Header row
    for j, header in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = CLR_BLUE
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(14)
            paragraph.font.color.rgb = CLR_WHITE
            paragraph.font.bold = True
            paragraph.font.name = "Calibri"
            paragraph.alignment = PP_ALIGN.CENTER
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    # Data rows
    highlight_cells = highlight_cells or []
    for i, row_data in enumerate(rows):
        for j, val in enumerate(row_data):
            cell = table.cell(i + 1, j)
            cell.text = val
            if i % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = CLR_LIGHT_GRAY
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = CLR_WHITE
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(13)
                paragraph.font.color.rgb = CLR_BLACK
                paragraph.font.name = "Calibri"
                paragraph.alignment = PP_ALIGN.CENTER
                if (i, j) in highlight_cells:
                    paragraph.font.bold = True
                    paragraph.font.color.rgb = CLR_ACCENT
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    if note:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = note

    if not table_caption or not table_ref:
        inferred_ref, inferred_caption = infer_table_ref_and_caption(title)
        if not table_ref:
            table_ref = inferred_ref
        if not table_caption:
            table_caption = inferred_caption
    if not source:
        source = "Source: Thesis manuscript and computed results"

    add_table_legend(slide, table_caption=table_caption, table_ref=table_ref, source=source)
    add_slide_footer(slide)


def add_figure_slide(slide, title: str, figure_names: list[str],
                     captions: list[str] | None = None, note: str = "",
                     max_per_row: int = 3):
    """Create a figure-focused slide with 1-3 images."""
    set_slide_bg(slide)

    # Title bar
    title_shape = slide.shapes.add_shape(
        1, Inches(0), Inches(0), SLIDE_WIDTH, Inches(1.1)
    )
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = CLR_DARK_BLUE
    title_shape.line.fill.background()

    accent_line = slide.shapes.add_shape(
        1, Inches(0), Inches(1.08), SLIDE_WIDTH, Inches(0.02)
    )
    accent_line.fill.solid()
    accent_line.fill.fore_color.rgb = CLR_TITLE_LINE
    accent_line.line.fill.background()

    tf_title = title_shape.text_frame
    tf_title.word_wrap = True
    p = tf_title.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.color.rgb = CLR_WHITE
    p.font.bold = True
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.LEFT
    tf_title.margin_left = Inches(0.5)
    tf_title.margin_top = Inches(0.15)

    # Resolve figures
    valid_figs: list[tuple[str, Path]] = []
    for fn in figure_names:
        fig_path = ensure_figure(fn)
        if fig_path:
            valid_figs.append((fn, fig_path))

    if not valid_figs:
        add_textbox(slide, Inches(2), Inches(3), Inches(9), Inches(1),
                    "[Figures not found]", Pt(20), CLR_GRAY, alignment=PP_ALIGN.CENTER)
        add_slide_footer(slide)
        return

    n = len(valid_figs)
    captions = captions or [""] * n

    if n == 1:
        fig_w = Inches(9)
        fig_h = Inches(5.5)
        fig_left = Inches(2.2)
        fig_top = Inches(1.4)
        try:
            pic = slide.shapes.add_picture(str(valid_figs[0][1]), fig_left, fig_top, width=fig_w)
            ratio = pic.height / pic.width
            pic.width = fig_w
            pic.height = int(fig_w * ratio)
            if pic.height > fig_h:
                pic.height = fig_h
                pic.width = int(fig_h / ratio)
            # Center horizontally
            pic.left = int((SLIDE_WIDTH - pic.width) / 2)

            mapped_ref, mapped_caption = infer_figure_ref_and_caption(valid_figs[0][0])
            primary_caption = captions[0] if captions and captions[0] else mapped_caption
            add_figure_legend(
                slide,
                pic.left,
                min(pic.top + pic.height + Inches(0.06), SLIDE_HEIGHT - Inches(0.45)),
                pic.width,
                caption=primary_caption,
                ref=mapped_ref,
                source=infer_figure_source(valid_figs[0][0]),
            )
        except Exception:
            pass

    elif n == 2:
        for idx in range(2):
            fig_w = Inches(5.8)
            fig_h = Inches(4.8)
            fig_left = Inches(0.4 + idx * 6.5)
            fig_top = Inches(1.4)
            try:
                pic = slide.shapes.add_picture(str(valid_figs[idx][1]), fig_left, fig_top, width=fig_w)
                ratio = pic.height / pic.width
                pic.width = fig_w
                pic.height = int(fig_w * ratio)
                if pic.height > fig_h:
                    pic.height = fig_h
                    pic.width = int(fig_h / ratio)

                mapped_ref, mapped_caption = infer_figure_ref_and_caption(valid_figs[idx][0])
                provided_caption = captions[idx] if idx < len(captions) else ""
                primary_caption = provided_caption if provided_caption else mapped_caption
                add_figure_legend(
                    slide,
                    pic.left,
                    min(pic.top + pic.height + Inches(0.06), SLIDE_HEIGHT - Inches(0.45)),
                    pic.width,
                    caption=primary_caption,
                    ref=mapped_ref,
                    source=infer_figure_source(valid_figs[idx][0]),
                )
            except Exception:
                pass

    else:  # 3
        for idx in range(min(n, 3)):
            fig_w = Inches(3.8)
            fig_h = Inches(4.5)
            fig_left = Inches(0.3 + idx * 4.3)
            fig_top = Inches(1.4)
            try:
                pic = slide.shapes.add_picture(str(valid_figs[idx][1]), fig_left, fig_top, width=fig_w)
                ratio = pic.height / pic.width
                pic.width = fig_w
                pic.height = int(fig_w * ratio)
                if pic.height > fig_h:
                    pic.height = fig_h
                    pic.width = int(fig_h / ratio)

                mapped_ref, mapped_caption = infer_figure_ref_and_caption(valid_figs[idx][0])
                provided_caption = captions[idx] if idx < len(captions) else ""
                primary_caption = provided_caption if provided_caption else mapped_caption
                add_figure_legend(
                    slide,
                    pic.left,
                    min(pic.top + pic.height + Inches(0.06), SLIDE_HEIGHT - Inches(0.45)),
                    pic.width,
                    caption=primary_caption,
                    ref=mapped_ref,
                    source=infer_figure_source(valid_figs[idx][0]),
                )
            except Exception:
                pass

    if note:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = note

    add_slide_footer(slide)


def add_section_divider(slide, section_title: str, subtitle: str = "", note: str = ""):
    """Create a section divider slide."""
    set_slide_bg(slide, CLR_DARK_BLUE)

    # Decorative line
    line = slide.shapes.add_shape(
        1, Inches(1), Inches(3.2), Inches(11.333), Inches(0.03)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = CLR_ACCENT
    line.line.fill.background()

    add_textbox(slide, Inches(1), Inches(2), Inches(11.333), Inches(1.2),
                section_title, Pt(40), CLR_WHITE, bold=True,
                alignment=PP_ALIGN.LEFT)

    if subtitle:
        add_textbox(slide, Inches(1), Inches(3.5), Inches(11.333), Inches(1),
                    subtitle, Pt(20), CLR_LIGHT_BLUE, alignment=PP_ALIGN.LEFT)

    if note:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = note

    add_slide_footer(slide)


# ===========================================================================
# MAIN PRESENTATION BUILDER
# ===========================================================================
def build_presentation():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    # Use blank layout for all slides
    blank_layout = prs.slide_layouts[6]  # Blank

    # -----------------------------------------------------------------------
    # SLIDE 1: TITLE
    # -----------------------------------------------------------------------
    author_name = extract_latex_macro(THESIS_PREAMBLE, "myAuthor", "[Your Name]")

    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, CLR_DARK_BLUE)

    # Logo
    logo_path = FIGURES / "ntua-logo.png"
    if logo_path.exists():
        slide.shapes.add_picture(str(logo_path), Inches(5.6), Inches(0.4),
                                 height=Inches(1.5))

    # Title
    add_textbox(slide, Inches(1), Inches(2.0), Inches(11.333), Inches(2.1),
                "Voice-Based Classification of\nParkinson's Disease Using\nClassical Machine Learning",
                Pt(34), CLR_WHITE, bold=True, alignment=PP_ALIGN.CENTER,
                font_name="Calibri")

    add_textbox(
        slide,
        Inches(1),
        Inches(4.75),
        Inches(11.333),
        Inches(0.3),
        "Research Demonstration — Not for clinical use",
        Pt(12),
        CLR_ACCENT,
        alignment=PP_ALIGN.CENTER,
    )

    # Divider line
    line = slide.shapes.add_shape(
        1, Inches(4), Inches(4.6), Inches(5.333), Inches(0.03)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = CLR_ACCENT
    line.line.fill.background()

    # Author info
    add_textbox(slide, Inches(1), Inches(5.0), Inches(11.333), Inches(0.5),
                f"Author: {author_name}", Pt(20), CLR_LIGHT_BLUE,
                alignment=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(1), Inches(5.35), Inches(11.333), Inches(0.45),
                "MSc Thesis Defense", Pt(18), CLR_LIGHT_BLUE,
                alignment=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(1), Inches(5.8), Inches(11.333), Inches(0.5),
                "National Technical University of Athens",
                Pt(16), CLR_MEDIUM_GRAY, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(1), Inches(6.25), Inches(11.333), Inches(0.5),
                "March 2026", Pt(16), CLR_MEDIUM_GRAY,
                alignment=PP_ALIGN.CENTER)

    slide.notes_slide.notes_text_frame.text = (
        "Welcome the committee. Wait for readiness before proceeding."
    )

    # -----------------------------------------------------------------------
    # SLIDE 2: OUTLINE
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_bullet_slide(slide, "Presentation Outline", [
        "1. Introduction & Motivation",
        "2. Related Work & Research Gap",
        "3. Datasets",
        "4. Methodology (Feature Extraction + ML Pipeline)",
        "5. Experimental Design (2×2×5 Factorial)",
        "6. Results (ROC-AUC, Ablation, Class Weighting)",
        "7. Discussion & Feature Importance",
        "8. Limitations, Conclusion & Future Work",
    ], note="I'll spend about 25 minutes, with most time on methodology and results. "
            "I'll keep discussion of limitations honest and transparent. "
            "Transition: Let's start with why this problem matters.")

    # -----------------------------------------------------------------------
    # SLIDE 3: PD AND SPEECH — THE CLINICAL PROBLEM
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_bullet_slide(slide,
        "Parkinson's Disease & Speech Impairment",
        [
            "PD: 2nd most common neurodegenerative disease (~10M worldwide)",
            "70–90% of PD patients develop measurable speech disorders",
            "Hypokinetic dysarthria: reduced loudness, monotone pitch, breathy quality",
            "Voice changes can precede motor symptoms by years (Harel et al. 2004)",
            "Current diagnosis: subjective clinical assessment — no objective biomarker",
        ],
        figure_name="Speech_Language_Assessment_Parkinson_Disease_Diagram.png",
        figure_width=5.0,
        note="Emphasize that voice is a non-invasive, low-cost, remotely collectible biomarker. "
             "The diagram shows clinical speech assessment across PD stages. "
             "Transition: This creates an opportunity for computational analysis."
    )

    # -----------------------------------------------------------------------
    # SLIDE 4: THE OPPORTUNITY — VOICE AS BIOMARKER
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_bullet_slide(slide,
        "The Opportunity — Voice as a Biomarker",
        [
            "Voice recordings capture PD-related acoustic changes objectively",
            "Can be collected via smartphone — scalable screening potential",
            "Acoustic features (jitter, shimmer, MFCCs, F₀) are quantifiable",
            "Classical ML can classify PD vs HC from feature vectors",
            "Growing literature — but persistent methodological problems",
        ],
        figure_name="speech_signal_hc_vs_pd.png",
        figure_width=5.5,
        note="The waveform comparison shows visible differences between HC and PD speech signals. "
             "Signal differences are real and measurable, but extracting reliable features and "
             "avoiding methodological pitfalls is harder than it looks. "
             "Transition: What does the literature say?"
    )

    # -----------------------------------------------------------------------
    # SLIDE 5: RESEARCH QUESTIONS
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_bullet_slide(slide,
        "Research Questions",
        [
            "RQ1: How well do classical ML models perform on PD voice classification?",
            "RQ2: Does increasing features from 47 → 78 improve performance?",
            "RQ3: Does balanced class weighting help with imbalanced data?",
            "RQ4: Are there differences between subject-level CV and standard CV?",
            "RQ5: Is there a performance difference between read vs spontaneous speech?",
        ],
        note="These five questions structure all 300 experiments. "
             "Each RQ will be answered with specific evidence in the results section. "
             "Transition: Before showing how I addressed these, let me summarize the literature gap."
    )

    # -----------------------------------------------------------------------
    # SLIDE 6: LITERATURE REVIEW
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_bullet_slide(slide,
        "Literature Review — Key Findings",
        [
            "SVM historically dominant (~91% accuracy — Little et al. 2009)",
            "~42% of 2020–2025 studies now use deep learning",
            "External validation in < 15% of studies",
            "Interpretability (SHAP/LIME) in < 10% of studies",
            "94% focus on detection; < 12% on progression monitoring",
            "Reporting quality varies widely (Sedigh-Malekroodi 2025, Xavier 2025)",
        ],
        note="The field has a reproducibility and overfitting problem. Many studies report "
             "inflated accuracy without proper validation. "
             "Transition: This is the gap I address."
    )

    # -----------------------------------------------------------------------
    # SLIDE 7: RESEARCH GAP & POSITIONING
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_table_slide(slide,
        "Research Gap & Thesis Positioning",
        ["Common Practice", "This Thesis"],
        [
            ["Random train/test split", "Grouped Stratified 5-Fold CV"],
            ["Report best result only", "All 300 experimental runs reported"],
            ["Tuned hyperparameters", "Fixed a priori parameters"],
            ["Single feature set", "Controlled ablation: 47 vs 78 features"],
            ["Ignore class imbalance", "Systematic class weighting analysis"],
            ["Minimal limitation discussion", "Full transparency on all limitations"],
        ],
        col_widths=[1, 1],
        note="I'm not claiming to beat the state of the art. I'm claiming to do it correctly "
             "and transparently. This is the core differentiator. "
             "Transition: Let me describe the data."
    )

    # -----------------------------------------------------------------------
    # SLIDE 8: DATASET A — MDVR-KCL
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_table_slide(slide,
        "Dataset A — MDVR-KCL (Raw Audio)",
        ["Property", "Value"],
        [
            ["Source", "King's College London (Zenodo)"],
            ["Format", "WAV PCM, mono, 16-bit, 44.1 kHz"],
            ["ReadText Subjects", "37 (21 HC, 16 PD)"],
            ["SpontaneousDialogue Subjects", "36 (21 HC, 15 PD)"],
            ["Recording Device", "Smartphone (Moto G4)"],
            ["Subject IDs", "✓ Available → Grouped CV possible"],
            ["Class Ratio", "~57:43 (HC:PD) — mild imbalance"],
        ],
        col_widths=[1.2, 2],
        note="The small sample is a limitation I'll address, but subject IDs are critical — "
             "they let us prevent data leakage. "
             "Transition: The second dataset is very different."
    )

    # -----------------------------------------------------------------------
    # SLIDE 9: DATASET B + CROSS-COMPARISON
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_table_slide(slide,
        "Dataset B & Cross-Dataset Comparison",
        ["Aspect", "Dataset A (MDVR-KCL)", "Dataset B (PD Speech)"],
        [
            ["Input", "Raw audio (WAV)", "Pre-extracted (CSV)"],
            ["Samples", "37/36 subjects", "756 samples (252 subjects)"],
            ["Subject IDs", "✓ Available", "✗ Not available"],
            ["Validation", "Grouped Stratified CV", "Stratified CV"],
            ["Speech Task", "Read / Spontaneous", "Sustained vowel /a/"],
            ["Class Balance", "57:43 (HC:PD)", "25:75 (HC:PD)"],
        ],
        col_widths=[1, 1.3, 1.3],
        note="Dataset B gives us higher statistical power but weaker methodological guarantees. "
             "This contrast is itself a finding. "
             "Transition: Now, how did I process the data?"
    )

    # -----------------------------------------------------------------------
    # SLIDE 10: PIPELINE OVERVIEW
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_figure_slide(slide,
        "Experimental Pipeline Overview",
        ["fig_pipeline_overview_thesis.png"],
        captions=["Pipeline A: WAV → Preprocessing → Feature Extraction → ML → Metrics  |  "
                  "Pipeline B: CSV → ML → Metrics"],
        note="Two pipelines, kept strictly separate. Dataset A goes through our feature extraction; "
             "Dataset B skips it. Both feed into the same 5 classifiers with identical evaluation. "
             "Transition: Let me detail the feature extraction step."
    )

    # -----------------------------------------------------------------------
    # SLIDE 11: FEATURE EXTRACTION
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_table_slide(slide,
        "Feature Extraction — Baseline (47) vs Extended (78)",
        ["Category", "Count", "Features"],
        [
            ["Prosodic", "21", "F₀ (4), Jitter (3), Shimmer (5), HNR (2), Intensity (3), Formants (6)"],
            ["MFCC means", "13", "13 cepstral coefficients (baseline spectral)"],
            ["Δ-MFCC means", "13", "First-order temporal derivatives"],
            ["— Baseline Total —", "47", "Prosodic + MFCC + Δ-MFCC"],
            ["MFCC std", "+13", "Cepstral variability (extended)"],
            ["ΔΔ-MFCC means", "+13", "Second-order dynamics (extended)"],
            ["Spectral shape", "+5", "Centroid, bandwidth, rolloff, flatness, ZCR"],
            ["— Extended Total —", "78", "Baseline + 31 additional features"],
        ],
        col_widths=[1.2, 0.6, 3],
        highlight_cells=[(3, 0), (3, 1), (7, 0), (7, 1)],
        note="The feature set captures phonatory dysfunction (jitter, shimmer) and spectral "
             "characteristics (MFCCs). The extension adds variability and higher-order dynamics. "
             "Tools: Parselmouth (Praat), librosa. Fixed parameters: 22050 Hz, seed 42. "
             "Transition: These features feed into five classifiers."
    )

    # -----------------------------------------------------------------------
    # SLIDE 12: MODELS & PARAMETERS
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_table_slide(slide,
        "Models & Parameters (Fixed A Priori)",
        ["Model", "Key Parameters", "Notes"],
        [
            ["Logistic Regression", "C=1.0, L2, lbfgs", "Linear baseline"],
            ["SVM (RBF kernel)", "C=1.0, γ=scale", "Non-linear, margin-based"],
            ["Random Forest", "100 trees, depth=10", "Ensemble, robust to noise"],
            ["Gradient Boosting", "100 trees, lr=0.1, depth=3", "Sequential ensemble"],
            ["XGBoost", "100 trees, lr=0.1", "Regularized boosting"],
        ],
        col_widths=[1.2, 1.3, 1.2],
        note="No hyperparameter tuning is a deliberate choice. At n=37, nested CV would be "
             "unreliable and introduce more variance than it reduces (Varma & Simon 2006). "
             "This is a conservative baseline. All pipelines include StandardScaler. "
             "Transition: How did I validate?"
    )

    # -----------------------------------------------------------------------
    # SLIDE 13: CROSS-VALIDATION STRATEGY
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_bullet_slide(slide,
        "Cross-Validation Strategy",
        [
            "Dataset A: Grouped Stratified 5-Fold CV",
            "Dataset B: Stratified 5-Fold CV (sample-level)",
            "All metrics: mean ± std across 5 folds",
            "Primary metric: ROC-AUC",
            "Secondary: Accuracy, Precision, Recall, F1-Score",
        ],
        sub_bullets={
            0: [
                "All recordings from one subject → same fold",
                "Prevents data leakage — the most important design choice",
            ],
            1: [
                "Subject IDs unavailable → potential within-subject leakage",
                "Results flagged as potentially optimistic",
            ],
        },
        note="This is the most important methodological decision. Grouped CV is what separates "
             "a reliable estimate from an inflated one. Most studies in the literature don't do this. "
             "Transition: Now let me describe the full experimental design."
    )

    # -----------------------------------------------------------------------
    # SLIDE 14: EXPERIMENTAL DESIGN
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_table_slide(slide,
        "Experimental Design — 2×2×5 Factorial (300 Runs)",
        ["Condition", "Features", "Weighting", "Models"],
        [
            ["C1", "47 (baseline)", "None", "LR, SVM, RF, GB, XGB"],
            ["C2", "47 (baseline)", "Balanced", "LR, SVM, RF, GB, XGB"],
            ["C3", "78 (extended)", "None", "LR, SVM, RF, GB, XGB"],
            ["C4", "78 (extended)", "Balanced", "LR, SVM, RF, GB, XGB"],
        ],
        col_widths=[0.8, 1.2, 0.8, 2],
        note="The factorial design lets me isolate the effect of each factor. "
             "4 conditions × 5 models × 3 datasets/tasks × 5 folds = 300 total runs. "
             "I report ALL 300 runs, not just the best. "
             "Transition: What did we find?"
    )

    # Add total runs summary below table
    add_textbox(slide, Inches(0.5), Inches(5.0), Inches(12.3), Inches(1.2),
                "", Pt(16), CLR_BLACK)
    tf_summary = slide.shapes[-1].text_frame
    tf_summary.word_wrap = True
    p = tf_summary.paragraphs[0]
    p.text = "Total: 4 conditions × 5 models × 3 datasets/tasks × 5 folds = 300 experimental runs"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = CLR_ACCENT
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.CENTER

    # -----------------------------------------------------------------------
    # SECTION DIVIDER: RESULTS
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_section_divider(slide, "Results",
                        "ROC-AUC · Ablation · Class Weighting · Variance",
                        note="Transition into the results section — the core of the defense.")

    # -----------------------------------------------------------------------
    # SLIDE 16: HEADLINE RESULTS
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_table_slide(slide,
        "Headline Results — Best ROC-AUC per Dataset",
        ["Dataset / Task", "Best Model", "ROC-AUC", "Condition"],
        [
            ["Dataset A (Spontaneous)", "Random Forest", "0.857 ± 0.171", "C3 (78, unweighted)"],
            ["Dataset A (ReadText)", "SVM (RBF)", "0.834 ± 0.153", "C3 (78, unweighted)"],
            ["Dataset B (PD Speech)", "XGBoost", "0.952 ± 0.015", "C1 (47, unweighted)"],
        ],
        col_widths=[1.3, 1, 1, 1.3],
        highlight_cells=[(0, 2), (2, 2)],
        note="Classical ML achieves meaningful discrimination. RF is most robust. "
             "Notice the variance: ±0.17 on Dataset A vs ±0.015 on Dataset B. "
             "Transition: Let me show the ROC curves."
    )
    # Add key insight below
    add_textbox(slide, Inches(0.5), Inches(4.8), Inches(12.3), Inches(1.5),
                "", Pt(16), CLR_BLACK)
    tf = slide.shapes[-1].text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Key: Random Forest is the most consistent performer across all conditions"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = CLR_BLUE
    p.font.name = "Calibri"
    add_paragraph(tf, "Dataset B scores substantially higher but with methodological caveats (no grouped CV)",
                  Pt(15), CLR_GRAY)

    # -----------------------------------------------------------------------
    # SLIDE 17: ROC CURVES — DATASET A
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_figure_slide(slide,
        "ROC Curves — Dataset A (Extended Features, Grouped 5-Fold CV)",
        ["fig_roc_readtext.pdf", "fig_roc_spontaneous.pdf"],
        captions=["(a) ReadText — SVM leads (0.834)", "(b) SpontaneousDialogue — RF leads (0.857)"],
        note="ReadText: SVM and RF dominate; LR moderate; GB weakest. "
             "SpontaneousDialogue: RF clearly best; SVM collapses to ~0.46. "
             "The spread between curves shows model sensitivity to the task. "
             "Transition: What about Dataset B?"
    )

    # -----------------------------------------------------------------------
    # SLIDE 18: ROC CURVES — DATASET B + CONFUSION MATRICES
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_figure_slide(slide,
        "ROC Curve — Dataset B & Confusion Matrices (Best Models)",
        ["fig_roc_dataset_b.pdf", "fig_confusion_readtext.pdf", "fig_confusion_spontaneous.pdf"],
        captions=[
            "(a) Dataset B — All models > 0.86",
            "(b) CM: ReadText (RF)",
            "(c) CM: Spontaneous (RF)",
        ],
        note="Dataset B curves are tightly clustered — easier task or data leakage. "
             "Confusion matrices show where errors cluster: false negatives (PD→HC) "
             "are the main issue — clinically the more dangerous error. "
             "Transition: Now let me isolate the feature extension effect — RQ2."
    )

    # -----------------------------------------------------------------------
    # SLIDE 19: FEATURE EXTENSION EFFECT (RQ2)
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_table_slide(slide,
        "RQ2 — Feature Extension Effect (Δ ROC-AUC: C3 − C1)",
        ["Model", "ReadText Δ", "Spontaneous Δ", "Interpretation"],
        [
            ["Logistic Regression", "−0.019", "+0.023", "Minimal change"],
            ["SVM (RBF)", "+0.220", "+0.053", "ReadText: dramatic gain"],
            ["Random Forest", "+0.232", "+0.029", "ReadText: dramatic gain"],
            ["Gradient Boosting", "+0.224", "+0.023", "ReadText: dramatic gain"],
            ["XGBoost", "+0.166", "−0.036", "Mixed"],
        ],
        col_widths=[1.2, 0.8, 0.8, 1.2],
        highlight_cells=[(1, 1), (2, 1), (3, 1)],
        note="Key finding: Feature extension dramatically improved ReadText (up to +23.2 pp) "
             "but had minimal effect on SpontaneousDialogue. Structured reading needs richer "
             "features; spontaneous speech naturally encodes PD cues through prosodic variation. "
             "Transition: What about class weighting?"
    )
    # Insight
    add_textbox(slide, Inches(0.5), Inches(5.8), Inches(12.3), Inches(1.0), "", Pt(16), CLR_BLACK)
    tf = slide.shapes[-1].text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Finding: Feature extension is task-dependent, not universal — up to +23.2 pp on ReadText, marginal on Spontaneous"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CLR_ACCENT
    p.font.name = "Calibri"

    # -----------------------------------------------------------------------
    # SLIDE 20: CLASS WEIGHTING EFFECT (RQ3)
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_table_slide(slide,
        "RQ3 — Class Weighting Effect (Random Forest, Dataset A)",
        ["Task / Features", "Δ ROC-AUC (Weighted − Unweighted)", "Verdict"],
        [
            ["ReadText / Baseline (47)", "+0.097", "Only positive case"],
            ["ReadText / Extended (78)", "−0.017", "Slightly harmful"],
            ["Spontaneous / Baseline (47)", "−0.001", "No effect"],
            ["Spontaneous / Extended (78)", "−0.034", "Slightly harmful"],
        ],
        col_widths=[1.5, 1.5, 1],
        highlight_cells=[(0, 1)],
        note="Class weighting provided no consistent benefit at ~1.3:1 imbalance. "
             "LR, SVM, GB, XGBoost all show negligible or negative effect. "
             "Useful negative evidence: practitioners shouldn't default to balanced weighting. "
             "Transition: Cross-dataset comparison and variance."
    )
    add_textbox(slide, Inches(0.5), Inches(5.2), Inches(12.3), Inches(1.5), "", Pt(16), CLR_BLACK)
    tf = slide.shapes[-1].text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Conclusion: At ~1.3:1 class imbalance, balanced weighting is unnecessary"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CLR_ACCENT
    p.font.name = "Calibri"
    add_paragraph(tf, "Other models (LR, SVM, GB, XGBoost): no benefit or slightly negative effect",
                  Pt(14), CLR_GRAY)

    # -----------------------------------------------------------------------
    # SLIDE 21: CROSS-DATASET COMPARISON & VARIANCE (RQ4)
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_table_slide(slide,
        "RQ4 — Cross-Dataset Comparison & Variance",
        ["Metric", "Dataset A (MDVR-KCL)", "Dataset B (PD Speech)"],
        [
            ["Best ROC-AUC", "0.857 ± 0.171", "0.952 ± 0.015"],
            ["ROC-AUC std range", "±0.15 – 0.30", "±0.01 – 0.03"],
            ["Accuracy std range", "±0.14 – 0.18", "±0.008 – 0.024"],
            ["F1 std range", "±0.21 – 0.39", "±0.006 – 0.015"],
        ],
        col_widths=[1.2, 1.3, 1.3],
        note="Performance gap is real but confounded: different sample size (37 vs 756), "
             "CV strategy, speech task, features, class balance. Cannot attribute to single factor. "
             "Dataset B's low variance suggests possible within-subject leakage."
    )
    add_textbox(slide, Inches(0.5), Inches(5.0), Inches(12.3), Inches(2.0), "", Pt(16), CLR_BLACK)
    tf = slide.shapes[-1].text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Confounders: sample size (37 vs 756), CV strategy, speech task, feature set, class balance"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CLR_RED
    p.font.name = "Calibri"
    add_paragraph(tf, "Dataset A's high variance is honest — ~7 subjects per fold with grouped CV",
                  Pt(14), CLR_GRAY)
    add_paragraph(tf, "Dataset B results flagged as potentially optimistic (no grouped CV possible)",
                  Pt(14), CLR_GRAY)

    # -----------------------------------------------------------------------
    # SLIDE 22: FEATURE IMPORTANCE — CATEGORY LEVEL
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_figure_slide(slide,
        "Feature Importance — Category-Level Aggregation (RF, Dataset A)",
        ["fig_imp_readtext_cats.png", "fig_imp_spontaneous_cats.png"],
        captions=[
            "(a) ReadText — MFCCs + pitch dominate",
            "(b) SpontaneousDialogue — MFCCs + shimmer dominate",
        ],
        note="MFCCs dominate (~28–32% of total importance). "
             "Pitch (F₀ max) is top-1 for ReadText. "
             "Shimmer (APQ11) is top-2 for SpontaneousDialogue. "
             "Cross-task stable features: delta_mfcc_2, autocorr_harmonicity, f0_mean, shimmer_apq. "
             "Transition: Permutation importance heatmaps."
    )

    # -----------------------------------------------------------------------
    # SLIDE 23: PERMUTATION IMPORTANCE HEATMAPS
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_figure_slide(slide,
        "Permutation Importance Heatmaps (Model-Agnostic)",
        ["fig_heatmap_readtext_permutation.png", "fig_heatmap_spontaneous_permutation.png"],
        captions=[
            "(a) ReadText — Feature × Model",
            "(b) SpontaneousDialogue — Feature × Model",
        ],
        note="Permutation importance measures actual predictive contribution. "
             "Sparse activation: a handful of features do most of the work. "
             "RF and XGBoost share similar importance profiles. "
             "GB importance is more concentrated on fewer features. "
             "Transition: Let me address the limitations honestly."
    )

    # -----------------------------------------------------------------------
    # SLIDE 24: LIMITATIONS
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_table_slide(slide,
        "Limitations — Honest Self-Assessment",
        ["Limitation", "Impact", "Mitigation"],
        [
            ["Small sample (n=37, Dataset A)", "High variance, limited power", "Grouped CV is more honest than inflated n"],
            ["No subject IDs (Dataset B)", "Potential leakage/optimism", "Clearly flagged throughout thesis"],
            ["No hyperparameter tuning", "May underestimate potential", "At n=37, nested CV unreliable (Varma 2006)"],
            ["No external validation", "Unknown generalization", "Explicitly listed as future work"],
            ["Classical ML only", "DL excluded by design", "Data too small for DL; provides baseline"],
            ["Single recording device", "Unknown cross-device robustness", "Standard research protocol"],
        ],
        col_widths=[1.3, 1.2, 1.5],
        note="Every limitation has a mitigation or justification documented in the thesis. "
             "Being explicit about what this study cannot claim is a strength. "
             "Transition: Despite these, the contributions are clear."
    )

    # -----------------------------------------------------------------------
    # SLIDE 25: CONTRIBUTIONS & CONCLUSION
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide)

    # Title bar
    title_shape = slide.shapes.add_shape(
        1, Inches(0), Inches(0), SLIDE_WIDTH, Inches(1.1)
    )
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = CLR_DARK_BLUE
    title_shape.line.fill.background()
    tf_t = title_shape.text_frame
    tf_t.margin_left = Inches(0.5)
    tf_t.margin_top = Inches(0.15)
    p = tf_t.paragraphs[0]
    p.text = "Contributions & Conclusion"
    p.font.size = Pt(28)
    p.font.color.rgb = CLR_WHITE
    p.font.bold = True
    p.font.name = "Calibri"

    # Left column: Contributions
    tf_left = add_textbox(slide, Inches(0.5), Inches(1.4), Inches(6), Inches(5.5),
                          "Contributions", Pt(20), CLR_BLUE, bold=True)
    contributions = [
        "C1: Rigorous grouped CV preventing subject leakage",
        "C2: Controlled feature ablation (47 vs 78) under identical conditions",
        "C3: Full reproducibility — fixed seed, default params, open pipeline",
        "C4: Permutation-based feature importance with cross-task analysis",
    ]
    for c in contributions:
        add_paragraph(tf_left, c, Pt(15), CLR_BLACK, space_before=Pt(8))

    # Right column: RQ Answers
    tf_right = add_textbox(slide, Inches(6.8), Inches(1.4), Inches(6), Inches(5.5),
                           "Research Question Answers", Pt(20), CLR_BLUE, bold=True)
    rqs = [
        ("RQ1:", "Classical ML is feasible (ROC-AUC 0.857)"),
        ("RQ2:", "Feature extension is task-dependent (+23 pp ReadText)"),
        ("RQ3:", "Class weighting provides no consistent benefit"),
        ("RQ4:", "Cross-dataset differences confounded"),
        ("RQ5:", "Spontaneous speech slightly stronger but task-specific"),
    ]
    for label, answer in rqs:
        p = add_paragraph(tf_right, f"{label} {answer}", Pt(14), CLR_BLACK, space_before=Pt(8))

    # Bottom message
    add_textbox(slide, Inches(0.5), Inches(6.3), Inches(12.3), Inches(0.8),
                "\"Voice-based PD classification is scientifically substantiated but not yet ready for clinical use.\"",
                Pt(16), CLR_ACCENT, bold=True, alignment=PP_ALIGN.CENTER)

    slide.notes_slide.notes_text_frame.text = (
        "Main message: voice-based PD classification is feasible with classical ML, "
        "but methodological rigor matters more than model sophistication. "
        "This work provides a transparent, reproducible baseline."
    )

    # -----------------------------------------------------------------------
    # SLIDE 26: FUTURE WORK & THANK YOU
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide, CLR_DARK_BLUE)

    add_textbox(slide, Inches(1), Inches(0.5), Inches(11.333), Inches(0.8),
                "Future Work", Pt(32), CLR_WHITE, bold=True)

    # Decorative line
    line = slide.shapes.add_shape(
        1, Inches(1), Inches(1.3), Inches(11.333), Inches(0.03)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = CLR_ACCENT
    line.line.fill.background()

    # Three columns
    for idx, (title, items) in enumerate([
        ("Short-term", [
            "Nested CV for hyperparameter tuning",
            "Feature selection (RFE, L1)",
            "Multi-task fusion (Read + Spontaneous)",
        ]),
        ("Medium-term", [
            "External validation on independent cohorts",
            "Deep learning comparison (with regularization)",
            "Longitudinal disease progression tracking",
        ]),
        ("Long-term", [
            "Smartphone-based screening integration",
            "Multi-modal fusion (voice + gait + tremor)",
            "Formal clinical validation",
        ]),
    ]):
        col_left = Inches(0.5 + idx * 4.3)
        tf = add_textbox(slide, col_left, Inches(1.6), Inches(3.8), Inches(0.5),
                         title, Pt(20), CLR_ACCENT, bold=True)
        tf_items = add_textbox(slide, col_left, Inches(2.3), Inches(3.8), Inches(2.5),
                               "", Pt(15), CLR_WHITE)
        first = True
        for item in items:
            if first:
                tf_items.paragraphs[0].text = f"• {item}"
                tf_items.paragraphs[0].font.size = Pt(15)
                tf_items.paragraphs[0].font.color.rgb = CLR_WHITE
                tf_items.paragraphs[0].font.name = "Calibri"
                tf_items.paragraphs[0].space_after = Pt(8)
                first = False
            else:
                add_paragraph(tf_items, f"• {item}", Pt(15), CLR_WHITE, space_before=Pt(6))

    # Thank you
    add_textbox(slide, Inches(1), Inches(5.3), Inches(11.333), Inches(0.8),
                "Thank You", Pt(36), CLR_WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)

    line2 = slide.shapes.add_shape(
        1, Inches(4), Inches(6.1), Inches(5.333), Inches(0.03)
    )
    line2.fill.solid()
    line2.fill.fore_color.rgb = CLR_ACCENT
    line2.line.fill.background()

    add_textbox(slide, Inches(1), Inches(6.3), Inches(11.333), Inches(0.5),
                "Questions?", Pt(24), CLR_LIGHT_BLUE,
                alignment=PP_ALIGN.CENTER)

    slide.notes_slide.notes_text_frame.text = (
        "The thesis concludes that voice-based PD classification is scientifically "
        "substantiated but not yet ready for clinical use. Open for questions."
    )

    # ===================================================================
    # BACKUP SLIDES
    # ===================================================================

    # -----------------------------------------------------------------------
    # BACKUP B1: FULL RESULTS C4 DATASET A
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_table_slide(slide,
        "Full Results — C4: Extended + Weighted (Dataset A)",
        ["Model", "Task", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC"],
        [
            ["LR", "ReadText", "73.2 ± 14.6", "0.63 ± 0.20", "0.78 ± 0.25", "0.67 ± 0.19", "0.698 ± 0.132"],
            ["SVM", "ReadText", "78.6 ± 10.8", "0.73 ± 0.15", "0.75 ± 0.25", "0.72 ± 0.16", "0.834 ± 0.153"],
            ["RF", "ReadText", "81.8 ± 14.0", "0.77 ± 0.18", "0.75 ± 0.25", "0.73 ± 0.21", "0.805 ± 0.182"],
            ["GB", "ReadText", "71.1 ± 14.8", "0.59 ± 0.18", "0.78 ± 0.25", "0.65 ± 0.18", "0.724 ± 0.214"],
            ["XGB", "ReadText", "77.1 ± 13.1", "0.67 ± 0.18", "0.78 ± 0.25", "0.70 ± 0.18", "0.794 ± 0.186"],
            ["LR", "Spont.", "69.3 ± 13.9", "0.61 ± 0.21", "0.70 ± 0.33", "0.59 ± 0.22", "0.783 ± 0.139"],
            ["SVM", "Spont.", "55.0 ± 17.7", "0.40 ± 0.21", "0.47 ± 0.42", "0.38 ± 0.30", "0.403 ± 0.347"],
            ["RF", "Spont.", "72.1 ± 20.3", "0.63 ± 0.28", "0.60 ± 0.42", "0.55 ± 0.32", "0.823 ± 0.209"],
            ["GB", "Spont.", "63.6 ± 10.1", "0.50 ± 0.11", "0.60 ± 0.22", "0.53 ± 0.15", "0.638 ± 0.146"],
            ["XGB", "Spont.", "61.4 ± 13.3", "0.45 ± 0.15", "0.47 ± 0.25", "0.43 ± 0.17", "0.687 ± 0.146"],
        ],
        col_widths=[0.6, 0.6, 0.9, 0.9, 0.8, 0.8, 1.0],
        note="Backup: Full C4 results for all 5 models across both Dataset A tasks."
    )

    # -----------------------------------------------------------------------
    # BACKUP B2: FULL RESULTS C4 DATASET B
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_table_slide(slide,
        "Full Results — C4: Extended + Weighted (Dataset B)",
        ["Model", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC"],
        [
            ["Logistic Regression", "0.805 ± 0.024", "0.862 ± 0.023", "0.875 ± 0.023", "0.868 ± 0.015", "0.867 ± 0.029"],
            ["SVM (RBF)", "0.839 ± 0.018", "0.891 ± 0.014", "0.889 ± 0.020", "0.890 ± 0.013", "0.900 ± 0.023"],
            ["Random Forest", "0.897 ± 0.016", "0.933 ± 0.011", "0.921 ± 0.017", "0.927 ± 0.012", "0.949 ± 0.012"],
            ["Gradient Boosting", "0.889 ± 0.020", "0.930 ± 0.014", "0.916 ± 0.019", "0.923 ± 0.014", "0.937 ± 0.019"],
            ["XGBoost", "0.900 ± 0.008", "0.935 ± 0.006", "0.925 ± 0.013", "0.930 ± 0.006", "0.952 ± 0.015"],
        ],
        col_widths=[1.2, 0.9, 0.9, 0.9, 0.9, 0.9],
        highlight_cells=[(4, 5)],
        note="Backup: Full results for Dataset B. XGBoost achieves best ROC-AUC 0.952."
    )

    # -----------------------------------------------------------------------
    # BACKUP B3: SVM COLLAPSE EXPLANATION
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_bullet_slide(slide,
        "SVM Collapse on SpontaneousDialogue",
        [
            "SVM (RBF) ROC-AUC drops to 0.407–0.460 on SpontaneousDialogue",
            "SVM is sensitive to curse of dimensionality at small n",
            "Spontaneous speech features have higher within-class variance",
            "At n=36, 47–78 features: margin-based boundary becomes unstable",
            "Expected behavior documented, not hidden",
        ],
        note="Use this slide if committee asks about the SVM anomaly. "
             "Key point: SVM-RBF collapses when feature-to-sample ratio is unfavorable "
             "AND the data has high within-class variance."
    )

    # -----------------------------------------------------------------------
    # BACKUP B4: DEMO APP
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide)
    title_shape = slide.shapes.add_shape(
        1, Inches(0), Inches(0), SLIDE_WIDTH, Inches(1.1)
    )
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = CLR_DARK_BLUE
    title_shape.line.fill.background()
    tf_t = title_shape.text_frame
    tf_t.margin_left = Inches(0.5)
    tf_t.margin_top = Inches(0.15)
    p = tf_t.paragraphs[0]
    p.text = "Demo Application — Research Prototype"
    p.font.size = Pt(26)
    p.font.color.rgb = CLR_WHITE
    p.font.bold = True
    p.font.name = "Calibri"

    # Architecture diagram
    arch_fig = ensure_figure("webapp-architecture.png")
    if arch_fig:
        pic = slide.shapes.add_picture(str(arch_fig), Inches(0.3), Inches(1.3),
                                       width=Inches(5.5))
        fig_ref, fig_caption = infer_figure_ref_and_caption("webapp-architecture.png")
        add_figure_legend(
            slide,
            pic.left,
            min(pic.top + pic.height + Inches(0.06), Inches(6.4)),
            pic.width,
            caption=fig_caption,
            ref=fig_ref,
        )

    # Screenshots
    for idx, (fn, cap) in enumerate([
        ("fig_demo_upload_audio.png", "Upload interface"),
        ("fig_demo_analysis_result.png", "Analysis result"),
    ]):
        fig_path = ensure_figure(fn)
        if fig_path:
            try:
                pic = slide.shapes.add_picture(str(fig_path), Inches(6.5 + idx * 3.3), Inches(1.3),
                                               width=Inches(3.0))
                ratio = pic.height / pic.width
                pic.height = int(Inches(3.0) * ratio)
                if pic.height > Inches(5.0):
                    pic.height = Inches(5.0)
                fig_ref, mapped_caption = infer_figure_ref_and_caption(fn)
                add_figure_legend(
                    slide,
                    pic.left,
                    min(pic.top + pic.height + Inches(0.06), Inches(6.4)),
                    pic.width,
                    caption=cap if cap else mapped_caption,
                    ref=fig_ref,
                )
            except Exception:
                pass

    # Disclaimer
    add_textbox(slide, Inches(0.5), Inches(6.8), Inches(12.3), Inches(0.5),
                "⚠ Research Demonstration Only — Not for clinical use",
                Pt(14), CLR_RED, bold=True, alignment=PP_ALIGN.CENTER)

    slide.notes_slide.notes_text_frame.text = (
        "Flask web app wrapping the trained RF model. "
        "Accepts audio upload or microphone recording. "
        "Extracts features → runs inference → displays result with confidence. "
        "Research prototype for thesis defense demonstration only."
    )

    # -----------------------------------------------------------------------
    # BACKUP B5: ROC-AUC all conditions (ReadText)
    # -----------------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_table_slide(slide,
        "Full ROC-AUC — Dataset A ReadText (All Conditions)",
        ["Model", "C1 (47, unw)", "C2 (47, wt)", "C3 (78, unw)", "C4 (78, wt)"],
        [
            ["Logistic Reg.", "0.717 ± 0.139", "0.717 ± 0.139", "0.698 ± 0.132", "0.698 ± 0.132"],
            ["SVM (RBF)", "0.614 ± 0.312", "0.542 ± 0.312", "0.834 ± 0.153", "0.834 ± 0.153"],
            ["Random Forest", "0.590 ± 0.302", "0.687 ± 0.258", "0.822 ± 0.166", "0.805 ± 0.182"],
            ["Gradient Boost", "0.500 ± 0.159", "0.500 ± 0.159", "0.724 ± 0.214", "0.724 ± 0.214"],
            ["XGBoost", "0.628 ± 0.203", "0.628 ± 0.203", "0.794 ± 0.186", "0.794 ± 0.186"],
        ],
        col_widths=[1.1, 1, 1, 1, 1],
        highlight_cells=[(1, 3), (2, 3)],
        note="Full ReadText ROC-AUC table across all 4 conditions. "
             "Shows C1→C3 improvement clearly for SVM, RF, GB."
    )

    # -----------------------------------------------------------------------
    # Save
    # -----------------------------------------------------------------------
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    prs.save(str(PPTX_OUT))
    print(f"✅ Presentation saved to: {PPTX_OUT}")
    print(f"   Total slides: {len(prs.slides)} (26 main + 5 backup)")


if __name__ == "__main__":
    build_presentation()
