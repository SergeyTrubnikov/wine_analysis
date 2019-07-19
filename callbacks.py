import base64
import io
from contextlib import closing

import dash_html_components as html
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

from app import app
from wine_df import *

plt.rcParams["figure.figsize"] = (8, 5)


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
        'pricerange': [price],
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
            xaxis={'type': 'log', 'title': 'Points', "autorange": True},
            yaxis={'title': 'Price', 'range': [20, 90], "autorange": True},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            showlegend=False,
            autosize=True,
            hovermode='closest'
        )
    }

@app.callback(
    Output('wine-result', 'children'),
    [Input("submit-button", "n_clicks")],
    [State('wine-color', 'value'),
     State('wine-price-range', 'value'),
     State('wine-country', 'value')
     ])
def update_words_cloud(n_clicks, color, price, country):
    try:
        country = country
        text = get_wc_df(winedata, country, color, price)

        wordcloud = WordCloud(stopwords=stopwords, background_color='white', width=800, height=600).generate(text)
        plt.figure(figsize=(12, 7))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        with closing(io.BytesIO()) as buf:
            plt.savefig(buf, format='png')
            buf.seek(0)
            encoded_image = base64.b64encode(buf.read())

        return html.Img(src='data:image/png;base64,%s' % encoded_image.decode(), style={"width": "100%"})

    except ValueError as error:
        print("Not enough words in wine description!\nDetails:  {}".format(error))
        return html.H3("Not enough words in wine description!\nDetails: {}".format(error))
