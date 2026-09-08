import pandas as pd
import streamlit as st


@st.cache_data
def dataframe_to_csv(dataframe: pd.DataFrame) -> bytes:
    """Convert a DataFrame into downloadable CSV bytes."""
    return dataframe.to_csv(index=False).encode("utf-8")


def render_csv_download(
    dataframe: pd.DataFrame,
    file_name: str,
    label: str = "Download filtered data",
    key: str | None = None,
) -> None:
    """Render a CSV download button."""
    csv_data = dataframe_to_csv(dataframe)
    st.download_button(
        label=label,
        data=csv_data,
        file_name=file_name,
        mime="text/csv",
        icon="⬇️",
        width="stretch",
        key=key,
        disabled=dataframe.empty,
    )
