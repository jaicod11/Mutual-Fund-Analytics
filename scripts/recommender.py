"""
recommender.py — Simple Fund Recommender System
Bluestock MF Analytics | Day 6

Usage:
    python scripts/recommender.py
    python scripts/recommender.py --risk Low
    python scripts/recommender.py --risk Moderate
    python scripts/recommender.py --risk High
"""

import pandas as pd
import argparse
from pathlib import Path


def load_data():
    """Load fund performance and master data."""
    proc = Path("data/processed/")
    perf        = pd.read_csv(proc / "07_scheme_performance.csv")
    fund_master = pd.read_csv(proc / "01_fund_master.csv")

    perf["amfi_code"]        = perf["amfi_code"].astype(int)
    fund_master["amfi_code"] = fund_master["amfi_code"].astype(int)

    # Merge performance with risk category from fund_master
    merged = perf.merge(
        fund_master[["amfi_code", "risk_category", "sub_category"]],
        on="amfi_code", how="left"
    )
    return merged


def recommend_funds(risk_appetite: str, data: pd.DataFrame = None) -> pd.DataFrame:
    """
    Returns top 3 fund recommendations based on risk appetite.

    Parameters:
        risk_appetite (str): 'Low' | 'Moderate' | 'High'
        data (DataFrame): pre-loaded merged dataframe (optional)

    Returns:
        DataFrame: top 3 recommended funds with key metrics
    """
    if data is None:
        data = load_data()

    risk_map = {
        "Low"     : ["Low", "Moderately Low"],
        "Moderate": ["Moderate", "Moderately High"],
        "High"    : ["High", "Very High"]
    }

    valid_risk = ["Low", "Moderate", "High"]
    if risk_appetite not in valid_risk:
        raise ValueError(f"risk_appetite must be one of {valid_risk}")

    grades   = risk_map[risk_appetite]
    filtered = data[data["risk_category"].isin(grades)]

    # Fallback to risk_grade if risk_category has no matches
    if filtered.empty:
        filtered = data[data["risk_grade"].str.contains(
            risk_appetite, case=False, na=False
        )]

    if filtered.empty:
        print(f"⚠️  No funds found for {risk_appetite} risk. Showing top funds overall.")
        filtered = data

    top3 = (filtered.nlargest(3, "sharpe_ratio")
                    [[
                        "amfi_code", "scheme_name", "fund_house",
                        "category", "sub_category",
                        "sharpe_ratio", "sortino_ratio",
                        "return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
                        "alpha", "beta",
                        "max_drawdown_pct", "expense_ratio_pct",
                        "risk_grade", "morningstar_rating"
                    ]]
                    .reset_index(drop=True))

    top3.index = top3.index + 1  # Rank starts from 1
    return top3


def print_recommendation(risk_appetite: str, df: pd.DataFrame):
    """Pretty print the recommendation table."""
    border = "=" * 70
    print(f"\n{border}")
    print(f"  🎯 FUND RECOMMENDATIONS — {risk_appetite.upper()} RISK APPETITE")
    print(border)
    print(f"  {'Rank':<5} {'Fund Name':<35} {'Sharpe':>7} {'3yr Ret%':>9} {'Exp%':>6}")
    print(f"  {'-'*65}")
    for rank, row in df.iterrows():
        print(f"  {rank:<5} {row['scheme_name'][:34]:<35} "
              f"{row['sharpe_ratio']:>7.3f} "
              f"{row['return_3yr_pct']:>9.2f} "
              f"{row['expense_ratio_pct']:>6.2f}")
    print(border)
    print(f"\n  📊 Detailed Metrics:")
    display_cols = ["scheme_name","sharpe_ratio","return_3yr_pct",
                    "alpha","max_drawdown_pct","expense_ratio_pct","risk_grade"]
    print(df[display_cols].to_string())
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Bluestock MF Fund Recommender — suggests top 3 funds by risk appetite"
    )
    parser.add_argument(
        "--risk",
        choices=["Low", "Moderate", "High"],
        default=None,
        help="Risk appetite level: Low | Moderate | High"
    )
    args = parser.parse_args()

    print("\n🚀 Bluestock MF — Fund Recommender System")
    print("=" * 70)

    data = load_data()
    print(f"✅ Loaded {len(data)} fund records\n")

    if args.risk:
        # Single recommendation
        result = recommend_funds(args.risk, data)
        print_recommendation(args.risk, result)
    else:
        # Show all three risk levels
        for appetite in ["Low", "Moderate", "High"]:
            result = recommend_funds(appetite, data)
            print_recommendation(appetite, result)


if __name__ == "__main__":
    main()
