import json, os, datetime, sys

# datos globales: s = solicitudes, e = estudiantes, r = responsables
d = {"s": [], "e": [], "r": []}
F = "datos.json"


def cargar():
    global d
    try:
        f = open(F)
        d = json.load(f)
    except:
        pass


def guardar():
    f = open(F, "w")
    json.dump(d, f)


# registra estudiante
def reg_est(i, nom, mail):
    for x in d["e"]:
        if x["id"] == i:
            return "ERROR"
    d["e"].append({"id": i, "nom": nom, "mail": mail})
    guardar()
    return "OK"


# registra responsable
def reg_resp(i, nom, area):
    for x in d["r"]:
        if x["id"] == i:
            return "ERROR"
    d["r"].append({"id": i, "nom": nom, "area": area})
    guardar()
    return "OK"


# registra una solicitud
# t: 1 constancia, 2 cambio de materia, 3 examen
# p: 1 baja, 2 media, 3 alta
# est: 0 pendiente, 1 en proceso, 2 resuelta, 3 rechazada
def reg(n, e, t, p, desc, r, est, f):
    if t != 1 and t != 2 and t != 3:
        return "ERROR"
    if p != 1 and p != 2 and p != 3:
        return "ERROR"
    if est < 0 or est > 3:
        return "ERROR"
    found = False
    for x in d["e"]:
        if x["id"] == e:
            found = True
    if found == False:
        return "ERROR"
    if r != 0:
        found2 = False
        for x in d["r"]:
            if x["id"] == r:
                found2 = True
        if found2 == False:
            return "ERROR"
    if len(desc) < 5:
        return "ERROR"
    d["s"].append({"id": n, "est": e, "t": t, "p": p, "d": desc, "r": r, "e": est, "f": f})
    guardar()
    return "OK"


def cambiar(i, ne):
    if ne < 0 or ne > 3:
        return "ERROR"
    for x in d["s"]:
        if x["id"] == i:
            if x["e"] == 2 or x["e"] == 3:
                return "ERROR"
            x["e"] = ne
            guardar()
            return "OK"
    return "ERROR"


def asignar(i, r):
    found = False
    for x in d["r"]:
        if x["id"] == r:
            found = True
    if found == False:
        return "ERROR"
    for x in d["s"]:
        if x["id"] == i:
            if x["e"] == 2 or x["e"] == 3:
                return "ERROR"
            x["r"] = r
            if x["e"] == 0:
                x["e"] = 1
            guardar()
            return "OK"
    return "ERROR"


# busca solicitudes e imprime resultado
def buscar(modo, v):
    c = 0
    for x in d["s"]:
        if modo == 1 and x["e"] == v:
            tn = ""
            if x["t"] == 1:
                tn = "Constancia"
            elif x["t"] == 2:
                tn = "Cambio de materia"
            elif x["t"] == 3:
                tn = "Examen"
            en = ""
            if x["e"] == 0:
                en = "Pendiente"
            elif x["e"] == 1:
                en = "En proceso"
            elif x["e"] == 2:
                en = "Resuelta"
            elif x["e"] == 3:
                en = "Rechazada"
            print(str(x["id"]) + " | " + tn + " | " + en + " | " + x["d"] + " | " + x["f"])
            c = c + 1
        if modo == 2 and x["t"] == v:
            tn = ""
            if x["t"] == 1:
                tn = "Constancia"
            elif x["t"] == 2:
                tn = "Cambio de materia"
            elif x["t"] == 3:
                tn = "Examen"
            en = ""
            if x["e"] == 0:
                en = "Pendiente"
            elif x["e"] == 1:
                en = "En proceso"
            elif x["e"] == 2:
                en = "Resuelta"
            elif x["e"] == 3:
                en = "Rechazada"
            print(str(x["id"]) + " | " + tn + " | " + en + " | " + x["d"] + " | " + x["f"])
            c = c + 1
        if modo == 3 and x["p"] == v:
            tn = ""
            if x["t"] == 1:
                tn = "Constancia"
            elif x["t"] == 2:
                tn = "Cambio de materia"
            elif x["t"] == 3:
                tn = "Examen"
            en = ""
            if x["e"] == 0:
                en = "Pendiente"
            elif x["e"] == 1:
                en = "En proceso"
            elif x["e"] == 2:
                en = "Resuelta"
            elif x["e"] == 3:
                en = "Rechazada"
            print(str(x["id"]) + " | " + tn + " | " + en + " | " + x["d"] + " | " + x["f"])
            c = c + 1
    print("Total: " + str(c))
    return c


def reporte():
    pend = 0
    proc = 0
    res = 0
    rech = 0
    alta = 0
    media = 0
    baja = 0
    for x in d["s"]:
        if x["e"] == 0:
            pend += 1
        if x["e"] == 1:
            proc += 1
        if x["e"] == 2:
            res += 1
        if x["e"] == 3:
            rech += 1
        if x["p"] == 3:
            alta += 1
        if x["p"] == 2:
            media += 1
        if x["p"] == 1:
            baja += 1
    print("=== REPORTE ===")
    print("Total solicitudes: " + str(len(d["s"])))
    print("Pendientes: " + str(pend))
    print("En proceso: " + str(proc))
    print("Resueltas: " + str(res))
    print("Rechazadas: " + str(rech))
    print("Prioridad alta: " + str(alta))
    print("Prioridad media: " + str(media))
    print("Prioridad baja: " + str(baja))
    sin = 0
    for x in d["s"]:
        if x["r"] == 0 and x["e"] != 3:
            sin = sin + 1
    print("Sin responsable: " + str(sin))
    f = open("reporte.txt", "w")
    f.write("Total: " + str(len(d["s"])) + " Pend: " + str(pend) + " Proc: " + str(proc) + " Res: " + str(res) + " Rech: " + str(rech))
    f.close()


# def calcular_demora(x):
#     return (datetime.datetime.now() - x["f"]).days


def viejo_exportar():
    # TODO: borrar, ya no se usa
    pass


def main():
    cargar()
    while True:
        print("")
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
            i = int(input("id: "))
            nom = input("nombre: ")
            mail = input("mail: ")
            print(reg_est(i, nom, mail))
        elif o == "2":
            i = int(input("id: "))
            nom = input("nombre: ")
            area = input("area: ")
            print(reg_resp(i, nom, area))
        elif o == "3":
            n = len(d["s"]) + 1
            e = int(input("id estudiante: "))
            t = int(input("tipo (1 constancia, 2 cambio materia, 3 examen): "))
            p = int(input("prioridad (1 baja, 2 media, 3 alta): "))
            desc = input("descripcion: ")
            r = int(input("id responsable (0 ninguno): "))
            f = datetime.datetime.now().strftime("%d/%m/%Y")
            print(reg(n, e, t, p, desc, r, 0, f))
        elif o == "4":
            i = int(input("id solicitud: "))
            ne = int(input("nuevo estado (0 pend, 1 proc, 2 res, 3 rech): "))
            print(cambiar(i, ne))
        elif o == "5":
            i = int(input("id solicitud: "))
            r = int(input("id responsable: "))
            print(asignar(i, r))
        elif o == "6":
            m = int(input("buscar por (1 estado, 2 tipo, 3 prioridad): "))
            v = int(input("valor: "))
            buscar(m, v)
        elif o == "7":
            reporte()
        elif o == "0":
            break
        else:
            print("opcion invalida")


main()