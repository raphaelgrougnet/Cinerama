"""
Démonstration des paramètres obligatoires
"""
import os

import dotenv
import bd
from flask import Flask, render_template, session, request

if not os.getenv('BD_UTILISATEUR'):
    dotenv.load_dotenv(".env")

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    print("Hello world")
    return render_template('base.jinja')
