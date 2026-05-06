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
from f1_monza.utils.constants import IMAGE_PATH


def _encode_png(path: Path) -> str:
    """Base64-encode a PNG so it can be embedded directly in HTML."""
    return base64.b64encode(path.read_bytes()).decode()


SECTOR_COPY = {
    "All sectors": (
        "Monza is the fastest circuit on the F1 calendar — drivers spend roughly 80% of every "
        "lap at full throttle. With long straights and only a handful of slow chicanes, the "
        "cars run extreme low-downforce setups."
    ),
    "Sector 1": (
        "Sector 1 starts on the main straight — the longest flat-out stretch of the season — "
        "and ends after Variante della Roggia. Drivers reach over 350 km/h before braking hard "
        "for Variante del Rettifilo, the tight first chicane where overtakes happen on lap 1."
    ),
    "Sector 2": (
        "Sector 2 winds through the Lesmo curves and the long Curva del Serraglio. Cars stay "
        "above 280 km/h for almost the entire sector, making aerodynamic balance and tyre "
        "temperature management critical."
    ),
    "Sector 3": (
        "Sector 3 includes the second Ascari chicane and the iconic Parabolica — a long "
        "right-hander leading onto the start-finish straight. A clean exit here directly "
        "translates to top speed past the line."
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
        <div style="background:#0F0F0F;border:1px solid #262626;border-radius:8px;padding:1rem 1.2rem;">
          <div style="font-size:0.72rem;letter-spacing:0.25em;color:#9A9A9A;text-transform:uppercase;margin-bottom:0.6rem;">
            Autodromo Nazionale Monza
          </div>
          <img src="data:image/png;base64,{track_b64}" style="width:100%;height:auto;max-height:240px;object-fit:contain;margin-bottom:0.8rem;" />
          <p style="font-size:0.85rem;color:#B8B8B8;line-height:1.5;margin:0;">
            {SECTOR_COPY.get(sector, "")}
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def dashboard_layout():
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

    # Top section: track + KPIs side by side
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

    st.divider()

    # Air temperature lollipop chart at the bottom
    with st.container(border=True):
        seasons_air_temp_chart(track_filter=track)


if __name__ == "__main__":
    dashboard_layout()
