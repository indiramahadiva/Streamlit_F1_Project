import plotly.graph_objects as go
import streamlit as st

from f1_monza.utils.constants import COMPOUND_COLOURS
from f1_monza.utils.helpers import get_stints_df


def tyre_strategy_chart(year: int) -> None:
    stints = get_stints_df()
    stints = stints[stints["year"] == year]

    if stints.empty:
        st.info(f"No stint data available for {year}.")
        return

    stints = stints.sort_values(["name_acronym", "stint_number"])

    fig = go.Figure()
    for compound, group in stints.groupby("compound"):
        fig.add_trace(
            go.Bar(
                y=group["name_acronym"],
                x=group["stint_length"],
                name=compound,
                orientation="h",
                marker=dict(
                    color=COMPOUND_COLOURS.get(compound, "#888888"),
                    line=dict(color="#0D0D0D", width=1),
                ),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    f"Compound: {compound}<br>"
                    "Stint length: %{x:.0f} laps<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        barmode="stack",
        height=520,
        title=dict(text=f"Tyre Strategy {year} — laps per stint", x=0),
        xaxis_title="Laps",
        yaxis_title=None,
        legend=dict(orientation="h", y=-0.1, x=0),
    )
    fig.update_yaxes(categoryorder="category descending")
    st.plotly_chart(fig, width="stretch")
