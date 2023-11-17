from flask import Blueprint, current_app as app, jsonify, session, request, abort, redirect
from bd import mongo
from bson.objectid import ObjectId

bp_api = Blueprint('api', __name__)

@bp_api.route('/mettre-en-favoris/<id>')
def mettre_en_favoris(id):
    utilisateur = session.get("utilisateur")
    is_favoris = False
    if utilisateur is None:
        abort(401)
    
    user = mongo.db.users.find_one(
        {
            "_id": ObjectId(utilisateur['_id'])
        }
    )

    film = mongo.db.films.find_one({"_id": ObjectId(id)})

    if(film is None):
        abort(404)

    for id_film in user['favoris']:
        if id_film == id:
            is_favoris = True
            break
    
    if(is_favoris):
        mongo.db.users.update_one(
            {
                "_id": ObjectId(utilisateur['_id'])
            },
            {
                "$pull": {
                    "favoris": id
                }
            }
        )
        return jsonify({"message": "Le film a été retiré des favoris."})
    else:
        mongo.db.users.update_one(
            {
                "_id": ObjectId(utilisateur['_id'])
            },
            {
                "$push": {
                    "favoris": id
                }
            }
        )
        return jsonify({"message": "Le film a été ajouté aux favoris."})






