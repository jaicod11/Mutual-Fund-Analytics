import pandas as pd
import numpy as np
import os

raw_path       = "data/raw/"
processed_path = "data/processed/"
os.makedirs(processed_path, exist_ok=True)

print("=" * 60)
print("  DAY 2 — DATA CLEANING")
print("=" * 60)

# ──────────────────────────────────────────────
# 1. CLEAN nav_history.csv
# ──────────────────────────────────────────────
print("\n📄 Cleaning nav_history.csv ...")
nav = pd.read_csv(raw_path + "02_nav_history.csv")

# Parse date to datetime
nav["date"] = pd.to_datetime(nav["date"])

# Sort by amfi_code + date
nav = nav.sort_values(["amfi_code", "date"]).reset_index(drop=True)

# Remove duplicates
before = len(nav)
nav = nav.drop_duplicates(subset=["amfi_code", "date"])
print(f"   Duplicates removed : {before - len(nav)}")

# Validate NAV > 0
invalid_nav = nav[nav["nav"] <= 0]
print(f"   Invalid NAV (<=0)  : {len(invalid_nav)}")
nav = nav[nav["nav"] > 0]

# ✅ FIXED: Forward-fill missing NAV (holidays/weekends) — loop per fund
all_filled = []
for code in nav["amfi_code"].unique():
    df_code = nav[nav["amfi_code"] == code].set_index("date")
    full_range = pd.date_range(df_code.index.min(), df_code.index.max(), freq="D")
    df_code = df_code.reindex(full_range)
    df_code["nav"] = df_code["nav"].ffill()
    df_code["amfi_code"] = code
    df_code = df_code.reset_index()
    df_code.columns = ["date", "nav", "amfi_code"]
    all_filled.append(df_code)

nav = pd.concat(all_filled, ignore_index=True)
nav = nav[["amfi_code", "date", "nav"]]

nav.to_csv(processed_path + "02_nav_history.csv", index=False)
print(f"   ✅ Saved — {len(nav)} records")

# ──────────────────────────────────────────────
# 2. CLEAN investor_transactions.csv
# ──────────────────────────────────────────────
print("\n📄 Cleaning investor_transactions.csv ...")
txn = pd.read_csv(raw_path + "08_investor_transactions.csv")

# Fix date format
txn["transaction_date"] = pd.to_datetime(txn["transaction_date"])

# Standardise transaction_type
txn["transaction_type"] = txn["transaction_type"].str.strip().str.title()
valid_types = ["Sip", "Lumpsum", "Redemption"]
invalid_types = txn[~txn["transaction_type"].isin(valid_types)]["transaction_type"].unique()
print(f"   Invalid transaction types : {invalid_types if len(invalid_types) > 0 else 'None ✅'}")

# Validate amount > 0
before = len(txn)
txn = txn[txn["amount_inr"] > 0]
print(f"   Invalid amounts removed   : {before - len(txn)}")

# Check KYC status values
valid_kyc = ["Verified", "Pending", "Rejected"]
invalid_kyc = txn[~txn["kyc_status"].isin(valid_kyc)]["kyc_status"].unique()
print(f"   Invalid KYC values        : {invalid_kyc if len(invalid_kyc) > 0 else 'None ✅'}")

# Remove duplicates
txn = txn.drop_duplicates().reset_index(drop=True)

txn.to_csv(processed_path + "08_investor_transactions.csv", index=False)
print(f"   ✅ Saved — {len(txn)} records")

# ──────────────────────────────────────────────
# 3. CLEAN scheme_performance.csv
# ──────────────────────────────────────────────
print("\n📄 Cleaning scheme_performance.csv ...")
perf = pd.read_csv(raw_path + "07_scheme_performance.csv")

# Validate return columns are numeric
return_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
               "benchmark_3yr_pct", "alpha", "beta", "sharpe_ratio",
               "sortino_ratio", "std_dev_ann_pct", "max_drawdown_pct"]
for col in return_cols:
    perf[col] = pd.to_numeric(perf[col], errors="coerce")

# Check expense_ratio range (0.1% - 2.5%)
out_of_range = perf[
    (perf["expense_ratio_pct"] < 0.1) |
    (perf["expense_ratio_pct"] > 2.5)
]
print(f"   Expense ratio out of range (0.1-2.5%) : {len(out_of_range)}")
if len(out_of_range) > 0:
    print(out_of_range[["scheme_name", "expense_ratio_pct"]])

# Flag anomalies — return > 100% or < -50%
anomalies = perf[
    (perf["return_1yr_pct"] > 100) |
    (perf["return_1yr_pct"] < -50)
]
print(f"   Return anomalies flagged  : {len(anomalies)}")

perf = perf.drop_duplicates().reset_index(drop=True)
perf.to_csv(processed_path + "07_scheme_performance.csv", index=False)
print(f"   ✅ Saved — {len(perf)} records")

# ──────────────────────────────────────────────
# 4. CLEAN REMAINING 7 FILES
# ──────────────────────────────────────────────
other_files = {
    "01_fund_master.csv":          "launch_date",
    "03_aum_by_fund_house.csv":    "date",
    "04_monthly_sip_inflows.csv":  "month",
    "05_category_inflows.csv":     "month",
    "06_industry_folio_count.csv": "month",
    "09_portfolio_holdings.csv":   "portfolio_date",
    "10_benchmark_indices.csv":    "date",
}

for filename, date_col in other_files.items():
    print(f"\n📄 Cleaning {filename} ...")
    df = pd.read_csv(raw_path + filename)
    df[date_col] = pd.to_datetime(df[date_col])
    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"   Duplicates removed : {before - len(df)}")
    df.to_csv(processed_path + filename, index=False)
    print(f"   ✅ Saved — {len(df)} records")

print("\n" + "=" * 60)
print("  ✅ ALL FILES CLEANED → data/processed/")
print("=" * 60)