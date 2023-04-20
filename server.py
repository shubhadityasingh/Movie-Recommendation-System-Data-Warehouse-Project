from flask import Flask, render_template, redirect, request, jsonify
import pickle
import pandas as pd
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import rec_sys


app = Flask(__name__)

movies_dict = pickle.load(open('model/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
current_user_id = -1

@app.route('/verify-login', methods=['GET', 'POST'])
def verify_login():
    print(request.form)
    email = request.form['email']
    password = request.form['password']

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="moviedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"""SELECT * FROM user WHERE email='{email}'""")
    userdetails = cursor.fetchall()[0]
    print(userdetails)
    mydb.close()

    if check_password_hash(userdetails[3], password) == True:
        current_user_id = userdetails[0]
        return jsonify({"status": True, "email": userdetails[2], "name": userdetails[1]})

    return jsonify({"status": False})


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fetch-recommendations', methods=['GET', 'POST'])
def fetchRecommendations():
    email = request.get_data().decode("utf-8")
    print(email)
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="moviedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"""SELECT * FROM user WHERE email='{email}'""")
    user_id = cursor.fetchall()[0][0]
    cursor.execute(f"""SELECT title FROM watched WHERE userid={user_id}""")
    movie_titles = cursor.fetchall()
    mydb.close()
    movies_list = []
    for i in movie_titles:
        movies_list.append(i[0])

    recommendations_list = rec_sys.recommendations(movies_list)
    return jsonify(recommendations_list)


@app.route('/watched')
def watched():
    return render_template('watched.html')

@app.route('/fetchwatchlist', methods=['GET', 'POST'])
def watchlist():
    email = request.get_data().decode("utf-8")
    print(email)
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="moviedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"""SELECT * FROM user WHERE email='{email}'""")
    user_id = cursor.fetchall()[0][0]
    cursor.execute(f"""SELECT title, movie_id FROM watched WHERE userid={user_id}""")
    movie_titles = cursor.fetchall()
    mydb.close()

    final_list = []
    for i in movie_titles:
        path = rec_sys.fetch_posters(i[1])
        final_list.append({"title": i[0], "path": path})
    return jsonify(final_list)


@app.route('/logout')
def logout():
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)