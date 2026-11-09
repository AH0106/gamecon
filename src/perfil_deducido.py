from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")

DEFAULT_URI = "mongodb+srv://cristobalcastro1_db_user:1234@cluster0.towey3r.mongodb.net/GameCon?retryWrites=true&w=majority"
client = MongoClient(os.getenv("MONGO_URI", DEFAULT_URI))
db = client[os.getenv("MONGO_DB", "GameCon")]

PESOS = {"favorito": 2, "visita": 1, "asistencia": 1}


def registrar_interaccion(asistente_id, objetivo_id, tipo_interaccion, tags_objetivo, fecha=None):
    """Registra una interacción y actualiza el perfil deducido del asistente."""
    db.interacciones.insert_one({
        "asistente_id": asistente_id,
        "objetivo_id": objetivo_id,
        "tipo": tipo_interaccion,
        "fecha": fecha,
    })

    # Un solo update con todos los $inc (antes era un update_one por tag)
    peso = PESOS.get(tipo_interaccion, 1)
    incrementos = {f"intereses_deducidos.{tag}": peso for tag in tags_objetivo}
    if incrementos:
        db.asistentes.update_one({"_id": asistente_id}, {"$inc": incrementos})
