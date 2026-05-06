import streamlit as st

from f1_monza.components.filters import compound_filter, year_filter
from f1_monza.components.kpis import (
    avg_lap_time_kpi,
    avg_track_temp_kpi,
    fastest_pit_driver_kpi,
    fastest_pit_kpi,
    laps_kpi,
    top_speed_kpi,
)
from f1_monza.components.visualizations import (
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

    # Top row: 6 KPIs
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

    # Middle row: tyre strategy (2/3) + donut (1/3)
    left, right = st.columns([2, 1])
    with left:
        with st.container(border=True):
            tyre_strategy_chart(year, compounds)
    with right:
        with st.container(border=True):
            starting_tyres_chart(year)


if __name__ == "__main__":
    dashboard_layout()
