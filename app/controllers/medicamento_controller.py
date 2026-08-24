from app.services.medicamento_service import MedicamentoService

class MedicamentoController:
    def __init__(self):
        self.service = MedicamentoService()

    def registrar_medicamento(self, datos):
        return self.service.ejecutar_registrar_medicamento(datos)
    
    def mostrar_medicamentos(self):
        return self.service.ejecutar_mostrar_medicamento()