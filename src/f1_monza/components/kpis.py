import pandas as pd
import streamlit as st

from f1_monza.utils.helpers import (
    get_drivers_df,
    get_laps_df,
    get_pit_df,
    get_weather_df,
)


def _render_kpi(label: str, value: str, sublabel: str | None = None) -> None:
    """Custom KPI card matching the Power BI style — big white value, small grey label below."""
    sublabel_html = (
        f'<div style="font-size:0.7rem;color:#FF8000;font-weight:600;margin-top:0.2rem;">{sublabel}</div>'
        if sublabel
        else ""
    )
    st.markdown(
        f"""
        <div style="background:#161616;border:1px solid #262626;border-radius:8px;padding:1rem 1.2rem;height:110px;display:flex;flex-direction:column;justify-content:space-between;">
          <div style="font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#888;font-weight:600;">{label}</div>
          <div>
            <div style="font-size:1.8rem;font-weight:800;color:#FFFFFF;line-height:1;">{value}</div>
            {sublabel_html}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def laps_kpi(year: int) -> None:
    """Scheduled race distance for the Monza Italian GP."""
    from f1_monza.utils.constants import SCHEDULED_LAPS

    total_laps = SCHEDULED_LAPS.get(year)
    if total_laps is None:
        _render_kpi("LAPS", "—")
        return
    _render_kpi("LAPS", str(total_laps))


def avg_track_temp_kpi(year: int) -> None:
    """Average track temperature during the Monza race."""
    weather = get_weather_df()
    df = weather[
        (weather["year"] == year)
        & (weather["circuit_short_name"] == "Monza")
        & (weather["session_name"] == "Race")
    ]
    if df.empty or df["track_temperature"].isna().all():
        _render_kpi("AVG TRACK TEMP", "—")
        return
    avg = df["track_temperature"].mean()
    _render_kpi("AVG TRACK TEMP", f"{avg:.2f} °C")


def top_speed_kpi(year: int) -> None:
    """Highest speed-trap reading in the Monza race."""
    drivers = get_drivers_df()
    race = drivers[(drivers["year"] == year) & (drivers["session_name"] == "Race")]
    if race.empty:
        _render_kpi("TOP SPEED", "—")
        return

    session_key = int(race["session_key"].iloc[0])
    laps = get_laps_df()
    race_laps = laps[laps["session_key"] == session_key]

    top_speed = race_laps["st_speed"].max()
    if pd.isna(top_speed):
        _render_kpi("TOP SPEED", "—")
        return
    _render_kpi("TOP SPEED", f"{int(top_speed)} km/h")


def avg_lap_time_kpi(year: int) -> None:
    """Average lap duration (mm:ss.sss), excluding pit-out laps and outliers."""
    drivers = get_drivers_df()
    race = drivers[(drivers["year"] == year) & (drivers["session_name"] == "Race")]
    if race.empty:
        _render_kpi("AVG LAP TIME", "—")
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
        _render_kpi("AVG LAP TIME", "—")
        return

    avg = race_laps["lap_duration"].mean()
    minutes = int(avg // 60)
    seconds = avg - minutes * 60
    _render_kpi("AVG LAP TIME", f"{minutes}:{seconds:06.3f}")


def fastest_pit_kpi(year: int) -> None:
    """Fastest pit lane time of the race."""
    pit = get_pit_df()
    pit = pit[pit["year"] == year]
    valid = pit[pit["pit_duration"].notna() & (pit["pit_duration"] > 0)]
    if valid.empty:
        _render_kpi("FASTEST PIT LANE", "—")
        return
    fastest = valid["pit_duration"].min()
    _render_kpi("FASTEST PIT LANE", f"{fastest:.1f} s")


def fastest_pit_driver_kpi(year: int) -> None:
    """Driver and team with the fastest pit lane time."""
    pit = get_pit_df()
    pit = pit[pit["year"] == year]
    valid = pit[pit["pit_duration"].notna() & (pit["pit_duration"] > 0)]
    if valid.empty:
        _render_kpi("FASTEST PIT DRIVER", "—")
        return
    row = valid.loc[valid["pit_duration"].idxmin()]
    _render_kpi(
        "FASTEST PIT DRIVER",
        str(row["name_acronym"]),
        sublabel=str(row["team_name"]),
    )
