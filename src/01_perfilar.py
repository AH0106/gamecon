
import pandas as pd


df_games = pd.read_csv("datos/raw/vgsales.csv.zip")
df_anime = pd.read_csv("datos/raw/anime-dataset-2025.csv")
df_comics = pd.read_json(
    "datos/raw/goodreads_books_comics_graphic.json.gz",
    lines=True,
    nrows=1000
)

print(f"\nColumnas de juegos:\n{df_games.columns}")
print(f"\nColumnas de anime:\n{df_anime.columns}")
print(f"\nColumnas de cómics:\n{df_comics.columns}")
