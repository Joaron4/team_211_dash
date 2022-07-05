from dash import  callback, html, dcc, Input, Output, MATCH, ALL
import dash_bootstrap_components as dbc

import json
import pandas as pd
from dash_labs.plugins import register_page   
import plotly.express as px 
import json
register_page(__name__, path="/crimes")

layout = html.Div(
    [
       
        dcc.Graph(id="bar-chart"),
    ]
)