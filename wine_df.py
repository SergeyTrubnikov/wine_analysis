import pandas as pd
from wordcloud import STOPWORDS, WordCloud

from stop_words import ADD_STOPWORDS

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
# filter_fields = {
#     'color': ['red'],
#     'pricerange':['Medium'],
#     'rating': ['Excellent']
# }

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
