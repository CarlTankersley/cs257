'''
    olympics-api.py
    Carl Tankersley and Soren DeHaan
    28 October 2021
    CS 257 - Software Design
'''

import argparse
import flask
import psycopg2
import json
from config import database, user, password

class OlympicsApp:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                database=database, user=user, password=password)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(e)
            exit()

flask_app = flask.Flask(__name__)
olympics_app = OlympicsApp()

def parse_args():
    parser = argparse.ArgumentParser('Flask API to query the Olympics database')
    parser.add_argument('host', help='the host on which the app is running')
    parser.add_argument('port', type=int, help='the port on which the app is listening')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    flask_app.run(host=args.host, port=args.port, debug=True)

@flask_app.route('/medalists/games/<games_id>')
def get_athletes(games_id):
    query = '''SELECT athletes.id, athletes.name, athletes.sex, events.sport, events.event, medals.medal, teams.noc
               FROM athletes, events, medals, games, links, teams
               WHERE games.id = %s
               AND links.athlete_id = athletes.id
               AND links.event_id = events.id
               AND links.medal_id = medals.id
               AND links.games_id = games.id
               AND links.team_id = teams.id
               AND medals.medal IS NOT NULL'''
    try:
        olympics_app.cursor.execute(query, (games_id,))
    except Exception as e:
        print(e)
        exit()
    athletes_list = []
    for athlete in olympics_app.cursor:
        noc = flask.request.args.get('noc')
        if noc and noc != athlete[6]:
            continue
        athlete_dict = {}
        athlete_dict['athlete_id'] = athlete[0]
        athlete_dict['athlete_name'] = athlete[1]
        athlete_dict['athlete_sex'] = athlete[2]
        athlete_dict['sport'] = athlete[3]
        athlete_dict['event'] = athlete[4]
        athlete_dict['medal'] = athlete[5]
        athletes_list.append(athlete_dict)
    return json.dumps(athletes_list)

@flask_app.route('/nocs')
def get_nocs():
    query = 'SELECT noc, country FROM teams ORDER BY noc'
    try:
        olympics_app.cursor.execute(query)
    except Exception as e:
        print(e)
        exit()
    noc_list = []
    for noc in olympics_app.cursor:
        noc_dict = {}
        noc_dict['abbreviation'] = noc[0]
        noc_dict['name'] = noc[1]
        noc_list.append(noc_dict)
    return json.dumps(noc_list)

@flask_app.route('/games')
def get_games():
    # TODO: make giant comment
    query = 'SELECT * FROM games'
    try:
        olympics_app.cursor.execute(query)
    except Exception as e:
        print(e)
        exit()
    games_list = []
    for game in olympics_app.cursor:
        game_dict = {}
        game_dict['id'] = game[0]
        game_dict['year'] = game[1]
        game_dict['season'] = game[2]
        game_dict['city'] = game[3]
        games_list.append(game_dict)
    return json.dumps(games_list)

if __name__ == '__main__':
    main()
