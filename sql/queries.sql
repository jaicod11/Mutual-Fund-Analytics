-- ── QUERY 1: Top 5 Funds by AUM ─────────────────────────────
-- Shows which fund houses manage the most money
SELECT
    fund_house,
    SUM(aum_crore)        AS total_aum_crore,
    ROUND(SUM(aum_lakh_crore), 2) AS total_aum_lakh_crore
FROM fact_aum
WHERE date = (SELECT MAX(date) FROM fact_aum)
GROUP BY fund_house
ORDER BY total_aum_crore DESC
LIMIT 5;


-- ── QUERY 2: Average NAV Per Month ──────────────────────────
-- Tracks how average NAV changes over months
SELECT
    SUBSTR(date, 1, 7)    AS month,
    ROUND(AVG(nav), 4)    AS avg_nav,
    COUNT(DISTINCT amfi_code) AS num_funds
FROM fact_nav
GROUP BY SUBSTR(date, 1, 7)
ORDER BY month;


-- ── QUERY 3: SIP Year-on-Year Growth ────────────────────────
-- Compares SIP inflows year over year
SELECT
    month,
    sip_inflow_crore,
    yoy_growth_pct
FROM fact_sip
WHERE yoy_growth_pct IS NOT NULL
ORDER BY month;


-- ── QUERY 4: Total Transactions by State ────────────────────
-- Shows which states have highest investment activity
SELECT
    state,
    COUNT(*)              AS total_transactions,
    SUM(amount_inr)       AS total_amount_inr,
    ROUND(AVG(amount_inr), 2) AS avg_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;


-- ── QUERY 5: Funds with Expense Ratio Below 1% ──────────────
-- Identifies low-cost funds — better for investors
SELECT
    f.scheme_name,
    f.fund_house,
    f.category,
    f.expense_ratio_pct
FROM dim_fund f
WHERE f.expense_ratio_pct < 1.0
ORDER BY f.expense_ratio_pct ASC;


-- ── QUERY 6: Best Performing Funds by 3-Year Return ─────────
-- Ranks funds by 3 year returns vs benchmark
SELECT
    scheme_name,
    fund_house,
    category,
    return_3yr_pct,
    benchmark_3yr_pct,
    ROUND(return_3yr_pct - benchmark_3yr_pct, 2) AS alpha_vs_benchmark
FROM fact_performance
ORDER BY return_3yr_pct DESC
LIMIT 10;


-- ── QUERY 7: Transaction Type Breakdown ─────────────────────
-- Splits total investment into SIP, Lumpsum, Redemption
SELECT
    transaction_type,
    COUNT(*)              AS total_count,
    SUM(amount_inr)       AS total_amount,
    ROUND(AVG(amount_inr), 2) AS avg_amount
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount DESC;


-- ── QUERY 8: Top Sectors in Portfolio Holdings ───────────────
-- Shows which sectors mutual funds invest in most
SELECT
    sector,
    COUNT(DISTINCT stock_symbol)  AS num_stocks,
    ROUND(SUM(weight_pct), 2)     AS total_weight_pct,
    ROUND(SUM(market_value_cr), 2) AS total_market_value_cr
FROM fact_portfolio
GROUP BY sector
ORDER BY total_market_value_cr DESC;


-- ── QUERY 9: NAV Growth of 5 Bluechip Funds ─────────────────
-- Compares how each bluechip fund's NAV has grown
SELECT
    n.amfi_code,
    f.scheme_name,
    MIN(n.nav)    AS nav_start,
    MAX(n.nav)    AS nav_latest,
    ROUND(
        ((MAX(n.nav) - MIN(n.nav)) / MIN(n.nav)) * 100, 2
    )             AS growth_pct
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
WHERE n.amfi_code IN (119551, 120503, 118632, 119092, 120841)
GROUP BY n.amfi_code, f.scheme_name
ORDER BY growth_pct DESC;


-- ── QUERY 10: Monthly Inflows by Category ────────────────────
-- Tracks which fund category attracts most money each month
SELECT
    month,
    category,
    net_inflow_crore,
    RANK() OVER (
        PARTITION BY month
        ORDER BY net_inflow_crore DESC
    ) AS rank_in_month
FROM fact_category
ORDER BY month, rank_in_month;