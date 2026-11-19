from dataclasses import asdict, dataclass, field
from enum import IntEnum

SIN_RESPONSABLE = 0


class ErrorDeNegocio(Exception):
    """Se viola una regla del dominio: dato inválido, entidad inexistente o estado final."""


class TipoSolicitud(IntEnum):
    CONSTANCIA = 1
    CAMBIO_MATERIA = 2
    EXAMEN = 3

    @property
    def etiqueta(self) -> str:
        return {
            TipoSolicitud.CONSTANCIA: "Constancia",
            TipoSolicitud.CAMBIO_MATERIA: "Cambio de materia",
            TipoSolicitud.EXAMEN: "Examen",
        }[self]


class Prioridad(IntEnum):
    BAJA = 1
    MEDIA = 2
    ALTA = 3


class EstadoSolicitud(IntEnum):
    PENDIENTE = 0
    EN_PROCESO = 1
    RESUELTA = 2
    RECHAZADA = 3

    @property
    def etiqueta(self) -> str:
        return {
            EstadoSolicitud.PENDIENTE: "Pendiente",
            EstadoSolicitud.EN_PROCESO: "En proceso",
            EstadoSolicitud.RESUELTA: "Resuelta",
            EstadoSolicitud.RECHAZADA: "Rechazada",
        }[self]

    @property
    def es_final(self) -> bool:
        return self in (EstadoSolicitud.RESUELTA, EstadoSolicitud.RECHAZADA)


@dataclass
class Estudiante:
    id: int
    nombre: str
    mail: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, datos: dict) -> "Estudiante":
        return cls(**datos)


@dataclass
class Responsable:
    id: int
    nombre: str
    area: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, datos: dict) -> "Responsable":
        return cls(**datos)


@dataclass
class Solicitud:
    id: int
    id_estudiante: int
    tipo: TipoSolicitud
    prioridad: Prioridad
    descripcion: str
    fecha: str
    id_responsable: int = SIN_RESPONSABLE
    estado: EstadoSolicitud = EstadoSolicitud.PENDIENTE

    def tiene_responsable(self) -> bool:
        return self.id_responsable != SIN_RESPONSABLE

    def cambiar_estado(self, nuevo_estado: EstadoSolicitud) -> None:
        self._exigir_modificable()
        self.estado = nuevo_estado

    def asignar_responsable(self, id_responsable: int) -> None:
        self._exigir_modificable()
        self.id_responsable = id_responsable
        if self.estado == EstadoSolicitud.PENDIENTE:
            self.estado = EstadoSolicitud.EN_PROCESO

    def _exigir_modificable(self) -> None:
        if self.estado.es_final:
            raise ErrorDeNegocio(
                f"La solicitud {self.id} está {self.estado.etiqueta.lower()} "
                "y no puede modificarse."
            )

    def to_dict(self) -> dict:
        datos = asdict(self)
        datos["tipo"] = int(self.tipo)
        datos["prioridad"] = int(self.prioridad)
        datos["estado"] = int(self.estado)
        return datos

    @classmethod
    def from_dict(cls, datos: dict) -> "Solicitud":
        return cls(
            **{
                **datos,
                "tipo": TipoSolicitud(datos["tipo"]),
                "prioridad": Prioridad(datos["prioridad"]),
                "estado": EstadoSolicitud(datos["estado"]),
            }
        )


@dataclass
class Datos:
    estudiantes: list[Estudiante] = field(default_factory=list)
    responsables: list[Responsable] = field(default_factory=list)
    solicitudes: list[Solicitud] = field(default_factory=list)
