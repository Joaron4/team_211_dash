import csv
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc

import json
import pandas as pd
from dash_labs.plugins import register_page
import plotly.offline as py     
import plotly.express as px 
import plotly.graph_objects as go
import json
bmanga = json.load(open('./data/barrios.geojson','r'))

register_page(__name__, path="/")

violencia = pd.read_csv('./data/violencia_clean.csv')
df = pd.DataFrame(violencia[['comuna','barrio','def_naturaleza']].groupby(['comuna','barrio','def_naturaleza']).size()).rename(columns={0:'count'}).reset_index()

table_header = [
    html.Thead(html.Tr([html.Th("Principales problemáticas"), html.Th("Principales grupos poblacionales afectados")],style = {"text-align":"center","color":"#2E7DA1"}))
]
row1 = html.Tr([html.Td(html.Img(src='https://lostripulantes5.files.wordpress.com/2021/07/wordcloud.png?w=750', width="100%",height='100%')), html.Td("")])

row4 = html.Tr([html.Td("lo que sea"), html.Td("Astra")])

table_body = [html.Tbody([row1,  row4])]

# ----------------------------------


# Build App
SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "height": "100%",
    "margin": "auto",
    "padding": "0px",
    "margin": "auto",
    "border": "5px black",
    "background-color": "#2EA18C",
}
SIDEBAR_SQUARES = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "height": 100,
    "width": '99%',
    "padding": "5%",
    "margin": "auto",
    "border": "5px black",
    "background-color": "WHITE",
    'flex-flow': 'column',
    "display":"flex",
    'overflowY': 'auto',
    'overflowX': 'hidden'

}


CONTENT_STYLE = {
    "margin-left": 0,
    "margin-right": 0,
    "padding": "5%",
}

TABLE_STYLE = {
    "margin-left": 0,
    "margin-right": 0,
    "padding": "5%",
    "text-color": "#2E7DA1",
    
}
blackbold={'color':'black', 'font-weight': 'bold'}


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
        dbc.Row(
            [
                dbc.Col(
                    dbc.Col(
                        html.Img(
                            src="https://cdn.iconscout.com/icon/free/png-256/team-200-517802.png",
                            height="40 px",
                            style={
                                "margin-left": "30%",
                                "margin-bottom": "20%",
                                "margin-top": "0px",
                            },
                        ),
                        width={"size": 3, "order": 5},
                    )
                ),
                dbc.Col(
                    html.P(
                        "Enfoque poblacional",
                        style={
                            "padding": "0px",
                            "color": "black",
                            "text-aling": "center",
                            "margin-bottom ": "0",
                            "margin-top ": "20%",
                            "font-size": "0.6 vw",
                        },
                    ),
                    width={"size": 9, "order": 1},
                ),
            ],
            align="center",
        ),
        dbc.Nav(
            [
                dbc.Col(
                    dbc.Table(
                        [
                           
                        ],
                        bordered=True,
                        style=SIDEBAR_SQUARES,
                        

                        
                        
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
                dbc.Col(
                    dbc.Col(
                        html.Img(
                            src="https://freesvg.org/img/1552598586.png",
                            height="50px",
                            style={
                                "margin-left": "20%",
                                "margin-bottom": "20%",
                                "margin-top": "0px",
                            },
                        ),
                        width={"size": 2, "order": 5},
                    )
                ),
                dbc.Col(
                    html.P(
                        "Problemática",
                        style={
                            "padding": "0px",
                            "color": "black",
                            "text-aling": "center",
                            "margin-bottom ": "0",
                            "margin-top ": "20%",
                            "font-size": "0.6 vw",
                        },
                    ),
                    width={"size": 9, "order": 1},
                ),
            ],
            align="center",
        ),
        dbc.Nav(
            [
                dbc.Col(
                    dbc.Table(
                        html.Div( 
                            dcc.Dropdown(id="slct_art",
                            options=[{'label':str(b),'value':b} for b in sorted(df['def_naturaleza'].unique())],
                            value=[b for b in sorted(df['def_naturaleza'].unique())],
                            multi=False,
                            
                            
                            )),
                        bordered=True,
                        style=SIDEBAR_SQUARES,
                    ),
                ),
            ],
            vertical=True,
            pills=True,
            navbar_scroll=True,
        ),
        html.Br(),
        html.Br(),
    ],
    style=SIDEBAR_STYLE,
)
#---------------------MAPA-----------------------
content = html.Div(
    [
      
       dcc.Graph(id='my_buc_map', figure={}) 
    ],
    style=CONTENT_STYLE,
)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=2, align="left"),
                dbc.Col(
                    [
                        html.Br(),
                        # -----------------TITULO-------------------------
                        html.H1(
                            "Bucaramanga",
                            style={"textAlign": "center", "color": "#2E7DA1"},
                        ),
                        # ------------------TABLA-------------------------
                        dbc.Row(
                            [
                                dbc.Col(content),
                                dbc.Col(
                                    dbc.Table(
                                        table_header + table_body,
                                        class_name="table table-bordered border-danger",
                                        bordered=True,
                                        responsive=True,
                                    ),
                                    style=TABLE_STYLE,
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
    ]
)

@callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_buc_map', component_property='figure')],
    [Input(component_id='slct_art', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The Article chosen by user was: {}".format(option_slctd)

   

    dff = df.copy()
    dff = dff[dff["def_naturaleza"] == option_slctd]

    # Plotly Express
    fig =px.choropleth_mapbox(dff, geojson=bmanga, color= 'count',
                    locations="barrio", featureidkey= "properties.NOMBRE",
                    mapbox_style="carto-positron",
                    center={"lat": 7.12539, "lon": -73.1198},#7.12539, -73.1198
                    zoom=11.5,
                    opacity=0.5)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return  fig,container


