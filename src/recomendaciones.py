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


def normalizar_id(asistente_id: str) -> str:
    limpio = asistente_id.strip()
    if limpio.isdigit():
        return f"ASIS_{int(limpio):04d}"
    if limpio.lower().startswith("asis_"):
        num_part = limpio[5:]
        if num_part.isdigit():
            return f"ASIS_{int(num_part):04d}"
    return limpio.upper()


def obtener_perfil_asistente(asistente_id: str):
    id_busqueda = normalizar_id(asistente_id)
    asistente = db.asistentes.find_one({"_id": id_busqueda})
    if not asistente:
        asistente = db.asistentes.find_one({"_id": asistente_id.strip()})

    if not asistente:
        return None, []

    declarados = asistente.get("intereses_declarados", []) or []
    deducidos = list(asistente.get("intereses_deducidos", {}).keys()) if asistente.get("intereses_deducidos") else []
    gustos_totales = sorted(list(set(declarados + deducidos)))
    return asistente, gustos_totales


def recomendar_stands(asistente_id: str, top_n: int = 5):
    asistente, gustos_usuario = obtener_perfil_asistente(asistente_id)
    if not asistente:
        return None

    if not gustos_usuario:
        return []

    pipeline = [
        {"$match": {"tags": {"$in": gustos_usuario}}},
        {"$project": {
            "nombre": 1,
            "dominio": 1,
            "ubicacion": 1,
            "tags": 1,
            "tags_coincidentes": {"$setIntersection": ["$tags", gustos_usuario]},
            "coincidencias": {"$size": {"$setIntersection": ["$tags", gustos_usuario]}}
        }},
        {"$sort": {"coincidencias": -1, "nombre": 1}},
        {"$limit": top_n}
    ]
    return list(db.stands.aggregate(pipeline))


def modo_interactivo():
    print("-" * 50)
    print("Recomendador de Stands - GameCon")
    print("Escriba 'salir' o 'q' para terminar.")
    print("-" * 50)

    while True:
        try:
            entrada = input("\nID del asistente: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nFin del programa.")
            break

        if not entrada or entrada.lower() in ("salir", "exit", "q"):
            print("Fin del programa.")
            break

        asistente, gustos = obtener_perfil_asistente(entrada)
        if not asistente:
            print(f"Error: Asistente '{entrada}' no encontrado.")
            continue

        declarados = asistente.get("intereses_declarados", []) or []
        deducidos = list(asistente.get("intereses_deducidos", {}).keys()) if asistente.get("intereses_deducidos") else []

        print(f"\nAsistente: {asistente.get('nombre', 'Sin nombre')} ({asistente['_id']})")
        print(f"Tags declarados: {', '.join(declarados) if declarados else 'Ninguno'}")
        if deducidos:
            print(f"Tags deducidos: {', '.join(deducidos)}")
        print(f"Tags a coincidir: {', '.join(gustos) if gustos else 'Sin tags'}")

        if not gustos:
            print("Aviso: El asistente no tiene tags asociados.")
            continue

        try:
            top_str = input("Cantidad de recomendaciones [5]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nFin del programa.")
            break

        top_n = int(top_str) if top_str.isdigit() and int(top_str) > 0 else 5
        recomendaciones = recomendar_stands(asistente["_id"], top_n=top_n)

        if not recomendaciones:
            print("No se encontraron stands con coincidencias.")
            continue

        print(f"\nTop {len(recomendaciones)} Stands:")
        for i, stand in enumerate(recomendaciones, 1):
            coincidencias = stand.get("coincidencias", 0)
            tags_matched = ", ".join(stand.get("tags_coincidentes", []))
            ubicacion = stand.get("ubicacion", "Sin ubicacion")
            dominio = stand.get("dominio", "General")

            print(f"  {i}. {stand['nombre']} [{dominio}] ({ubicacion})")
            print(f"     Coincidencias ({coincidencias}): {tags_matched}")


if __name__ == "__main__":
    modo_interactivo()
