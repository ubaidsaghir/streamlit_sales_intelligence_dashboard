from html import escape

import streamlit as st


def apply_global_styles() -> None:
    """Apply the global application design system."""
    st.markdown(
        """
        <style>
            :root {
                --bg-900: #071822;
                --bg-800: #0d2230;
                --bg-700: #123247;
                --panel: rgba(14, 27, 38, 0.88);
                --panel-soft: rgba(20, 37, 50, 0.9);
                --panel-lift: rgba(29, 49, 67, 0.96);
                --border: rgba(148, 163, 184, 0.16);
                --text: #edf7ff;
                --muted: #acc6d9;
                --accent: #75d9ff;
                --accent-2: #7ef0c5;
                --accent-3: #8ea9ff;
                --accent-4: #f7b267;
                --shadow: rgba(2, 6, 23, 0.45);
            }

            .stApp {
                background:
                    radial-gradient(circle at 10% 15%, rgba(117, 217, 255, 0.12), transparent 18%),
                    radial-gradient(circle at 85% 12%, rgba(126, 240, 197, 0.08), transparent 22%),
                    linear-gradient(180deg, var(--bg-900) 0%, #0b1d2b 100%);
            }

            .block-container {
                max-width: 1480px;
                padding-top: 1.2rem;
                padding-bottom: 2.5rem;
            }

            [data-testid="stHeader"] {
                background: transparent;
            }

            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, rgba(9, 19, 30, 0.98), rgba(11, 25, 37, 0.98));
                border-right: 1px solid var(--border);
            }

            .app-hero {
                position: relative;
                overflow: hidden;
                padding: 2rem 2rem 1.5rem;
                margin-bottom: 1.1rem;
                border: 1px solid rgba(117, 217, 255, 0.22);
                border-radius: 26px;
                background: linear-gradient(135deg, rgba(16, 35, 49, 0.94), rgba(14, 30, 42, 0.96));
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.22);
            }

            .app-hero::before {
                content: "";
                position: absolute;
                inset: -75px auto auto -95px;
                width: 260px;
                height: 260px;
                border-radius: 50%;
                background: rgba(117, 217, 255, 0.08);
            }

            .app-hero::after {
                content: "";
                position: absolute;
                right: -90px;
                top: -90px;
                width: 230px;
                height: 230px;
                border-radius: 50%;
                background: rgba(126, 240, 197, 0.06);
            }

            .hero-eyebrow {
                position: relative;
                z-index: 1;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 0.42rem 0.95rem;
                margin-bottom: 0.9rem;
                border: 1px solid rgba(117, 217, 255, 0.35);
                border-radius: 999px;
                background: rgba(117, 217, 255, 0.08);
                color: var(--accent);
                font-size: 0.74rem;
                font-weight: 700;
                letter-spacing: 0.1rem;
                text-transform: uppercase;
                box-shadow: inset 0 0 0 1px rgba(117, 217, 255, 0.08);
            }

            .hero-title-row {
                position: relative;
                z-index: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.8rem;
                width: 100%;
            }

            .hero-icon {
                font-size: clamp(2rem, 4vw, 3rem);
                line-height: 1;
            }

            .hero-title {
                margin: 0;
                color: var(--text);
                font-size: clamp(2rem, 3vw, 3.2rem);
                font-weight: 800;
                letter-spacing: -0.05em;
                line-height: 1.1;
            }

            .hero-subtitle {
                position: relative;
                z-index: 1;
                display: block;
                width: 100%;
                max-width: 820px;
                margin: 0.8rem auto 0;
                color: var(--muted);
                font-size: 1rem;
                line-height: 1.7;
                text-align: center;
            }

            .hero-rule {
                position: relative;
                z-index: 1;
                width: 84px;
                height: 3px;
                margin: 1.2rem auto 0;
                border-radius: 999px;
                background: linear-gradient(90deg, transparent, var(--accent), transparent);
            }

            .nav-caption {
                margin: 0.2rem 0 0.55rem;
                color: #6d8aa6;
                font-size: 0.73rem;
                font-weight: 700;
                letter-spacing: 0.09rem;
                text-align: center;
                text-transform: uppercase;
            }

            div[data-testid="stPageLink"] {
                width: 100%;
            }

            div[data-testid="stPageLink"] a {
                display: flex;
                min-height: 46px;
                align-items: center;
                justify-content: center;
                padding: 0.7rem 0.85rem;
                border: 1px solid var(--border);
                border-radius: 12px;
                background: rgba(12, 25, 36, 0.85);
                color: #dfeefb;
                font-weight: 650;
                text-align: center;
                transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease;
            }

            div[data-testid="stPageLink"] a:hover {
                transform: translateY(-2px);
                border-color: rgba(88, 211, 255, 0.5);
                background: rgba(88, 211, 255, 0.06);
                color: #ffffff;
            }

            div[data-testid="stPageLink"] a[aria-current="page"] {
                border-color: rgba(126, 240, 197, 0.6);
                background: linear-gradient(135deg, rgba(16, 120, 177, 0.45), rgba(39, 99, 235, 0.35));
                color: #ffffff;
                box-shadow: 0 8px 18px rgba(16, 185, 129, 0.12);
            }

            .section-heading {
                margin: 1.65rem 0 0.85rem;
                text-align: center;
            }

            .section-title {
                margin: 0;
                color: var(--text);
                font-size: 1.5rem;
                font-weight: 760;
                letter-spacing: -0.02em;
                text-align: center;
            }

            .section-description {
                margin: 0.35rem auto 0;
                max-width: 900px;
                color: var(--muted);
                font-size: 0.92rem;
                line-height: 1.6;
                text-align: center;
            }

            .kpi-card {
                height: 100%;
                min-height: 145px;
                padding: 1.2rem 1.15rem;
                border: 1px solid rgba(148, 163, 184, 0.18);
                border-radius: 18px;
                background: linear-gradient(180deg, rgba(19, 34, 46, 0.96), rgba(12, 22, 31, 0.98));
                box-shadow: 0 14px 30px rgba(2, 6, 23, 0.18);
                transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
            }

            .kpi-card:hover {
                transform: translateY(-3px);
                border-color: rgba(117, 217, 255, 0.38);
                box-shadow: 0 18px 34px rgba(2, 6, 23, 0.24);
            }

            .kpi-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 0.8rem;
            }

            .kpi-label {
                color: var(--muted);
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.08rem;
                text-transform: uppercase;
            }

            .kpi-icon {
                font-size: 1.5rem;
            }

            .kpi-value {
                margin-top: 0.65rem;
                color: var(--text);
                font-size: clamp(1.3rem, 2vw, 1.9rem);
                font-weight: 820;
                line-height: 1.2;
            }

            .kpi-value-compact {
                max-width: 100%;
                font-size: clamp(0.96rem, 1.6vw, 1.35rem);
                overflow-wrap: anywhere;
                word-break: break-word;
                white-space: normal;
            }

            .kpi-helper {
                margin-top: 0.45rem;
                color: #7b94af;
                font-size: 0.78rem;
                line-height: 1.5;
            }

            .empty-state {
                padding: 2.5rem 1.5rem;
                border: 1px dashed rgba(148, 163, 184, 0.35);
                border-radius: 18px;
                background: rgba(15, 29, 48, 0.42);
                color: var(--muted);
                text-align: center;
            }

            .empty-state-icon {
                margin-bottom: 0.7rem;
                font-size: 2.4rem;
            }

            .app-footer {
                margin-top: 2.8rem;
                padding: 1.2rem 1rem 0.75rem;
                border-top: 1px solid rgba(148, 163, 184, 0.12);
                color: #7b94af;
                font-size: 0.8rem;
                text-align: center;
            }

            div[data-testid="stDataFrame"] {
                border: 1px solid rgba(148, 163, 184, 0.18);
                border-radius: 14px;
                overflow: hidden;
            }

            @media (max-width: 800px) {
                .app-hero {
                    padding: 1.5rem 1rem;
                }

                .hero-title-row {
                    flex-direction: column;
                    gap: 0.3rem;
                }

                .hero-subtitle {
                    font-size: 0.94rem;
                }

                .kpi-card {
                    min-height: auto;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str, icon: str, eyebrow: str) -> None:
    """Render the shared professional page header."""
    header_html = (
        '<section class="app-hero">'
        f'<div class="hero-eyebrow">{escape(eyebrow)}</div>'
        '<div class="hero-title-row">'
        f'<span class="hero-icon">{escape(icon)}</span>'
        f'<h1 class="hero-title">{escape(title)}</h1>'
        '</div>'
        f'<p class="hero-subtitle">{escape(subtitle)}</p>'
        '<div class="hero-rule"></div>'
        '</section>'
    )
    st.markdown(header_html, unsafe_allow_html=True)


def section_header(title: str, description: str = "") -> None:
    """Render a reusable section heading."""
    description_html = f'<p class="section-description">{escape(description)}</p>' if description else ""
    st.markdown(
        '<div class="section-heading">'
        f'<h2 class="section-title">{escape(title)}</h2>'
        f'{description_html}'
        '</div>',
        unsafe_allow_html=True,
    )


def page_footer() -> None:
    """Render the application footer."""
    st.markdown(
        '<footer class="app-footer">'
        'Northstar Sales Analytics&nbsp;&nbsp;•&nbsp;&nbsp;'
        'Business Intelligence Platform&nbsp;&nbsp;•&nbsp;&nbsp;'
        'Version 1.0'
        '</footer>',
        unsafe_allow_html=True,
    )


def style_plotly_figure(figure, height: int = 420):
    """Apply consistent styling to a Plotly figure."""
    figure.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=25, r=25, t=60, b=35),
        legend_title_text="",
        font=dict(family="Arial", size=13),
    )
    return figure
