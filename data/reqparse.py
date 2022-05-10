import datetime

from flask_restful import reqparse, abort, Api, Resource

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('email', required=True)
parser.add_argument('hashed_password', required=True)
parser.add_argument('modifed_date', required=True)
