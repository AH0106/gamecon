import pandas as pd
import random
import faker

#configuración inicial
fake = faker.Faker('es_CL')  #genera nombres 
NUM_USUARIOS = 100     #asistentes a simular

#vocabulario controlado, se puede añadir mas si es necesario 
tags_validos = [
    "action", "adventure", "fantasy", "sci-fi", "horror", "mystery",
    "romance", "slice_of_life", "sports", "supernatural", "suspense",
    "isekai", "mecha", "psychological", "strategy", "role-playing",
    "shooter", "racing", "comedy", "drama"
]

datos = []
for i in range(1, NUM_USUARIOS + 1):
    #id s
    asistente_id = f"ASIS_{i:04d}"
    
    nombre = fake.name()
    
    #3 gustos unidos por coma para q se vea bien en un CSV
    gustos_aleatorios = random.sample(tags_validos, 3)
    gustos_declarados = ", ".join(gustos_aleatorios)
    
    datos.append({
        "asistente_id": asistente_id,
        "nombre": nombre,
        "gustos_declarados": gustos_declarados
    })

#guardar como CSV
df = pd.DataFrame(datos)

ruta_salida = "c:/Users/sofia/Desktop/intento dba/asistentes_simulados.csv"
df.to_csv(ruta_salida, index=False, encoding="utf-8")

print(f"¡Éxito! Se generaron {NUM_USUARIOS} asistentes en: {ruta_salida}")
print("\nVista previa de los datos:")
print(df.head())