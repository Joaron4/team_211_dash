from dash import Dash, callback, html, dcc
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import matplotlib as mpl
import gunicorn                     #whilst your local machine's webserver doesn't need this, Heroku's linux webserver (i.e. dyno) does. I.e. This is your HTTP server
from whitenoise import WhiteNoise   #for serving static files on Heroku

# Instantiate dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Reference the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
server = app.server 

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku) 
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/') 

# Define Dash layout
def create_dash_layout(app):
    table_header = [
        html.Thead(html.Tr([html.Th("Principales problemáticas"), html.Th("Principales grupos poblacionales afectados")],style = {"text-align":"center","color":"#2E7DA1"}))
    ]
    row1 = html.Tr([html.Td(html.Img(src='https://lostripulantes5.files.wordpress.com/2021/07/wordcloud.png?w=750', width="100%",height='100%')), html.Td("")])

    row4 = html.Tr([html.Td("lo que sea"), html.Td("Astra")])

    table_body = [html.Tbody([row1,  row4])]

    #----------------------------------


    


    # Set browser tab title
    app.title = "Your app title" 
    
    navbar = dbc.Navbar(
        dbc.Container(
            [
                
                    
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Escudo_de_Bucaramanga.svg/1200px-Escudo_de_Bucaramanga.svg.png", height="30px")),
                            dbc.Col(dbc.NavbarBrand("Alcaldía de Bucaramanga", style = {"text-align":"left","text-color":"white", "margin":"0px"})),
                        ],
                        align="left",
                        
                    ),
                    
            
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
            ]
        ),
        color = "#2EA18C",
        style=NAVBAR_STYLE,
    )
    #------------SIDEBAR-------------------------------
    sidebar = html.Div(
        [
            html.H2("Team 211", className="border border-secondary",style = {"color":"#2E7DA1","padding":"5%","background-color": "white",'textAlign': 'center'}),
            html.P(
                "Seleccione uno o más filtros para personalizar su búsqueda", className="lead",style = {"color":"white","padding":"5%", "font-size":"1 vw"}
            ),
            html.Hr(style = {'width':'95%','margin': 'auto','background-color': 'black'}),
            html.Br(),
            dbc.Row([
                
                dbc.Col(dbc.Col(html.Img(src="https://cdn.iconscout.com/icon/free/png-256/team-200-517802.png", height="40 px",style ={'margin-left':'30%','margin-bottom':'20%','margin-top':'0px'}),width={"size": 3, "order": 5})),
                dbc.Col(html.P('Enfoque poblacional',style = {"padding":"0px","color":"black",'text-aling':'center', "margin-bottom ": "0", "margin-top ": "20%", "font-size":"0.6 vw"}),width={"size": 9, "order": 1}),
                
                
            ],align="center"),
            dbc.Nav(
                [
                    
                    dbc.Col(
                        dbc.Table([
                            dbc.NavLink("Mujeres", href="/", active="exact"),
                            dbc.NavLink("Niños, niñas y adolescentes", href="/page-1", active="exact"),
                            dbc.NavLink("Habitantes de calle"),
                            dbc.NavLink("Trabajadoras sexuales"),
                            
                            
                        ], 
                            bordered=True,
                            style = SIDEBAR_SQUARES),
                        
                    ),
                    
                ],
                vertical=True,
                pills=True,
                
            ),
            html.Hr(style = {'width':'95%','margin': 'auto','background-color': 'black'}),
            html.Br(),
            dbc.Row([
                
                dbc.Col(dbc.Col(html.Img(src="https://freesvg.org/img/1552598586.png", height="50px",style ={'margin-left':'20%','margin-bottom':'20%','margin-top':'0px'}),width={"size": 2, "order": 5})),
                dbc.Col(html.P('Problemática',style = {"padding":"0px","color":"black",'text-aling':'center', "margin-bottom ": "0", "margin-top ": "20%", "font-size":"0.6 vw"}),width={"size": 9, "order": 1}),
                
                
            ],align="center"),
            dbc.Nav(
                [
                    
                    dbc.Col(
                        dbc.Table([
                            dbc.NavLink("Acoso", href="/", active="exact"),
                            dbc.NavLink("Violación", href="/page-2", active="exact"),
                            dbc.NavLink("Abuso sexual"),
                            dbc.NavLink("Homicidios"),
                        ], 
                            bordered=True,
                            style = SIDEBAR_SQUARES),
                        
                    ),
                    
                ],
                vertical=True,
                pills=True,
                navbar_scroll = True,
                
            ),
            html.Br(),
            html.Br(),
        
        ],
        style=SIDEBAR_STYLE,
    
    )
    content =html.Div([
            
            ], style = CONTENT_STYLE)

    app.layout = html.Div([
        dbc.Row(dbc.Col(navbar)),
        dbc.Row(
        [
            
            dbc.Col(sidebar,width=2,align="left"), 
            dbc.Col([
                html.Br(),
                #-----------------TITULO-------------------------
                html.H1("Bucaramanga", style={'textAlign': 'center',"color":"#2E7DA1"}),
                #------------------TABLA-------------------------
                dbc.Row([
                    dbc.Col(content),
                    dbc.Col(dbc.Table(table_header+table_body, class_name= 'table table-bordered border-danger', bordered=True,responsive= True), style = TABLE_STYLE)
                ])
            ]),
        
        
        ])
        
    ])

    return app

# Construct the dash layout
create_dash_layout(app)

# Run flask app
if __name__ == "__main__": app.run_server(debug=False, host='0.0.0.0', port=8050)
