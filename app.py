import streamlit as st

from utils.navigation import render_top_navigation
from utils.ui import apply_global_styles, page_footer, page_header


st.set_page_config(
    page_title="Northstar Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

home_page = st.Page("pages/0_Home.py", title="Home", icon="🏠", default=True)
overview_page = st.Page("pages/1_Data_Overview.py", title="Data Overview", icon="📋", url_path="data-overview")
sales_page = st.Page("pages/2_Sales_Analysis.py", title="Sales Analysis", icon="📈", url_path="sales-analysis")
profit_page = st.Page("pages/3_Profit_Analysis.py", title="Profit Analysis", icon="💰", url_path="profit-analysis")
upload_page = st.Page("pages/4_Upload_Data.py", title="Upload Data", icon="📤", url_path="upload-data")

current_page = st.navigation(
    [home_page, overview_page, sales_page, profit_page, upload_page],
    position="hidden",
)

page_metadata = {
    "Home": {
        "title": "Sales Intelligence Dashboard",
        "subtitle": "Explore revenue, profitability, customer behavior, and operational trends from one modern analytics workspace.",
        "icon": "📊",
        "eyebrow": "Business Intelligence",
    },
    "Data Overview": {
        "title": "Data Overview",
        "subtitle": "Inspect the active dataset structure, quality signals, and field-level health before deeper analysis.",
        "icon": "📋",
        "eyebrow": "Dataset Inspection",
    },
    "Sales Analysis": {
        "title": "Sales Analysis",
        "subtitle": "Track sales movements across products, customer segments, regions, and time periods.",
        "icon": "📈",
        "eyebrow": "Revenue Intelligence",
    },
    "Profit Analysis": {
        "title": "Profit Analysis",
        "subtitle": "Evaluate margin performance, profitability drivers, and value creation across the business.",
        "icon": "💰",
        "eyebrow": "Margin Insights",
    },
    "Upload Data": {
        "title": "Upload Data",
        "subtitle": "Upload, validate, preview, and activate custom sales datasets without changing the app code.",
        "icon": "📤",
        "eyebrow": "Data Management",
    },
}

metadata = page_metadata[current_page.title]

apply_global_styles()
page_header(
    title=metadata["title"],
    subtitle=metadata["subtitle"],
    icon=metadata["icon"],
    eyebrow=metadata["eyebrow"],
)
render_top_navigation()

current_page.run()
page_footer()
