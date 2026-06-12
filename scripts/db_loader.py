import pandas as pd
from sqlalchemy import create_engine, text
import os

processed_path = "data/processed/"
os.makedirs("data/db", exist_ok=True)
DB_PATH = "data/db/bluestock_mf.db"

# Creating SQLite engine
engine = create_engine(f"sqlite:///{DB_PATH}")

print("=" * 60)
print("  DAY 2 — LOADING DATA INTO SQLITE")
print("=" * 60)

# 1. Creating schema from schema.sql

print("\n📐 Creating schema ...")
with open("sql/schema.sql", "r") as f:
    schema_sql = f.read()

with engine.connect() as conn:
    for statement in schema_sql.split(";"):
        stmt = statement.strip()
        if stmt:
            conn.execute(text(stmt))
    conn.commit()
print("   ✅ Schema created")

# STEP 2: Loading each cleaned CSV into SQLite

tables = {
    "dim_fund":          ("01_fund_master.csv",          "amfi_code"),
    "fact_nav":          ("02_nav_history.csv",           "amfi_code"),
    "fact_aum":          ("03_aum_by_fund_house.csv",     "fund_house"),
    "fact_transactions": ("08_investor_transactions.csv", "investor_id"),
    "fact_performance":  ("07_scheme_performance.csv",    "amfi_code"),
    "fact_portfolio":    ("09_portfolio_holdings.csv",    "amfi_code"),
    "fact_sip":          ("04_monthly_sip_inflows.csv",   "month"),
    "fact_category":     ("05_category_inflows.csv",      "month"),
    "fact_folio":        ("06_industry_folio_count.csv",  "month"),
    "fact_benchmark":    ("10_benchmark_indices.csv",     "date"),
}

print("\n📥 Loading tables ...")
for table_name, (filename, _) in tables.items():
    filepath = os.path.join(processed_path, filename)
    df = pd.read_csv(filepath)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"   ✅ {table_name:25s} → {len(df):6,} rows")

# 3. Verify row counts match source CSVs

print("\n🔍 Verifying row counts ...")
with engine.connect() as conn:
    for table_name, (filename, _) in tables.items():
        source_df  = pd.read_csv(os.path.join(processed_path, filename))
        db_count   = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        source_count = len(source_df)
        match = "✅" if db_count == source_count else "❌ MISMATCH"
        print(f"   {table_name:25s}: source={source_count:6,}  db={db_count:6,}  {match}")

print("\n" + "=" * 60)
print(f"  ✅ DATABASE READY → {DB_PATH}")
print("=" * 60)