from dash import  callback, html, dcc, Input, Output, MATCH, ALL
import dash_bootstrap_components as dbc

import json
import pandas as pd
from dash_labs.plugins import register_page   
import plotly.express as px 
import json
bmanga = json.load(open('./data/barrios.geojson','r'))
register_page(__name__, path="/crimes")

delitos = pd.read_csv('./data/delitos_final.csv')

df = delitos.groupby(["ano"]).size().to_frame("quantity").reset_index()
df1 = df.to_dict()

table_header = [
    html.Thead(html.Tr([html.Th("Principales problemáticas"), html.Th("Principales grupos poblacionales afectados")],style = {"text-align":"center","color":"#2E7DA1"}))
]
row1 = html.Tr([html.Td(html.Img(src='https://lostripulantes5.files.wordpress.com/2021/07/wordcloud.png?w=750', width="100%",height='100%')), html.Td("")])

row4 = html.Tr([html.Td("lo que sea"), html.Td("Astra")])

table_body = [html.Tbody([row1,  row4])]

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



#---------------------MAPA-----------------------
content = html.Div(
    [
        
        dcc.Graph(id='my_buc_map',figure={}) 
    ],
    style=CONTENT_STYLE,
)
 

layout = html.Div(
    [   dcc.Store(id="stored-data", data=df1),
        dbc.Row(
            [
                
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