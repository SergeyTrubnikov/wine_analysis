# -*- coding: utf-8 -*-

import io

from contextlib import closing

import base64

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from stop_words import ADD_STOPWORDS
import pandas as pd

from wordcloud import WordCloud, STOPWORDS

import matplotlib.pyplot as plt
import plotly.graph_objs as go

from datetime import datetime

import os

plt.rcParams["figure.figsize"] = (8, 5)

winedata = pd.read_csv('wine_final_translated.csv', index_col=0)
winedata = winedata.reset_index()
stopwords = set(STOPWORDS)
stopwords.update(ADD_STOPWORDS)


# Get dataframe for wordcloud
def get_wc_df(df, country, color, price):
    text = " ".join(text for text in df[(df.country == country)& (df.color == color)& (df.pricerange == price)].translated_description)
    return text


# Getting country list
def get_country_list(df):
    df = df.groupby("country", as_index=False).mean()
    countries = list(df["country"])
    options = [{"label": country, "value": country} for country in countries]
    return options

def get_wine_colors(df):
    df = winedata
    countries = list(df["country"])
    options = [{"label": country, "value": country} for country in countries]
    return options


# Filtering dataframe
def full_gen_df(df,filter_fields, groupby_fields):
    df_full=df[df.filter(list(filter_fields.keys())).isin(filter_fields).all(axis=1)].groupby(groupby_fields)[['points', 'price']].mean()
    return df_full.reset_index()

# Group by fields
group_by_fields = ["country", "variety"]

# Filter fields
filter_fields = {
    'color': ['red'],
    'pricerange':['Medium'],
    'rating': ['Excellent']
}

# Request the data

# Wine country
wine_country = list(winedata["country"].dropna().unique())

# Wine colors
wine_colors = list(winedata["color"].dropna().unique())

# Wine price ranges
wine_price_range = list(winedata["pricerange"].dropna().unique())

# Wine rating
wine_rating = list(winedata["rating"].dropna().unique())

# Wine points
min_points = int(winedata["points"].min())
max_points = int(winedata["points"].max())

# Wine prices
min_price = int(winedata["price"].min())
max_price = int(winedata["price"].max())

# --------------------------------------------------------------------------------------------

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ["https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"]
external_scripts = [
    {
        "src": "https://code.jquery.com/jquery-3.3.1.slim.min.js",
        "integrity": "sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
        "crossorigin": "anonymous"
    },

    {
        "src": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js",
        "integrity": "sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49",
        "crossorigin": "anonymous"
    },

    {
        "src": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js",
        "integrity": "sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy",
        "crossorigin": "anonymous"
    }
]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)

colors = {
    "background": "#111111",
    "text": "#7FDBFF"
}

