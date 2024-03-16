import numpy as np
import datetime
import plotly.graph_objects as go
import streamlit as st

def plot_hourly_series(
    *args,
    colors=("#1d3c34", "#4d4b32", "#4d4b32"),
    xlabel=None,
    ylabel=None,
    ymin=None,
    ymax=None,
    height=200,
    showlegend=True,
    linemode=False,
    xtick_datemode=True
):
    num_series = len(args) // 2
    colors = colors[:num_series]  # Ensure colors match the number of series
    y_arrays = [arg for arg in args[::2]]
    if xtick_datemode:
        start = datetime.datetime(2023, 1, 1, 0)  # Start from January 1, 2023, 00:00
        end = datetime.datetime(2023, 12, 31, 23)  # End on December 31, 2023, 23:00
        hours = int((end - start).total_seconds() / 3600) + 1
        x_arr = np.array([start + datetime.timedelta(hours=i) for i in range(hours)])
        ticksuffix = None
    else:
        x_arr = np.arange(0, 8760, 1)
        start = 0
        end = 8760
        ticksuffix = ' t'
    fig = go.Figure()
    if linemode == False:
        stackgroup='one'
        fill='tonexty'
        width=0
        barmode='stack'
    else:
        stackgroup, fill, width, barmode = None, None, 1, None
    for i in range(num_series):
        fig.add_trace(
            go.Scatter(
                x=x_arr,
                y=y_arrays[i],
                stackgroup=stackgroup,
                fill=fill,
                line=dict(width=width, color=colors[i]),
                name=f"{args[i*2+1]}:<br>{int(round(np.sum(y_arrays[i]),-2)):,} kWh/år | {float(round(np.max(y_arrays[i]),1)):,} kW".replace(",", " ").replace(".", ",")
                )
            )
    fig.update_layout(
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.01, bgcolor="rgba(0,0,0,0)"),
        height=height,
        xaxis_title=xlabel, 
        yaxis_title=ylabel,
        barmode=barmode, 
        margin=dict(l=0, r=0, t=0, b=0, pad=0),
        showlegend=showlegend
    )
    fig.update_xaxes(
        ticksuffix=ticksuffix,
        tickformat="%d.%b",
        range=[start, end],
        mirror=True,
        ticks="outside",
        showline=True,
        linecolor="black",
        gridcolor="lightgrey",
    )
    fig.update_yaxes(
        ticksuffix=' kW',
        range=[ymin, ymax],
        mirror=True,
        ticks="outside",
        showline=True,
        linecolor="black",
        gridcolor="lightgrey",
    )
    st.plotly_chart(fig, use_container_width=True, config = {'displayModeBar': False, 'staticPlot': False})
