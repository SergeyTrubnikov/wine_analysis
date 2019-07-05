# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
import os
import base64

plt.rcParams["figure.figsize"] = (18, 10)

winedata = pd.read_csv('wine_final_translated.csv', index_col=0)
winedata = winedata.reset_index()
stopwords = set(STOPWORDS)


# Getting country list
def get_country_list(df):
    df = df.groupby("country", as_index=False).mean()
    countries = list(df["country"])
    options = [{"label": country, "value": country} for country in countries]
    return options


# Request the data


min_points = int(winedata["points"].min())
max_points = int(winedata["points"].max())

min_price = int(winedata["price"].min())
max_price = int(winedata["price"].max())

# --------------------------------------------------------------------------------------------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    "background": "#111111",
    "text": "#7FDBFF"
}

app.layout = html.Div([

    # Dropdown container
    html.Div([
        html.Div([
            html.Label('Country'),
            dcc.Dropdown(
                id="wine_country",
                options=get_country_list(winedata),
                value='US',
                placeholder="Select a country..."
            )], style={"fontColor": "lightgrey"}),
    ], style={"width": "20%"}),

    # Checklist container
    html.Div([
        html.Div([
            html.Label('Wine color'),
            dcc.Checklist(
                id="wine_color",
                options=[
                    {'label': 'Red wine', 'value': 'RED'},
                    {'label': 'White wine', 'value': 'WHITE'},
                ],
                value=['RED', 'WHITE'],
            )]),
    ]),

    # Sliders container
    html.Div([
        html.Div([
            html.Label('Price'),
            dcc.Slider(
                id="wine_price",
                min=min_price,
                max=max_price,
                step=1,
                marks={
                    min_price: str(min_price),
                    max_price: str(max_price),
                },
                value=80,
            )]),
        html.Div(id="price_value"),

        html.Div([
            html.Label('Points'),
            dcc.Slider(
                id="wine_points",
                min=min_points,
                max=max_points,
                step=0.1,
                marks={
                    min_points: str(min_points),
                    max_points: str(max_points),
                },
                value=85,
            )]),
        html.Div(id="points_value")
    ], style={"width": "48%"}),

    html.Div([
        html.Img(id="wine_result")
    ])
])


@app.callback(
    Output(component_id="points_value", component_property="children"),
    [Input(component_id="wine_points", component_property="value")]
)
def update_points(input_value):
    return "You choice: {}".format(input_value)


@app.callback(
    Output(component_id="price_value", component_property="children"),
    [Input(component_id="wine_price", component_property="value")]
)
def update_price(input_value):
    return "You choice: {}".format(input_value)


@app.callback(
    Output("wine_result", "src"),
    [Input("wine_country", "value"),
     Input("wine_color", "value"),
     Input("wine_price", "value"),
     Input("wine_points", "value")]
)
def generate_words_cloud(wine_country, wine_color, wine_price, wine_points):
    winedata = pd.read_csv('wine_final_translated.csv', index_col=0)
    winedata = winedata.reset_index()
    stopwords = set(STOPWORDS)
    result = "./assets/result.png"
    result_name = "result.png"
    image_directory = os.getcwd() + result_name
    stopwords = set(STOPWORDS)
    country = wine_country
    color = wine_color
    price = wine_price
    points = wine_points
    # text = " ".join(text for text in winedata[(winedata.country==country)&(winedata.color==color)&(winedata.price==int(price))&(winedata.points==int(points))].translated_description)
    text = " ".join(text for text in winedata[(winedata.country == country)].translated_description)
    wordcloud = WordCloud(stopwords=stopwords).generate(text)
    wordcloud.to_file(result)
    image = "/assets/{}".format(result_name)
    return image


if __name__ == "__main__":
    app.run_server(debug=True)

