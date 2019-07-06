# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

from datetime import datetime

import os

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

    html.Button(id="submit_button", n_clicks=0, children="Submit"),

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
    [Input("submit_button", "n_clicks")],
    [State("wine_country", "value")]
    # State("wine_color", "value"),
    # State("wine_price", "value"),
    # State("wine_points", "value")]
)
def generate_words_cloud(n_clicks, value):
    if n_clicks > 0:
        winedata = pd.read_csv('wine_final_translated.csv', index_col=0)
        winedata = winedata.reset_index()
        result_folder = "./assets/"

        # removing old clouds
        files_to_remove = [os.path.join(result_folder, item) for item in os.listdir(result_folder)]
        for item in files_to_remove:
            os.remove(item)

        result_name = "result_{}.png".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
        stopwords = set(STOPWORDS)
        country = value
        text = " ".join(text for text in winedata[(winedata.country == country)].translated_description)
        wordcloud = WordCloud(stopwords=stopwords, background_color='white').generate(text)
        wordcloud.to_file("{}{}".format(result_folder, result_name))
        image = "/assets/{}".format(result_name)
        print("Clicks: {}".format(n_clicks))
        print("Country: {}".format(value))
        return image


if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_hot_reload=False)
