from dash import  callback, html, dcc, Input, Output, MATCH, ALL
import dash_bootstrap_components as dbc

import json
import pandas as pd
from dash_labs.plugins import register_page   
import plotly.express as px 
import json
from sidebar import create_sidebar
from data.definitions import default_definition, definition2
bmanga = json.load(open('./data/barrios.geojson','r',encoding='utf-8'))

register_page(__name__, path="/comportamientos")


violencia = pd.read_csv('./data/mc_clean.csv')
df = pd.DataFrame(violencia[['LOCALIDAD','BARRIO_HECHOS','AÑO_NUM','CAPT']].groupby(['LOCALIDAD','BARRIO_HECHOS','AÑO_NUM','CAPT']).size()).rename(columns={0:'count'}).reset_index()
df1 = df.to_dict()
table_header = [
    html.Thead(html.Tr([html.Th("Principales problemáticas"), html.Th("Principales grupos poblacionales afectados")],style = {"text-align":"center","color":"#2E7DA1"}))
]
row1 = html.Tr([html.Td(dcc.Graph(id="line_plot"),)])

row4 = html.Tr([html.Td(html.P(default_definition),id="description_text_comportamientos",style={ 'text-align': 'justify'})])

table_body = [html.Tbody([row1,  row4])]

# ----------SIDEBAR------------------------
sidebar = create_sidebar('select_chapt1')

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



#---------------------MAPA-----------------------
content = html.Div(
    [
    	
        html.Br(),
    	
    	dcc.Slider(2017, 2021, 1,
               marks = {2017 : '2017',
                       2018 : '2018',
                       2019 : '2019',
                       2020 : '2020',
                       2021 : '2021'
                       },
               value=2017,
               id='my_slider'
    ),
    
    html.Br(),
        
        dcc.Graph(id='my_map_mc',figure={}) 
    ],
    style=CONTENT_STYLE,
)
 

layout = html.Div(
    [   dcc.Store(id="stored-data_mc", data=df1),
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, align="left"),
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
                                        table_body,
                                        responsive=True
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
@callback(Output("select_chapt1", "children"), Input("stored-data_mc", "data"))
def populate_dropdownvalues(data):
    dff = pd.DataFrame(data)
    return (
        dcc.Dropdown(id = 'select_chapt',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         placeholder = 'Select Option',
                         options = [{'label':str(b),'value':b} for b in sorted(df['CAPT'].unique())], 
                         className = 'dcc_compon'
                            
                            ),
    )

@callback(
    
    Output(component_id='my_map_mc', component_property='figure'),
    Input(component_id='my_slider', component_property='value'),
    Input(component_id='select_chapt', component_property='value')
)
def update_graph(year,chapt):

    dff = df.copy()
    dff = dff[(dff["AÑO_NUM"] == year) & (dff["CAPT"] == chapt )]

    # Plotly Express
    fig =px.choropleth_mapbox(dff, geojson=bmanga, color= 'count',
                    locations="BARRIO_HECHOS", featureidkey= "properties.NOMBRE",
                    mapbox_style="carto-positron",
    center={"lat": 7.12539, "lon": -73.1198},#7.12539, -73.1198
    zoom=11.5,
    opacity=0.5)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return  fig
    
    
@callback(
    Output("line_plot", "figure"), 
    Input("select_chapt", "value"))
    
def update_line_chart(chapter):
    dff = df.copy()
    dff_sum = dff.groupby(['LOCALIDAD', 'AÑO_NUM','CAPT'], as_index=False)['count'].sum()
    fig = px.line(dff_sum[dff_sum["CAPT"] == chapter], 
        x="AÑO_NUM", y="count", color='LOCALIDAD',
        title = chapter) 
    return fig    

@callback(
    Output(component_id="description_text_comportamientos", component_property="children"),
    Input(component_id="select_chapt", component_property="value"),
    
)
def update_output_div(chapt):
    
    if chapt not in definition2:
        return html.P(default_definition)
    else:
        return html.P(str(definition2[chapt]))

    
    
    

