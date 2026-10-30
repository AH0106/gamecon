from numpy import column_stack
import pandas as pd
from pathlib import Path


try:
    RAIZ = Path(__file__).resolve().parent.parent
except NameError:
    cwd = Path.cwd()
    RAIZ = cwd.parent if cwd.name == "src" else cwd
RAW = RAIZ / "datos" / "raw"

df_games = pd.read_csv(RAW / "vgsales.csv")
df_anime = pd.read_csv(RAW / "anime-dataset-2025.csv")
df_comics = pd.read_json(
    RAW / "goodreads_books_comics_graphic.json.gz",
    lines=True,
    nrows=1000
)

def describe(df, name):
    """Descripcion del dataset"""
    print("\nDescripcion del dataset ", name)
    print(df.describe())

def nulls_count(df, name):
    """ Función para ver los nulos de cada dataset"""

    print("\nConteo de nulos en ", name)    # imprime: anime
    print(df.isnull().sum()[df.isnull().sum() > 0])

def duplicates(df, name, subset=None):
    """ Duplicados por data set"""
    print("\nConteo de duplicados en ", name)
    print(df.duplicated(subset=subset).sum())

def list(df_name, name):
    print(df_name.columns.tolist())


def descripcion_completa(df_name, name, subset = None):
    """Descripcion completa del dataset
    """
    describe(df_name, name)
    nulls_count(df_name, name )
    duplicates(df_name, name, subset)
    list(df_name, name)



if __name__ == "__main__":
    descripcion_completa(df_anime, 'anime')
    descripcion_completa(df_games, 'games')
    descripcion_completa(df_comics, 'comics', subset=['book_id'])
