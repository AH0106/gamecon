import json
import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")

DEFAULT_URI = "mongodb+srv://cristobalcastro1_db_user:1234@cluster0.towey3r.mongodb.net/GameCon?retryWrites=true&w=majority"
client = MongoClient(os.getenv("MONGO_URI", DEFAULT_URI))
db = client[os.getenv("MONGO_DB", "GameCon")]

CONSULTA = {"tags": {"$in": ["isekai", "mecha"]}}
NOMBRE_INDICE = "idx_tags"


def medir():
    plan = db.stands.find(CONSULTA).explain()
    stats = plan["executionStats"]
    plan_txt = json.dumps(plan["queryPlanner"]["winningPlan"])
    etapa = "IXSCAN" if "IXSCAN" in plan_txt else ("COLLSCAN" if "COLLSCAN" in plan_txt else "otra")
    return {
        "etapa": etapa,
        "docs_examinados": stats["totalDocsExamined"],
        "claves_examinadas": stats["totalKeysExamined"],
        "devueltos": stats["nReturned"],
        "ms": stats["executionTimeMillis"],
    }


if __name__ == "__main__":
    total = db.stands.count_documents({})
    if NOMBRE_INDICE in db.stands.index_information():
        db.stands.drop_index(NOMBRE_INDICE)
    antes = medir()
    db.stands.create_index("tags", name=NOMBRE_INDICE)   # multikey: tags es un arreglo
    despues = medir()

    print(f"Consulta: {CONSULTA}   (colección stands: {total} documentos)\n")
    print(f"{'':20}{'SIN índice':>14}{'CON índice':>14}")
    for k in antes:
        print(f"{k:20}{str(antes[k]):>14}{str(despues[k]):>14}")
