from __future__ import annotations

import re
from typing import Iterable

import pandas as pd


def normalize_string(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def _normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


def detect_columns(df: pd.DataFrame) -> dict:
    normalized_map = { _normalize_name(col): col for col in df.columns }
    result = {
        "date": None,
        "sales": None,
        "profit": None,
        "quantity": None,
        "product": None,
        "category": None,
        "customer": None,
        "region": None,
        "order_id": None,
        "status": None,
    }

    patterns = {
        "date": ["date", "orderdate", "transactiondate", "saledate", "createdat", "invoicedate"],
        "sales": ["sales", "revenue", "totalsales", "amount", "netsales", "saleamount"],
        "profit": ["profit", "totalprofit", "netprofit", "margin", "grossprofit"],
        "quantity": ["quantity", "qty", "units", "unitssold", "orderquantity"],
        "product": ["product", "productname", "item", "itemname", "sku", "productid"],
        "category": ["category", "productcategory", "segment", "subcategory"],
        "customer": ["customer", "customername", "client", "customerid", "clientname"],
        "region": ["region", "state", "country", "territory", "market"],
        "order_id": ["orderid", "order", "ordernumber", "salesorder"],
        "status": ["status", "orderstatus", "salesstatus"],
    }

    for key, aliases in patterns.items():
        for alias in aliases:
            if alias in normalized_map:
                result[key] = normalized_map[alias]
                break

    if result["date"] is None:
        for col in df.columns:
            lower = col.lower()
            if "date" in lower:
                result["date"] = col
                break

    if result["customer"] is None:
        for col in df.columns:
            lower = col.lower()
            if "customer" in lower or "client" in lower:
                result["customer"] = col
                break

    if result["region"] is None:
        for col in df.columns:
            lower = col.lower()
            if "state" in lower or "region" in lower or "city" in lower or "country" in lower:
                result["region"] = col
                break

    if result["order_id"] is None:
        for col in df.columns:
            lower = col.lower()
            if "order" in lower and "id" in lower:
                result["order_id"] = col
                break

    return result


def calculate_total_orders(df: pd.DataFrame) -> int:
    col = detect_columns(df).get("order_id")
    if col:
        return int(df[col].nunique()) if df.empty is False else 0
    return int(len(df))


def calculate_total_customers(df: pd.DataFrame) -> int:
    col = detect_columns(df).get("customer")
    if col:
        return int(df[col].dropna().nunique())
    return 0


def calculate_total_sales(df: pd.DataFrame) -> float | None:
    sales_col = detect_columns(df).get("sales")
    if not sales_col:
        return None
    numeric = pd.to_numeric(df[sales_col], errors="coerce")
    return float(numeric.sum())


def calculate_total_profit(df: pd.DataFrame) -> float | None:
    profit_col = detect_columns(df).get("profit")
    if not profit_col:
        return None
    numeric = pd.to_numeric(df[profit_col], errors="coerce")
    return float(numeric.sum())


def calculate_profit_margin(df: pd.DataFrame) -> float | None:
    sales_col = detect_columns(df).get("sales")
    profit_col = detect_columns(df).get("profit")
    if not sales_col or not profit_col:
        return None
    sales = pd.to_numeric(df[sales_col], errors="coerce").fillna(0)
    profit = pd.to_numeric(df[profit_col], errors="coerce").fillna(0)
    total_sales = sales.sum()
    if pd.isna(total_sales) or total_sales == 0:
        return None
    return float((profit.sum() / total_sales) * 100)


def calculate_average_order_value(df: pd.DataFrame) -> float | None:
    sales_col = detect_columns(df).get("sales")
    order_count = calculate_total_orders(df)
    if not sales_col or order_count == 0:
        return None
    sales_total = calculate_total_sales(df)
    if sales_total is None:
        return None
    return float(sales_total / order_count)


def calculate_growth(df: pd.DataFrame, date_col: str | None = None) -> float:
    if df.empty:
        return 0.0
    if date_col is None:
        date_col = detect_columns(df).get("date")
    if not date_col:
        return 0.0

    try:
        series = pd.to_datetime(df[date_col], errors="coerce")
    except Exception:
        return 0.0

    filtered = df.copy()
    filtered[date_col] = series
    filtered = filtered.dropna(subset=[date_col]).sort_values(date_col)
    if filtered.empty:
        return 0.0

    sales_col = detect_columns(df).get("sales")
    if sales_col:
        totals = filtered.groupby(pd.Grouper(key=date_col, freq="M"))[sales_col].sum()
    else:
        totals = filtered.groupby(pd.Grouper(key=date_col, freq="M")).size()

    if len(totals) < 2:
        return 0.0
    first = totals.iloc[0]
    last = totals.iloc[-1]
    if first == 0:
        return 0.0
    return float(((last - first) / first) * 100)


def get_top_products(df: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    product_col = detect_columns(df).get("product")
    sales_col = detect_columns(df).get("sales")
    if not product_col:
        return pd.DataFrame(columns=["Product", "Sales"])
    if sales_col:
        return (
            df.groupby(product_col, dropna=False)
            .agg(Sales=(sales_col, "sum"))
            .reset_index()
            .rename(columns={product_col: "Product"})
            .sort_values("Sales", ascending=False)
            .head(limit)
        )
    return (
        df.groupby(product_col, dropna=False)
        .size()
        .reset_index(name="Sales")
        .rename(columns={product_col: "Product"})
        .sort_values("Sales", ascending=False)
        .head(limit)
    )


def get_top_customers(df: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    customer_col = detect_columns(df).get("customer")
    sales_col = detect_columns(df).get("sales")
    if not customer_col:
        return pd.DataFrame(columns=["Customer", "Revenue"]) if sales_col else pd.DataFrame(columns=["Customer", "Orders"])
    if sales_col:
        summary = (
            df.groupby(customer_col, dropna=False)
            .agg(Revenue=(sales_col, "sum"), Orders=("Order ID" if "Order ID" in df.columns else customer_col, "count"))
            .reset_index()
            .rename(columns={customer_col: "Customer"})
            .sort_values("Revenue", ascending=False)
            .head(limit)
        )
        return summary
    summary = (
        df.groupby(customer_col, dropna=False)
        .size()
        .reset_index(name="Orders")
        .rename(columns={customer_col: "Customer"})
        .sort_values("Orders", ascending=False)
        .head(limit)
    )
    return summary


def get_top_regions(df: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    region_col = detect_columns(df).get("region")
    sales_col = detect_columns(df).get("sales")
    if not region_col:
        return pd.DataFrame(columns=["Region", "Sales"])
    if sales_col:
        return (
            df.groupby(region_col, dropna=False)
            .agg(Sales=(sales_col, "sum"))
            .reset_index()
            .rename(columns={region_col: "Region"})
            .sort_values("Sales", ascending=False)
            .head(limit)
        )
    return (
        df.groupby(region_col, dropna=False)
        .size()
        .reset_index(name="Orders")
        .rename(columns={region_col: "Region"})
        .sort_values("Orders", ascending=False)
        .head(limit)
    )


def get_order_summary_by_period(df: pd.DataFrame, period: str = "M") -> pd.DataFrame:
    date_col = detect_columns(df).get("date")
    if not date_col:
        return pd.DataFrame(columns=["Period", "Orders"])

    parsed = pd.to_datetime(df[date_col], errors="coerce")
    working = df.copy()
    working[date_col] = parsed
    working = working.dropna(subset=[date_col])

    if period == "D":
        grouped = working.groupby(pd.Grouper(key=date_col, freq="D")).size().reset_index(name="Orders")
    elif period == "M":
        grouped = working.groupby(pd.Grouper(key=date_col, freq="M")).size().reset_index(name="Orders")
    else:
        grouped = working.groupby(pd.Grouper(key=date_col, freq="Q")).size().reset_index(name="Orders")

    grouped = grouped.rename(columns={date_col: "Period"})
    return grouped


def get_monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    date_col = detect_columns(df).get("date")
    sales_col = detect_columns(df).get("sales")
    if not date_col:
        return pd.DataFrame(columns=["Month", "Orders"])

    working = df.copy()
    working[date_col] = pd.to_datetime(working[date_col], errors="coerce")
    working = working.dropna(subset=[date_col])

    if sales_col:
        grouped = working.groupby(pd.Grouper(key=date_col, freq="M"))[sales_col].sum().reset_index()
        grouped.columns = ["Month", "Sales"]
    else:
        grouped = working.groupby(pd.Grouper(key=date_col, freq="M")).size().reset_index(name="Sales")
        grouped.columns = ["Month", "Sales"]
    return grouped
