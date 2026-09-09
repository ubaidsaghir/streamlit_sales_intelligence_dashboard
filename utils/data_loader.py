from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = ROOT_DIR / "Data" / "sales_dataset.csv"

REQUIRED_COLUMNS = [
    "Order_ID",
    "Order_Date",
    "Region",
    "Product",
    "Customer",
    "Sales",
    "Profit",
]

COLUMN_ALIASES = {
    "Order_ID": ["Order_ID", "Order ID", "OrderID", "order_id"],
    "Order_Date": ["Order_Date", "Order Date", "OrderDate", "order_date"],
    "Region": ["Region", "region"],
    "Product": ["Product", "product"],
    "Customer": ["Customer", "Customer_Name", "Customer Name", "customer_name", "customer"],
    "Sales": ["Sales", "Net_Sales", "Gross_Sales", "net_sales", "gross_sales", "sales", "Revenue"],
    "Profit": ["Profit", "profit", "Total_Profit", "total_profit"],
}


def _resolve_alias(dataframe: pd.DataFrame, column_name: str) -> str | None:
    """Return the first matching alias for a canonical column name."""
    for alias in COLUMN_ALIASES.get(column_name, [column_name]):
        if alias in dataframe.columns:
            return alias
    return None


def validate_columns(dataframe: pd.DataFrame) -> list[str]:
    """Return required columns missing from the dataframe."""
    missing: list[str] = []
    for column in REQUIRED_COLUMNS:
        if _resolve_alias(dataframe, column) is None:
            missing.append(column)
    return missing


def clean_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize the sales dataframe."""
    cleaned = dataframe.copy()

    for canonical_column, aliases in COLUMN_ALIASES.items():
        resolved_alias = _resolve_alias(cleaned, canonical_column)
        if resolved_alias and canonical_column not in cleaned.columns:
            cleaned[canonical_column] = cleaned[resolved_alias]

    if "Customer_Name" in cleaned.columns and "Customer" not in cleaned.columns:
        cleaned["Customer"] = cleaned["Customer_Name"]
    if "Net_Sales" in cleaned.columns and "Sales" not in cleaned.columns:
        cleaned["Sales"] = cleaned["Net_Sales"]
    elif "Gross_Sales" in cleaned.columns and "Sales" not in cleaned.columns:
        cleaned["Sales"] = cleaned["Gross_Sales"]

    if "Order_Date" in cleaned.columns:
        cleaned["Order_Date"] = pd.to_datetime(cleaned["Order_Date"], errors="coerce")

    for column in ["Sales", "Profit", "Quantity", "Unit_Price", "Discount_Amount", "Gross_Sales", "Net_Sales", "Unit_Cost", "Total_Cost", "Discount_Pct", "Profit_Margin_Pct"]:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    for column in [
        "Region",
        "Product",
        "Customer",
        "State",
        "Category",
        "Customer_Segment",
        "Sales_Rep",
        "Customer_ID",
        "Customer_Name",
        "Ship_Mode",
        "Payment_Method",
        "Order_Status",
        "Returned",
        "Month",
        "Quarter",
    ]:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].astype("string").str.strip()

    available_required_columns = [column for column in REQUIRED_COLUMNS if column in cleaned.columns]
    if available_required_columns:
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
    return st.session_state.get("active_source", "sales_dataset.csv")


def set_active_data(dataframe: pd.DataFrame, source_name: str) -> None:
    """Save an uploaded dataframe in session state."""
    st.session_state["active_dataset"] = dataframe.copy()
    st.session_state["active_source"] = source_name


def reset_active_data() -> None:
    """Return the dashboard to the default dataset."""
    st.session_state.pop("active_dataset", None)
    st.session_state.pop("active_source", None)
