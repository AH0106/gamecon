"""Simula visitas, favoritos y asistencias a charlas para poblar
la colección interacciones y los intereses_deducidos de cada asistente."""
import random
from perfil_deducido import db, registrar_interaccion
from recomendaciones import recomendar_stands

SEMILLA = 42
STANDS_POR_ASISTENTE = 4      # stands que visita, elegidos de su top-10 recomendado
TOP_CANDIDATOS = 10
PROB_FAVORITO = 0.3           # probabilidad de que la visita sea "favorito"
FECHAS = ["07-11-2026", "08-11-2026", "09-11-2026"]


def simular():
    random.seed(SEMILLA)

    # Idempotente: borrar interacciones previas y resetear perfiles deducidos
    db.interacciones.delete_many({})
    db.asistentes.update_many({}, {"$set": {"intereses_deducidos": {}}})

    total = 0
    for asis in db.asistentes.find({}, {"intereses_declarados": 1}):
        gustos = asis.get("intereses_declarados", [])
        if not gustos:
            continue

        # 1) Visita stands de su top-10 (calculado solo con sus gustos declarados,
        #    porque el perfil deducido parte vacío). Elegir al azar entre TODOS los
        #    stands afines sesga hacia los estudios gigantes con 60 tags.
        candidatos = recomendar_stands(asis["_id"], top_n=TOP_CANDIDATOS) or []
        stands = random.sample(candidatos, min(STANDS_POR_ASISTENTE, len(candidatos)))
        for s in stands:
            tipo = "favorito" if random.random() < PROB_FAVORITO else "visita"
            registrar_interaccion(asis["_id"], s["_id"], tipo, s["tags"], random.choice(FECHAS))
            total += 1

        # 2) Asiste a una charla afín, si existe
        charla = list(db.presentaciones.aggregate([
            {"$match": {"tags": {"$in": gustos}}},
            {"$sample": {"size": 1}},
        ]))
        if charla:
            c = charla[0]
            registrar_interaccion(asis["_id"], c["_id"], "asistencia", c["tags"], c["fecha"])
            total += 1

    con_perfil = db.asistentes.count_documents({"intereses_deducidos": {"$ne": {}}})
    print(f"-> {total} interacciones registradas "
          f"({db.interacciones.count_documents({})} en MongoDB).")
    print(f"-> {con_perfil} asistentes con intereses deducidos.")


if __name__ == "__main__":
    simular()
