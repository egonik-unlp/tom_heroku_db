import click
from flask.cli import with_appcontext

# from .extensions import db
# from .models import User, Question
from app import db
from database_management import Token
@click.command(name='create_tables')
@with_appcontext
def create_tables():
	db.create_all()
	
    
