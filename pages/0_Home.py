import streamlit as st

from utils.components import kpi_card, navigation_card
from utils.data_loader import get_active_data, get_active_source
from utils.filters import render_dashboard_filters
from utils.formatters import compact_filename
from utils.ui import section_header


dataframe = get_active_data()
active_source = get_active_source()
filtered_data = render_dashboard_filters(dataframe=dataframe, key_prefix="home")

minimum_date = filtered_data["Order_Date"].min()
maximum_date = filtered_data["Order_Date"].max()
date_coverage = f"{minimum_date:%b %Y} – {maximum_date:%b %Y}"

section_header("Dashboard Overview", "A summary of the active dataset and available analytics modules.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    kpi_card(
        label="Data Source",
        value=compact_filename(active_source, max_length=26),
        icon="🗂️",
        helper="Current dashboard dataset",
        compact_value=True,
        tooltip=active_source,
    )
with col2:
    kpi_card(label="Records Shown", value=f"{len(filtered_data):,}", icon="📑", helper=f"Filtered from {len(dataframe):,} records")
with col3:
    kpi_card(label="Date Coverage", value=date_coverage, icon="📅", helper="Available reporting period")
with col4:
    kpi_card(label="Dashboard Status", value="Operational", icon="✅", helper="All analytics pages available")

section_header("Quick Business Insights", "Automatically calculated from the active dataset.")

total_sales = filtered_data["Sales"].sum()
total_profit = filtered_data["Profit"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0
region_sales = filtered_data.groupby("Region")["Sales"].sum()
top_region = region_sales.idxmax() if not region_sales.empty else "N/A"
product_sales = filtered_data.groupby("Product")["Sales"].sum()
top_product = product_sales.idxmax() if not product_sales.empty else "N/A"

insight1, insight2, insight3, insight4 = st.columns(4)
with insight1:
    kpi_card("Total Sales", f"${total_sales:,.0f}", "💵", "Across all transactions")
with insight2:
    kpi_card("Total Profit", f"${total_profit:,.0f}", "💰", "Across all transactions")
with insight3:
    kpi_card("Profit Margin", f"{profit_margin:.1f}%", "📊", "Profit as a percentage of sales")
with insight4:
    kpi_card("Top Region", top_region, "🌍", f"Top product: {top_product}")

section_header("Explore the Workspace", "Open a dashboard page to begin analyzing the dataset.")

left_column, right_column = st.columns(2)
with left_column:
    navigation_card(title="Data Overview", description="Review columns, types, missing values, duplicates, and record quality.", page="pages/1_Data_Overview.py", icon="📋")
    navigation_card(title="Sales Analysis", description="Analyze revenue by region, product, customer, and reporting period.", page="pages/2_Sales_Analysis.py", icon="📈")
with right_column:
    navigation_card(title="Profit Analysis", description="Review margin trends, profitability drivers, and business performance.", page="pages/3_Profit_Analysis.py", icon="💰")
    navigation_card(title="Upload Data", description="Upload another CSV and validate before activating it for the full dashboard.", page="pages/4_Upload_Data.py", icon="📤")
