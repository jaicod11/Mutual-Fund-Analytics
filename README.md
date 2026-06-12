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
- **Risk analytics** — Historical VaR, CVaR, Rolling Sharpe, Sector HHI Concentration
- **Investor analytics** — Cohort analysis, SIP continuity tracking
- **Fund Recommender** — risk-based fund suggestions (Low/Moderate/High)
- **Fund Scorecard** — composite 0–100 ranking across all 40 funds
- **4-page interactive Tableau Public dashboard**

---

## 📁 Folder Structure

```
Mutual Fund Analytics/
├── data/
│   ├── raw/                    ← Original downloaded CSV files + live NAV
│   ├── processed/              ← Cleaned, validated CSVs + output CSVs
│   ├── tableau/                ← 13 CSVs prepared for Tableau dashboard
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
│   └── recommender.py          ← Fund recommender (risk-based)
├── sql/
│   ├── schema.sql              ← CREATE TABLE statements (star schema)
│   └── queries.sql             ← 10 analytical SQL queries
├── dashboard/
│   ├── bluestock_mf_dashboard.twbx  ← Tableau Public dashboard (4 pages)
│   ├── Dashboard.pdf
│   └── dashboard_page1.png ... page4.png
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
│   ├── chart_14_var_cvar.png
│   ├── chart_15_cohort_analysis.png
│   ├── chart_16_sip_continuity.png
│   ├── chart_17_hhi_concentration.png
│   ├── rolling_sharpe_chart.png
│   ├── Final_Report.pdf
│   └── Presentation.pptx
├── prepare_tableau_data.py      ← Generates data/tableau/ CSVs for dashboard
├── run_pipeline.py               ← Master script — runs full pipeline end-to-end
├── data_dictionary.md            ← All columns, types, business definitions
├── requirements.txt               ← Python dependencies
└── README.md
```

---

## 📦 Datasets Used

| # | File | Rows | Description |
|---|------|------|-------------|
| 1 | `01_fund_master.csv` | 40 | Fund metadata — AMC, category, risk grade |
| 2 | `02_nav_history.csv` | 64,320 | Daily NAV for all schemes (forward-filled) |
| 3 | `03_aum_by_fund_house.csv` | 90 | Monthly AUM per AMC |
| 4 | `04_monthly_sip_inflows.csv` | 48 | Industry-wide SIP data |
| 5 | `05_category_inflows.csv` | 144 | Net inflows by fund category |
| 6 | `06_industry_folio_count.csv` | 21 | Total investor folios |
| 7 | `07_scheme_performance.csv` | 40 | Risk-return metrics per fund |
| 8 | `08_investor_transactions.csv` | 32,778 | Individual transaction records |
| 9 | `09_portfolio_holdings.csv` | 322 | Stock-level fund holdings |
| 10 | `10_benchmark_indices.csv` | 8,050 | Nifty 50 & Nifty 100 daily values |

**Generated output files:**
| File | Description |
|------|-------------|
| `alpha_beta.csv` | Alpha & Beta for all 40 funds vs Nifty 100 |
| `fund_scorecard.csv` | Composite 0–100 score ranking for all funds |
| `var_cvar_report.csv` | Historical VaR 95% and CVaR per fund |
| `sip_continuity.csv` | SIP continuity status per investor |

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

# 4. Run the full pipeline (cleaning → DB → live NAV → recommender)
python run_pipeline.py --skip-nav

# 5. Open Jupyter notebooks for analysis
jupyter notebook

# 6. Open the dashboard
# Open dashboard/bluestock_mf_dashboard.twbx in Tableau Public (free)
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
| 9 | 15–20% of frequent SIP investors are at-risk of discontinuity (gap > 35 days) |
| 10 | Small Cap funds show highest VaR/CVaR — largest single-day tail risk |

---

## 📈 Performance & Risk Metrics Computed

| Metric | Formula |
|--------|---------|
| **Daily Return** | NAV_t / NAV_t-1 − 1 |
| **CAGR** | (NAV_end / NAV_start) ^ (1/n) − 1 |
| **Sharpe Ratio** | (Rp − Rf) / σ × √252 \| Rf = 6.5% |
| **Sortino Ratio** | (Rp − Rf) / σ_downside × √252 |
| **Rolling Sharpe** | 90-day rolling mean/std × √252 |
| **Beta** | Cov(fund, benchmark) / Var(benchmark) |
| **Alpha** | Intercept × 252 (OLS regression) |
| **Max Drawdown** | min(NAV / running_max − 1) |
| **Historical VaR (95%)** | 5th percentile of daily returns |
| **CVaR (95%)** | Mean of returns below VaR threshold |
| **Sector HHI** | Σ(sector weight²) — concentration measure |
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
| **scipy** | OLS regression (Alpha/Beta), VaR |
| **jupyter** | Notebook environment |
| **mfapi.in** | Live NAV API |
| **Tableau Public** | Interactive 4-page dashboard |
| **Git / GitHub** | Version control |

---

## 👤 Author

**Internship Project** — Bluestock Fintech  
*Data Analytics Internship | June 2026*

---

## 📄 License

This project is for educational and internship purposes only.  
Data sourced from AMFI India and mfapi.in.