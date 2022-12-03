'''
Matrix Factorization
'''
import pandas as pd
import numpy as np
from util import get_movies, get_ratings, get_users
from math import *
import random
import os,sys

os.chdir(sys.path[0])

def save_pq(P,Q,rating_matrix):
    P = np.array(P)
    Q = np.array(Q)
    rm = np.array(rating_matrix)
    np.savez('pq.npz',P=P,Q=Q,rm=rm)

class MatrixFactorization():
    def __init__(self) -> None:
        self.loadData()
        # get all userID and all movieID
        self.all_users = self.user_movie['UserID'].tolist()
        self.all_users = list(set(self.all_users))      # 6040 in total, 3706 in total.
        self.num_of_users = max(self.all_users)

        self.all_movies = self.user_movie['MovieID'].tolist()
        self.all_movies = list(set(self.all_movies))
        self.num_of_movies = max(self.all_movies)

        self.num_of_movie_types = len(self.movie_types)
        # matrix factorization
        if os.path.exists('pq.npz'):
            pq_npz = np.load('pq.npz')
            self.P = pq_npz['P']
            self.Q = pq_npz['Q']
            self.rating_matrix = pq_npz['rm']
        else:
            # split training set and testing set
            self.trainData,self.testData = self.splitData(3,47)
            # get rating_matrix
            self.get_rating_matrix()
            self.P,self.Q = self.matrixFactorization()
            save_pq(self.P,self.Q,self.rating_matrix)
            # get new matrix factorization
        self.new_rating_matrix = self.newRatingMatrix(self.P,self.Q)
    
    def get_rating_matrix(self):
        '''
        get rating matrix, each row is userId and each column is movieID, the element is rating.
        change self.trainData dict to matrix
        '''
        # initialize zero matrix
        self.rating_matrix = np.zeros((self.num_of_users,self.num_of_movies))
        # set user-movie ratings
        for user, movie_rating in self.trainData.items():
            for movie,rating in movie_rating.items():
                self.rating_matrix[user,movie] = rating
    
    def loadData(self):
        # get movie table
        self.movies = get_movies()
        # get rating table
        self.ratings = get_ratings()
        # merge the two tables, if only want a part of data, please slice self.data
        self.data = pd.merge(self.movies,self.ratings,on='MovieID')
        # select a part of keys and sort the table by UserID
        self.user_movie = self.data[['UserID','Rating','MovieID','Title']].sort_values('UserID')
        # get all types of movies
        self.movie_types = set()
        for line in self.movies['Genres']:
            types = line.split('|')
            for type in types:
                self.movie_types.add(type)
    
    def allDataToTrain(self):
        train = {}
        for idx in self.user_movie.index:
            # get each line data
            line = self.user_movie.iloc[idx].values
            # split the line
            userID, rating , movieID, title = line
            userID = userID - 1
            movieID = movieID - 1
            train.setdefault(userID,{})
            train[userID][movieID] = rating
        return train

    def splitData(self, k, seed, M=8):
        # k : param, seed: random seed, M: random maxinum
        # split training set and testing set
        train, test = {},{}
        random.seed(seed)

        for idx in self.user_movie.index:
            # get each line data
            try:
                line = self.user_movie.iloc[idx].values
            except:
                continue
            # split the line
            userID, rating , movieID, title = line
            userID = userID - 1
            movieID = movieID - 1
            if random.randint(0,M) == k:
                test.setdefault(userID,{})
                test[userID][movieID] = rating
            else:
                train.setdefault(userID,{})
                train[userID][movieID] = rating
        return train,test
    
    def matrixFactorization(self):
        '''
        matrix factorization based on graident descent
        '''
        # get shape of rating matrix
        m,n = self.rating_matrix.shape
        K = self.num_of_movie_types
        # initialize P,Q matrix factorized. That means R = P * Q
        # R has shape (m,n), P has shape (m,k), Q has shape (k,n)
        P = np.mat(np.random.random((m, K)))
        Q = np.mat(np.random.random((K, n)))

        # hyperparameter
        lr = 0.0002
        beta = 0.02
        epochs = 1
        # training
        for epoch in range(epochs):
            for i in range(m):
                for j in range(n):
                    if self.rating_matrix[i,j] > 0:
                        error = self.rating_matrix[i,j]
                        for k in range(K):
                            error = error - P[i,k] * Q[k,j]
                        for k in range(K):
                            P[i,k] = P[i,k] + lr * (2 * error * Q[k,j] - beta * P[i,k])
                            Q[k,j] = Q[k,j] + lr * (2 * error * P[i,k] - beta * Q[k,j])
            loss = 0.0
            for i in range(m):
                for j in range(n):
                    if self.rating_matrix[i,j] > 0:
                        error = 0.0
                        for k in range(K):
                            error = error + P[i,k]*Q[k,j]
                        loss = (self.rating_matrix[i,j] - error) * (self.rating_matrix[i,j] - error)
                        for k in range(K):
                            loss = loss + beta * (P[i,k] * P[i,k] + Q[k,j] * Q[k,j]) / 2
            print('epoch {}, the loss is {}'.format(epoch,loss))
            if loss < 0.001:
                break
        return P,Q
    
    def newRatingMatrix(self,P,Q):
        return np.matmul(P, Q)
    
    def recommend(self,user_rec,nitems=4):
        user_rec = user_rec - 1
        assert nitems < self.num_of_movies

        movies_rating_not_seen = []
        for id,rating in enumerate(self.rating_matrix[user_rec]):
            if rating == 0:
                movies_rating_not_seen.append((id,rating))
        sorted_movie_rating = sorted(movies_rating_not_seen,key=lambda x : x[1],reverse=True)
        rec_movies = [sorted_movie_rating[i][0] for i in range(min(len(sorted_movie_rating),nitems))]
        return rec_movies

mf = MatrixFactorization()
# results = mf.recommend(178)
