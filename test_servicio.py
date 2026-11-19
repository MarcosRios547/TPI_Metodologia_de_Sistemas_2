import pytest

from models import ErrorDeNegocio, EstadoSolicitud
from repository import InMemoryRepository, JsonRepository
from service import CampoBusqueda, CriterioBusqueda, NuevaSolicitud, RequestService


def nueva(**cambios) -> NuevaSolicitud:
    base = dict(id_estudiante=1, tipo=1, prioridad=2, descripcion="Necesito una constancia")
    base.update(cambios)
    return NuevaSolicitud(**base)


@pytest.fixture
def servicio() -> RequestService:
    servicio = RequestService(InMemoryRepository())
    servicio.registrar_estudiante(1, "Ana Pérez", "ana@example.com")
    servicio.registrar_responsable(1, "Luis Gómez", "Alumnado")
    return servicio


def test_p1_registrar_estudiante_nuevo():
    servicio = RequestService(InMemoryRepository())
    servicio.registrar_estudiante(1, "Ana", "ana@example.com")


def test_p2_estudiante_duplicado(servicio):
    with pytest.raises(ErrorDeNegocio):
        servicio.registrar_estudiante(1, "Otra", "otra@example.com")


def test_p3_registrar_responsable_nuevo():
    servicio = RequestService(InMemoryRepository())
    servicio.registrar_responsable(1, "Luis", "Alumnado")


def test_p4_registrar_solicitud_valida(servicio):
    solicitud = servicio.registrar_solicitud(nueva())
    assert solicitud.id == 1
    assert solicitud.estado == EstadoSolicitud.PENDIENTE


def test_p5_tipo_invalido(servicio):
    with pytest.raises(ErrorDeNegocio):
        servicio.registrar_solicitud(nueva(tipo=5))


def test_p6_prioridad_invalida(servicio):
    with pytest.raises(ErrorDeNegocio):
        servicio.registrar_solicitud(nueva(prioridad=0))


def test_p7_estudiante_inexistente(servicio):
    with pytest.raises(ErrorDeNegocio):
        servicio.registrar_solicitud(nueva(id_estudiante=99))


def test_p8_descripcion_corta(servicio):
    with pytest.raises(ErrorDeNegocio):
        servicio.registrar_solicitud(nueva(descripcion="hola"))


def test_p9_cambiar_estado_pendiente_a_en_proceso(servicio):
    servicio.registrar_solicitud(nueva())
    servicio.cambiar_estado(1, EstadoSolicitud.EN_PROCESO)
    assert servicio.buscar(CriterioBusqueda(CampoBusqueda.ESTADO, 1))[0].id == 1


def test_p10_no_se_modifica_solicitud_resuelta(servicio):
    servicio.registrar_solicitud(nueva())
    servicio.cambiar_estado(1, EstadoSolicitud.RESUELTA)
    with pytest.raises(ErrorDeNegocio):
        servicio.cambiar_estado(1, EstadoSolicitud.EN_PROCESO)


def test_p11_asignar_responsable_pasa_a_en_proceso(servicio):
    servicio.registrar_solicitud(nueva())
    servicio.asignar_responsable(1, 1)
    solicitud = servicio.buscar(CriterioBusqueda(CampoBusqueda.ESTADO, 1))[0]
    assert solicitud.id_responsable == 1


def test_p12_responsable_inexistente(servicio):
    servicio.registrar_solicitud(nueva())
    with pytest.raises(ErrorDeNegocio):
        servicio.asignar_responsable(1, 99)


def test_p13_buscar_por_estado(servicio):
    servicio.registrar_solicitud(nueva())
    servicio.registrar_solicitud(nueva(tipo=2))
    resultados = servicio.buscar(CriterioBusqueda(CampoBusqueda.ESTADO, 0))
    assert len(resultados) == 2


def test_p14_reporte(servicio):
    servicio.registrar_solicitud(nueva(prioridad=3))
    servicio.registrar_solicitud(nueva(prioridad=1))
    servicio.registrar_solicitud(nueva(prioridad=2))
    servicio.cambiar_estado(2, EstadoSolicitud.RECHAZADA)
    servicio.asignar_responsable(3, 1)
    reporte = servicio.generar_reporte()
    assert reporte.total == 3
    assert reporte.por_estado[EstadoSolicitud.PENDIENTE] == 1
    assert reporte.por_estado[EstadoSolicitud.EN_PROCESO] == 1
    assert reporte.por_estado[EstadoSolicitud.RECHAZADA] == 1
    assert reporte.sin_responsable == 1


def test_p15_persistencia_en_json(tmp_path):
    ruta = str(tmp_path / "datos.json")
    primero = RequestService(JsonRepository(ruta))
    primero.registrar_estudiante(1, "Ana", "ana@example.com")
    primero.registrar_solicitud(nueva())
    segundo = RequestService(JsonRepository(ruta))
    assert len(segundo.buscar(CriterioBusqueda(CampoBusqueda.ESTADO, 0))) == 1


def test_registrar_con_responsable_queda_pendiente(servicio):
    """Regresión detectada: el original siempre registraba como Pendiente."""
    solicitud = servicio.registrar_solicitud(nueva(id_responsable=1))
    assert solicitud.estado == EstadoSolicitud.PENDIENTE
