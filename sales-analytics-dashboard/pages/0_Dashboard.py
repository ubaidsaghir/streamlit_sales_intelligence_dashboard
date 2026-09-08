from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.calculations import (
    calculate_average_order_value,
    calculate_profit_margin,
    calculate_total_customers,
    calculate_total_orders,
    calculate_total_sales,
    detect_columns,
    get_top_customers,
    get_top_products,
    get_top_regions,
)
from utils.charts import bar_chart, line_chart
from utils.data_loader import get_active_dataframe
from utils.ui import format_currency, format_number, format_percent, render_kpi_card, render_section_header


st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")


def prepare_dashboard_data(df: pd.DataFrame) -> pd.DataFrame:
    cols = detect_columns(df)
    working = df.copy()
    if cols["date"]:
        working[cols["date"]] = pd.to_datetime(working[cols["date"]], errors="coerce")
        working = working.dropna(subset=[cols["date"]])
    if cols["sales"]:
        working[cols["sales"]] = pd.to_numeric(working[cols["sales"]], errors="coerce")
    if cols["profit"]:
        working[cols["profit"]] = pd.to_numeric(working[cols["profit"]], errors="coerce")
    return working


def main() -> None:
    df = prepare_dashboard_data(get_active_dataframe())
    if df.empty:
        st.warning("No data available. Upload a CSV or restore the default dataset.")
        return

    cols = detect_columns(df)

    sales_total = calculate_total_sales(df) if cols["sales"] else float(len(df))
    order_total = calculate_total_orders(df)
    customer_total = calculate_total_customers(df)
    profit_total = 0.0 if cols["profit"] is None else pd.to_numeric(df[cols["profit"]], errors="coerce").fillna(0).sum()
    margin = calculate_profit_margin(df) if cols["sales"] and cols["profit"] else 0.0
    avg_order_value = calculate_average_order_value(df) if cols["sales"] else float(len(df) / max(order_total, 1))

    cols_kpi = st.columns(6)
    metrics = [
        ("Total Sales", format_currency(sales_total), "Revenue across all records", "#0f766e"),
        ("Total Orders", format_number(order_total), "Orders processed", "#2563eb"),
        ("Total Customers", format_number(customer_total), "Unique customer accounts", "#7c3aed"),
        ("Total Profit", format_currency(profit_total), "Net profit contribution", "#16a34a"),
        ("Profit Margin", format_percent(margin if margin is not None else 0.0), "Profit percentage", "#ea580c"),
        ("Average Order Value", format_currency(avg_order_value), "Average order size", "#0284c7"),
    ]
    for col, (label, value, delta, color) in zip(cols_kpi, metrics):
        with col:
            render_kpi_card(label, value, delta, color)

    render_section_header("Sales Performance", "Track order and revenue momentum over time.")
    sales_df = df.copy()
    if cols["date"]:
        sales_df[cols["date"]] = pd.to_datetime(sales_df[cols["date"]], errors="coerce")
        sales_df = sales_df.dropna(subset=[cols["date"]])
        sales_by_month = sales_df.groupby(pd.Grouper(key=cols["date"], freq="M")).agg(
            Sales=(cols["sales"] if cols["sales"] else cols["date"], lambda s: float(s.sum()) if pd.api.types.is_numeric_dtype(s) else len(s)),
            Orders=(cols["order_id"] if cols["order_id"] else cols["date"], lambda s: s.nunique() if s.dtype != "datetime64[ns]" else len(s)),
        ).reset_index()
    else:
        sales_by_month = pd.DataFrame({"Date": [pd.Timestamp.now()], "Sales": [len(df)], "Orders": [len(df)]})

    if sales_by_month.empty:
        sales_by_month = pd.DataFrame({"Date": [pd.Timestamp.now()], "Sales": [0], "Orders": [0]})
        sales_by_month.columns = ["Date", "Sales", "Orders"]

    sales_by_month = sales_by_month.rename(columns={sales_by_month.columns[0]: "Date"})
    if "Date" in sales_by_month.columns:
        sales_by_month["Date"] = pd.to_datetime(sales_by_month["Date"], errors="coerce")

    trend_col, orders_col = st.columns(2)
    with trend_col:
        st.plotly_chart(line_chart(sales_by_month, "Date", "Sales", "Sales Over Time"), use_container_width=True)
    with orders_col:
        st.plotly_chart(line_chart(sales_by_month, "Date", "Orders", "Orders Over Time", color="#7c3aed"), use_container_width=True)

    render_section_header("Business Breakdown", "Understand the mix of demand and sales contribution across trading dimensions.")
    breakdown_col1, breakdown_col2, breakdown_col3 = st.columns(3)

    if cols["region"]:
        region_data = df.groupby(cols["region"], dropna=False).agg(Sales=(cols["sales"] if cols["sales"] else cols["region"], lambda s: float(s.sum()) if pd.api.types.is_numeric_dtype(s) else len(s))).reset_index()
        region_data = region_data.rename(columns={cols["region"]: "Region"})
        with breakdown_col1:
            st.plotly_chart(bar_chart(region_data, "Region", "Sales", "Sales by Region", horizontal=True), use_container_width=True)
    else:
        with breakdown_col1:
            st.info("No region column detected in the current dataset.")

    if cols["category"]:
        category_data = df.groupby(cols["category"], dropna=False).agg(Sales=(cols["sales"] if cols["sales"] else cols["category"], lambda s: float(s.sum()) if pd.api.types.is_numeric_dtype(s) else len(s))).reset_index()
        category_data = category_data.rename(columns={cols["category"]: "Category"})
        with breakdown_col2:
            st.plotly_chart(bar_chart(category_data, "Category", "Sales", "Sales by Category"), use_container_width=True)
    else:
        with breakdown_col2:
            st.info("No category column detected in the current dataset.")

    product_data = get_top_products(df, limit=10)
    with breakdown_col3:
        st.plotly_chart(bar_chart(product_data, "Product", "Sales", "Sales by Product", horizontal=True), use_container_width=True)

    render_section_header("Profitability", "Monitor the profit contribution and margin profile by business segment.")
    profit_col1, profit_col2, profit_col3 = st.columns(3)
    if cols["category"] and cols["profit"]:
        profit_by_category = df.groupby(cols["category"], dropna=False)[cols["profit"]].sum().reset_index()
        profit_by_category.columns = ["Category", "Profit"]
        with profit_col1:
            st.plotly_chart(bar_chart(profit_by_category, "Category", "Profit", "Profit by Category"), use_container_width=True)
    else:
        with profit_col1:
            st.info("Profit or category data is not available for profitability breakdown.")

    if cols["product"] and cols["profit"]:
        profit_by_product = df.groupby(cols["product"], dropna=False)[cols["profit"]].sum().reset_index().sort_values(cols["profit"], ascending=False).head(10)
        profit_by_product.columns = ["Product", "Profit"]
        with profit_col2:
            st.plotly_chart(bar_chart(profit_by_product, "Product", "Profit", "Profit by Product", horizontal=True), use_container_width=True)
    else:
        with profit_col2:
            st.info("Product-level profit data is not available.")

    if cols["date"] and cols["profit"]:
        profit_trend = df.copy()
        profit_trend[cols["date"]] = pd.to_datetime(profit_trend[cols["date"]], errors="coerce")
        profit_trend = profit_trend.dropna(subset=[cols["date"]])
        profit_trend = profit_trend.groupby(pd.Grouper(key=cols["date"], freq="M"))[cols["profit"]].sum().reset_index()
        profit_trend.columns = ["Date", "Profit"]
        with profit_col3:
            st.plotly_chart(line_chart(profit_trend, "Date", "Profit", "Profit Trend", color="#16a34a"), use_container_width=True)
    else:
        with profit_col3:
            st.info("Date or profit data is not available to calculate profit trend.")

    render_section_header("Top Performers", "Identify the strongest contributors across product, customer and region dimensions.")
    performer_col1, performer_col2, performer_col3 = st.columns(3)
    with performer_col1:
        top_products = get_top_products(df, limit=10)
        st.dataframe(top_products.head(10), use_container_width=True, hide_index=True)
    with performer_col2:
        top_customers = get_top_customers(df, limit=10)
        st.dataframe(top_customers.head(10), use_container_width=True, hide_index=True)
    with performer_col3:
        top_regions = get_top_regions(df, limit=10)
        st.dataframe(top_regions.head(10), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
