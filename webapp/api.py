'''Soren DeHaan and Carl Tankersley
   11/15/2021
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
    rand_int = random.randint(0, 100)
    query = '''SELECT main_speaker, title
               FROM event_speaker_talk
               WHERE id = %s'''
    connection, cursor = setup_db()
    cursor.execute(query, (str(rand_int),))
    speaker = {}
    for row in cursor:
        speaker = {'name': row[0], 'title': row[1]}
    cursor.close()
    connection.close()
    return json.dumps(speaker)


@api.route('/search_videos/')
def search_videos():
    fields = "id, name, description, duration, image"
    table = "talk_info"
    conditions = ""
    sort = "name"

    sort_argument = flask.request.args.get('sort')
    if sort_argument == 'duration':
        sort = sort_argument

    search_argument = flask.request.args.get('search')
    conditions += f"name LIKE '%{search_argument}%'"

    query = (f"SELECT {fields} "
             f"FROM {table} "
             f"WHERE {conditions}"
             f"ORDER BY {sort}")

    talk_list = []
    connection, cursor = setup_db()
    cursor.execute(query, tuple())
    for row in cursor:
        talk = {'id': row[0],
                'name': row[1],
                'description': row[2],
                'duration': row[3],
                'image': row[4]}
        talk_list.append(talk)
    cursor.close()
    connection.close()

    return json.dumps(talk_list)
