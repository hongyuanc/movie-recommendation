# movie_recommendation
# made by: Hong

#%%
import numpy as np
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

#%%
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
    """
    removes the {} in the datasheet
    """
    list = []
    for i in ast.literal_eval(x):
        list.append(i['name'])
    return list

def convert_cast(x):
    """
    finds and return the an actor
    """
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
    """
    looks for the director and returns the name
    """
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

# summing up important keys into a new column
movies['key'] = movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# creating a new DataFrame object
new = movies[['movie_id', 'title', 'key']]

# removes [] in key, and if the object is not iterable, we ignore it
new.loc[:, 'key'] = new['key'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)

# same application excepts turns everything into lowercase - easier
# for data processing
new.loc[:, 'key'] = new['key'].apply(lambda x: x.lower() if isinstance(x, str) else x)

#
# FILTERING DATA USING VECTORS AND MATRICIES
#

#%%
cv = CountVectorizer(max_features = 5000, stop_words = 'english')

new.loc[:, 'key'] = new['key'].fillna('')
vectors = cv.fit_transform(new['key']).toarray()

#%%
ps = PorterStemmer()

def stem(x):
    """
    turns a string into its original stem using PorterStemmer
    """
    list = []
    for i in x.split():
        list.append(ps.stem(i))
    return ' '.join(list)

new.loc[:, 'key'] = new['key'].apply(stem)

#%%
similarity = cosine_similarity(vectors)

#%%
print(new)
# %%
