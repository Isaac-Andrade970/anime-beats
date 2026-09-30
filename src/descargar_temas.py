import requests

url = "https://api.animethemes.moe/anime"
params = {
    "page[size]": 5,
    "include": "animethemes.song.artists,resources",
}

respuesta = requests.get(url, params=params)
datos = respuesta.json()

for anime in datos["anime"]:
    print(anime["name"], anime["year"])