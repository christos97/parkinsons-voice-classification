import shutil
import os
from pathlib import Path
import sys

# =============================================================================
# FIGURE MAPPING CONFIGURATION
# Format: "Source Filename (in outputs/)" : "Destination Filename (in thesis/figures/)"
# AI AGENTS: EDIT THIS DICTIONARY to add or rename figures.
# =============================================================================

FIGURE_MAPPING = {
    # Dataset A Results
    "roc_curve_ReadText.pdf": "fig_roc_readtext.pdf",
    "roc_curve_SpontaneousDialogue.pdf": "fig_roc_spontaneous.pdf",
    "confusion_matrix_ReadText.pdf": "fig_confusion_readtext.pdf",
    
    # Dataset B Results
    "roc_curve_DatasetB.pdf": "fig_roc_dataset_b.pdf",
    
    # Feature Analysis - Heatmaps
    "heatmap_readtext.png": "fig_heatmap_readtext.png",
    "heatmap_spontaneous.png": "fig_heatmap_spontaneous.png",

    # Feature Importance - Main Body (RF)
    "importance_readtext_randomforest.png": "fig_imp_readtext_rf.png",
    "importance_spontaneous_randomforest.png": "fig_imp_spontaneous_rf.png",
    "importance_pd_speech_randomforest.png": "fig_imp_datasetb_rf.png",

    # Feature Importance - Appendix (LR & Categories)
    "importance_readtext_logisticregression.png": "fig_imp_readtext_lr.png",
    "importance_spontaneous_logisticregression.png": "fig_imp_spontaneous_lr.png",
    "importance_pd_speech_logisticregression.png": "fig_imp_datasetb_lr.png",
    "importance_readtext_categories.png": "fig_imp_readtext_cats.png",
    "importance_spontaneous_categories.png": "fig_imp_spontaneous_cats.png",

}

# =============================================================================
# SYNC LOGIC (DO NOT EDIT USUALLY)
# =============================================================================

SOURCE_ROOT = Path("outputs")
DEST_ROOT = Path("thesis/figures")

def find_file(filename, search_path):
    """Recursively find a file in search_path. Returns Path object or None."""
    matches = list(search_path.rglob(filename))
    if not matches:
        return None
    # If multiple copies exist, prefer the most recently modified one
    return max(matches, key=lambda p: p.stat().st_mtime)

def main():
    print(f"🔄 Syncing figures from '{SOURCE_ROOT}' to '{DEST_ROOT}'...")
    
    if not SOURCE_ROOT.exists():
        print(f"⚠️  Warning: Source directory '{SOURCE_ROOT}' not found. build pipeline first?")
        return

    # Ensure destination exists
    DEST_ROOT.mkdir(parents=True, exist_ok=True)
    
    synced_count = 0
    missing_count = 0
    
    for src_name, dest_name in FIGURE_MAPPING.items():
        src_path = find_file(src_name, SOURCE_ROOT)
        dest_path = DEST_ROOT / dest_name
        
        if src_path:
            try:
                shutil.copy2(src_path, dest_path)
                print(f"✅ Synced: {src_name} -> {dest_name}")
                synced_count += 1
            except Exception as e:
                print(f"❌ Error copying {src_name}: {e}")
        else:
            print(f"⚠️  Missing: {src_name} (expected in outputs/)")
            missing_count += 1
            
    print("-" * 40)
    print(f"Summary: {synced_count} synced, {missing_count} missing.")
    if missing_count > 0:
        print("Tip: Run 'make pipeline' to generate missing figures.")

if __name__ == "__main__":
    main()
