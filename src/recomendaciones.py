from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/")) #se debe cambiar cuando se tenga la base real
db = client["gamecon_db"]

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