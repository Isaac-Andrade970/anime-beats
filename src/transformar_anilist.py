import json
import pandas as pd

with open("data/raw/anilist_anime.json", encoding="utf-8") as archivo:
    animes = json.load(archivo)

filas_notas = []
filas_generos = []

for a in animes:
    filas_notas.append({
        "mal_id": a["mal_id"],
        "nota": a["nota"],
        "popularidad": a["popularidad"],
        "favoritos": a["favoritos"],
        "episodios": a["episodios"],
        "estudio": a["estudios"][0] if a["estudios"] else None,
    })
    for genero in a["generos"]:
        filas_generos.append({"mal_id": a["mal_id"], "genero": genero})

pd.DataFrame(filas_notas).to_csv("data/processed/notas.csv", index=False)
pd.DataFrame(filas_generos).to_csv("data/processed/generos.csv", index=False)

print("Notas:", len(filas_notas))
print("Filas de géneros:", len(filas_generos))