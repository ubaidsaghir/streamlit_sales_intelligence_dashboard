import plotly.express as px
import streamlit as st

from utils.components import empty_state, kpi_card
from utils.data_loader import get_active_data
from utils.export import render_csv_download
from utils.filters import render_dashboard_filters
from utils.ui import section_header, style_plotly_figure


dataframe = get_active_data()
filtered_data = render_dashboard_filters(dataframe=dataframe, key_prefix="sales")

if filtered_data.empty:
    empty_state(title="No sales records found", description="Adjust the filters to include more records.", icon="🔍")
    st.stop()

total_sales = filtered_data["Sales"].sum()
average_sale = filtered_data["Sales"].mean()
total_orders = filtered_data["Order_ID"].nunique()
region_totals = filtered_data.groupby("Region")["Sales"].sum()
top_region = region_totals.idxmax() if not region_totals.empty else "N/A"

section_header("Sales Performance", "Key sales indicators for the selected filters.")

metric1, metric2, metric3, metric4 = st.columns(4)
with metric1:
    kpi_card("Total Sales", f"${total_sales:,.0f}", "💵", "Filtered reporting period")
with metric2:
    kpi_card("Average Sale", f"${average_sale:,.2f}", "🧾", "Average transaction value")
with metric3:
    kpi_card("Total Orders", f"{total_orders:,}", "🛒", "Unique orders")
with metric4:
    kpi_card("Top Region", top_region, "🌍", "Highest sales contribution")

download_column, info_column = st.columns([1, 3])
with download_column:
    render_csv_download(dataframe=filtered_data, file_name="filtered_sales_data.csv", label="Download sales data", key="download_sales_data")
with info_column:
    st.info(f"The downloaded CSV will contain **{len(filtered_data):,} filtered records**.")

section_header("Sales Visualizations", "Explore sales trends and business segment performance.")

trend_tab, breakdown_tab, customers_tab = st.tabs(["Sales Trend", "Regional & Product Breakdown", "Customer Analysis"])

with trend_tab:
    monthly_sales = (
        filtered_data.assign(Month=filtered_data["Order_Date"].dt.to_period("M").astype(str))
        .groupby("Month", as_index=False)["Sales"]
        .sum()
        .sort_values("Month")
    )
    trend_figure = px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend",
        labels={"Month": "Reporting Month", "Sales": "Sales Amount"},
    )
    st.plotly_chart(style_plotly_figure(trend_figure), width="stretch")

with breakdown_tab:
    left_chart, right_chart = st.columns(2)
    sales_by_region = filtered_data.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    sales_by_product = filtered_data.groupby("Product", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)

    with left_chart:
        region_figure = px.bar(sales_by_region, x="Region", y="Sales", title="Sales by Region")
        st.plotly_chart(style_plotly_figure(region_figure), width="stretch")

    with right_chart:
        product_figure = px.bar(sales_by_product, x="Sales", y="Product", orientation="h", title="Sales by Product")
        st.plotly_chart(style_plotly_figure(product_figure), width="stretch")

with customers_tab:
    customer_sales = (
        filtered_data.groupby("Customer", as_index=False)
        .agg(Total_Sales=("Sales", "sum"), Orders=("Order_ID", "nunique"), Average_Sale=("Sales", "mean"))
        .sort_values("Total_Sales", ascending=False)
    )
    customer_figure = px.bar(customer_sales.head(10), x="Total_Sales", y="Customer", orientation="h", title="Top Customers by Sales")
    st.plotly_chart(style_plotly_figure(customer_figure), width="stretch")
    st.dataframe(customer_sales, width="stretch", hide_index=True)
