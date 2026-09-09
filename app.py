from pathlib import Path

import pandas as pd
import streamlit as st

from utils.data_loader import clean_data
from utils.navigation import render_top_navigation
from utils.ui import apply_global_styles, page_footer, page_header

DEFAULT_DATA_PATH = Path(__file__).resolve().parent / "Data" / "sales_dataset.csv"


def load_orders_data() -> pd.DataFrame:
    """Load the active sales dataset used across the project."""
    return clean_data(pd.read_csv(DEFAULT_DATA_PATH))


def prepare_orders_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Add legacy summary fields used by existing scripts/tests."""
    cleaned = dataframe.copy()
    if "Order_Date" in cleaned.columns:
        cleaned["Order_Date"] = pd.to_datetime(cleaned["Order_Date"], errors="coerce")
    cleaned["order_month"] = cleaned["Order_Date"].dt.strftime("%B")
    cleaned["order_year"] = cleaned["Order_Date"].dt.year
    cleaned["order_day_name"] = cleaned["Order_Date"].dt.day_name()
    if "Customer" in cleaned.columns:
        cleaned["customer_order_count"] = cleaned.groupby("Customer")["Order_ID"].transform("count")
    else:
        cleaned["customer_order_count"] = 1
    return cleaned


def run_app() -> None:
    """Render the Streamlit dashboard entry point."""
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


if __name__ == "__main__":
    run_app()
