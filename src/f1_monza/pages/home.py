import base64
from pathlib import Path

import streamlit as st

from f1_monza.utils.constants import IMAGE_PATH, STYLE_PATH
from f1_monza.utils.helpers import read_css


def _read_svg(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _encode_png(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def home():
    read_css(STYLE_PATH / "dashboard.css")

    monza_title = _read_svg(IMAGE_PATH / "monza_title.svg")
    track_b64 = _encode_png(IMAGE_PATH / "track_full.png")

    # Hero — title and tagline only
    hero_html = (
        '<div class="hero">'
        f'<div class="hero-title-wrap">{monza_title}</div>'
        '<div class="hero-tagline">Trackmetrics - Group 2 </div>'
        "</div>"
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    # Track image + welcome text side by side
    img_col, text_col = st.columns([1, 1])

    with img_col:
        track_html = (
            '<div class="hero-track">'
            f'<img src="data:image/png;base64,{track_b64}" alt="Autodromo Nazionale Monza" />'
            '<div class="hero-track-caption">Autodromo Nazionale Monza</div>'
            "</div>"
        )
        st.markdown(track_html, unsafe_allow_html=True)

    with text_col:
        st.markdown("""
            ## Welcome to Monza

            Monza is the **fastest circuit on the F1 calendar** — drivers spend roughly 80%
            of every lap at full throttle.

            For new fans, this race is the perfect place to start understanding
            **laps, sectors and tyre strategy** — two of the most decisive levers in modern Formula 1.

            Use the navigation on the left to open the dashboard or browse the raw data.
            """)


if __name__ == "__main__":
    home()
