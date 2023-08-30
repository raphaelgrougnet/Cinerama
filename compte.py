import datetime
import hashlib
import re

from flask import redirect, render_template, request, session, Blueprint, current_app as app

import bd


def hacher_mdp(mdp_en_clair):
    """Prend un mot de passe en clair et lui applique une fonction de hachage"""
    return hashlib.sha512(mdp_en_clair.encode()).hexdigest()


