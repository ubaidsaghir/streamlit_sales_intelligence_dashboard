import pandas as pd

from app import load_orders_data, prepare_orders_data


def test_load_orders_data_reads_csv_and_validates_columns():
    df = load_orders_data()

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["Order ID", "Order Date", "CustomerName", "State", "City"]
    assert len(df) == 500
    assert df["Order ID"].notna().all()
    assert df["Order Date"].notna().all()


def test_prepare_orders_data_adds_order_date_and_summary_fields():
    df = prepare_orders_data(load_orders_data())

    assert "order_month" in df.columns
    assert "order_year" in df.columns
    assert "order_day_name" in df.columns
    assert "customer_order_count" in df.columns
    assert df["order_month"].notna().all()
    assert df["customer_order_count"].ge(1).all()
