from repository import JsonRepository
from service import RequestService

def main():
    repo = JsonRepository("datos.json")
    service = RequestService(repo)

    while True:
        print("\n=== SISTEMA DE GESTIÓN ACADÉMICA ===")
        print("1 Registrar estudiante")
        print("2 Registrar responsable")
        print("3 Registrar solicitud")
        print("4 Cambiar estado")
        print("5 Asignar responsable")
        print("6 Buscar")
        print("7 Reporte")
        print("0 Salir")
        
        o = input("> ")
        if o == "1":
            try:
                i = int(input("id: "))
                nom = input("nombre: ")
                mail = input("mail: ")
                print(service.registrar_estudiante(i, nom, mail))
            except ValueError:
                print("Error: ID inválido.")
        elif o == "2":
            try:
                i = int(input("id: "))
                nom = input("nombre: ")
                area = input("area: ")
                print(service.registrar_responsable(i, nom, area))
            except ValueError:
                print("Error: ID inválido.")
        elif o == "3":
            try:
                e = int(input("id estudiante: "))
                t = int(input("tipo (1 constancia, 2 cambio materia, 3 examen): "))
                p = int(input("prioridad (1 baja, 2 media, 3 alta): "))
                desc = input("descripcion: ")
                r = int(input("id responsable (0 ninguno): "))
                print(service.registrar_solicitud(e, t, p, desc, r))
            except ValueError:
                print("Error: Valores numéricos inválidos.")
        elif o == "4":
            try:
                i = int(input("id solicitud: "))
                ne = int(input("nuevo estado (0 pend, 1 proc, 2 res, 3 rech): "))
                print(service.cambiar_estado(i, ne))
            except ValueError:
                print("Error: Valores numéricos inválidos.")
        elif o == "5":
            try:
                i = int(input("id solicitud: "))
                r = int(input("id responsable: "))
                print(service.asignar_responsable(i, r))
            except ValueError:
                print("Error: Valores numéricos inválidos.")
        elif o == "6":
            try:
                m = int(input("buscar por (1 estado, 2 tipo, 3 prioridad): "))
                v = int(input("valor: "))
                resultados, total = service.buscar(m, v)
                for x in resultados:
                    print(f"{x['id']} | {x['tipo']} | {x['estado']} | {x['descripcion']} | {x['fecha']}")
                print(f"Total: {total}")
            except ValueError:
                print("Error: Valores numéricos inválidos.")
        elif o == "7":
            rep = service.generar_reporte()
            print("=== REPORTE ===")
            print(f"Total solicitudes: {rep['total']}")
            print(f"Pendientes: {rep['pend']}")
            print(f"En proceso: {rep['proc']}")
            print(f"Resueltas: {rep['res']}")
            print(f"Rechazadas: {rep['rech']}")
            print(f"Prioridad alta: {rep['alta']}")
            print(f"Prioridad media: {rep['media']}")
            print(f"Prioridad baja: {rep['baja']}")
            print(f"Sin responsable: {rep['sin_resp']}")
        elif o == "0":
            break
        else:
            print("opcion invalida")

if __name__ == "__main__":
    main()