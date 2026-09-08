# Sales Intelligence Dashboard

A professional Streamlit sales analytics dashboard designed to explore revenue, profit, customer behavior, and operational trends from a single modern business intelligence workspace.

## Overview

This project provides a complete analytics experience for sales data, including:

- KPI cards for revenue, profit, profit margin, and top-performing segments
- Sales analysis across product, region, and customer dimensions
- Profitability analysis with trend and contribution views
- Data overview for schema validation, data health, and record quality
- Upload and validation workflow for custom CSV datasets
- Multi-page navigation and dark enterprise dashboard styling

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## Project Structure

```text
streamlit_project/
├── app.py
├── README.md
├── requirements.txt
├── Data/
├── pages/
├── utils/
├── tests/
└── .streamlit/
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data Requirements

The app expects a sales dataset with relevant columns such as:

- Date / Order Date
- Sales
- Profit
- Region
- Product
- Customer

If a custom CSV is uploaded, the app validates the required columns before activating it.

## Dashboard Pages

- Home
- Data Overview
- Sales Analysis
- Profit Analysis
- Upload Data

## Notes

This project is intended for business reporting and dashboard-style exploration, with a focus on clean UI, operational readability, and reliable data inspection.
