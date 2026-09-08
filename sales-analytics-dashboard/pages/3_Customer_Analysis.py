from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.calculations import calculate_total_customers, detect_columns
from utils.charts import bar_chart, line_chart
from utils.data_loader import get_active_dataframe
from utils.ui import format_currency, format_number, render_kpi_card, render_section_header


st.set_page_config(page_title="Customer Analysis", layout="wide")


def main() -> None:
    df = get_active_dataframe()
    if df.empty:
        st.warning("No customer data is available.")
        return

    cols = detect_columns(df)
    customer_col = cols.get("customer")
    sales_col = cols.get("sales")
    date_col = cols.get("date")

    if not customer_col:
        st.info("No customer column was detected in the current dataset, so customer analytics cannot be generated.")
        return

    customer_summary = df.groupby(customer_col, dropna=False).agg(
        Revenue=(sales_col if sales_col else customer_col, lambda s: float(s.sum()) if pd.api.types.is_numeric_dtype(s) else len(s)),
        Orders=(customer_col, "count"),
    ).reset_index().rename(columns={customer_col: "Customer"})

    if sales_col:
        customer_summary["Revenue"] = pd.to_numeric(customer_summary["Revenue"], errors="coerce").fillna(0)
    customer_summary["Orders"] = pd.to_numeric(customer_summary["Orders"], errors="coerce").fillna(0)
    customer_summary = customer_summary.sort_values(["Revenue" if sales_col else "Orders", "Orders"], ascending=False)

    total_customers = calculate_total_customers(df)
    avg_revenue = customer_summary["Revenue"].mean() if sales_col else 0
    top_customer = customer_summary.iloc[0]["Customer"] if not customer_summary.empty else "N/A"
    top_customer_revenue = customer_summary.iloc[0]["Revenue"] if not customer_summary.empty else 0

    metric_cols = st.columns(4)
    with metric_cols[0]:
        render_kpi_card("Total Customers", format_number(total_customers), "Active customer base", "#2563eb")
    with metric_cols[1]:
        render_kpi_card("Avg Revenue per Customer", format_currency(avg_revenue), "Average customer value", "#7c3aed")
    with metric_cols[2]:
        render_kpi_card("Top Customer", str(top_customer), f"{format_currency(top_customer_revenue)} revenue", "#0ea5e9")
    with metric_cols[3]:
        render_kpi_card("Customer Order Frequency", f"{customer_summary['Orders'].mean():.1f}", "Orders per customer on average", "#16a34a")

    render_section_header("Customer Value", "Review which customers contribute the most revenue and order volume.")
    c1, c2 = st.columns(2)
    with c1:
        top_by_revenue = customer_summary.head(10).rename(columns={"Customer": "Customer", "Revenue": "Revenue"})
        st.plotly_chart(bar_chart(top_by_revenue, "Customer", "Revenue", "Top Customers by Revenue", horizontal=True), use_container_width=True)
    with c2:
        top_by_orders = customer_summary.head(10).rename(columns={"Customer": "Customer", "Orders": "Orders"})
        st.plotly_chart(bar_chart(top_by_orders, "Customer", "Orders", "Top Customers by Orders", horizontal=True), use_container_width=True)

    render_section_header("Customer Distribution", "Understand concentration and distribution of customer spend.")
    dist_col1, dist_col2 = st.columns(2)
    if sales_col:
        customer_dist = customer_summary[["Customer", "Revenue"]].copy()
        with dist_col1:
            st.plotly_chart(bar_chart(customer_dist.head(20), "Customer", "Revenue", "Customer Revenue Distribution", horizontal=True), use_container_width=True)
    else:
        with dist_col1:
            st.info("Customer revenue is not available for distribution analysis.")

    if date_col and sales_col:
        trend_df = df[[customer_col, date_col, sales_col]].copy()
        trend_df[date_col] = pd.to_datetime(trend_df[date_col], errors="coerce")
        trend_df = trend_df.dropna(subset=[date_col])
        trend_df = trend_df.groupby(pd.Grouper(key=date_col, freq="M")).agg(Revenue=(sales_col, "sum")).reset_index()
        trend_df.columns = ["Month", "Revenue"]
        with dist_col2:
            st.plotly_chart(line_chart(trend_df, "Month", "Revenue", "Customer Sales Trend"), use_container_width=True)
    else:
        with dist_col2:
            st.info("A valid date and revenue column are required for customer sales trend analysis.")

    st.subheader("Customer Detail Table")
    search_term = st.text_input("Search customer", placeholder="Type a customer name")
    searchable = customer_summary.copy()
    if search_term:
        searchable = searchable[searchable["Customer"].str.contains(search_term, case=False, na=False)]
    st.dataframe(searchable, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
