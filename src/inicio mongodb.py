from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/") #crea variable para vincular el codigo con una base en mongo, aqui se debe cambiar cuando se cree el database en mongo
client = MongoClient(MONGO_URI)                                  #se crea la conexion con la base de datos
db = client["gamecon_db"]                                        #selecciona (o prepara para crear) la base de datos donde se trabajara

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