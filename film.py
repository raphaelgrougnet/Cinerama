from flask import redirect, render_template, jsonify, request, session, Blueprint, abort, current_app as app
from bd import mongo
from datetime import datetime
from bson.objectid import ObjectId

bp_film = Blueprint('film', __name__)

@bp_film.route('/<id>', methods=['GET', 'POST'])
def film(id):
    """
    Affiche le profil de l'utilisateur
    """
    is_favoris = False
    is_visionne = False
    utilisateur = session.get("utilisateur")

    film = mongo.db.films.find_one({"_id": ObjectId(id)})

    if utilisateur is not None:
        user = mongo.db.users.find_one(
            {
                "_id": ObjectId(utilisateur['_id'])
            }
        )
    else:
        user = None

    if film is None:
        abort(404)

    if user is not None:
        for id_film in user['favoris']:
            if str(id_film) == str(id):
                is_favoris = True
                break
    else:
        is_favoris = False

    is_visionne = False
    if user is not None:
        for film_visionne in user['visionnes']:
            if str(film_visionne['id_film']) == str(id):
                is_visionne = True
                break
    else:
        is_visionne = False

    commentaires = list(mongo.db.commentaires.find({"id_film": ObjectId(id)}).sort("date_post", -1))
    for commentaire in commentaires:
        commentaire["date_post"] = commentaire["date_post"].strftime("%d/%m/%Y")
        commentaire["utilisateur"] = mongo.db.users.find_one({"_id": ObjectId(commentaire["id_user"])})
        commentaire["utilisateur"]["_id"] = str(commentaire["utilisateur"]["_id"])

    film["Released"] = film["Released"].strftime("%d/%m/%Y")
    film["Metascore"] = int(film["Metascore"])

    if request.method == 'POST':
        if "from2" in request.form:
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
        elif "form1" in request.form:
            utilisateur = session.get("utilisateur")
            if utilisateur is None or user is None:
                return redirect('/login')

            if(is_favoris):
                mongo.db.users.update_one(
                    {
                        "_id": ObjectId(utilisateur['_id'])
                    },
                    {
                        "$pull": {
                            "favoris": ObjectId(id)
                        }
                    }
                )
                return redirect('/film/' + id)
            else:
                mongo.db.users.update_one(
                    {
                        "_id": ObjectId(utilisateur['_id'])
                    },
                    {
                        "$push": {
                            "favoris": ObjectId(id)
                        }
                    }
                )
                return redirect('/film/' + id)
        elif "form3" in request.form:
            utilisateur = session.get("utilisateur")
            if utilisateur is None or user is None:
                return redirect('/login')

            if(is_visionne):
                mongo.db.users.update_one(
                    {
                        "_id": ObjectId(utilisateur['_id'])
                    },
                    {
                        "$pull": {
                            "visionnes": {
                                "id_film": ObjectId(id)
                            }
                        }
                    },                
                )       
                return redirect('/film/' + id)
            else:
                mongo.db.users.update_one(
                    {
                        "_id": ObjectId(utilisateur['_id'])
                    },
                    {
                        "$push": {
                            "visionnes": {
                                "id_film": ObjectId(id),
                                "date_visionne": datetime.now()
                            }
                        }
                    }
                )
                return redirect('/film/' + id)

            
        else:
            abort(404)

    return render_template('film/film.html', 
                        utilisateur=utilisateur, 
                        film=film,
                        commentaires=commentaires,
                        is_favoris=is_favoris,
                        is_visionne=is_visionne)


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
                                      "date_post": date_post,
                                      "isDeleted" : False})
    
@bp_film.route('/<string:idFilm>/commentaire/<string:idCommentaire>/supprimer', methods=['POST'])
def supprimer_commentaire(idFilm, idCommentaire):
    """
    Supprime un commentaire
    """
    utilisateur = session.get("utilisateur")
    if utilisateur is None:
        abort(401)
    commentaire = mongo.db.commentaires.find_one({"_id": ObjectId(idCommentaire)})
    if commentaire is None:
        abort(404)
    
    if commentaire["id_user"] == ObjectId(utilisateur["_id"]) or utilisateur["is_admin"]:
        mongo.db.commentaires.update_one({"_id": ObjectId(idCommentaire)}, {"$set": {"isDeleted": True}})
        mongo.db.films.update_one({"_id": ObjectId(idFilm)}, {"$pull": {"Commentaires": ObjectId(idCommentaire)}})
        mongo.db.users.update_one({"_id": ObjectId(utilisateur["_id"])}, {"$pull": {"commentaires": ObjectId(idCommentaire)}})
        return redirect('/film/' + idFilm)

    abort(401)
    
@bp_film.route('/<string:idFilm>/commentaire/<string:idCommentaire>/reactiver', methods=['POST'])
def reactiver_commentaire(idFilm, idCommentaire):
    """
    Supprime un commentaire
    """
    utilisateur = session.get("utilisateur")
    if utilisateur is None:
        abort(401)
    commentaire = mongo.db.commentaires.find_one({"_id": ObjectId(idCommentaire)})
    if commentaire is None:
        abort(404)
    
    if utilisateur["is_admin"]:
        mongo.db.commentaires.update_one({"_id": ObjectId(idCommentaire)}, {"$set": {"isDeleted": False}})
        mongo.db.films.update_one({"_id": ObjectId(idFilm)}, {"$pull": {"Commentaires": ObjectId(idCommentaire)}})
        mongo.db.users.update_one({"_id": ObjectId(utilisateur["_id"])}, {"$pull": {"commentaires": ObjectId(idCommentaire)}})
        return redirect('/film/' + idFilm)

    abort(401)