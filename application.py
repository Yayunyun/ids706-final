import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import streamlit as st
import pickle

data = pd.read_csv("./clean_df/clean_df.csv")
data = data.drop(['Unnamed: 0'],axis = 1)
data = data.dropna(subset=['overview','director','runtime','year']).reset_index(drop=True)
data = data.fillna('')
text_data = ['title','director','actor','overview','genres_list','key','country']
data[text_data] = data[text_data].astype(str)
data["key"] = data["key"].str.encode('ascii', 'ignore').str.decode('ascii')

with open("cosine_sim.pickle", 'rb') as f:
    cosine_sim = pickle.load(f)

indices = pd.Series(data.index, index = data['title']).drop_duplicates()

def get_recommendations(title, cosine_sim0 = cosine_sim,num=10, indices0 = indices):
    idx = indices0[title]
    sim_scores = list(enumerate(cosine_sim0[idx]))  # Get the similarity scores of all movies wrt input movie
    sim_scores = sor ted(sim_scores, key = lambda x : x[1], reverse = True)
    sim_scores = sim_scores[1:num+1]
    movie_indices = [i[0] for i in sim_scores]
    return data['title'].iloc[movie_indices]


def main():
    st.title("Movie Recommender")
    st.write("This is a movie recommender based on the IMDB dataset.")
    st.write("The user can select a song and the recommender will find the 10 most similar songs.")

    menu = ["Home", "Recommender"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.subheader("Home")
        st.write("This is the home page.")
    elif choice == "Recommender":
        st.subheader("Recommender")
        st.write("Please enter the movie you like.")
        movie_list = data['title'].unique()
        selected_movie = st.selectbox( "Type or select a movie from the dropdown", movie_list)
        num_of_movie = st.slider("Number of songs to recommend", 1, 30, 5)
        if st.button("Recommend"):
            recommendation = get_recommendations(selected_movie,num = num_of_movie)
            st.write(recommendation)

if __name__ == '__main__':
    main()