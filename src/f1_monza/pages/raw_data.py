import streamlit as st

from f1_monza.utils.helpers import (
    get_drivers_df,
    get_laps_df,
    get_pit_df,
    get_positions_df,
    get_sessions_df,
    get_stints_df,
    get_weather_df,
)


def raw_data():
    st.title("Raw Data")
    st.caption(
        "All tables fetched from the OpenF1 API and exported to CSV. "
        "Use the tabs below to inspect each dataset."
    )

    tabs = st.tabs(
        ["Stints", "Pit stops", "Drivers", "Laps", "Positions", "Weather", "Sessions"]
    )

    with tabs[0]:
        st.dataframe(get_stints_df(), width="stretch")
    with tabs[1]:
        st.dataframe(get_pit_df(), width="stretch")
    with tabs[2]:
        st.dataframe(get_drivers_df(), width="stretch")
    with tabs[3]:
        st.dataframe(get_laps_df(), width="stretch")
    with tabs[4]:
        st.dataframe(get_positions_df(), width="stretch")
    with tabs[5]:
        st.dataframe(get_weather_df(), width="stretch")
    with tabs[6]:
        st.dataframe(get_sessions_df(), width="stretch")


if __name__ == "__main__":
    raw_data()