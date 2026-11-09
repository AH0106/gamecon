import pandas as pd
from limpieza import obtener_datos_limpios

# Contenido adulto: fuera del vocabulario de una feria abierta a todo público


def normalizar(tag):
    return str(tag).strip().lower().replace(" ", "_")

def generar_stands(df_games, df_anime, df_comics):
    stands = []

    # 1. Procesar Juegos (Publisher -> Stand)
    for n_juego, (productor, group) in enumerate(df_games.groupby('productor'), 1):
        generos = [
            normalizar(g) for g in group['genero'].dropna().unique()
            if pd.notna(g) and str(g).strip().lower() not in ['misc', 'nan', '']
        ]
        stands.append({
            "nombre": str(productor),
            "dominio": "juego",
            "ubicacion": f"Zona Juegos - Stand {n_juego}",
            "tags": generos
        })

    # 2. Procesar Anime (Studios -> Stand)
    for n_anime, (productor, group) in enumerate(df_anime.groupby('productor'), 1):
        raw_series = pd.concat([group['genero'], group['Themes']]).dropna().astype(str)
        raw_exploded = raw_series.str.split(',').explode().astype(str).str.strip()
        generos = [
            normalizar(g) for g in raw_exploded.unique()
            if g and g.lower() not in ['nan', 'none', 'misc', ''] 
        ]
        stands.append({
            "nombre": str(productor),
            "dominio": "anime",
            "ubicacion": f"Zona Anime - Stand {n_anime}",
            "tags": generos
        })

    # 3. Procesar Comics/Mangas (Publisher -> Stand)
    for n_comic, (productor, group) in enumerate(df_comics.groupby('productor'), 1):
        stands.append({
            "nombre": str(productor),
            "dominio": "manga_comic",
            "ubicacion": f"Zona Comics - Stand {n_comic}",
            "tags": ["comic/manga"]
        })

    return pd.DataFrame(stands)

def generar_vocabulario_tags(df_stands):
    filas = df_stands[["dominio", "tags"]].explode("tags").dropna()
    vocabulario = []
    for tag, grupo in filas.groupby("tags"):
        dominios = sorted(grupo["dominio"].unique())
        vocabulario.append({
            "_id": tag,
            # general = conecta 2 o mas dominios; especifico = vive en uno solo
            "nivel": "general" if len(dominios) > 1 else "especifico",
            "dominios": dominios,
            "frecuencia": len(grupo)   # n de stands que lo tienen (para IDF)
        })
    return pd.DataFrame(vocabulario)




if __name__ == "__main__":

    df_games, df_anime, df_comics = obtener_datos_limpios()

    df_stands = generar_stands(df_games, df_anime, df_comics)
    df_tags = generar_vocabulario_tags(df_stands)
    df_stands.dropna(how='all')


    print(f"Stands generados: {len(df_stands)}")
    print(df_stands)

    print(f"Tags en vocabulario: {len(df_tags)}")
    df_tags = df_tags.sort_values(by='frecuencia', ascending=False)
    print(df_tags)
