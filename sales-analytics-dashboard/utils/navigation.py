from __future__ import annotations

import streamlit as st


def render_top_navigation(current_page: str) -> None:
    pages = [
        ("Dashboard", "📊", "Dashboard"),
        ("Sales Overview", "💹", "Sales Overview"),
        ("Product Analysis", "🧩", "Product Analysis"),
        ("Customer Analysis", "👥", "Customer Analysis"),
        ("Profitability", "📈", "Profitability"),
        ("Data Management", "🗂️", "Data Management"),
    ]

    st.markdown(
        """
        <style>
        .topnav {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            padding: 0.25rem 0 1rem 0;
        }
        .nav-item {
            border-radius: 12px;
            padding: 0.72rem 1rem;
            text-decoration: none;
            color: #36506e;
            background: rgba(255,255,255,0.6);
            border: 1px solid rgba(24, 50, 77, 0.08);
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .nav-item:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 18px rgba(25, 60, 100, 0.08);
        }
        .nav-item.active {
            background: linear-gradient(135deg, #0d1f35 0%, #173a5a 100%);
            color: white;
            border-color: rgba(17, 48, 75, 0.15);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    nav_links = []
    for label, icon, page_name in pages:
        css_class = "nav-item active" if page_name == current_page else "nav-item"
        nav_links.append(f'<a class="{css_class}" href="#">{icon} {label}</a>')

    st.markdown(f'<div class="topnav">{"".join(nav_links)}</div>', unsafe_allow_html=True)
