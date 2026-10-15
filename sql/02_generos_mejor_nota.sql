-- ¿Qué géneros tienen la mejor nota promedio?
SELECT
  g.genero,
  ROUND(AVG(n.nota), 1) AS nota_promedio,
  COUNT(*) AS cantidad
FROM `anime_beats.generos` AS g
JOIN `anime_beats.notas` AS n
  ON g.mal_id = n.mal_id
WHERE g.genero != 'Hentai'
GROUP BY g.genero
HAVING COUNT(*) >= 50
ORDER BY nota_promedio DESC;