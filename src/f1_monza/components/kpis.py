import streamlit as st
import pandas as pd

from f1_monza.utils.helpers import get_drivers_df, get_laps_df
from f1_monza.utils.helpers import get_weather_df


def laps_kpi(year: int) -> None:
    """Scheduled race distance for the Monza Italian GP."""
    from f1_monza.utils.constants import SCHEDULED_LAPS

    total_laps = SCHEDULED_LAPS.get(year)
    if total_laps is None:
        st.metric(label="LAPS", value="—")
        return
    st.metric(label="LAPS", value=total_laps)


def avg_track_temp_kpi(year: int) -> None:
    """Average track temperature during the Monza race."""
    weather = get_weather_df()
    df = weather[
        (weather["year"] == year)
        & (weather["circuit_short_name"] == "Monza")
        & (weather["session_name"] == "Race")
    ]
    if df.empty or df["track_temperature"].isna().all():
        st.metric(label="AVG TRACK TEMP", value="—")
        return
    avg = df["track_temperature"].mean()
    st.metric(label="AVG TRACK TEMP", value=f"{avg:.2f} °C")


def top_speed_kpi(year: int) -> None:
    """Highest speed-trap reading in the Monza race."""
    drivers = get_drivers_df()
    race = drivers[(drivers["year"] == year) & (drivers["session_name"] == "Race")]
    if race.empty:
        st.metric(label="TOP SPEED", value="—")
        return

    session_key = int(race["session_key"].iloc[0])
    laps = get_laps_df()
    race_laps = laps[laps["session_key"] == session_key]

    top_speed = race_laps["st_speed"].max()
    if pd.isna(top_speed):
        st.metric(label="TOP SPEED", value="—")
        return
    st.metric(label="TOP SPEED", value=f"{int(top_speed)} km/h")


def avg_lap_time_kpi(year: int) -> None:
    """Average lap duration (mm:ss.sss), excluding pit-out laps and outliers."""
    drivers = get_drivers_df()
    race = drivers[(drivers["year"] == year) & (drivers["session_name"] == "Race")]
    if race.empty:
        st.metric(label="AVG LAP TIME", value="—")
        return

    session_key = int(race["session_key"].iloc[0])
    laps = get_laps_df()
    race_laps = laps[
        (laps["session_key"] == session_key)
        & (laps["is_pit_out_lap"] == False)  # noqa: E712
        & (laps["lap_duration"].notna())
        & (laps["lap_duration"] < 180)
    ]
    if race_laps.empty:
        st.metric(label="AVG LAP TIME", value="—")
        return

    avg = race_laps["lap_duration"].mean()
    minutes = int(avg // 60)
    seconds = avg - minutes * 60
    st.metric(label="AVG LAP TIME", value=f"{minutes}:{seconds:06.3f}")
