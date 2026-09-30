import json
import os
import pandas as pd

# 1. Leer el JSON descargado
with open("data/raw/anime_temas.json", encoding="utf-8") as archivo:
    animes = json.load(archivo)

# 2. Listas vacías donde iremos juntando las filas de cada tabla
filas_anime = []
filas_temas = []
filas_artistas = []

# 3. Recorrer cada anime y repartir sus datos en las 3 tablas
for anime in animes:

    # Buscar el ID de MyAnimeList (lo usaremos para unir con Jikan)
    mal_id = None
    for recurso in anime.get("resources", []):
        if recurso["site"] == "MyAnimeList":
            mal_id = recurso["external_id"]

    filas_anime.append({
        "anime_id": anime["id"],
        "nombre": anime["name"],
        "anio": anime["year"],
        "temporada": anime["season"],
        "formato": anime["media_format"],
        "mal_id": mal_id,
    })

    for tema in anime.get("animethemes", []):
        cancion = tema.get("song") or {}

        filas_temas.append({
            "tema_id": tema["id"],
            "anime_id": anime["id"],
            "tipo": tema["type"],
            "slug": tema["slug"],
            "cancion": cancion.get("title"),
        })

        for artista in cancion.get("artists", []):
            filas_artistas.append({
                "tema_id": tema["id"],
                "artista": artista["name"],
            })

# 4. Convertir las listas en tablas de pandas (DataFrames)
df_anime = pd.DataFrame(filas_anime)
df_temas = pd.DataFrame(filas_temas)
df_artistas = pd.DataFrame(filas_artistas)

# 5. Guardar cada tabla como CSV
os.makedirs("data/processed", exist_ok=True)
df_anime.to_csv("data/processed/anime.csv", index=False)
df_temas.to_csv("data/processed/temas.csv", index=False)
df_artistas.to_csv("data/processed/artistas.csv", index=False)

print("Animes:", len(df_anime))
print("Temas:", len(df_temas))
print("Filas de artistas:", len(df_artistas))
print()
print(df_temas.head())