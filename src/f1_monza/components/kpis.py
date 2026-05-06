import streamlit as st

from f1_monza.utils.helpers import get_drivers_df, get_laps_df


def laps_kpi(year: int) -> None:
    drivers = get_drivers_df()
    race = drivers[(drivers["year"] == year) & (drivers["session_name"] == "Race")]
    if race.empty:
        st.metric(label="LAPS", value="—")
        return

    session_key = int(race["session_key"].iloc[0])
    laps = get_laps_df()
    race_laps = laps[laps["session_key"] == session_key]

    if race_laps.empty:
        st.metric(label="LAPS", value="—")
        return

    drivers_max = race_laps.groupby("driver_number")["lap_number"].max()
    total_laps = int(drivers_max.mode().iloc[0])

    st.metric(label="LAPS", value=total_laps)
