import pandas as pd

raw_path = "data/raw/"

fund_master = pd.read_csv(raw_path + "01_fund_master.csv")
nav_history  = pd.read_csv(raw_path + "02_nav_history.csv")

master_codes  = set(fund_master["amfi_code"])
history_codes = set(nav_history["amfi_code"])
missing       = master_codes - history_codes

print("=" * 50)
print("  DATA QUALITY SUMMARY")
print("=" * 50)

print(f"\nFund Master   : {fund_master.shape[0]} records")
print(f"NAV History   : {nav_history.shape[0]} records")
print(f"Missing AMFI codes: {missing if missing else 'None ✅'}")

files = {
    "01_fund_master.csv":          "fund_master",
    "02_nav_history.csv":          "nav_history",
    "03_aum_by_fund_house.csv":    "aum_by_fund_house",
    "04_monthly_sip_inflows.csv":  "monthly_sip_inflows",
    "05_category_inflows.csv":     "category_inflows",
    "06_industry_folio_count.csv": "industry_folio_count",
    "07_scheme_performance.csv":   "scheme_performance",
    "08_investor_transactions.csv":"investor_transactions",
    "09_portfolio_holdings.csv":   "portfolio_holdings",
    "10_benchmark_indices.csv":    "benchmark_indices",
}

print("\n── Null Values Per File ──")
for filename, label in files.items():
    df = pd.read_csv(raw_path + filename)
    nulls = df.isnull().sum().sum()
    status = "✅" if nulls == 0 else f"⚠️  {nulls} nulls"
    print(f"  {label:30s}: {status}")

print("\n✅ Data Quality Check Complete")