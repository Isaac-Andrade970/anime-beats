-- ¿Los animes con más temas tienen mejor nota? ¿Y más episodios?
WITH temas_por_anime AS (
  SELECT anime_id, COUNT(*) AS num_temas
  FROM `anime_beats.temas`
  GROUP BY anime_id
)
SELECT
  LEAST(tp.num_temas, 6) AS grupo_temas,
  ROUND(AVG(n.nota), 1) AS nota_promedio,
  ROUND(AVG(n.episodios), 1) AS episodios_promedio,
  COUNT(*) AS cantidad
FROM temas_por_anime AS tp
JOIN `anime_beats.anime` AS an
  ON tp.anime_id = an.anime_id
JOIN `anime_beats.notas` AS n
  ON an.mal_id = n.mal_id
WHERE n.nota IS NOT NULL
GROUP BY grupo_temas
ORDER BY grupo_temas;