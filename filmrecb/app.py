from ctypes.wintypes import INT
import json
from pickle import NONE
from flask import Flask, request
import os
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import zipfile
from util import *
import shutil
import base64
import urllib
import re
# from filmrecb import userCF
from userCF import userCF


app = Flask(__name__)
CORS(app, supports_credentials=True)

basedir = os.path.abspath(os.path.dirname(__file__))


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "../data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "20222022"

db = SQLAlchemy(app)


# create table tb_movie (
#     movie_id INT primary key,
#     movie_name char(64),
#     movie_poster char(64)
# );
class Movie(db.Model):
    __tablename__ = 'tb_movie'

    movie_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(64))
    movie_poster = db.Column(db.String(64))


# create table tb_genres (
#     g_id INTEGER PRIMARY KEY,
#     g_name char(64)
# );
class Genres(db.Model):
    __tablename__ = 'tb_genres'

    g_id = db.Column(db.Integer, primary_key=True)
    g_name = db.Column(db.String(64))
    
id = 11

# create table tb_movie_genres (
#     mg_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     movie_id INTEGER,
#     g_id INTEGER,
#     FOREIGN KEY(movie_id) REFERENCES tb_movie(movie_id),
#     FOREIGN KEY(g_id) REFERENCES tb_genres(g_id)
# );
class MovieGenres(db.Model):
    __tablename__ = 'tb_movie_genres'

    mg_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g_id = db.Column(db.Integer, db.ForeignKey('tb_genres.g_id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('tb_movie.movie_id'))



# 10 movies recommended
def get_rec_movies():
    res = userCF.recommend(id)
    print(res)
    return res


def get_movies_by_id(ids):
    res = []
    for id in ids:
        m = Movie.query.filter(Movie.movie_id == int(id)).first()
        if m is not None:
            d = dict()
            d["name"] = m.movie_name
            d["id"] = m.movie_id
            d["poster"] = m.movie_poster
            all_genres = db.session.query(Genres.g_name).filter(Genres.g_id == MovieGenres.g_id).filter(MovieGenres.movie_id == m.movie_id).all()
            d["genres"] =[]
            for i in all_genres:
                d["genres"].extend(i)
            res.append(d)
    print(res)
    return res


@app.route('/api/search', methods=['POST'])
@cross_origin(supports_credentials=True)
def search_movie():
    json_data = request.json
    name = json_data["name"]
    print(name)
    t = Movie.query.filter(Movie.movie_name.startswith(name)).first()
    res = None
    if t is not None:
        res = dict()
        res["name"] = t.movie_name
        res["id"] = t.movie_id
        res["poster"] = t.movie_poster
        all_genres = db.session.query(Genres.g_name).filter(Genres.g_id == MovieGenres.g_id).filter(MovieGenres.movie_id == t.movie_id).all()
        res["genres"] =[]
        for i in all_genres:
            res["genres"].extend(i)

    return {"data": {"movies": res, "rec": get_movies_by_id(get_rec_movies())}, "status": 200, "message": ""}

algo = "CF"

@app.route('/api/algo', methods=['POST'])
@cross_origin(supports_credentials=True)
def change_rec_algo():
    global algo
    json_data = request.json
    algo = json_data["algo"]
    return {"data": {}, "status": 200, "message": ""}


@app.route('/api/movies', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_movies():
    page = int(request.args.get('page')) - 1
    label = int(request.args.get('label'))
    
    all_movies = Movie.query.all()

    all_genres = Genres.query.all()
    # g_id -> g_name
    d1 = dict()
    for g in all_genres:
        d1[g.g_id] = g.g_name

    all_movie_genres = MovieGenres.query.all()
    # movie_id -> genres []
    d2 = dict()
    for g in all_movie_genres:
        if g.movie_id not in d2.keys():
            d2[g.movie_id] = []
        d2[g.movie_id].append(g.g_id)

    res = []

    all_movies_t = []
    for m in all_movies:
        if label == -1:
            all_movies_t = all_movies
            break
        if label in d2[m.movie_id]:
            all_movies_t.append(m)


    for m in all_movies_t[page * 12: (page + 1) * 12]:
        res.append({"name": m.movie_name, "id": m.movie_id, "poster": "", "genres": list(map(lambda x: d1[x], d2[m.movie_id]))})
    return {"data": {"movies": res, "total": len(all_movies_t)}, "status": 200, "message": ""}


if __name__ == '__main__':
    app.run(port=8848)
