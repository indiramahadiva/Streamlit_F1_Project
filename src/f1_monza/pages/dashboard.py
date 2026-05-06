import streamlit as st

from f1_monza.components.filters import (
    air_temp_track_filter,
    compound_filter,
    lap_metric_filter,
    session_filter,
    year_filter,
)
from f1_monza.components.kpis import (
    avg_lap_time_kpi,
    avg_track_temp_kpi,
    fastest_pit_driver_kpi,
    fastest_pit_kpi,
    laps_kpi,
    top_speed_kpi,
)
from f1_monza.components.visualizations import (
    fastest_lap_gap_chart,
    seasons_air_temp_chart,
    starting_tyres_chart,
    tyre_strategy_chart,
)


def dashboard_layout():
    st.title("Dashboard")
    st.caption("Italian Grand Prix · Monza")

    with st.sidebar:
        st.markdown("### Filters")
        year = year_filter()
        compounds = compound_filter()
        st.markdown("---")
        st.markdown("### Air-temp chart")
        track = air_temp_track_filter()

    # KPI row
    kpi_cols = st.columns(6)
    with kpi_cols[0]:
        laps_kpi(year)
    with kpi_cols[1]:
        avg_track_temp_kpi(year)
    with kpi_cols[2]:
        top_speed_kpi(year)
    with kpi_cols[3]:
        avg_lap_time_kpi(year)
    with kpi_cols[4]:
        fastest_pit_kpi(year)
    with kpi_cols[5]:
        fastest_pit_driver_kpi(year)

    st.divider()

    # Fastest lap gap chart
    st.markdown("### Fastest lap analysis")
    toggle_cols = st.columns([1, 2])
    with toggle_cols[0]:
        session_type = session_filter()
    with toggle_cols[1]:
        metric = lap_metric_filter()
    with st.container(border=True):
        fastest_lap_gap_chart(year, session_type=session_type, metric=metric)

    st.divider()

    # Tyre strategy + starting tyres
    left, right = st.columns([2, 1])
    with left:
        with st.container(border=True):
            tyre_strategy_chart(year, compounds)
    with right:
        with st.container(border=True):
            starting_tyres_chart(year)

    st.divider()

    # Air temperature line chart at the bottom
    with st.container(border=True):
        seasons_air_temp_chart(track_filter=track)


if __name__ == "__main__":
    dashboard_layout()
