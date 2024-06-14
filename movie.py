# movie recommendation system

import tkinter as tk
from tkinter import Listbox
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer

class MovieRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Recommendation System")

        self.label = tk.Label(root, text="Enter Movie Name:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=10)

        self.button = tk.Button(root, text="Recommend", command=self.get_recommendations)
        self.button.pack(pady=10)

        self.listbox = Listbox(root, width=50, height=10)
        self.listbox.pack(pady=10)

        # Load and preprocess data
        self.new, self.similarity = self.load_and_preprocess_data()

        self.entry.bind('<Return>', self.get_recommendations)

    def load_and_preprocess_data(self):
        credits = pd.read_csv('credits.csv')
        movies = pd.read_csv('movies.csv')

        movies = movies.merge(credits, on='title')
        movies = movies[['movie_id', 'title', 'genres', 'keywords', 'cast', 'crew']]
        movies.dropna(inplace=True)

        def convert(x):
            return [i['name'] for i in ast.literal_eval(x)]

        def convert_cast(x):
            return [i['name'] for i in ast.literal_eval(x)[:3]]

        def director(x):
            return [i['name'] for i in ast.literal_eval(x) if i['job'] == 'Director']

        movies['genres'] = movies['genres'].apply(convert)
        movies['keywords'] = movies['keywords'].apply(convert)
        movies['cast'] = movies['cast'].apply(convert_cast)
        movies['crew'] = movies['crew'].apply(director)

        for col in ['genres', 'keywords', 'cast', 'crew']:
            movies[col] = movies[col].apply(lambda x: [i.replace(" ", "") for i in x])

        movies['key'] = movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
        new = movies[['movie_id', 'title', 'key', 'genres']].copy()
        new.loc[:,'key'] = new['key'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)
        new.loc[:,'key'] = new['key'].apply(lambda x: x.lower() if isinstance(x, str) else x)

        ps = PorterStemmer()
        def stem(x):
            return ' '.join([ps.stem(i) for i in x.split()])

        new.loc[:,'key'] = new['key'].apply(stem)

        cv = CountVectorizer(max_features=5000, stop_words='english')
        vectors = cv.fit_transform(new['key']).toarray()
        similarity = cosine_similarity(vectors)

        return new, similarity

    def recommend(self, movie):
        movie = movie.lower()
        index = self.new[self.new['title'].str.lower() == movie].index[0]
        distances = self.similarity[index]
        m_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        for i in m_list:
            title = self.new.iloc[i[0]].title
            genres = self.new.iloc[i[0]].genres[0]

            recommended_movies.append(title)

        return recommended_movies

    def get_recommendations(self, event=None):
        movie_name = self.entry.get()
        self.listbox.delete(0, tk.END)
        try:
            recommendations = self.recommend(movie_name)
            for movie in recommendations:
                self.listbox.insert(tk.END, movie)
        except IndexError:
            self.listbox.insert(tk.END, "Error, movie not found. Try another?")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieRecommenderApp(root)

    # starts the console in the middle of the screen
    window_width = 400
    window_height = 350
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2))

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    root.mainloop()