from pathlib import Path
from datetime import datetime, timedelta
import os
import random
from dotenv import load_dotenv
from pymongo import MongoClient

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")

DEFAULT_URI = "mongodb+srv://cristobalcastro1_db_user:1234@cluster0.towey3r.mongodb.net/GameCon?retryWrites=true&w=majority"

NUM_PRESENTACIONES = 20
SEMILLA = 42
EXCLUIR = {"hentai", "erotica"}

# Mismos nombres de dominio que en la colección stands
titulos = {
    "juego": [
        "El futuro del RPG japonés", "Speedrun: Cómo romper un juego en 20 minutos",
        "Diseño de niveles en plataformas 2D", "Historia de los videojuegos retro",
        "Competitivo: Estrategias de alto nivel", "Indies que cambiaron la industria",
        "Creando tu primer juego en Unity", "Los mejores juegos de 2026"
    ],
    "anime": [
        "Top 10 animes de la temporada", "Cómo se produce un anime",
        "De manga a anime: el proceso de adaptación", "Cosplay: guía para principiantes",
        "Los mejores villanos del anime", "Isekai: ¿por qué nos encantan?",
        "Animación 2D vs 3D", "Historia del anime en los 90s"
    ],
    "manga_comic": [
        "Mangakas emergentes que debes conocer", "El arte del manga shojo",
        "Cómo publicar tu primer manga", "One Piece: análisis de 25 años",
        "Manga independiente vs editorial", "Técnicas de dibujo digital"
    ],
}

lugares = [
    "Zona 1 - Escenario Principal", "Zona 2 - Sala de Charlas",
    "Zona 3 - Auditorio Anime", "Zona 4 - Sala de Juegos",
    "Zona 6 - Taller Creativo", "Zona 7 - Sala de Cómics",
    "Zona 8 - Escenario Secundario"
]

dias_convencion = [
    datetime(2026, 11, 7, 10, 0),
    datetime(2026, 11, 8, 10, 0),
    datetime(2026, 11, 9, 10, 0),
]


def crear_presentaciones():
    random.seed(SEMILLA)
    client = MongoClient(os.getenv("MONGO_URI", DEFAULT_URI))
    db = client[os.getenv("MONGO_DB", "GameCon")]

    # Tags por dominio, sacados del vocabulario (campo "dominios" que genera el ETL)
    tags_por_dominio = {d: [] for d in titulos}
    for t in db.tags.find({}, {"_id": 1, "dominios": 1}):
        if t["_id"] in EXCLUIR:
            continue
        for d in t.get("dominios", []):
            if d in tags_por_dominio:
                tags_por_dominio[d].append(t["_id"])

    docs = []
    for i in range(1, NUM_PRESENTACIONES + 1):
        dominio = random.choice(list(titulos))
        inicio = random.choice(dias_convencion) + timedelta(
            hours=random.randint(0, 8), minutes=random.choice([0, 30]))
        fin = inicio + timedelta(minutes=random.choice([30, 45, 60, 90]))
        pool = tags_por_dominio[dominio]
        docs.append({
            "_id": f"PRES_{i:04d}",
            "titulo": random.choice(titulos[dominio]),
            "dominio": dominio,
            "fecha": inicio.strftime("%d-%m-%Y"),
            "hora_inicio": inicio.strftime("%H:%M"),
            "hora_termino": fin.strftime("%H:%M"),
            "tags": random.sample(pool, min(2, len(pool))),
            "lugar": random.choice(lugares),
        })

    db.presentaciones.delete_many({})
    db.presentaciones.insert_many(docs)
    print(f"-> {db.presentaciones.count_documents({})} presentaciones en MongoDB.")
    print("Ejemplo:", docs[0])


if __name__ == "__main__":
    crear_presentaciones()
