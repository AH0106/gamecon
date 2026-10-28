import perfilar as p



ds_games = p.df_games.copy()
ds_anime = p.df_anime.copy()
ds_comics = p.df_comics.copy()


ds_games = ds_games.drop_duplicates()
ds_games = ds_games.dropna(subset=['Year', 'Publisher'])
ds_games = ds_games.rename(columns={'Name': 'name', 'Publisher': 'productor', })
p.descripcion_completa(ds_games,'games')

ds_anime = ds_anime.drop_duplicates()
ds_anime = ds_anime.dropna(subset=[
    'Title English', 'Title Japanese', 'Type', 'Episodes', 'Aired From', 'Aired To', 'Score', 'Rank', 'Synopsis', 'Studios', 'Genres', 'Themes',
])
ds_anime = ds_anime.rename(columns={'Title': 'name', 'Studios': 'productor', 'Genres': 'genero'})
p.descripcion_completa(ds_anime,'anime')


ds_comics = ds_comics.drop_duplicates(subset=["book_id"])
ds_comics = ds_comics.rename(columns={'title': 'name', 'publisher': 'productor'})
p.descripcion_completa(ds_comics, 'comics', subset=["book_id"])
