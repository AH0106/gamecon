from pathlib import Path
import os
import random
import faker
from dotenv import load_dotenv
from pymongo import MongoClient

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")

DEFAULT_URI = "mongodb+srv://cristobalcastro1_db_user:1234@cluster0.towey3r.mongodb.net/GameCon?retryWrites=true&w=majority"

NUM_USUARIOS = 100   # asistentes a simular
GUSTOS_POR_ASISTENTE = 3
SEMILLA = 42         # misma semilla -> mismos asistentes en cada corrida (reproducible)

# Tags que NO se asignan a asistentes simulados (contenido adulto)
EXCLUIR = {"hentai", "erotica"}


def crear_asistentes():
    random.seed(SEMILLA)
    faker.Faker.seed(SEMILLA)
    fake = faker.Faker("es_CL")

    client = MongoClient(os.getenv("MONGO_URI", DEFAULT_URI))
    db = client[os.getenv("MONGO_DB", "GameCon")]

    # Los gustos salen del vocabulario controlado que generó el ETL (colección tags),
    # así ningún asistente puede tener un gusto que no exista en algún stand.
    tags_validos = sorted(t["_id"] for t in db.tags.find({}, {"_id": 1}) if t["_id"] not in EXCLUIR)
    if len(tags_validos) < GUSTOS_POR_ASISTENTE:
        raise SystemExit("La colección tags está vacía: corre primero cargar_mongo.py")

    docs = []
    for i in range(1, NUM_USUARIOS + 1):
        docs.append({
            "_id": f"ASIS_{i:04d}",
            "nombre": fake.name(),
            "intereses_declarados": random.sample(tags_validos, GUSTOS_POR_ASISTENTE),
            "intereses_deducidos": {}
        })

    # Carga idempotente: vaciar y volver a insertar
    db.asistentes.delete_many({})
    db.asistentes.insert_many(docs)
    print(f"-> {db.asistentes.count_documents({})} asistentes en MongoDB "
          f"(gustos tomados de {len(tags_validos)} tags del vocabulario).")
    print("Ejemplo:", docs[0])


if __name__ == "__main__":
    crear_asistentes()
