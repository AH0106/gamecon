from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")

DEFAULT_URI = "mongodb+srv://cristobalcastro1_db_user:1234@cluster0.towey3r.mongodb.net/GameCon?retryWrites=true&w=majority"
client = MongoClient(os.getenv("MONGO_URI", DEFAULT_URI))
db = client[os.getenv("MONGO_DB", "GameCon")]

def registrar_interaccion(asistente_id, objetivo_id, tipo_interaccion, tags_objetivo):
    """Registra una interacción y actualiza el perfil deducido del asistente."""
    #guardar la interaccion (sin tope)
    db.interacciones.insert_one({
        "asistente_id": asistente_id,
        "objetivo_id": objetivo_id,
        "tipo": tipo_interaccion
    })

    #actualizar el perfil deducido
    peso = 2 if tipo_interaccion == "favorito" else 1
    for tag in tags_objetivo:
        db.asistentes.update_one(
            {"_id": asistente_id},
            {"$inc": {f"intereses_deducidos.{tag}": peso}}
        )
    print(f"Interacción '{tipo_interaccion}' registrada, perfil actualizado")
