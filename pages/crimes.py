from dash import callback, html, dcc, Input, Output, MATCH, ALL
import dash_bootstrap_components as dbc

import json
import pandas as pd
from dash_labs.plugins import register_page
import plotly.express as px
import json
from sidebar import create_sidebar


register_page(__name__, path="/crimes")
# ---------preparing the dataset------------------------------
delitos = pd.read_csv("./data/delitos_clean.csv", encoding="utf-8")
delitos_group = (
    pd.DataFrame(delitos.groupby(["latitud", "longitud", "conducta"]).size())
    .rename(columns={0: "count"})
    .reset_index()
)
delitos1 = delitos_group.to_dict()
sidebar = create_sidebar("drop_container_crimes1", "drop_container_crimes2")
# ---------------------------LAYOUT-------------------------------
layout = html.Div(
    [
        dcc.Store(id="stored-data1", data=delitos1),
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, align="left"),
                dbc.Col(
                    dcc.Graph(id="scatter_buc"),
                ),
            ]
        ),
    ]
)
# --------------------------DROPDOWNS--------------------------


@callback(Output("drop_container_crimes1", "children"), Input("stored-data1", "data"))
def populate_dropdownvalues(data):
    dff = pd.DataFrame(data)
    return (
        dcc.Dropdown(
            id="crimes_labels",
            options=[
                {"label": str(b).lower().capitalize(), "value": b}
                for b in sorted(dff["conducta"][dff["conducta"].notnull()].unique())
            ],
            value=[
                b for b in sorted(dff["conducta"][dff["conducta"].notnull()].unique())
            ],
            multi=False,
        ),
    )


# -----------------------MAP-------------------------------------------
@callback(
    Output(component_id="scatter_buc", component_property="figure"),
    Input(component_id="crimes_labels", component_property="value"),
)
def update_graph(nat):
    print("------------------>", nat)

    df = delitos_group.copy()

    # Plotly Express

    fig = px.scatter_mapbox(
        df[df["conducta"] == nat],
        lat="latitud",
        lon="longitud",
        mapbox_style="carto-positron",
        center={"lat": 7.12539, "lon": -73.1198},  # 7.12539, -73.1198
        zoom=11.5,
        opacity=0.5,
        size="count",
        color="conducta",
        hover_name="conducta",
        hover_data=["count", "longitud", "latitud"],
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
