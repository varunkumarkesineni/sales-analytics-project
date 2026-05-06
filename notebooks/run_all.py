"""
RUN ALL SCRIPTS IN ORDER
=========================
Run this single file to execute the entire pipeline end-to-end.

Usage:
    python notebooks/run_all.py
"""

import subprocess, sys, os

scripts = [
    ("01_data_cleaning.py",   "Step 1: Data Cleaning"),
    ("02_kpi_analysis.py",    "Step 2: KPI Analysis"),
    ("03_rfm_segmentation.py","Step 3: RFM Segmentation"),
    ("04_cohort_analysis.py", "Step 4: Cohort Analysis"),
    ("05_churn_prediction.py","Step 5: Churn Prediction"),
]

print("=" * 55)
print("   SALES ANALYTICS PROJECT — Full Pipeline Run")
print("=" * 55)

for script, label in scripts:
    print(f"\n{'='*55}")
    print(f"  🚀 {label}")
    print(f"{'='*55}")
    result = subprocess.run(
        [sys.executable, os.path.join("notebooks", script)],
        capture_output=False
    )
    if result.returncode != 0:
        print(f"❌ {script} failed. Fix errors above and retry.")
        sys.exit(1)

print("\n" + "="*55)
print("  ✅ ALL STEPS COMPLETE!")
print("  📁 Check outputs/ folder for all results")
print("  📊 Check outputs/charts/ for all visualizations")
print("="*55)
