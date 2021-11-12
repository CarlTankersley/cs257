'''Soren DeHaan and Carl Tankersley
   11/11/2021
   CS 257 - Software Design'''

import psycopg2
import flask
import random
import json
from config import database, user, password

api = flask.Blueprint('api', __name__)


def setup_db():
    try:
        connection = psycopg2.connect(
            database=database, user=user, password=password)
        cursor = connection.cursor()
    except Exception as e:
        print(e)
        exit()
    return connection, cursor


@api.route('/random/')
def get_random_speaker():
    rand_int = random.randint(0, 1000)
    query = '''SELECT main_speaker, title
               FROM event_speaker_talk
               WHERE id = %d'''
    cursor, connection = setup_db()
    cursor.execute(query, (rand_int,))
    speaker = {}
    for row in cursor:
        speaker = {'name': row[0], 'title': row[1]}
    cursor.close()
    connection.close()
    return json.dumps(speaker)
