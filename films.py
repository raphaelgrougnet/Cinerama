from flask import redirect, render_template, request, session, Blueprint, abort, current_app as app
from bd import mongo
from datetime import datetime
from bson.objectid import ObjectId
bp_films = Blueprint('films', __name__)

@bp_films.route('/', methods=['GET'])
def films():
    """
    Affiche la liste des films
    """
    recherche = request.args.get('recherche')
    chkName = request.args.get('name')
    chkDate = request.args.get('date')
    chkNote = request.args.get('note')
    utilisateur = session.get("utilisateur")
    query = {}
    sort = []
    if recherche:
        query["Title"] = {"$regex": recherche, "$options": "i"}
    if chkName:
        sort.append(("Title", 1))
    if chkDate:
        sort.append(("Released", -1))
    if chkNote:
        sort.append(("Metascore", -1))
    if not sort and not query:
        films = list(mongo.db.films.find())
    elif not sort:
        films = list(mongo.db.films.find(query))
    elif not query:
        films = list(mongo.db.films.find().sort(sort))
    else:
        films = list(mongo.db.films.find(query).sort(sort))
    for film in films:
        film['_id'] = str(film['_id'])
        film['Metascore'] = int(film['Metascore'])
    print
    return render_template('films/films.html', utilisateur=utilisateur, films=films)
