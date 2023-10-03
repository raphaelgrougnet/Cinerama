import os
import re
import hashlib
import dotenv
from datetime import datetime
from profil import bp_profil
from flask import Flask, render_template, session, request, redirect, url_for
from flask_pymongo import PyMongo


if not os.getenv('CONNEXION_BD'):
    dotenv.load_dotenv(".env")

app = Flask(__name__)
app.register_blueprint(bp_profil, url_prefix='/profil')
app.config['MONGO_URI'] = os.getenv('CONNEXION_BD')

app.secret_key = os.getenv('SECRET_KEY')

mongo = PyMongo(app)


def hacher_mdp(mdp_en_clair):
    """Prend un mot de passe en clair et lui applique une fonction de hachage"""
    return hashlib.sha512(mdp_en_clair.encode()).hexdigest()


@app.route('/')
def index():
    films = list(mongo.db.films.find().sort('Released', -1))
    for film in films:
        date = film["Released"]
        film["Released"] = date.strftime("%d-%m-%Y")
    return render_template('index.html', utilisateur=session.get("utilisateur"), films=films)


@app.route('/login', methods=['GET', 'POST'])
def login():
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
                                   value_username=username)

        passwordHashed = hacher_mdp(password)
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
            "visionnes" : utilisateur_trouve["visionnes"],
            "favoris" : utilisateur_trouve["favoris"],
            "commentaires" : utilisateur_trouve["commentaires"],
            "is_admin" : utilisateur_trouve["is_admin"],
            "is_premium" : utilisateur_trouve["is_premium"]
        }

        session.permanent = True
        session["utilisateur"] = user
        return redirect(url_for('index'), 303)

        
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
    return redirect(url_for('index'))
