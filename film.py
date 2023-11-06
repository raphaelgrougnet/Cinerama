from flask import redirect, render_template, request, session, Blueprint, abort, current_app as app
from bd import mongo
from datetime import datetime
from bson.objectid import ObjectId
bp_film = Blueprint('film', __name__)

@bp_film.route('/<id>', methods=['GET', 'POST'])
def film(id):
    """
    Affiche le profil de l'utilisateur
    """
    
    utilisateur = session.get("utilisateur")

    film = mongo.db.films.find_one({"_id": ObjectId(id)})

    if film is None:
        abort(404)

    commentaires = list(mongo.db.commentaires.find({"id_film": ObjectId(id)}).sort("date_post", -1))
    for commentaire in commentaires:
        commentaire["date_post"] = commentaire["date_post"].strftime("%d/%m/%Y")
        commentaire["utilisateur"] = mongo.db.users.find_one({"_id": ObjectId(commentaire["id_user"])})

    film["Released"] = film["Released"].strftime("%d/%m/%Y")
    film["Metascore"] = int(film["Metascore"])

    if request.method == 'POST':
        if utilisateur is None:
            return redirect('/login')
        commentaire = request.form.get("commentaire").strip()
        if commentaire == "":
            return render_template('film/film.html',
                               utilisateur=utilisateur,
                               film=film,
                               commentaires=commentaires,
                               message_erreur="Vous devez saisir un commentaire de plus de 5 caractères.")
        id_user = ObjectId(utilisateur["_id"])
        id_film = ObjectId(id)
        date_post = datetime.now()
        commentaire_inséré = mongo.db.commentaires.insert_one({"description": commentaire,
                                        "id_user": id_user,
                                        "id_film": id_film,
                                        "date_post": date_post})
        mongo.db.films.update_one({"_id": ObjectId(id)}, {"$push": {"Commentaires": ObjectId(commentaire_inséré.inserted_id)}})
        mongo.db.users.update_one({"_id": ObjectId(id_user)}, {"$push": {"commentaires": ObjectId(commentaire_inséré.inserted_id)}})
        return redirect('/film/' + id)


    return render_template('film/film.html', 
                        utilisateur=utilisateur, 
                        film=film,
                        commentaires=commentaires)


def ajout_commentaire(id):
    """
    Ajoute un commentaire à un film
    """
    utilisateur = session.get("utilisateur")
    if utilisateur is None:
        return redirect('/login')
    commentaire = request.form.get("commentaire").strip()
    id_user = ObjectId(utilisateur["_id"])
    id_film = ObjectId(id)
    date_post = datetime.now()
    mongo.db.commentaires.insert_one({"description": commentaire,
                                      "id_user": id_user,
                                      "id_film": id_film,
                                      "date_post": date_post})