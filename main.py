import psycopg2

conn_params = {
    "database": "postgres",
    "user": "postgres",
    "password": "secret",
    "host": "localhost",
    "port": "5433"
}


def execute_query(query):
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            if query.strip().upper().startswith("SELECT"):
                return cur.fetchall()
            conn.commit()


# 1. Выборка всех стадионов с их вместимостью, отсортированных по убыванию вместимости
print("1. Выборка всех стадионов с их вместимостью, отсортированных по убыванию вместимости")
stadiums_query = "SELECT name, capacity FROM UEFA.stadiums ORDER BY capacity DESC;"
stadiums = execute_query(stadiums_query)
print(stadiums)

print("2. Выборка игроков, играющих за определенную команду")
players_query = "SELECT first_name, last_name, team, position FROM UEFA.players WHERE team = 'FC Barcelona';"
players = execute_query(players_query)
print(players)

print("3. Выборка матчей с общим числом забитых голов больше 5")
matches_query = """
SELECT match_id, home_team, away_team, home_team_score, away_team_score, (home_team_score + away_team_score) as total_goals 
FROM UEFA.matches WHERE (home_team_score + away_team_score) > 5
ORDER BY total_goals DESC;
"""
matches = execute_query(matches_query)
print(matches)

print("4. Выборка для отображения домашних стадионов команд")
home_stadiums_query = """
SELECT t.team_name, t.home_stadium, s.city, s.capacity
FROM UEFA.teams t
JOIN UEFA.stadiums s ON t.home_stadium = s.name
ORDER BY t.team_name;
"""
home_stadiums = execute_query(home_stadiums_query)
print(home_stadiums)

print("5. Выборка тренеров с количеством игроков в их командах")
managers_query = """
SELECT m.first_name, m.last_name, m.team, COUNT(p.player_id) AS player_count
FROM UEFA.managers m
JOIN UEFA.players p ON m.team = p.team
WHERE m.team != ''
GROUP BY m.first_name, m.last_name, m.team
ORDER BY player_count DESC;
"""
managers = execute_query(managers_query)
print(managers)

print("6. Топ-10 игроков по количеству забитых голов")
top_scorers_query = """
SELECT p.first_name, p.last_name, p.team, CountGoals.total_goals
FROM UEFA.players p
JOIN (
  SELECT player_id, COUNT(goal_id) AS total_goals
  FROM UEFA.goals
  GROUP BY player_id
  ORDER BY total_goals DESC
  LIMIT 10
) CountGoals ON p.player_id = CountGoals.player_id;
"""
top_scorers = execute_query(top_scorers_query)
print(top_scorers)

print("7. Выборка матчей с детализацией по каждому голу")
detailed_goals_query = """
SELECT m.match_id, m.home_team, m.away_team, g.duration, g.goal_desc, p.first_name || ' ' || p.last_name AS scorer, a.first_name || ' ' || a.last_name AS assistant
FROM UEFA.goals g
JOIN UEFA.matches m ON g.match_id = m.match_id
JOIN UEFA.players p ON g.player_id = p.player_id
LEFT JOIN UEFA.players a ON g.assist = a.player_id;
"""
detailed_goals = execute_query(detailed_goals_query)
print(detailed_goals)

print("8. Вставка нового матча")
insert_match_query = """
INSERT INTO UEFA.matches (match_id, season, date_time, home_team, away_team, stadium, home_team_score, away_team_score)
VALUES ('match123', '2023-2024', NOW(), 'FC Barcelona', 'Real Madrid', 'Camp Nou', 2, 2);
"""
execute_query(insert_match_query)

check_query = "SELECT * FROM UEFA.matches WHERE match_id = 'match123';"

print("Проверка")
check = execute_query(check_query)
print(check)

print("9. Изменение данных матча")
update_match_query = """
UPDATE UEFA.matches
SET home_team = 'Paris Saint-Germain',
    date_time = now()
WHERE match_id = 'match123';
"""
execute_query(update_match_query)

print("Проверка")
check = execute_query(check_query)
print(check)

print("10. Удаление матча")
# 10. Удаление матча
delete_match_query = "DELETE FROM UEFA.matches WHERE match_id = 'match123';"
execute_query(delete_match_query)

print("Проверка")
check = execute_query(check_query)
print(check)
