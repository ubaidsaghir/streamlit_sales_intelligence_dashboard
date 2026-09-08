import streamlit as st

NAVIGATION_PAGES = [
    {"path": "pages/0_Home.py", "label": "Home", "icon": "🏠"},
    {"path": "pages/1_Data_Overview.py", "label": "Data Overview", "icon": "📋"},
    {"path": "pages/2_Sales_Analysis.py", "label": "Sales Analysis", "icon": "📈"},
    {"path": "pages/3_Profit_Analysis.py", "label": "Profit Analysis", "icon": "💰"},
    {"path": "pages/4_Upload_Data.py", "label": "Upload Data", "icon": "📤"},
]


def render_top_navigation() -> None:
    """Render a horizontal navigation bar below the page header."""
    st.html(
        """
        <div class="nav-caption">Dashboard Navigation</div>
        """
    )

    with st.container(border=True):
        columns = st.columns(len(NAVIGATION_PAGES), gap="small")
        for column, page in zip(columns, NAVIGATION_PAGES):
            with column:
                st.page_link(page["path"], label=page["label"], icon=page["icon"], width="stretch")


def render_sidebar_navigation() -> None:
    """Render navigation links inside the sidebar."""
    with st.sidebar:
        st.markdown("## 📊 Sales Hub")
        st.caption("Executive analytics workspace")
        st.divider()
        for page in NAVIGATION_PAGES:
            st.page_link(page["path"], label=page["label"], icon=page["icon"], width="stretch")
        st.divider()
        st.caption("Application status")
        st.success("System operational")
        st.caption("Version 1.0.0")
