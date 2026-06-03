# Data Dictionary — Mutual Fund Analytics
**Project:** Bluestock MF Analytics  
**Database:** bluestock_mf.db  
**Last Updated:** Day 2

---

## Table 1: `dim_fund` (Fund Master)
**Source:** `data/processed/01_fund_master.csv`  
**Description:** Master dimension table containing metadata for all mutual fund schemes.

| Column | Data Type | Description |
|---|---|---|
| `amfi_code` | INTEGER (PK) | Unique AMFI scheme code assigned to each mutual fund |
| `fund_house` | TEXT | Name of the Asset Management Company (AMC) e.g. SBI Mutual Fund |
| `scheme_name` | TEXT | Full name of the mutual fund scheme |
| `category` | TEXT | Broad category — Equity or Debt |
| `sub_category` | TEXT | Specific sub-category e.g. Large Cap, Small Cap, Gilt, Liquid |
| `plan` | TEXT | Plan type — Direct or Regular |
| `launch_date` | TEXT | Date when the scheme was launched |
| `benchmark` | TEXT | Index used to benchmark fund performance e.g. NIFTY 50 |
| `expense_ratio_pct` | REAL | Annual fee charged by fund house as % of AUM (0.1% – 2.5%) |
| `exit_load_pct` | REAL | Fee charged on redemption before lock-in period |
| `min_sip_amount` | INTEGER | Minimum monthly SIP investment in INR |
| `min_lumpsum_amount` | INTEGER | Minimum one-time investment in INR |
| `fund_manager` | TEXT | Name of the fund manager managing the scheme |
| `risk_category` | TEXT | SEBI risk level — Low / Moderate / Moderately High / High / Very High |
| `sebi_category_code` | TEXT | SEBI assigned category code e.g. EC01, EC03 |

---

## Table 2: `dim_date` (Date Dimension)
**Source:** Generated  
**Description:** Date dimension for time-based analysis.

| Column | Data Type | Description |
|---|---|---|
| `date_id` | TEXT (PK) | Date in YYYY-MM-DD format |
| `year` | INTEGER | Calendar year |
| `month` | INTEGER | Month number (1–12) |
| `day` | INTEGER | Day of month |
| `quarter` | INTEGER | Quarter (1–4) |
| `month_name` | TEXT | Full month name e.g. January |
| `day_of_week` | TEXT | Day name e.g. Monday |

---

## Table 3: `fact_nav` (NAV History)
**Source:** `data/processed/02_nav_history.csv`  
**Description:** Daily Net Asset Value for all 40 fund schemes from 2022 onwards.

| Column | Data Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-generated row ID |
| `amfi_code` | INTEGER (FK) | References dim_fund.amfi_code |
| `date` | TEXT | NAV date in YYYY-MM-DD format |
| `nav` | REAL | Net Asset Value in INR — price of one unit of the fund |

---

## Table 4: `fact_transactions` (Investor Transactions)
**Source:** `data/processed/08_investor_transactions.csv`  
**Description:** Individual investor transaction records including purchases and redemptions.

| Column | Data Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-generated row ID |
| `investor_id` | TEXT | Unique investor identifier e.g. INV003054 |
| `transaction_date` | TEXT | Date of transaction in YYYY-MM-DD format |
| `amfi_code` | INTEGER (FK) | References dim_fund.amfi_code |
| `transaction_type` | TEXT | Type — Sip / Lumpsum / Redemption |
| `amount_inr` | INTEGER | Transaction amount in INR |
| `state` | TEXT | Indian state of the investor |
| `city` | TEXT | City of the investor |
| `city_tier` | TEXT | City classification — Tier 1 / Tier 2 / Tier 3 |
| `age_group` | TEXT | Investor age bracket e.g. 25-34 |
| `gender` | TEXT | Investor gender |
| `annual_income_lakh` | REAL | Investor annual income in lakhs |
| `payment_mode` | TEXT | Payment method — UPI / Cheque / Mandate |
| `kyc_status` | TEXT | KYC verification status — Verified / Pending / Rejected |

---

## Table 5: `fact_performance` (Scheme Performance)
**Source:** `data/processed/07_scheme_performance.csv`  
**Description:** Performance metrics and risk ratios for all 40 fund schemes.

