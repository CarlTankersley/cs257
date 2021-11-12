'''Soren DeHaan and Carl Tankersley
   11/11/2021
   CS 257 - Software Design'''

import psycopg2
import flask
from config import database, user, password

api = flask.Blueprint('api', __name__)

def setup_db():
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
        cursor = connection.cursor()
    except Exception as e:
        print(e)
        exit()
    return connection, cursor
