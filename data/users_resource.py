from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.users import User
from flask import jsonify, request
from data.reqparse import parser
import datetime

def abort_if_news_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")


class NewsResource(Resource):
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        news = session.query(User).get(user_id)
        return jsonify({'user': news.to_dict(
            only=('id', 'name', 'age', 'email', 'hashed_password', 'modifed_date'))})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        news = session.query(User).get(user_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class NewsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'name', 'age', 'email', 'hashed_password', 'modifed_date')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = User(
            id=args['id'],
            name=args['name'],
            age=args['age'],
            email=args['email'],
            hashed_password=args['hashed_password'],
            modifed_date=datetime.datetime.strptime(args['modifed_date'], '%Y-%m-%d %H:%M:%S.%f')
        )
        if session.query(User).get(args['id']) or session.query(User).get(args['id']):
            return jsonify({'error': 'Id already exists'})
        else:
            session.add(news)
            session.commit()
            return jsonify({'success': 'OK'})