# GAMECON

Sistema de recomendación de stands para una feria tipo Comic-Con.
Proyecto semestral de Bases de Datos Avanzadas y Big Data, UDP.

## Dominios

- Juegos
- Anime
- Cómics / Manga

## Puesta en marcha

```bash
git clone <url-del-repo>
cd gamecon
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Datos

Los datasets NO están en el repositorio: pesan demasiado y la licencia de
Goodreads prohíbe su redistribución. Cada quien los descarga y los deja en
`datos/raw/` con estos nombres exactos:

| Archivo en `datos/raw/` | Fuente | Link |
|---|---|---|
| `vgsales.csv.zip` | https://www.kaggle.com/datasets/gregorut/videogamesales | |
| `anime_details.csv` | Anime Dataset 2025 (Kaggle) | https://www.kaggle.com/datasets/rafidahmed816/anime-dataset-2025 | 
| `anime_stats.csv` | Anime Dataset 2025 (Kaggle) | https://www.kaggle.com/datasets/rafidahmed816/anime-dataset-2025 |
| `anime_favs.csv` | Anime Dataset 2025 (Kaggle) | https://www.kaggle.com/datasets/rafidahmed816/anime-dataset-2025 | 
| `goodreads_books_comics_graphic.json.gz` | https://cseweb.ucsd.edu/~jmcauley/datasets/goodreads.html | https://mcauleylab.ucsd.edu/public_datasets/gdrive/goodreads/byGenre/goodreads_books_comics_graphic.json.gz | 

## Estructura

```
datos/raw/         descargado tal cual, nunca se modifica
datos/interim/     normalizado por fuente
datos/processed/   listo para cargar a Mongo
config/            tablas de decisión (mapeo de tags)
src/               scripts del pipeline, numerados por orden
```

## Pipeline

1. `src/01_perfilar.py` — inspección de cada fuente
2. (pendiente)
