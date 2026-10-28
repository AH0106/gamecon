import pandas as pd
from pathlib import Path


RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "datos" / "raw"

df_games = pd.read_csv(RAW / "vgsales.csv.zip")
df_anime = pd.read_csv(RAW / "anime-dataset-2025.csv")
df_comics = pd.read_json(
    RAW / "goodreads_books_comics_graphic.json.gz",
    lines=True,
    nrows=1000
)


print(f"\n Columnas del dataset de juegos{df_games.columns}")
print(f"\n Columnas del dataset de anime{df_anime.columns}")
print(f"\n Columnas del dataset de comics{df_comics.columns}")


def describe(df, name):
    """Descripcion del dataset"""
    print(f"\nDescripcion del dataset {name}")
    print(df.describe())

def nulls_count(df, name):
    """ Función para ver los nulos de cada dataset"""
    
    print(f"\nConteo de nulos en {name}")    # imprime: anime
    print(df.isnull().sum()[df.isnull().sum() > 0])

def duplicates(df_name, name):
    """ Duplicados por data set"""
    print(f"\nConteo de duplicados en {name}")    # imprime: anime
    print(df_name.duplicated().sum())

describe(df_anime, "anime")
nulls_count(df_anime, "anime")
duplicates(df_anime, "anime")
