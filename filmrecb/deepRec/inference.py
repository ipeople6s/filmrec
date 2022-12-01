import numpy as np
import torch
import os,sys
import pandas as pd

from deepctrmodels.deepfm import Deepfm

os.chdir(sys.path[0])

if __name__ == "__main__":

    if os.path.exists('pre_ratings.csv'):
        userData = pd.read_csv('pre_users.csv')
        movieData = pd.read_csv('pre_movies.csv')
        ratingData = pd.read_csv('pre_ratings.csv')
        feature_names = ['Title', 'Genres'] + ['Gender', 'Age', 'Occupation', 'Zip-code']
    else:
        raise FileNotFoundError

    device = 'cpu'
    use_cuda = True
    if use_cuda and torch.cuda.is_available():
        print('cuda ready...')
        device = 'cuda:0'

    movie_feat_sizes = {feat: len(movieData[feat].unique()) for feat in ['Title', 'Genres']}
    user_feat_sizes = {feat: len(userData[feat].unique()) for feat in ['Gender', 'Age', 'Occupation', 'Zip-code']}
    feat_sizes = {}
    feat_sizes.update(movie_feat_sizes)
    feat_sizes.update(user_feat_sizes)
    #
    xDeepFM_model = torch.load('xdeepfm.pt')
    onn_model = torch.load('onn.pt')

    print('输入查询的用户ID')
    userID = int(input())
    rank = {}
    for index, row in movieData.iterrows():
        input_net = dict(zip(['Title', 'Genres'], row[['Title_enc', 'Genres_enc']].tolist()))
        input_net.update(dict(zip(['Gender', 'Age', 'Occupation', 'Zip-code'], userData.loc[
            userID, ['Gender_enc', 'Age_enc', 'Occupation_enc', 'Zip-code_enc']])))
        input_net = pd.DataFrame([input_net])
        rank[index] = xDeepFM_model.predict(input_net, batch_size=1).squeeze()
    ids = np.array(sorted(rank.items(), key=lambda d: d[1], reverse=True)[:5])
    print(movieData.loc[ids[:, 0], 'Title'], ids[:, 1])