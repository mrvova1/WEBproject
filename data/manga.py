import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Manga(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Manga'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Release_year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    Title_status = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    Translation_status = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    Author = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Artist = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Interpritator_team = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Number_of_chapters = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Oblojka = sqlalchemy.Column(sqlalchemy.BLOB)

    def __repr__(self):
        return f'<Team> {self.name}'
