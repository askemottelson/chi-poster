from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists
from sqlalchemy import create_engine
import os

basedir = os.path.abspath(os.path.dirname(__file__))

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)


mysqlstr = 'mysql+mysqlconnector://bodyui:avbib1947al@130.225.99.29/HCI?charset=utf8'


engine = create_engine(mysqlstr, echo=False)

Base = declarative_base()

# Create the database if it does not exists:
#if not database_exists(engine.url):
# from models import *
# Base.metadata.create_all(engine)
#engine.execute("SET NAMES 'utf8';")
#engine.execute("SET CHARACTER SET utf8;")

# Create a database session
Session = sessionmaker()
Session.configure(bind=engine)

db = Session()


def create_session():
	engine = create_engine(mysqlstr)
	Session = sessionmaker(bind=engine)
	session = Session()
	session._model_changes = {}
	return session