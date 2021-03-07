# Imports from 3rd party libraries
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
from map import get_map

# Imports from this application
from app import app

# 2 row layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
row1 = dbc.Row(
    [
        dcc.Markdown(
            """        
            ## See where your music falls in the map of music
            """
        ),
        # dcc.Link(dbc.Button('Your Call To Action', color='primary'), href='/predictions')
    ],
    # md=4,
)

# gapminder = px.data.gapminder()
# fig = px.scatter(gapminder.query("year==2007"),
#                  x="gdpPercap",
#                  y="lifeExp",
#                  size="pop",
#                  color="continent",
#                  hover_name="country",
#                  log_x=True,
#                  size_max=60,
#                  )

favorites = [
    '1xShPgQbOUa98avWJQFDBY',  # Personal Jesus - Depeche Mode
    '4ChBLndekjzQveHPsn3r6W',  # Let It Be (feat. Veela) - Blackmill
    '1pbHy9VBpSyZh56xuujZz0',  # In The Dark - DEV
]

row2 = dbc.Row(
    [
        dcc.Graph(figure=get_map(highlight=favorites))
    ]
)

layout = dbc.Col([row1, row2])
