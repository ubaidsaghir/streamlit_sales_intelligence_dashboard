from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.calculations import calculate_average_order_value, calculate_growth, calculate_total_orders, calculate_total_sales, detect_columns
from utils.charts import bar_chart, line_chart
from utils.data_loader import get_active_dataframe
from utils.ui import format_currency, format_number, format_percent, render_kpi_card, render_section_header


st.set_page_config(page_title="Sales Overview", layout="wide")


def prepare_sales_view(df: pd.DataFrame) -> pd.DataFrame:
    cols = detect_columns(df)
    working = df.copy()
    for key in ["date", "sales", "profit", "quantity", "product", "category", "customer", "region", "status"]:
        candidate = cols.get(key)
        if candidate and candidate in working.columns:
            if key == "date":
                working[candidate] = pd.to_datetime(working[candidate], errors="coerce")
            elif key in {"sales", "profit", "quantity"}:
                working[candidate] = pd.to_numeric(working[candidate], errors="coerce")
    return working.dropna(subset=[cols["date"]] if cols["date"] else []).copy()


def build_filters(df: pd.DataFrame) -> pd.DataFrame:
    cols = detect_columns(df)
    filtered = df.copy()

    if cols["date"]:
        min_date = filtered[cols["date"]].min().date()
        max_date = filtered[cols["date"]].max().date()
        start_date, end_date = st.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
        filtered = filtered[(filtered[cols["date"]].dt.date >= start_date) & (filtered[cols["date"]].dt.date <= end_date)]

    for filter_key, label in [("region", "Region"), ("category", "Category"), ("product", "Product"), ("status", "Order Status"), ("customer", "Customer")]:
        candidate_col = cols.get(filter_key)
        if candidate_col and candidate_col in filtered.columns:
            options = sorted(filtered[candidate_col].dropna().astype(str).unique())
            selected = st.multiselect(label, options, default=options)
            filtered = filtered[filtered[candidate_col].astype(str).isin(selected)]

    return filtered


def main() -> None:
    data = prepare_sales_view(get_active_dataframe())
    if data.empty:
        st.warning("No valid data is available for the sales overview page.")
        return

    filtered = build_filters(data)
    cols = detect_columns(filtered)

    total_sales = calculate_total_sales(filtered)
    total_orders = calculate_total_orders(filtered)
    avg_order = calculate_average_order_value(filtered)
    growth = calculate_growth(filtered, cols["date"])

    metric_cols = st.columns(4)
    with metric_cols[0]:
        render_kpi_card("Total Sales", format_currency(total_sales), "Revenue in selected period", "#2563eb")
    with metric_cols[1]:
        render_kpi_card("Total Orders", format_number(total_orders), "Transactions recorded", "#0ea5e9")
    with metric_cols[2]:
        render_kpi_card("Average Order Value", format_currency(avg_order), "Average basket size", "#8b5cf6")
    with metric_cols[3]:
        render_kpi_card("Growth", format_percent(growth), "Period-over-period change", "#16a34a")

    render_section_header("Sales Performance Trends", "Review daily and monthly movement across the selected period.")
    trend_col1, trend_col2 = st.columns(2)

    if cols["date"]:
        daily = filtered.copy()
        daily[cols["date"]] = pd.to_datetime(daily[cols["date"]], errors="coerce")
        daily = daily.dropna(subset=[cols["date"]])
        daily_sales = daily.groupby(pd.Grouper(key=cols["date"], freq="D")).agg(Sales=(cols["sales"] if cols["sales"] else cols["date"], lambda s: float(s.sum()) if pd.api.types.is_numeric_dtype(s) else len(s))).reset_index()
        daily_sales.columns = ["Date", "Sales"]
        with trend_col1:
            st.plotly_chart(line_chart(daily_sales, "Date", "Sales", "Daily Sales"), use_container_width=True)

        monthly_sales = daily.groupby(pd.Grouper(key=cols["date"], freq="M")).agg(Sales=(cols["sales"] if cols["sales"] else cols["date"], lambda s: float(s.sum()) if pd.api.types.is_numeric_dtype(s) else len(s))).reset_index()
        monthly_sales.columns = ["Month", "Sales"]
        with trend_col2:
            st.plotly_chart(line_chart(monthly_sales, "Month", "Sales", "Monthly Sales", color="#7c3aed"), use_container_width=True)
    else:
        st.warning("A valid date column is required for time-based sales trend analysis.")

    render_section_header("Segment Analysis", "Break down sales by region, category and order status.")
    segment_col1, segment_col2, segment_col3 = st.columns(3)

    if cols["region"]:
        region_summary = filtered.groupby(cols["region"], dropna=False).agg(Sales=(cols["sales"] if cols["sales"] else cols["region"], lambda s: float(s.sum()) if pd.api.types.is_numeric_dtype(s) else len(s))).reset_index().rename(columns={cols["region"]: "Region"})
        with segment_col1:
            st.plotly_chart(bar_chart(region_summary, "Region", "Sales", "Sales by Region", horizontal=True), use_container_width=True)
    else:
        with segment_col1:
            st.info("No region column is available in the active dataset.")

    if cols["category"]:
        category_summary = filtered.groupby(cols["category"], dropna=False).agg(Sales=(cols["sales"] if cols["sales"] else cols["category"], lambda s: float(s.sum()) if pd.api.types.is_numeric_dtype(s) else len(s))).reset_index().rename(columns={cols["category"]: "Category"})
        with segment_col2:
            st.plotly_chart(bar_chart(category_summary, "Category", "Sales", "Sales by Category"), use_container_width=True)
    else:
        with segment_col2:
            st.info("No category column is available in the active dataset.")

    if cols["status"]:
        status_summary = filtered.groupby(cols["status"], dropna=False).agg(Sales=(cols["sales"] if cols["sales"] else cols["status"], lambda s: float(s.sum()) if pd.api.types.is_numeric_dtype(s) else len(s))).reset_index().rename(columns={cols["status"]: "Order Status"})
        with segment_col3:
            st.plotly_chart(bar_chart(status_summary, "Order Status", "Sales", "Sales by Order Status"), use_container_width=True)
    else:
        with segment_col3:
            st.info("No order status column is available in the active dataset.")

    st.subheader("Filtered Sales Table")
    display_cols = [col for col in filtered.columns if col in {"Order ID", "Order Date", "CustomerName", "State", "City"} or "date" in col.lower() or "customer" in col.lower() or "region" in col.lower() or "category" in col.lower() or "product" in col.lower() or "sales" in col.lower() or "profit" in col.lower()]
    st.dataframe(filtered[display_cols].head(250) if display_cols else filtered.head(250), use_container_width=True)


if __name__ == "__main__":
    main()
