from pathlib import Path

import re
import streamlit as st

from f1_monza.utils.constants import IMAGE_PATH, STYLE_PATH
from f1_monza.utils.helpers import (
    get_drivers_df,
    get_positions_df,
    read_css,
)


def _read_svg(path: Path) -> str:
    """Read an SVG and strip its internal <style>...</style> block.

    Streamlit's markdown renderer pulls <style> tags out of inline SVGs, which
    breaks the rendering. We remove the style block and rely on the elements'
    fill attributes (or external CSS) for colour.
    """
    svg = path.read_text(encoding="utf-8")
    # Remove the <defs><style>...</style></defs> block
    svg = re.sub(r"<defs>.*?</defs>", "", svg, flags=re.DOTALL)
    return svg


def _info_card(title: str, value: str, sublabel: str | None = None) -> None:
    """Small card used in the info and winners rows."""
    sub_html = (
        f'<div style="font-size:0.78rem;color:#B8B8B8;margin-top:0.3rem;">{sublabel}</div>'
        if sublabel
        else ""
    )
    st.markdown(
        f"""
        <div style="background:#161616;border:1px solid #262626;border-radius:8px;padding:1rem 1.2rem;height:120px;display:flex;flex-direction:column;justify-content:center;">
          <div style="font-size:0.7rem;letter-spacing:0.18em;text-transform:uppercase;color:#888;font-weight:600;margin-bottom:0.4rem;">{title}</div>
          <div style="font-size:1.4rem;font-weight:700;color:#FFFFFF;line-height:1.2;">{value}</div>
          {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _section_header(text: str) -> None:
    st.markdown(
        f"""
        <div style="font-size:0.78rem;letter-spacing:0.32em;color:#E10600;font-weight:700;margin-top:2rem;margin-bottom:0.8rem;">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _get_monza_winners() -> dict[int, tuple[str, str]]:
    """Return {year: (driver_acronym, team_name)} for the Monza race winner."""
    positions = get_positions_df()
    drivers = get_drivers_df()

    race_winners = positions[
        (positions["position"] == 1) & (positions["session_type"] == "Race")
    ]

    out: dict[int, tuple[str, str]] = {}
    for year in [2023, 2024, 2025]:
        row = race_winners[race_winners["year"] == year]
        if row.empty:
            continue
        winner_number = int(row["driver_number"].iloc[0])
        session_key = int(row["session_key"].iloc[0])

        drv = drivers[
            (drivers["session_key"] == session_key)
            & (drivers["driver_number"] == winner_number)
        ]
        if drv.empty:
            continue
        out[year] = (
            str(drv["name_acronym"].iloc[0]),
            str(drv["team_name"].iloc[0]),
        )
    return out


def home():
    read_css(STYLE_PATH / "dashboard.css")

    monza_title = _read_svg(IMAGE_PATH / "monza_title.svg")
    trackmetrics_logo = _read_svg(IMAGE_PATH / "trackmetrics_logo.svg")

    # ----- Hero with Trackmetrics logo + MONZA title -----
    hero_html = (
        '<div class="hero">'
        f'<div class="hero-logo">{trackmetrics_logo}</div>'
        '<div class="hero-eyebrow">ITALIAN GRAND PRIX</div>'
        f'<div class="hero-title-wrap">{monza_title}</div>'
        "</div>"
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    # ----- Welcome paragraph -----
    st.markdown("""
        Welcome to **F1 — Trackmetrics Dashboard**, F1 is a fast-growing sport, but for new fans the data can feel
        overwhelming. Together with a UX design team, we're building
        visualizations that make the sport easier to understand.​
        """)

    # ----- About the project -----
    _section_header("ABOUT THE PROJECT")
    cols = st.columns(3)
    with cols[0]:
        _info_card(
            "COURSE", "Data Engineering & UX Designer '25'", sublabel="Group 2 project"
        )
    with cols[1]:
        _info_card("DATA SOURCE", "OpenF1 API", sublabel="Real-time F1 telemetry")
    with cols[2]:
        _info_card("STACK", "Python · DuckDB", sublabel="Streamlit · Plotly · Power BI")

    # ----- Monza winners -----
    _section_header("ITALIAN GP WINNERS")
    winners = _get_monza_winners()
    win_cols = st.columns(3)
    for col, year in zip(win_cols, [2023, 2024, 2025]):
        with col:
            if year in winners:
                driver, team = winners[year]
                _info_card(str(year), driver, sublabel=team)
            else:
                _info_card(str(year), "—", sublabel="No data")

    # ----- New to F1? -----
    _section_header("NEW TO F1?")

    with st.expander("🏁 What's a pit stop?"):
        st.write(
            "When a driver pulls into the pit lane to swap tyres. The crew has the four "
            "wheels off and on in **2 to 3 seconds**, but the full pit-lane time is closer "
            "to **22-25 seconds** because of the speed limit on the way in and out."
        )

    with st.expander("🛞 What's a stint?"):
        st.write(
            "A continuous run of laps on the same set of tyres. Drivers do **1 to 3 stints "
            "per race**, separated by pit stops. The chart on the dashboard shows each "
            "driver's stints as coloured segments — colour matches the compound used."
        )

    with st.expander("🔴 🟡 ⚪ What are the tyre compounds?"):
        st.write(
            "Each race weekend Pirelli supplies three dry compounds:\n\n"
            "- **🔴 SOFT** — fastest but wears out quickly\n"
            "- **🟡 MEDIUM** — the all-rounder\n"
            "- **⚪ HARD** — slower but lasts longer\n\n"
            "Choosing **when to pit** and **which compound to switch to** is what separates "
            "a podium from a midfield finish."
        )

    with st.expander("📊 How do I use this dashboard?"):
        st.write(
            "Open **Dashboard** in the sidebar to see KPIs and charts for each year. "
            "Use the **Season** filter to switch between 2023, 2024, and 2025. "
            "Toggle **Sector view** to see different parts of the track highlighted. "
            "Browse **Raw Data** to see the underlying CSVs."
        )


if __name__ == "__main__":
    home()
