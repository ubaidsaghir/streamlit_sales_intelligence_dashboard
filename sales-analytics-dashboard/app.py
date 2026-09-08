from __future__ import annotations

from pathlib import Path

import streamlit as st

from utils.data_loader import load_default_dataset
from utils.ui import apply_global_styles, render_footer, render_header


DATA_PATH = Path(__file__).resolve().parent / "data" / "sales_data.csv"


def configure_app_state() -> None:
    if "sales_df" not in st.session_state:
        st.session_state["sales_df"] = load_default_dataset(DATA_PATH)
    if "dataset_path" not in st.session_state:
        st.session_state["dataset_path"] = str(DATA_PATH)


def main() -> None:
    configure_app_state()
    st.set_page_config(
        page_title="Sales Analytics Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_global_styles()
    render_header(
        "Sales Performance Center",
        "Monitor sales activity, customer patterns, and operational performance from a single workspace.",
    )

    pages = [
        st.Page("pages/0_Dashboard.py", title="Dashboard", icon="📊"),
        st.Page("pages/1_Sales_Overview.py", title="Sales Overview", icon="📈"),
        st.Page("pages/2_Product_Analysis.py", title="Product Analysis", icon="🧩"),
        st.Page("pages/3_Customer_Analysis.py", title="Customer Analysis", icon="👥"),
        st.Page("pages/4_Profitability.py", title="Profitability", icon="💹"),
        st.Page("pages/5_Data_Management.py", title="Data Management", icon="🗂️"),
    ]
    navigation = st.navigation(pages)
    navigation.run()
    render_footer()


if __name__ == "__main__":
    main()
