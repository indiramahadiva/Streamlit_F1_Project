import streamlit as st


def home():
    st.title("F1 — Group 2")
    st.markdown("## Italian Grand Prix · Monza 2023–2025")
    st.write(
        "Welcome! F1 is a fast-growing sport, but for new fans the data can feel overwhelming. Together with a UX design team, we're building visualizations that make the sport easier to understand.​"
    )


if __name__ == "__main__":
    home()