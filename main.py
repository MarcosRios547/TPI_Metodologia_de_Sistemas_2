from models import EstadoSolicitud, ErrorDeNegocio, Prioridad
from repository import ErrorDeAlmacenamiento, JsonRepository
from service import CampoBusqueda, CriterioBusqueda, NuevaSolicitud, RequestService

ARCHIVO_REPORTE = "reporte.txt"

ETIQUETA_ESTADO_REPORTE = {
    EstadoSolicitud.PENDIENTE: "Pendientes",
    EstadoSolicitud.EN_PROCESO: "En proceso",
    EstadoSolicitud.RESUELTA: "Resueltas",
    EstadoSolicitud.RECHAZADA: "Rechazadas",
}
ETIQUETA_PRIORIDAD_REPORTE = {
    Prioridad.ALTA: "Prioridad alta",
    Prioridad.MEDIA: "Prioridad media",
    Prioridad.BAJA: "Prioridad baja",
}


def pedir_entero(mensaje: str) -> int:
    return int(input(mensaje))


def registrar_estudiante(servicio: RequestService) -> None:
    id_estudiante = pedir_entero("id: ")
    nombre = input("nombre: ")
    mail = input("mail: ")
    servicio.registrar_estudiante(id_estudiante, nombre, mail)
    print("OK")


def registrar_responsable(servicio: RequestService) -> None:
    id_responsable = pedir_entero("id: ")
    nombre = input("nombre: ")
    area = input("area: ")
    servicio.registrar_responsable(id_responsable, nombre, area)
    print("OK")


def registrar_solicitud(servicio: RequestService) -> None:
    nueva = NuevaSolicitud(
        id_estudiante=pedir_entero("id estudiante: "),
        tipo=pedir_entero("tipo (1 constancia, 2 cambio materia, 3 examen): "),
        prioridad=pedir_entero("prioridad (1 baja, 2 media, 3 alta): "),
        descripcion=input("descripcion: "),
        id_responsable=pedir_entero("id responsable (0 ninguno): "),
    )
    servicio.registrar_solicitud(nueva)
    print("OK")


def cambiar_estado(servicio: RequestService) -> None:
    id_solicitud = pedir_entero("id solicitud: ")
    nuevo_estado = pedir_entero("nuevo estado (0 pend, 1 proc, 2 res, 3 rech): ")
    servicio.cambiar_estado(id_solicitud, nuevo_estado)
    print("OK")


def asignar_responsable(servicio: RequestService) -> None:
    id_solicitud = pedir_entero("id solicitud: ")
    id_responsable = pedir_entero("id responsable: ")
    servicio.asignar_responsable(id_solicitud, id_responsable)
    print("OK")


def buscar(servicio: RequestService) -> None:
    campo = pedir_entero("buscar por (1 estado, 2 tipo, 3 prioridad): ")
    valor = pedir_entero("valor: ")
    try:
        criterio = CriterioBusqueda(CampoBusqueda(campo), valor)
    except ValueError as error:
        raise ErrorDeNegocio(f"Criterio de búsqueda inválido: {campo}.") from error
    resultados = servicio.buscar(criterio)
    for s in resultados:
        print(f"{s.id} | {s.tipo.etiqueta} | {s.estado.etiqueta} | {s.descripcion} | {s.fecha}")
    print(f"Total: {len(resultados)}")


def reporte(servicio: RequestService) -> None:
    resumen = servicio.generar_reporte()
    print("=== REPORTE ===")
    print(f"Total solicitudes: {resumen.total}")
    for estado, etiqueta in ETIQUETA_ESTADO_REPORTE.items():
        print(f"{etiqueta}: {resumen.por_estado[estado]}")
    for prioridad, etiqueta in ETIQUETA_PRIORIDAD_REPORTE.items():
        print(f"{etiqueta}: {resumen.por_prioridad[prioridad]}")
    print(f"Sin responsable: {resumen.sin_responsable}")
    exportar_reporte_txt(resumen)


def exportar_reporte_txt(resumen) -> None:
    linea = (
        f"Total: {resumen.total} "
        f"Pend: {resumen.por_estado[EstadoSolicitud.PENDIENTE]} "
        f"Proc: {resumen.por_estado[EstadoSolicitud.EN_PROCESO]} "
        f"Res: {resumen.por_estado[EstadoSolicitud.RESUELTA]} "
        f"Rech: {resumen.por_estado[EstadoSolicitud.RECHAZADA]}"
    )
    try:
        with open(ARCHIVO_REPORTE, "w", encoding="utf-8") as archivo:
            archivo.write(linea)
    except OSError as error:
        print(f"Aviso: no se pudo escribir {ARCHIVO_REPORTE}: {error}")


ACCIONES = {
    "1": registrar_estudiante,
    "2": registrar_responsable,
    "3": registrar_solicitud,
    "4": cambiar_estado,
    "5": asignar_responsable,
    "6": buscar,
    "7": reporte,
}


def mostrar_menu() -> None:
    print("\n=== SISTEMA DE GESTIÓN ACADÉMICA ===")
    print("1 Registrar estudiante")
    print("2 Registrar responsable")
    print("3 Registrar solicitud")
    print("4 Cambiar estado")
    print("5 Asignar responsable")
    print("6 Buscar")
    print("7 Reporte")
    print("0 Salir")


def ejecutar(accion, servicio: RequestService) -> None:
    try:
        accion(servicio)
    except ValueError:
        print("Error: se esperaba un valor numérico.")
    except ErrorDeNegocio as error:
        print(f"ERROR: {error}")
    except ErrorDeAlmacenamiento as error:
        print(f"ERROR de almacenamiento: {error}")


def main() -> None:
    servicio = RequestService(JsonRepository("datos.json"))
    while True:
        mostrar_menu()
        opcion = input("> ")
        if opcion == "0":
            break
        accion = ACCIONES.get(opcion)
        if accion is None:
            print("opcion invalida")
            continue
        ejecutar(accion, servicio)


if __name__ == "__main__":
    main()
