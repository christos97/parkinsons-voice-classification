#!/usr/bin/env python
"""
Experiment Runner

Runs all classification experiments:
1. Dataset A - ReadText (grouped CV)
2. Dataset A - SpontaneousDialogue (grouped CV)
3. Dataset B - Pre-extracted features (standard CV)

Saves results to outputs/results/
"""

import pandas as pd

from parkinsons_voice_classification.data.mdvr_kcl import load_features as load_mdvr_features
from parkinsons_voice_classification.data.pd_speech import load_features as load_pd_speech_features
from parkinsons_voice_classification.models.training import run_cv, summarize_results
from parkinsons_voice_classification.config import OUTPUTS_DIR


def main():
    """Run experiments on all datasets."""
    
    results_dir = OUTPUTS_DIR / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    all_results = []
    
    print("=" * 70)
    print("PARKINSON'S DISEASE VOICE CLASSIFICATION EXPERIMENTS")
    print("=" * 70)
    
    # =========================================================================
    # Experiment 1: Dataset A - ReadText
    # =========================================================================
    print("\n[1/3] Dataset A - ReadText (Grouped Stratified 5-Fold CV)")
    print("-" * 70)
    
    try:
        X, y, groups = load_mdvr_features("ReadText")
        print(f"  Loaded: {X.shape[0]} samples, {X.shape[1]} features")
        print(f"  Subjects: {len(set(groups))}, HC: {(y==0).sum()}, PD: {(y==1).sum()}")
        
        results_a1 = run_cv(X, y, groups=groups, use_groups=True)
        results_a1['dataset'] = 'MDVR-KCL'
        results_a1['task'] = 'ReadText'
        all_results.append(results_a1)
        
        summary = summarize_results(results_a1)
        print("\n  Results:")
        for model in summary['model'].unique():
            print(f"\n  {model}:")
            model_summary = summary[summary['model'] == model]
            for _, row in model_summary.iterrows():
                print(f"    {row['metric']:12s}: {row['mean_std']}")
    except FileNotFoundError as e:
        print(f"  ⚠ Skipped: {e}")
    
    # =========================================================================
    # Experiment 2: Dataset A - SpontaneousDialogue
    # =========================================================================
    print("\n[2/3] Dataset A - SpontaneousDialogue (Grouped Stratified 5-Fold CV)")
    print("-" * 70)
    
    try:
        X, y, groups = load_mdvr_features("SpontaneousDialogue")
        print(f"  Loaded: {X.shape[0]} samples, {X.shape[1]} features")
        print(f"  Subjects: {len(set(groups))}, HC: {(y==0).sum()}, PD: {(y==1).sum()}")
        
        results_a2 = run_cv(X, y, groups=groups, use_groups=True)
        results_a2['dataset'] = 'MDVR-KCL'
        results_a2['task'] = 'SpontaneousDialogue'
        all_results.append(results_a2)
        
        summary = summarize_results(results_a2)
        print("\n  Results:")
        for model in summary['model'].unique():
            print(f"\n  {model}:")
            model_summary = summary[summary['model'] == model]
            for _, row in model_summary.iterrows():
                print(f"    {row['metric']:12s}: {row['mean_std']}")
    except FileNotFoundError as e:
        print(f"  ⚠ Skipped: {e}")
    
    # =========================================================================
    # Experiment 3: Dataset B - Pre-extracted features
    # =========================================================================
    print("\n[3/3] Dataset B - PD_SPEECH_FEATURES (Stratified 5-Fold CV)")
    print("-" * 70)
    
    X, y = load_pd_speech_features()
    print(f"  Loaded: {X.shape[0]} samples, {X.shape[1]} features")
    print(f"  HC: {(y==0).sum()}, PD: {(y==1).sum()}")
    
    results_b = run_cv(X, y, use_groups=False)
    results_b['dataset'] = 'PD_SPEECH_FEATURES'
    results_b['task'] = 'N/A'
    all_results.append(results_b)
    
    summary = summarize_results(results_b)
    print("\n  Results:")
    for model in summary['model'].unique():
        print(f"\n  {model}:")
        model_summary = summary[summary['model'] == model]
        for _, row in model_summary.iterrows():
            print(f"    {row['metric']:12s}: {row['mean_std']}")
    
    # =========================================================================
    # Save all results
    # =========================================================================
    if all_results:
        combined = pd.concat(all_results, ignore_index=True)
        results_path = results_dir / "all_results.csv"
        combined.to_csv(results_path, index=False)
        print(f"\n\nResults saved to: {results_path}")
        
        # Also save summary
        summary_path = results_dir / "summary.csv"
        full_summary = summarize_results(combined)
        full_summary.to_csv(summary_path, index=False)
        print(f"Summary saved to: {summary_path}")
    
    print("\n" + "=" * 70)
    print("All experiments complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
