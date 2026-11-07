import json
import random
import os
from datetime import datetime, timedelta

NUM_PRESENTACIONES = 20  

#titulos 100% real no fake
titulos_juegos = [
    "El futuro del RPG japonés", "Speedrun: Cómo romper un juego en 20 minutos",
    "Diseño de niveles en plataformas 2D", "Historia de los videojuegos retro",
    "Competitivo: Estrategias de alto nivel", "Indies que cambiaron la industria",
    "Creando tu primer juego en Unity", "Los mejores juegos de 2026"
]

titulos_anime = [
    "Top 10 animes de la temporada", "Cómo se produce un anime",
    "De manga a anime: el proceso de adaptación", "Cosplay: guía para principiantes",
    "Los mejores villanos del anime", "Isekai: ¿por qué nos encantan?",
    "Animación 2D vs 3D", "Historia del anime en los 90s"
]

titulos_manga = [
    "Mangakas emergentes que debes conocer", "El arte del manga shojo",
    "Cómo publicar tu primer manga", "One Piece: análisis de 25 años",
    "Manga independiente vs editorial", "Técnicas de dibujo digital"
]

titulos_musica = [
    "Música en videojuegos: de 8-bits a orquestas", "Bandas sonoras icónicas",
    "Concierto: Tributo a los 2000s", "DJ Set: Anime Openings",
    "Composición para videojuegos indie"
]

tags_validos = [
    "action", "adventure", "fantasy", "sci-fi", "horror", "mystery",
    "romance", "slice_of_life", "sports", "supernatural", "suspense",
    "isekai", "mecha", "psychological", "strategy", "role-playing",
    "shooter", "racing", "comedy", "drama"
]

#zonas de la convencion
lugares = [
    "Zona 1 - Escenario Principal", "Zona 2 - Sala de Charlas",
    "Zona 3 - Auditorio Anime", "Zona 4 - Sala de Juegos",
    "Zona 5 - Área de Música", "Zona 6 - Taller Creativo",
    "Zona 7 - Sala de Cómics", "Zona 8 - Escenario Secundario"
]

#fechas de la supuesta convencion 
dias_convencion = [
    datetime(2026, 11, 7, 10, 0),   # Sábado 7 Nov - Día 1
    datetime(2026, 11, 8, 10, 0),   # Domingo 8 Nov - Día 2
    datetime(2026, 11, 9, 10, 0),   # Lunes 9 Nov - Día 3
]

#generar las presentaciones
presentaciones = []

for i in range(1, NUM_PRESENTACIONES + 1):
    # Elegir dominio al azar
    dominio = random.choice(["juegos", "anime", "manga", "musica"])
    
    # Elegir título según dominio
    if dominio == "juegos":
        titulo = random.choice(titulos_juegos)
    elif dominio == "anime":
        titulo = random.choice(titulos_anime)
    elif dominio == "manga":
        titulo = random.choice(titulos_manga)
    else:
        titulo = random.choice(titulos_musica)
    
    # Generar día y hora aleatoria (entre 10:00 y 18:00)
    dia_base = random.choice(dias_convencion)
    hora_inicio = dia_base + timedelta(hours=random.randint(0, 8), minutes=random.choice([0, 30]))
    duracion_minutos = random.choice([30, 45, 60, 90])  # Duración típica de charlas
    hora_termino = hora_inicio + timedelta(minutes=duracion_minutos)
    
    # Elegir EXACTAMENTE 2 tags únicos
    tags_elegidos = random.sample(tags_validos, 2)
    
    # Elegir lugar
    lugar = random.choice(lugares)
    
    # Armar el documento con la estructura de MongoDB
    documento = {
        "_id": f"PRES_{i:04d}",  # ID legible (ej: PRES_0001)
        "titulo": titulo,
        "dominio": dominio,
        "fecha": hora_inicio.strftime("%d-%m-%Y"),  # Ej: "07-11-2026"
        "hora_inicio": hora_inicio.strftime("%H:%M"),  # Ej: "13:30"
        "hora_termino": hora_termino.strftime("%H:%M"),  # Ej: "15:00"
        "tags": tags_elegidos,
        "lugar": lugar
    }
    
    presentaciones.append(documento)




# 6. Guardar como JSON
ruta_salida = "presentaciones.json"
ruta_absoluta = os.path.abspath(ruta_salida)
print(f"📂 El archivo se está guardando en esta ruta exacta: {ruta_absoluta}")
with open(ruta_salida, mode='w', encoding='utf-8') as archivo:
    json.dump(presentaciones, archivo, indent=4, ensure_ascii=False)

print(f"✅ ¡Listo! Se generaron {NUM_PRESENTACIONES} presentaciones en '{ruta_salida}'")
print(f"\n📅 Fechas de la convención: 7, 8 y 9 de Noviembre 2026")
print(f"🎤 Dominios incluidos: juegos, anime, manga, música")
print(f"🏷️ Tags usados: {len(tags_validos)} del vocabulario controlado")

# Mostrar un ejemplo
print("\n📄 Ejemplo de documento generado:")
print(json.dumps(presentaciones[0], indent=4, ensure_ascii=False))

import os # (Asegúrate de que 'import os' esté al principio de tu script)

# ... (todo tu código de generación) ...


