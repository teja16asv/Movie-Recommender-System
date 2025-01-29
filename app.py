#importing required libraries
import pandas as pd
import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=4eae279994a99aaea9226d3b51cbff63&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movies,similarity,movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances=similarity[movie_index]
    movies_list= sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies,recommended_movie_posters


def main():

    st.header('Movie Recommender System')
    
    #importing movies data from the pickle file
    movies_dict = pickle.load(open("D:\MoviesDataset\movie_dict.pkl",'rb'))
    #importing computed distances basis movie index
    similarity = pickle.load(open('D:\MoviesDataset\similarity.pkl','rb'))
    
    #Converting pickle file into a pandas dataframe
    movies=pd.DataFrame(movies_dict)
    
    #creating a streamlit dropdown to let the user select movie
    selected_movie_name = st.selectbox(
        "Select the Movie: ",
        movies['title'].values)
    
    #Creating button to recommend movies
    if st.button('Show Recommendation'):
        names,posters=recommend(movies,similarity,selected_movie_name)
        
        #movies to be displayed in 5 columns
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.header(names[0])
            st.image(posters[0])
        with col2:
            st.header(names[1])
            st.image(posters[1])
        with col3:
            st.header(names[2])
            st.image(posters[2])
        with col4:
            st.header(names[3])
            st.image(posters[3])
        with col5:
            st.header(names[4])
            st.image(posters[4])

    #using html code to change background colour of streamlit web app
    st.markdown('<style>.stApp {background-color: #333333;}</style>', unsafe_allow_html=True)

#Code Execution begins here
if __name__=="__main__":
    main()


