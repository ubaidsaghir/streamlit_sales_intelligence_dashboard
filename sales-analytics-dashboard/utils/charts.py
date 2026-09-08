from __future__ import annotations

import plotly.express as px


def line_chart(df, x_col, y_col, title, color="#1d9bf0"):
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        markers=True,
        title=title,
        template="plotly_white",
        color_discrete_sequence=[color],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


def bar_chart(df, x_col, y_col, title, horizontal=False, color_scale="Blues"):
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        orientation="h" if horizontal else "v",
        title=title,
        template="plotly_white",
        color=y_col if not horizontal else x_col,
        color_continuous_scale=color_scale,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


def area_chart(df, x_col, y_col, title, color="#56ccf2"):
    fig = px.area(
        df,
        x=x_col,
        y=y_col,
        title=title,
        template="plotly_white",
        color_discrete_sequence=[color],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


def pie_chart(df, names_col, values_col, title):
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title,
        template="plotly_white",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


def scatter_chart(df, x_col, y_col, title, color_col=None):
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col if color_col else None,
        title=title,
        template="plotly_white",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig
