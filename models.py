class Estudiante:
    def __init__(self, id_estudiante, nombre, mail):
        self.id = id_estudiante
        self.nombre = nombre
        self.mail = mail

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "mail": self.mail}


class Responsable:
    def __init__(self, id_responsable, nombre, area):
        self.id = id_responsable
        self.nombre = nombre
        self.area = area

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "area": self.area}


class Solicitud:
    def __init__(self, id_solicitud, id_estudiante, tipo, prioridad, descripcion, id_responsable=0, estado=0, fecha=""):
        self.id = id_solicitud
        self.id_estudiante = id_estudiante
        self.tipo = tipo  
        self.prioridad = prioridad 
        self.descripcion = descripcion
        self.id_responsable = id_responsable
        self.estado = estado  
        self.fecha = fecha

    def to_dict(self):
        return {
            "id": self.id,
            "est": self.id_estudiante,
            "t": self.tipo,
            "p": self.prioridad,
            "d": self.descripcion,
            "r": self.id_responsable,
            "e": self.estado,
            "f": self.fecha
        }