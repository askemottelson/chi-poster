from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship, relation, backref

from sqlalchemy_views import CreateView
from sqlalchemy.types import Date

from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.types import TIMESTAMP

Base = declarative_base()

class Venue(Base):
    __tablename__ = "venue"
    id = Column(Integer, primary_key=True)
    name = Column(String(500))


class Paper(Base):
    __tablename__ = "paper"
    id = Column(Integer, primary_key=True)
    abstract = Column(LONGTEXT)
    text = Column(LONGTEXT)
    clean_text = Column(LONGTEXT)
    title = Column(String(500))
    venue_id = Column(Integer, ForeignKey(Venue.id))
    DOI = Column(String(500))
    year = Column(Integer)

    paper_authors = relationship("PaperAuthor")


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)

    name = Column(String(200))
    affiliation = Column(String(200))


class PaperAuthor(Base):
    __tablename__ = "paper_author"
    id = Column(Integer, primary_key=True)

    author_id = Column(Integer, ForeignKey(Author.id))
    paper_id = Column(Integer, ForeignKey(Paper.id))
    rank = Column(Integer)

    author = relationship("Author")




