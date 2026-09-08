from pathlib import Path

import pandas as pd
import streamlit as st

DEFAULT_DATA_PATH = Path("Data/sales_bulk_data.csv")

REQUIRED_COLUMNS = [
    "Order_ID",
    "Order_Date",
    "Region",
    "Product",
    "Customer",
    "Sales",
    "Profit",
]


def validate_columns(dataframe: pd.DataFrame) -> list[str]:
    """Return required columns missing from the dataframe."""
    return [column for column in REQUIRED_COLUMNS if column not in dataframe.columns]


def clean_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize the sales dataframe."""
    cleaned = dataframe.copy()

    if "Order_Date" in cleaned.columns:
        cleaned["Order_Date"] = pd.to_datetime(cleaned["Order_Date"], errors="coerce")

    for column in ["Order_ID", "Sales", "Profit"]:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    for column in ["Region", "Product", "Customer"]:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].astype("string").str.strip()

    available_required_columns = [column for column in REQUIRED_COLUMNS if column in cleaned.columns]
    cleaned = cleaned.dropna(subset=available_required_columns)
    cleaned = cleaned.drop_duplicates()
    return cleaned.reset_index(drop=True)


@st.cache_data
def load_default_data() -> pd.DataFrame:
    """Load and cache the default sales dataset."""
    dataframe = pd.read_csv(DEFAULT_DATA_PATH)
    return clean_data(dataframe)


def get_active_data() -> pd.DataFrame:
    """Return uploaded data or the default dataset."""
    if "active_dataset" in st.session_state:
        return st.session_state["active_dataset"].copy()
    return load_default_data().copy()


def get_active_source() -> str:
    """Return the name of the active data source."""
    return st.session_state.get("active_source", "Default bulk sales CSV")


def set_active_data(dataframe: pd.DataFrame, source_name: str) -> None:
    """Save an uploaded dataframe in session state."""
    st.session_state["active_dataset"] = dataframe.copy()
    st.session_state["active_source"] = source_name


def reset_active_data() -> None:
    """Return the dashboard to the default dataset."""
    st.session_state.pop("active_dataset", None)
    st.session_state.pop("active_source", None)
