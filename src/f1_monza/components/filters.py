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


from f1_monza.utils.helpers import get_stints_df


def compound_filter(key: str = "compound_filter") -> list[str]:
    """Multi-select of tyre compounds present in the data."""
    compounds = sorted(get_stints_df()["compound"].dropna().unique().tolist())
    return st.multiselect(
        label="Compound",
        options=compounds,
        default=compounds,
        key=key,
    )


def session_filter(key: str = "session_filter") -> str:
    """Toggle between Qualifying and Race for the fastest lap chart."""
    return st.radio(
        label="Session",
        options=["Qualifying", "Race"],
        index=1,
        horizontal=True,
        key=key,
    )


def lap_metric_filter(key: str = "lap_metric_filter") -> str:
    """Choose between full-lap and per-sector view."""
    return st.radio(
        label="View",
        options=["Lap", "Sector 1", "Sector 2", "Sector 3"],
        index=0,
        horizontal=True,
        key=key,
    )
