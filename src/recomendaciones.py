from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os

try:
    RAIZ = Path(__file__).resolve().parent.parent
except NameError:
    cwd = Path.cwd()
    RAIZ = cwd.parent if cwd.name == "src" else cwd

load_dotenv(RAIZ / ".env")

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client[os.getenv("MONGO_DB", "GameCon")]

def recomendar_stands(asistente_id, top_n=5):
    asistente = db.asistentes.find_one({"_id": asistente_id})
    if not asistente:
        return "Asistente no encontrado"

    gustos_usuario = list(set(asistente.get("intereses_declarados", []) +
                              list(asistente.get("intereses_deducidos", {}).keys())))

    pipeline = [
        {"$match": {"tags": {"$in": gustos_usuario}}},
        {"$project": {
            "nombre": 1, "dominio": 1,
            "coincidencias": {"$size": {"$setIntersection": ["$tags", gustos_usuario]}}
        }},
        {"$sort": {"coincidencias": -1}},
        {"$limit": top_n}
    ]
    return list(db.stands.aggregate(pipeline))


if __name__ == "__main__":
    print("Probando recomendador con ASIS_0001 (Ricardo Mellado)...")
    recs = recomendar_stands("ASIS_0092", top_n=5)
    for i, r in enumerate(recs, 1):
        print(f"  {i}. {r['nombre']} ({r['dominio']}) - Coincidencias: {r['coincidencias']}")
