import json
import time
import requests

url = "https://api.animethemes.moe/anime"
params = {
    "page[size]": 50,
    "include": "animethemes.song.artists,resources",
}

todos_los_animes = []
pagina = 1
max_paginas = 1000  # límite para probar; después lo quitaremos

while url is not None and pagina <= max_paginas:
    print(f"Descargando página {pagina}...")

    respuesta = requests.get(url, params=params)
    respuesta.raise_for_status()
    datos = respuesta.json()

    todos_los_animes.extend(datos["anime"])

    url = datos["links"]["next"]
    params = None
    pagina += 1
    time.sleep(1)

print(f"Total descargado: {len(todos_los_animes)} animes")

with open("data/raw/anime_temas.json", "w", encoding="utf-8") as archivo:
    json.dump(todos_los_animes, archivo, ensure_ascii=False, indent=2)

print("Guardado en data/raw/anime_temas.json")