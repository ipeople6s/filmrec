'''
dataset: movielens 1m
data_root: ../data/ml-1m

tree:
    ml-1m
        movies.dat
        ratings.dat
        users.dat
        DataExplain.md

Data Explanition:
    ratings.dat : 
        contains each user's rating to each movie
        UserID::MovieID::Rating::Timestamp
    users.dat:
        user information
        UserID::Gender::Age::Occupation::Zip-code
    movies.dat:
        movie information
        MovieID::Title::Genres
    
    PS: see more details in DataExplain.md

Functions: change dat file to list
'''

import os
import pandas as pd

data_root = '../data/ml-1m'

def get_movies():
    # get movies.dat path
    movies_path = os.path.join(data_root,'movies.dat')
    # open movies.dat file
    cols = ['MovieID','Title','Genres']
    df = pd.read_csv(movies_path,sep='::',encoding='ISO-8859-1',header=None)
    df.columns = cols
    return df

def get_ratings():
    # get ratings.dat path
    ratings_path = os.path.join(data_root,'ratings.dat')
    # open ratings.dat file
    cols = ['UserID','MovieID','Rating','Timestamp']
    df = pd.read_csv(ratings_path,sep='::',encoding='ISO-8859-1',header=None)
    df.columns = cols
    return df

def get_users():
    # get users.dat path
    users_path = os.path.join(data_root,'users.dat')
    # open users.dat file
    cols = ['UserID','Gender','Age','Occupation','Zip-code']
    df = pd.read_csv(users_path,sep='::',encoding='ISO-8859-1',header=None)
    df.columns = cols
    return df