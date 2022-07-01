from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import folium
import json
import pandas as pd
import branca
import geopandas

Dash.register_page(__name__, path="/")

violencia = pd.read_csv("./data/violencia_clean.csv", encoding="utf-8")

barrios = violencia[["barrio", "orden"]].groupby("barrio").count().reset_index()

# color scheme
min_occ, max_occ = barrios["orden"].quantile([0.01, 0.99]).apply(round, 2)

colormap = branca.colormap.LinearColormap(
    colors=["#FBE9E7", "#D9CA11", "#D9CA11", "darkred"], vmin=min_occ, vmax=max_occ
)
colormap.caption = "Total Casos de violencia intrafamiliar y de género"

barrios_bmanga = geopandas.read_file(
    "https://raw.githubusercontent.com/Joaron4/team211_datasets/main/Barrios-polygon.geojson",
    driver="GeoJSON",
)
barrios_bmanga_occ = barrios_bmanga.merge(
    barrios, how="left", left_on="NOMBRE", right_on="barrio"
)
barrios_bmanga_occ["orden"] = barrios_bmanga_occ["orden"].fillna(0).astype("int")

m = folium.Map(location=[7.12539, -73.1198], zoom_start=12.5, tiles="OpenStreetMap")
# def heat_dict(x): #to acces the key in the dict
#     x=json_file
#     for i in range(len(x['features'])):
#         dict_json = x['features'][i]
#     return dict_json
def mapa():
    # ----------------------COLORES MAPA-----------------------------
    # bmanga_color ={'fillColor': '#00000000', 'color': '#228B22', 'weight': 1.5}
    style_function = lambda x: {
        "fillColor": colormap(x["properties"]["orden"]),
        "color": "black",
        "weight": 2,
        "fillOpacity": 0.7,
        "color": "#228B22",
        "weight": 1.5,
    }

    # ----------BUCARAMANGA---------------------------------
    folium.GeoJson(
        json.loads(barrios_bmanga_occ.to_json()),
        style_function=style_function,
        name="Barrios Bucaramanga",
        tooltip=folium.GeoJsonTooltip(
            fields=["Comuna", "NOMBRE", "orden"],
            aliases=["Comuna", "Barrio:", "Casos"],
            localize=True,
        ),
    ).add_to(m)

    return m


table_header = [
    html.Thead(
        html.Tr(
            [
                html.Th("Principales problemáticas"),
                html.Th("Principales grupos poblacionales afectados"),
            ],
            style={"text-align": "center", "color": "#2E7DA1"},
        )
    )
]
row1 = html.Tr(
    [
        html.Td(
            html.Img(
                src="https://lostripulantes5.files.wordpress.com/2021/07/wordcloud.png?w=750",
                width="100%",
                height="100%",
            )
        ),
        html.Td(""),
    ]
)

bmanga = mapa()
bmanga.save("Bucaramanga.html")

row4 = html.Tr([html.Td("lo que sea"), html.Td("Astra")])

table_body = [html.Tbody([row1, row4])]

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
    "height": "100%",
    "width": "90%",
    "margin": "auto",
    "padding": "10%",
    "margin": "auto",
    "border": "5px black",
    "background-color": "WHITE",
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
                            dbc.NavLink("Mujeres", href="/", active="exact"),
                            dbc.NavLink(
                                "Niños, niñas y adolescentes",
                                href="/page-1",
                                active="exact",
                            ),
                            dbc.NavLink("Habitantes de calle"),
                            dbc.NavLink("Trabajadoras sexuales"),
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
                        [
                            dbc.NavLink("Acoso", href="/", active="exact"),
                            dbc.NavLink("Violación", href="/page-2", active="exact"),
                            dbc.NavLink("Abuso sexual"),
                            dbc.NavLink("Homicidios"),
                        ],
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
content = html.Div(
    [
        html.Iframe(
            id="map",
            srcDoc=open("Bucaramanga.html", "r").read(),
            width="600",
            height="600",
            className="embed-responsive-item",
        )
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
