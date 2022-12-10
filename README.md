# Brief

I implement two deep learning based recommender algorithm (xDeepFM and ONN) and two non-deep learning based recommender algorithm (Collaborative Filter and Matrix Decomposition Algorithm based on Gradient Descent) to recommend movies for system users. Besides, I designed a Ib user interface for the recommender system, which can visualize recommender results and make it convenient for users to utilize the system. Then, I give an overview of the development of recommender systems, and compare the performance of the four algorithms I use.

# Running the project

## Project setup

```shell
cd filmrecf
npm install
```

### Compiles and hot-reloads for development

```shell
npm run serve
```

### Compiles and minifies for production

```shell
npm run build
```

### Lints and fixes files

```shell
npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

### Start

```shell
npm run serve
cd ../filmrecb
python app.py
```



# Algorithm

## Collaborative Filter

The details of collaborative filter can be seen in *userCF.py* in filmrecb directory. The procedure of the algorithm is as follows:

1. Establish user behavior matrix.
2. For a user to be recommended, calculate the cosine similarity with other users.
3. Select users with Top-K similarities as set $U_r$
4. Compute films that rated by users in $U_r$. Then find films with top ratings by these users.

## Matrix Decomposition Algorithm

The details of collaborative filter can be seen in *MF.py* in filmrecb directory. The procedure of the algorithm is as follows:

1. Establish user behavior matrix.
2. Training with P and Q matrix according to FunkSVD.
3. Define a new rating matrix $R_{new}$.
4. Recommend films which is 0 rating in user behavior matrix and top rating in $R_{new}$.

## xDeepFm and ONN

The details of collaborative filter can be seen in *inference.py, train_deepfm.py, train_nffm.py* in deeper directory.

These two deep learning models are CTR models. So I change the movielens data to fit with CTR model.
