#!/usr/bin/env python3
"""Generate 5-Slide RQ Answers PowerPoint Presentation.

Creates a focused 5-slide presentation answering RQ1–RQ5 for the MSc thesis
defense on "Voice-Based Classification of Parkinson's Disease Using Classical ML".

Usage:
    poetry run python scripts/generate_rq_slides.py
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.chart.data import ChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
import lxml.etree as etree

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "outputs"
PPTX_OUT = OUTPUT_DIR / "rq_slides.pptx"

# Slide dimensions (16:9 widescreen)
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# ---------------------------------------------------------------------------
# Color Palette (consistent with main defense presentation)
# ---------------------------------------------------------------------------
CLR_DARK_BLUE = RGBColor(0x00, 0x2B, 0x5C)
CLR_BLUE = RGBColor(0x00, 0x56, 0xA0)
CLR_LIGHT_BLUE = RGBColor(0xD6, 0xE8, 0xF7)
CLR_ACCENT = RGBColor(0xE8, 0x6C, 0x00)
CLR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CLR_BLACK = RGBColor(0x1A, 0x1A, 0x1A)
CLR_GRAY = RGBColor(0x66, 0x66, 0x66)
CLR_LIGHT_GRAY = RGBColor(0xF2, 0xF2, 0xF2)
CLR_GREEN = RGBColor(0x2E, 0x7D, 0x32)
CLR_RED = RGBColor(0xC6, 0x28, 0x28)
CLR_BG = RGBColor(0xF8, 0xFB, 0xFF)
CLR_TITLE_LINE = RGBColor(0x3B, 0x82, 0xF6)
CLR_ANSWER = RGBColor(0x00, 0x56, 0xA0)  # answer box back
CLR_ANSWER_TEXT = RGBColor(0xFF, 0xFF, 0xFF)
CLR_CAVEAT = RGBColor(0xFF, 0xF3, 0xE0)  # warm yellow for caveat
CLR_CAVEAT_BORDER = RGBColor(0xE8, 0x6C, 0x00)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def set_slide_bg(slide, color: RGBColor = CLR_BG) -> None:
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_title_bar(slide, title: str, font_size: int = 27) -> None:
    """Render the standard dark-blue title bar at top of slide."""
    bar = slide.shapes.add_shape(1, Inches(0), Inches(0), SLIDE_WIDTH, Inches(1.05))
    bar.fill.solid()
    bar.fill.fore_color.rgb = CLR_DARK_BLUE
    bar.line.fill.background()

    accent = slide.shapes.add_shape(1, Inches(0), Inches(1.03), SLIDE_WIDTH, Inches(0.025))
    accent.fill.solid()
    accent.fill.fore_color.rgb = CLR_TITLE_LINE
    accent.line.fill.background()

    tf = bar.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.5)
    tf.margin_top = Inches(0.12)
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(font_size)
    p.font.color.rgb = CLR_WHITE
    p.font.bold = True
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.LEFT


def add_footer(slide) -> None:
    line = slide.shapes.add_shape(1, Inches(0.5), Inches(7.06), Inches(12.3), Inches(0.01))
    line.fill.solid()
    line.fill.fore_color.rgb = CLR_ACCENT
    line.line.fill.background()
    txb = slide.shapes.add_textbox(Inches(0.5), Inches(7.10), Inches(12.3), Inches(0.24))
    tf = txb.text_frame
    p = tf.paragraphs[0]
    p.text = "Διπλωματική Εργασία — Μάρτιος 2026"
    p.font.size = Pt(9)
    p.font.color.rgb = CLR_ACCENT
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.RIGHT


def add_textbox(slide, left, top, width, height, text="", font_size=Pt(16),
                font_color=CLR_BLACK, bold=False, alignment=PP_ALIGN.LEFT,
                font_name="Calibri", italic=False):
    txb = slide.shapes.add_textbox(left, top, width, height)
    tf = txb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = font_size
    p.font.color.rgb = font_color
    p.font.bold = bold
    p.font.italic = italic
    p.font.name = font_name
    p.alignment = alignment
    return tf


def add_paragraph(tf, text, font_size=Pt(15), font_color=CLR_BLACK, bold=False,
                  alignment=PP_ALIGN.LEFT, space_before=Pt(4), level=0,
                  font_name="Calibri", italic=False):
    p = tf.add_paragraph()
    p.text = text
    p.font.size = font_size
    p.font.color.rgb = font_color
    p.font.bold = bold
    p.font.italic = italic
    p.font.name = font_name
    p.alignment = alignment
    p.space_before = space_before
    p.level = level
    return p


def add_answer_box(slide, left, top, width, answer_text: str) -> None:
    """Render a highlighted 'Answer' box."""
    box = slide.shapes.add_shape(1, left, top, width, Inches(0.62))
    box.fill.solid()
    box.fill.fore_color.rgb = CLR_BLUE
    # border
    box.line.color.rgb = CLR_DARK_BLUE
    box.line.width = Pt(1.5)

    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.18)
    tf.margin_top = Inches(0.06)
    tf.margin_right = Inches(0.1)
    p = tf.paragraphs[0]
    p.font.size = Pt(14)
    p.font.color.rgb = CLR_WHITE
    p.font.bold = True
    p.font.name = "Calibri"
    p.text = answer_text
    p.alignment = PP_ALIGN.LEFT


def add_caveat_box(slide, left, top, width, height, caveat_text: str) -> None:
    """Render an orange-bordered caveat box."""
    box = slide.shapes.add_shape(1, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = CLR_CAVEAT
    box.line.color.rgb = CLR_CAVEAT_BORDER
    box.line.width = Pt(1.5)

    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_top = Inches(0.05)
    tf.margin_right = Inches(0.1)
    p = tf.paragraphs[0]
    p.font.size = Pt(12.5)
    p.font.color.rgb = CLR_BLACK
    p.font.bold = True
    p.font.italic = False
    p.font.name = "Calibri"
    p.text = caveat_text
    p.alignment = PP_ALIGN.LEFT


def add_table(slide, left, top, width, headers, rows,
              col_widths=None, highlight_cells=None, font_size=12,
              header_color=CLR_BLUE):
    """Add a data table to the slide."""
    n_rows = len(rows) + 1
    n_cols = len(headers)
    height = Inches(0.38) * n_rows

    if col_widths:
        total = sum(col_widths)
        actual_widths = [int(w / total * width) for w in col_widths]
    else:
        actual_widths = [width // n_cols] * n_cols

    tbl_shape = slide.shapes.add_table(n_rows, n_cols, left, top, width, height)
    tbl = tbl_shape.table

    for i, w in enumerate(actual_widths):
        tbl.columns[i].width = w

    highlight_cells = highlight_cells or []

    for j, hdr in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.text = hdr
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_color
        for para in cell.text_frame.paragraphs:
            para.font.size = Pt(font_size)
            para.font.color.rgb = CLR_WHITE
            para.font.bold = True
            para.font.name = "Calibri"
            para.alignment = PP_ALIGN.CENTER
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    for i, row_data in enumerate(rows):
        for j, val in enumerate(row_data):
            cell = tbl.cell(i + 1, j)
            cell.text = val
            if i % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = CLR_LIGHT_GRAY
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = CLR_WHITE
            for para in cell.text_frame.paragraphs:
                para.font.size = Pt(font_size)
                para.font.name = "Calibri"
                para.alignment = PP_ALIGN.CENTER
                if (i, j) in highlight_cells:
                    para.font.bold = True
                    para.font.color.rgb = CLR_ACCENT
                else:
                    para.font.color.rgb = CLR_BLACK
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    return tbl_shape


def add_bar_chart(slide, left, top, width, height,
                  categories, series_data, title="", y_min=0.0, y_max=1.0):
    """Add a grouped bar chart."""
    chart_data = ChartData()
    chart_data.categories = categories
    for series_name, values in series_data:
        chart_data.add_series(series_name, values)

    chart_shape = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED, left, top, width, height, chart_data
    )
    chart = chart_shape.chart
    chart.has_title = bool(title)
    if title:
        chart.chart_title.text_frame.text = title
        chart.chart_title.text_frame.paragraphs[0].font.size = Pt(11)

    chart.has_legend = len(series_data) > 1
    if chart.has_legend:
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False

    # Y-axis bounds
    va = chart.value_axis
    va.minimum_scale = y_min
    va.maximum_scale = y_max
    va.major_unit = 0.1
    va.has_major_gridlines = True

    # Series colors
    palette = [CLR_BLUE, CLR_ACCENT, CLR_GREEN, CLR_RED, CLR_DARK_BLUE]
    for i, series in enumerate(chart.series):
        series.format.fill.solid()
        series.format.fill.fore_color.rgb = palette[i % len(palette)]

    return chart_shape


# ---------------------------------------------------------------------------
# Slide 1 — RQ1: Classical ML Performance
# ---------------------------------------------------------------------------
def build_rq1(prs: Presentation) -> None:
    slide_layout = prs.slide_layouts[6]  # blank
    slide = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide)
    add_title_bar(slide, "RQ1 — Πόσο καλά αποδίδουν τα κλασικά ML μοντέλα;")

    # ---- Left column: bullet summary ----
    tf = add_textbox(slide, Inches(0.5), Inches(1.2), Inches(5.8), Inches(4.5),
                     font_size=Pt(14.5))
    tf.paragraphs[0].text = ""

    bullets = [
        ("Κλασική ML → διαχωρισμός PD/HC πάνω από τυχαίο επίπεδο", False),
        ("Dataset A (subject-level CV):", True),
        ("  Best ROC-AUC: 0.857 ± 0.171  (RF, Spontaneous, ext)", False),
        ("  Best ROC-AUC: 0.834 ± 0.153  (SVM, ReadText, ext)", False),
        ("  Υψηλή διακύμανση ανά fold — αβεβαιότητα εκτίμησης", False),
        ("Dataset B (pre-extracted, no subject IDs):", True),
        ("  ROC-AUC ≈ 0.94–0.95 — ενδεχομένως αισιόδοξη εκτίμηση", False),
        ("  (άγνωστη επικάλυψη υποκειμένων μεταξύ train/test)", False),
        ("LR παρέχει ισχυρή baseline σε Dataset A (0.717–0.783)", False),
    ]

    first = True
    for text, bold in bullets:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.text = text
        p.font.size = Pt(13.5)
        p.font.bold = bold
        p.font.color.rgb = CLR_DARK_BLUE if bold else CLR_BLACK
        p.font.name = "Calibri"
        p.space_before = Pt(4 if bold else 2)
        p.level = 0

    # Answer box
    add_answer_box(
        slide, Inches(0.5), Inches(5.85), Inches(5.8),
        "Απάντηση RQ1: Η κλασική ML είναι βιώσιμη baseline — "
        "ROC-AUC 0.83–0.86 (Dataset A) με αβεβαιότητα, ≥ 0.94 (Dataset B) "
        "με επιφύλαξη."
    )

    # ---- Right: summary table (best per dataset/task) ----
    tbl_left = Inches(6.6)
    tbl_top = Inches(1.25)
    tbl_width = Inches(6.45)

    headers = ["Dataset / Task", "Best Model", "ROC-AUC (mean ± std)"]
    rows = [
        ["A · ReadText (ext)", "SVM RBF", "0.834 ± 0.153"],
        ["A · Spontaneous (ext)", "RF", "0.857 ± 0.171"],
        ["A · ReadText (base)", "LR", "0.717 ± 0.139"],
        ["A · Spontaneous (base)", "RF", "0.828 ± 0.148"],
        ["B · PD Speech (base)", "XGBoost", "0.952 ± 0.015"],
        ["B · PD Speech (base)", "RF", "0.940 ± 0.013"],
    ]
    col_widths = [3.2, 2.0, 2.8]
    highlight = [(0, 2), (1, 2), (4, 2), (5, 2)]

    add_table(slide, tbl_left, tbl_top, tbl_width,
              headers, rows, col_widths=col_widths,
              highlight_cells=highlight, font_size=12)

    # legend
    leg = slide.shapes.add_textbox(tbl_left, Inches(1.25) + Inches(0.38) * 7 + Inches(0.08),
                                   tbl_width, Inches(0.28))
    ltf = leg.text_frame
    lp = ltf.paragraphs[0]
    lp.text = ("tab:best-results-summary  |  ext = 78 features, base = 47 features  "
               "|  Source: thesis results")
    lp.font.size = Pt(9.5)
    lp.font.color.rgb = CLR_GRAY
    lp.font.name = "Calibri"
    lp.alignment = PP_ALIGN.CENTER

    add_footer(slide)


# ---------------------------------------------------------------------------
# Slide 2 — RQ2: Feature Extension 47→78
# ---------------------------------------------------------------------------
def build_rq2(prs: Presentation) -> None:
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide)
    add_title_bar(slide, "RQ2 — Βελτιώνει η επέκταση χαρακτηριστικών (47→78) την απόδοση;")

    # Left: bullets
    tf = add_textbox(slide, Inches(0.5), Inches(1.2), Inches(5.8), Inches(4.5),
                     font_size=Pt(14))
    tf.paragraphs[0].text = ""

    bullets = [
        ("ReadText: σαφής βελτίωση με 78 features", True),
        ("  RF: 0.590 → 0.822  (Δ = +0.232)", False),
        ("  SVM: 0.614 → 0.834  (Δ = +0.220)", False),
        ("  GB:  0.500 → 0.724  (Δ = +0.224)", False),
        ("SpontaneousDialogue: μικρή / ασταθής επίδραση", True),
        ("  RF: 0.828 → 0.857  (Δ = +0.029)", False),
        ("  SVM: 0.407 → 0.460  (Δ = +0.053, υψ. std)", False),
        ("  XGB: 0.723 → 0.687  (Δ = −0.036)", False),
        ("Το αποτέλεσμα είναι task-dependent", False),
        ("Επέκταση ≠ καθολική βελτίωση", False),
    ]

    first = True
    for text, bold in bullets:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.text = text
        p.font.size = Pt(13.5)
        p.font.bold = bold
        p.font.color.rgb = CLR_DARK_BLUE if bold else CLR_BLACK
        p.font.name = "Calibri"
        p.space_before = Pt(4 if bold else 2)
        p.level = 0

    add_answer_box(
        slide, Inches(0.5), Inches(5.85), Inches(5.8),
        "Απάντηση RQ2: Ναι, κυρίως στο ReadText (Δ ROC-AUC ≈ +0.20–0.23). "
        "Στο SpontaneousDialogue η επίδραση είναι μικρή ή μη-σταθερή."
    )

    # Right: Δ ROC-AUC table (baseline → extended, unweighted)
    tbl_left = Inches(6.6)
    tbl_top = Inches(1.25)
    tbl_width = Inches(6.45)

    headers = ["Model", "ReadText\nbase→ext (Δ)", "Spontaneous\nbase→ext (Δ)"]
    rows = [
        ["LogisticRegression", "0.717 → 0.698  (−0.019)", "0.760 → 0.783  (+0.023)"],
        ["RandomForest",       "0.590 → 0.822  (+0.232)", "0.828 → 0.857  (+0.029)"],
        ["SVM RBF",            "0.614 → 0.834  (+0.220)", "0.407 → 0.460  (+0.053)"],
        ["GradientBoosting",   "0.500 → 0.724  (+0.224)", "0.615 → 0.638  (+0.023)"],
        ["XGBoost",            "0.628 → 0.794  (+0.166)", "0.723 → 0.687  (−0.036)"],
    ]
    col_widths = [2.5, 2.5, 2.5]
    # Highlight clearly positive ReadText deltas
    highlight = [(1, 1), (2, 1), (3, 1), (4, 1)]
    add_table(slide, tbl_left, tbl_top, tbl_width,
              headers, rows, col_widths=col_widths,
              highlight_cells=highlight, font_size=11.5)

    leg = slide.shapes.add_textbox(tbl_left, Inches(1.25) + Inches(0.38) * 6 + Inches(0.08),
                                   tbl_width, Inches(0.28))
    ltf = leg.text_frame
    lp = ltf.paragraphs[0]
    lp.text = ("tab:ablation-main  |  Δ ROC-AUC = extended − baseline (C3 − C1), unweighted  "
               "|  Source: thesis results")
    lp.font.size = Pt(9.5)
    lp.font.color.rgb = CLR_GRAY
    lp.font.name = "Calibri"
    lp.alignment = PP_ALIGN.CENTER

    add_footer(slide)


# ---------------------------------------------------------------------------
# Slide 3 — RQ3: Class Weighting
# ---------------------------------------------------------------------------
def build_rq3(prs: Presentation) -> None:
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide)
    add_title_bar(slide, "RQ3 — Βοηθά το class weighting σε ανισορροπία κλάσεων;")

    # Left bullets
    tf = add_textbox(slide, Inches(0.5), Inches(1.2), Inches(5.8), Inches(4.5),
                     font_size=Pt(14))
    tf.paragraphs[0].text = ""

    bullets = [
        ("Ελέγχθηκε: unweighted vs balanced, όλα μοντέλα/σενάρια", False),
        ("Dataset A ανισορροπία ≈ 1.3:1  (HC > PD)", False),
        ("ReadText (ext): weighting ≠ σταθερό κέρδος", True),
        ("  RF: 0.822 → 0.805  (−0.017)", False),
        ("  SVM: 0.834 → 0.834  (0.000)", False),
        ("  GB:  0.724 → 0.724  (0.000)", False),
        ("Spontaneous (ext): αντίστοιχα ουδέτερο ή αρνητικό", True),
        ("  RF: 0.857 → 0.823  (−0.034)", False),
        ("  LR: 0.783 → 0.783  (0.000)", False),
        ("Dataset B: μικρή ουδέτερη/θετική επίδραση  (RF +0.009)", False),
        ("Για 1.3:1 class ratio → weighting δεν φαίνεται αναγκαίο", False),
    ]

    first = True
    for text, bold in bullets:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.text = text
        p.font.size = Pt(13)
        p.font.bold = bold
        p.font.color.rgb = CLR_DARK_BLUE if bold else CLR_BLACK
        p.font.name = "Calibri"
        p.space_before = Pt(4 if bold else 1)
        p.level = 0

    add_answer_box(
        slide, Inches(0.5), Inches(5.85), Inches(5.8),
        "Απάντηση RQ3: Δεν παρατηρείται σταθερό κέρδος από balanced class weighting. "
        "Για ανισορροπία ~1.3:1, η επίδραση είναι ουδέτερη ή ελαφρά αρνητική."
    )

    # Right: weighting comparison table (RF as primary model)
    tbl_left = Inches(6.6)
    tbl_top = Inches(1.25)
    tbl_width = Inches(6.45)

    headers = ["Task / Feature set", "Unweighted\nROC-AUC", "Weighted\nROC-AUC", "Δ"]
    rows = [
        ["ReadText · baseline",      "0.590 ± 0.302", "0.687 ± 0.258", "+0.097"],
        ["ReadText · extended",      "0.822 ± 0.166", "0.805 ± 0.182", "−0.017"],
        ["Spontaneous · baseline",   "0.828 ± 0.148", "0.827 ± 0.133", "−0.001"],
        ["Spontaneous · extended",   "0.857 ± 0.171", "0.823 ± 0.209", "−0.034"],
        ["Dataset B · baseline",     "0.940 ± 0.013", "0.949 ± 0.012", "+0.009"],
        ["Dataset B · extended",     "0.940 ± 0.013", "0.949 ± 0.012", "+0.009"],
    ]
    col_widths = [2.8, 1.8, 1.8, 0.8]
    # Highlight negative Δ cells to show no consistent benefit
    highlight_neg = [(1, 3), (3, 3)]
    add_table(slide, tbl_left, tbl_top, tbl_width,
              headers, rows, col_widths=col_widths,
              highlight_cells=highlight_neg, font_size=11.5)

    # Sub-label: model
    sub = slide.shapes.add_textbox(tbl_left, Inches(1.25) + Inches(0.38) * 0 - Inches(0.05),
                                   tbl_width, Inches(0.25))
    stf = sub.text_frame
    sp = stf.paragraphs[0]
    sp.text = "Μοντέλο: Random Forest"
    sp.font.size = Pt(10)
    sp.font.color.rgb = CLR_GRAY
    sp.font.italic = True
    sp.font.name = "Calibri"
    sp.alignment = PP_ALIGN.RIGHT

    leg = slide.shapes.add_textbox(tbl_left, Inches(1.25) + Inches(0.38) * 7 + Inches(0.08),
                                   tbl_width, Inches(0.28))
    ltf = leg.text_frame
    lp = ltf.paragraphs[0]
    lp.text = ("tab:weighting-main  |  Unweighted = C1/C3, Weighted = C2/C4  "
               "|  Source: thesis results")
    lp.font.size = Pt(9.5)
    lp.font.color.rgb = CLR_GRAY
    lp.font.name = "Calibri"
    lp.alignment = PP_ALIGN.CENTER

    add_footer(slide)


# ---------------------------------------------------------------------------
# Slide 4 — RQ4: Subject-level CV vs Standard CV
# ---------------------------------------------------------------------------
def build_rq4(prs: Presentation) -> None:
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide)
    add_title_bar(slide, "RQ4 — Διαφέρει η εκτίμηση μεταξύ Subject-Level CV (A) και Standard CV (B);")

    # Left: bullets
    tf = add_textbox(slide, Inches(0.5), Inches(1.18), Inches(5.8), Inches(4.7),
                     font_size=Pt(14))
    tf.paragraphs[0].text = ""

    bullets = [
        ("Dataset A — Grouped Stratified 5-Fold (CV ανά υποκείμενο):", True),
        ("  Πιο συντηρητικές εκτιμήσεις ROC-AUC", False),
        ("  Μεγαλύτερη διακύμανση (std ≈ 0.13–0.31)", False),
        ("  Αντικατοπτρίζει πραγματική γενίκευση σε νέα υποκείμενα", False),
        ("Dataset B — Stratified 5-Fold (χωρίς subject IDs):", True),
        ("  Υψηλότερες εκτιμήσεις (XGB: 0.952 ± 0.015)", False),
        ("  Πολύ μικρότερη διακύμανση (std ≈ 0.01–0.03)", False),
        ("  Πιθανή διαρροή λόγω άγνωστης επικάλυψης υποκειμένων", False),
        ("⚠ Η σύγκριση A vs B είναι confounded:", False),
        ("  Διαφορετικό n, task, features, CV στρατηγική", False),
        ("  Δεν αποδίδεται διαφορά σε έναν μόνο παράγοντα", False),
    ]

    first = True
    for text, bold in bullets:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.text = text
        p.font.size = Pt(13)
        p.font.bold = bold
        p.font.color.rgb = CLR_DARK_BLUE if bold else CLR_BLACK
        p.font.name = "Calibri"
        p.space_before = Pt(4 if bold else 1)
        p.level = 0

    add_answer_box(
        slide, Inches(0.5), Inches(5.85), Inches(5.8),
        "Απάντηση RQ4: Ναι, ουσιαστική διαφορά εκτίμησης. "
        "Τα αποτελέσματα Dataset B ερμηνεύονται με επιφύλαξη λόγω πολλαπλών "
        "συγχυτικών παραγόντων."
    )

    # Right: variance comparison table
    tbl_left = Inches(6.6)
    tbl_top = Inches(1.25)
    tbl_width = Inches(6.45)

    headers = ["Σενάριο", "Best ROC-AUC", "std", "CV Στρατηγική"]
    rows = [
        ["A · Read (base)",    "0.717",  "±0.139", "Grouped Stratified"],
        ["A · Read (ext)",     "0.834",  "±0.153", "Grouped Stratified"],
        ["A · Spont (base)",   "0.828",  "±0.148", "Grouped Stratified"],
        ["A · Spont (ext)",    "0.857",  "±0.171", "Grouped Stratified"],
        ["B · baseline",       "0.952",  "±0.015", "Stratified (no IDs)"],
        ["B · extended",       "0.952",  "±0.015", "Stratified (no IDs)"],
    ]
    col_widths = [2.2, 1.8, 1.0, 2.5]
    add_table(slide, tbl_left, tbl_top, tbl_width,
              headers, rows, col_widths=col_widths,
              highlight_cells=[(4, 1), (5, 1)], font_size=12)

    # Caveat box for Dataset B
    add_caveat_box(
        slide,
        tbl_left, Inches(1.25) + Inches(0.38) * 7 + Inches(0.15),
        tbl_width, Inches(0.7),
        "⚠ Dataset B: Subject IDs άγνωστα → πιθανή διαρροή "
        "train/test · Εκτιμήσεις ενδεχομένως αισιόδοξες"
    )

    add_footer(slide)


# ---------------------------------------------------------------------------
# Slide 5 — RQ5: Read Speech vs Spontaneous Speech
# ---------------------------------------------------------------------------
def build_rq5(prs: Presentation) -> None:
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide)
    add_title_bar(slide, "RQ5 — Διαφέρει η απόδοση μεταξύ Read Speech και Spontaneous Speech;")

    # Left: bullets
    tf = add_textbox(slide, Inches(0.5), Inches(1.18), Inches(5.9), Inches(4.7),
                     font_size=Pt(14))
    tf.paragraphs[0].text = ""

    bullets = [
        ("Και οι 2 εργασίες: χρήσιμη πληροφορία για PD/HC", False),
        ("Best ROC-AUC:", True),
        ("  ReadText (ext):      SVM 0.834 ± 0.153", False),
        ("  Spontaneous (ext):   RF  0.857 ± 0.171", False),
        ("  → Spontaneous οριακά ανώτερο (Δ ≈ +0.023)", False),
        ("Επέκταση 47→78 features:", True),
        ("  ReadText:      μεγάλη βελτίωση  (+0.22 SVM, +0.23 RF)", False),
        ("  Spontaneous:   μικρή / ασταθής  (+0.03 RF, −0.04 XGB)", False),
        ("ReadText ωφελείται περισσότερο από επέκταση features", False),
        ("Spontaneous φαίνεται πιο ανθεκτικό σε αλλαγές feature set", False),
        ("(πιο σταθερό LR/RF, ασταθές SVM ανεξαρτήτως feature set)", False),
    ]

    first = True
    for text, bold in bullets:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.text = text
        p.font.size = Pt(13)
        p.font.bold = bold
        p.font.color.rgb = CLR_DARK_BLUE if bold else CLR_BLACK
        p.font.name = "Calibri"
        p.space_before = Pt(4 if bold else 1)
        p.level = 0

    add_answer_box(
        slide, Inches(0.5), Inches(5.85), Inches(5.9),
        "Απάντηση RQ5: Ναι, διαφορές υπάρχουν. Spontaneous ≥ ReadText best ROC-AUC. "
        "ReadText ωφελείται σαφώς από feature expansion· Spontaneous πιο σταθερό."
    )

    # Right: side-by-side comparison table
    tbl_left = Inches(6.65)
    tbl_top = Inches(1.25)
    tbl_width = Inches(6.4)

    headers = ["Model", "ReadText\n47 feat.", "ReadText\n78 feat.", "Spont.\n47 feat.", "Spont.\n78 feat."]
    rows = [
        ["LogReg",  "0.717", "0.698", "0.760", "0.783"],
        ["RF",      "0.590", "0.822", "0.828", "0.857"],
        ["SVM RBF", "0.614", "0.834", "0.407", "0.460"],
        ["GradBoost","0.500","0.724", "0.615", "0.638"],
        ["XGBoost", "0.628", "0.794", "0.723", "0.687"],
    ]
    col_widths = [1.8, 1.2, 1.2, 1.2, 1.2]
    # Highlight best values: ReadText ext SVM (row2, col2), Spontaneous ext RF (row1, col3)
    highlight = [(1, 2), (1, 4), (2, 2)]
    add_table(slide, tbl_left, tbl_top, tbl_width,
              headers, rows, col_widths=col_widths,
              highlight_cells=highlight, font_size=12)

    leg = slide.shapes.add_textbox(tbl_left, Inches(1.25) + Inches(0.38) * 6 + Inches(0.1),
                                   tbl_width, Inches(0.28))
    ltf = leg.text_frame
    lp = ltf.paragraphs[0]
    lp.text = ("ROC-AUC mean per model (unweighted) — best per column highlighted  "
               "|  Source: thesis results")
    lp.font.size = Pt(9.5)
    lp.font.color.rgb = CLR_GRAY
    lp.font.name = "Calibri"
    lp.alignment = PP_ALIGN.CENTER

    # Small note about confounding
    add_caveat_box(
        slide,
        tbl_left, Inches(1.25) + Inches(0.38) * 6 + Inches(0.48),
        tbl_width, Inches(0.55),
        "⚠ ReadText n=37, SpontaneousDialogue n=36 subjects (Dataset A) — "
        "small N, wide CIs, interpret cautiously"
    )

    add_footer(slide)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    print("Building RQ slides…")
    build_rq1(prs)
    print("  [1/5] RQ1 — Classical ML Performance ✓")
    build_rq2(prs)
    print("  [2/5] RQ2 — Feature Extension Effect ✓")
    build_rq3(prs)
    print("  [3/5] RQ3 — Class Weighting ✓")
    build_rq4(prs)
    print("  [4/5] RQ4 — Subject-Level CV vs Standard CV ✓")
    build_rq5(prs)
    print("  [5/5] RQ5 — Read Speech vs Spontaneous Speech ✓")

    PPTX_OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(PPTX_OUT)
    print(f"\nSaved → {PPTX_OUT}")


if __name__ == "__main__":
    main()
