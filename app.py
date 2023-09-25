"""
Démonstration des paramètres obligatoires
"""
import os

import dotenv
from flask import Flask, render_template, session, request, redirect, url_for
import hashlib

if not os.getenv('BD_UTILISATEUR'):
    dotenv.load_dotenv(".env")

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

def hacher_mdp(mdp_en_clair):
    """Prend un mot de passe en clair et lui applique une fonction de hachage"""
    return hashlib.sha512(mdp_en_clair.encode()).hexdigest()

@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user = user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        classe_erreur_username = ""
        classe_erreur_password = ""

        username = request.form.get('username', default='')
        password = request.form.get('password', default='')

        if not username:
            classe_erreur_username = "is-invalid"
        if not password:
            classe_erreur_password = "is-invalid"
        
        if classe_erreur_username or classe_erreur_password:
            return render_template('login.html',
                                   classe_erreur_username=classe_erreur_username,
                                   classe_erreur_password=classe_erreur_password, 
                                   class_erreur_login="visually-hidden",
                                   value_username=username)

        passwordHashed = hacher_mdp(password)
        # utilisateur_trouve = bd.get_compte(username, passwordHashed)
        utilisateur_trouve = None
        if utilisateur_trouve:
            session.permanent = True
            session["utilisateur"] = utilisateur_trouve
            return redirect(url_for('index'), 303)

        if not utilisateur_trouve:
            return render_template('login.html')
    return render_template('login.html', class_erreur_login="visually-hidden")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form.get('user')
        if user:
            session['user'] = user
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))