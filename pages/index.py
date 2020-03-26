import pickle
import dash
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go


from app import app


column1 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## Balence Chemical Equations

            Some chemical equations are easy to balence, and some arent. This works on both.
            """
        ),
        dcc.Link(dbc.Button('Alright, let's get to it then', color='primary'), href='/balence')
    ],
    md=4,
)


layout = dbc.Row([column1, column2])
