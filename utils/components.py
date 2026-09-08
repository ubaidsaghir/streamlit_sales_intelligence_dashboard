from html import escape

import streamlit as st


def kpi_card(
    label: str,
    value: str,
    icon: str,
    helper: str = "",
    compact_value: bool = False,
    tooltip: str | None = None,
) -> None:
    """Render a reusable KPI card."""
    helper_html = ""
    if helper:
        helper_html = f'<div class="kpi-helper">{escape(str(helper))}</div>'

    value_class = "kpi-value"
    if compact_value:
        value_class += " kpi-value-compact"

    tooltip_html = f' title="{escape(str(tooltip), quote=True)}"' if tooltip else ""

    card_html = (
        '<div class="kpi-card">'
        '<div class="kpi-header">'
        f'<div class="kpi-label">{escape(str(label))}</div>'
        f'<div class="kpi-icon">{escape(str(icon))}</div>'
        '</div>'
        f'<div class="{value_class}"{tooltip_html}>{escape(str(value))}</div>'
        f'{helper_html}'
        '</div>'
    )
    st.html(card_html)


def navigation_card(
    title: str,
    description: str,
    page: str,
    icon: str,
) -> None:
    """Render a page navigation card."""
    with st.container(border=True):
        st.subheader(f"{icon} {title}")
        st.caption(description)
        st.page_link(page, label=f"Open {title}", icon="➡️", width="stretch")


def empty_state(
    title: str,
    description: str,
    icon: str = "📭",
) -> None:
    """Render an empty result message."""
    st.html(
        '<div class="empty-state">'
        f'<div class="empty-state-icon">{escape(icon)}</div>'
        f'<h3>{escape(title)}</h3>'
        f'<p>{escape(description)}</p>'
        '</div>'
    )
