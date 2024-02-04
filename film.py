from flask import redirect, render_template, jsonify, request, session, Blueprint, abort, current_app as app
from bd import mongo
from form import FilmForm
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
        if 'user_liked' in commentaire and commentaire['user_liked']:
            for like in commentaire['user_liked']:
                if utilisateur is not None and str(like['id_user']) == str(utilisateur['_id']):
                    commentaire['is_critique'] = True
                    if like['is_like']:
                        commentaire['is_like'] = True
                    else:
                        commentaire['is_like'] = False
                else:
                    commentaire['is_critique'] = False
                    commentaire['is_like'] = None
                    
        


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
                                            "date_post": date_post,
                                            "isDeleted": False,
                                            "like_up": 0,
                                            "like_down": 0,
                                            "user_liked": []})
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
        elif "form4" in request.form:
            utilisateur = session.get("utilisateur")
            if utilisateur is None or user is None:
                return redirect('/login')
            
            id_com = request.form.get("id_commentaire")

            for com in commentaires:
                if str(com['_id']) == str(id_com):
                    lecom = com
                    break
            if lecom['user_liked']:
                if lecom['is_like']:
                    mongo.db.commentaires.update_one(
                        {
                            "_id": ObjectId(id_com)
                        },
                        {
                            "$inc": {
                                "like_up": -1
                            },
                            "$pull": {
                                "user_liked": {
                                    "id_user": ObjectId(utilisateur['_id'])
                                }
                            }
                        }
                    )
                    return redirect('/film/' + id)
                else:
                    mongo.db.commentaires.update_one(
                        {
                            "_id": ObjectId(id_com),
                            "user_liked.id_user": ObjectId(utilisateur['_id'])
                        },
                        {
                            "$set": {
                                "user_liked.$.is_like": True
                            },
                            "$inc": {
                                "like_up": 1,
                                "like_down": -1
                            }  
                        }
                    )

                    return redirect('/film/' + id)
            else:
                mongo.db.commentaires.update_one(
                    {
                        "_id": ObjectId(id_com)
                    },
                    {
                        "$inc": {
                            "like_up": 1
                        },
                        "$push": {
                            "user_liked": {
                                "id_user": ObjectId(utilisateur['_id']),
                                "is_like": True
                            }
                        }
                    }
                )
                return redirect('/film/' + id)
        elif "form5" in request.form:
            utilisateur = session.get("utilisateur")
            if utilisateur is None or user is None:
                return redirect('/login')
            
            id_com = request.form.get("id_commentaire")
            for com in commentaires:
                if str(com['_id']) == str(id_com):
                    lecom = com
                    break

            if lecom['user_liked']:
                if lecom['is_like'] == False:
                    mongo.db.commentaires.update_one(
                        {
                            "_id": ObjectId(id_com)
                        },
                        {
                            "$inc": {
                                "like_down": -1
                            },
                            "$pull": {
                                "user_liked": {
                                    "id_user": ObjectId(utilisateur['_id'])
                                }
                            }
                        }
                    )
                    return redirect('/film/' + id)
                else:
                    mongo.db.commentaires.update_one(
                        {
                            "_id": ObjectId(id_com),
                            "user_liked.id_user": ObjectId(utilisateur['_id'])
                        },
                        {
                            "$inc": {
                                "like_down": 1,
                                "like_up": -1
                            },
                            "$set": {
                                "user_liked.$.is_like": False
                            }
                        }
                    )

                    return redirect('/film/' + id)
            else:
                mongo.db.commentaires.update_one(
                    {
                        "_id": ObjectId(id_com)
                    },
                    {
                        "$inc": {
                                "like_down": 1,
                            },
                        "$push": {
                            "user_liked": {
                                "id_user": ObjectId(utilisateur['_id']),
                                "is_like": False
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
        mongo.db.users.update_one({"_id": ObjectId(utilisateur["_id"])}, {"$pull": {"commentaires": ObjectId(idCommentaire)}})
        return redirect('/film/' + idFilm)

    abort(401)


@bp_film.route('/ajout-film', methods=['GET', 'POST'])
def ajout():
    utilisateur = session.get("utilisateur")
    if utilisateur is None:
        return redirect('/login')
    if not utilisateur["is_admin"]:
        abort(401)
    form = FilmForm(request.form)
    if request.method == 'POST' and form.validate():
        titre = form.titre.data
        dateSortie = form.dateSortie.data
        annee = dateSortie.year
        dateSortie = datetime(dateSortie.year, dateSortie.month, dateSortie.day)
        #rated = form.rated.data
        duree = str(form.duree.data) + " min"
        realisateur = form.realisateur.data
        writers = form.writers.data
        acteurs = form.acteurs.data
        genres = form.genres.data
        synopsis = form.synopsis.data
        langue = form.langue.data
        pays = form.pays.data
        #typeFilm = form.typeFilm.data
        #reponse = form.reponse.data
        image = form.image.data
        #awards = form.awards.data
        metascore = str(form.metascore.data)
        #imdbRating = form.imdbRating.data
        #imdbVotes = form.imdbVotes.data
        #imdbID = form.imdbID.data

        result = mongo.db.films.insert_one({"Title": titre,
                                   "Year": str(annee),
                                   "Released": dateSortie,                      
                                   "Runtime": duree,
                                   "Director": realisateur,
                                   "Writer": writers,
                                   "Actors": acteurs,
                                   "Genre": genres,
                                   "Plot": synopsis,
                                   "Language": langue,
                                   "Country": pays,                                                                
                                   "Poster": image,
                                   "Metascore": metascore,})
        film_id = result.inserted_id
        
        return redirect('/film/' + str(film_id))
    
    return render_template('film/ajout.html', form=form, utilisateur=utilisateur)

