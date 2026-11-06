from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client[os.getenv("MONGO_DB", "GameCon")]                                        #selecciona (o prepara para crear) la base de datos donde se trabajara

def inicializar_colecciones():
    colecciones = ["tags", "stands", "presentaciones", "asistentes", "interacciones"]
    for col in colecciones:
        if col not in db.list_collection_names():
            db.create_collection(col)
            print(f"Colección '{col}' creada.")
        else:
            print(f"Colección '{col}' ya existe.")

if __name__ == "__main__":
    inicializar_colecciones()
