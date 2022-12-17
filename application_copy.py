import pandas as pd
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import coo_matrix, hstack
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
import streamlit as st

data = pd.read_csv("./clean_df/clean_df.csv")
data = data.drop(['Unnamed: 0'],axis = 1)
data = data.dropna(subset=['overview','director','runtime','year']).reset_index(drop=True)
data = data.fillna('')
text_data = ['title','director','actor','overview','genres_list','key','country']
data[text_data] = data[text_data].astype(str)
data["key"] = data["key"].str.encode('ascii', 'ignore').str.decode('ascii')

def to_dummy(col,num = None):
    li = set()
    for i in range(len(data[col])):
        if num is None:
            try:
                num = len(data[col][i].split(','))
            except:
                print(data[col][i])
        for act in data[col][i].split(',')[:num]:
            li.add(act)
    li = list(li)
    for element in li:
        data[element] = data[col].astype(str).str.contains(element, case=False).astype(int)

@st.cache
def convert(dum):
    for d in dum:
        if d == 'actor':
            to_dummy(d,num = 4)
        else:
            to_dummy(d)
        print(d)
dum = ['country','director','actor','genres_list','key']
convert(dum)

X = data.drop(['id','title','director','actor', 'overview','genres_list','key','country'], axis=1)
scaler = StandardScaler()
X = scaler.fit_transform(X)
tfidf = TfidfVectorizer(stop_words = 'english')  # initialising the TF-IDF Vector object
tfidf_matrix = tfidf.fit_transform(data['overview'])  # Constructing the TF-IDF Matrix (no. of movies x every word in vocabulary)
X = hstack([X,tfidf_matrix]).toarray()
cosine_sim = linear_kernel(X, X)  # Constructing the Cosine Similarity Matrix (no. of movies x no. of movies)
indices = pd.Series(data.index, index = data['title']).drop_duplicates()

# Function that inputs movie titles and outputs top 10 movies similar to it

def get_recommendations(title, cosine_sim = cosine_sim):
    idx = indices[title]

    sim_scores = list(enumerate(cosine_sim[idx]))  # Get the similarity scores of all movies wrt input movie
    sim_scores = sorted(sim_scores, key = lambda x : x[1], reverse = True)
    sim_scores = sim_scores[1:11]

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