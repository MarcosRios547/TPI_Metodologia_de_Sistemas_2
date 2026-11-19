from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum

from models import (
    SIN_RESPONSABLE,
    Datos,
    ErrorDeNegocio,
    Estudiante,
    EstadoSolicitud,
    Prioridad,
    Responsable,
    Solicitud,
    TipoSolicitud,
)
from repository import RepositorioDatos

FORMATO_FECHA = "%d/%m/%Y"
LARGO_MINIMO_DESCRIPCION = 5


class CampoBusqueda(IntEnum):
    ESTADO = 1
    TIPO = 2
    PRIORIDAD = 3


@dataclass(frozen=True)
class CriterioBusqueda:
    campo: CampoBusqueda
    valor: int


@dataclass(frozen=True)
class NuevaSolicitud:
    id_estudiante: int
    tipo: int
    prioridad: int
    descripcion: str
    id_responsable: int = SIN_RESPONSABLE


@dataclass(frozen=True)
class ReporteResumen:
    total: int
    por_estado: dict
    por_prioridad: dict
    sin_responsable: int


def _a_enum(clase, valor: int, nombre: str):
    try:
        return clase(valor)
    except ValueError as error:
        raise ErrorDeNegocio(f"Valor inválido para {nombre}: {valor}.") from error


def _exigir_existente(items: list, id_buscado: int, entidad: str) -> None:
    if not any(item.id == id_buscado for item in items):
        raise ErrorDeNegocio(f"No existe {entidad} con id {id_buscado}.")


def _exigir_inexistente(items: list, id_buscado: int, entidad: str) -> None:
    if any(item.id == id_buscado for item in items):
        raise ErrorDeNegocio(f"Ya existe {entidad} con id {id_buscado}.")


class RequestService:
    def __init__(self, repositorio: RepositorioDatos):
        self._repositorio = repositorio

    def registrar_estudiante(self, id_estudiante: int, nombre: str, mail: str) -> None:
        datos = self._repositorio.cargar()
        _exigir_inexistente(datos.estudiantes, id_estudiante, "un estudiante")
        datos.estudiantes.append(Estudiante(id_estudiante, nombre, mail))
        self._repositorio.guardar(datos)

    def registrar_responsable(self, id_responsable: int, nombre: str, area: str) -> None:
        datos = self._repositorio.cargar()
        _exigir_inexistente(datos.responsables, id_responsable, "un responsable")
        datos.responsables.append(Responsable(id_responsable, nombre, area))
        self._repositorio.guardar(datos)

    def registrar_solicitud(self, nueva: NuevaSolicitud) -> Solicitud:
        tipo = _a_enum(TipoSolicitud, nueva.tipo, "tipo")
        prioridad = _a_enum(Prioridad, nueva.prioridad, "prioridad")
        if len(nueva.descripcion) < LARGO_MINIMO_DESCRIPCION:
            raise ErrorDeNegocio(
                f"La descripción debe tener al menos {LARGO_MINIMO_DESCRIPCION} caracteres."
            )

        datos = self._repositorio.cargar()
        _exigir_existente(datos.estudiantes, nueva.id_estudiante, "un estudiante")
        if nueva.id_responsable != SIN_RESPONSABLE:
            _exigir_existente(datos.responsables, nueva.id_responsable, "un responsable")

        solicitud = Solicitud(
            id=self._siguiente_id(datos),
            id_estudiante=nueva.id_estudiante,
            tipo=tipo,
            prioridad=prioridad,
            descripcion=nueva.descripcion,
            fecha=datetime.now().strftime(FORMATO_FECHA),
            id_responsable=nueva.id_responsable,
        )
        datos.solicitudes.append(solicitud)
        self._repositorio.guardar(datos)
        return solicitud

    def cambiar_estado(self, id_solicitud: int, nuevo_estado: int) -> None:
        estado = _a_enum(EstadoSolicitud, nuevo_estado, "estado")
        datos = self._repositorio.cargar()
        self._obtener_solicitud(datos, id_solicitud).cambiar_estado(estado)
        self._repositorio.guardar(datos)

    def asignar_responsable(self, id_solicitud: int, id_responsable: int) -> None:
        datos = self._repositorio.cargar()
        _exigir_existente(datos.responsables, id_responsable, "un responsable")
        self._obtener_solicitud(datos, id_solicitud).asignar_responsable(id_responsable)
        self._repositorio.guardar(datos)

    def buscar(self, criterio: CriterioBusqueda) -> list[Solicitud]:
        valor_de = {
            CampoBusqueda.ESTADO: lambda s: s.estado,
            CampoBusqueda.TIPO: lambda s: s.tipo,
            CampoBusqueda.PRIORIDAD: lambda s: s.prioridad,
        }[criterio.campo]
        solicitudes = self._repositorio.cargar().solicitudes
        return [s for s in solicitudes if valor_de(s) == criterio.valor]

    def generar_reporte(self) -> ReporteResumen:
        solicitudes = self._repositorio.cargar().solicitudes
        por_estado = {estado: 0 for estado in EstadoSolicitud}
        por_prioridad = {prioridad: 0 for prioridad in Prioridad}
        for solicitud in solicitudes:
            por_estado[solicitud.estado] += 1
            por_prioridad[solicitud.prioridad] += 1
        sin_responsable = sum(
            1
            for s in solicitudes
            if not s.tiene_responsable() and s.estado != EstadoSolicitud.RECHAZADA
        )
        return ReporteResumen(len(solicitudes), por_estado, por_prioridad, sin_responsable)

    @staticmethod
    def _siguiente_id(datos: Datos) -> int:
        return max((s.id for s in datos.solicitudes), default=0) + 1

    @staticmethod
    def _obtener_solicitud(datos: Datos, id_solicitud: int) -> Solicitud:
        for solicitud in datos.solicitudes:
            if solicitud.id == id_solicitud:
                return solicitud
        raise ErrorDeNegocio(f"No existe una solicitud con id {id_solicitud}.")
