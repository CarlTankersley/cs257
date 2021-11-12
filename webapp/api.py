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
