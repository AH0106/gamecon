import pandas as pd
from pathlib import Path

try:
    RAIZ = Path(__file__).resolve().parent.parent
except NameError:
    cwd = Path.cwd()
    RAIZ = cwd.parent if cwd.name == "src" else cwd

RAW = RAIZ / "datos" / "raw"

def cargar_datos_raw():
    """Carga y retorna los DataFrames crudos sin alterar sus índices."""
    df_games = pd.read_csv(RAW / "vgsales.csv")
    df_anime = pd.read_csv(RAW / "anime-dataset-2025.csv")
    df_comics = pd.read_json(
        RAW / "goodreads_books_comics_graphic.json.gz",
        lines=True,
        nrows=1000
    )
    return df_games, df_anime, df_comics

if __name__ == "__main__":
    df_games, df_anime, df_comics = cargar_datos_raw()
    print("Lectura cruda completada.")
