# Anime Beats 🎵

Análisis de datos de la música del anime: openings, endings y los artistas detrás de ellos.

**Estado:** 🚧 en desarrollo

## Preguntas que responde

- ¿Qué artistas han cantado más openings y endings?
- ¿En qué años se registran más temas?
- ¿Cómo cambia la cantidad de temas a lo largo del tiempo?

## Principales hallazgos

- **2018 es el año con más temas registrados** (803), seguido de 2017 (766) y 2019 (686): el período 2017–2019 concentra la mayor actividad.
- **Openings:** angela lidera con 33, seguida muy de cerca por Nana Mizuki (32) y JAM Project (30). No hay un artista que domine claramente.
- **Endings:** Kana Hanazawa lidera con 79, seguida de Rie Takahashi (75) y Nao Toyama (64).

El detalle de cada análisis está en [HALLAZGOS.md](HALLAZGOS.md).

## Datos

Los datos vienen de la API pública de [AnimeThemes](https://animethemes.moe/), que incluye cada anime con sus openings, endings, canciones y artistas. El script descarga todas las páginas de la API respetando una pausa entre llamadas.

## Proceso

1. **Extracción:** `src/descargar_temas.py` descarga los datos de la API y los guarda en `data/raw/`.
2. **Limpieza y transformación:** con pandas se ordenan los temas por anime, tipo (opening/ending), año y artista. El resultado queda en `data/processed/`.
3. **Análisis:** conteos y rankings por artista y por año.
4. **Conclusiones:** documentadas en `HALLAZGOS.md`.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python src/descargar_temas.py
```

## Tecnologías

Python · pandas · requests

## Próximos pasos

- Dashboard interactivo en Looker Studio
- Cruzar los temas con la nota y popularidad de cada anime
- Comparar artistas por estudio de animación

## Autor

Isaac Andrade · [LinkedIn](https://www.linkedin.com/in/isaac-andrade-6652142b1/) · [GitHub](https://github.com/Isaac-Andrade970)
