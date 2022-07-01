from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import dash
import json
import pandas as pd
from dash_labs.plugins import register_page


register_page(__name__, path="/")



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
