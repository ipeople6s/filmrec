import numpy as np
import torch
import os,sys
import pandas as pd
from sklearn.preprocessing import LabelEncoder
# from .deepctrmodels import Deepfm
from deepctrmodels.deepfm import Deepfm
# from deepctrmodels.deepfm import Deepfm



# os.chdir(sys.path[0])

def inference(user_id,model,n_items=4):
    print(os.getcwd())
    if os.path.exists(package_directory + 'pre_ratings.csv'):
        userData = pd.read_csv(package_directory + 'pre_users.csv')
        movieData = pd.read_csv(package_directory + 'pre_movies.csv')
        ratingData = pd.read_csv(package_directory + 'pre_ratings.csv')
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

    rank = {}
    for index, row in movieData.iterrows():
        input_net = dict(zip(['Title', 'Genres'], row[['Title_enc', 'Genres_enc']].tolist()))
        input_net.update(dict(zip(['Gender', 'Age', 'Occupation', 'Zip-code'], userData.loc[
            user_id, ['Gender_enc', 'Age_enc', 'Occupation_enc', 'Zip-code_enc']])))
        input_net = pd.DataFrame([input_net])
        rank[index] = model.predict(input_net, batch_size=1).squeeze()
    ids = np.array(sorted(rank.items(), key=lambda d: d[1], reverse=True)[:5])
    res = [int(entry[0]) for entry in ids]
    return res[:min(len(res),n_items)]


package_directory = os.path.dirname(os.path.abspath(__file__)) + "/"

def get_deepfm():
    userData = None
    movieData = None
    target = 'Rating'

    if os.path.exists(package_directory + 'pre_ratings.csv'):
        userData = pd.read_csv(package_directory + 'pre_users.csv')
        movieData = pd.read_csv(package_directory + 'pre_movies.csv')
        ratingData = pd.read_csv(package_directory + 'pre_ratings.csv')
        feature_names = ['Title', 'Genres'] + ['Gender', 'Age', 'Occupation', 'Zip-code']
    else:
        userData = pd.read_csv(package_directory + 'ml-1m/users.dat', names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'], sep='::',
                               engine='python')
        movieData = pd.read_csv(package_directory + 'ml-1m/movies.dat', names=['MovieID', 'Title', 'Genres'], sep='::', engine='python',
                                encoding='ISO-8859-1')
        ratingData = pd.read_csv(package_directory + 'ml-1m/ratings.dat', names=['UserID', 'MovieID', 'Rating', 'Timestamp'], sep='::',
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
        userData.to_csv(package_directory + 'pre_users.csv')
        movieData.to_csv(package_directory + 'pre_movies.csv')
        ratingData.to_csv(package_directory + 'pre_ratings.csv')


    movie_feat_sizes = {feat: len(movieData[feat].unique()) for feat in ['Title', 'Genres']}
    user_feat_sizes = {feat: len(userData[feat].unique()) for feat in ['Gender', 'Age', 'Occupation', 'Zip-code']}
    feat_sizes = {}
    feat_sizes.update(movie_feat_sizes)
    feat_sizes.update(user_feat_sizes)

    use_cuda = True
    cuda_to_use = torch.device(f'cuda:0')
    device = cuda_to_use if torch.cuda.is_available() else "cpu"

    model = Deepfm(feat_sizes, sparse_feature_columns=feature_names, dense_feature_columns=[],
                   dnn_hidden_units=[400, 400, 400], dnn_dropout=0.9, ebedding_size=8,
                   l2_reg_linear=1e-3, device=device)
    
    model = model.load_state_dict(torch.load(package_directory + 'xdeepfm.pt'))
    return model

def get_model():
    xDeepFM_model = torch.load(package_directory + 'xdeepfm.pt')
    onn_model = torch.load(os.path.join(package_directory, 'onn.pt'))
    return xDeepFM_model, onn_model

def main():

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
    print(ids)
    print(movieData.loc[ids[:, 0], 'Title'], ids[:, 1])

# xDeepFM_model = torch.load('xdeepfm.pt')
# onn_model = torch.load('onn.pt')
# print('输入查询的用户ID')
# userID = int(input())
# res = inference(userID,onn_model)
