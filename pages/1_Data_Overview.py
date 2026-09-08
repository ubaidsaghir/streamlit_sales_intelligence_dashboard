import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_float_dtype,
    is_integer_dtype,
    is_string_dtype,
)

from utils.components import kpi_card
from utils.data_loader import get_active_data, get_active_source
from utils.ui import section_header


def friendly_data_type(dtype) -> str:
    if is_datetime64_any_dtype(dtype):
        return "Date/Time"
    if is_integer_dtype(dtype):
        return "Whole Number"
    if is_float_dtype(dtype):
        return "Decimal Number"
    if is_bool_dtype(dtype):
        return "True/False"
    if is_string_dtype(dtype):
        return "Text"
    return str(dtype)


dataframe = get_active_data()
source_name = get_active_source()

section_header("Dataset Summary", f"Current dataset: {source_name}")

metric1, metric2, metric3, metric4 = st.columns(4)
with metric1:
    kpi_card("Total Rows", f"{len(dataframe):,}", "📑", "Clean records")
with metric2:
    kpi_card("Total Columns", str(len(dataframe.columns)), "🧱", "Available fields")
with metric3:
    kpi_card("Missing Values", f"{int(dataframe.isna().sum().sum()):,}", "⚠️", "Across the complete dataset")
with metric4:
    kpi_card("Duplicate Rows", f"{int(dataframe.duplicated().sum()):,}", "📋", "Exact duplicate records")

section_header("Column Profile", "Review the structure and quality of every column.")
column_information = pd.DataFrame(
    {
        "Column": dataframe.columns,
        "Data Type": [friendly_data_type(dtype) for dtype in dataframe.dtypes],
        "Missing Values": dataframe.isna().sum().values,
        "Unique Values": dataframe.nunique().values,
    }
)
st.dataframe(column_information, hide_index=True, width="stretch")

section_header("Dataset Exploration", "Inspect records and summary statistics.")
preview_tab, summary_tab, quality_tab = st.tabs(["Data Preview", "Numerical Summary", "Data Quality"])

with preview_tab:
    row_count = st.slider("Number of records to display", min_value=5, max_value=100, value=20, step=5)
    st.dataframe(dataframe.head(row_count), width="stretch", hide_index=True)

with summary_tab:
    numeric_summary = dataframe.select_dtypes(include="number").describe().transpose().reset_index().rename(columns={"index": "Column"})
    st.dataframe(numeric_summary, width="stretch", hide_index=True)

with quality_tab:
    quality_table = pd.DataFrame(
        {
            "Column": dataframe.columns,
            "Complete Records": (len(dataframe) - dataframe.isna().sum()).values,
            "Missing Records": dataframe.isna().sum().values,
            "Completeness %": ((1 - dataframe.isna().sum() / max(len(dataframe), 1)) * 100).round(2).values,
        }
    )
    st.dataframe(quality_table, width="stretch", hide_index=True)
