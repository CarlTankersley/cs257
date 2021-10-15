'''
    Carl Tankersley
    14 Oct 2021
    CS 257 - Software Design
    
    This is some seriously ugly code, but it's going to run exactly once, so I don't care
'''

import csv
from os import terminal_size

with open("archive/athlete_events.csv") as athlete_events:
    file = csv.reader(athlete_events)
    athletes_found = set()
    games_found = set()
    events_found = set()
    medals_found = set()
    athletes_rows = []
    games_rows = []
    events_rows = []
    medals_rows = []
    for line in file:
        if line[1] not in athletes_found:
            athletes_rows.append([line[1], line[2], line[4], line[5]])
            athletes_found.add(line[0])
        if line[8] not in games_found:
            games_rows.append([line[9], line[10], line[11]])
            games_found.add(line[8])
        if line[13] not in events_found:
            sport_length = len(line[12]) + 1
            events_rows.append([line[12], line[13][sport_length:]])
            events_found.add(line[13])
        if line[14] not in medals_found:
            medals_rows.append(line[14])
            medals_found.add(line[14])

with open("archive/noc_regions.csv") as team_info:
    file = csv.reader(team_info)
    teams_found = set()
    countries_found = set()
    teams_rows = []
    for line in file:
        if line[0] not in teams_found or line[1] not in countries_found:
            teams_rows.append([line[0], line[1]])
            teams_found.add(line[0])
            countries_found.add(line[1])

with open("data/athletes.csv", 'w') as file:
    writer = csv.writer(file)
    id = 0
    for row in athletes_rows:
        if row == athletes_rows[0]: # ignore column headers
            continue
        writer.writerow([id] + row)
        id += 1


with open("data/games.csv", 'w') as file:
    writer = csv.writer(file)
    id = 0
    for row in games_rows:
        if row == games_rows[0]:
            continue
        writer.writerow([id] + row)
        id += 1

with open("data/events.csv", 'w') as file:
    writer = csv.writer(file)
    id = 0
    for row in events_rows:
        if row == events_rows[0]:
            continue
        writer.writerow([id] + row)
        id += 1

with open("data/medals.csv", 'w') as file:
    writer = csv.writer(file)
    id = 0
    for row in medals_rows:
        if row == medals_rows[0]:
            continue
        writer.writerow([id] + [row])
        id += 1

with open("data/teams.csv", 'w') as file:
    writer = csv.writer(file)
    id = 0
    for row in teams_rows:
        if row == teams_rows[0]:
            continue
        writer.writerow([id] + row)
        id += 1

# Making dictionaries with keys being fields from the csv, and values being the corresponding ID
with open("data/athletes.csv") as athletes:
    athletes_dict = {}
    file = csv.reader(athletes)
    for line in file:
        if line[1] not in athletes_dict.keys():
            athletes_dict[line[1]] = line[0]

with open("data/events.csv") as events:
    events_dict = {}
    file = csv.reader(events)
    for line in file:
        if line[1] + ' ' + line[2] not in events_dict.keys():
            events_dict[line[1] + ' ' + line[2]] = line[0]

with open("data/games.csv") as games:
    games_dict = {}
    file = csv.reader(games)
    for line in file:
        if (line[1] + ' ' + line[2]) not in games_dict.keys():
            games_dict[line[1] + ' ' + line[2]] = line[0]

with open("data/medals.csv") as medals:
    medals_dict = {}
    file = csv.reader(medals)
    for line in file:
        if line[1] not in medals_dict.keys():
            medals_dict[line[1]] = line[0]

with open("data/teams.csv") as teams:
    teams_dict = {}
    file = csv.reader(teams)
    for line in file:
        if line[1] not in teams_dict.keys():
            teams_dict[line[1]] = line[0]

# Make linking table csv file
with open("archive/athlete_events.csv") as source_file, open("data/links.csv", 'w') as destination_file:
    reader = csv.reader(source_file)
    writer = csv.writer(destination_file)
    for line in reader:
        if line[0] == 'ID': # Ignore column headers
            continue
        athlete_id = athletes_dict[line[1]]
        event_id = events_dict[line[13]]
        games_id = games_dict[line[8]]
        medals_id = medals_dict[line[14]]
        teams_id = teams_dict[line[7]]
        writer.writerow([athlete_id, event_id, games_id, medals_id, teams_id])
