import pandas as pd

from app import load_orders_data, prepare_orders_data


def test_load_orders_data_reads_sales_dataset_and_validates_core_columns():
    df = load_orders_data()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    required_columns = {"Order_ID", "Order_Date", "Region", "Product", "Customer", "Sales", "Profit"}
    assert required_columns.issubset(df.columns)
    assert df["Order_ID"].notna().all()
    assert df["Order_Date"].notna().all()
    assert df["Sales"].ge(0).all()


def test_prepare_orders_data_adds_time_and_customer_summary_fields():
    df = prepare_orders_data(load_orders_data())

    assert "order_month" in df.columns
    assert "order_year" in df.columns
    assert "order_day_name" in df.columns
    assert "customer_order_count" in df.columns
    assert df["order_month"].notna().all()
    assert df["customer_order_count"].ge(1).all()
