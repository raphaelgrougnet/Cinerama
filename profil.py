import os
import re
import dotenv
from flask import Flask, redirect, render_template, request, session, Blueprint, abort, current_app as app
from bd import mongo
from bson.objectid import ObjectId

bp_profil = Blueprint('profil', __name__)



@bp_profil.route('/')
def profil():
    """
    Affiche le profil de l'utilisateur
    """
    utilisateur = session.get("utilisateur")
    
    if utilisateur is None:
        abort(404)
    
    user = mongo.db.users.find_one(
        {
            "_id": ObjectId(utilisateur['_id'])
        }
    )
    
    commentaires = list(mongo.db.commentaires.find(
        {
            "id_user": ObjectId(user['_id'])
        }
    ))

    for c in commentaires:
        film = mongo.db.films.find_one({"_id": ObjectId(c['id_film'])})
        c['nom_film'] = film['Title']
        date = c["date_post"]
        c["date_post"] = date.strftime("%d-%m-%Y")

        
    
    return render_template('profil/profil.html', utilisateur=utilisateur, commentaires=commentaires)

@bp_profil.route('/favoris')
def favoris():
    """
    Affiche les favoris de l'utilisateur
    """
    utilisateur = session.get("utilisateur")

    if utilisateur is None:
        abort(404)
    
    user = mongo.db.users.find_one({"_id": ObjectId(utilisateur['_id'])})
    id_film = user['favoris']
    films = []
    for id in id_film:
        films.append(mongo.db.films.find_one({"_id": ObjectId(id)}))
       
   

    return render_template('profil/profil_favoris.html', utilisateur=utilisateur, films=films)

@bp_profil.route('/visionne')
def visionne():
    """
    Affiche les vidéos visionnées de l'utilisateur
    """
    utilisateur = session.get("utilisateur")
    
    if utilisateur is None:
        abort(404)

    user = mongo.db.users.find_one({"_id": ObjectId(utilisateur['_id'])})
    visionnes = user['visionnes']

    sorted_vis = sorted(visionnes, key=lambda x: x["date_visionne"], reverse=True)
    films = []
    for v in sorted_vis:
        date = v["date_visionne"]
        v["date_visionne"] = date.strftime("%d-%m-%Y")
        film = mongo.db.films.find_one({"_id": ObjectId(v['id_film'])})
        film['date_visionne'] = v["date_visionne"]
        films.append(film)
    
    return render_template('profil/profil_visionne.html', utilisateur=utilisateur, films=films)