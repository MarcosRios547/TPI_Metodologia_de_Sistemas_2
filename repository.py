import copy
import json
from typing import Protocol

from models import Datos, Estudiante, Responsable, Solicitud


class ErrorDeAlmacenamiento(Exception):
    """No se pudo leer o escribir el medio de persistencia."""


class RepositorioDatos(Protocol):
    """Contrato mínimo que necesita el servicio (ISP); cualquier implementación lo cumple (LSP)."""

    def cargar(self) -> Datos: ...

    def guardar(self, datos: Datos) -> None: ...


class JsonRepository:
    def __init__(self, ruta: str = "datos.json"):
        self._ruta = ruta

    def cargar(self) -> Datos:
        try:
            with open(self._ruta, encoding="utf-8") as archivo:
                crudo = json.load(archivo)
        except FileNotFoundError:
            return Datos()
        except (OSError, json.JSONDecodeError) as error:
            raise ErrorDeAlmacenamiento(f"No se pudo leer {self._ruta}: {error}") from error
        return Datos(
            estudiantes=[Estudiante.from_dict(x) for x in crudo.get("estudiantes", [])],
            responsables=[Responsable.from_dict(x) for x in crudo.get("responsables", [])],
            solicitudes=[Solicitud.from_dict(x) for x in crudo.get("solicitudes", [])],
        )

    def guardar(self, datos: Datos) -> None:
        crudo = {
            "estudiantes": [x.to_dict() for x in datos.estudiantes],
            "responsables": [x.to_dict() for x in datos.responsables],
            "solicitudes": [x.to_dict() for x in datos.solicitudes],
        }
        try:
            with open(self._ruta, "w", encoding="utf-8") as archivo:
                json.dump(crudo, archivo, indent=4, ensure_ascii=False)
        except OSError as error:
            raise ErrorDeAlmacenamiento(f"No se pudo escribir {self._ruta}: {error}") from error


class InMemoryRepository:
    """Implementación sustituible para pruebas, sin tocar el disco."""

    def __init__(self):
        self._datos = Datos()

    def cargar(self) -> Datos:
        return copy.deepcopy(self._datos)

    def guardar(self, datos: Datos) -> None:
        self._datos = copy.deepcopy(datos)
