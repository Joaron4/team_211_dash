from html.entities import html5
from dash import callback, html, dcc, Input, Output, MATCH, ALL
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
#----------------GEOJSON-------------------
bmanga = json.load(open("./data/barrios.geojson", "r", encoding="utf-8"))

problems = ['estudiante', 'fuerza publica', 'líder cívico', 'maestro', 'ninguna', 'otro', 'persona dedicada al cuidado del hogar', 'persona en situación de prostitución', 'persona que cuida a otros', 'reciclador', 'servidor publico', 'trabajadora domestica']
register_page(__name__, path="/")
#-----------------DATASETS-----------------
violencia = pd.read_csv("./data/violencia_clean.csv")
df = pd.DataFrame(
    violencia[["orden", "comuna", "barrio", "def_naturaleza", "nom_actividad"]][
        (violencia["municipio"] == "bucaramanga")
        & (violencia["barrio"] != "SIN INFORMACION")
    ]
)
df["barrio"] = df["barrio"].str.replace("UNIVERSIDAD", "LA UNIVERSIDAD")


df1 = df.to_dict()
table_header = [
    html.Thead(
        html.Tr(
            [
                html.Th(html.Div(id="problematica_text", children=[])),
                
            ],
            style={"text-align": "center", "color": "#2E7DA1"},
        )
    )
]
#--------DEFAULT FILTERED DATASET----------
violencia_default= df.groupby('barrio').count().reset_index().sort_values('orden',ascending=False)
# --------------DEFAULT MAP--------------------
def default_map():
    
    fig = px.choropleth_mapbox(
            violencia_default,
            geojson=bmanga,
            color="orden",
            locations="barrio",
            featureidkey="properties.NOMBRE",
            mapbox_style="carto-positron",
            center={"lat": 7.12539, "lon": -73.1198},  # 7.12539, -73.1198
            zoom=11.5,
            opacity=0.5,
            
        )
    return fig
# ------------------DEFAULT WORDCLOUD --------------------
def plot_wordcloud(data):
    d = data.values
    wc = WordCloud(background_color="white")
    wc.generate(" ".join(d))
    return wc.to_image()

# ------------------DEFAULT BARPLOT --------------------

def default_barplot():
    shorten = dict()
    for barrio in violencia_default["barrio"]:
        shorten[barrio] = barrio[0:22].lower().capitalize()
    violencia_barrios = violencia_default.replace(shorten)
    fig = px.bar(
        violencia_barrios[violencia_barrios['barrio']!='SIN INFORMACION' ].head(10).sort_values(by='orden').rename(columns={'orden':'ocurrencias'}),
        y='barrio',
        x= 'ocurrencias',
        orientation ='h',
    title = 'Ocurrencias de por barrio'
    )
    return fig   

#-------------------TABLE--------------------------
row1 = html.Tr(
    [html.Td(html.Img(id="image_wc", width='100%' , height=200))] #wordcloud
)

row4 = html.Tr(
    [html.Td([dcc.Graph(id="barplot_barrios", figure=default_barplot())]) ]#barplot
)

table_body = [html.Tbody([row1, row4])]

# ------------SIDEBAR-------------------------------
sidebar = create_sidebar("dropdown-container1", "dropdown-container2")
# ----------------------------------------------------------
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
    "width": "99%",
    "padding": "5%",
    "margin": "auto",
    "border": "5px black",
    "background-color": "WHITE",
    "flex-flow": "column",
    "display": "flex",
    "overflowY": "auto",
    "overflowX": "hidden",
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
blackbold = {"color": "black", "font-weight": "bold"}


# ---------------------MAPA-----------------------
content = html.Div(

    [dcc.Graph(id="my_buc_map", figure=default_map())],

    style=CONTENT_STYLE,
)


