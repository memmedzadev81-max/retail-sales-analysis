"""
Retail Sales Data Pipeline
==========================
Real-world style junior Data Analyst project:
1. Generate realistic synthetic sales data (like Superstore / e-commerce)
2. Clean & transform with Pandas
3. Load into SQLite database
4. Ready for SQL analysis + Streamlit dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "retail_sales.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

# ------------------------------------------------------------------
# 1. Generate realistic synthetic data
# ------------------------------------------------------------------
print("Generating realistic retail sales data...")

n_rows = 5000

# Categories & products (typical e-commerce / superstore)
categories = {
    "Furniture": ["Bookcases", "Chairs", "Tables", "Furnishings"],
    "Office Supplies": ["Binders", "Paper", "Storage", "Art", "Envelopes", "Labels", "Fasteners"],
    "Technology": ["Phones", "Accessories", "Machines", "Copiers"]
}

regions = ["East", "West", "Central", "South"]
segments = ["Consumer", "Corporate", "Home Office"]
ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]

# Date range: last 2 years
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_range = (end_date - start_date).days

rows = []
for i in range(n_rows):
    cat = np.random.choice(list(categories.keys()))
    subcat = np.random.choice(categories[cat])
    region = np.random.choice(regions, p=[0.28, 0.32, 0.22, 0.18])
    segment = np.random.choice(segments, p=[0.52, 0.30, 0.18])
    ship_mode = np.random.choice(ship_modes, p=[0.55, 0.22, 0.15, 0.08])

    order_date = start_date + timedelta(days=np.random.randint(0, date_range + 1))
    ship_date = order_date + timedelta(days=np.random.randint(1, 8))

    # Realistic price & quantity
    if cat == "Furniture":
        unit_price = round(np.random.uniform(50, 800), 2)
        qty = np.random.randint(1, 6)
    elif cat == "Technology":
        unit_price = round(np.random.uniform(30, 1200), 2)
        qty = np.random.randint(1, 5)
    else:
        unit_price = round(np.random.uniform(5, 150), 2)
        qty = np.random.randint(1, 12)

    sales = round(unit_price * qty, 2)
    discount = round(np.random.choice([0, 0.05, 0.1, 0.15, 0.2, 0.3], p=[0.4, 0.2, 0.15, 0.1, 0.1, 0.05]), 2)
    profit = round(sales * (1 - discount) * np.random.uniform(0.08, 0.35) - sales * discount * 0.3, 2)

    rows.append({
        "order_id": f"ORD-{20240000 + i}",
        "order_date": order_date.strftime("%Y-%m-%d"),
        "ship_date": ship_date.strftime("%Y-%m-%d"),
        "ship_mode": ship_mode,
        "customer_id": f"CUS-{np.random.randint(1000, 9999)}",
        "segment": segment,
        "region": region,
        "category": cat,
        "sub_category": subcat,
        "product_name": f"{subcat} Model {np.random.randint(100, 999)}",
        "quantity": qty,
        "unit_price": unit_price,
        "sales": sales,
        "discount": discount,
        "profit": profit
    })

df = pd.DataFrame(rows)

# ------------------------------------------------------------------
# 2. Basic cleaning / feature engineering (real pipeline style)
# ------------------------------------------------------------------
print("Cleaning and transforming data...")

df["order_date"] = pd.to_datetime(df["order_date"])
df["ship_date"] = pd.to_datetime(df["ship_date"])
df["days_to_ship"] = (df["ship_date"] - df["order_date"]).dt.days
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.strftime("%B")
df["quarter"] = df["order_date"].dt.quarter
df["profit_margin"] = round(df["profit"] / df["sales"] * 100, 2)

# Remove any negative sales (shouldn't happen but real data hygiene)
df = df[df["sales"] > 0].copy()

# Save cleaned CSV
csv_path = DATA_DIR / "retail_sales_cleaned.csv"
df.to_csv(csv_path, index=False)
print(f"Cleaned CSV saved → {csv_path}")
print(f"Shape: {df.shape}")
print(df.head(3).to_string())

# ------------------------------------------------------------------
# 3. Load into SQLite
# ------------------------------------------------------------------
print("\nLoading data into SQLite...")

conn = sqlite3.connect(DB_PATH)

# Drop if exists (for re-runs)
conn.execute("DROP TABLE IF EXISTS sales")

df.to_sql("sales", conn, index=False, if_exists="replace")

# Create useful indexes (real practice)
conn.execute("CREATE INDEX IF NOT EXISTS idx_order_date ON sales(order_date)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_region ON sales(region)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON sales(category)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_segment ON sales(segment)")

conn.commit()
conn.close()

print(f"SQLite database ready → {DB_PATH}")
print("Done! Pipeline finished successfully.")
