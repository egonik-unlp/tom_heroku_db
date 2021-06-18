from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

db_name="database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(db_name)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
# SQLALCHEMY_TRACK_MODIFICATIONS
db=SQLAlchemy(app)