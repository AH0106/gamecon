
import limpieza as limp


comics = limp.ds_comics.copy()
anime = limp.ds_anime.copy()
games = limp.ds_games.copy()


tags_anime = anime.groupby('genero').agg(list)

productores_anime = anime.groupby("name").agg(n_titulos = ('name', 'nunique'))
print(tags_anime)
