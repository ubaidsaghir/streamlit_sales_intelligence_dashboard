from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.calculations import calculate_profit_margin, detect_columns
from utils.charts import bar_chart, line_chart
from utils.data_loader import get_active_dataframe
from utils.ui import format_currency, format_percent, render_kpi_card, render_section_header


st.set_page_config(page_title="Profitability", layout="wide")


def main() -> None:
    df = get_active_dataframe()
    if df.empty:
        st.warning("No data available for profitability analysis.")
        return

    cols = detect_columns(df)
    if not cols["profit"]:
        st.info("No profit column is available in this dataset, so profitability metrics cannot be computed.")
        return

    profit_col = cols["profit"]
    sales_col = cols["sales"]
    category_col = cols["category"]
    region_col = cols["region"]
    product_col = cols["product"]
    date_col = cols["date"]

    df = df.copy()
    df[profit_col] = pd.to_numeric(df[profit_col], errors="coerce")
    if sales_col:
        df[sales_col] = pd.to_numeric(df[sales_col], errors="coerce")

    total_profit = df[profit_col].sum()
    margin = calculate_profit_margin(df)
    avg_profit_per_order = df[profit_col].mean() if not df.empty else 0

    profitable_category = df.groupby(category_col if category_col else profit_col, dropna=False)[profit_col].sum().reset_index().sort_values(profit_col, ascending=False).head(1) if category_col else pd.DataFrame(columns=["Category", "Profit"])
    profitable_product = df.groupby(product_col if product_col else profit_col, dropna=False)[profit_col].sum().reset_index().sort_values(profit_col, ascending=False).head(1) if product_col else pd.DataFrame(columns=["Product", "Profit"])

    metric_cols = st.columns(4)
    with metric_cols[0]:
        render_kpi_card("Total Profit", format_currency(total_profit), "Net contribution across records", "#16a34a")
    with metric_cols[1]:
        render_kpi_card("Profit Margin", format_percent(margin if margin is not None else 0), "Profit relative to sales", "#2563eb")
    with metric_cols[2]:
        render_kpi_card("Avg Profit per Order", format_currency(avg_profit_per_order), "Per transaction average", "#7c3aed")
    with metric_cols[3]:
        render_kpi_card("Top Category", profitable_category.iloc[0][0] if not profitable_category.empty else "N/A", f"{format_currency(profitable_category.iloc[0][1]) if not profitable_category.empty else '0'} profit", "#f59e0b")

    render_section_header("Profitability Performance", "Review trends, categories and regional profit distribution.")
    p1, p2 = st.columns(2)
    if date_col:
        profit_trend = df.copy()
        profit_trend[date_col] = pd.to_datetime(profit_trend[date_col], errors="coerce")
        profit_trend = profit_trend.dropna(subset=[date_col])
        profit_trend = profit_trend.groupby(pd.Grouper(key=date_col, freq="M"))[profit_col].sum().reset_index()
        profit_trend.columns = ["Date", "Profit"]
        with p1:
            st.plotly_chart(line_chart(profit_trend, "Date", "Profit", "Profit Trend"), use_container_width=True)
    else:
        with p1:
            st.info("A valid date column is not available for profit trend analysis.")

    if category_col:
        category_profit = df.groupby(category_col, dropna=False)[profit_col].sum().reset_index().rename(columns={category_col: "Category", profit_col: "Profit"})
        with p2:
            st.plotly_chart(bar_chart(category_profit, "Category", "Profit", "Profit by Category"), use_container_width=True)
    else:
        with p2:
            st.info("A category field is not available for category-level profitability.")

    render_section_header("Regional and Product Contribution", "Highlight where profitability is strongest and where it needs attention.")
    p3, p4 = st.columns(2)
    if region_col:
        region_profit = df.groupby(region_col, dropna=False)[profit_col].sum().reset_index().rename(columns={region_col: "Region", profit_col: "Profit"})
        with p3:
            st.plotly_chart(bar_chart(region_profit, "Region", "Profit", "Profit by Region", horizontal=True), use_container_width=True)
    else:
        with p3:
            st.info("No region column is available for regional profitability analysis.")

    if product_col:
        product_profit = df.groupby(product_col, dropna=False)[profit_col].sum().reset_index().rename(columns={product_col: "Product", profit_col: "Profit"}).sort_values("Profit", ascending=False).head(20)
        with p4:
            st.plotly_chart(bar_chart(product_profit, "Product", "Profit", "Profit by Product", horizontal=True), use_container_width=True)
    else:
        with p4:
            st.info("No product column is available for product-level profitability analysis.")

    st.subheader("Profitability Summary")
    if category_col:
        summary = df.groupby(category_col, dropna=False).agg(
            Profit=(profit_col, "sum"),
            Sales=(sales_col if sales_col else profit_col, lambda s: float(s.sum()) if pd.api.types.is_numeric_dtype(s) else 0),
        ).reset_index().rename(columns={category_col: "Category"})
        if sales_col:
            summary["Margin"] = (summary["Profit"] / summary["Sales"].replace(0, pd.NA)) * 100
        else:
            summary["Margin"] = 0
        st.dataframe(summary.sort_values("Profit", ascending=False), use_container_width=True)


if __name__ == "__main__":
    main()
