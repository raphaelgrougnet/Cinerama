from flask_pymongo import PyMongo
from flask import Flask
import os
app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('CONNEXION_BD')
mongo = PyMongo(app)
