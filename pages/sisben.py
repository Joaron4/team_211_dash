from dash import  callback, html, dcc, Input, Output, MATCH, ALL
import dash_bootstrap_components as dbc

import json
import pandas as pd
from dash_labs.plugins import register_page
import plotly.express as px
import json
from sidebar import create_sidebar

# app = Dash(__name__)

register_page(__name__, path="/sisben")

sidebar= create_sidebar('dropdown_slct_barrios','dropdown_tempana')

# load datasets----------------------------------------------
bmanga = json.load(open('./data/barrios.geojson','r',encoding='utf-8'))

df_GrupoSisben = pd.read_csv('https://raw.githubusercontent.com/Joaron4/team211_datasets/main/S4_Grupo_SisbenIV.csv',sep=';',encoding="utf_8")
df_GrupoSisben_1 = df_GrupoSisben.to_dict()
#print(df_GrupoSisben)

df_Sexo = pd.read_csv('https://raw.githubusercontent.com/Joaron4/team211_datasets/main/S4_Sexo_IV.csv',sep=';',encoding="utf_8")
df_Sexo_1 = df_Sexo.to_dict()
# print(df_Sexo)

df_GrupoEtario = pd.read_csv('https://raw.githubusercontent.com/Joaron4/team211_datasets/main/S4_Rango_Etario_IV.csv',sep=';',encoding="utf_8")
df_GrupoEtario_1 = df_GrupoEtario.to_dict()
# print(df_GrupoEtario)

# main geojson
# from urllib.request import urlopen
# import json
# with urlopen('https://raw.githubusercontent.com/Joaron4/team211_datasets/main/Barrios-polygon.geojson') as response:
#       counties = json.load(response)
# just for check, too
# print(counties)

dataset_selected = 1



# ----------------------------------------------------------------
# Layer principal de la pagina

table_header = [
    html.Thead(html.Tr([html.Th("Personas por Rangos Etarios"), html.Th("Personas por Sexo")],style = {"text-align":"center","color":"#2E7DA1"}))
]
row1 = html.Tr([html.Td(html.Img(src='https://lostripulantes5.files.wordpress.com/2021/07/wordcloud.png?w=750', width="100%",height='100%')), html.Td("")])

row4 = html.Tr([
        html.Td("*Informacion calculada con los datos de edad calculada capturados en la encuesta SISBEN IV"),
        html.Td("**Informacion obtenidos con los datos de sexo capturados en la encuesta SISBEN IV")
])

table_body = [html.Tbody([row1,  row4])]

#------------------------------------------------------------------
# contenido de la estructura de la pagina
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
    "display": "flex",
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
blackbold = {'color': 'black', 'font-weight': 'bold'}



# ---------------------MAPA-----------------------
content = html.Div(
    [

       

        # html.Div(id='output_container', children=[]),
        html.Br(),

        dcc.Graph(id='mi_buc_map', figure={})
    ],
    style=CONTENT_STYLE,
)



# ------------------------------------------------------------------------------
# App layout
# app.layout = html.Div([
layout = html.Div(
    [dcc.Store(id="stored-sisben",
               data=df_GrupoSisben_1
               ),
    dcc.Store(id="stored-sisben1",
               data=df_GrupoEtario_1
               ),
    #df_Sexo_1
    dcc.Store(id="stored-sisben2",
               data=df_Sexo_1
               ),
     dbc.Row(
         [
            dbc.Col(sidebar, width=3, align="left"),
            dbc.Col(
                 [
                     html.Br(),
                     # -----------------TITULO-------------------------
                     html.H1(
                         "Bucaramanga - SISBEN IV",
                         style={"textAlign": "center", "color": "#2E7DA1"},
                     ),
                     # ------------------TABLA-------------------------
                     dbc.Row(
                         [
                             dbc.Col(content),
                             dbc.Col(
                                 # dbc.Table(
                                     # table_header + table_body,
                                     # class_name="table table-bordered border-danger",
                                     # bordered=True,
                                     # responsive=True,

                                    dcc.Graph(id='mi_ge_pie',figure={}),
                                 # ),
                                 # style=TABLE_STYLE,
                             ),
                             dbc.Col(
                                    dcc.Graph(id='mi_sex_barchart',figure={})
                             )
                         ]
                     ),
                 ]
             ),
         ]
     ),
     ]
)

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
#---------------------------DROPDOWN CALLBACKS--------------------------

@callback(Output("dropdown_slct_barrios", "children"), Input("stored-sisben", "data"))
def populate_dropdownvalues(data):
    
    return (
          dcc.Dropdown(id="slct_group",
                     options=[{'label': str("Grupo: " + b), 'value': b} for b in
                              sorted(df_GrupoSisben['Grupo'].unique())],
                     multi=False,
                     value='A',
                     # style={'width': "40%"},
                     # searchable=True
                     ),
    )

# -------------------------------------CALLBACK FOR MAP-----------------------------------------------

#--------------------------------------------------
@callback(
    Output(component_id='mi_buc_map', component_property='figure'),
    Input(component_id='slct_barrios', component_property='value'),
    Input(component_id='slct_group', component_property='value')
)


def update_graph1(barrio_slctd,option_slctd):
    




    dff = df_GrupoSisben.copy()
    dff = dff[dff["Grupo"] == option_slctd]
   
    if barrio_slctd == 0:
       
        dff = dff[dff["BARRIO_AT"] == "SI"]
       


# hacer el mapa (version1)
    fig = px.choropleth_mapbox(dff,geojson=bmanga, color="personas",
                      locations="NOM_BARRIO", featureidkey="properties.NOMBRE",
                      mapbox_style="carto-positron", range_color=[0, max(dff["personas"])],
                      center = {"lat": 7.12539, "lon": -73.1198},
                      zoom = 11.5,
                      opacity = 0.5
                      )

    fig.update_geos(fitbounds="locations",visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


# ------------------CALLBACK FOR PIECHART--------------------
@callback(
    Output(component_id='mi_ge_pie', component_property='figure'),
    Input(component_id='slct_barrios', component_property='value'),
    Input(component_id='slct_group', component_property='value')
)
def update_pie(tipo_barrios,grupo):
    dfge = df_GrupoEtario.copy()
    dfge = dfge[dfge["Grupo"] == grupo]

    if tipo_barrios == 0:

        dfge = dfge[dfge["BARRIO_AT"] == "SI"]
        

    fig = px.pie(dfge, values='personas', names='rango etario',
                       title='Personas por Rango Etario')
    return fig

# ------------------CALLBACK FOR BARCHART--------------------
@callback(
    Output(component_id='mi_sex_barchart', component_property='figure'),
    Input(component_id='slct_barrios', component_property='value'),
    Input(component_id='slct_group', component_property='value')
)
def update_pie(tipo_barrios,grupo):
    dfsx = df_Sexo.copy()
    dfsx = dfsx[dfsx["Grupo"] == grupo]

    if tipo_barrios == 0:
        
        dfsx = dfsx[dfsx["BARRIO_AT"] == "SI"]
        

    fig = px.histogram(dfsx, x="sexo_persona", y="personas",
                       barmode='group',
                       title='Personas por Sexo', text_auto=True)
    return fig