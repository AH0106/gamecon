from pymongo import database_shared

import limpieza as limp


class tags: 
    """Vocabulario controlado y tabla de mapeo"""
    def __init__(self, id, nivel, origin, frecuency) -> None:
        self.id = id
        self.nivel = nivel
        self.origin = origin
        self.frecuency = frecuency

    def agregar_tag(self, dataset):
        """Funcion para agregar tags desde los generos del dataset"""


class stand: 
    """Clase generadora de stands"""
    def __init__(self, id, name, ubication, tags ) -> None:
        self.id = id
        self.name = name
        self.ubication = ubication
        self.tags = tags

    def agregar_stand(self, dataset): 
        """Funcion para agregar stands desde un dataset"""
        for index, column in dataset['productor']:
            stand= {
                'id': index,
                'name': dataset['name'],
                'generos': dataset['genero']
            }
        


class presentacion: 
    """Presentaciones"""
    def __init__(self, id, titulo, inicio, fin, tags, stand_id) -> None:
        self.id = id
        self.titulo = titulo
        self.inicio = inicio
        self.fin = fin
        self.tags = tags
        self.stand_id = stand_id

class asistentes: 
    def __init__(self, id, name, intereses_declarados, intereses_deducidos) -> None:
        """Representacion de asistentes a la convencion"""
        self.id = id
        self.name = name 
        self.intereses_declarados = intereses_declarados
        self.intereses_deducidos = intereses_deducidos

class interacciones: 
    """Clase para representar las interacciones"""
    def __init__(self, id, asistente_id, objetivo_id, tipo, fecha) -> None:
        self.id = id
        self.asistente_id = asistente_id
        self.objetivo_id = objetivo_id
        self.tipo = tipo
        self.fecha = fecha
