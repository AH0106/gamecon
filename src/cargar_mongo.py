import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd

# Cargar variables de entorno
RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "GameCon")

# Importar generadores de stands y tags
import sys
sys.path.append(str(RAIZ / "src"))
from limpieza import obtener_datos_limpios
from procesar_tags import generar_stands, generar_vocabulario_tags


def cargar_datos_a_mongo():
    print(f"Conectando a MongoDB ({MONGO_DB})...")
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]

    # 1. Obtener DataFrames limpios y procesados
    print("Generando stands y vocabulario desde los datasets...")
    df_games, df_anime, df_comics = obtener_datos_limpios()
    df_stands = generar_stands(df_games, df_anime, df_comics)
    df_tags = generar_vocabulario_tags(df_stands)

    # 2. Cargar stands (idempotente: vaciamos y volvemos a insertar)
    print(f"Cargando {len(df_stands)} stands...")
    db.stands.delete_many({})
    docs_stands = df_stands.to_dict(orient="records")
    db.stands.insert_many(docs_stands)
    print(f"-> {db.stands.count_documents({})} stands en MongoDB.")

    # 3. Cargar tags
    print(f"Cargando {len(df_tags)} tags...")
    db.tags.delete_many({})
    docs_tags = df_tags.to_dict(orient="records")
    db.tags.insert_many(docs_tags)
    print(f"-> {db.tags.count_documents({})} tags en MongoDB.")

    print("\n¡Carga completada con éxito!")


if __name__ == "__main__":
    cargar_datos_a_mongo()
