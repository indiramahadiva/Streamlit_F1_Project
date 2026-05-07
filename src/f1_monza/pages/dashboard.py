import base64
from pathlib import Path

import streamlit as st

from f1_monza.components.filters import (
    air_temp_track_filter,
    compound_filter,
    lap_metric_filter,
    sector_filter,
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
from f1_monza.utils.constants import IMAGE_PATH, STYLE_PATH
from f1_monza.utils.helpers import read_css


def _encode_png(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def _read_svg(path: Path) -> str:
    return path.read_text(encoding="utf-8")


SECTOR_COPY = {
    "All sectors": (
        "Monza is the fastest track on the F1 calendar, nicknamed the 'Temple of Speed'. At 5.793 km with only 11 corners, drivers spend around 80% of the lap at full throttle. The low-downforce setup rewards slipstreaming and bravery into the chicanes."
    ),
    "Sector 1": (
        "Sector 1 starts on the main straight — the longest flat-out stretch of the season — and ends after Variante della Roggia. Drivers reach over 350 km/h before braking hard for Variante del Rettifilo, the tight first chicane where overtakes happen on lap 1."
    ),
    "Sector 2": (
        "Sector 2 runs through Curva di Lesmo 1 and 2, down to Ascari. Monza's most technical section: medium-to-high speed corners where aerodynamic balance separates the front-runners. Ascari demands precision — small errors cost big time."
    ),
    "Sector 3": (
        "Sector 3 is defined by the legendary Parabolica — a long sweeping right-hander leading onto the main straight. Carrying speed through Parabolica is critical because lost momentum compounds across the kilometre-long straight."
    ),
}


def _track_panel(sector: str) -> None:
    """Track image + sector commentary panel."""
    sector_to_file = {
        "All sectors": "track_full.png",
        "Sector 1": "track_sector_1.png",
        "Sector 2": "track_sector_2.png",
        "Sector 3": "track_sector_3.png",
    }
    track_b64 = _encode_png(IMAGE_PATH / sector_to_file[sector])
    st.markdown(
        f"""
        <div class="track-panel">
          <div class="track-eyebrow">Autodromo Nazionale Monza</div>
          <img class="track-img" src="data:image/png;base64,{track_b64}" alt="Monza track" />
          <p class="track-copy">{SECTOR_COPY.get(sector, "")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _tyre_legend() -> None:
    soft = _read_svg(IMAGE_PATH / "wheel_soft.svg")
    medium = _read_svg(IMAGE_PATH / "wheel_medium.svg")
    hard = _read_svg(IMAGE_PATH / "wheel_hard.svg")
    st.markdown(
        f"""
        <div class="tyre-legend">
            <div class="tyre-item">{hard}<span>HARD</span></div>
            <div class="tyre-item">{medium}<span>MEDIUM</span></div>
            <div class="tyre-item">{soft}<span>SOFT</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def dashboard_layout():
    read_css(STYLE_PATH / "dashboard.css")

    st.title("Dashboard")
    st.caption("Italian Grand Prix · Monza")

    with st.sidebar:
        st.markdown("### Filters")
        year = year_filter()
        compounds = compound_filter()
        sector = sector_filter()
        st.markdown("---")
        st.markdown("### Air-temp chart")
        track = air_temp_track_filter()

    # Top section: track + KPIs side by side (2x3 grid)
    track_col, kpi_col = st.columns([1, 2])
    with track_col:
        _track_panel(sector)
    with kpi_col:
        r1 = st.columns(3)
        with r1[0]:
            laps_kpi(year)
        with r1[1]:
            avg_track_temp_kpi(year)
        with r1[2]:
            top_speed_kpi(year)
        r2 = st.columns(3)
        with r2[0]:
            avg_lap_time_kpi(year)
        with r2[1]:
            fastest_pit_kpi(year)
        with r2[2]:
            fastest_pit_driver_kpi(year)

    st.divider()

    # Fastest lap gap chart with toggles
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

    _tyre_legend()

    st.divider()

    # Air temperature lollipop chart at the bottom
    with st.container(border=True):
        seasons_air_temp_chart(track_filter=track)


if __name__ == "__main__":
    dashboard_layout()
