from html.entities import html5
import base64
import datetime
import io
import dash_table
from dash_labs.plugins import register_page
import dash
from dash import callback, html, dcc, Input, Output, MATCH, ALL
from wordcloud import WordCloud
import dash_bootstrap_components as dbc
import dash.dependencies as dd
from dash.dependencies import Input, Output, State
from io import BytesIO
import json
import base64
import polars as pl
import plotly.express as px

import json
import os


import base64
import os
from urllib.parse import quote as urlquote
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams


nltk.download("stopwords")
nltk.download("punkt")

stop_words = set(stopwords.words("spanish"))


def preprocess_text(text):
    words = nltk.word_tokenize(text.lower())
    filtered_words = [
        word.strip().lower()
        for word in words
        if word.isalnum()
        and word.strip().lower() not in stop_words
        and word.strip().lower() not in ["de", "para", "sobre", "etc"]
    ]
    return " ".join(filtered_words)


def extract_ngrams(text, n=4):
    preprocessed_text = preprocess_text(text)
    blob = nltk.Text(nltk.word_tokenize(preprocessed_text))
    return list(ngrams(blob, n))


# Instantiate dash app
register_page(__name__, path="/")


layout = html.Div(
    [
        html.Br(),
        # -----------------TITULO-------------------------
        html.H1(
            "Hablemos de Alimentación",
            style={"textAlign": "center", "color": "#2E7DA1"},
        ),
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Arrastra  ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        html.Div(id="output-div"),
        html.Div(id="output-datatable"),
    ]
)


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        alimentos = pl.read_excel(io.BytesIO(decoded)).drop(
            [
                "Hora de inicio",
                "Hora de finalización",
                "Correo electrónico",
                "Nombre",
                "Hora de la última modificación",
            ]
        )
        alimentos.columns = [i.lower().strip() for i in alimentos.columns]

    except Exception as e:
        return html.Div(["Error subiendo el archivo"])

    return html.Div(
        [
            html.P("Selecciona una pregunta"),
            dcc.Dropdown(
                id="axis-data",
                options=[
                    {
                        "label": "¿suele cocinar la mayoría de sus comidas o depende principalmente de comidas preparadas? ",
                        "value": "cocinar",
                    },
                    {
                        "label": "¿Con qué frecuencia desayunas, almuerzas y cenas durante la semana?",
                        "value": "habitos",
                    },
                    {
                        "label": "¿Cuántas porciones de hortalizas y frutas consumes al día, en promedio?",
                        "value": "frutas",
                    },
                    {
                        "label": "¿Con qué frecuencia consume alimentos provenientes de la comida callejera o puestos de comida cerca de la universidad/colegio?",
                        "value": "callejera",
                    },
                    {
                        "label": "¿Cuanto gastas diariamente en tu alimentación?",
                        "value": "gasto",
                    },
                    {
                        "label": "¿Has experimentado cambios en sus hábitos alimentarios desde que ingresaste a la universidad?",
                        "value": "cambios",
                    },
                    {
                        "label": "¿Qué obstáculos o desafíos enfrentas para lograr una alimentación más saludable? ",
                        "value": "obstaculos",
                    },
                    {
                        "label": "¿Consideras que dispones de tiempo suficiente durante su jornada diaria para alimentarte adecuadamente? ",
                        "value": "tiempo",
                    },
                    {
                        "label": "¿Consideras que la oferta de alimentos disponibles en la universidad y sus alrededores es suficiente y adecuada para satisfacer sus necesidades alimentarias? ",
                        "value": "oferta",
                    },
                    {
                        "label": "¿Qué barreras o dificultades encuentra para mantener una alimentación saludable en el entorno universitario?  ",
                        "value": "barreras",
                    },
                    {
                        "label": "¿Has experimentado alguna experiencia negativa relacionada con la alimentación en la universidad? ",
                        "value": "negativa",
                    },
                ],
            ),
            html.Button(id="submit-button", children="Crear Gráfica"),
            html.Hr(),
            dcc.Store(id="stored-data", data=alimentos.to_dict(as_series=False)),
            html.Hr(),  # horizontal line
            # For debugging, display the raw contents provided by the web browser
        ]
    )


