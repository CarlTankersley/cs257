'''
    olympics.py
    Carl Tankersley
    18 October 2021
    CS 257 - Software Design
'''

import psycopg2
import argparse
from config import database, user, password
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL) # avoids broken pipe errors when output is piped into less, as in olympics.sh

def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--help", action='store_true')
    parser.add_argument("-a", "--athletes-from-noc", metavar='athletes', dest='athletes', nargs=1, type=str)
    parser.add_argument("-g", "--gold-medals", dest='gold', action='store_true')
    parser.add_argument("-m", "--medalists", action='store_true')
    return parser.parse_args()

def main():
    connection, cursor = setup_db_connection()
    args = parse_args()
    if args.athletes:
        result = query_athletes(cursor, args.athletes)
        rows = format_athletes(result)
        print_rows(rows)
    elif args.gold:
        result = query_gold(cursor)
        rows = format_gold(result)
        print_rows(rows)
    elif args.medalists:
        result = query_medalists(cursor)
        rows = format_medalists(result)
        print_rows(rows)
    else:
        print_help()
    connection.close()

def setup_db_connection():
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
        cursor = connection.cursor()
    except Exception as e:
        print(e)
        exit()
    return connection, cursor

def query_athletes(cursor, noc):
    query = '''SELECT DISTINCT athletes.name 
               FROM athletes, teams, links
               WHERE teams.noc = %s
               AND links.team_id = teams.id
               AND links.athlete_id = athletes.id
               ORDER BY athletes.name'''
    try:
        cursor.execute(query, noc)
    except Exception as e:
        print(e)
        exit()
    return cursor

def query_gold(cursor):
    query = '''SELECT teams.noc, COUNT(DISTINCT (events.event, events.sport, games.year)) gold_medals
               FROM teams, medals, links, events, games
               WHERE medals.medal = 'Gold'
               AND links.medal_id = medals.id
               AND links.team_id = teams.id
               AND links.games_id = games.id
               AND links.event_id = events.id
               GROUP BY teams.noc
               ORDER BY gold_medals DESC'''
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()
    return cursor

def query_medalists(cursor):
    #TODO: Figure out what's going on with this
    
    query = '''SELECT some_shit FROM somewhere'''

def format_athletes(rows):
    rows_formatted = []
    for row in rows:
        rows_formatted.append(row[0])
    return rows_formatted

def format_gold(rows):
    rows_formatted = ['NOC | Gold Medals', '-----------------']
    for row in rows:
        row_string = row[0] + ' | ' + str(row[1])
        rows_formatted.append(row_string)
    return rows_formatted

def format_medalists(rows):
    #TODO: implement this once the query is figured out
    pass

def print_help():
    with open('olympics-usage.txt') as help_file:
        print(help_file.read())

def print_rows(rows):
    for row in rows:
        print(row)

if __name__ == '__main__':
    main()
