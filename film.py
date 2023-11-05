from flask import redirect, render_template, request, session, Blueprint, abort, current_app as app
from bd import mongo
from bson.objectid import ObjectId
bp_film = Blueprint('film', __name__)

@bp_film.route('/<id>')
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

    return render_template('film/film.html', 
                           utilisateur=utilisateur, 
                           film=film,
                           commentaires=commentaires,)