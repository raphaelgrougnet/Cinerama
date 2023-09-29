from flask import redirect, render_template, request, session, Blueprint, abort, current_app as app

bp_profil = Blueprint('profil', __name__)



@bp_profil.route('/')
def profil():
    """
    Affiche le profil de l'utilisateur
    """
    utilisateur = session.get("utilisateur")

    if utilisateur is None:
        abort(404)
    return render_template('profil/profil.html', utilisateur=utilisateur)

@bp_profil.route('/favoris')
def favoris():
    """
    Affiche les favoris de l'utilisateur
    """
    utilisateur = session.get("utilisateur")

    if utilisateur is None:
        abort(404)
    return render_template('profil/profil_favoris.html', utilisateur=utilisateur)

@bp_profil.route('/visionne')
def visionne():
    """
    Affiche les vidéos visionnées de l'utilisateur
    """
    utilisateur = session.get("utilisateur")
    if utilisateur is None:
        abort(404)
    return render_template('profil/profil_visionne.html', utilisateur=utilisateur)