from dash import Dash, callback, html, dcc

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import matplotlib as mpl
import dash_labs as dl
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import gunicorn  # whilst your local machine's webserver doesn't need this, Heroku's linux webserver (i.e. dyno) does. I.e. This is your HTTP server
from whitenoise import WhiteNoise  # for serving static files on Heroku
import json
# Instantiate dash app
violencia = pd.read_csv('./data/violencia_clean.csv')
bmanga = json.load(open('./data/barrios.geojson','r'))

app = Dash(
    __name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.FLATLY]
)

# Reference the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
server = app.server

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku)
server.wsgi_app = WhiteNoise(server.wsgi_app, root="static/")

# Define Dash l

NAVBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": "20%",
    " height": "45%",
    "width": "100%",
    "padding": "1%",
    "text-color": "white",
    "background-color": "#2EA18C",
}

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Escudo_de_Bucaramanga.svg/1200px-Escudo_de_Bucaramanga.svg.png",
                            height="30px",
                        )
                    ),
                    dbc.Col(
                        dbc.NavbarBrand(
                            "Alcaldía de Bucaramanga",
                            style={
                                "text-align": "left",
                                "text-color": "white",
                                "margin": "0px",
                            },
                        )
                    ),
                ],
                align="left",
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="#2EA18C",
    style=NAVBAR_STYLE,
)
app.layout = dbc.Container(
    [navbar, dl.plugins.page_container],
    fluid=True,
)







# Run flask app
if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8050)
