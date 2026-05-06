import streamlit as st

from f1_monza.utils.constants import MONZA_YEARS


def year_filter(key: str = "year_filter", default_index: int = 2) -> int:
    """Year picker. Default index 2 = 2025."""
    return st.selectbox(
        label="Season",
        options=MONZA_YEARS,
        index=default_index,
        key=key,
    )
