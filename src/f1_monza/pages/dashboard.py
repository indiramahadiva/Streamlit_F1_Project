import streamlit as st

from f1_monza.components.filters import year_filter
from f1_monza.components.kpis import (
    avg_lap_time_kpi,
    avg_track_temp_kpi,
    laps_kpi,
    top_speed_kpi,
)
from f1_monza.components.visualizations import tyre_strategy_chart


def dashboard_layout():
    st.title("Dashboard")
    st.caption("Italian Grand Prix · Monza")

    with st.sidebar:
        st.markdown("### Filters")
        year = year_filter()

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        laps_kpi(year)
    with kpi_cols[1]:
        avg_track_temp_kpi(year)
    with kpi_cols[2]:
        top_speed_kpi(year)
    with kpi_cols[3]:
        avg_lap_time_kpi(year)

    st.divider()

    tyre_strategy_chart(year)


if __name__ == "__main__":
    dashboard_layout()
