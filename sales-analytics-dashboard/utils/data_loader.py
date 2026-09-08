from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = ROOT_DIR / "data" / "sales_data.csv"


@st.cache_data
def load_default_dataset(path: str | Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load the default CSV dataset from disk."""
    df = pd.read_csv(path)
    return df


@st.cache_data
def load_uploaded_dataset(uploaded_file) -> pd.DataFrame:
    """Load a CSV uploaded through the Streamlit file uploader."""
    if uploaded_file is None:
        return pd.DataFrame()
    return pd.read_csv(uploaded_file)


@st.cache_data
def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply a common baseline cleanup to the incoming dataset."""
    if df is None or df.empty:
        return pd.DataFrame()

    cleaned = df.copy()
    for column in cleaned.columns:
        if cleaned[column].dtype == object:
            cleaned[column] = cleaned[column].astype(str).str.strip()
    return cleaned


@st.cache_data
def transform_orders_dataframe(df: Optional[pd.DataFrame]) -> pd.DataFrame:
    """Normalize the supplied Orders table and create business-friendly derived columns."""
    if df is None:
        return pd.DataFrame()

    cleaned = normalize_dataframe(df).copy()

    if "Order Date" in cleaned.columns:
        cleaned["Order Date"] = pd.to_datetime(cleaned["Order Date"], errors="coerce", dayfirst=True)
        cleaned = cleaned.dropna(subset=["Order Date"]).sort_values("Order Date").reset_index(drop=True)

    for col_name in ["Order ID", "CustomerName", "State", "City"]:
        if col_name in cleaned.columns:
            cleaned[col_name] = cleaned[col_name].replace({"nan": pd.NA, "None": pd.NA, "": pd.NA})
            cleaned[col_name] = cleaned[col_name].astype(str).str.strip()
            cleaned[col_name] = cleaned[col_name].replace({"nan": pd.NA, "None": pd.NA, "": pd.NA})

    if "CustomerName" in cleaned.columns:
        cleaned["customer_order_count"] = cleaned.groupby("CustomerName")["Order ID"].transform("count")
    if "State" in cleaned.columns:
        cleaned["state_order_count"] = cleaned.groupby("State")["Order ID"].transform("count")
    if "City" in cleaned.columns:
        cleaned["city_order_count"] = cleaned.groupby("City")["Order ID"].transform("count")
    if "Order Date" in cleaned.columns:
        cleaned["order_month"] = cleaned["Order Date"].dt.to_period("M").astype(str)
        cleaned["order_year"] = cleaned["Order Date"].dt.year
        cleaned["order_day_name"] = cleaned["Order Date"].dt.day_name()

    return cleaned


@st.cache_data
def prepare_dataframe(df: Optional[pd.DataFrame]) -> pd.DataFrame:
    """Standardize and validate the working dataset."""
    if df is None:
        return pd.DataFrame()

    cleaned = transform_orders_dataframe(df)

    for col in list(cleaned.columns):
        if cleaned[col].dtype == object:
            cleaned[col] = cleaned[col].replace({"nan": pd.NA, "None": pd.NA, "": pd.NA})

    return cleaned


@st.cache_data
def inspect_dataset(df: pd.DataFrame) -> dict:
    """Return a structured profile of the dataset."""
    if df is None or df.empty:
        return {
            "rows": 0,
            "columns": 0,
            "missing_values": 0,
            "duplicate_rows": 0,
            "dtypes": {},
            "date_range": None,
        }

    data = prepare_dataframe(df)
    missing_values = int(data.isna().sum().sum())
    duplicate_rows = int(data.duplicated().sum())

    profile = {
        "rows": int(len(data)),
        "columns": int(len(data.columns)),
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "dtypes": {str(k): str(v) for k, v in data.dtypes.items()},
        "date_range": None,
    }

    date_candidates = [
        col for col in data.columns if "date" in col.lower() or "time" in col.lower()
    ]
    if date_candidates:
        candidate = date_candidates[0]
        parsed = pd.to_datetime(data[candidate], errors="coerce")
        valid_dates = parsed.dropna()
        if not valid_dates.empty:
            profile["date_range"] = (
                valid_dates.min().strftime("%Y-%m-%d"),
                valid_dates.max().strftime("%Y-%m-%d"),
            )

    return profile


@st.cache_data
def get_active_dataframe() -> pd.DataFrame:
    """Return the currently active dataset from session state or default file."""
    if "sales_df" in st.session_state and st.session_state["sales_df"] is not None:
        return st.session_state["sales_df"]

    path = st.session_state.get("dataset_path", DEFAULT_DATA_PATH)
    if Path(path).exists():
        return transform_orders_dataframe(load_default_dataset(path))
    return pd.DataFrame()
