import pandas as pd

# 1. Cargar las tablas
anime = pd.read_csv("data/processed/anime.csv")
temas = pd.read_csv("data/processed/temas.csv")
artistas = pd.read_csv("data/processed/artistas.csv")

# 2. Unir artistas con temas para saber si cada canción es OP o ED
artistas_temas = artistas.merge(temas, on="tema_id")

# Pregunta 1: ¿Qué artistas han cantado más openings?
solo_endings = artistas_temas[artistas_temas["tipo"] == "ED"]
top_endings = solo_endings["artista"].value_counts().head(10)

print("Top 10 artistas con más endings:")
print(top_endings)
print()

# Pregunta 2: ¿Qué años tuvieron más temas de anime?
temas_anio = temas.merge(anime, on="anime_id")
por_anio = temas_anio["anio"].value_counts().head(5)

print("Años con más temas:")
print(por_anio)