import perfilar as p



ds_games = p.df_games.copy()
ds_anime = p.df_anime.copy()
ds_comics = p.df_comics.copy()


ds_games = ds_games.drop_duplicates()
ds_games = ds_games.dropna(subset=['Year', 'Publisher'])
ds_game = ds_games.drop(columns = ['Platform','NA_Sales', 'Platform', 'EU_Sales', 'JP_Sales', 'Other_Sales'])
ds_games = ds_games.rename(columns={'Name': 'name', 'Publisher': 'productor', })

#p.descripcion_completa(ds_games,'games')

ds_anime = ds_anime.drop_duplicates()
ds_anime = ds_anime.dropna(subset=['Title English', 'Title Japanese', 'Score', 'Rank', 'Studios', 'Genres', 'Themes'])
ds_anime = ds_anime.drop(columns=['Type', 'Source', 'Episodes', 'Status', 'Airing', 'Aired From', 'Aired To','Synopsis'])
ds_anime = ds_anime.rename(columns={'Title': 'name', 'Studios': 'productor', 'Genres': 'genero'})

#p.descripcion_completa(ds_anime,'anime')


ds_comics = ds_comics.drop_duplicates(subset=["book_id"])
ds_comics = ds_comics.rename(columns={'title': 'name', 'publisher': 'productor'})
ds_comics = ds_comics.drop(columns=['text_reviews_count', 'series',  'language_code', 'popular_shelves', 'asin', 'is_ebook', 'kindle_asin', 'format', 'link', 'authors', 'num_pages', 'publication_day', 'isbn13', 'publication_month', 'edition_information', 'publication_year', 'url', 'image_url', 'work_id', 'title_without_series'])
#p.descripcion_completa(ds_comics, 'comics', subset=["book_id"])
