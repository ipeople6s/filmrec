'''
user collaborative flitering algorithm:
    based on user and his/her rating on movies
'''

import pandas as pd
import numpy as np
from util import get_movies, get_ratings, get_users
from math import *
import random

class UserCF():
    def __init__(self):
        self.loadData()
        # get all userID and all movieID
        self.all_users = self.user_movie['UserID'].tolist()
        self.all_users = list(set(self.all_users))
        self.all_movies = self.user_movie['MovieID'].tolist()
        self.all_movies = list(set(self.all_movies))
        # split training set and testing set
        self.trainData,self.testData = self.splitData(3,47)
    
    def loadData(self):
        # get movie table
        self.movies = get_movies()
        # get rating table
        self.ratings = get_ratings()
        # merge the two tables
        self.data = pd.merge(self.movies,self.ratings,on='MovieID')
        # select a part of keys and sort the table by UserID
        self.user_movie = self.data[['UserID','Rating','MovieID','Title']].sort_values('UserID')
    
    def splitData(self,k,seed,M=8):
        # k : param, seed: random seed, M: random maxinum
        # split training set and testing set
        train, test = {},{}
        random.seed(seed)

        for idx in self.user_movie.index:
            # get each line data
            line = self.user_movie.iloc[idx].values
            # split the line
            userID, rating , movieID, title = line
            if random.randint(0,M) == k:
                test.setdefault(userID,{})
                test[userID][movieID] = rating
            else:
                train.setdefault(userID,{})
                train[userID][movieID] = rating
        return train,test
    
    def userSimilarity(self,user1,user2):
        try:
            user1_dict = self.trainData[user1].clone()
            user2_dict = self.trainData[user2].clone()
        except:
            # if user2 or user1 doesn't exist
            return -1
        # fill 0 with user2_dict where movie1 not exists
        for movie1 in user1_dict.keys():
            if movie1 not in user2_dict.keys():
                user2_dict[movie1] = 0
        # fill 0 with user1_dict where movie1 not exists
        for movie2 in user2_dict.keys():
            if movie2 not in user1_dict.keys():
                user1_dict[movie2] = 0
        
        # compute cos similirity
        user1_vec,user2_vec = [],[]
        for movie in user1_dict.keys():
            rating1 = user1_dict[movie]
            rating2 = user2_dict[movie]
            user1_vec.append(rating1)
            user2_vec.append(rating2)
        
        return self.cosSim(user1_vec,user2_vec)
    
    # cosine similirity
    def cosSim(self,vec1,vec2):
        norm1 = sqrt(np.sum([i ** 2 for i in vec1]))
        norm2 = sqrt(np.sum([i ** 2 for i in vec2]))

        if norm1 == 0 or norm2 == 0:
            return -1
        
        mult = np.sum([vec1[i] * vec2[i] for i in range(len(vec1))])

        return mult / (norm1 * norm2)
    
    # recommend movies
    # user_rec: userID, k: the topk similirity, nitems: the number of movies recommended
    def recommend(self,user_rec,k=8,nitems=4):
        # contains all user sim with the parameter 'user_rec'
        results = {}
        user_sims = {}
        for userID in self.all_users:
            if user_rec != userID:
                sim = self.userSimilarity(user_rec,userID)
                user_sims[userID] = sim
        
        user_sims_sorted = sorted(user_sims.items(),key=lambda x : x[1], reverse=True)
        user_sims_sorted = [item[0] for item in user_sims_sorted]
        # users with topk similirity
        topk_sim_users = user_sims_sorted[:k]
        # loop each user
        for user in topk_sim_users:
            # get all movie and rating
            user_dict = self.trainData[user]
            # sort
            user_dict = sorted(user_dict.items(),key=lambda x : x[1], reverse=True)
            movies = [item[0] for item in user_dict]
            # add to result
            for movie in movies:
                if movie not in results.keys():
                    results.setdefault(movie,1)
                else:
                    results[movie] = results[movie] + 1

        return list(dict(sorted(results.items(),key = lambda x : x[1],reverse=True)[0:min(nitems,len(results))]).keys())
                

userCF = UserCF()