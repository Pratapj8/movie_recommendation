import pandas as pd
import numpy as np

# Load data
user = pd.read_csv("/Users/apple/Downloads/Data_science_file/3RI/3RI Machine learning /Movie_recommendation_Project/user.csv")
movies = pd.read_csv("/Users/apple/Downloads/Data_science_file/3RI/3RI Machine learning /Movie_recommendation_Project/movies.csv")

# Preprocessing
user.drop("timestamp", axis=1, inplace=True)
df = pd.merge(left=user, right=movies, on="item_id")
df["title"] = df["title"].apply(lambda x: "The " + x.replace(", The", "") if ", The" in x else x)

valid_movies = df["title"].value_counts().reset_index().query("count >= 100")["title"].tolist()
df = df[df["title"].isin(valid_movies)].reset_index(drop=True)

# Popularity-based (correlation matrix)
movie_matrix = pd.pivot_table(df, index="user_id", columns="title", values="rating", fill_value=0)
movies_corr = movie_matrix.corr()

def recommend_movie(movie_id):
    movie_title = df.query(f"item_id=={movie_id}")["title"].head(1).values[0]
    return movies_corr[movie_title].sort_values(ascending=False).head(6)[1:].index.tolist()

# Content-based filtering
def content_based_recommendation(user_id):
    recommended = set()
    for item_id in df[(df["user_id"] == user_id) & (df["rating"] >= 4)]["item_id"]:
        recommended.update(recommend_movie(item_id))
    watched = set(df[df["user_id"] == user_id]["title"])
    return list(recommended - watched)

# Collaborative filtering
user_matrix = pd.pivot_table(df, columns="user_id", index="title", values="rating", fill_value=0)
user_corr = user_matrix.corr()

def collaborative_recommendation(user_id):
    ls = []
    for sim_user in user_corr[user_id].sort_values(ascending=False).head(6)[1:].index:
        ls.extend(df[(df["user_id"] == sim_user) & (df["rating"] >= 4)]["item_id"].tolist())
    all_users_movies = set(ls)
    my_user_movies = set(df[df["user_id"] == user_id]["item_id"].tolist())
    return df[df["item_id"].isin(list(all_users_movies - my_user_movies))]["title"].unique().tolist()
