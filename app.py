"""
Démonstration des paramètres obligatoires
"""
import os

import dotenv
import bd
from profil import bp_profil
from flask import Flask, render_template, session, request

if not os.getenv('BD_UTILISATEUR'):
    dotenv.load_dotenv(".env")

app = Flask(__name__)

app.register_blueprint(bp_profil, url_prefix='/profil')

app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    print("Hello world")
    return render_template('index.html', accueil_active=True)
