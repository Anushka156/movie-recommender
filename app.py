import streamlit as st
import pickle
import pandas as pd
import requests
import gzip
import os

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []

    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster((movie_id)))
    return recommended_movies, recommended_movies_posters





def fetch_poster(movie_id):
    try:
        url = f"https://api.tmdb.org/3/movie/{movie_id}?api_key=3095bd1a400bd451a57e18d466a5ee91&language=en-US"
        data = requests.get(url, timeout=5).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
    except Exception:
        pass
    return "https://via.placeholder.com/500x750?text=Poster+Not+Available"

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

if os.path.exists('similarity.pkl'):
    similarity = pickle.load(open('similarity.pkl', 'rb'))
elif os.path.exists('similarity.pkl.gz'):
    with gzip.open('similarity.pkl.gz', 'rb') as f:
        similarity = pickle.load(f)
else:
    st.error("Similarity matrix file not found!")
    st.stop()

# Netflix-inspired styling
st.markdown("""
<style>
/* Main app background with dark cinematic overlay */
.stApp {
    background: linear-gradient(rgba(0, 0, 0, 0.82), rgba(15, 15, 15, 0.94)),
                url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=1920&auto=format&fit=crop');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: #FFFFFF;
}

/* Header & Typography */
.netflix-title {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    color: #E50914;
    font-size: 3.2rem;
    font-weight: 900;
    letter-spacing: 2px;
    text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.8), 0 0 25px rgba(229, 9, 20, 0.4);
    margin-bottom: 0.2rem;
    text-transform: uppercase;
}

.netflix-subtitle {
    color: #CCCCCC;
    font-size: 1.1rem;
    margin-bottom: 1.8rem;
    font-weight: 400;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.8);
}

/* Label styling */
label[data-testid="stWidgetLabel"] p {
    color: #FFFFFF !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
}

/* Netflix Red Button */
div.stButton > button {
    background-color: #E50914 !important;
    color: #FFFFFF !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    padding: 0.6rem 2.2rem !important;
    border: none !important;
    border-radius: 4px !important;
    box-shadow: 0 4px 15px rgba(229, 9, 20, 0.4) !important;
    transition: all 0.3s ease-in-out !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

div.stButton > button:hover {
    background-color: #B80710 !important;
    box-shadow: 0 6px 25px rgba(229, 9, 20, 0.8) !important;
    transform: scale(1.03) !important;
}

/* Movie Poster Image styling with zoom effect */
div[data-testid="stImage"] img {
    border-radius: 8px !important;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.7) !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}

div[data-testid="stImage"] img:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 10px 25px rgba(229, 9, 20, 0.6) !important;
}

/* Card titles */
.movie-title {
    color: #FFFFFF;
    font-size: 1rem;
    font-weight: 600;
    text-align: center;
    margin-top: 0.6rem;
    margin-bottom: 0.4rem;
    height: 2.8rem;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="netflix-title">MOVIE RECOMMENDER</div>', unsafe_allow_html=True)
st.markdown('<div class="netflix-subtitle">Discover movies you will love based on your favorites</div>', unsafe_allow_html=True)

selected_movie_name = st.selectbox('Select a movie to get recommendations:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(f'<div class="movie-title">{names[i]}</div>', unsafe_allow_html=True)


