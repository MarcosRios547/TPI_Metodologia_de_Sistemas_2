import datetime

class RequestService:
    def __init__(self, repository):
        self.repository = repository

    def registrar_estudiante(self, id_est, nombre, mail):
        datos = self.repository.cargar()
        for x in datos["e"]:
            if x["id"] == id_est:
                return "ERROR"
        datos["e"].append({"id": id_est, "nombre": nombre, "mail": mail})
        self.repository.guardar(datos)
        return "OK"

    def registrar_responsable(self, id_resp, nombre, area):
        datos = self.repository.cargar()
        for x in datos["r"]:
            if x["id"] == id_resp:
                return "ERROR"
        datos["r"].append({"id": id_resp, "nombre": nombre, "area": area})
        self.repository.guardar(datos)
        return "OK"

    def registrar_solicitud(self, id_est, tipo, prioridad, descripcion, id_responsable=0):
        if tipo not in [1, 2, 3] or prioridad not in [1, 2, 3]:
            return "ERROR"
        if len(descripcion) < 5:
            return "ERROR"
        
        datos = self.repository.cargar()
        
        found_est = any(x["id"] == id_est for x in datos["e"])
        if not found_est:
            return "ERROR"
        
        if id_responsable != 0:
            found_resp = any(x["id"] == id_responsable for x in datos["r"])
            if not found_resp:
                return "ERROR"

        id_sol = len(datos["s"]) + 1
        fecha = datetime.datetime.now().strftime("%d/%m/%Y")
        estado = 1 if id_responsable != 0 else 0

        nueva_sol = {
            "id": id_sol,
            "est": id_est,
            "t": tipo,
            "p": prioridad,
            "d": descripcion,
            "r": id_responsable,
            "e": estado,
            "f": fecha
        }
        datos["s"].append(nueva_sol)
        self.repository.guardar(datos)
        return "OK"

    def cambiar_estado(self, id_sol, nuevo_estado):
        if nuevo_estado not in [0, 1, 2, 3]:
            return "ERROR"
        datos = self.repository.cargar()
        for x in datos["s"]:
            if x["id"] == id_sol:
                if x["e"] in [2, 3]:
                    return "ERROR"
                x["e"] = nuevo_estado
                self.repository.guardar(datos)
                return "OK"
        return "ERROR"

    def asignar_responsable(self, id_sol, id_resp):
        datos = self.repository.cargar()
        found_resp = any(x["id"] == id_resp for x in datos["r"])
        if not found_resp:
            return "ERROR"
        
        for x in datos["s"]:
            if x["id"] == id_sol:
                if x["e"] in [2, 3]:
                    return "ERROR"
                x["r"] = id_resp
                if x["e"] == 0:
                    x["e"] = 1
                self.repository.guardar(datos)
                return "OK"
        return "ERROR"

    def buscar(self, modo, valor):
        datos = self.repository.cargar()
        resultados = []
        c = 0
        for x in datos["s"]:
            match = False
            if modo == 1 and x["e"] == valor:
                match = True
            elif modo == 2 and x["t"] == valor:
                match = True
            elif modo == 3 and x["p"] == valor:
                match = True

            if match:
                tipo_nombre = {1: "Constancia", 2: "Cambio de materia", 3: "Examen"}.get(x["t"], "")
                estado_nombre = {0: "Pendiente", 1: "En proceso", 2: "Resuelta", 3: "Rechazada"}.get(x["e"], "")
                resultados.append({
                    "id": x["id"],
                    "tipo": tipo_nombre,
                    "estado": estado_nombre,
                    "descripcion": x["d"],
                    "fecha": x["f"]
                })
                c += 1
        return resultados, c

    def generar_reporte(self):
        datos = self.repository.cargar()
        solicitudes = datos["s"]
        total = len(solicitudes)
        pend = sum(1 for x in solicitudes if x["e"] == 0)
        proc = sum(1 for x in solicitudes if x["e"] == 1)
        res = sum(1 for x in solicitudes if x["e"] == 2)
        rech = sum(1 for x in solicitudes if x["e"] == 3)
        alta = sum(1 for x in solicitudes if x["p"] == 3)
        media = sum(1 for x in solicitudes if x["p"] == 2)
        baja = sum(1 for x in solicitudes if x["p"] == 1)
        sin_resp = sum(1 for x in solicitudes if x["r"] == 0 and x["e"] != 3)

        try:
            with open("reporte.txt", "w", encoding="utf-8") as f:
                f.write(f"Total: {total} Pend: {pend} Proc: {proc} Res: {res} Rech: {rech}")
        except Exception:
            pass

        return {
            "total": total,
            "pend": pend,
            "proc": proc,
            "res": res,
            "rech": rech,
            "alta": alta,
            "media": media,
            "baja": baja,
            "sin_resp": sin_resp
        }