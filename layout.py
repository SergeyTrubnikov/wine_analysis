import dash_core_components as dcc
import dash_html_components as html

from wine_df import *

layout = html.Div(className="container-fluid",  style={"backgroundColor": "#F8F9FA"}, children=[

    # Header
    html.Div(className="row", children=[
        html.Div(className="col-12", style={"height": "60", "backgroundColor": "#343a40", "color": "white"}, children=[
            html.H1("Wine Analysis", style={"textAlign": "center", "fontWeight": "bold"}, className="font-italic")
        ])
    ]),

    # Body

    html.Div(className="row", children=[

        # Column 1 - Inputs
        html.Div(className="col-2", children=[

            html.Div(className="row", children=[
                html.Div(className="col-12", children=[
                    html.P(),
                    html.H6("Choose wine criterions:"),
                ])
            ]),

            html.Div(className="row", children=[
                html.Div(className="col-12", children=[
                    html.Label("Color", style={"textAlign": "left", "color": "#6c757d"}),
                    dcc.Dropdown(
                        id="wine-color",
                        options=[{"label": color.capitalize(), "value": color} for color in wine_colors],
                        value='red',
                        placeholder="Select wine color...",
                        clearable=False,
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
                        placeholder="Select wine price...",
                        clearable=False
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
                        clearable=False
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
                        clearable=False
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
                            html.Div(id="wine-result")
                        ])
                    ])
                ])
            ])
        ])
    ]),
])
