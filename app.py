from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json
import random

app = Flask(__name__)

# Load recipes
with open('recipes.json') as f:
    RECIPES = json.load(f)


# LOGIN PAGE
@app.route('/')
def home():
    return render_template('login.html')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            # ✅ IMPORTANT FIX HERE
            return redirect(url_for('home_page'))
        else:
            return render_template('login.html', error="Invalid email or password")

    return render_template('login.html')


# SIGNUP
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                  (name, email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template('signup.html')


# HOME PAGE
@app.route('/home')
def home_page():
    return render_template('home.html')


# MOOD PAGE
@app.route('/mood')
def mood():
    return render_template('mood.html')


# DETECT PAGE
@app.route('/detect')
def detect():
    return render_template('detect.html')


# RECOMMEND RECIPE
@app.route('/recommend', methods=['POST'])
def recommend():
    mood = request.form.get('mood', '').lower()
    diet = request.form.get('diet', 'veg').lower()

    matched = [r for r in RECIPES if mood in r['mood'] and r['diet'] == diet]

    if not matched:
        matched = RECIPES

    recipe = random.choice(matched)

    return render_template('result.html', recipe=recipe, mood=mood)


# LOGOUT
@app.route('/logout')
def logout():
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)