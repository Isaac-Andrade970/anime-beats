import json
import time
import pandas as pd
import requests

URL = "https://graphql.anilist.co"
ARCHIVO = "data/raw/anilist_anime.json"

CONSULTA = """
query ($ids: [Int]) {
  Page(perPage: 50) {
    media(idMal_in: $ids, type: ANIME) {
      idMal
      title { romaji }
      averageScore
      popularity
      favourites
      episodes
      genres
      studios(isMain: true) { nodes { name } }
    }
  }
}
"""


def pedir_grupo(ids):
    """Pide hasta 50 animes a AniList. Reintenta si falla."""
    for intento in range(5):
        try:
            respuesta = requests.post(
                URL,
                json={"query": CONSULTA, "variables": {"ids": ids}},
                timeout=30,
            )
            if respuesta.status_code == 200:
                return respuesta.json()["data"]["Page"]["media"]
            if respuesta.status_code == 429:
                espera = int(respuesta.headers.get("Retry-After", 60))
                print(f"  Límite alcanzado, esperando {espera} segundos...")
                time.sleep(espera)
                continue
            print(f"  Error {respuesta.status_code}, reintentando...")
        except requests.RequestException:
            print("  Problema de conexión, reintentando...")
        time.sleep(5)
    raise Exception("No se pudo descargar un grupo de animes")


# 1. Obtener los mal_id como lista de números
anime = pd.read_csv("data/processed/anime.csv")
ids = anime["mal_id"].dropna().astype(int).unique().tolist()
print(f"Animes a consultar: {len(ids)}")

# 2. Pedirlos en grupos de 50
resultados = []
for inicio in range(0, len(ids), 50):
    grupo = ids[inicio:inicio + 50]
    medios = pedir_grupo(grupo)

    for m in medios:
        resultados.append({
            "mal_id": m["idMal"],
            "titulo": m["title"]["romaji"],
            "nota": m["averageScore"],
            "popularidad": m["popularity"],
            "favoritos": m["favourites"],
            "episodios": m["episodes"],
            "generos": m["genres"],
            "estudios": [s["name"] for s in m["studios"]["nodes"]],
        })

    print(f"Avance: {min(inicio + 50, len(ids))} de {len(ids)}")
    time.sleep(2.5)

# 3. Guardar
with open(ARCHIVO, "w", encoding="utf-8") as archivo:
    json.dump(resultados, archivo, ensure_ascii=False)

print(f"Listo: {len(resultados)} animes guardados en {ARCHIVO}")