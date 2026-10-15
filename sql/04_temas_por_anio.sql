-- ¿Cuántos openings y endings hubo cada año?
SELECT 
  a.anio,
  t.tipo,
  COUNT(*) AS cantidad
FROM `anime_beats.anime` AS a 
JOIN `anime_beats.temas` AS t
  ON a.anime_id = t.anime_id
WHERE a.anio IS NOT NULL
GROUP BY a.anio, t.tipo
ORDER BY a.anio ASC, t.tipo;
