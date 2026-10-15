-- ¿Qué artistas cantan en los animes mejor evaluados?
SELECT 
  a.artista,
  ROUND(AVG(n.nota), 1) AS nota_promedio,
  COUNT(*) AS cantidad
FROM `anime_beats.artistas` AS a
INNER JOIN `anime_beats.temas` AS t
  ON a.tema_id = t.tema_id
INNER JOIN `anime_beats.anime` AS an
  ON t.anime_id = an.anime_id
INNER JOIN `anime_beats.notas` AS n
  ON an.mal_id = n.mal_id
GROUP BY a.artista
HAVING COUNT(*) >= 10
ORDER BY nota_promedio DESC;