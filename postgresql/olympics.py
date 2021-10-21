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
# Avoids broken pipe errors when piping output into less, which is helpful when printing thousands of lines at a time
signal(SIGPIPE, SIG_DFL) 

def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--help", action='store_true')
    parser.add_argument("-a", "--athletes-from-noc", metavar='athletes', dest='athletes', nargs=1, type=str)
    parser.add_argument("-g", "--gold-medals", dest='gold', action='store_true')
    parser.add_argument("-m", "--medalists", nargs=1, type=str)
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
        result = query_medalists(cursor, args.medalists)
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

def query_medalists(cursor, noc):
    #Thank you to Dave Musicant, who helped me figure this monstrosity out
    query = '''SELECT DISTINCT athletes.name, Gold, Silver, Bronze, COALESCE(Gold, 0) + COALESCE(Silver, 0) + COALESCE(Bronze, 0) AS Total
               FROM teams, links, (athletes
               LEFT JOIN (SELECT links.athlete_id AS athlete_id, COUNT(links.medal_id) AS Bronze
                   FROM links, medals
                   WHERE medals.medal = 'Bronze'
                   AND links.medal_id = medals.id
                   GROUP BY links.athlete_id) bronze_count ON athletes.id = bronze_count.athlete_id
               LEFT JOIN (SELECT links.athlete_id AS athlete_id, COUNT(links.medal_id) AS Silver
                   FROM links, medals
                   WHERE medals.medal = 'Silver'
                   AND links.medal_id = medals.id
                   GROUP BY links.athlete_id) silver_count ON athletes.id = silver_count.athlete_id
               LEFT JOIN (SELECT links.athlete_id AS athlete_id, COUNT(links.medal_id) AS Gold
                   FROM links, medals
                   WHERE medals.medal = 'Gold'
                   AND links.medal_id = medals.id
                   GROUP BY links.athlete_id) gold_count ON athletes.id = gold_count.athlete_id)
               WHERE links.team_id = teams.id
               AND links.athlete_id = athletes.id
               AND teams.noc = %s
               ORDER BY Total DESC'''
    try:
        cursor.execute(query, noc)
    except Exception as e:
        print(e)
        exit()
    return cursor

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

def format_medalists(cursor):
    max_length = 0
    lines = []
    rows = []
    for row in cursor:
        rows.append(list(row))
        if len(row[0]) > max_length:
            max_length = len(row[0])
    lines.append('Athlete' + ' '*(max_length-7) + ' |  Gold  | Silver | Bronze | Total')
    lines.append('-'*max_length + '-+--------+--------+--------+-------')
    for row in rows:
        spaces = max_length - len(row[0])
        for elt in range(len(row)):
            row[elt] = row[elt] or 0
        gold_space = 1 if row[1] // 10 > 0 else 2
        # This ugly mess adds spaces so that everything lines up nicely in the output
        lines.append(row[0] + ' '*spaces + ' |   ' + str(row[1]) + ' '*gold_space + '  |   ' \
                     + str(row[2]) + '    |   ' + str(row[3]) + '    |   ' + str(row[4]))
    return lines

def print_help():
    with open('olympics-usage.txt') as help_file:
        print(help_file.read())

def print_rows(rows):
    for row in rows:
        print(row)

if __name__ == '__main__':
    main()
