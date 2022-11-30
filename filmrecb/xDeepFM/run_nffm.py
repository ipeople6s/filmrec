import pandas as pd
import torch
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from deepctrmodels.inputs import SparseFeat, get_feature_names
from deepctrmodels.models import onn, xdeepfm
import os,sys

os.chdir(sys.path[0])

if __name__ == "__main__":

    target = ['Rating']
    if os.path.exists('pre_ratings.csv'):
        userData = pd.read_csv('pre_users.csv')
        movieData = pd.read_csv('pre_movies.csv')
        data = pd.read_csv("./pre_ratings.csv")
        sparse_features = ['Title', 'Genres'] + ['Gender', 'Age', 'Occupation', 'Zip-code']
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
        #LabelEncoder()，labelize item
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

    # 2.count #unique features for each sparse field

    fixlen_feature_columns = [SparseFeat(feat, movieData[feat].nunique())
                              for feat in ['Title', 'Genres']] + [SparseFeat(feat, userData[feat].nunique())
                                                                  for feat in
                                                                  ['Gender', 'Age', 'Occupation', 'Zip-code']]
    linear_feature_columns = fixlen_feature_columns
    dnn_feature_columns = fixlen_feature_columns
    feature_names = get_feature_names(linear_feature_columns + dnn_feature_columns)

    # 3.generate input data for model
    train, test = train_test_split(data, test_size=0.2)
    train_model_input = {name: train[name] for name in feature_names}
    test_model_input = {name: test[name] for name in feature_names}
    # 4.Define Model,train,predict and evaluate

    device = 'cpu'
    use_cuda = True
    if use_cuda and torch.cuda.is_available():
        print('cuda ready...')
        device = 'cuda:0'

    model = onn.ONN(linear_feature_columns, dnn_feature_columns, task='regression', device=device)
    model.compile("adam", "mse", metrics=['mse'], )

    history = model.fit(train_model_input, train[target].values, batch_size=256, epochs=10, verbose=2,
                        validation_split=0.2)
    torch.save(model, 'ONN.pt')

    pred_ans = model.predict(test_model_input, batch_size=256)
    print("test MSE", round(mean_squared_error(
        test[target].values, pred_ans), 4))
