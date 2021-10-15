SELECT noc, country FROM teams ORDER BY noc;

SELECT DISTINCT athletes.name FROM athletes, teams, links
WHERE teams.country = 'Kenya'
AND links.team_id = teams.id
AND links.athlete_id = athletes.id;

SELECT games.year, games.city, events.sport, events.event, medals.medal
FROM athletes, games, events, medals, links
WHERE athletes.name LIKE 'Greg%Louganis'
AND links.athlete_id = athletes.id
AND links.games_id = games.id
AND links.event_id = events.id
AND links.medal_id = medals.id
AND medals.medal IS NOT NULL
ORDER BY games.year;

SELECT teams.noc, COUNT(DISTINCT (events.event, games.year)) gold_medals
FROM teams, medals, links, events, games
WHERE medals.medal = 'Gold'
AND links.medal_id = medals.id
AND links.team_id = teams.id
AND links.games_id = games.id
AND links.event_id = events.id
GROUP BY teams.noc
ORDER BY COUNT(medals.medal) DESC;
