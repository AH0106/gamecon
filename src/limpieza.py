from perfilar import cargar_datos_raw

def obtener_datos_limpios():
    df_games, df_anime, df_comics = cargar_datos_raw()

    # 1. Juegos
    df_games = df_games.copy().drop_duplicates()
    cols_eliminar_games = ['Platform', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
    df_games = df_games.drop(columns=[c for c in cols_eliminar_games if c in df_games.columns])
    df_games = df_games.rename(columns={'Name': 'name', 'Publisher': 'productor', 'Genre': 'genero'})
    df_games = df_games.dropna(subset=['productor', 'name'])
    df_games['genero'] = df_games['genero'].astype(str).str.strip()
    df_games['dominio'] = 'juego'

    # 2. Anime
    df_anime = df_anime.copy().drop_duplicates()
    cols_eliminar_anime = ['Type', 'Source', 'Episodes', 'Status', 'Airing', 'Aired From', 'Aired To', 'Synopsis']
    df_anime = df_anime.drop(columns=[c for c in cols_eliminar_anime if c in df_anime.columns])
    df_anime = df_anime.rename(columns={'Title': 'name', 'Studios': 'productor', 'Genres': 'genero'})
    df_anime = df_anime.dropna(subset=['productor', 'name'])
    df_anime['dominio'] = 'anime'

    # 3. Cómics
    df_comics = df_comics.copy().drop_duplicates(subset=['book_id'])
    cols_a_borrar_comics = [
        'text_reviews_count', 'series', 'language_code', 'asin', 
        'is_ebook', 'kindle_asin', 'format', 'link', 'authors', 'num_pages', 
        'publication_day', 'isbn13', 'publication_month', 'edition_information', 
        'publication_year', 'url', 'image_url', 'work_id', 'title_without_series', 'country_code',
        'isbn', 'popular_shelves', 'average_rating', 'description','similar_books', 'book_id', 'ratings_count'
    ]
    df_comics = df_comics.drop(columns=[c for c in cols_a_borrar_comics if c in df_comics.columns])
    df_comics = df_comics.rename(columns={'title': 'name', 'publisher': 'productor'})
    df_comics = df_comics.dropna(subset=['productor', 'name'])
    df_comics['genero'] = 'Comic/Manga'
    df_comics['dominio'] = 'manga_comic'


    return df_games, df_anime, df_comics


print(obtener_datos_limpios())


def vacio_a_nulo(column):
    if column is None:
        return None

    limpio = column.astype("string").str.strip()
    basura = {"", "nan", "none", "misc", "null", "n/a", "-"}
    
    return limpio.mask(limpio.str.lower().isin(basura))




def quitar_tildes(x):
    if x != str(x):        
        return x
    x = x.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
