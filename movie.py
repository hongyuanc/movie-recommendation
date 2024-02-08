import numpy as np
import pandas as pd
import ast

credits = pd.read_csv('credits.csv')
movies = pd.read_csv('movies.csv')

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

movies = movies.merge(credits, on = 'title')
movies = movies [['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

movies.dropna(inplace=True)

def convert(x):
    list = []
    for y in ast.literal_eval(x):
        list.append(y['name'])
    return list

movies['genres'] = convert(movies['genres'])
movies['keywords'] = convert(movies['keywords'])

print(movies.isnull().sum())