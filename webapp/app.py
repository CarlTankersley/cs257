import flask
import json
import psycopg2
import argparse
from config import database, user, password

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=str, help="host on which to run the service")
    parser.add_argument("port", type=int, help="port on which the service is listening")
    args = parser.parse_args()
    return args

def setup_db_connection():
    

def main():
    args = parse_args()
    connection, cursor = setup_db_connection()
    app.run(host=args.host, port=args.port, debug=True)


    
if __name__ == '__main__':
    app = flask.Flask(__name__)
    main()