| Column | Data Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-generated row ID |
| `amfi_code` | INTEGER (FK) | References dim_fund.amfi_code |
| `scheme_name` | TEXT | Name of the fund scheme |
| `fund_house` | TEXT | Name of the AMC |
| `category` | TEXT | Fund category |
| `plan` | TEXT | Direct or Regular plan |
| `return_1yr_pct` | REAL | 1-year return as percentage |
| `return_3yr_pct` | REAL | 3-year annualised return as percentage |
| `return_5yr_pct` | REAL | 5-year annualised return as percentage |
| `benchmark_3yr_pct` | REAL | 3-year benchmark index return for comparison |
| `alpha` | REAL | Excess return over benchmark — higher is better |
| `beta` | REAL | Fund volatility relative to market — 1 = market-like |
| `sharpe_ratio` | REAL | Risk-adjusted return — higher means better return per unit risk |
| `sortino_ratio` | REAL | Like Sharpe but only penalises downside risk |
| `std_dev_ann_pct` | REAL | Annualised standard deviation — measure of volatility |
| `max_drawdown_pct` | REAL | Largest peak-to-trough decline — negative value |
| `aum_crore` | INTEGER | Assets Under Management in crores |
| `expense_ratio_pct` | REAL | Annual management fee as % |
| `morningstar_rating` | INTEGER | Star rating 1–5 from Morningstar |
| `risk_grade` | TEXT | Risk classification — Low / Moderate / High / Very High |

---

## Table 6: `fact_aum` (AUM by Fund House)
**Source:** `data/processed/03_aum_by_fund_house.csv`  
**Description:** Monthly AUM (Assets Under Management) data per fund house.

| Column | Data Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-generated row ID |
| `date` | TEXT | Month-end date |
| `fund_house` | TEXT | Name of the AMC |
| `aum_lakh_crore` | REAL | AUM in lakh crores |
| `aum_crore` | INTEGER | AUM in crores |
| `num_schemes` | INTEGER | Number of active schemes by that fund house |

---

## Table 7: `fact_portfolio` (Portfolio Holdings)
**Source:** `data/processed/09_portfolio_holdings.csv`  
**Description:** Stock-level holdings of each mutual fund scheme.

| Column | Data Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-generated row ID |
| `amfi_code` | INTEGER (FK) | References dim_fund.amfi_code |
| `stock_symbol` | TEXT | BSE/NSE stock ticker symbol |
| `stock_name` | TEXT | Full company name |
| `sector` | TEXT | Industry sector of the stock |
| `weight_pct` | REAL | Stock's % weight in the fund portfolio |
| `market_value_cr` | REAL | Market value of holding in crores |
| `current_price_inr` | REAL | Current stock price in INR |
| `portfolio_date` | TEXT | Date of portfolio disclosure |

---

## Table 8: `fact_sip` (Monthly SIP Inflows)
**Source:** `data/processed/04_monthly_sip_inflows.csv`  
**Description:** Industry-wide monthly SIP (Systematic Investment Plan) data.

| Column | Data Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-generated row ID |
| `month` | TEXT | Month in YYYY-MM format |
| `sip_inflow_crore` | INTEGER | Total SIP inflow in crores |
| `active_sip_accounts_crore` | REAL | Total active SIP accounts in crores |
| `new_sip_accounts_lakh` | REAL | New SIP accounts opened in that month (lakhs) |
| `sip_aum_lakh_crore` | REAL | Total SIP AUM in lakh crores |
| `yoy_growth_pct` | REAL | Year-on-year growth % — NULL for first 12 months |

---

## Table 9: `fact_category` (Category Inflows)
**Source:** `data/processed/05_category_inflows.csv`  
**Description:** Monthly net inflows broken down by fund category.

| Column | Data Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-generated row ID |
| `month` | TEXT | Month in YYYY-MM format |
| `category` | TEXT | Fund category e.g. Large Cap / Mid Cap / Small Cap |
| `net_inflow_crore` | REAL | Net inflow (purchases minus redemptions) in crores |

---

## Table 10: `fact_folio` (Industry Folio Count)
**Source:** `data/processed/06_industry_folio_count.csv`  
**Description:** Total number of investor folios across the mutual fund industry.

| Column | Data Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-generated row ID |
| `month` | TEXT | Month in YYYY-MM format |
| `total_folios_crore` | REAL | Total folios across all categories in crores |
| `equity_folios_crore` | REAL | Equity fund folios in crores |
| `debt_folios_crore` | REAL | Debt fund folios in crores |
| `hybrid_folios_crore` | REAL | Hybrid fund folios in crores |
| `others_folios_crore` | REAL | Other category folios in crores |

---

## Table 11: `fact_benchmark` (Benchmark Indices)
**Source:** `data/processed/10_benchmark_indices.csv`  
**Description:** Daily closing values of benchmark indices like NIFTY 50.

| Column | Data Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-generated row ID |
| `date` | TEXT | Date in YYYY-MM-DD format |
| `index_name` | TEXT | Name of benchmark index e.g. NIFTY50 |
| `close_value` | REAL | Closing value of the index on that date |

---

## Known Data Anomalies

| File | Anomaly | Reason |
|---|---|---|
| `fact_sip` | 12 NULL values in `yoy_growth_pct` | First 12 months (2022) have no prior year data |

---

*Data Dictionary generated as part of Day 2 — Data Cleaning + SQL Database Design*