import re
from pathlib import Path

import streamlit as st

from f1_monza.utils.constants import IMAGE_PATH, MARKDOWN_PATH, STYLE_PATH
from f1_monza.utils.helpers import (
    get_drivers_df,
    get_positions_df,
    read_css,
    read_textfile,
)


def _read_svg(path: Path) -> str:
    """Read an SVG and strip its internal <style>...</style> block.

    Streamlit's markdown renderer pulls <style> tags out of inline SVGs, which
    breaks the rendering. We remove the style block and rely on external CSS
    for colour.
    """
    svg = path.read_text(encoding="utf-8")
    svg = re.sub(r"<defs>.*?</defs>", "", svg, flags=re.DOTALL)
    return svg


def _info_card(title: str, value: str, sublabel: str | None = None) -> None:
    sub_html = f'<div class="info-card-sublabel">{sublabel}</div>' if sublabel else ""
    st.markdown(
        f"""
        <div class="info-card">
          <div class="info-card-title">{title}</div>
          <div class="info-card-value">{value}</div>
          {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _section_header(text: str) -> None:
    st.markdown(
        f'<div class="section-header">{text}</div>',
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

    # ----- Hero -----
    hero_html = (
        '<div class="hero">'
        f'<div class="hero-logo">{trackmetrics_logo}</div>'
        f'<div class="hero-title-wrap">{monza_title}</div>'
        "</div>"
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    # ----- Welcome paragraph -----
    st.markdown(read_textfile(MARKDOWN_PATH / "welcome.md"))

    # ----- About the project -----
    _section_header("ABOUT THE PROJECT")
    cols = st.columns(3)
    with cols[0]:
        _info_card(
            "COURSE", "Data Engineering '25", sublabel="Group project, 4 students"
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
        st.markdown(read_textfile(MARKDOWN_PATH / "pit_stop_explainer.md"))

    with st.expander("🛞 What's a stint?"):
        st.markdown(read_textfile(MARKDOWN_PATH / "stint_explainer.md"))

    with st.expander("🔴 🟡 ⚪ What are the tyre compounds?"):
        st.markdown(read_textfile(MARKDOWN_PATH / "compounds_explainer.md"))

    with st.expander("📊 How do I use this dashboard?"):
        st.markdown(read_textfile(MARKDOWN_PATH / "dashboard_usage.md"))


if __name__ == "__main__":
    home()
