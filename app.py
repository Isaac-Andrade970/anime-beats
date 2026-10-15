import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Anime Beats", page_icon="🎵", layout="wide")


# 1. Cargar los datos
@st.cache_data
def cargar_datos():
    anime = pd.read_csv("data/processed/anime.csv")
    anime["mal_id"] = anime["mal_id"].astype("Int64")
    temas = pd.read_csv("data/processed/temas.csv")
    artistas = pd.read_csv("data/processed/artistas.csv")
    notas = pd.read_csv("data/processed/notas.csv")
    generos = pd.read_csv("data/processed/generos.csv")
    return anime, temas, artistas, notas, generos


anime, temas, artistas, notas, generos = cargar_datos()


# 2. Título
st.title("🎵 Anime Beats")
st.caption("La música del anime en datos: openings, endings y los artistas detrás de ellos.")


# 3. Números principales
col1, col2, col3 = st.columns(3)
col1.metric("Animes analizados", f"{len(anime):,}".replace(",", "."))
col2.metric("Openings y endings", f"{len(temas):,}".replace(",", "."))
col3.metric("Animes con nota", f"{len(notas):,}".replace(",", "."))


# 4. Top artistas
def top_artistas(tipo):
    """Devuelve los 15 artistas con más temas del tipo indicado (OP o ED)."""
    df = artistas.merge(temas, on="tema_id")
    df = df[df["tipo"] == tipo]
    top = df["artista"].value_counts().head(15).reset_index()
    top.columns = ["artista", "cantidad"]
    return top


def grafico_barras(df, titulo):
    fig = px.bar(df, x="cantidad", y="artista", orientation="h", text="cantidad", title=titulo)
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, yaxis_title="", xaxis_title="")
    fig.update_traces(textposition="outside")
    return fig


st.header("¿Quién canta la música del anime?")
izquierda, derecha = st.columns(2)
izquierda.plotly_chart(grafico_barras(top_artistas("OP"), "Artistas con más openings"))
derecha.plotly_chart(grafico_barras(top_artistas("ED"), "Artistas con más endings"))
st.info(
    "Varias de las artistas con más temas son actrices de voz (seiyuu). "
    "En los endings su presencia es todavía más fuerte: Kana Hanazawa tiene 79 endings, pero solo 25 openings."
)


# 5. Temas por año
st.header("¿Cómo ha cambiado la música del anime?")
por_anio = temas.merge(anime, on="anime_id").dropna(subset=["anio"])
por_anio = por_anio.groupby(["anio", "tipo"]).size().reset_index(name="cantidad")
fig = px.line(por_anio, x="anio", y="cantidad", color="tipo", markers=True,
              labels={"anio": "Año", "cantidad": "Temas", "tipo": "Tipo"})
st.plotly_chart(fig)
st.info(
    "Hasta el año 2000 había casi la misma cantidad de openings que de endings. Desde 2005, los endings "
    "superan claramente a los openings: en 2018 hubo más de 500 endings y menos de 300 openings. "
    "Una posible explicación es que los animes modernos cambian el ending más seguido o usan endings especiales."
)
st.warning(
    "Precaución: 2018 fue el año con más temas (803), pero los años recientes pueden estar incompletos "
    "en la base de datos. Además, 2026 todavía no termina, por eso la línea cae al final."
)


# 6. Música vs nota
st.header("¿Más música significa mejor anime?")
temas_por_anime = temas.groupby("anime_id").size().reset_index(name="num_temas")
df = anime.merge(temas_por_anime, on="anime_id").merge(notas, on="mal_id")
df = df.dropna(subset=["nota"])
df["grupo_temas"] = df["num_temas"].clip(upper=6).astype(str).replace("6", "6+")
resumen = df.groupby("grupo_temas").agg(
    nota_promedio=("nota", "mean"),
    episodios_promedio=("episodios", "mean"),
).round(1).reset_index()

izquierda, derecha = st.columns(2)

fig_nota = px.bar(resumen, x="grupo_temas", y="nota_promedio", text="nota_promedio",
                  title="Nota promedio según cantidad de temas",
                  labels={"grupo_temas": "Cantidad de temas", "nota_promedio": "Nota (0-100)"})
fig_nota.update_xaxes(type="category")
izquierda.plotly_chart(fig_nota)

fig_eps = px.bar(resumen, x="grupo_temas", y="episodios_promedio", text="episodios_promedio",
                 title="Episodios promedio según cantidad de temas",
                 labels={"grupo_temas": "Cantidad de temas", "episodios_promedio": "Episodios"})
fig_eps.update_xaxes(type="category")
derecha.plotly_chart(fig_eps)

st.info(
    "Los animes con más temas tienen mejor nota, pero también son mucho más largos. "
    "Probablemente las series exitosas se renuevan y por eso acumulan más temas: "
    "la música no causa la buena nota. Correlación no implica causalidad."
)


# 7. Géneros
st.header("¿Qué géneros son los mejor evaluados?")
g = generos[generos["genero"] != "Hentai"].merge(notas, on="mal_id").dropna(subset=["nota"])
por_genero = g.groupby("genero").agg(
    nota_promedio=("nota", "mean"),
    cantidad=("nota", "size"),
).round(1).reset_index()
por_genero = por_genero[por_genero["cantidad"] >= 50]
fig = px.bar(por_genero, x="nota_promedio", y="genero", orientation="h", text="nota_promedio",
             hover_data=["cantidad"], labels={"nota_promedio": "Nota promedio", "genero": ""})
fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=550)
st.plotly_chart(fig)
st.info("Thriller, Psychological y Drama lideran. Los géneros masivos como Comedy y Action quedan en la mitad.")


# 8. Artistas en los animes mejor evaluados
st.header("¿Qué artistas cantan en los animes mejor evaluados?")
a = artistas.merge(temas, on="tema_id").merge(anime, on="anime_id").merge(notas, on="mal_id")
a = a.dropna(subset=["nota"])
top = a.groupby("artista").agg(
    nota_promedio=("nota", "mean"),
    temas=("nota", "size"),
).round(1).reset_index()
top = top[top["temas"] >= 10].sort_values("nota_promedio", ascending=False).head(20)
fig = px.bar(top, x="nota_promedio", y="artista", orientation="h", text="nota_promedio",
             hover_data=["temas"], labels={"nota_promedio": "Nota promedio", "artista": ""},
             title="Artistas con al menos 10 temas, ordenados por la nota de sus animes")
fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=600)
st.plotly_chart(fig)
st.info(
    "Las actrices de voz dominan en cantidad de temas, pero los animes mejor evaluados suelen contar "
    "con bandas reconocidas. Ojo: artistas como Linked Horizon trabajan sobre todo con una franquicia "
    "(Ataque a los Titanes), así que su nota refleja el éxito de esa serie."
)

st.caption("Datos: AnimeThemes y AniList. Proyecto de Isaac Andrade.")