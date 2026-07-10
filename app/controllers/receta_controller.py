from app.services.receta_service import RecetaService

class RecetaController:
    def __init__(self):
        self.service = RecetaService()

    def registrar_receta(self, datos):
        return self.service.ejecutar_registrar_receta(datos)