from dash import Dash, callback, html, dcc

import dash_bootstrap_components as dbc
from matplotlib.pyplot import title

# ------------SIDEBAR-------------------------------
def create_sidebar(id1, id2=None, id3=None):
    """Creates a sidebar
    arg1(id1): the callback dropdown id
    arg1(id2): the callback dropdown id
    return sidebar"""

    title_second_id= html.Div()
    second_id = html.Div()

    if id2 != None:
        
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
            html.P(
                "Seleccione uno o más filtros para personalizar su búsqueda",
                className="lead",
                style={"color": "white", "padding": "5%", "font-size": "1 vw"},
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
                        dbc.NavLink("crimenes", active=True, href="/crimes")
                    ),
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
            html.P("Enfoque poblacional", className="problematica"),
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


#-----------------SIDEBARPARACRIMES------------------

def create_sidebar_crimes(id1, id2, id3):
    """Creates a sidebar
    arg1(id1): the callback dropdown id
    arg1(id2): the callback dropdown id
    return sidebar"""

    title_second_id= html.Div()
    second_id = html.Div()

    tittle_third_id = html.Div()
    third_id = html.Div()

    if id2 != None:
        
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
    
    if id3 != None:
        
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
            html.P(
                "Seleccione uno o más filtros para personalizar su búsqueda",
                className="lead",
                style={"color": "white", "padding": "5%", "font-size": "1 vw"},
            ),
            html.Hr(
                style={"width": "95%", "margin": "auto", "background-color": "black"}
            ),
            html.Br(),
            dbc.DropdownMenu(
                [
                    dbc.DropdownMenuItem(
                        dbc.NavLink("Violencia de género", active=True, href="/")
                    ),
                    dbc.DropdownMenuItem(
                        dbc.NavLink("crimenes", active=True, href="/crimes")
                    ),
                    dbc.DropdownMenuItem(dbc.NavLink("Comportamientos contrarios a la convivencia", active=True, href="/comportamientos")),
                    dbc.DropdownMenuItem(dbc.NavLink("Habitantes de calle", active=True, href="/chc"))

                ],
                label="Problemas",
                nav=True,
                className="dropdown-item btn btn-danger",
            ),
            html.Hr(
                style={"width": "95%", "margin": "auto", "background-color": "black"}
            ),
            html.Br(),
            dbc.Row(
                [
                    html.P("Por tipo de Delitos", className="problematica"),
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