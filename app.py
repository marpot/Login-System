import hashlib

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("login.html")

def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('secret'))
    return render_template('login.html', error=error)

def validate(username, password):
    con = sqlite3.connect('static/user.db')
    completion = False
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Users")
        rows = cur.fetchall()
        for row in rows:
            dbUser = row[0]
            dbPass = row[1]
            if dbUser == username:
                completion = check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == hashlib.md5(user_password.encode()).hexdigest()


if __name__ == "__main__":
    app.run()

