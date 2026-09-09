# 📊 Sales Intelligence Dashboard

A polished Streamlit-based sales analytics project built to explore revenue, profitability, customer behavior, and operational trends from a modern business intelligence workspace.

## ✨ Overview

This dashboard helps business teams quickly answer questions such as:

- Which regions and products generate the most revenue?
- What is the profit margin across different time periods?
- Which customers contribute the most sales?
- Are there quality issues or missing values in the active dataset?

The app includes a dark premium UI, multi-page navigation, KPI summaries, interactive charts, and an upload workflow for custom CSV files.

## 🚀 Included Features

- KPI cards for sales, profit, margin, and leader metrics
- Sales trend and segmentation analysis by region, product, and customer
- Profitability dashboard with margin and performance drivers
- Data overview page for schema inspection and quality checks
- Upload and validation workflow for custom sales CSV files
- Responsive dark layout with enterprise-style styling

## 🧰 Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- GitHub for version control and project sharing

## 📁 Project Structure

```text
streamlit_project/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── Data/
│   └── sales_dataset.csv
├── pages/
│   ├── 0_Home.py
│   ├── 1_Data_Overview.py
│   ├── 2_Sales_Analysis.py
│   ├── 3_Profit_Analysis.py
│   └── 4_Upload_Data.py
├── utils/
│   ├── components.py
│   ├── data_loader.py
│   ├── export.py
│   ├── filters.py
│   ├── navigation.py
│   └── ui.py
├── tests/
└── .streamlit/
```

## 📊 Default Dataset

The project uses the dataset located at:

- `Data/sales_dataset.csv`

This file contains order-level sales data with fields such as:

- `Order_ID`
- `Order_Date`
- `Region`
- `Product`
- `Customer`
- `Sales`
- `Profit`
- `Category`
- `State`
- `Ship_Mode`
- `Payment_Method`
- `Order_Status`

## ▶️ Run the App Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

## 🧪 Data Validation Workflow

Users can upload a CSV file from the dashboard and the app will:

1. Check the required fields
2. Clean invalid or duplicate records
3. Preview the cleaned dataset
4. Activate the uploaded dataset across all dashboard pages

## 🧭 Dashboard Pages

- Home
- Data Overview
- Sales Analysis
- Profit Analysis
- Upload Data

## 🔗 GitHub Repository

This project is maintained as a GitHub repository and can be pushed or cloned using the standard Git workflow.

## 📝 Notes

This project is designed for business reporting, sales monitoring, and data exploration with a clean enterprise look and reliable analytics workflow.
