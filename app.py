import pickle
import streamlit as st
import requests

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=07f8d87d813dd120113d0006541744fc&language=en-US"
    response = requests.get(url)
    movie_data = response.json()

    movie_details = {
        'title': movie_data.get('title', 'N/A'),
        'poster_path': f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path', '')}",
        'cast': [cast_member['name'] for cast_member in movie_data.get('credits', {}).get('cast', [])][:5],
        'ratings': movie_data.get('vote_average', 'N/A'),
        'overview': movie_data.get('overview', 'N/A')
    }
    return movie_details

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:  # Assuming you want the top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        movie_details = fetch_movie_details(movie_id)  # Ensure this returns a dictionary
        recommended_movies.append(movie_details)
    return recommended_movies



st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movies = recommend(selected_movie)
    cols = st.columns(5)
    for i, movie_details in enumerate(recommended_movies):
        with cols[i]:
            st.image(movie_details['poster_path'], caption=movie_details['title'])
            with st.expander("See details"):
                st.write(f"Ratings: {movie_details['ratings']}")
                st.write(f"Overview: {movie_details['overview']}")





