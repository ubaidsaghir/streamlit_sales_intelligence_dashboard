# Sales Analytics Dashboard

A production-style, multi-page Streamlit analytics application built around the uploaded sales/orders CSV. The project is designed to be modular, maintainable, and ready for extension.

## Features

- Executive dashboard with KPI cards and trend analysis
- Sales overview with date and segment filters
- Product analytics with available product-level views
- Customer-level analysis and repeat purchase insights
- Profitability monitoring where profit data is available
- Data management page for CSV upload, validation, preview, and export
- Centralized navigation and reusable UI components

## Architecture

The application follows a modular Streamlit design:

- `app.py` manages global configuration, navigation, header, and footer
- `pages/` contains independent dashboard pages
- `utils/` holds shared loading, calculation, chart, and UI logic
- `data/` stores the source CSV files
- `scripts/` contains dataset generation utilities

## Folder structure

```text
sales-analytics-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml
├── data/
│   ├── sales_data.csv
│   └── sales_bulk_data.csv
├── pages/
│   ├── 0_Dashboard.py
│   ├── 1_Sales_Overview.py
│   ├── 2_Product_Analysis.py
│   ├── 3_Customer_Analysis.py
│   ├── 4_Profitability.py
│   └── 5_Data_Management.py
├── utils/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── calculations.py
│   ├── charts.py
│   ├── navigation.py
│   └── ui.py
└── scripts/
    └── generate_data.py
```

## Dataset

This project uses the CSV file as the primary source of truth. The uploaded Orders table is copied into:

- `data/sales_data.csv`
- `data/sales_bulk_data.csv`

The app includes dynamic column detection so it can adapt to different CSV schemas and gracefully handle missing optional fields.

## Installation

```bash
pip install -r requirements.txt
```

## Run the app

```bash
streamlit run app.py
```

## Technologies used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
