# 📊 Retail Sales Analysis Dashboard

**Junior Data Analyst Portfolio Project**

Real-world style end-to-end project:
**Python (data generation + cleaning) → SQLite (SQL analysis) → Streamlit Dashboard (visualizations)**

---

## Project Overview

This project simulates a typical junior Data Analyst workflow found in e-commerce / retail companies:

1. **Generate & clean** realistic sales data with Python (Pandas)
2. **Load** the cleaned data into a SQLite database
3. **Write business SQL queries** for KPIs, trends, segment analysis, discount impact etc.
4. **Build an interactive dashboard** with Streamlit + Plotly

### Dataset
- 5,000 synthetic order lines
- Period: 2024 – 2025
- Dimensions: Region, Category, Sub-Category, Customer Segment, Ship Mode
- Metrics: Sales, Profit, Quantity, Discount, Profit Margin, Days to Ship

---

## Project Structure

```
retail-sales-analysis/
├── data/
│   ├── retail_sales_cleaned.csv   # Cleaned data (generated)
│   └── retail_sales.db            # SQLite database (generated)
├── scripts/
│   └── generate_and_process_data.py
├── sql/
│   └── analysis_queries.sql       # Ready-to-run business queries
├── dashboard/
│   └── app.py                     # Streamlit dashboard
├── requirements.txt
└── README.md
```

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate data (creates CSV + SQLite DB)
```bash
python scripts/generate_and_process_data.py
```

### 3. Launch the dashboard
```bash
streamlit run dashboard/app.py
```

The dashboard will open in your browser with interactive filters (Year, Region, Category, Segment).

---

## SQL Queries Included

The file `sql/analysis_queries.sql` contains 12 practical queries:

| # | Query | Business Use |
|---|-------|--------------|
| 1 | Overall KPIs | Executive summary |
| 2 | Sales & Profit by Year | YoY view |
| 3 | Monthly Sales Trend | Time series |
| 4 | Sales by Region | Geographic performance |
| 5 | Category Performance | Product mix |
| 6 | Top 10 Sub-Categories | Ranking |
| 7 | Customer Segment Analysis | Who buys most |
| 8 | Shipping Mode Performance | Operations |
| 9 | Region × Category | Cross analysis |
| 10 | Top profitable products | Product focus |
| 11 | Discount impact | Pricing insight |
| 12 | Year-over-Year growth | Growth tracking |

You can run them directly against `data/retail_sales.db` with any SQLite client or Python.

---

## Skills Demonstrated

- **Python**: Pandas data generation, cleaning, feature engineering
- **SQL**: Aggregations, CASE, CTEs, business logic
- **Visualization**: Interactive dashboard (Streamlit + Plotly)
- **Data Pipeline**: Generate → Clean → SQLite → Dashboard
- **Business sense**: Profit margin, discount impact, segment analysis

---

## Author

Junior Data Analyst portfolio project  
Created as a realistic end-to-end example (Python → SQL → Dashboard)

Feel free to fork, improve or use as a template for your own portfolio.
