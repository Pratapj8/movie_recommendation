import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

user = pd.read_csv("/Users/apple/Downloads/Data_science_file/3RI/3RI Machine learning /Movie_recommendation_Project/user.csv")
movies = pd.read_csv("/Users/apple/Downloads/Data_science_file/3RI/3RI Machine learning /Movie_recommendation_Project/movies.csv")

user.head()

movies.head()

user.drop("timestamp", axis=1, inplace=True)

df = pd.merge(left=user, right=movies, left_on="item_id", right_on="item_id")

df.groupby("title")["rating"].mean().sort_values(ascending=False)

df.head()

"The " + df.iloc[26613][3].replace(", The", "")

df["title"] = df["title"].apply(lambda x: "The " + x.replace(", The", "") if ", The " in x else x)

df

df.groupby("title")["rating"].mean().sort_values(ascending=False)

valid_movies = df["title"].value_counts().reset_index().query("count >= 100")["title"].tolist()

df = df[df["title"].isin(valid_movies)]

df.reset_index(drop=True, inplace=True)

df

df.info()

df.duplicated().sum()

movie_matrix = pd.pivot_table(df, index="user_id", columns="title", values="rating", fill_value=0)
movie_matrix

movies_corr = movie_matrix.corr()

movies_corr

movies_corr["Air Force One (1997)"].sort_values(ascending=False).head(6)[1:]

movies_corr["Star Wars (1977)"].sort_values(ascending=False).head(11)[1:]

df.iloc[432]["title"]

df.query(f"item_id=={50}")["title"][0]

def recommend_movie(movies_id):
    movie_title = df.query(f"item_id=={movies_id}")["title"].head(1).values[0]
    return movies_corr[movie_title].sort_values(ascending=False).head(6)[1:].index.tolist()

recommend_movie(50)

for i in df.query("user_id == 23 and rating >= 4")["item_id"].tolist():
    print(i)

len(df.query("user_id == 23 and rating >= 4")["item_id"].tolist())

recommend_movie(172)

ls = []
for i in df.query("user_id == 0 and rating >= 4")["item_id"].tolist():
    ls.append(recommend_movie(i))

list(set(np.array(ls).ravel()))

def content_based_recommendation_pre(user_id):
    ls = []
    for i in df.query(f"user_id == {user_id} and rating >= 4")["item_id"].tolist():
        ls.append(recommend_movie(i))
    
    return np.sort(np.unique(np.array(ls).ravel()))

content_based_recommendation_pre(23)

dummy_movies_set = content_based_recommendation_pre(23)

len(df[(df["user_id"]==23) & ~(df["title"].isin(dummy_movies_set))]["title"].tolist())

def content_based_recommendation(user_id):
    st = set()
    for i in df[(df["user_id"]==user_id) & (df["rating"]>= 4)]["item_id"].tolist():
        st.update(recommend_movie(i))
    
    return st - set(df[df["user_id"]==user_id]["title"].tolist())

len(content_based_recommendation(23))





user_matrix = pd.pivot_table(df, columns="user_id", index="title", values="rating", fill_value=0)
user_matrix

user_corr = user_matrix.corr()
user_corr

user_corr[5].sort_values(ascending=False).head(6)[1:]

ls = []
for i in user_corr[5].sort_values(ascending=False).head(6)[1:].index:
    for j in df[(df["user_id"]==i) & (df["rating"] >= 4)]["item_id"].tolist():
        ls.append(j)

all_users_movies = set(ls)
all_users_movies

my_user_movies = set(df[df["user_id"]==5]["item_id"].tolist())

all_users_movies - my_user_movies

df.iloc[list(all_users_movies - my_user_movies)]["title"].tolist()

def collaborative_recommendation(user_id):
    ls = []
    for i in user_corr[user_id].sort_values(ascending=False).head(6)[1:].index:
        for j in df[(df["user_id"]==i) & (df["rating"] >= 4)]["item_id"].tolist():
            ls.append(j)
    all_users_movies = set(ls)
    my_user_movies = set(df[df["user_id"]==user_id]["item_id"].tolist())
    return df.iloc[list(all_users_movies - my_user_movies)]["title"].tolist()

collaborative_recommendation(5)

df.iloc[list(all_users_movies - my_user_movies)]["title"].tolist() == collaborative_recommendation(5)

df[df["user_id"]==0]

content_based_recommendation(user_id=0)

collaborative_recommendation(user_id=0)

recommend_movie(movies_id=23)



