import pandas as pd
from limpieza import df_games, df_anime, df_comics

def generar_stands():
    stands = []

    # 1. Procesar Juegos (Publisher -> Stand)
    for productor, group in df_games.groupby('productor'):
        generos = [
            str(g).strip() for g in group['genero'].dropna().unique() 
            if pd.notna(g) and str(g).strip() not in ['Misc', 'nan', '']
        ]
        stands.append({
            "nombre": str(productor),
            "dominio": "juego",
            "ubicacion": f"Zona Juegos - Stand {len(stands) + 1}",
            "tags": generos
        })

    # 2. Procesar Anime (Studios -> Stand)
    for productor, group in df_anime.groupby('productor'):
        raw_series = group['genero'].dropna().astype(str)
        raw_exploded = raw_series.str.split(',').explode().astype(str).str.strip()
        generos = [
            g for g in raw_exploded.unique() 
            if g and g.lower() not in ['nan', 'none', 'misc']
        ]
        stands.append({
            "nombre": str(productor),
            "dominio": "anime",
            "ubicacion": f"Zona Anime - Stand {len(stands) + 1}",
            "tags": generos
        })

    # 3. Procesar Comics/Mangas (Publisher -> Stand)
    for productor, group in df_comics.groupby('productor'):
        stands.append({
            "nombre": str(productor),
            "dominio": "manga_comic",
            "ubicacion": f"Zona Comics - Stand {len(stands) + 1}",
            "tags": ["Comic/Manga"]
        })

    return pd.DataFrame(stands)

def generar_vocabulario_tags(df_stands):
    todos_los_tags = set(tag for tags_list in df_stands['tags'] for tag in tags_list)
    
    vocabulario = []
    for tag in todos_los_tags:
        frecuencia = sum(1 for tags_list in df_stands['tags'] if tag in tags_list)
        vocabulario.append({
            "_id": tag.lower().replace(" ", "_"),
            "nivel": "general" if frecuencia > 10 else "especifico",
            "origenes": [tag],
            "frecuencia": frecuencia
        })
    return pd.DataFrame(vocabulario)

if __name__ == "__main__":
    df_stands = generar_stands()
    df_tags = generar_vocabulario_tags(df_stands)

    print("--- Procesamiento completado ---")
    print(f"Stands generados sin nulos: {len(df_stands)}")
    print(f"Tags en vocabulario: {len(df_tags)}")