layout = html.Div(
    [
        dcc.Store(id="stored-data", data=df1),
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



# ---------MAP--------------------
@callback(

    Output(component_id="my_buc_map", component_property="figure"),
    Input(component_id="select_ind", component_property="value"),
    Input(component_id="select_nat", component_property="value"),
)
def update_graph(ind, nat):


    dff = df.copy()
    dff = dff = (
        pd.DataFrame(
            dff[(dff["nom_actividad"] == ind) & (dff["def_naturaleza"] == nat)]
            .groupby(["barrio"])
            .size()
        )
        .rename(columns={0: "count"})
        .reset_index()
    )
    # Plotly Express
    fig = px.choropleth_mapbox(
        dff,
        geojson=bmanga,
        color="count",
        locations="barrio",
        featureidkey="properties.NOMBRE",
        mapbox_style="carto-positron",
        center={"lat": 7.12539, "lon": -73.1198},  # 7.12539, -73.1198
        zoom=11.5,
        opacity=0.5,
        height = 400
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    if ind == 'Todos los enfoques' or nat == 'Todas las problemáticas':
        return default_map()
    else:
        return fig


# ---------BARPLOTS-----------------------
@callback(
    Output(component_id="barplot_barrios", component_property="figure"),
    Input(component_id="select_ind", component_property="value"),
    Input(component_id="select_nat", component_property="value"),
)
def update_graph(ind, nat):

    violencia_barrios = pd.DataFrame(
        violencia[
            (violencia["municipio"] == "bucaramanga")
            & (violencia["def_naturaleza"] == nat)
            & (violencia["nom_actividad"] == ind)
            & (violencia["barrio"] != "SIN INFORMACION")
        ]
        .groupby("barrio")
        .count()
        .reset_index()
        .sort_values("naturaleza", ascending=False),
    )
    shorten = dict()
    for barrio in violencia_barrios["barrio"]:
        shorten[barrio] = barrio[0:22].lower().capitalize()
    violencia_barrios = violencia_barrios.replace(shorten)

    # Plotly Express
    fig = px.bar(
        violencia_barrios.head(5)
        .sort_values(by="orden")
        .rename(columns={"orden": "ocurrencias"}),
        y="barrio",
        x="ocurrencias",
        orientation="h",
        title="Ocurrencias de " + str(nat) + " por barrio",
        labels={
            "ocurrencias": "Ocurrencias",
            "barrio": "Barrio",
        },
    )
    if nat == 'Todas las problemáticas'  or ind == 'Todos los enfoques':
        return default_barplot()
    else:
        return fig


# -------DROPDOWNS CALLBACKS-----------
@callback(Output("dropdown-container1", "children"), Input("stored-data", "data"))
def populate_dropdownvalues(data):
    dff = pd.DataFrame(data)
    lista =sorted(dff["nom_actividad"].unique())
    lista.insert(0,'Todos los enfoques')
    return (
        dcc.Dropdown(
            id="select_ind",
            options=[
                
                {"label": str(b).capitalize(), "value": b}
                for b in lista
                
            ],
            value=[b for b in sorted(dff["nom_actividad"].unique())],
            multi=False, 
        ),
    )


@callback(Output("dropdown-container2", "children"), Input("stored-data", "data"))
def populate_dropdownvalues(data):
    dff = pd.DataFrame(data)
    lista =sorted(dff["def_naturaleza"].unique())
    lista.insert(0,'Todas las problemáticas')
    return (
        dcc.Dropdown(
            id="select_nat",
            options=[
                {"label": str(b).capitalize(), "value": b}
                for b in lista
            ],
            value=[b for b in sorted(dff["def_naturaleza"].unique())],
            multi=False,
        ),
    )


# -------------WORDCLOUD CALLBACK-------------------
@callback(
    dd.Output("image_wc", "src"),
    [dd.Input(component_id="select_ind", component_property="value")],
)
def make_image(ind):
    if ind == 'Todos los enfoques':
        dff = df.copy()
        img = BytesIO()
        plot_wordcloud(dff["def_naturaleza"]).save(img, format="PNG")
        return "data:image/png;base64,{}".format(base64.b64encode(img.getvalue()).decode())
    elif ind not in problems:
        dff = df.copy()
        img = BytesIO()
        plot_wordcloud(dff["def_naturaleza"]).save(img, format="PNG")
        return "data:image/png;base64,{}".format(base64.b64encode(img.getvalue()).decode())
    else:
        dff = df.copy()
        dff = dff[(dff["nom_actividad"] == ind)]
        img = BytesIO()
        plot_wordcloud(dff["def_naturaleza"]).save(img, format="PNG")
        return "data:image/png;base64,{}".format(base64.b64encode(img.getvalue()).decode())


@callback(
    Output(component_id="problematica_text", component_property="children"),
    Input(component_id="select_ind", component_property="value"),
    Input(component_id="select_nat", component_property="value"),
)
def update_output_div(ind,nat):
    
    if ind not in problems:
        return html.H5('Principales problemáticas Bucaramanga')
    elif ind == 'Todos los enfoques':
        return html.H5('Principales problemáticas Bucaramanga')
    elif nat== 'Todas las problemáticas':
        return html.H5('Principales problemáticas Bucaramanga')
    else:
        return html.H5("Principales problemáticas que afectan al enfoque poblacional: " + str(ind))

