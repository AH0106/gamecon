from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/")) #se cambia cuando tengamos la base
db = client["gamecon_db"]

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