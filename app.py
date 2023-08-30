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


# @app.errorhandler(404)
# def page_non_trouvee(error):
#     """Affiche la page d'erreur 404"""
#
#
#
# @app.errorhandler(500)
# def erreur_interne(error):
#
#
#
# @app.errorhandler(403)
# def erreur_compte(error):
#
#
#
# @app.errorhandler(400)
# def erreur_requete(error):
#
#
#
# @app.errorhandler(401)
# def erreur_non_autorise(error):

