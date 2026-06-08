# 📊 Bluestock MF Analytics — Capstone Project I

> **Mutual Fund Data Analytics Platform** | India | 2022–2026  
> Built during a Data Analytics Internship at Bluestock Fintech

---

## 🗂️ Project Overview

A complete end-to-end data analytics pipeline for Indian Mutual Funds covering:
- **40 fund schemes** across 10 AMCs (SBI, HDFC, ICICI, Nippon, Axis, Kotak, and more)
- **64,320+ NAV records** from 2022 to 2026 with holiday forward-fill
- **32,778 investor transactions** across Indian states and city tiers
- **Live NAV fetching** from [mfapi.in](https://api.mfapi.in) API
- **SQLite star schema** with 11 fact and dimension tables
- **Performance analytics** — Sharpe, Sortino, Alpha, Beta, CAGR, Max Drawdown
- **Fund Scorecard** — composite 0–100 ranking across all 40 funds

---

## 📁 Folder Structure

```
Mutual Fund Analytics/
├── data/
│   ├── raw/                    ← Original downloaded CSV files + live NAV
│   ├── processed/              ← Cleaned, validated CSVs + output CSVs
│   └── db/
│       └── bluestock_mf.db     ← SQLite database (not tracked in Git)
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
├── scripts/
│   ├── etl_pipeline.py         ← Load all 10 CSVs, inspect shape/dtypes
│   ├── live_nav_fetch.py       ← Fetch live NAV from mfapi.in
│   ├── data_cleaning.py        ← Clean all datasets → data/processed/
│   ├── db_loader.py            ← Load cleaned data into SQLite
│   ├── data_quality_summary.py ← AMFI code validation + null checks
│   └── compute_metrics.py      ← Sharpe, Sortino, CAGR, Alpha, Beta
├── sql/
│   ├── schema.sql              ← CREATE TABLE statements (star schema)
│   └── queries.sql             ← 10 analytical SQL queries
├── dashboard/
│   └── bluestock_mf.pbix       ← Power BI dashboard (4 pages)
├── reports/
│   ├── chart_01_nav_trend.png
│   ├── chart_02_aum_growth.png
│   ├── chart_03_sip_inflow.png
│   ├── chart_04_category_heatmap.png
│   ├── chart_05_investor_demographics.png
│   ├── chart_06_geographic.png
│   ├── chart_07_folio_growth.png
│   ├── chart_08_correlation_matrix.png
│   ├── chart_09_sector_donut.png
│   ├── chart_10_risk_return.png
│   ├── chart_11_return_distribution.png
│   ├── chart_12_fund_scorecard.png
│   ├── chart_13_benchmark_comparison.png
│   ├── Final_Report.pdf
│   └── Presentation.pptx
├── data_dictionary.md          ← All columns, types, business definitions
├── requirements.txt            ← Python dependencies
└── README.md
```

---

## 📦 Datasets Used

| # | File | Rows | Description |
|---|------|------|-------------|
| 1 | `01_fund_master.csv` | 40 | Fund metadata — AMC, category, risk grade |
| 2 | `02_nav_history.csv` | 46,000+ | Daily NAV for all schemes |
| 3 | `03_aum_by_fund_house.csv` | 90 | Monthly AUM per AMC |
| 4 | `04_monthly_sip_inflows.csv` | 48 | Industry-wide SIP data |
| 5 | `05_category_inflows.csv` | 144 | Net inflows by fund category |
| 6 | `06_industry_folio_count.csv` | 21 | Total investor folios |
| 7 | `07_scheme_performance.csv` | 40 | Risk-return metrics per fund |
| 8 | `08_investor_transactions.csv` | 32,778 | Individual transaction records |
| 9 | `09_portfolio_holdings.csv` | 322 | Stock-level fund holdings |
| 10 | `10_benchmark_indices.csv` | 8,050 | Nifty 50 & Nifty 100 daily values |

---

## 🗄️ Database Schema (Star Schema)

```
dim_fund ──────────────────────────────────────────────┐
  amfi_code (PK)                                        │
  fund_house, scheme_name, category                     │
  expense_ratio_pct, risk_category                      │
                                                        │
fact_nav           → amfi_code FK → dim_fund           │
fact_transactions  → amfi_code FK → dim_fund           │
fact_performance   → amfi_code FK → dim_fund           │
fact_portfolio     → amfi_code FK → dim_fund           │
fact_aum           (fund_house aggregation)            │
fact_sip           (industry-wide monthly)             │
fact_category      (category-wise monthly)             │
fact_folio         (industry-wide monthly)             │
fact_benchmark     (Nifty 50 & Nifty 100 daily)       │
```

---

## 🚀 Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/mutual-fund-analytics.git
cd mutual-fund-analytics

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the ETL pipeline
python scripts/data_cleaning.py
python scripts/db_loader.py

# 5. Open Jupyter notebooks
jupyter notebook
```

---

## 📊 Key Findings

| # | Finding |
|---|---------|
| 1 | SBI Mutual Fund dominates with ~₹12.5 Lakh Crore AUM |
| 2 | SIP inflows hit all-time high of ₹31,002 Crore in Dec 2025 |
| 3 | Total industry folios doubled from 13.26 Cr to 26.12 Cr (2022–2025) |
| 4 | Bluechip funds showed strong NAV growth in 2023 bull run |
| 5 | Age 25–34 is the largest investor segment |
| 6 | Financial Services & IT sectors dominate equity fund holdings |
| 7 | Large Cap Direct funds offer best risk-adjusted returns (Sharpe > 1.0) |
| 8 | Maharashtra, Delhi & Karnataka lead in SIP investment amounts |

---

## 📈 Performance Metrics Computed

| Metric | Formula |
|--------|---------|
| **Daily Return** | NAV_t / NAV_t-1 − 1 |
| **CAGR** | (NAV_end / NAV_start) ^ (1/n) − 1 |
| **Sharpe Ratio** | (Rp − Rf) / σ × √252 \| Rf = 6.5% |
| **Sortino Ratio** | (Rp − Rf) / σ_downside × √252 |
| **Beta** | Cov(fund, benchmark) / Var(benchmark) |
| **Alpha** | Intercept × 252 (OLS regression) |
| **Max Drawdown** | min(NAV / running_max − 1) |
| **Fund Score** | 30% CAGR + 25% Sharpe + 20% Alpha + 15% ExpenseRatio⁻¹ + 10% MaxDD⁻¹ |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.11** | Core language |
| **pandas** | Data manipulation |
| **numpy** | Numerical computation |
| **matplotlib / seaborn** | Static charts |
| **plotly** | Interactive charts |
| **sqlalchemy** | Database ORM |
| **SQLite** | Local database |
| **scipy** | OLS regression (Alpha/Beta) |
| **jupyter** | Notebook environment |
| **mfapi.in** | Live NAV API |
| **Power BI** | Dashboard |
| **Git / GitHub** | Version control |

---

## 👤 Author

**Internship Project** — Bluestock Fintech  
*Data Analytics Internship | June 2026*

---

## 📄 License

This project is for educational and internship purposes only.  
Data sourced from AMFI India and mfapi.in.