from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=RAIZ / ".env")

DEFAULT_URI = "mongodb+srv://cristobalcastro1_db_user:1234@cluster0.towey3r.mongodb.net/GameCon?retryWrites=true&w=majority"
MONGO_URI = os.getenv("MONGO_URI", DEFAULT_URI)
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
