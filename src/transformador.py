import pandas as pd
from pathlib import Path
import os
import shutil
import urllib.request
import kagglehub


# Determinar la raíz del proyecto de forma segura para Terminal y REPL
try:
    RAIZ = Path(__file__).resolve().parent.parent
except NameError:
    cwd = Path.cwd()
    RAIZ = cwd.parent if cwd.name == "src" else cwd

RAW = RAIZ / "datos" / "raw"
RAW.mkdir(parents=True, exist_ok=True)


def descargar_kaggle():
    print("Descargando datasets de Kaggle...")
    ruta_vgsales = kagglehub.dataset_download("gregorut/videogamesales")
    ruta_anime2025 = kagglehub.dataset_download("rafidahmed816/anime-dataset-2025")

    for ruta in [ruta_vgsales, ruta_anime2025]:
        for root, _, files in os.walk(ruta):
            for f in files:
                if f.endswith(".complete"):
                    continue
                origen = os.path.join(root, f)
                destino = RAW / f
                if not destino.exists():
                    shutil.copy2(origen, destino)
                    print(f"Copiado a raw: {f}")
                else:
                    print(f"Ya existe en raw: {f}")

        # Elimina la carpeta de caché y su contenido
        shutil.rmtree(ruta, ignore_errors=True)
        print(f"Caché eliminada: {ruta}")

def descargar_goodreads():
    nombre="goodreads_books_comics_graphic.json.gz"
    destino = RAW/nombre

    if destino.exists():
        print(f"ya se encuentra {nombre} en la carpeta")
        return

    url=f"https://mcauleylab.ucsd.edu/public_datasets/gdrive/goodreads/byGenre/goodreads_books_comics_graphic.json.gz"
    with urllib.request.urlopen(url) as r, open(destino, "wb") as f:
        shutil.copyfileobj(r, f)



if __name__ == "__main__":
    descargar_kaggle()
    descargar_goodreads()
