import streamlit as st

from f1_monza.components.visualizations import tyre_strategy_chart


def dashboard_layout():
    st.title("Dashboard")
    st.caption("Italian Grand Prix · Monza")

    tyre_strategy_chart(year=2025)


if __name__ == "__main__":
    dashboard_layout()
