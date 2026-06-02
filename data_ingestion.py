import pandas as pd
import os

raw_path = "data/raw/"

csv_files = {
    "fund_master":          "01_fund_master.csv",
    "nav_history":          "02_nav_history.csv",
    "aum_by_fund_house":    "03_aum_by_fund_house.csv",
    "monthly_sip_inflows":  "04_monthly_sip_inflows.csv",
    "category_inflows":     "05_category_inflows.csv",
    "industry_folio_count": "06_industry_folio_count.csv",
    "scheme_performance":   "07_scheme_performance.csv",
    "investor_transactions":"08_investor_transactions.csv",
    "portfolio_holdings":   "09_portfolio_holdings.csv",
    "benchmark_indices":    "10_benchmark_indices.csv",
}

dataframes = {}

print("=" * 60)
print("  LOADING ALL 10 CSV FILES")
print("=" * 60)

for name, filename in csv_files.items():
    filepath = os.path.join(raw_path, filename)
    df = pd.read_csv(filepath)
    dataframes[name] = df

    print(f"\n📄 {filename}")
    print(f"   Shape   : {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"   Columns : {list(df.columns)}")
    print(f"   Dtypes  :\n{df.dtypes.to_string()}")
    print(f"   Head(3) :\n{df.head(3).to_string()}")
    print(f"   Nulls   :\n{df.isnull().sum().to_string()}")
    print("-" * 60)

print("\n" + "=" * 60)
print("  FUND MASTER — UNIQUE VALUES")
print("=" * 60)
fm = dataframes["fund_master"]
print(f"\nFund Houses ({fm['fund_house'].nunique()}):")
for h in fm["fund_house"].unique():
    print(f"  - {h}")

print(f"\nCategories: {list(fm['category'].unique())}")
print(f"\nSub-Categories: {list(fm['sub_category'].unique())}")
print(f"\nRisk Categories: {list(fm['risk_category'].unique())}")
print(f"\nSEBI Category Codes: {list(fm['sebi_category_code'].unique())}")

print("\n" + "=" * 60)
print("  AMFI CODE VALIDATION")
print("=" * 60)
master_codes = set(dataframes["fund_master"]["amfi_code"])
history_codes = set(dataframes["nav_history"]["amfi_code"])

missing_in_history = master_codes - history_codes
extra_in_history   = history_codes - master_codes

print(f"\nTotal codes in fund_master  : {len(master_codes)}")
print(f"Total codes in nav_history  : {len(history_codes)}")
print(f"Codes MISSING from nav_history: {missing_in_history if missing_in_history else 'None ✅'}")
print(f"Extra codes in nav_history   : {extra_in_history if extra_in_history else 'None ✅'}")

print("\n" + "=" * 60)
print("  DATA QUALITY SUMMARY")
print("=" * 60)
for name, df in dataframes.items():
    total_nulls = df.isnull().sum().sum()
    print(f"\n{name}:")
    print(f"  Rows      : {df.shape[0]}")
    print(f"  Columns   : {df.shape[1]}")
    print(f"  Total Nulls: {total_nulls}", "⚠️" if total_nulls > 0 else "✅")
    if total_nulls > 0:
        null_cols = df.isnull().sum()
        null_cols = null_cols[null_cols > 0]
        print(f"  Null Columns:\n{null_cols.to_string()}")

print("\n" + "=" * 60)
print("  ✅ DATA INGESTION COMPLETE")
print("=" * 60)