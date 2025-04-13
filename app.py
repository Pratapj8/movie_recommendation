import streamlit as st
from recommendation_functions import (
    recommend_movie,
    content_based_recommendation,
    collaborative_recommendation
)
import time
import pandas as pd

# Load movies data for searching by name
movies = pd.read_csv("movies.csv")  # Ensure the path is correct

# Title and Introduction
st.title("🎬 Movie Recommendation System")
st.markdown("""
Welcome to the **Movie Recommendation System**. You can get personalized movie recommendations based on different algorithms:
- Popularity-Based
- Content-Based Filtering
- Collaborative Filtering
""")

# Sidebar for selection
st.sidebar.title("Recommendation Settings")
method = st.sidebar.selectbox(
    "Choose a recommendation method:",
    (
        "Function 1: Popularity Based",
        "Function 2: Content-Based Filtering",
        "Function 3: Collaborative Filtering"
    )
)

# Movie ID or User ID input
if method == "Function 1: Popularity Based":
    movie_id = st.sidebar.text_input("Enter Movie ID:", "")
    num_recommendations = st.sidebar.slider("Number of Recommendations", 1, 5, 5)

elif method == "Function 2: Content-Based Filtering" or method == "Function 3: Collaborative Filtering":
    user_id = st.sidebar.text_input("Enter User ID:", "")
    num_recommendations = st.sidebar.slider("Number of Recommendations", 1, 5, 5)

# Feature: Search movie by ID and display its name
#st.sidebar.header("Movie ID  ",movie_id)
if movie_id:
    try:
        movie_id = int(movie_id)  # Ensure that Movie ID is an integer
        movie_name = movies[movies["item_id"] == movie_id]["title"].values
        if movie_name.size > 0:
            st.sidebar.write(f"**Movie Name for Movie ID {movie_id}:** {movie_name[0]}")
        else:
            st.sidebar.write("No movie found with that Movie ID.")
    except ValueError:
        st.sidebar.write("Please enter a valid numeric Movie ID.")

# Feature: Search movie by name
st.sidebar.header("Search Movie by Name")
movie_name = st.sidebar.text_input("Enter Movie Name to Get Movie ID:", "")
if movie_name:
    # Try to find the movie in the dataset
    movie_name = movie_name.lower()
    movie_found = movies[movies["title"].str.lower().str.contains(movie_name)]
    if not movie_found.empty:
        st.sidebar.write("Movies Found:")
        for _, row in movie_found.iterrows():
            st.sidebar.write(f"**Movie ID**: {row['item_id']} | **Title**: {row['title']}")
    else:
        st.sidebar.write("No movie found with that name.")

# Add a loading spinner
with st.spinner("Fetching recommendations..."):
    time.sleep(2)  # Simulate loading

# Display recommendations based on selected method
if method == "Function 1: Popularity Based":
    if movie_id:
        try:
            recs = recommend_movie(int(movie_id))
            # Fetch movie name
            movie_title = movies[movies["item_id"] == int(movie_id)]["title"].values
            if movie_title.size > 0:
                movie_title = movie_title[0]
            else:
                movie_title = f"Movie ID {movie_id}"

            st.write(f"🎥 **Top {num_recommendations} Movies Similar to '{movie_title}':**")
            st.write(recs[:num_recommendations])
        except Exception as e:
            st.error(f"Error: {e}")


elif method == "Function 2: Content-Based Filtering":
    if user_id:
        try:
            recs = content_based_recommendation(int(user_id))
            st.write(f"🎥 **Top {num_recommendations} Movies for User ID {user_id}:**")
            st.write(recs[:num_recommendations])
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid User ID.")

elif method == "Function 3: Collaborative Filtering":
    if user_id:
        try:
            recs = collaborative_recommendation(int(user_id))
            st.write(f"🎥 **Top {num_recommendations} Movies for User ID {user_id} based on Similar Users:**")
            st.write(recs[:num_recommendations])
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid User ID.")
