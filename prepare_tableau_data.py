"""
DAY 5 — Prepare Data Files for Tableau Public
Run this script first before opening Tableau
"""
import pandas as pd
import numpy as np
import os
from pathlib import Path

if os.path.basename(os.getcwd()) == 'notebooks':
    os.chdir('..')

proc = Path("data/processed/")
tableau_path = Path("data/tableau/")
tableau_path.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("  PREPARING TABLEAU DATA FILES")
print("=" * 60)

# ── FILE 1: Industry AUM Trend (Page 1) ────────────────────────
aum = pd.read_csv(proc / "03_aum_by_fund_house.csv")
aum["date"] = pd.to_datetime(aum["date"])
aum["year"] = aum["date"].dt.year

# Monthly total AUM
aum_trend = (aum.groupby("date")["aum_lakh_crore"]
               .sum()
               .reset_index())
aum_trend.columns = ["date", "total_aum_lakh_crore"]
aum_trend.to_csv(tableau_path / "t1_aum_trend.csv", index=False)
print(f"✅ t1_aum_trend.csv         → {len(aum_trend)} rows")

# AUM by fund house (latest month)
aum_by_house = (aum[aum["date"] == aum["date"].max()]
                .groupby("fund_house")["aum_lakh_crore"]
                .sum()
                .reset_index()
                .sort_values("aum_lakh_crore", ascending=False))
aum_by_house.to_csv(tableau_path / "t1_aum_by_house.csv", index=False)
print(f"✅ t1_aum_by_house.csv      → {len(aum_by_house)} rows")

# KPI values
sip = pd.read_csv(proc / "04_monthly_sip_inflows.csv")
folio = pd.read_csv(proc / "06_industry_folio_count.csv")
fm = pd.read_csv(proc / "01_fund_master.csv")

kpis = pd.DataFrame([{
    "metric": "Total AUM (₹ Lakh Cr)",
    "value": round(aum_by_house["aum_lakh_crore"].sum(), 2),
    "unit": "Lakh Crore"
},{
    "metric": "SIP Inflows (₹ Crore)",
    "value": int(sip["sip_inflow_crore"].max()),
    "unit": "Crore"
},{
    "metric": "Total Folios (Crore)",
    "value": round(folio["total_folios_crore"].max(), 2),
    "unit": "Crore"
},{
    "metric": "Total Schemes",
    "value": len(fm),
    "unit": "Schemes"
}])
kpis.to_csv(tableau_path / "t1_kpis.csv", index=False)
print(f"✅ t1_kpis.csv              → {len(kpis)} rows")

# ── FILE 2: Fund Performance (Page 2) ──────────────────────────
perf = pd.read_csv(proc / "07_scheme_performance.csv")
perf_clean = perf[[
    "amfi_code","scheme_name","fund_house","category","plan",
    "return_1yr_pct","return_3yr_pct","return_5yr_pct",
    "sharpe_ratio","sortino_ratio","alpha","beta",
    "std_dev_ann_pct","max_drawdown_pct",
    "aum_crore","expense_ratio_pct","risk_grade","morningstar_rating"
]].copy()
perf_clean.to_csv(tableau_path / "t2_fund_performance.csv", index=False)
print(f"✅ t2_fund_performance.csv  → {len(perf_clean)} rows")

# Fund scorecard
try:
    scorecard = pd.read_csv(proc / "fund_scorecard.csv")
    scorecard.to_csv(tableau_path / "t2_fund_scorecard.csv", index=False)
    print(f"✅ t2_fund_scorecard.csv   → {len(scorecard)} rows")
except:
    print("⚠️  fund_scorecard.csv not found — skipping")

# NAV history (sample for speed — last 3 years)
nav = pd.read_csv(proc / "02_nav_history.csv")
nav["date"] = pd.to_datetime(nav["date"])
nav_3yr = nav[nav["date"] >= nav["date"].max() - pd.DateOffset(years=3)]
nav_3yr = nav_3yr.merge(fm[["amfi_code","scheme_name","fund_house","category"]], on="amfi_code", how="left")
nav_3yr["date"] = nav_3yr["date"].astype(str)
nav_3yr.to_csv(tableau_path / "t2_nav_history.csv", index=False)
print(f"✅ t2_nav_history.csv       → {len(nav_3yr):,} rows")

