import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import datashader as ds
import pandas as pd
import numpy as np
import colorcet as cc


def get_map(highlight=[]):
    songs = pd.read_csv('songs-tsne.zip')
    agg = ds.Canvas(plot_width=700, plot_height=700).points(songs, 'tsne1', 'tsne2')
    # imshow parameters https://plotly.com/python-api-reference/generated/plotly.express.imshow.html
    fig = px.imshow(
        img=agg,
        color_continuous_scale='ice',  # https://plotly.com/python/builtin-colorscales/
        zmax=10,
        color_continuous_midpoint=4,
        aspect='equal',
        title='A Map of 170k Songs on Spotify',
        width=800, height=800,
    )
    X = songs[songs['id'].isin(highlight)]['tsne1'].to_list()
    Y = songs[songs['id'].isin(highlight)]['tsne2'].to_list()
    fig.add_trace(go.Scatter(mode='markers', x=X, y=Y, marker=dict(
        color='LightSkyBlue',
        size=12,
        line=dict(
            color='MediumPurple',
            width=1.2
        ))))
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    return fig
