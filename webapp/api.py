'''Soren DeHaan and Carl Tankersley
   11/15/2021
   CS 257 - Software Design'''

import psycopg2
import flask
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
    rand_query = '''SELECT id
               FROM event_speaker_talk
               ORDER BY RANDOM()
               LIMIT 1'''
    connection, cursor = setup_db()
    cursor.execute(rand_query, ())
    speaker = {}
    for row in cursor:
        speaker = {'id': row[0]}
        break
    cursor.close()
    connection.close()
    return get_video(speaker['id'])


@api.route('/search_videos/')
def search_videos():
    # print("searching")
    fields = "talk_info.id, talk_info.name, talk_info.description, talk_info.duration, talk_info.image"
    table = "talk_info"
    sort = "name"
    table_linkers = ""

    sort_argument = flask.request.args.get('sort')
    # print(sort_argument)
    if sort_argument == '"Name (A-Z)"':
        sort = 'name'
    elif sort_argument == '"Name (Z-A)"':
        sort = 'name DESC'
    elif sort_argument == '"Duration (low to high)"':
        sort = 'duration'
    elif sort_argument == '"Duration (high to low)"':
        sort = 'duration DESC'
    elif sort_argument == '"Rating: Beautiful"' or sort_argument == '"Rating: Confusing"' \
            or sort_argument == '"Rating: Courageous"' or sort_argument == '"Rating: Fascinating"' \
            or sort_argument == '"Rating: Funny"' or sort_argument == '"Rating: Informative"' \
            or sort_argument == '"Rating: Ingenious"' or sort_argument == '"Rating: Inspiring"' \
            or sort_argument == '"Rating: Jaw-Dropping"' or sort_argument == '"Rating: Longwinded"' \
            or sort_argument == '"Rating: Obnoxious"' or sort_argument == '"Rating: Ok"' \
            or sort_argument == '"Rating: Persuasive"' or sort_argument == '"Rating: Unconvincing"':
        table += ", ratings"
        table_linkers = "AND talk_info.id = ratings.id"
        sort = "ratings."
        sort += sort_argument[9:-1].lower().replace("-", "_") + " DESC"

    search_argument = flask.request.args.get('search')
    # print(search_argument)

    query = (f"SELECT {fields} "  # Note that fields, table, and sort are not user input
             f"FROM {table} "
             "WHERE name LIKE %s "
             f"{table_linkers} "
             f"ORDER BY {sort} "
             "LIMIT 100")
    print(query)
    talk_list = []
    connection, cursor = setup_db()
    if sort_argument == 'random':
        # print("jk, it's random")
        query = (f"SELECT {fields} "
                 f"FROM {table} "
                 "ORDER BY RANDOM()"
                 "LIMIT 1")
        cursor.execute(query, ())
    else:
        search_argument = '%' + search_argument + '%'
        cursor.execute(query, (search_argument,))
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


@api.route('/video/<talk_id>')
def get_video(talk_id):
    fields = "id, url, image, name, description, duration"
    table = "talk_info"

    search_argument = int(talk_id)
    print(search_argument)

    query = (f"SELECT {fields} "  # Note that fields, table, and sort are not user input
             f"FROM {table} "
             f"WHERE id = {search_argument} ")
    print(query)
    connection, cursor = setup_db()
    cursor.execute(query, (search_argument,))
    talk = {}
    for row in cursor:
        talk = {'id': row[0],
                'url': row[1],
                'image': row[2],
                'name': row[3],
                'description': row[4],
                'duration': row[5]}
        break
    cursor.close()
    connection.close()

    return json.dumps(talk)


@api.route('/help/')
def display_help():
    return flask.send_file('api_documentation.txt')