# Benchmark
bench = pd.read_csv(proc / "10_benchmark_indices.csv")
bench["date"] = pd.to_datetime(bench["date"])
bench_3yr = bench[bench["date"] >= bench["date"].max() - pd.DateOffset(years=3)]
bench_3yr["date"] = bench_3yr["date"].astype(str)
bench_3yr.to_csv(tableau_path / "t2_benchmark.csv", index=False)
print(f"✅ t2_benchmark.csv         → {len(bench_3yr):,} rows")

# ── FILE 3: Investor Analytics (Page 3) ────────────────────────
txn = pd.read_csv(proc / "08_investor_transactions.csv")

# By state
state_agg = (txn.groupby("state")
               .agg(total_transactions=("amount_inr","count"),
                    total_amount=("amount_inr","sum"),
                    avg_amount=("amount_inr","mean"))
               .reset_index()
               .sort_values("total_amount", ascending=False))
state_agg.to_csv(tableau_path / "t3_by_state.csv", index=False)
print(f"✅ t3_by_state.csv          → {len(state_agg)} rows")

# By transaction type
type_agg = (txn.groupby("transaction_type")
              .agg(count=("amount_inr","count"),
                   total_amount=("amount_inr","sum"))
              .reset_index())
type_agg.to_csv(tableau_path / "t3_transaction_type.csv", index=False)
print(f"✅ t3_transaction_type.csv  → {len(type_agg)} rows")

# By age group
age_agg = (txn.groupby(["age_group","transaction_type"])
             .agg(avg_amount=("amount_inr","mean"),
                  count=("amount_inr","count"))
             .reset_index())
age_agg.to_csv(tableau_path / "t3_by_age.csv", index=False)
print(f"✅ t3_by_age.csv            → {len(age_agg)} rows")

# Monthly transaction volume
txn["transaction_date"] = pd.to_datetime(txn["transaction_date"])
txn["month"] = txn["transaction_date"].dt.to_period("M").astype(str)
monthly_txn = (txn.groupby(["month","transaction_type"])
                 .agg(count=("amount_inr","count"),
                      total=("amount_inr","sum"))
                 .reset_index())
monthly_txn.to_csv(tableau_path / "t3_monthly_volume.csv", index=False)
print(f"✅ t3_monthly_volume.csv    → {len(monthly_txn)} rows")

# City tier
tier_agg = (txn.groupby("city_tier")
              .agg(count=("amount_inr","count"),
                   total=("amount_inr","sum"))
              .reset_index())
tier_agg.to_csv(tableau_path / "t3_city_tier.csv", index=False)
print(f"✅ t3_city_tier.csv         → {len(tier_agg)} rows")

# ── FILE 4: SIP & Market Trends (Page 4) ───────────────────────
sip["month"] = pd.to_datetime(sip["month"])
sip["month_str"] = sip["month"].dt.strftime("%Y-%m")
sip.to_csv(tableau_path / "t4_sip_inflows.csv", index=False)
print(f"✅ t4_sip_inflows.csv       → {len(sip)} rows")

# Nifty 50 monthly
nifty50 = bench[bench["index_name"].str.contains("50", na=False)].copy()
nifty50["month"] = nifty50["date"].dt.to_period("M").astype(str)
nifty50_monthly = (nifty50.groupby("month")["close_value"]
                          .last()
                          .reset_index())
nifty50_monthly.to_csv(tableau_path / "t4_nifty50.csv", index=False)
print(f"✅ t4_nifty50.csv           → {len(nifty50_monthly)} rows")

# Category inflows
cat = pd.read_csv(proc / "05_category_inflows.csv")
cat["month"] = pd.to_datetime(cat["month"]).dt.strftime("%Y-%m")
cat.to_csv(tableau_path / "t4_category_inflows.csv", index=False)
print(f"✅ t4_category_inflows.csv  → {len(cat)} rows")

# Top 5 categories FY25
cat_fy25 = cat[cat["month"].str.startswith("2025")]
top5_cat = (cat_fy25.groupby("category")["net_inflow_crore"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(5)
                    .reset_index())
top5_cat.to_csv(tableau_path / "t4_top5_categories.csv", index=False)
print(f"✅ t4_top5_categories.csv   → {len(top5_cat)} rows")

print(f"\n✅ ALL TABLEAU FILES READY → data/tableau/")
print(f"   Total files: {len(list(tableau_path.glob('*.csv')))}")
