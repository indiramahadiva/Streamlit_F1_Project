from pathlib import Path

import pandas as pd
import streamlit as st

from f1_monza.utils.constants import DATA_PATH


def read_textfile(path: Path) -> str:
    """Read a plain text or markdown file."""
    with open(path, encoding="utf-8") as file:
        return file.read()


def read_css(path: Path) -> None:
    """Inject a CSS file into the Streamlit page."""
    css = read_textfile(path)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Data loaders
# -----------------------------------------------------------------------------
@st.cache_data
def get_stints_df() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH / "stints.csv")


@st.cache_data
def get_pit_df() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH / "pit_with_compound.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


@st.cache_data
def get_drivers_df() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH / "drivers_clean_updated.csv")


@st.cache_data
def get_laps_df() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH / "laps_clean_updated.csv")


@st.cache_data
def get_positions_df() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH / "final_positions.csv")


@st.cache_data
def get_weather_df() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH / "all_weather_data.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)
    return df


@st.cache_data
def get_sessions_df() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH / "sessions_data.csv")


@st.cache_data
def get_seasons_air_temp() -> pd.DataFrame:
    """Race-only mean air temperature per track per year — for the cross-track line chart."""
    df = get_weather_df()
    race = df[df["session_name"] == "Race"]
    agg = (
        race.groupby(["year", "circuit_short_name"])["air_temperature"]
        .mean()
        .round(1)
        .reset_index()
    )
    return agg
