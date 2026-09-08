from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.calculations import detect_columns, get_top_products
from utils.charts import bar_chart
from utils.data_loader import get_active_dataframe
from utils.ui import format_currency, format_number, format_percent, render_kpi_card, render_section_header


st.set_page_config(page_title="Product Analysis", layout="wide")


def prepare_product_data(df: pd.DataFrame) -> pd.DataFrame:
    cols = detect_columns(df)
    working = df.copy()
    if cols["sales"]:
        working[cols["sales"]] = pd.to_numeric(working[cols["sales"]], errors="coerce")
    if cols["profit"]:
        working[cols["profit"]] = pd.to_numeric(working[cols["profit"]], errors="coerce")
    if cols["quantity"]:
        working[cols["quantity"]] = pd.to_numeric(working[cols["quantity"]], errors="coerce")
    return working


def main() -> None:
    df = prepare_product_data(get_active_dataframe())
    if df.empty:
        st.warning("No product data is available.")
        return

    cols = detect_columns(df)

    total_products = df[cols["product"]].nunique() if cols["product"] else 0
    best_selling = get_top_products(df, limit=1)
    best_selling_name = best_selling["Product"].iloc[0] if not best_selling.empty else "N/A"
    best_selling_sales = best_selling["Sales"].iloc[0] if not best_selling.empty else 0

    highest_revenue = df.groupby(cols["product"], dropna=False)[cols["sales"]].sum().reset_index().sort_values(cols["sales"], ascending=False).head(1) if cols["sales"] and cols["product"] else pd.DataFrame(columns=["Product", "Sales"])
    highest_revenue_product = highest_revenue.iloc[0][cols["product"]] if not highest_revenue.empty else "N/A"
    highest_revenue_value = highest_revenue.iloc[0][cols["sales"]] if not highest_revenue.empty else 0

    most_profitable = df.groupby(cols["product"], dropna=False)[cols["profit"]].sum().reset_index().sort_values(cols["profit"], ascending=False).head(1) if cols["profit"] and cols["product"] else pd.DataFrame(columns=["Product", "Profit"])
    most_profitable_product = most_profitable.iloc[0][cols["product"]] if not most_profitable.empty else "N/A"
    most_profitable_value = most_profitable.iloc[0][cols["profit"]] if not most_profitable.empty else 0

    metric_cols = st.columns(5)
    with metric_cols[0]:
        render_kpi_card("Total Products", format_number(total_products), "Distinct products in the dataset", "#2563eb")
    with metric_cols[1]:
        render_kpi_card("Best Seller", str(best_selling_name), f"{format_currency(best_selling_sales)} sales", "#0ea5e9")
    with metric_cols[2]:
        render_kpi_card("Highest Revenue Product", str(highest_revenue_product), f"{format_currency(highest_revenue_value)} revenue", "#7c3aed")
    with metric_cols[3]:
        render_kpi_card("Most Profitable Product", str(most_profitable_product), f"{format_currency(most_profitable_value)} profit", "#16a34a")
    with metric_cols[4]:
        render_kpi_card("Lowest Performance", "Review below", "See product detail table", "#f59e0b")

    render_section_header("Product Performance", "Compare sales and profitability across the product portfolio.")
    chart_col1, chart_col2 = st.columns(2)

    top_products = get_top_products(df, limit=10)
    with chart_col1:
        st.plotly_chart(bar_chart(top_products, "Product", "Sales", "Top 10 Products by Sales", horizontal=True), use_container_width=True)

    if cols["profit"] and cols["product"]:
        profit_by_product = df.groupby(cols["product"], dropna=False)[cols["profit"]].sum().reset_index().sort_values(cols["profit"], ascending=False).head(10)
        profit_by_product.columns = ["Product", "Profit"]
        with chart_col2:
            st.plotly_chart(bar_chart(profit_by_product, "Product", "Profit", "Top 10 Products by Profit", horizontal=True), use_container_width=True)
    else:
        with chart_col2:
            st.info("Profit data is not available for product profit ranking.")

    render_section_header("Category Mix", "Understand category concentration and contribution by sales and profit.")
    cat_col1, cat_col2 = st.columns(2)

    if cols["category"] and cols["sales"]:
        sales_category = df.groupby(cols["category"], dropna=False)[cols["sales"]].sum().reset_index().rename(columns={cols["category"]: "Category", cols["sales"]: "Sales"})
        with cat_col1:
            st.plotly_chart(bar_chart(sales_category, "Category", "Sales", "Sales by Category"), use_container_width=True)
    else:
        with cat_col1:
            st.info("No category/sales data available.")

    if cols["category"] and cols["profit"]:
        profit_category = df.groupby(cols["category"], dropna=False)[cols["profit"]].sum().reset_index().rename(columns={cols["category"]: "Category", cols["profit"]: "Profit"})
        with cat_col2:
            st.plotly_chart(bar_chart(profit_category, "Category", "Profit", "Profit by Category"), use_container_width=True)
    else:
        with cat_col2:
            st.info("No category/profit data available.")

    render_section_header("Product Performance Detail", "Detailed product attributes and profitability metrics.")
    product_table = df.copy()
    if cols["product"]:
        product_table = product_table.groupby(cols["product"], dropna=False).agg(
            Category=(cols["category"] if cols["category"] else cols["product"], lambda s: s.dropna().iloc[0] if not s.dropna().empty else "N/A"),
            Quantity=(cols["quantity"] if cols["quantity"] else cols["product"], lambda s: float(s.sum()) if pd.api.types.is_numeric_dtype(s) else len(s)),
            Sales=(cols["sales"] if cols["sales"] else cols["product"], lambda s: float(s.sum()) if pd.api.types.is_numeric_dtype(s) else len(s)),
            Profit=(cols["profit"] if cols["profit"] else cols["product"], lambda s: float(s.sum()) if pd.api.types.is_numeric_dtype(s) else 0),
        ).reset_index().rename(columns={cols["product"]: "Product"})
        if cols["sales"] and cols["profit"]:
            product_table["Profit Margin"] = (product_table["Profit"] / product_table["Sales"].replace(0, pd.NA)) * 100
        else:
            product_table["Profit Margin"] = 0
        st.dataframe(product_table.sort_values("Sales", ascending=False).head(50), use_container_width=True)
    else:
        st.info("No product column detected. Product detail table cannot be generated.")


if __name__ == "__main__":
    main()