app.layout = html.Div(className="container-fluid",  style={"backgroundColor": "#F8F9FA"}, children=[

    # Header
    html.Div(className="row", children=[
        html.Div(className="col-12", style={"height": "60", "backgroundColor": "#343a40", "color": "white"}, children=[
            html.H1("Wine Analysis", style={"textAlign": "center", "fontWeight": "bold"})
        ])
    ]),

    # First row
    html.Div(className="row", children=[
        html.Div(className="col-3", children=[
            html.H2("", style={"textAlign": "center"})
        ]),
        html.Div(className="col-9", children=[
            html.H2("Wine Graph", style={"textAlign": "center"})
        ]),
    ]),

    # Second row

    html.Div(className="row", children=[

        # Column 1 - Inputs
        html.Div(className="col-2", children=[

            html.Div(className="row", children=[
                html.Div(className="col-12", children=[
                    html.P("Choose wine criterions:")
                ])
            ]),

            html.Div(className="row", children=[
                html.Div(className="col-12", children=[
                    html.Label("Color", style={"textAlign": "left", "color": "#6c757d"}),
                    dcc.Dropdown(
                        id="wine-color",
                        options=[{"label": color.capitalize(), "value": color} for color in wine_colors],
                        value='red',
                        placeholder="Select wine color..."
                    )
                ])
            ]),

            html.Br(),

            html.Div(className="row", children=[
                html.Div(className="col-12", children=[
                    html.Label("Price", style={"textAlign": "left", "color": "#6c757d"}),
                    dcc.Dropdown(
                        id="wine-price-range",
                        options=[{"label": price, "value": price} for price in wine_price_range],
                        value='Expensive',
                        placeholder="Select wine price..."
                    )
                ])
            ]),

            html.Br(),

            html.Div(className="row", children=[
                html.Div(className="col-12", children=[
                    html.Label("Rating", style={"textAlign": "left", "color": "#6c757d"}),
                    dcc.Dropdown(
                        id="wine-rating",
                        options=[{"label": rating, "value": rating} for rating in wine_rating],
                        value='Excellent',
                        placeholder="Select wine rating...",
                    )
                ])
            ]),

            html.Br(),

            html.Div(className="row", children=[
                html.Div(className="col-12", children=[
                    html.Label("Country", style={"textAlign": "left", "color": "#6c757d"}),
                    dcc.Dropdown(
                        id="wine-country",
                        options=[{"label": country, "value": country} for country in wine_country],
                        value="US",
                        placeholder="Select country...",
                    )
                ])
            ]),

            html.Div(className="row", children=[
                html.Div(className="col-4", style={"textAlign": "center"}, children=[
                    html.Br(),
                    html.Button("Submit", id="submit-button", n_clicks=0, className="btn btn-success"),
                    html.Br(),
                ])
            ]),
        ]),

        # Column 2 - Outputs
        html.Div(className="col-10", style={"overflowY": "scroll", "height": 600}, children=[
            html.Div(className="row", children=[
                html.Div(className="col-12", children=[
                    html.Div(className="card", children=[
                        html.Div(className="card-body", style={"Align": "center"}, children=[
                                dcc.Graph(id='wine-graph', style={"width": "100%"})
                        ])
                    ])
                ])
            ]),
            html.Div(className="row", children=[
                html.Div(className="col-12", children=[
                    html.Div(className="card", children=[
                        html.Div(className="card-body", style={"textAlign": "center"}, children=[
                            html.Img(id="wine-result", style={"width": "100%"})
                        ])
                    ])
                ])
            ])
        ])
    ]),
])

@app.callback(
    Output('wine-graph', 'figure'),
    [Input("submit-button", "n_clicks")],
    [State('wine-color', 'value'),
     State('wine-price-range', 'value'),
     State('wine-rating', 'value')
     ])
def update_figure(n_clicks, color, price, rating):
    filter_fields = {
        'color': [color],
        'price_range': [price],
        'rating': [rating]
    }
    filtered_df = full_gen_df(winedata, filter_fields, group_by_fields)
    traces = []
    for i in filtered_df.country.unique():
        df_by_country = filtered_df[filtered_df['country'] == i]
        traces.append(go.Scatter(

            x=df_by_country['points'],
            y=df_by_country['price'],
            text=["Country: {}<br>Variety: {}".format(marker[0], marker[1]) for marker in df_by_country[['country', "variety"]].values.tolist()],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 10,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=""
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            width=860,
            height=500,
            xaxis={'type': 'log', 'title': 'Points'},
            yaxis={'title': 'Price', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            showlegend=False,
            autosize=True,
            hovermode='closest'
        )
    }

@app.callback(
    Output('wine-result', 'src'),
    [Input("submit-button", "n_clicks")],
    [State('wine-color', 'value'),
     State('wine-price-range', 'value'),
     State('wine-country', 'value')
     ])
def update_words_cloud(n_clicks, color, price, country):

        country = country
        text = get_wc_df(winedata, country, color, price)

        wordcloud = WordCloud(stopwords=stopwords, background_color='white', width=800, height=500).generate(text)
        plt.figure(figsize=(12, 7))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        with closing(io.BytesIO()) as buf:
            plt.savefig(buf, format='png')
            buf.seek(0)
            encoded_image = base64.b64encode(buf.read())

        return 'data:image/png;base64,%s' % encoded_image.decode()


if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_hot_reload=False)
