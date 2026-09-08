from __future__ import annotations

from typing import Iterable

import pandas as pd
import streamlit as st


def apply_global_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #0b1220;
            --panel: #111827;
            --panel-2: #1f2937;
            --muted: #9aa7bd;
            --text: #e5eefb;
            --primary: #7dd3fc;
            --primary-dark: #38bdf8;
            --success: #34d399;
            --warning: #fbbf24;
            --danger: #f87171;
            --border: rgba(148, 163, 184, 0.16);
            --shadow: rgba(2, 6, 23, 0.45);
        }

        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #09111d 0%, #111827 100%);
            color: var(--text);
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .app-shell {
            background: rgba(15, 23, 42, 0.9);
            border-radius: 20px;
            padding: 1.2rem;
            box-shadow: 0 12px 35px var(--shadow);
        }

        .primary-header {
            background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
            color: white;
            border-radius: 18px;
            padding: 1.3rem 1.5rem;
            box-shadow: 0 20px 35px rgba(15, 23, 42, 0.35);
            margin-bottom: 1.2rem;
            border: 1px solid rgba(148, 163, 184, 0.18);
        }

        .primary-header h1 {
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
        }

        .header-subtitle {
            color: rgba(255,255,255,0.75);
            margin-top: 0.45rem;
            display: block;
        }

        .nav-panel {
            background: rgba(17, 24, 39, 0.9);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 0.45rem 0.65rem;
            margin-bottom: 1rem;
            box-shadow: 0 10px 18px rgba(2, 6, 23, 0.25);
        }

        .kpi-card {
            background: linear-gradient(180deg, rgba(17, 24, 39, 1) 0%, rgba(15, 23, 42, 1) 100%);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1rem 1.1rem;
            box-shadow: 0 12px 18px rgba(2, 6, 23, 0.2);
            min-height: 130px;
        }

        .section-header {
            color: var(--text);
            font-weight: 700;
            letter-spacing: -0.02em;
            margin: 1.5rem 0 0.75rem 0;
        }

        .info-card {
            background: linear-gradient(180deg, rgba(17, 24, 39, 1) 0%, rgba(15, 23, 42, 1) 100%);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1rem;
            box-shadow: 0 10px 16px rgba(2, 6, 23, 0.18);
        }

        [data-testid="stSidebar"] {
            background: #0f172a;
        }

        .stMetric {
            background: rgba(17, 24, 39, 0.96);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 0.9rem 0.9rem 0.7rem 0.9rem;
        }

        div[data-testid="stDataFrame"] {
            background: rgba(15, 23, 42, 0.9);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="primary-header">
            <h1>{title}</h1>
            <span class="header-subtitle">{subtitle}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, subtitle: str | None = None) -> None:
    st.markdown(f"<div class='section-header'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.caption(subtitle)


def render_kpi_card(label: str, value: str, delta: str | None = None, accent: str = "#1d9bf0") -> None:
    delta_html = f"<div style='color:{accent}; font-size: 0.78rem; margin-top: 0.55rem;'>{delta}</div>" if delta else ""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div style="font-size: 0.75rem; letter-spacing: 0.08em; text-transform: uppercase; color: #667a91;">{label}</div>
            <div style="font-size: 2rem; font-weight: 700; color: #162433; margin-top: 0.35rem;">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="info-card">
            <div style="font-weight: 700; margin-bottom: 0.5rem;">{title}</div>
            <div style="color: #4b5f77; line-height: 1.5;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        """
        <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid rgba(19, 34, 53, 0.08); text-align: center; color: #5c7189; font-size: 0.82rem;">
            Sales Analytics Dashboard • Built with Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_currency(value) -> str:
    if value is None or pd.isna(value):
        return "$0.00"
    return f"${value:,.2f}"


def format_percent(value) -> str:
    if value is None or pd.isna(value):
        return "0.00%"
    return f"{value:.2f}%"


def format_number(value) -> str:
    if value is None or pd.isna(value):
        return "0"
    if isinstance(value, (int, float)):
        return f"{value:,.0f}"
    return str(value)
