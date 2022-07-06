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

df = delitos.groupby(["ano","barrios_hecho","conducta"]).size().to_frame("cantidad de delitos").reset_index().rename(columns={"barrios_hecho":'barrio'})
df1 = df.to_dict()

lista = sorted(df['conducta'].unique())
lista.insert(0,"TOTAL DELITOS")

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
        dcc.Dropdown(id="select_conducta",
                            options=[
                                    {'label':str(b),'value':b} for b in lista],
                            value="TOTAL DELITOS",
                            #value=[b for b in sorted(df['conducta'].unique())],
                            multi=False,
                            
                            
                            ),
        html.Br(),
    	
    	dcc.Slider(2010, 2021, 1,
               marks = {2010 : '2010',
                       2011 : '2011',
                       2012 : '2012',
                       2013 : '2013',
                       2014 : '2014',
                       2015 : '2015',
                       2016 : '2016',
                       2017 : '2017',
                       2018 : '2018',
                       2019 : '2019',
                       2020 : '2020',
                       2021 : '2021'
                       },
               value=2010,
               id='my_slider'
    ),

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

@callback(

    Output(component_id='my_buc_map', component_property='figure'),
    Input(component_id='my_slider', component_property='value'),
    Input(component_id='select_conducta', component_property='value')
)
def update_graph(year,conducta):   
    dff = df.copy()
    if conducta=="TOTAL DELITOS":
        dff = dff.groupby(["ano","barrio"]).sum().reset_index()
        dff = dff[(dff["ano"] == year)]
    else:
        dff = dff[(dff["ano"] == year) & (dff["conducta"] == conducta )]

    # Plotly Express
    fig =px.choropleth_mapbox(dff, geojson=bmanga, color= 'cantidad de delitos',
                    locations="barrio", featureidkey= "properties.NOMBRE",
                    mapbox_style="carto-positron",
    center={"lat": 7.12539, "lon": -73.1198},
    zoom=11.5,
    opacity=0.5)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return  fig
