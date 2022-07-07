from dash import  callback, html, dcc, Input, Output, MATCH, ALL
from wordcloud import WordCloud
import dash_bootstrap_components as dbc
import dash.dependencies as dd
from io import BytesIO
import json
import base64
import pandas as pd
from dash_labs.plugins import register_page   
import plotly.express as px 
import json
from sidebar import create_sidebar



bmanga = json.load(open('./data/Comunas.geojson','r'))

register_page(__name__, path="/chc")

df = pd.read_csv('./data/chc_big.csv')

df1 = df.to_dict()

table_header = [
    html.Thead(html.Tr([html.Div(id='some_text',children=[]), html.Th("Principales grupos poblacionales afectados")],style = {"text-align":"center","color":"#2E7DA1"}))
]
row1 = html.Tr([html.Td(html.Img(id="wc_chc", width="100%",height='100%')), html.Td("")])

row4 = html.Tr([html.Td("lo que sea"), html.Td("Astra")])

table_body = [html.Tbody([row1,  row4])]

#---------SIDEBAR-----------------------

sidebar = create_sidebar('select_gender',"select_kind")


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

	html.Br(),
        
        dcc.Graph(id='my_chc_map',figure={}) ,
        
        
        
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
                                        	dcc.Graph(id='my_chc_barchart',figure={}),
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

#------------------WORDCLOUD CREATION--------------------
def plot_wordcloud(data):
    d = data.values 
    wc = WordCloud(background_color='white', width=1080, height=360)
    wc.generate(' '.join(d))
    return wc.to_image()
    
    
#------------------CALLBACKS FOR DROPDOWNS--------------------

@callback(Output('select_gender', "children"),
    Input("stored-data_mc", "data"))
def populate_dropdownvalues(data):
    dff = pd.DataFrame(data)
    return(
            dcc.Dropdown(id = 'select_gender',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'Masculino',
                         placeholder = 'Select Option',
                         options = [{'label': c, 'value': c}
                                    for c in df['GENERO'].unique()], className = 'dcc_compon'),
    )

@callback(Output('select_kind', "children"),
    Input("stored-data_mc", "data"))
def populate_dropdownvalues(data):
    dff = pd.DataFrame(data)
    return(
            dcc.Dropdown(id = 'select_kind',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'Razón por la cual vive en la calle',
                         placeholder = 'Select Option',
                         options = [{'label': c, 'value': c}
                                    for c in df['kind'].unique()], className = 'dcc_compon'),

        )



#------------------CALLBACK FOR MAP--------------------

@callback(
            Output('my_chc_map', 'figure'),
            Input('select_gender', 'value'),
            Input('select_kind', 'value'),
            Input('select_specific', 'value')
            )
def update_graph(genero, tipo, otro):

    dff = df.copy()
    dff = dff[(dff["GENERO"] == genero) & (dff["kind"] == tipo) & (dff["clave"] == otro)]

    fig = px.choropleth_mapbox(dff, geojson=bmanga, color= 'count',
                        locations="COMUNA", featureidkey= "properties.NOMBRE_COM",
                        mapbox_style="carto-positron",
        center={"lat": 7.12539, "lon": -73.1198},#7.12539, -73.1198
        zoom=11.5,
        opacity=0.5)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig
    

#------------------CALLBACK FOR BARCHART--------------------
@callback(
            Output('my_chc_barchart', 'figure'),
            Input('select_gender', 'value'),
            Input('select_kind', 'value')
            )
def update_bar_chart(gen, kin):
    
    dff = df.copy()
    mask = (dff["GENERO"] == gen) & (dff["kind"] == kin)
    fig = px.bar(df[mask], x="count", y='COMUNA', 
                 color="clave",  barmode = 'stack',
                 title= kin + '<br>' + 'Género ' +  gen + '<br>' + '2019')
    return fig

#------------------CALLBACK FOR WORDCLOUD--------------------
    
@callback(dd.Output('wc_chc', 'src'), 
	[dd.Input(component_id='select_kind', component_property='value'),
	dd.Input(component_id='select_gender', component_property='value')])
	
def make_image(ind, gend):
    dff = df.copy()
    imag = BytesIO()
    plot_wordcloud(dff[(dff["GENDER"] == gend) & (dff["kind"] == ind)]['clave']).save(imag, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(imag.getvalue()).decode())





#-------------------------------------------

    
#     html.P('Seleccione opción:', className = 'fix_label', style = {'color': 'black'}),
#             dcc.Dropdown(id = 'select_specific',
#                          multi = False,
#                          clearable = True,
#                          disabled = False,
#                          style = {'display': True},
#                          placeholder = 'Select Specific',
#                          options = [], className = 'dcc_compon'),

# @callback(Output('select_specific', 'options'),
#     Input('select_gender', 'value'),
#     Input('select_kind', 'value')
#     )
# def get_country_options(genero, kind):

#     dff = df[(df['GENERO'] == genero) & (df['kind'] == kind)]
#     return [{'label': i, 'value': i} for i in dff['clave'].unique()]