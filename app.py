"""
Démonstration des paramètres obligatoires
"""
import os

import dotenv
import bd
from flask import Flask, render_template, session, request, redirect, url_for

if not os.getenv('BD_UTILISATEUR'):
    dotenv.load_dotenv(".env")

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user = user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        if user:
            session['user'] = user
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))