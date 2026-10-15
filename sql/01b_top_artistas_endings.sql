-- ¿Qué artistas han cantado más endings de anime?
SELECT
  a.artista,
  COUNT(*) AS endings
FROM `anime_beats.artistas` AS a
JOIN `anime_beats.temas` AS t
  ON a.tema_id = t.tema_id
WHERE t.tipo = 'ED'
GROUP BY a.artista
ORDER BY endings DESC
LIMIT 15;