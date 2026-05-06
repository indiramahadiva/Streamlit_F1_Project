import plotly.graph_objects as go
import streamlit as st

from f1_monza.utils.constants import COMPOUND_COLOURS
from f1_monza.utils.helpers import get_drivers_df, get_laps_df, get_stints_df


def tyre_strategy_chart(year: int, compounds: list[str] | None = None) -> None:
    stints = get_stints_df()
    stints = stints[stints["year"] == year]

    if compounds:
        stints = stints[stints["compound"].isin(compounds)]

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


def starting_tyres_chart(year: int) -> None:
    """Donut chart: which compound did drivers start the race on?"""
    stints = get_stints_df()
    stints = stints[stints["year"] == year]

    starting = stints[stints["stint_number"] == 1]
    if starting.empty:
        st.info(f"No starting-tyre data available for {year}.")
        return

    counts = starting["compound"].value_counts().reset_index()
    counts.columns = ["compound", "drivers"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=counts["compound"],
                values=counts["drivers"],
                hole=0.55,
                marker=dict(
                    colors=[
                        COMPOUND_COLOURS.get(c, "#888888") for c in counts["compound"]
                    ],
                    line=dict(color="#0D0D0D", width=2),
                ),
                textinfo="label+value",
                textfont=dict(size=14, color="#0D0D0D"),
                hovertemplate="<b>%{label}</b><br>%{value} drivers<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        height=420,
        title=dict(text="Drivers' Starting Tyres", x=0),
        showlegend=False,
    )
    st.plotly_chart(fig, width="stretch")


def fastest_lap_gap_chart(
    year: int, session_type: str = "Race", metric: str = "Lap"
) -> None:
    """Bar chart of gap-to-fastest, ranked slowest at top.

    For sector views, takes each driver's fastest LAP and reads the corresponding
    sector duration from that lap.
    """
    drivers = get_drivers_df()
    laps = get_laps_df()

    session_rows = drivers[
        (drivers["year"] == year) & (drivers["session_name"] == session_type)
    ]
    if session_rows.empty:
        st.info(f"No {session_type} session found for {year}.")
        return
    session_key = int(session_rows["session_key"].iloc[0])

    metric_to_col = {
        "Lap": "lap_duration",
        "Sector 1": "duration_sector_1",
        "Sector 2": "duration_sector_2",
        "Sector 3": "duration_sector_3",
    }
    col = metric_to_col[metric]

    session_laps = laps[
        (laps["session_key"] == session_key)
        & (laps["is_pit_out_lap"] == False)  # noqa: E712
        & (laps["lap_duration"].notna())
        & (laps["lap_duration"] < 180)
    ].copy()
    if session_laps.empty:
        st.info(f"No valid laps in {year} {session_type}.")
        return

    fastest_idx = session_laps.groupby("driver_number")["lap_duration"].idxmin()
    fastest_laps = session_laps.loc[fastest_idx].copy()
    fastest_laps = fastest_laps[fastest_laps[col].notna()]
    if fastest_laps.empty:
        st.info(f"No {metric} data available for {year} {session_type}.")
        return

    driver_lookup = drivers[drivers["session_key"] == session_key][
        ["driver_number", "name_acronym", "team_name", "team_colour"]
    ].drop_duplicates("driver_number")
    fastest_laps = fastest_laps.merge(driver_lookup, on="driver_number", how="left")

    fastest_value = fastest_laps[col].min()
    fastest_laps["gap"] = fastest_laps[col] - fastest_value
    fastest_laps = fastest_laps.sort_values("gap", ascending=False)
    fastest_laps["rank"] = fastest_laps["gap"].rank(method="min").astype(int)
    fastest_laps["label"] = fastest_laps.apply(
        lambda r: f"P{int(r['rank']):02d}. {r['name_acronym']}", axis=1
    )

    def _format_gap(row):
        if row["gap"] == 0:
            # Pole/fastest gets the absolute time
            if metric == "Lap":
                # Format full lap time as M:SS.sss
                total = row[col]
                minutes = int(total // 60)
                seconds = total - minutes * 60
                return f"{minutes}:{seconds:06.3f}"
            # Sector times stay as plain seconds
            return f"{row[col]:.3f}"
        return f"+{row['gap']:.3f}"

    fastest_laps["gap_text"] = fastest_laps.apply(_format_gap, axis=1)
    fastest_laps["team_colour"] = fastest_laps["team_colour"].fillna("888888")
    fastest_laps["bar_colour"] = "#" + fastest_laps["team_colour"].astype(str)

    fig = go.Figure(
        go.Bar(
            x=fastest_laps["gap"],
            y=fastest_laps["label"],
            orientation="h",
            marker=dict(
                color=fastest_laps["bar_colour"], line=dict(color="#0D0D0D", width=0.5)
            ),
            text=fastest_laps["gap_text"],
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                f"{metric}: %{{customdata:.3f}}s<br>"
                "Gap: %{x:.3f}s<extra></extra>"
            ),
            customdata=fastest_laps[col],
        )
    )
    fig.update_layout(
        height=560,
        title=dict(text=f"Fastest {metric.lower()} — {session_type} {year}", x=0),
        showlegend=False,
        bargap=0.25,
        xaxis_title="Gap to fastest (seconds)",
    )
    st.plotly_chart(fig, width="stretch")
