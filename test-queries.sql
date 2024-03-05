--1. Выборка всех стадионов с их вместимостью, отсортированных по убыванию вместимости
SELECT name, capacity FROM UEFA.stadiums ORDER BY capacity DESC;

--2. Выборка игроков с указанием их команды и позиции, играющих за определенную команду
SELECT first_name, last_name, team, position FROM UEFA.players WHERE team = 'FC Barcelona';

--3. Выборка матчей, где общее число забитых голов было больше 5, отсортированных по убыванию голов
SELECT match_id, home_team, away_team, home_team_score, away_team_score, (home_team_score + away_team_score) as total_goals FROM UEFA.matches WHERE (home_team_score + away_team_score) > 5
ORDER BY total_goals DESC;

-- 4. Выборка для отображения домашних стадионов команд и их вместимости, отсортированных по алфавиту
SELECT t.team_name, t.home_stadium, s.city, s.capacity
FROM UEFA.teams t
JOIN UEFA.stadiums s ON t.home_stadium = s.name
ORDER BY team_name;

-- 5. Выборка тренеров с количеством игроков в их командах
SELECT m.first_name, m.last_name, m.team, COUNT(p.player_id) AS player_count
FROM UEFA.managers m
JOIN UEFA.players p ON m.team = p.team
WHERE m.team != ''
GROUP BY m.first_name, m.last_name, m.team
ORDER BY player_count DESC;

-- 6. Топ-10 игроков по количеству забитых голов, с указанием их имени, фамилии и команды.
SELECT p.first_name, p.last_name, p.team, CountGoals.total_goals
FROM UEFA.players p
JOIN (
  SELECT player_id, COUNT(goal_id) AS total_goals
  FROM UEFA.goals
  GROUP BY player_id
  ORDER BY total_goals DESC
  LIMIT 10
) CountGoals ON p.player_id = CountGoals.player_id;

-- 7. Выборка матчей с детализацией по каждому голу
SELECT m.match_id, m.home_team, m.away_team, g.duration, g.goal_desc, p.first_name || ' ' || p.last_name AS scorer, a.first_name || ' ' || a.last_name AS assistant
FROM UEFA.goals g
JOIN UEFA.matches m ON g.match_id = m.match_id
JOIN UEFA.players p ON g.player_id = p.player_id
LEFT JOIN UEFA.players a ON g.assist = a.player_id;

-- 8. Вставка нового матча
INSERT INTO UEFA.matches (match_id, season, date_time, home_team, away_team, stadium, home_team_score, away_team_score)
VALUES ('match123', '2023-2024', NOW(), 'FC Barcelona', 'Real Madrid', 'Camp Nou', 2, 2);

-- 9. Изменение данных матча
UPDATE UEFA.matches
SET home_team = 'Paris Saint-Germain',
    date_time = now()
WHERE match_id = 'match123';

-- 10. Удаление
DELETE FROM UEFA.matches
WHERE match_id = 'match123';

SELECT * FROM UEFA.matches
WHERE match_id = 'match123';

