import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="F1 – Group 2 | Monza",
    page_icon="🏎",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGES_DIR = Path(__file__).parent / "pages"

pages = [
    st.Page(PAGES_DIR / "home.py", title="Home", icon="🏁"),
    st.Page(PAGES_DIR / "dashboard.py", title="Dashboard", icon="📊"),
    st.Page(PAGES_DIR / "raw_data.py", title="Raw Data", icon="🗂"),
]

pg = st.navigation(pages)
pg.run()