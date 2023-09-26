from flask import redirect, render_template, request, session, Blueprint, abort, current_app as app
import bd

bp_profil = Blueprint('profil', __name__)


utilisateur = {
    "username": "user1",
    "email": "user1@example.com",
    "password": "password1",
    "first_name": "John",
    "last_name": "Doe",
    "is_admin": False,
    "is_premium": False,
    "karma": 535,

}

@bp_profil.route('/')
def profil():
    """
    Affiche le profil de l'utilisateur
    """
    #user = session.get("utilisateur")
    user = utilisateur
    if user is None:
        abort(404)
    return render_template('profil/profil.html', user=user)

@bp_profil.route('/favoris')
def favoris():
    """
    Affiche les favoris de l'utilisateur
    """
    #user = session.get("utilisateur")
    user = utilisateur
    if user is None:
        abort(404)
    return render_template('profil/profil_favoris.html', user=user)

@bp_profil.route('/visionne')
def visionne():
    """
    Affiche les vidéos visionnées de l'utilisateur
    """
    #user = session.get("utilisateur")
    user = utilisateur
    if user is None:
        abort(404)
    return render_template('profil/profil_visionne.html', user=user)