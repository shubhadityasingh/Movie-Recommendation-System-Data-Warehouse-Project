import pickle
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def fetch_posters(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=a8ceee02bc23cd72797db38f57aa42c1&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommendations(movies_list):
    # movies_list = ['Superman Returns', 'Spider-Man 3']
    tag = movies_df[movies_df['title'].isin(movies_list)].tags.str.cat(sep=' ')
    q = pd.DataFrame({"title": "shubh","tags":tag},index=[5000])
    df1 = pd.concat([movies_df, q])
    vectors = cv.fit_transform(df1['tags']).toarray()
    cv.get_feature_names_out()
    similarity = cosine_similarity(vectors)
    distances = similarity[-1]
    movies_output = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:(9+len(movies_list))]
    recommended_movies = []
    for i in movies_output:
        tmp = movies_df.iloc[i[0]]
        if tmp.title not in movies_list:
            path = fetch_posters(tmp.movie_id)
            recommended_movies.append({"title":tmp.title, "path": path})
    return recommended_movies



movies_dict = pickle.load(open('model/movie_dict.pkl', 'rb'))
movies_df = pd.DataFrame(movies_dict)
cv = CountVectorizer(max_features=5000, stop_words='english')