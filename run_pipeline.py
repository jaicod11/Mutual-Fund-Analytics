"""
run_pipeline.py — Master Execution Script
Bluestock MF Analytics | Capstone Project I

Runs the complete analytics pipeline end-to-end:
    Step 1: Data Cleaning     → data/processed/
    Step 2: Database Loading  → data/db/bluestock_mf.db
    Step 3: Live NAV Fetch    → data/raw/nav_*.csv
    Step 4: Recommender Test  → console output

Usage:
    python run_pipeline.py              # Run all steps
    python run_pipeline.py --step 1    # Run only step 1
    python run_pipeline.py --skip-nav  # Skip live NAV fetch
"""

import subprocess
import argparse
import sys
import time
from pathlib import Path


def run_step(name: str, script: str, description: str) -> bool:
    """Run a pipeline step and return success status."""
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"  {description}")
    print(f"{'='*60}")

    start = time.time()
    result = subprocess.run(
        [sys.executable, script],
        capture_output=False
    )
    elapsed = time.time() - start

    if result.returncode == 0:
        print(f"\n  ✅ {name} completed in {elapsed:.1f}s")
        return True
    else:
        print(f"\n  ❌ {name} FAILED (exit code {result.returncode})")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Bluestock MF Analytics — Master Pipeline Runner"
    )
    parser.add_argument("--step", type=int, choices=[1, 2, 3, 4],
                        help="Run only a specific step (1-4)")
    parser.add_argument("--skip-nav", action="store_true",
                        help="Skip live NAV fetch (requires internet)")
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  BLUESTOCK MF ANALYTICS — PIPELINE RUNNER")
    print("=" * 60)
    print("  Project: Capstone Project I — Mutual Fund Analytics")
    print("  Company: Bluestock Fintech | June 2026")
    print("=" * 60)

    # Verify we're in the project root
    if not Path("data").exists():
        print("❌ Error: Run this script from the project root directory")
        print("   Expected: data/, notebooks/, scripts/ folders to exist")
        sys.exit(1)

    steps = [
        (1, "STEP 1 — Data Cleaning",
         "scripts/data_cleaning.py",
         "Clean all 10 CSV datasets → data/processed/"),
        (2, "STEP 2 — Database Loading",
         "scripts/db_loader.py",
         "Load cleaned data into SQLite star schema → data/db/bluestock_mf.db"),
        (3, "STEP 3 — Live NAV Fetch",
         "scripts/live_nav_fetch.py",
         "Fetch latest NAV from mfapi.in for 6 key schemes"),
        (4, "STEP 4 — Fund Recommender",
         "scripts/recommender.py",
         "Run fund recommendations for Low / Moderate / High risk"),
    ]

    results = {}
    total_start = time.time()

    for step_num, name, script, description in steps:
        # Filter by --step if specified
        if args.step and step_num != args.step:
            continue
        # Skip NAV fetch if --skip-nav
        if args.skip_nav and step_num == 3:
            print(f"\n⏭️  Skipping {name} (--skip-nav flag)")
            continue
        # Check script exists
        if not Path(script).exists():
            print(f"\n⚠️  {name}: Script not found at {script} — skipping")
            results[step_num] = False
            continue

        success = run_step(name, script, description)
        results[step_num] = success

        if not success and step_num in [1, 2]:
            print(f"\n❌ Critical step failed. Stopping pipeline.")
            break

    # Summary
    total_elapsed = time.time() - total_start
    print(f"\n{'='*60}")
    print(f"  PIPELINE SUMMARY  ({total_elapsed:.1f}s total)")
    print(f"{'='*60}")
    for step_num, name, _, _ in steps:
        if step_num in results:
            status = "✅ PASSED" if results[step_num] else "❌ FAILED"
            print(f"  Step {step_num}: {status}")
        elif args.step and step_num != args.step:
            print(f"  Step {step_num}: ⏭️  SKIPPED (not selected)")
        else:
            print(f"  Step {step_num}: ⏭️  SKIPPED")

    all_passed = all(results.values()) if results else False
    print(f"\n  Overall: {'✅ ALL STEPS PASSED' if all_passed else '⚠️  SOME STEPS FAILED'}")
    print("=" * 60)

    if all_passed:
        print("\n🚀 Pipeline complete! You can now:")
        print("   → Open notebooks/ in Jupyter for analysis")
        print("   → Open dashboard/bluestock_mf_dashboard.twbx in Tableau")
        print("   → View reports/ for all chart PNGs")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
