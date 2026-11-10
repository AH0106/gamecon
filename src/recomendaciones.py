from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import math
import os

try:
    RAIZ = Path(__file__).resolve().parent.parent
except NameError:
    cwd = Path.cwd()
    RAIZ = cwd.parent if cwd.name == "src" else cwd

load_dotenv(RAIZ / ".env")

DEFAULT_URI = "mongodb+srv://cristobalcastro1_db_user:1234@cluster0.towey3r.mongodb.net/GameCon?retryWrites=true&w=majority"
client = MongoClient(os.getenv("MONGO_URI", DEFAULT_URI))
db = client[os.getenv("MONGO_DB", "bdgamecon")]

TOP_DEDUCIDOS = 5


def calcular_idf(tags):
    """idf(t) = ln(N / df_t): N = total de stands, df_t = stands que tienen el tag.
    Un tag que tienen casi todos los stands pesa ~0; uno raro pesa mucho."""
    n = db.stands.estimated_document_count()
    frec = {t["_id"]: t["frecuencia"] for t in db.tags.find({"_id": {"$in": tags}})}
    return [math.log(n / frec[t]) if frec.get(t) else 0.0 for t in tags]


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
    # Solo los TOP_DEDUCIDOS tags más representativos de sus interacciones (si no, un
    # stand con 60 tags inunda el perfil y todo se vuelve "gusto" del asistente)
    ded = asistente.get("intereses_deducidos") or {}
    # Se ordenan por conteo x idf (TF-IDF del perfil): un tag genérico como "action"
    # se repite mucho pero pesa poco; uno raro y repetido define el gusto real.
    idf_ded = dict(zip(ded, calcular_idf(list(ded))))
    deducidos = sorted(ded, key=lambda t: -ded[t] * idf_ded[t])[:TOP_DEDUCIDOS]
    gustos_totales = sorted(set(declarados + deducidos))
    return asistente, gustos_totales


def recomendar_stands(asistente_id: str, top_n: int = 5):
    asistente, gustos_usuario = obtener_perfil_asistente(asistente_id)
    if not asistente:
        return None

    if not gustos_usuario:
        return []

    pesos = calcular_idf(gustos_usuario)   # pesos[i] corresponde a gustos_usuario[i]
    comunes = {"$setIntersection": ["$tags", gustos_usuario]}

    pipeline = [
        {"$match": {"tags": {"$in": gustos_usuario}}},          # usa el índice idx_tags
        {"$project": {
            "nombre": 1,
            "dominio": 1,
            "ubicacion": 1,
            "tags": 1,
            "tags_coincidentes": comunes,
            "coincidencias": {"$size": comunes},
            # puntaje = (suma del idf de los tags en común) / raíz(n° de tags del stand)
            # El divisor evita que un estudio con 60 tags gane siempre solo por ser grande.
            "puntaje": {"$divide": [
                {"$sum": {"$map": {
                    "input": comunes,
                    "as": "t",
                    "in": {"$arrayElemAt": [pesos, {"$indexOfArray": [gustos_usuario, "$$t"]}]}
                }}},
                {"$sqrt": {"$size": "$tags"}}
            ]}
        }},
        {"$sort": {"puntaje": -1, "coincidencias": -1, "nombre": 1}},
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
        deducidos = [t for t in gustos if t not in declarados]

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
            print(f"     Puntaje IDF {stand.get('puntaje', 0):.2f} | Coincidencias ({coincidencias}): {tags_matched}")


if __name__ == "__main__":
    modo_interactivo()
