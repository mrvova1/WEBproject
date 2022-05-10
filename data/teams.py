import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Teams(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Interpritator_teams'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Line_up = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Permissions = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f'<Team> {self.name}'
