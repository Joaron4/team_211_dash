from matplotlib.pyplot import figure
from dash import  callback, html, dcc, Input, Output, MATCH, ALL
import dash_bootstrap_components as dbc
import dash.dependencies as dd
from io import BytesIO
import base64
import json
import pandas as pd
from dash_labs.plugins import register_page
from sidebar import create_sidebar_crimes
import plotly.express as px 


bmanga = json.load(open('./data/barrios.geojson','r',encoding="utf-8"))
register_page(__name__, path="/crimes")

delitos = pd.read_csv('./data/delitos_final.csv')

df = delitos.groupby(["barrios_hecho","ano","conducta","genero","curso_de_vida"]).size().to_frame("cantidad de delitos").reset_index().rename(columns={"barrios_hecho":'barrio'})
df1 = df.to_dict()


lista_genero = ["FEMENINO","MASCULINO"]
lista_edad = ["01. Primera infancia","02. Infancia","03. Adolescencia","04. Jovenes","05. Adultez","06. Persona Mayor"]
lista_conducta = sorted(df['conducta'].unique())
lista_conducta.insert(0,"TOTAL DELITOS")

table_header = [
    html.Thead(html.Tr([html.Th("Principales problemáticas"), html.Th("Principales grupos poblacionales afectados")],style = {"text-align":"center","color":"#2E7DA1"}))
]

# row1 =  html.Tr([html.Td("lo que sea"), html.Td("Giovanny")])
# row4 = html.Tr([html.Td("lo que sea"), html.Td("Giovanny")])
# table_body = [html.Tbody([row1,  row4])]

#---------SIDEBAR-----------------------

sidebar = create_sidebar_crimes('select_conducta',"select_variable")


# -------------------------------------

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
    html.P('Seleccione el tipo de delito:', className = 'fix_label', style = {'color': 'black'}),    
        
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

        dcc.Graph(id='my_crime_map',figure={}) 
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
                                        dcc.Graph(id='the_graph', figure={})
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

#-------------CALLBACKS FOR SIDEBAR-------------------

@callback(Output("select_conducta", "children"), Input("stored-data_mc", "data"))
def populate_dropdownvalues(data):
    dff = pd.DataFrame(data)
    return (
        dcc.Dropdown(id="select_conducta",
                            multi=False,
                            clearable = True,
                            disabled = False,
                            style = {'display': True},
                            placeholder = 'Select Option',
                            value="TOTAL DELITOS",
                            options=[{'label':str(b),'value':b} for b in lista_conducta],
                            className = 'dcc_compon'
                            ),
    )


#--------------CALLBACKS FOR MAP---------------------

@callback(

    Output(component_id='my_crime_map', component_property='figure'),
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

#--------------CALLBACKS FOR BARCHART---------------------

@callback(

    Output(component_id='the_graph', component_property='figure'),
    Input(component_id='my_slider', component_property='value'),
    Input(component_id='select_conducta', component_property='value')
)

def update_barchart(year,conducta):   
    dgg = df.copy()
    if conducta=="TOTAL DELITOS":
        dgg = dgg.groupby(["ano","barrio"]).sum().reset_index()
        dgg = dgg[(dgg["ano"] == year)]
        dgg = dgg.sort_values(by="cantidad de delitos", ascending=False).head(5)

        # Plotly Express
        barchart=px.bar(
            data_frame=dgg,
            x=dgg["barrio"],
            y=dgg['cantidad de delitos'],
            title="Los cinco barrios con mayor casos de: "+conducta,
            color=dgg["barrio"],
            color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta"]
            )

    else:
        dgg = dgg[(dgg["ano"] == year) & (dgg["conducta"] == conducta )]
        dgg = dgg.sort_values(by="cantidad de delitos", ascending=False).head(5)
        # Plotly Express
        barchart=px.bar(
            data_frame=dgg,
            x=dgg["barrio"],
            y=dgg['cantidad de delitos'],
            title="Los cinco barrios con mayor casos de: "+conducta,
            color=dgg["barrio"],
            color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta"]
            )

    return (barchart)