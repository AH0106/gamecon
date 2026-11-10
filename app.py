import os
import sys
from pathlib import Path
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno
RAIZ = Path(__file__).resolve().parent
load_dotenv(RAIZ / ".env")

DEFAULT_URI = "mongodb+srv://cristobalcastro1_db_user:1234@cluster0.towey3r.mongodb.net/GameCon?retryWrites=true&w=majority"
MONGO_URI = os.getenv("MONGO_URI", DEFAULT_URI)
MONGO_DB = os.getenv("MONGO_DB", "bdgamecon")

sys.path.append(str(RAIZ / "src"))
from recomendaciones import recomendar_stands, obtener_perfil_asistente

# Configuración de Streamlit
st.set_page_config(page_title="GAMECON · Buscador de Stands", page_icon="🎮", layout="wide")


@st.cache_resource
def get_db():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=4000)
    return client, client[MONGO_DB]


try:
    client, db = get_db()
    client.admin.command("ping")
    mongo_ok = True
except Exception as e:
    mongo_ok = False
    error_msg = str(e)


# --- BARRA LATERAL ---
st.sidebar.title("🎮 GAMECON 2026")
st.sidebar.caption("Buscador y Recomendador de Stands")

# Estado de MongoDB / Réplicas
if mongo_ok:
    st.sidebar.success(f"🟢 Conectado a `{MONGO_DB}`")
    nodos = list(client.nodes)
    if nodos:
        st.sidebar.caption(f"**Host Activo:** `{nodos[0][0]}`")
else:
    st.sidebar.error("🔴 Error de conexión a MongoDB")
    st.sidebar.code(error_msg)
    st.stop()

# Métricas del catálogo
total_stands = db.stands.count_documents({})
st.sidebar.metric("Total Stands en BD", f"{total_stands:,}")

# Obtener lista de todos los tags disponibles en la BD
tags_disponibles = sorted(t for t in db.stands.distinct("tags") if t)

# Modo de búsqueda
st.sidebar.divider()
modo = st.sidebar.radio("Modo de búsqueda:", ["🔍 Buscar por Tags", "👤 Recomendador por Asistente"])


# --- VISTA 1: BÚSQUEDA DIRECTA POR TAGS ---
if modo == "🔍 Buscar por Tags":
    st.title("🔍 Buscador de Stands por Tags")
    st.caption("Ingresa o selecciona tags de interés para encontrar stands en la feria.")

    # Barra de búsqueda con multiselect y texto libre
    default_tags = [t for t in ["action", "role-playing"] if t in tags_disponibles]
    tags_seleccionados = st.multiselect(
        "Elige uno o más tags:",
        options=tags_disponibles,
        default=default_tags
    )

    col_filtro, col_limite = st.columns([2, 1])
    with col_filtro:
        dominio_filtro = st.selectbox("Filtrar por dominio:", ["Todos", "Juegos", "Anime", "Comics/Manga"])
    with col_limite:
        top_k = st.slider("Resultados máximos:", min_value=5, max_value=30, value=10)

    if not tags_seleccionados:
        st.info("👆 Selecciona al menos un tag arriba para buscar stands.")
    else:
        # Pipeline de agregación en MongoDB
        match_query = {"tags": {"$in": tags_seleccionados}}
        if dominio_filtro == "Juegos":
            match_query["dominio"] = "juego"
        elif dominio_filtro == "Anime":
            match_query["dominio"] = "anime"
        elif dominio_filtro == "Comics/Manga":
            match_query["dominio"] = "manga_comic"

        pipeline = [
            {"$match": match_query},
            {"$project": {
                "nombre": 1,
                "dominio": 1,
                "ubicacion": 1,
                "tags": 1,
                "tags_coincidentes": {"$setIntersection": ["$tags", tags_seleccionados]},
                "coincidencias": {"$size": {"$setIntersection": ["$tags", tags_seleccionados]}}
            }},
            {"$sort": {"coincidencias": -1, "nombre": 1}},
            {"$limit": top_k}
        ]

        resultados = list(db.stands.aggregate(pipeline))

        st.subheader(f"Resultados encontrados ({len(resultados)})")

        if not resultados:
            st.warning("No hay stands que coincidan con esos tags y filtro.")
        else:
            for i, st_doc in enumerate(resultados, 1):
                dominio = st_doc.get("dominio", "General")
                icono = "🎮" if dominio == "juego" else ("⛩️" if dominio == "anime" else "📚")
                coincidencias = st_doc.get("coincidencias", 0)
                matched = st_doc.get("tags_coincidentes", [])
                todos_tags = st_doc.get("tags", [])

                with st.container():
                    st.markdown(f"### {i}. {icono} {st_doc['nombre']}")
                    st.write(f"📍 **{st_doc.get('ubicacion', 'Sin ubicación')}** · *Dominio:* {dominio.upper()} · **Coincidencias:** `{coincidencias}`")

                    # Mostrar tags resaltando los coincidentes
                    tags_html = " ".join([
                        f"**:green[`{t}`]**" if t in matched else f"`{t}`"
                        for t in todos_tags
                    ])
                    st.write("Tags del stand: " + tags_html)
                    st.divider()


# --- VISTA 2: RECOMENDADOR POR ASISTENTE ---
else:
    st.title("👤 Recomendador de Asistentes")

    asistentes_cursor = db.asistentes.find({}, {"_id": 1, "nombre": 1}).sort("nombre", 1)
    opciones_asistentes = {f"{a['nombre']} ({a['_id']})": a["_id"] for a in asistentes_cursor}

    sel_asistente = st.selectbox("Selecciona un Asistente:", list(opciones_asistentes.keys()))
    asistente_id = opciones_asistentes[sel_asistente]

    asistente = db.asistentes.find_one({"_id": asistente_id})
    if asistente:
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Intereses Declarados:**")
            st.write(" ".join([f"`{t}`" for t in asistente.get("intereses_declarados", [])]))
        with c2:
            st.write("**Intereses Deducidos:**")
            ded = asistente.get("intereses_deducidos", {})
            top_ded = sorted(ded.items(), key=lambda x: -x[1])[:8]
            st.write(" ".join([f"`{t} (+{p})`" for t, p in top_ded]) if ded else "*Sin interacciones*")

        st.divider()
        # Misma lógica que src/recomendaciones.py (perfil top-5 deducidos + ranking IDF)
        _, gustos = obtener_perfil_asistente(asistente_id)
        st.write("**Tags usados para recomendar:** " + " ".join(f"`{t}`" for t in gustos))

        recs = recomendar_stands(asistente_id, top_n=5) or []
        st.subheader("Top 5 Stands Recomendados:")
        for j, r in enumerate(recs, 1):
            dom = r.get("dominio", "General")
            ico = "🎮" if dom == "juego" else ("⛩️" if dom == "anime" else "📚")
            st.write(f"**{j}. {ico} {r['nombre']}** ({r.get('ubicacion')}) — "
                     f"Puntaje IDF: `{r['puntaje']:.2f}` · Coincidencias: `{r['coincidencias']}` "
                     f"({', '.join(r['tags_coincidentes'])})")
