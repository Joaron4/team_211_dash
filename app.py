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
df = pd.DataFrame(violencia[['comuna','barrio','def_naturaleza','nom_actividad']].groupby(['comuna','barrio','def_naturaleza','nom_actividad']).size()).rename(columns={0:'count'}).reset_index()

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
# ------------SIDEBAR-------------------------------
sidebar = html.Div(
    [
        html.H2(
            "Team 211",
            className="border border-secondary",
            style={
                "color": "#2E7DA1",
                "padding": "5%",
                "background-color": "white",
                "textAlign": "center",
            },
        ),
        html.P(
            "Seleccione uno o más filtros para personalizar su búsqueda",
            className="lead",
            style={"color": "white", "padding": "5%", "font-size": "1 vw"},
        ),
        html.Hr(style={"width": "95%", "margin": "auto", "background-color": "black"}),
        html.Br(),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem(dbc.NavLink("Violencia de género", active=True, href="/")),
             dbc.DropdownMenuItem(dbc.NavLink("crimenes", active=True, href="/crimes"))],
            label="Problemas",
            nav=True,
            className='dropdown-item btn btn-danger'
        ),
        html.Hr(style={"width": "95%", "margin": "auto", "background-color": "black"}),
        html.Br(),
        dbc.Row(
            [
                
                    
                
                    html.P(
                        "Enfoque poblacional",
                        className= 'problematica'
                        
                    ),
                   
              
                
            ],
            align="center",
        ),
        dbc.Nav(
            [
                dbc.Col(
                    dbc.Table(
                     html.Div( 
                           
                            id='dropdown-container1', children=[])
                        

                        
                        
                    ),
                ),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(style={"width": "95%", "margin": "auto", "background-color": "black"}),
        html.Br(),
        dbc.Row(
            [
                
                
                    html.P( 
                        "Problemática",className='problematica',
                        
                    ),
                    
                
            ],
            align="center",
        ),
        dbc.Nav(
            [
                dbc.Col(

                    dbc.Table(
                        html.Div(  id='dropdown-container2', children=[]
                            )),
                        
                    
                ),
            ],
            vertical=True,
            pills=True,
            navbar_scroll=True,
        ),
        html.Br(),
        html.Br(),
    ],
   id='SIDEBAR_STYLE',  
)
app.layout = dbc.Container(
    [dbc.Row([

        navbar,
        dbc.Col( sidebar,width=3,align="left"),
        dbc.Col( dl.plugins.page_container,align="left",className='g-0')
    ])],
    className='g-0',
    fluid=True,
)








# Run flask app
if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8050)