"""
Retail Sales Dashboard
======================
Interactive Streamlit dashboard for the Retail Sales Analysis project.
Run: streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "retail_sales.db"

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM sales", conn)
    conn.close()
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df

df = load_data()

# ------------------------------------------------------------------
# Sidebar filters
# ------------------------------------------------------------------
st.sidebar.header("Filters")

years = sorted(df["year"].unique())
selected_years = st.sidebar.multiselect("Year", years, default=years)

regions = sorted(df["region"].unique())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)

categories = sorted(df["category"].unique())
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)

segments = sorted(df["segment"].unique())
selected_segments = st.sidebar.multiselect("Segment", segments, default=segments)

# Apply filters
mask = (
    df["year"].isin(selected_years) &
    df["region"].isin(selected_regions) &
    df["category"].isin(selected_categories) &
    df["segment"].isin(selected_segments)
)
filtered = df[mask].copy()

# ------------------------------------------------------------------
# Header + KPIs
# ------------------------------------------------------------------
st.title("📊 Retail Sales Analysis Dashboard")
st.caption("Junior Data Analyst Project • Python → SQL → Visualization")

if filtered.empty:
    st.warning("No data for the selected filters.")
    st.stop()

total_sales = filtered["sales"].sum()
total_profit = filtered["profit"].sum()
total_orders = len(filtered)
avg_margin = filtered["profit_margin"].mean()
total_units = filtered["quantity"].sum()

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Total Sales", f"${total_sales:,.0f}")
kpi2.metric("Total Profit", f"${total_profit:,.0f}")
kpi3.metric("Orders", f"{total_orders:,}")
kpi4.metric("Avg Margin", f"{avg_margin:.1f}%")
kpi5.metric("Units Sold", f"{total_units:,}")

st.divider()

# ------------------------------------------------------------------
# Row 1: Trend + Region
# ------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales Trend by Month")
    monthly = (
        filtered.groupby(["year", "month", "month_name"], as_index=False)
        .agg(sales=("sales", "sum"), profit=("profit", "sum"))
        .sort_values(["year", "month"])
    )
    monthly["period"] = monthly["year"].astype(str) + "-" + monthly["month"].astype(str).str.zfill(2)
    fig_trend = px.line(
        monthly, x="period", y="sales",
        markers=True, title=None,
        labels={"period": "Month", "sales": "Sales ($)"}
    )
    fig_trend.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=350)
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.subheader("Sales by Region")
    region_df = (
        filtered.groupby("region", as_index=False)
        .agg(sales=("sales", "sum"), profit=("profit", "sum"))
        .sort_values("sales", ascending=False)
    )
    fig_region = px.bar(
        region_df, x="region", y="sales", color="profit",
        color_continuous_scale="Teal",
        labels={"sales": "Sales ($)", "region": "Region", "profit": "Profit"}
    )
    fig_region.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=350)
    st.plotly_chart(fig_region, use_container_width=True)

# ------------------------------------------------------------------
# Row 2: Category + Segment
# ------------------------------------------------------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("Sales by Category")
    cat_df = (
        filtered.groupby("category", as_index=False)
        .agg(sales=("sales", "sum"), profit=("profit", "sum"))
    )
    fig_cat = px.pie(
        cat_df, values="sales", names="category",
        hole=0.45, color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_cat.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=350)
    st.plotly_chart(fig_cat, use_container_width=True)

with col4:
    st.subheader("Sales by Customer Segment")
    seg_df = (
        filtered.groupby("segment", as_index=False)
        .agg(sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "count"))
    )
    fig_seg = px.bar(
        seg_df, x="segment", y="sales", text="orders",
        color="segment", color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_seg.update_traces(textposition="outside")
    fig_seg.update_layout(showlegend=False, margin=dict(l=20, r=20, t=30, b=20), height=350)
    st.plotly_chart(fig_seg, use_container_width=True)

# ------------------------------------------------------------------
# Row 3: Sub-category ranking + Discount impact
# ------------------------------------------------------------------
col5, col6 = st.columns(2)

with col5:
    st.subheader("Top 10 Sub-Categories by Sales")
    sub_df = (
        filtered.groupby(["sub_category", "category"], as_index=False)
        .agg(sales=("sales", "sum"), profit=("profit", "sum"))
        .sort_values("sales", ascending=False)
        .head(10)
    )
    fig_sub = px.bar(
        sub_df, y="sub_category", x="sales", orientation="h",
        color="category",
        labels={"sales": "Sales ($)", "sub_category": ""}
    )
    fig_sub.update_layout(yaxis={"categoryorder": "total ascending"},
                          margin=dict(l=20, r=20, t=30, b=20), height=400)
    st.plotly_chart(fig_sub, use_container_width=True)

with col6:
    st.subheader("Discount Impact on Profit Margin")
    def discount_band(d):
        if d == 0:
            return "No Discount"
        elif d <= 0.10:
            return "Low (1-10%)"
        elif d <= 0.20:
            return "Medium (11-20%)"
        else:
            return "High (>20%)"

    filtered["discount_band"] = filtered["discount"].apply(discount_band)
    order = ["No Discount", "Low (1-10%)", "Medium (11-20%)", "High (>20%)"]
    disc_df = (
        filtered.groupby("discount_band", as_index=False)
        .agg(avg_margin=("profit_margin", "mean"), orders=("order_id", "count"))
    )
    disc_df["discount_band"] = pd.Categorical(disc_df["discount_band"], categories=order, ordered=True)
    disc_df = disc_df.sort_values("discount_band")

    fig_disc = px.bar(
        disc_df, x="discount_band", y="avg_margin",
        text="orders", color="avg_margin",
        color_continuous_scale="RdYlGn",
        labels={"avg_margin": "Avg Profit Margin %", "discount_band": "Discount Band"}
    )
    fig_disc.update_traces(textposition="outside")
    fig_disc.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=400)
    st.plotly_chart(fig_disc, use_container_width=True)

# ------------------------------------------------------------------
# Data table
# ------------------------------------------------------------------
st.divider()
st.subheader("Sample of Filtered Data")
st.dataframe(
    filtered[["order_id", "order_date", "region", "segment", "category",
              "sub_category", "sales", "profit", "profit_margin", "discount"]].head(100),
    use_container_width=True
)

st.caption("Data source: Synthetic retail sales (2024-2025) • Built with Python, SQLite, Streamlit & Plotly")
