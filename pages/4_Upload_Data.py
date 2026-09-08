import pandas as pd
import streamlit as st

from utils.components import kpi_card
from utils.data_loader import REQUIRED_COLUMNS, clean_data, get_active_source, reset_active_data, set_active_data, validate_columns
from utils.ui import section_header


section_header("Active Data Source", "The selected dataset is shared across every dashboard page.")

source_column, action_column = st.columns([3, 1])
with source_column:
    st.info(f"Current source: **{get_active_source()}**")
with action_column:
    if st.button("Use default data", icon="🔄", width="stretch"):
        reset_active_data()
        st.success("The default dataset is now active.")
        st.rerun()

section_header("Upload a Sales Dataset", "The CSV must contain the required dashboard columns.")

template_df = pd.DataFrame(columns=REQUIRED_COLUMNS)
left_column, right_column = st.columns([2, 1])
with left_column:
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], help="Upload a dataset with the expected sales schema.")
with right_column:
    st.download_button(
        label="Download CSV template",
        data=template_df.to_csv(index=False),
        file_name="sales_data_template.csv",
        mime="text/csv",
        icon="⬇️",
        width="stretch",
    )
    with st.expander("Required columns"):
        for column in REQUIRED_COLUMNS:
            st.write(f"• `{column}`")

if uploaded_file is not None:
    try:
        raw_dataframe = pd.read_csv(uploaded_file)
    except pd.errors.EmptyDataError:
        st.error("The uploaded CSV file is empty.")
        st.stop()
    except Exception as error:
        st.error(f"Could not read the CSV file: {error}")
        st.stop()

    missing_columns = validate_columns(raw_dataframe)
    if missing_columns:
        st.error("The uploaded file is missing these required columns: " + ", ".join(missing_columns))
        st.stop()

    cleaned_dataframe = clean_data(raw_dataframe)
    removed_rows = len(raw_dataframe) - len(cleaned_dataframe)

    section_header("Upload Validation", "Review the cleaned data before activating it.")

    metric1, metric2, metric3, metric4 = st.columns(4)
    with metric1:
        kpi_card("Uploaded Rows", f"{len(raw_dataframe):,}", "📥", "Rows read from the file")
    with metric2:
        kpi_card("Valid Rows", f"{len(cleaned_dataframe):,}", "✅", "Rows ready for analysis")
    with metric3:
        kpi_card("Removed Rows", f"{removed_rows:,}", "🧹", "Invalid or duplicate records")
    with metric4:
        kpi_card("Columns", f"{len(cleaned_dataframe.columns):,}", "🧱", "Available dataset fields")

    st.subheader("Cleaned Data Preview")
    st.dataframe(cleaned_dataframe.head(100), width="stretch", hide_index=True)

    if cleaned_dataframe.empty:
        st.error("No valid records remain after cleaning.")
    else:
        if st.button("Use this dataset", type="primary", icon="✅", width="stretch"):
            set_active_data(dataframe=cleaned_dataframe, source_name=uploaded_file.name)
            st.success("The uploaded dataset is now active across all dashboard pages.")
            st.rerun()
else:
    st.info("No file has been selected. The dashboard will continue using the current data source.")
