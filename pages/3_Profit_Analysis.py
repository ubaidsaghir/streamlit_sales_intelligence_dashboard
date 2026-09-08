import plotly.express as px
import streamlit as st

from utils.components import empty_state, kpi_card
from utils.data_loader import get_active_data
from utils.export import render_csv_download
from utils.filters import render_dashboard_filters
from utils.ui import section_header, style_plotly_figure


dataframe = get_active_data()
filtered_data = render_dashboard_filters(dataframe=dataframe, key_prefix="profit")

if filtered_data.empty:
    empty_state(title="No profit records found", description="Adjust the filters to include more records.", icon="🔍")
    st.stop()

total_profit = filtered_data["Profit"].sum()
average_profit = filtered_data["Profit"].mean()
total_sales = filtered_data["Sales"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0
product_profit = filtered_data.groupby("Product")["Profit"].sum()
top_product = product_profit.idxmax() if not product_profit.empty else "N/A"

section_header("Profitability Performance", "Key profit indicators for the selected filters.")

metric1, metric2, metric3, metric4 = st.columns(4)
with metric1:
    kpi_card("Total Profit", f"${total_profit:,.0f}", "💰", "Filtered reporting period")
with metric2:
    kpi_card("Average Profit", f"${average_profit:,.2f}", "🧾", "Average profit per record")
with metric3:
    kpi_card("Profit Margin", f"{profit_margin:.1f}%", "📊", "Profit divided by sales")
with metric4:
    kpi_card("Top Product", top_product, "🏆", "Highest total profit")

download_column, info_column = st.columns([1, 3])
with download_column:
    render_csv_download(dataframe=filtered_data, file_name="filtered_profit_data.csv", label="Download profit data", key="download_profit_data")
with info_column:
    st.info(f"The downloaded CSV will contain **{len(filtered_data):,} filtered records**.")

section_header("Profitability Visualizations", "Analyze profit trends and performance drivers.")

trend_tab, breakdown_tab, relationship_tab = st.tabs(["Profit Trend", "Business Breakdown", "Sales vs Profit"])

with trend_tab:
    monthly_profit = (
        filtered_data.assign(Month=filtered_data["Order_Date"].dt.to_period("M").astype(str))
        .groupby("Month", as_index=False)["Profit"]
        .sum()
        .sort_values("Month")
    )
    trend_figure = px.area(monthly_profit, x="Month", y="Profit", title="Monthly Profit Trend", labels={"Month": "Reporting Month", "Profit": "Profit Amount"})
    st.plotly_chart(style_plotly_figure(trend_figure), width="stretch")

with breakdown_tab:
    left_chart, right_chart = st.columns(2)
    profit_by_product = filtered_data.groupby("Product", as_index=False)["Profit"].sum().sort_values("Profit", ascending=False)
    profit_by_region = filtered_data.groupby("Region", as_index=False)["Profit"].sum().sort_values("Profit", ascending=False)

    with left_chart:
        product_figure = px.bar(profit_by_product, x="Profit", y="Product", orientation="h", title="Profit by Product")
        st.plotly_chart(style_plotly_figure(product_figure), width="stretch")

    with right_chart:
        region_figure = px.pie(profit_by_region, names="Region", values="Profit", hole=0.48, title="Profit Share by Region")
        st.plotly_chart(style_plotly_figure(region_figure), width="stretch")

with relationship_tab:
    relationship_figure = px.scatter(
        filtered_data,
        x="Sales",
        y="Profit",
        color="Region",
        symbol="Product",
        hover_data=["Order_ID", "Customer", "Order_Date"],
        title="Sales and Profit Relationship",
    )
    st.plotly_chart(style_plotly_figure(relationship_figure, height=520), width="stretch")
