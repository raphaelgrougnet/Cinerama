"""
Connexion à la BD
"""
import dotenv
import os
import contextlib
import types

import mysql.connector


@contextlib.contextmanager
def creer_connexion():
    """Pour créer une connexion à la BD"""
    conn = mysql.connector.connect(
        user=os.getenv("BD_UTILISATEUR"),
        password=os.getenv("BD_MOT_DE_PASSE"),
        host=os.getenv("BD_HOST"),
        database=os.getenv("BD_NOM"),
        raise_on_warnings=True
    )

    # Pour ajouter la méthode get_curseur() à l'objet connexion
    conn.get_curseur = types.MethodType(get_curseur, conn)

    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()


@contextlib.contextmanager
def get_curseur(self):
    """Permet d'avoir les enregistrements sous forme de dictionnaires"""
    curseur = self.cursor(dictionary=True)
    try:
        yield curseur
    finally:
        curseur.close()