@callback(
    Output("output-datatable", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d)
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children


@callback(
    Output("output-div", "children"),
    Input("submit-button", "n_clicks"),
    State("stored-data", "data"),
    State("axis-data", "value"),
)
def make_graphs(n, data, axis_data):
    if n is None:
        return dash.no_update
    elif axis_data == "cocinar":
        fig = px.bar(
            data,
            x="usualmente, ¿suele cocinar la mayoría de sus comidas o depende principalmente de comidas preparadas? (ejemplos de comidas preparadas: alimentos congelados, comidas para llevar, platos precocinados...",
            y="id",
            title="Hábitos alimenticios Diarios",
            barmode="stack",
        )

        # Replace x-axis labels
        new_x_labels = {
            "A veces omito alguna de las comidas": "Omito alguna",
            "Usualmente, solo hago dos de las tres comidas": "Solo dos comidas",
            "No desayuno, almuerzo ni ceno regularmente.": "Es irregular",
            "Desayuno, almuerzo y ceno todos los días.": "Las tres comidas",
        }
        fig.update_xaxes(
            tickvals=list(new_x_labels.keys()),
            ticktext=list(new_x_labels.values()),
        )

        # Replace y-axis label
        new_y_label = "Total  estudiantes"
        fig.update_yaxes(title_text=new_y_label)

        # Update layout to hide tools and change background
        fig.update_layout(
            plot_bgcolor="white",  # Change background color to white
            showlegend=False,  # To show legend (set to False to hide)
            xaxis_title="Frecuencia",  # X-axis label
            yaxis_title="Total estudiantes",  # Y-axis label
            hovermode="x",
            title_x=0.5,
            xaxis={"categoryorder": "total ascending"},
        )

        # Hide the Plotly Express tools
        fig.update_xaxes(showgrid=False, showticklabels=True)
        fig.update_yaxes(showgrid=True, showticklabels=True)

        # print(data)
        return dcc.Graph(figure=fig)
    elif axis_data == "habitos":
        fig = px.bar(
            data,
            x="¿con qué frecuencia desayunas, almuerzas y cenas durante la semana?",
            y="id",
            title="Hábitos alimenticios Diarios",
            barmode="stack",
        )

        # Replace x-axis labels
        new_x_labels = {
            "A veces omito alguna de las comidas principales.": "Omito alguna",
            "Usualmente, solo hago dos de las tres comidas": "Solo dos comidas",
            "No desayuno, almuerzo ni ceno regularmente.": "Es irregular",
            "Desayuno, almuerzo y ceno todos los días.": "Las tres comidas",
        }
        fig.update_xaxes(
            tickvals=list(new_x_labels.keys()),
            ticktext=list(new_x_labels.values()),
            title_text="Day of the Week",
        )

        # Replace y-axis label
        new_y_label = "Total  estudiantes"
        fig.update_yaxes(title_text=new_y_label)

        # Update layout to hide tools and change background
        fig.update_layout(
            plot_bgcolor="white",  # Change background color to white
            showlegend=False,  # To show legend (set to False to hide)
            xaxis_title="Frecuencia",  # X-axis label
            yaxis_title="Total estudiantes",  # Y-axis label
            hovermode="x",
            title_x=0.5,
            xaxis={"categoryorder": "total ascending"},
        )

        # Hide the Plotly Express tools
        fig.update_xaxes(showgrid=False, showticklabels=True)
        fig.update_yaxes(showgrid=True, showticklabels=True)
        return dcc.Graph(figure=fig)
    elif axis_data == "frutas":
        data = pl.from_dict(data)
        fruits_frequency_dict = {
            "Ninguna al día": 0,
            "Menos de una porción al día (por ejemplo: medio plátano, un puñado de uvas)": 0.5,
            "Una porción al día (por ejemplo: una manzana, una zanahoria)": 1,
            "Dos o más porciones al día (por ejemplo: una ensalada mixta con lechuga, tomate y pepino, una taza de fresas y una porción de brócoli": 2,
        }
        data = data.with_columns(
            pl.col(
                "¿cuántas porciones de hortalizas y frutas consumes al día, en promedio?"
            ).map_dict(fruits_frequency_dict)
        )
        data = data.to_dict(as_series=False)
        fig = px.histogram(
            data,
            nbins=4,
            x="¿cuántas porciones de hortalizas y frutas consumes al día, en promedio?",
            title="Frutas y verduiras por día",
        )

        # Update trace to set bar color to red
        fig.update_traces(
            marker_color="red", marker_line_color="white", marker_line_width=1
        )

        # Update layout
        fig.update_layout(
            bargap=0,
            plot_bgcolor="white",  # Change background color to white
            showlegend=False,  # To show legend (set to False to hide)
            xaxis_title="Veces promedio al día",  # Y-axis label
            hovermode="x",
            title_x=0.5,
        )

        # Hide the Plotly Express tools
        fig.update_xaxes(showgrid=False, showticklabels=False)
        fig.update_yaxes(showgrid=False, showticklabels=False)
        return dcc.Graph(figure=fig)

    elif axis_data == "callejera":
        data = pl.from_dict(data)
        callejera_frequency_dict = {
            "Menos de una vez a la semana": 0.5,
            "Una vez a la semana.": 1.0,
            "Dos o más veces a la semana.": 2,
            "No consumo comida callejera o de puestos de comida": 0.0,
            "Todos los días": 3,
        }
        data = data.with_columns(
            pl.col(
                "¿con qué frecuencia consume alimentos provenientes de la comida callejera o puestos de comida cerca de la universidad/colegio?"
            ).map_dict(callejera_frequency_dict)
        )
        data = data.to_dict(as_series=False)
        fig = px.histogram(
            data,
            nbins=5,
            x="¿con qué frecuencia consume alimentos provenientes de la comida callejera o puestos de comida cerca de la universidad/colegio?",
            title="Consumo comida Callejera",
        )

        # Update trace to set bar color to red
        fig.update_traces(
            marker_color="yellow", marker_line_color="white", marker_line_width=1
        )

        # Update layout
        fig.update_layout(
            bargap=0,
            plot_bgcolor="white",  # Change background color to white
            showlegend=False,  # To show legend (set to False to hide)
            xaxis_title="Veces promedio la semana",  # Y-axis label
            hovermode="x",
            title_x=0.5,
        )

        # Hide the Plotly Express tools
        fig.update_xaxes(showgrid=False, showticklabels=False)
        fig.update_yaxes(showgrid=False, showticklabels=False)
        return dcc.Graph(figure=fig)

    elif axis_data == "gasto":
        data = pl.from_dict(data)
        expenses_frequency_dict = {
            "Entre 0 y 10.000 pesos": 10_000,
            "Entre 10.00 y 20.000 pesos ": 20_000,
            "Entre 20.000 y 50.000 pesos": 50_000,
            "Más de 50.000 pesos ": 60_00,
            "Todos los días": 3,
        }
        data = data.with_columns(
            pl.col("cuanto gastas diariamente en tu alimentación?").map_dict(
                expenses_frequency_dict
            )
        )
        data = data.to_dict(as_series=False)
        fig = px.histogram(
            data,
            nbins=5,
            x="cuanto gastas diariamente en tu alimentación?",
            title="Consumo comida Callejera",
        )

        # Update trace to set bar color to red
        fig.update_traces(
            marker_color="purple", marker_line_color="white", marker_line_width=1
        )

        # Update layout
        fig.update_layout(
            bargap=0,
            plot_bgcolor="white",  # Change background color to white
            showlegend=False,  # To show legend (set to False to hide)
            xaxis_title="Dinero Gastado",  # Y-axis label
            hovermode="x",
            title_x=0.5,
        )

        # Hide the Plotly Express tools
        fig.update_xaxes(showgrid=False, showticklabels=False)
        fig.update_yaxes(showgrid=False, showticklabels=False)
        return dcc.Graph(figure=fig)
    elif axis_data == "cambios":
        data = pl.from_dict(data)
        changes_frequency_dict = {
            "Sí, he experimentado cambios significativos.": "Sí",
            "Sí, pero los cambios han sido mínimos.": "Sí",
            "No, mis hábitos alimentarios se mantienen prácticamente iguales": "No",
            "No estoy seguro/a.": "No",
        }
        data = data.with_columns(
            pl.col(
                "¿has experimentado cambios en sus hábitos alimentarios desde que ingresaste a la universidad?"
            ).map_dict(changes_frequency_dict)
        )
        data = data.to_dict(as_series=False)
        fig = px.bar(
            data,
            x="¿has experimentado cambios en sus hábitos alimentarios desde que ingresaste a la universidad?",
            y="id",
            title="¿Han Cambiado tus Hábitos Alimenticios?",
            barmode="stack",
        )

        # Replace y-axis label
        new_y_label = "Total  estudiantes"
        fig.update_yaxes(title_text=new_y_label)

        # Update layout to hide tools and change background
        fig.update_layout(
            plot_bgcolor="white",  # Change background color to white
            showlegend=False,  # To show legend (set to False to hide)
            xaxis_title="Frecuencia",  # X-axis label
            yaxis_title="Total estudiantes",  # Y-axis label
            hovermode="x",
            title_x=0.5,
            xaxis={"categoryorder": "total ascending"},
        )

        # Hide the Plotly Express tools
        fig.update_xaxes(showgrid=False, showticklabels=True)
        fig.update_yaxes(showgrid=True, showticklabels=True)
        return dcc.Graph(figure=fig)

    elif axis_data == "obstaculos":
        data = pl.from_dict(data)
        data = data.with_columns(
            pl.col(
                "¿qué obstáculos o desafíos enfrentas para lograr una alimentación más saludable? marca todas las que consideres."
            ).apply(preprocess_text)
        )
        text = " ".join(
            data[
                "¿qué obstáculos o desafíos enfrentas para lograr una alimentación más saludable? marca todas las que consideres."
            ].drop_nulls()
        )

        # Create a WordCloud object
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
            text
        )
        fig = px.imshow(wordcloud.to_array(), template="plotly_white")
        fig.update_layout(
            title="Principales desafios para una alimentación saludable",
            xaxis=dict(showline=False, showticklabels=False, showgrid=False),
            yaxis=dict(showline=False, showticklabels=False, showgrid=False),
            title_x=0.5,
        )
        return dcc.Graph(figure=fig)
    elif axis_data == "tiempo":
        data = pl.from_dict(data)

        time_frequency_dict = {
            "Sí, tengo tiempo suficiente para planificar y preparar mis comidas.": "Sí",
            "A veces, depende de mí carga de trabajo y horarios.": "A veces",
            "No, suelo tener poco tiempo y termino comiendo rápidamente o saltándome comidas": "No",
        }
        data = data.with_columns(
            pl.col(
                "¿consideras que dispones de tiempo suficiente durante su jornada diaria para alimentarte adecuadamente?"
            ).map_dict(time_frequency_dict)
        )
        data = data.to_dict(as_series=False)
        fig = px.bar(
            data,
            x="¿consideras que dispones de tiempo suficiente durante su jornada diaria para alimentarte adecuadamente?",
            y="id",
            title="¿Tienes tiempo para alimentarte?",
            barmode="stack",
        )

        # Replace y-axis label
        new_y_label = "Total  estudiantes"
        fig.update_yaxes(title_text=new_y_label)

        # Update layout to hide tools and change background
        fig.update_layout(
            plot_bgcolor="white",  # Change background color to white
            showlegend=False,  # To show legend (set to False to hide)
            xaxis_title="Frecuencia",  # X-axis label
            yaxis_title="Total estudiantes",  # Y-axis label
            hovermode="x",
            title_x=0.5,
            xaxis={"categoryorder": "total ascending"},
        )

        # Hide the Plotly Express tools
        fig.update_xaxes(showgrid=False, showticklabels=True)
        fig.update_yaxes(showgrid=True, showticklabels=True)
        return dcc.Graph(figure=fig)

        # Show the updated plot
    elif axis_data == "oferta":
        data = pl.from_dict(data)
        data = data.with_columns(
            pl.col(
                "¿consideras que la oferta de alimentos disponibles en la universidad y sus alrededores es suficiente y adecuada para satisfacer sus necesidades alimentarias?"
            ).apply(preprocess_text)
        )
        text = " ".join(
            data[
                "¿consideras que la oferta de alimentos disponibles en la universidad y sus alrededores es suficiente y adecuada para satisfacer sus necesidades alimentarias?"
            ].drop_nulls()
        )

        # Create a WordCloud object
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
            text
        )
        fig = px.imshow(wordcloud.to_array(), template="plotly_white")
        fig.update_layout(
            title="Oferta de Alimentos en la universidad",
            xaxis=dict(showline=False, showticklabels=False, showgrid=False),
            yaxis=dict(showline=False, showticklabels=False, showgrid=False),
            title_x=0.5,
        )
        return dcc.Graph(figure=fig)
    elif axis_data == "barreras":
        data = pl.from_dict(data)
        data = data.with_columns(
            pl.col(
                "¿qué barreras o dificultades encuentra para mantener una alimentación saludable en el entorno universitario? marca todas las que consideres"
            ).apply(preprocess_text)
        )
        text = " ".join(
            data[
                "¿qué barreras o dificultades encuentra para mantener una alimentación saludable en el entorno universitario? marca todas las que consideres"
            ].drop_nulls()
        )

        # Create a WordCloud object
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
            text
        )
        fig = px.imshow(wordcloud.to_array(), template="plotly_white")
        fig.update_layout(
            title="Dificultades para alimentarse saludablemente",
            xaxis=dict(showline=False, showticklabels=False, showgrid=False),
            yaxis=dict(showline=False, showticklabels=False, showgrid=False),
            title_x=0.5,
        )
        return dcc.Graph(figure=fig)
    elif axis_data == "negativa":
        data = pl.from_dict(data)
        string_column = "¿has experimentado alguna experiencia negativa relacionada con la alimentación en la universidad? marca todas las que consideres"
        default_responses = [
            "Sí, la falta de opciones adecuadas para dietas especiales.;",
            "Sí, la dificultad para encontrar opciones saludables.;",
            "Si, la calidad de la comida preparada no es buena;",
            "Si, los espacios físicos no son suficientes y tengo que esperar mucho/hacer fila.;",
            "No, no he tenido experiencias negativas relacionadas con la alimentación en la universidad.;",
        ]
        data = data.with_columns(
            pl.when(pl.col(string_column).is_in(default_responses))
            .then(pl.col(string_column))
            .otherwise("Varios")
            .keep_name()
        ).fill_null("Multiples Problemas")
        data = data.to_dict(as_series=False)
        fig = px.bar(
            data,
            x="¿has experimentado alguna experiencia negativa relacionada con la alimentación en la universidad? marca todas las que consideres",
            y="id",
            title="¿Has experimentado problemas con la Universidad?",
            barmode="stack",
        )
        fig.update_traces(marker_color="green")

        # Replace x-axis labels
        new_x_labels = {
            "Sí, la falta de opciones adecuadas para dietas especiales.;": "Falta de dietas especiales",
            "Sí, la dificultad para encontrar opciones saludables.;": "No hay opciones saludables",
            "Si, la calidad de la comida preparada no es buena;": "Mala Calidad",
            "Si, los espacios físicos no son suficientes y tengo que esperar mucho/hacer fila.;": "Mucha Fila",
            "No, no he tenido experiencias negativas relacionadas con la alimentación en la universidad.;": "No",
            "Varios": "Multiples Problemas",
        }
        fig.update_xaxes(
            tickvals=list(new_x_labels.keys()), ticktext=list(new_x_labels.values())
        )

        # Replace y-axis label
        new_y_label = "Total  estudiantes"
        fig.update_yaxes(title_text=new_y_label)

        # Update layout to hide tools and change background
        fig.update_layout(
            plot_bgcolor="white",  # Change background color to white
            showlegend=False,  # To show legend (set to False to hide)
            xaxis_title="Promedio de Consumo",  # X-axis label
            yaxis_title="Total estudiantes",  # Y-axis label
            hovermode="x",
            title_x=0.5,
            xaxis={"categoryorder": "total ascending"},
        )

        # Hide the Plotly Express tools
        fig.update_xaxes(showgrid=False, showticklabels=True)
        fig.update_yaxes(showgrid=True, showticklabels=True)
        return dcc.Graph(figure=fig)

    else:
        bar_fig = px.bar(data, x="Hora de inicio", y="ID")
        # print(data)
        return dcc.Graph(figure=bar_fig)
