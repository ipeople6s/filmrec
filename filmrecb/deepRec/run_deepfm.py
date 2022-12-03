# -*- coding: utf-8 -*-
import pandas as pd
import torch
from sklearn.metrics import log_loss, roc_auc_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, Binarizer
import sys
import os

import torch.nn as nn
import numpy as np
import torch.utils.data as Data
from torch.utils.data import DataLoader
import torch.optim as optim
import torch.nn.functional as F
from sklearn.metrics import log_loss, roc_auc_score
from collections import OrderedDict, namedtuple, defaultdict
import random
import os,sys
from deepctrmodels.deepfm import Deepfm
from deepctrmodels import Deepfm


os.chdir(sys.path[0])

if __name__ == "__main__":

    seed = 1024
    torch.manual_seed(seed)  # 为CPU设置随机种子
    torch.cuda.manual_seed(seed)  # 为当前GPU设置随机种子
    torch.cuda.manual_seed_all(seed)  # 为所有GPU设置随机种子
    np.random.seed(seed)
    random.seed(seed)

    userData = None
    movieData = None
    target = 'Rating'

    if os.path.exists('pre_ratings.csv'):
        userData = pd.read_csv('pre_users.csv')
        movieData = pd.read_csv('pre_movies.csv')
        ratingData = pd.read_csv('pre_ratings.csv')
        feature_names = ['Title', 'Genres'] + ['Gender', 'Age', 'Occupation', 'Zip-code']
    else:
        userData = pd.read_csv('ml-1m/users.dat', names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'], sep='::',
                               engine='python')
        movieData = pd.read_csv('ml-1m/movies.dat', names=['MovieID', 'Title', 'Genres'], sep='::', engine='python',
                                encoding='ISO-8859-1')
        ratingData = pd.read_csv('ml-1m/ratings.dat', names=['UserID', 'MovieID', 'Rating', 'Timestamp'], sep='::',
                                 engine='python')
        userData = userData.rename(index=userData['UserID']).drop('UserID', axis=1)
        movieData = movieData.rename(index=movieData['MovieID']).drop('MovieID', axis=1)

        feature_names = userData.columns.tolist() + movieData.columns.tolist()
        ratingData = ratingData.reindex(columns=ratingData.columns.tolist() + feature_names)

        # 1.Label Encoding for sparse features,and do simple Transformation for dense features
        # LabelEncoder()，labelize item
        for feat, col in movieData.iteritems():
            lbe = LabelEncoder()
            movieData[feat + '_enc'] = lbe.fit_transform(col)

        for feat, col in userData.iteritems():
            lbe = LabelEncoder()
            userData[feat + '_enc'] = lbe.fit_transform(col)

        # max-min 0-1
        # mms = MinMaxScaler(feature_range=(1, 5))
        # ratingData[['Rating']] = mms.fit_transform(ratingData[['Rating']])

        for index, row in ratingData.iterrows():
            for feat in ['Title', 'Genres']:
                ratingData.loc[index, feat] = movieData.loc[int(row['MovieID']), feat + '_enc']
            for feat in ['Gender', 'Age', 'Occupation', 'Zip-code']:
                ratingData.loc[index, feat] = userData.loc[int(row['UserID']), feat + '_enc']
        userData.to_csv('pre_users.csv')
        movieData.to_csv('pre_movies.csv')
        ratingData.to_csv('pre_ratings.csv')


    # # 2.count #unique features for each sparse field,and record dense feature field name
    movie_feat_sizes = {feat: len(movieData[feat].unique()) for feat in ['Title', 'Genres']}
    user_feat_sizes = {feat: len(userData[feat].unique()) for feat in ['Gender', 'Age', 'Occupation', 'Zip-code']}
    feat_sizes = {}
    feat_sizes.update(movie_feat_sizes)
    feat_sizes.update(user_feat_sizes)

    # 3.generate input data for model
    train, test = train_test_split(ratingData, test_size=0.9, random_state=2020)
    train_model_input = {name: train[name] for name in feature_names}
    test_model_input = {name: test[name] for name in feature_names}

    # # 4.Define Model,train,predict and evaluate
    use_cuda = True
    cuda_to_use = torch.device(f'cuda:0')
    device = cuda_to_use if torch.cuda.is_available() else "cpu"

    model = Deepfm(feat_sizes, sparse_feature_columns=feature_names, dense_feature_columns=[],
                   dnn_hidden_units=[400, 400, 400], dnn_dropout=0.9, ebedding_size=8,
                   l2_reg_linear=1e-3, device=device)

    model.fit(train_model_input, train[target].values, None, None, batch_size=200,
              epochs=1000, verbose=1)
    torch.save(model, 'xdeepfm.pt')

    print("final test")
    pred_ans = model.predict(test_model_input, batch_size=256)
    print("test MSE", round(mean_squared_error(
        test[target].values, pred_ans), 4))
