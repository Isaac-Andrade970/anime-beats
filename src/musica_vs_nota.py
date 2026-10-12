import pandas as pd

anime = pd.read_csv("data/processed/anime.csv")
temas = pd.read_csv("data/processed/temas.csv")
notas = pd.read_csv("data/processed/notas.csv")

# 1. Contar cuántos temas tiene cada anime
temas_por_anime = temas.groupby("anime_id").size().reset_index(name="num_temas")

# 2. Unir todo en una sola tabla
anime["mal_id"] = anime["mal_id"].astype("Int64")
df = anime.merge(temas_por_anime, on="anime_id").merge(notas, on="mal_id")
df = df.dropna(subset=["nota"])

# 3. Agrupar: 1 tema, 2 temas... y "6 o más"
df["grupo_temas"] = df["num_temas"].clip(upper=6)
resumen = df.groupby("grupo_temas")["episodios"].agg(["mean", "count"]).round(1)

print("Promedio de episodios según cantidad de temas (6 = 6 o más):")
print(resumen)
print()
print("Correlación temas vs nota:", round(df["num_temas"].corr(df["nota"]), 2))