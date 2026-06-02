import pandas as pd

fund_master = pd.read_csv("data/raw/fund_master.csv")
nav_history = pd.read_csv("data/raw/nav_history.csv")

# Check unique values
print("Fund Houses:", fund_master["fund_house"].nunique())
print(fund_master["fund_house"].unique())

print("\nCategories:", fund_master["category"].unique())
print("Sub-categories:", fund_master["sub_category"].unique())
print("Risk Grades:", fund_master["risk_grade"].unique())

# Validate AMFI codes
master_codes = set(fund_master["scheme_code"])
history_codes = set(nav_history["scheme_code"])

missing = master_codes - history_codes
print(f"\n⚠️ Codes in fund_master but missing in nav_history: {len(missing)}")
print(missing)

# Data quality summary
print("\n--- DATA QUALITY SUMMARY ---")
print(f"Total funds in master: {len(fund_master)}")
print(f"Total NAV records: {len(nav_history)}")
print(f"Missing scheme codes: {len(missing)}")