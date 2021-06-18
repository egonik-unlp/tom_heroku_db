from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import click
from flask.cli import with_appcontext

import os
app = Flask(__name__)
api = Api(app)

# db_name="database.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(db_name)
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(db_name)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
# SQLALCHEMY_TRACK_MODIFICATIONS
db=SQLAlchemy(app)


@click.command(name='create_tables')
@with_appcontext
def create_tables():
	db.create_all()
	
app.cli.add_command(create_tables)
    
