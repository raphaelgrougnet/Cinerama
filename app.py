import os
import hashlib
import dotenv
from flask import Flask, render_template, session, request, redirect, url_for
from flask_pymongo import PyMongo

if not os.getenv('CONNEXION_BD'):
    dotenv.load_dotenv(".env")

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('CONNEXION_BD')
app.secret_key = os.getenv('SECRET_KEY')

mongo = PyMongo(app)

def hacher_mdp(mdp_en_clair):
    """Prend un mot de passe en clair et lui applique une fonction de hachage"""
    return hashlib.sha512(mdp_en_clair.encode()).hexdigest()

@app.route('/')
def index():
    return render_template('index.html', utilisateur = session.get("utilisateur"))


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
        utilisateur_trouve = mongo.db.users.find_one({"username": username, "password": passwordHashed})
        if utilisateur_trouve:
            user = {
                "id": str(utilisateur_trouve["_id"]),
                "username": utilisateur_trouve["username"],
                "first_name": utilisateur_trouve["first"],
                "last_name": utilisateur_trouve["last"],
                "email": utilisateur_trouve["email"],
                "pfp": utilisateur_trouve["large"],
            }
            session.permanent = True
            session["utilisateur"] = user
            return redirect(url_for('index'), 303)

        if not utilisateur_trouve:
            return render_template('login.html', utilisateur = session.get("utilisateur"))
    return render_template('login.html', class_erreur_login="visually-hidden", utilisateur = session.get("utilisateur"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name', default='')
        last_name = request.form.get('last_name', default='')
        username = request.form.get('username', default='')
        email = request.form.get('email', default='')
        password1 = request.form.get('password1', default='')
        password2 = request.form.get('password2', default='')

        classe_erreur_first_name = ""
        classe_erreur_last_name = ""
        classe_erreur_username = ""
        classe_erreur_email = ""
        classe_erreur_password1 = ""
        classe_erreur_password2 = ""

        if not first_name:
            classe_erreur_first_name = "is-invalid"
        if not last_name:
            classe_erreur_last_name = "is-invalid"
        if not username:
            classe_erreur_username = "is-invalid"
        if not email:
            classe_erreur_email = "is-invalid"
        if not password1:
            classe_erreur_password1 = "is-invalid"
        if not password2:
            classe_erreur_password2 = "is-invalid"
        if password1 != password2:
            classe_erreur_password1 = "is-invalid"
            classe_erreur_password2 = "is-invalid"

        if classe_erreur_first_name or classe_erreur_last_name or classe_erreur_username or classe_erreur_email or classe_erreur_password1 or classe_erreur_password2:
            return render_template('register.html',
                                   classe_erreur_first_name=classe_erreur_first_name if classe_erreur_first_name else "is-valid",
                                   classe_erreur_last_name=classe_erreur_last_name if classe_erreur_last_name else "is-valid",
                                   classe_erreur_username=classe_erreur_username if classe_erreur_username else "is-valid",
                                   classe_erreur_email=classe_erreur_email if classe_erreur_email else "is-valid",
                                   classe_erreur_password1=classe_erreur_password1 if classe_erreur_password1 else "is-valid",
                                   classe_erreur_password2=classe_erreur_password2 if classe_erreur_password2 else "is-valid",
                                   value_first_name=first_name if not classe_erreur_first_name else "",
                                   value_last_name=last_name if not classe_erreur_last_name else "",
                                   value_username=username if not classe_erreur_username else "",
                                   value_email=email if not classe_erreur_email else "",
                                   value_password1=password1 if not classe_erreur_password1 else "",
                                   value_password2=password2 if not classe_erreur_password2 else "")

        passwordHashed = hacher_mdp(password1)
        # utilisateur_trouve = bd.get_compte(username, passwordHashed)
        utilisateur_trouve = None
        if utilisateur_trouve:
            session.permanent = True
            session["utilisateur"] = utilisateur_trouve
            return redirect(url_for('index'), 303)

        if not utilisateur_trouve:
            return render_template('register.html')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))