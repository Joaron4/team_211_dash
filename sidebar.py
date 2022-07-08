from dash import Dash, callback, html, dcc

import dash_bootstrap_components as dbc
from matplotlib.pyplot import title

# ------------SIDEBAR-------------------------------
def create_sidebar(id1, id2=None, id3=None):
    """Creates a sidebar
    arg1(id1): the callback dropdown id
    arg1(id2): the callback dropdown id
    return sidebar"""
    first_title= html.Div()
    title_second_id= html.Div()
    second_id = html.Div()
    tittle_third_id = html.Div()
    third_id = html.Div()
    if id1 == 'select_conducta':
        first_title= html.P("Por tipo de Delitos", className="problematica")
    elif id1 == 'select_gender':
        first_title= html.P("Seleccione género: ", className="problematica")
    elif id1 == 'dropdown_slct_barrios':
        first_title= html.P("Filtro de barrios de Alerta Temprana", className="problematica")
    elif id1 == 'select_chapt1':
        first_title= html.P("Cantidad de infractores", className="problematica")

    else:
        first_title= html.P("Enfoque poblacional", className="problematica")
    if id2 != None:
        if id2 == 'select_edad':
            title_second_id= dbc.Row(
                    [
                        html.P(
                            "Por edad de la victima",
                            className="problematica",
                        ),
                    ],
                    align="center",
                )
            second_id = dbc.Nav(
                    [
                        dbc.Col(
                            dbc.Table(html.Div(id=id2, children=[])),
                        ),
                    ],
                    vertical=True,
                    pills=True,
                    navbar_scroll=True,
                )
        elif id2 == 'select_kind':
            title_second_id= dbc.Row(
                    [
                        html.P(
                            "Seleccione aspecto: ",
                            className="problematica",
                        ),
                    ],
                    align="center",
                )
            second_id = dbc.Nav(
                    [
                        dbc.Col(
                            dbc.Table(html.Div(id=id2, children=[])),
                        ),
                    ],
                    vertical=True,
                    pills=True,
                    navbar_scroll=True,
                )
        elif id2 == 'dropdown_tempana':
            title_second_id = dbc.Row(
                    [
                        html.P(
                            "Grupos Resultado Encuesta SISBEN IV",
                            className="problematica",
                        ),
                    ],
                    align="center",
                )
            second_id =dcc.Dropdown(id="slct_barrios",
                     options=[
                         {"label": "Todos los barrios", "value": 1},
                         {"label": "Solo barrios de alerta temprana", "value": 0}],
                     multi=False,
                     value=1,
                     #style={'width': "90%","align-items":"center"},
                     searchable=True
                     )
        else:
            title_second_id= dbc.Row(
                    [
                        html.P(
                            "Problemática",
                            className="problematica",
                        ),
                    ],
                    align="center",
                )
            second_id = dbc.Nav(
                    [
                        dbc.Col(
                            dbc.Table(html.Div(id=id2, children=[])),
                        ),
                    ],
                    vertical=True,
                    pills=True,
                    navbar_scroll=True,
                )
    
    if id3 != None:
        if id3 == 'select_genero':
            tittle_third_id= dbc.Row(
                [
                    html.P(
                        "Por género de la victima",
                        className="problematica",
                    ),
                ],
                align="center",
                )
            third_id = dbc.Nav(
                [
                    dbc.Col(
                        dbc.Table(html.Div(id=id3, children=[])),
                    ),
                ],
                vertical=True,
                pills=True,
                navbar_scroll=True,
                )
        elif id3=="select_specific":
            tittle_third_id= dbc.Row(
                [
                    html.P(
                        "Selecciones Opción: ",
                        className="problematica",
                    ),
                ],
                align="center",
                )
            third_id = dbc.Nav(
                [
                    dbc.Col(
                        dbc.Table(html.Div(id=id3, children=[])),
                    ),
                ],
                vertical=True,
                pills=True,
                navbar_scroll=True,
                )


    return html.Div(
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
            html.Hr(
                style={"width": "95%", "margin": "auto", "background-color": "black"}
            ),
            html.H6(
                "Este dashboard permite vizualizar, mediante georreferenciaciones y gráficas algunas de la problemáticas planteadas en la alerta temprana N° 28 de 2021",
                className="lead",
                style={"color": "white", "padding": "5%", "font-size": "1 vw",'text-align': 'justify'},
            ),
            html.Hr(
                style={"width": "95%", "margin": "1%", "background-color": "black"}
            ),
            html.H6(
                "Para utilizarlo, primero seleccione uno de los cinco problemas identificados en la alerta temprana en 'problemas alerta temprana' y luego, usando los menus deplegables seleccione uno o más filtros para personalizar su búsqueda",
                className="lead",
                style={"color": "white", "padding": "5%", "font-size": "1 vw",'text-align': 'justify'},
            ),
            html.Hr(
                style={"width": "95%", "margin": "auto", "background-color": "black"}
            ),
            html.Br(),
            dbc.DropdownMenu(
                [
                    dbc.DropdownMenuItem(
                        dbc.NavLink("Violencia de género e intrafamiliar", active=True, href="/")
                    ),
                    dbc.DropdownMenuItem(
                        dbc.NavLink("Crimenes", active=True, href="/crimes")
                    ),
                    dbc.DropdownMenuItem(dbc.NavLink("SISBEN IV", active=True, href="/sisben")),
                    dbc.DropdownMenuItem(dbc.NavLink("Comportamientos contrarios a la convivencia", active=True, href="/comportamientos")),
                    dbc.DropdownMenuItem(dbc.NavLink("Habitantes de calle", active=True, href="/chc"))

                ],
                label="Problemas alerta temprana",
                nav=True,
                toggle_style={"color":"black","text-align":"center"}
                
            ),
            html.Br(),
            html.Hr(
                style={"width": "95%", "margin": "auto", "background-color": "black"}
            ),
            html.Br(),
            dbc.Row(
                [
                   first_title,
                ],
                align="center",
            ),
            dbc.Nav(
                [
                    dbc.Col(
                        dbc.Table(html.Div(id=id1, children=[])),
                    ),
                ],
                vertical=True,
                pills=True,
            ),
            html.Hr(
                style={"width": "95%", "margin": "auto", "background-color": "black"}
            ),
            html.Br(),
            title_second_id,
            second_id,
            tittle_third_id,
            third_id,
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
        ],
        id="SIDEBAR_STYLE",
    )


