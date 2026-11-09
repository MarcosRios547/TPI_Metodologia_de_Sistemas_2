import json
import os

class JsonRepository:
    def __init__(self, filename="datos.json"):
        self.filename = filename

    def cargar(self):
        if not os.path.exists(self.filename):
            return {"s": [], "e": [], "r": []}
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"s": [], "e": [], "r": []}

    def guardar(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)