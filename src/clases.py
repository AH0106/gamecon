from typing import List, Dict, Optional
from bson import ObjectId

class Tag: 
    """Vocabulario controlado y tabla de mapeo (D2)"""
    def __init__(self, id_tag: str, nivel: str, origenes: List[str], frecuencia: int = 0):
        self._id = id_tag  # String normalizado
        self.nivel = nivel  # general o específico
        self.origenes = origenes  # Géneros originales mapeados
        self.frecuencia = frecuencia

    def to_dict(self) -> dict:
        return {
            "_id": self._id,
            "nivel": self.nivel,
            "origenes": self.origenes,
            "frecuencia": self.frecuencia
        }

class Stand: 
    """Representación de un Productor/Stand (D1)"""
    def __init__(self, nombre: str, dominio: str, ubicacion: str, tags: List[str], _id: Optional[ObjectId] = None):
        self._id = _id or ObjectId()
        self.nombre = nombre
        self.dominio = dominio  # juego, anime, manga_comic, musica
        self.ubicacion = ubicacion
        self.tags = tags

    def to_dict(self) -> dict:
        return {
            "_id": self._id,
            "nombre": self.nombre,
            "dominio": self.dominio,
            "ubicacion": self.ubicacion,
            "tags": self.tags
        }

class Presentacion: 
    """Eventos del escenario"""
    def __init__(self, titulo: str, inicio: str, fin: str, tags: List[str], stand_id: ObjectId, _id: Optional[ObjectId] = None):
        self._id = _id or ObjectId()
        self.titulo = titulo
        self.inicio = inicio
        self.fin = fin
        self.tags = tags
        self.stand_id = stand_id

    def to_dict(self) -> dict:
        return {
            "_id": self._id,
            "titulo": self.titulo,
            "inicio": self.inicio,
            "fin": self.fin,
            "tags": self.tags,
            "stand_id": self.stand_id
        }

class Asistente: 
    """Perfil del asistente (D3, D4)"""
    def __init__(self, nombre: str, intereses_declarados: List[str], intereses_deducidos: Optional[Dict[str, int]] = None, _id: Optional[ObjectId] = None):
        self._id = _id or ObjectId()
        self.nombre = nombre
        self.intereses_declarados = intereses_declarados[:8]  # Tope de 8 intereses declarados
        self.intereses_deducidos = intereses_deducidos or {}

    def to_dict(self) -> dict:
        return {
            "_id": self._id,
            "nombre": self.nombre,
            "intereses_declarados": self.intereses_declarados,
            "intereses_deducidos": self.intereses_deducidos
        }

class Interaccion: 
    """Registro de eventos/interacciones (D3)"""
    def __init__(self, asistente_id: ObjectId, objetivo_id: ObjectId, tipo: str, fecha: str, _id: Optional[ObjectId] = None):
        self._id = _id or ObjectId()
        self.asistente_id = asistente_id
        self.objetivo_id = objetivo_id
        self.tipo = tipo  # visita, asistencia, favorito
        self.fecha = fecha

    def to_dict(self) -> dict:
        return {
            "_id": self._id,
            "asistente_id": self.asistente_id,
            "objetivo_id": self.objetivo_id,
            "tipo": self.tipo,
            "fecha": self.fecha
        }
