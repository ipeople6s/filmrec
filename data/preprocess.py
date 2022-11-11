from os import listdir
import urllib.request
import pandas as pd
import requests
import base64
import time
# pip3 install cinemagoer
from imdb import Cinemagoer
import sqlite3

def get_base64(url):
    return "data:image/png;base64," + str(base64.b64encode(requests.get(url).content), encoding = "utf-8")

def get_url(movie_title, num=0):
    if num == 4:
        print(movie_title)
        return None
    imdb = Cinemagoer()
    movies = imdb.search_movie(movie_title)
    if len(movies) == 0:
        return get_url(movie_title, num + 1)
    movie = movies[0]
    cover_url = movie.get("full-size cover url", "").strip()
    return cover_url

def download_poster(url, movie_id):
    if url == None:
        return
    if url == "https://m.media-amazon.png":
        return
    filename = './data/posters/' + movie_id + '.jpg'
    with urllib.request.urlopen(url) as response:
        with open(filename, 'wb') as out_image:
            out_image.write(response.read())

'''
get posters
'''
def get_posters(start=0):
    cols = ["movie_id", "title", "genres"]
    df = pd.read_table("./data/ml-1m/movies.dat", sep="::", header=None, names=cols, encoding="utf-8")

    itr = 0
    for row in df.itertuples():
        itr += 1

        if itr < start:
            continue

        if str(row[1]) + ".jpg" in listdir("./data/posters/"):
            continue
        url = get_url(row[2])
        print(row[2], url)
        download_poster(url, str(row[1]))
        time.sleep(0.6)
    return


def insert_movies():
    conn = sqlite3.connect('./data.db')
    cols = ["movie_id", "title", "genres"]
    df = pd.read_table("./data/ml-1m/movies.dat", sep="::", header=None, names=cols, encoding="utf-8")
    for row in df.itertuples():
        conn.execute("INSERT INTO tb_movie (movie_id,movie_name) VALUES (?, ?)", (row[1], row[2]))
    conn.commit()
    conn.close()

def insert_genres():
    d = dict()
    d["Action"] = 0
    d["Adventure"] = 1
    d["Animation"] = 2
    d["Children's"] = 3
    d["Comedy"] = 4
    d["Crime"] = 5
    d["Documentary"] = 6
    d["Drama"] = 7
    d["Fantasy"] = 8
    d["Film-Noir"] = 9
    d["Horror"] = 10
    d["Musical"] = 11
    d["Mystery"] = 12
    d["Romance"] = 13
    d["Sci-Fi"] = 14
    d["Thriller"] = 15
    d["War"] = 16
    d["Western"] = 17

    conn = sqlite3.connect('./data.db')
    for k, v in d.items():
        conn.execute("INSERT INTO tb_genres (g_id,g_name) VALUES (?, ?)", (v, k))
    conn.commit()

    cols = ["movie_id", "title", "genres"]
    df = pd.read_table("./data/ml-1m/movies.dat", sep="::", header=None, names=cols, encoding="utf-8")
    for row in df.itertuples():
        genres = row[3].split("|")
        for g in genres:
            conn.execute("INSERT INTO tb_movie_genres (movie_id,g_id) VALUES (?, ?)", (row[1], d[g]))
    conn.commit()
    conn.close()

'''
Different posters come in different sizes
'''
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
def resize_img():
    from PIL import Image
    for f in listdir("./filmrecb/static/"):
        img = Image.open("./filmrecb/static/" + f)
        # print(img.size)
        img = img.resize((500, 750))
        img.save("./filmrecb/static/" + f)

resize_img()
# get_posters(2000)

# insert_data()