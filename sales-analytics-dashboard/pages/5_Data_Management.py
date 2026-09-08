from __future__ import annotations

from io import StringIO

import pandas as pd
import streamlit as st

from utils.data_loader import inspect_dataset, load_uploaded_dataset, prepare_dataframe


st.set_page_config(page_title="Data Management", layout="wide")


def format_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isna().sum().reset_index()
    missing.columns = ["Column", "Missing Values"]
    return missing


def main() -> None:
    st.subheader("Dataset Management")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        st.session_state["sales_df"] = prepare_dataframe(load_uploaded_dataset(uploaded_file))
        st.session_state["dataset_path"] = uploaded_file.name

    current_df = st.session_state.get("sales_df")
    if current_df is None or current_df.empty:
        st.info("No CSV is currently loaded. Use the uploader to load a dataset, or the default dataset will be used when available.")
        return

    st.success("Dataset loaded successfully and stored in session state.")

    profile = inspect_dataset(current_df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", profile["rows"])
    col2.metric("Columns", profile["columns"])
    col3.metric("Missing Values", profile["missing_values"])
    col4.metric("Duplicate Rows", profile["duplicate_rows"])

    st.markdown("### Dataset Preview")
    st.dataframe(current_df.head(200), use_container_width=True)

    st.markdown("### Validation Summary")
    validation_cols = st.columns(2)
    with validation_cols[0]:
        st.write("**Data types**")
        st.dataframe(pd.DataFrame({"Column": list(profile["dtypes"].keys()), "Data Type": list(profile["dtypes"].values())}), use_container_width=True)
    with validation_cols[1]:
        st.write("**Missing values**")
        st.dataframe(format_missing_values(current_df), use_container_width=True)

    st.markdown("### Date Range")
    date_candidates = [col for col in current_df.columns if "date" in col.lower()]
    if date_candidates:
        first = pd.to_datetime(current_df[date_candidates[0]], errors="coerce").dropna()
        if not first.empty:
            st.write(f"{first.min().strftime('%Y-%m-%d')} to {first.max().strftime('%Y-%m-%d')}")
        else:
            st.warning("Date column detected but no valid date values were found.")
    else:
        st.info("No date column was detected in the active dataset.")

    csv_buffer = StringIO()
    current_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="Download processed CSV",
        data=csv_buffer.getvalue(),
        file_name="processed_data.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
