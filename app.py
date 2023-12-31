import os
import re
import hashlib
import dotenv
from datetime import *
from profil import bp_profil
from film import bp_film
from films import bp_films
from api import bp_api
from bson.objectid import ObjectId
from flask import Flask, render_template, session, request, redirect, url_for, make_response
from flask_pymongo import PyMongo


if not os.getenv('CONNEXION_BD'):
    dotenv.load_dotenv(".env")

app = Flask(__name__)
app.register_blueprint(bp_profil, url_prefix='/profil')
app.register_blueprint(bp_film, url_prefix='/film')
app.register_blueprint(bp_films, url_prefix='/films')
app.register_blueprint(bp_api, url_prefix='/api' )
app.config['MONGO_URI'] = os.getenv('CONNEXION_BD')

app.secret_key = os.getenv('SECRET_KEY')

mongo = PyMongo(app)


def hacher_mdp(mdp_en_clair):
    """Prend un mot de passe en clair et lui applique une fonction de hachage"""
    return hashlib.sha512(mdp_en_clair.encode()).hexdigest()


@app.route('/')
def index():
    films = list(mongo.db.films.find().sort('Released', -1).limit(15))
    films_notes = list(mongo.db.films.find().sort('Metascore', -1).limit(15))
    for film in films:
        date = film["Released"]
        id = str(film["_id"])
        film["_id"] = id
        film["Released"] = date.strftime("%d-%m-%Y")
        film["Metascore"] = int(film["Metascore"])

    for film in films_notes:
        date = film["Released"]
        id = str(film["_id"])
        film["_id"] = id
        film["Released"] = date.strftime("%d-%m-%Y")
        film["Metascore"] = int(film["Metascore"])


    
    resp = make_response(render_template('index.html', utilisateur=session.get("utilisateur"), films=films, films_notes=films_notes, introPlayed=request.cookies.get('introPlayed'), class_connexion_succes=request.cookies.get('newLoggin'), class_deconnexion_succes=request.cookies.get('newLoggout')))
    resp.set_cookie('introPlayed', "True")
    resp.set_cookie('newLoggin', 'hide')
    resp.set_cookie('newLoggout', 'hide')
    return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
    regex_email = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if session.get("utilisateur"):
        return redirect(url_for('index'), 303)
    if request.method == 'POST':

        classe_erreur_username = ""
        classe_erreur_password = ""

        username = request.form.get('username', default='')
        username = username.lower()
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
                                   value_username=username,
                                   utilisateur=None)

        passwordHashed = hacher_mdp(password)
        if re.match(regex_email, username):
            utilisateur_trouve = mongo.db.users.find_one(
                {"email": username, "password": passwordHashed})
        else:
            utilisateur_trouve = mongo.db.users.find_one(
                {"username": username, "password": passwordHashed})
        

        if not utilisateur_trouve:
            return render_template('login.html', utilisateur = None)
        user = {
            "_id": str(utilisateur_trouve["_id"]),
            "first": utilisateur_trouve["first"],
            "last": utilisateur_trouve["last"],
            "email": utilisateur_trouve["email"],
            "username": utilisateur_trouve["username"],
            "pfp" : utilisateur_trouve["pfp"],
            "karma" : utilisateur_trouve["karma"],
            "visionnes" : list(),
            "favoris" : list(),
            "commentaires" : list(),
            "is_admin" : utilisateur_trouve["is_admin"],
            "is_premium" : utilisateur_trouve["is_premium"]
        }

        for i in range(len(utilisateur_trouve["visionnes"])):
            utilisateur_trouve["visionnes"][i] = str(ObjectId(utilisateur_trouve["visionnes"][i]['id_film']))

        for i in range(len(utilisateur_trouve["favoris"])):
            utilisateur_trouve["favoris"][i] = str(ObjectId(utilisateur_trouve["favoris"][i]))
        
        for i in range(len(utilisateur_trouve["commentaires"])):
            utilisateur_trouve["commentaires"][i] = str(ObjectId(utilisateur_trouve["commentaires"][i]))

        print(utilisateur_trouve["commentaires"])

        session.permanent = True
        session["utilisateur"] = user
        resp = make_response(redirect(url_for('index'), 303))
        resp.set_cookie('newLoggin', 'show')
        return resp

        
    return render_template('login.html', class_erreur_login="visually-hidden", utilisateur=session.get("utilisateur"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    regex_email = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    regex_password = "^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    if request.method == 'POST':

        first_name = request.form.get('first_name', default='')
        last_name = request.form.get('last_name', default='')
        username = request.form.get('username', default='')
        username = username.lower()
        email = request.form.get('email', default='')
        password1 = request.form.get('password1', default='')
        password2 = request.form.get('password2', default='')

        value_champs = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
        }
        contenu_erreur = {
            "first_name": "Le prénom est obligatoire",
            "last_name": "Le nom est obligatoire",
            "username": "Le nom d'utilisateur est obligatoire",
            "email": "L'adresse courriel est obligatoire",
            "password1": "Le mot de passe est obligatoire",
            "password2": "La confirmation du mot de passe est obligatoire",
        }
        classe_erreur = {
            "first_name": "is-valid",
            "last_name": "is-valid",
            "username": "is-valid",
            "email": "is-valid",
            "password1": "is-valid",
            "password2": "is-valid",
        }

        utilisateur_existant = mongo.db.users.find_one(
            {"username": username}, {"_id": 0})
        
        email_existant = mongo.db.users.find_one(
            {"email": email}, {"_id": 0})
        

        if not first_name:
            classe_erreur["first_name"] = "is-invalid"
        if not last_name:
            classe_erreur["last_name"] = "is-invalid"
        if not username:
            classe_erreur["username"] = "is-invalid"
        elif utilisateur_existant:
            classe_erreur["username"] = "is-invalid"
            contenu_erreur["username"] = "Le nom d'utilisateur est déjà utilisé"
        if not email:
            classe_erreur["email"] = "is-invalid"
        elif not re.match(regex_email, email):
            classe_erreur["email"] = "is-invalid"
            contenu_erreur["email"] = "L'adresse courriel n'est pas valide"
        elif email_existant:
            classe_erreur["email"] = "is-invalid"
            contenu_erreur["email"] = "L'adresse courriel est déjà utilisée"

        if not password1:
            classe_erreur["password1"] = "is-invalid"
        elif not re.match(regex_password, password1):
            classe_erreur["password1"] = "is-invalid"
            contenu_erreur["password1"] = "Le mot de passe doit contenir au moins 8 caractères, une majuscule, un chiffre et un caractère spécial"
            
        if not password2:
            classe_erreur["password2"] = "is-invalid"
        elif not re.match(regex_password, password2):
            classe_erreur["password2"] = "is-invalid"
            contenu_erreur["password2"] = "Le mot de passe doit contenir au moins 8 caractères, une majuscule, un chiffre et un caractère spécial"

        if password1 != password2:
            classe_erreur["password1"] = "is-invalid"
            classe_erreur["password2"] = "is-invalid"
            contenu_erreur["password2"] = "Les mots de passe ne sont pas identiques"

        if classe_erreur["first_name"] == "is-invalid" or classe_erreur["last_name"] == "is-invalid" or classe_erreur["username"] == "is-invalid" or classe_erreur["email"] == "is-invalid" or classe_erreur["password1"] == "is-invalid" or classe_erreur["password2"] == "is-invalid":
            return render_template('register.html',
                                   classe_erreur=classe_erreur,
                                   value_champs=value_champs,
                                   contenu_erreur=contenu_erreur,
                                   utilisateur= session.get("utilisateur"))
        
        passwordHashed = hacher_mdp(password1)
        nouvel_utilisateur = {
            "first": first_name,
            "last": last_name,
            "email": email,
            "username": username,
            "password": passwordHashed,
            "pfp" : "/static/images/profils/default_pfp.jpg",
            "karma" : 0,
            "visionnes" : [],
            "favoris" : [],
            "commentaires" : [],
            "is_admin" : False,
            "is_premium" : False
        }
        mongo.db.users.insert_one(nouvel_utilisateur)
        nouvel_utilisateur = mongo.db.users.find_one({"username": username, "password" : passwordHashed})
        user = {
            "_id": str(nouvel_utilisateur["_id"]),
            "first": nouvel_utilisateur["first"],
            "last": nouvel_utilisateur["last"],
            "email": nouvel_utilisateur["email"],
            "username": nouvel_utilisateur["username"],
            "pfp" : nouvel_utilisateur["pfp"],
            "karma" : nouvel_utilisateur["karma"],
            "visionnes" : nouvel_utilisateur["visionnes"],
            "favoris" : nouvel_utilisateur["favoris"],
            "commentaires" : nouvel_utilisateur["commentaires"],
            "is_admin" : nouvel_utilisateur["is_admin"],
            "is_premium" : nouvel_utilisateur["is_premium"]
        }
        session.permanent = True
        session["utilisateur"] = user
        return redirect(url_for('index'), 303)
    
    return render_template('register.html',
                           classe_erreur=None,
                           value_champs=None,
                           contenu_erreur=None,
                           utilisateur = session.get("utilisateur"))


@app.route('/logout')
def logout():
    session.clear()
    resp = make_response(redirect(url_for('index'), 303))
    resp.set_cookie('newLoggout', 'show')
    return resp

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', utilisateur=session.get("utilisateur")), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', utilisateur=session.get("utilisateur")), 500

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html', utilisateur=session.get("utilisateur")), 403

