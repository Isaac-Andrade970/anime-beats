SELECT
  a.artista,
  COUNT(*) AS openings
FROM `anime_beats.artistas` AS a
JOIN `anime_beats.temas` AS t
  ON a.tema_id = t.tema_id
WHERE t.tipo = 'OP'
GROUP BY a.artista
ORDER BY openings DESC
LIMIT 10;