import numpy as np
import pandas as pd
import ast

# opening the files
credits = pd.read_csv('credits.csv')
movies = pd.read_csv('movies.csv')

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

# merges two datasets on one title
movies = movies.merge(credits, on = 'title')

# selects important titles only for filtering recommendations
movies = movies [['movie_id', 'title', 'genres', 'keywords', 'cast', 'crew']]

# drops all empty vars
movies.dropna(inplace=True)

# functions that uses ast to evaluate and modify the contents of the spreadsheet
def convert(x):
    list = []
    for i in ast.literal_eval(x):
        list.append(i['name'])
    return list

def convert_cast(x):
    list = []
    count = 0
    for i in ast.literal_eval(x):
        if count != 3:
            list.append(i['name'])
            count += 1
        else:
            break
        return list
    
def director(x):
    list = []
    for i in ast.literal_eval(x):
        if i['job'] == 'Director':
            list.append(i['name'])
    return list        

def clear_spaces(x):
    """ 
    removes spaces in inputs
    """
    return x.apply(lambda cell:[i.replace(" ", "") for i in cell] \
                   if type(cell) == list else cell)

# applying the functions to clean the dataset
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert_cast)
movies['crew'] = movies['crew'].apply(director)

# iterating though movies to clear the spaces
for x, y in movies.items():
    movies[x] = clear_spaces(movies[x])

movies['key'] = movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new = movies[['movie_id', 'title', 'key']]

print(new)